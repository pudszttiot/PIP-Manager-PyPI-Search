import sys
import os
from os import path

import requests
from bs4 import BeautifulSoup
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


class PyPISearchThread(QThread):
    search_results_ready = pyqtSignal(list)

    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        try:
            response = requests.get(f"https://pypi.org/search/?q={self.query}")
            if response.status_code == 200:
                data = self.parse_search_results(response.text)
                self.search_results_ready.emit(data)
            else:
                self.search_results_ready.emit([])
        except requests.RequestException:
            self.search_results_ready.emit([])

    def parse_search_results(self, html):
        soup = BeautifulSoup(html, "html.parser")
        results = []
        for package in soup.find_all("a", class_="package-snippet"):
            name = package.find("span", class_="package-snippet__name").text.strip()
            description = package.find("p", class_="package-snippet__description").text.strip()
            results.append({"name": name, "description": description})
        return results


class PyPISearchApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PIP Manager + PyPI Search")
        self.setGeometry(550, 250, 800, 600)
        self.setStyleSheet("background-color: #006dad;")  # Change background color here
        self.setWindowIcon(QIcon(os.path.abspath(r"../Images/PyPI3resized.ico")))

        layout = QVBoxLayout()

        search_label = QLabel("Package Name:")
        search_label.setStyleSheet("color: white;")
        layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter package name...")
        self.search_input.setStyleSheet(
            "background-color: white; border: 1px solid #ccc; border-radius: 5px; padding: 5px;"
        )
        self.search_input.returnPressed.connect(self.search_packages)
        layout.addWidget(self.search_input)

        search_button = QPushButton("Search")
        search_button.setStyleSheet(
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

        # Add an icon to the search button
        search_icon = QIcon(r"../Images/search.png")  # Provide the path to your icon
        search_button.setIcon(search_icon)

        search_button.clicked.connect(self.search_packages)
        layout.addWidget(search_button)


        packages_label = QLabel("Available Packages:")
        packages_label.setStyleSheet("color: white;")
        layout.addWidget(packages_label)

        self.packages_list = QListWidget()
        self.packages_list.setStyleSheet(
            """
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #448ACA;
                color: white;
            }
            """
        )
        self.packages_list.itemClicked.connect(self.display_package_info)
        layout.addWidget(self.packages_list)

        package_info_label = QLabel("Package Information:")
        package_info_label.setStyleSheet("color: white;")
        layout.addWidget(package_info_label)

        self.package_info_display = QTextBrowser()
        self.package_info_display.setStyleSheet(
            """
            QTextBrowser {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            """
        )
        layout.addWidget(self.package_info_display)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def search_packages(self):
        query = self.search_input.text()
        if query:
            self.progress_bar.setVisible(True)
            self.packages_list.clear()
            self.package_info_display.clear()
            self.thread = PyPISearchThread(query)
            self.thread.search_results_ready.connect(self.display_search_results)
            self.thread.finished.connect(self.hide_progress_bar)
            self.thread.start()

    def display_search_results(self, data):
        if not data:
            self.show_error_message("No packages found.")
            return
        for package in data:
            self.packages_list.addItem(package["name"])

    def display_package_info(self, item):
        package_name = item.text()
        self.package_info_display.clear()
        self.package_info_display.setPlainText("Loading package info...")
        self.thread = PyPISearchThread(package_name)
        self.thread.search_results_ready.connect(self.display_package_info_ready)
        self.thread.start()

    def display_package_info_ready(self, data):
        if not data:
            self.show_error_message("Failed to retrieve package info.")
            return
        package_info = next((x for x in data if x["name"] == self.sender().query), None)
        if package_info:
            self.package_info_display.clear()
            self.package_info_display.setPlainText(package_info["description"])
        else:
            self.show_error_message("Failed to retrieve package info.")

    def hide_progress_bar(self):
        self.progress_bar.setVisible(False)

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Error")
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(message)
        msg_box.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PyPISearchApp()
    window.show()
    sys.exit(app.exec_())
