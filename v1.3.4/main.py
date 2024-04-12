import sys

from pip_package_manager import PipPackageManagerApp
from pypi_search_app import PyPISearchApp
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QDialog,
    QLabel,
    QMainWindow,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
)


class HelpDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("How to Use...")
        self.setGeometry(400, 200, 940, 800)
        self.setWindowIcon(QIcon(r"../Images/PyPI3resized.ico"))

        layout = QVBoxLayout(self)

        # Create a scroll area
        scroll_area = QScrollArea(self)
        layout.addWidget(scroll_area)

        # Create a QLabel for the help content
        label = QLabel(self)
        label.setTextFormat(1)  # Set text format to RichText
        label.setText(
            """
            <html>
            <body>
                <p style="text-align: center;"><h2><span style="color: #00FF00;">===================================</span></h2>
        <h1><span style="color: #F5F5F5;">🛠 PIP Manager + PyPI Search 🛠</span></h1>
        <h2><span style="color: #FFFFFF;">📝 Version: 1.3.4</span></h2>
        <h2><span style="color: #FFFFFF;">📅 Release Date: January 30, 2024</span></h2>
        <h2><span style="color: #00FF00;">===================================</span></h2>

        <p style="text-align: center;">
        <span style="color: #282c34; background-color: yellow;">The
        <strong><span style="color: #000000; background-color: yellow;">PIP Manager</span></strong>
        <span style="color: #282c34; background-color: yellow;"> application offers a user-friendly interface for installing, uninstalling,<br>upgrading, listing installed packages and checking outdated packages.</span>

        <br>
        <span style="color: yellow; background-color: #0073b7;"><br>Also included is a <strong><span style="color: yellow; background-color: #0073b7;">PyPI Search</span></strong> which enables users to search Python packages available on<br>the Python Package Index (PyPI).</span></p>

        <br>
        <p><h3><span style="color: #ff00ff;">Here's how to switch between the <span style="color: #030303; background-color: #f5f5f5;">PIP Manager</span> & <span style="color: #030303; background-color: #f5f5f5;">PyPI Search:</span></h3></p>
        <br><span style="color: #f5f5f5;">﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏</span>
        <br>
        <br>
• Open PIP Manager Tab:
        <ol>

            <li>Once the Python GUI application is running, you'll see two tabs <span style="color: #FF6600;">"PIP Manager"</span> & <span style="color: #FF6600;">"PyPI Search"</span>
            <br>Click on the <strong><span style="color: #FF6600;">"PIP Manager"</span></strong> tab.</li>
        </ol>

• Open PyPI Search Tab:
        <ol>

            <li>To switch to the <span style="color: #FF6600;">"PyPI Search"</span> functionality, click on the <strong><span style="color: #FF6600;">"PyPI Search"</span></strong> tab.</li>
        </ol>


        <br>
        <p><h3><span style="color: #ff00ff;">Here's how to use <span style="color: #030303; background-color: #f5f5f5;">PIP Manager:</span></h3></p>
        <br><span style="color: #f5f5f5;">﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏</span>
        <br>
        <br>

        • Installing a Package:
        <ol>

            <li>Start by typing the name of the package you want to install in the <span style="color: #FF6600;">"Package Name"</span> field at the top of the page.</li>
            <li>Click on the <strong><span style="color: #FF6600;">"Install"</span></strong> button.</li>
            <li>Wait for the installation process to complete.</li>
        </ol>

        • Uninstalling a Package:
        <ol>

            <li>Start by typing the name of the package you want to uninstall in the <span style="color: #FF6600;">"Package Name"</span> field at the top of the page.</li>
            <li>Click on the <strong><span style="color: #FF6600;">"Uninstall"</span></strong> button.</li>
            <li>Wait for the uninstallation process to complete.</li>
            </ol>

        • Upgrading a Package:
        <ol>

            <li>Start by typing the name of the package you want to upgrade in the <span style="color: #FF6600;">"Package Name"</span> field at the top of the page.</li>
            <li>Click on the <strong><span style="color: #FF6600;">"Upgrade Package"</span></strong> button.</li>
            <li>Wait for the upgrade process to complete.</li>
            </ol>

        • List Installed Packages:
        <ol>

            <li>Click on the <strong><span style="color: #FF6600;">"List Installed Packages"</span></strong> button.</li>
            <li>Wait for the system to gather the information.</li>
            <li>Once completed, you'll see a list of all installed packages along with their versions in the <span style="color: #FF6600;">"Results"</span> field<br>at the bottom of the page.</li>
            <li>You can now review the list to see what packages are installed on your system.</li>
            </ol>

        • Check Outdated Packages:
        <ol>

            <li>Click on the <strong><span style="color: #FF6600;">"Check Outdated Packages"</span></strong> button.</li>
            <li>The system will now scan for any outdated packages.</li>
            <li>Once completed, you'll see a list of all outdated packages along information such as the current version and<br>the latest available version in the <span style="color: #FF6600;">"Results"</span> field at the bottom of the page.</li>
            <li>You can now review this list to determine which packages need updating.</li>
            </ol>

        • Package Info:
        <ol>

            <li>Enter the name of the package you want information about in the <span style="color: #FF6600;">"Package Name"</span> field at the top of the page.</li>
            <li>Click on the <strong><span style="color: #FF6600;">"Package Info"</span></strong> button.</li>
            <li>Wait for the system to gather the information.</li>
            <li>Once completed, you'll then receive detailed information about the specified package including its version,<br>dependencies, and more in the <span style="color: #FF6600;">"Results"</span> field at the bottom of the page.</li>
            </ol>

        • Clear:
        <ol>

            <li>Click on the <strong><span style="color: #FF6600;">"Clear"</span></strong> button.</li>
            <li>Upon clicking, all current search results and installed packages will be cleared from the display.</li>
            <li>The <span style="color: #FF6600;">"Package Name"</span> field will be emptied, ready for you to enter a new input.</li>
            </ol>

            <br>


            <p><h3><span style="color: #ff00ff;">Here's how to use <span style="color: #030303; background-color: #f5f5f5;">PyPI Search:</span></h3></p>
        <br><span style="color: #f5f5f5;">﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏</span>
        <br>
        <br>

        • Using the Application:
        <ol>

            <li>In the input field type the name of the package you want to search for.</li>
            <li>Click on the <strong><span style="color: #FF6600;">"Search"</span></strong> button or hit Enter to initiate the search.</li>
        </ol>

        • View Available Packages:
        <ol>

            <li>Wait for the search results to appear in the <span style="color: #FF6600;">"Available Packages"</span> list.</li>
            <li>Once the search is complete, a list of available packages will be displayed in the <span style="color: #FF6600;">"Available Packages"</span> section.</li>
            <li>Click on a package name in the list to view its information.</li>
            </ol>

        • Interacting with the Application:
        <ol>

            <li>You can search for multiple packages by repeating steps 4 and 5.</li>
            <li>If no packages are found for your search query, an error message will appear.</li>
            <li>If there's an issue retrieving package information, an error message will also appear.</li>
            </ol>

        • Closing the Application:
        <ol>

            <li>You can close the application window by clicking the close button (X) on the top right corner of the window.</li>
            </ol>


        <p><strong>That's it!</strong>...Thank you for using <strong><span style="color: #FFD700;">PIP Manager + PyPI Search !</span></strong></p>


        <!-- Add an image here -->
        <p style="text-align: center;"><img src="Images/pipmanager1.png" alt="pipmanager.png" width="300" height="180" border="1">

        <h6 style="color: #e8eaea;">▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃▃</h6>



    <h3><span style="color: #39ff14; background-color: #000000;">╬╬══▲▲▲ <u>MY CHANNELS</u> ▲▲▲══╬╬</span></h3></p>
        <br>
        <br>

        <span>
        <img src="Socials/Github.png" alt="Github.png" width="20" height="20" border="2">
        <a href="https://github.com/pudszttiot" style="display:inline-block; text-decoration:none; color:#e8eaea; margin-right:20px;" onclick="openLink('https://github.com/pudszttiot')">Github</a>
        </span>

        <span>
        <img src="Socials/Youtube.png" alt="Youtube.png" width="20" height="20" border="2">
        <a href="https://youtube.com/@pudszTTIOT" style="display:inline-block; text-decoration:none; color:#ff0000;" onclick="openLink('https://youtube.com/@pudszTTIOT')">YouTube</a>
        </span>

        <span>
        <img src="Socials/SourceForge.png" alt="SourceForge.png" width="20" height="20" border="2">
        <a href="https://sourceforge.net/u/pudszttiot" style="display:inline-block; text-decoration:none; color:#ee730a;" onclick="openLink('https://sourceforge.net/u/pudszttiot')">SourceForge</a>
        </span>

        <span>
        <img src="Socials/Dailymotion.png" alt="Dailymotion.png" width="20" height="20" border="2">
        <a href="https://dailymotion.com/pudszttiot" style="display:inline-block; text-decoration:none; color:#0062ff;" onclick="openLink('https://dailymotion.com/pudszttiot')">Dailymotion</a>
        </span>

        <span>
        <img src="Socials/Blogger.png" alt="Blogger.png" width="20" height="20" border="2">
        <a href="https://pudszttiot.blogspot.com" style="display:inline-block; text-decoration:none; color:#ff5722;" onclick="openLink('https://pudszttiot.blogspot.com')">Blogger</a>
        </span>

        <script>
        function openLink(url) {
            QDesktopServices.openUrl(QUrl(url));
        }
        </script>
            </body>
            </html>
        """
        )

        label.setOpenExternalLinks(True)
        label.setStyleSheet(
            "color: #1E90FF; background-color: #333333; padding: 10px;"
            "border: 2px solid #1E90FF; border-radius: 10px;"
        )

        # Set the QLabel as the widget inside the scroll area
        scroll_area.setWidget(label)


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PIP Manager + PyPI Search")
        self.setGeometry(550, 250, 800, 600)
        self.setStyleSheet("background-color: ;")  # Change background color here
        self.setWindowIcon(QIcon(r"../Images/PyPI3resized.ico"))


        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.init_tabs()
        self.create_menu_bar()

    def init_tabs(self):
        self.pip_manager_tab = PipPackageManagerApp()
        self.pypi_search_tab = PyPISearchApp()

        self.tab_widget.addTab(self.pip_manager_tab, "PIP Manager")
        self.tab_widget.addTab(self.pypi_search_tab, "PyPI Search")

        # Apply stylesheet to customize tab colors
        self.tab_widget.setStyleSheet(
            """
            QTabBar::tab:selected {
                background: #2196F3; /* Blue */
                color: white;
            }

            QTabBar::tab:!selected {
                background: #BBDEFB; /* Light Blue */
                color: black;
            }
        """
        )

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu with submenu
        help_menu = menubar.addMenu("Help")
        how_to_use_action = QAction("How to Use...", self)
        how_to_use_action.triggered.connect(self.show_how_to_use_dialog)
        help_menu.addAction(how_to_use_action)

    def show_how_to_use_dialog(self):
        dialog = HelpDialog()
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
