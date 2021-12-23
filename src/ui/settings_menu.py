from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox
from src.config import VAULT_DIRECTORY

MENU_WIDTH = 400
MENU_HEIGHT = 150


class SettingsMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setWindowFlags(Qt.Dialog)
        self.setFixedSize(MENU_WIDTH, MENU_HEIGHT)

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Vault Directory:"))
        vault_field = QLineEdit(VAULT_DIRECTORY)
        layout.addWidget(vault_field)

        layout.addWidget(QLabel("Hotkey:"))
        hotkey_field = QLineEdit("Alt+F3")
        hotkey_field.setDisabled(True)
        layout.addWidget(hotkey_field)

        layout.addWidget(QLabel("Use Default Editor:"))
        default_editor_checkbox = QCheckBox()
        layout.addWidget(default_editor_checkbox)

