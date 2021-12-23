import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu

ICON_PATH = rf"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\res\icon.png"


class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(QIcon(ICON_PATH), parent)
        self.menu = QMenu(parent)
        self.open_action = self.menu.addAction("Open")
        self.settings_action = self.menu.addAction("Settings")
        self.quit_action = self.menu.addAction("Quit")
        self.setContextMenu(self.menu)
