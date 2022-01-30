from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QFileDialog, QPushButton, QHBoxLayout
from src.config import Config, WINDOW_ICON_PATH, FOLDER_ICON_PATH

MENU_WIDTH = 400
MENU_HEIGHT = 150


class SettingsMenu(QWidget):
    def __init__(self, config: Config):
        super().__init__()
        self._config = config
        self.setWindowTitle("Settings")
        self.setWindowFlags(Qt.Dialog)
        self.setFixedSize(MENU_WIDTH, MENU_HEIGHT)
        self.setWindowIcon(QIcon(WINDOW_ICON_PATH))

        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Vault Directory:"))
        vault_layout = QHBoxLayout()
        layout.addLayout(vault_layout)

        self._vault_field = QLineEdit(config.vault_directory)
        self._vault_field.setDisabled(True)
        vault_layout.addWidget(self._vault_field)

        open_dialog_button = QPushButton("")
        open_dialog_button.setIcon(QIcon(FOLDER_ICON_PATH))
        open_dialog_button.setFixedHeight(22)
        open_dialog_button.clicked.connect(self.open_file_dialog)
        vault_layout.addWidget(open_dialog_button)

        layout.addWidget(QLabel("Hotkey:"))
        hotkey_field = QLineEdit("Alt+F8")
        hotkey_field.setDisabled(True)
        layout.addWidget(hotkey_field)

        layout.addWidget(QLabel("Use Default Editor:"))
        default_editor_checkbox = QCheckBox()
        default_editor_checkbox.setChecked(config.use_default_editor)
        default_editor_checkbox.toggled.connect(self.toggle_default_editor_checkbox)
        layout.addWidget(default_editor_checkbox)

    def open_file_dialog(self):
        vault_directory = QFileDialog.getExistingDirectory(self, "Select Vault Directory")
        if vault_directory:
            self._vault_field.setText(vault_directory)
            self._config.vault_directory = vault_directory

    def toggle_default_editor_checkbox(self, enabled: bool):
        self._config.use_default_editor = enabled
