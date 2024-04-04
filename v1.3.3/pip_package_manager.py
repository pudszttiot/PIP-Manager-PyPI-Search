import os
import subprocess
import sys
from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QTextOption
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

class WorkerThread(QThread):
    operation_completed = pyqtSignal(str)
    progress_updated = pyqtSignal(int)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            process = subprocess.Popen(self.command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

            while process.poll() is None:
                line = process.stderr.readline().strip()
                if line:
                    try:
                        progress = int(line)
                        self.progress_updated.emit(progress)
                    except ValueError:
                        pass

            result = process.communicate()[0]
            self.operation_completed.emit(result.decode("utf-8"))
        except Exception as e:
            self.operation_completed.emit(str(e))


class ConvertOutdatedThread(QThread):
    operation_completed = pyqtSignal(str)
    progress_updated = pyqtSignal(int)

    def run(self):
        try:
            with open('outdated.txt', 'r') as infile:
                lines = infile.readlines()[2:]

            total_lines = len(lines)
            processed_lines = 0

            converted_lines = []
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        package_name = parts[0]
                        latest_version = parts[2]
                        converted_lines.append(f"{package_name}=={latest_version}")

                processed_lines += 1
                progress = processed_lines * 100 // total_lines
                self.progress_updated.emit(progress)

            with open('outdated_freeze.txt', 'w') as outfile:
                outfile.write('\n'.join(converted_lines))

            result = "Conversion completed. Output saved to 'outdated_freeze.txt'"
            self.operation_completed.emit(result)
        except Exception as e:
            self.operation_completed.emit(str(e))


class PipPackageManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PIP Manager + PyPI Search")
        self.setGeometry(550, 250, 800, 600)
        self.setStyleSheet("background-color: #006dad;")
        self.setWindowIcon(QIcon(os.path.abspath(r"../Images/PyPI3resized.ico")))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout()

        package_layout = QHBoxLayout()
        package_layout.addWidget(QLabel("Package Name:", self, styleSheet="color: #ffffff;"))
        self.package_var = QLineEdit(self)
        self.package_var.setStyleSheet("background-color: #ffffff; color: #000000;")
        package_layout.addWidget(self.package_var)
        layout.addLayout(package_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.create_button("Install", self.install_package, r"../Images/install.png"))
        buttons_layout.addWidget(self.create_button("Uninstall", self.uninstall_package, r"../Images/uninstall.png"))
        buttons_layout.addWidget(self.create_button("Update➖Upgrade", self.upgrade_package, r"../Images/upgrade.png"))
        layout.addLayout(buttons_layout)

        for button_info in [("List Installed Packages", self.list_packages, r"../Images/checklist.png"),
                            ("Check Outdated Packages", self.check_outdated_packages, r"../Images/outdated2.png"),
                            ("Package Info", self.show_package_info, r"../Images/box2.png"),
                            ("Create .txt File for Outdated Packages (outdated.txt)", self.output_outdated_to_requirements, r"../Images/text.png"),
                            ("Create .txt File for Installed Packages (installed.txt)", self.output_installed_to_requirements, r"../Images/text.png")]:
            layout.addWidget(self.create_button(*button_info))

        self.status_label = QLabel(self)
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        self.progressbar = QProgressBar(self)
        self.progressbar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #006dad;
                border-radius: 5px;
                background-color: #ffffff;
                text-align: center;
                color: #006dad;
            }
            QProgressBar::chunk {
                background-color: #39FF14;
                width: 20px;
                margin: 1px;
            }
            QProgressBar::chunk:disabled {
                background-color: #cccccc;
            }
            QProgressBar::chunk:active {
                background-color: #39FF14;
            }
        """)
        layout.addWidget(self.progressbar)
        self.progressbar.hide()

        layout.addWidget(QLabel("Results:", self, styleSheet="color: #ffffff;"))
        self.result_text = QTextEdit(self)
        self.result_text.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.result_text.setWordWrapMode(QTextOption.WrapAnywhere)
        layout.addWidget(self.result_text)

        layout.addWidget(self.create_button("Clear", self.clear_result, r"../Images/clean4.png", alignment=Qt.AlignCenter))

        self.central_widget.setLayout(layout)

    def create_button(self, text, slot, icon_path=None, alignment=None):
        button = QPushButton(text, self)
        button.clicked.connect(slot)
        if icon_path:
            button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(30, 30))
        button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                border: 2px solid #000000;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

        return button

    def execute_command_with_loading(self, command):
        self.progressbar.setValue(0)
        self.progressbar.show()
        self.progressbar.setFormat("")

        self.progress_thread = WorkerThread(command)
        self.progress_thread.operation_completed.connect(self.show_result)
        self.progress_thread.progress_updated.connect(self.progressbar.setValue)
        self.progress_thread.start()

        self.progressbar.setRange(0, 0)
        self.set_buttons_enabled(False)
        self.status_label.setStyleSheet("color: #00FF00;")
        self.status_label.setText("Processing...")

    def set_buttons_enabled(self, enabled):
        for child in self.findChildren(QPushButton):
            child.setEnabled(enabled)

    def install_package(self):
        package_names = self.package_var.text().split(",")
        package_names = [pkg.strip() for pkg in package_names]
        if package_names:
            self.status_label.setText(f"Installing {', '.join(package_names)}...")
            command = f"pip install {' '.join(package_names)}"
            self.execute_command_with_loading(command)

    def uninstall_package(self):
        package_names = self.package_var.text().split(",")
        package_names = [pkg.strip() for pkg in package_names]
        if package_names:
            self.status_label.setText(f"Uninstalling {', '.join(package_names)}...")
            command = f"pip uninstall -y {' '.join(package_names)}"
            self.execute_command_with_loading(command)

    def upgrade_package(self):
        package_names = self.package_var.text().split(",")
        package_names = [pkg.strip() for pkg in package_names]
        if package_names:
            self.status_label.setText(f"Upgrading {', '.join(package_names)}...")
            command = f"pip install --upgrade {' '.join(package_names)}"
            self.execute_command_with_loading(command)

    def list_packages(self):
        self.status_label.setText("Listing Installed Packages...")
        command = "pip list"
        self.execute_command_with_loading(command)

    def check_outdated_packages(self):
        self.status_label.setText("Checking Outdated Packages...")
        command = "pip list --outdated"
        self.execute_command_with_loading(command)

    def show_package_info(self):
        package_name = self.package_var.text()
        if package_name:
            self.status_label.setText(f"Fetching Info for {package_name}...")
            command = f"pip show {package_name}"
            self.execute_command_with_loading(command)

    def output_outdated_to_requirements(self):
        self.status_label.setText("Outputting outdated packages to File (outdated.txt)...")
        command = "pip list --outdated --format columns > outdated.txt"
        try:
            subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            self.convert_outdated_thread = ConvertOutdatedThread()
            self.convert_outdated_thread.operation_completed.connect(self.show_result)
            self.convert_outdated_thread.progress_updated.connect(self.progressbar.setValue)
            self.convert_outdated_thread.start()
        except subprocess.CalledProcessError as e:
            self.show_result(e.output.decode("utf-8"))
        except Exception as e:
            self.show_result(str(e))
            self.execute_command_with_loading(command)

    def output_installed_to_requirements(self):
        self.status_label.setText("Outputting installed packages to File (installed.txt)...")
        command = "pip freeze > installed.txt"
        self.execute_command_with_loading(command)

    def show_result(self, result):
        self.result_text.clear()
        self.result_text.insertPlainText(result)
        self.status_label.setStyleSheet("color: #FFFF00;")
        self.status_label.setText("Operation completed.")
        self.progressbar.setRange(0, 1)
        self.progressbar.setValue(1)
        self.set_buttons_enabled(True)
        self.progressbar.hide()

    def clear_result(self):
        self.result_text.clear()
        self.status_label.clear()
        self.progressbar.setRange(0, 1)
        self.progressbar.setValue(1)
        self.set_buttons_enabled(True)
        self.progressbar.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PipPackageManagerApp()
    ex.show()
    sys.exit(app.exec_())
