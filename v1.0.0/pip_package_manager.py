import sys
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QProgressBar,
    QVBoxLayout,
    QWidget,
    QMessageBox,
)
from PyQt5.QtGui import QIcon, QFont, QPixmap, QTextOption
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QSize
import subprocess
from os import path


class WorkerThread(QThread):
    operation_completed = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            result = subprocess.check_output(
                self.command, shell=True, stderr=subprocess.STDOUT
            )
            self.operation_completed.emit(result.decode("utf-8"))
        except subprocess.CalledProcessError as e:
            self.operation_completed.emit(e.output.decode("utf-8"))


class PipPackageManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PIP Manager + PyPI Search")
        self.setGeometry(550, 250, 800, 600)
        self.setStyleSheet("background-color: #006dad;")  # Change background color here
        icon_path = path.join(path.dirname(__file__), "images", "PyPI3resized.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout()

        package_layout = QHBoxLayout()
        package_layout.addWidget(
            QLabel("Package Name:", self, styleSheet="color: #ffffff;")
        )  # Adjust label text color here
        self.package_var = QLineEdit(self)
        self.package_var.setStyleSheet(
            "background-color: #ffffff; color: #000000;"
        )  # Change QLineEdit color
        package_layout.addWidget(self.package_var)
        layout.addLayout(package_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(
            self.create_button("Install", self.install_package, "install.png")
        )
        buttons_layout.addWidget(
            self.create_button("Uninstall", self.uninstall_package, "uninstall.png")
        )
        buttons_layout.addWidget(
            self.create_button("Upgrade Package", self.upgrade_package, "upgrade.png")
        )
        layout.addLayout(buttons_layout)

        layout.addWidget(
            self.create_button(
                "List Installed Packages", self.list_packages, "list.png"
            )
        )
        layout.addWidget(
            self.create_button(
                "Check Outdated Packages", self.check_outdated_packages, "outdated.png"
            )
        )
        layout.addWidget(
            self.create_button("Package Info", self.show_package_info, "info.png")
        )

        self.status_label = QLabel(self)
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        self.progressbar = QProgressBar(self)
        self.progressbar.setStyleSheet(
            """
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
                margin: 1px; /* Add margin to chunks for better visual separation */
            }
            QProgressBar::chunk:disabled {
                background-color: #cccccc; /* Change color of disabled chunks */
            }
            QProgressBar::chunk:active {
                background-color: #39FF14; /* Change color of active chunks */
            }
            """
        )
        layout.addWidget(self.progressbar)
        self.progressbar.hide()

        layout.addWidget(
            QLabel("Results:", self, styleSheet="color: #ffffff;")
        )  # Adjust label text color here
        self.result_text = QTextEdit(self)
        self.result_text.setStyleSheet(
            "background-color: #ffffff; color: #000000;"
        )  # Change QTextEdit color
        self.result_text.setWordWrapMode(QTextOption.WrapAnywhere)
        layout.addWidget(self.result_text)

        layout.addWidget(
            self.create_button(
                "Clear", self.clear_result, "clear.png", alignment=Qt.AlignCenter
            )
        )

        self.central_widget.setLayout(layout)

    def create_button(self, text, slot, icon_path=None, alignment=None):
        button = QPushButton(text, self)
        button.clicked.connect(slot)
        if icon_path:
            button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(30, 30))
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                border: 2px solid #000000; /* Border around the button */
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            """
        )

        return button

    def execute_command_with_loading(self, command):
        self.progressbar.setValue(0)
        self.progressbar.show()
        self.progressbar.setFormat("")

        self.progress_thread = WorkerThread(command)
        self.progress_thread.operation_completed.connect(self.show_result)
        self.progress_thread.start()

        self.progressbar.setRange(0, 0)
        self.set_buttons_enabled(False)
        self.status_label.setStyleSheet(
            "color: #00FF00;"
        )  # Change color of processing text
        self.status_label.setText("Processing...")

    def set_buttons_enabled(self, enabled):
        for child in self.findChildren(QPushButton):
            child.setEnabled(enabled)

    def install_package(self):
        package_name = self.package_var.text()
        if package_name:
            self.status_label.setText(f"Installing {package_name}...")
            command = f"pip install {package_name}"
            self.execute_command_with_loading(command)

    def uninstall_package(self):
        package_name = self.package_var.text()
        if package_name:
            self.status_label.setText(f"Uninstalling {package_name}...")
            command = f"pip uninstall -y {package_name}"
            self.execute_command_with_loading(command)

    def upgrade_package(self):
        package_name = self.package_var.text()
        if package_name:
            self.status_label.setText(f"Upgrading {package_name}...")
            command = f"pip install --upgrade {package_name}"
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

    def show_result(self, result):
        self.result_text.clear()
        self.result_text.insertPlainText(result)
        self.status_label.setStyleSheet(
            "color: #FFFF00;"
        )  # Change color of completed text
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
