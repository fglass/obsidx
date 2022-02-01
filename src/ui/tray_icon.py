from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from src.config import APP_NAME, WINDOW_ICON_PATH


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(QIcon(WINDOW_ICON_PATH), parent)
        self.menu = QMenu(parent)
        self.open_action = self.menu.addAction("Open")
        self.settings_action = self.menu.addAction("Settings")
        self.quit_action = self.menu.addAction("Quit")
        self.setContextMenu(self.menu)
        self.setToolTip(APP_NAME)
