import json
import logging
import os
import win32con
from PyQt5.QtCore import QObject

# App constants
APP_NAME = "obsidx"
WINDOW_NAME = u"obsidx – app.py"
CONFIG_FILE = rf"{os.path.expanduser('~')}\.obsidx"
RESOURCE_PATH = rf"{os.path.dirname(os.path.dirname((os.path.abspath(__file__))))}\res"
WINDOW_ICON_PATH = rf"{RESOURCE_PATH}\icon.png"
FOLDER_ICON_PATH = rf"{RESOURCE_PATH}\folder.png"

# UI constants
BACKGROUND_COLOUR = "#202020"
DARK_COLOUR = "#161616"
ACCENT_COLOUR = "#483699"
TEXT_COLOUR = "#d1d2d3"
FONT_SIZE = 11


class Config(QObject):
    def __init__(self):
        super().__init__()
        self._toggle_hotkey = (win32con.VK_F12, (win32con.MOD_WIN, win32con.MOD_ALT))
        self._vault_directory = ""
        self._use_default_editor = False
        self._load()

    @property
    def toggle_hotkey(self):
        return self._toggle_hotkey

    @property
    def vault_directory(self):
        return self._vault_directory

    @property
    def use_default_editor(self):
        return self._use_default_editor

    @vault_directory.setter
    def vault_directory(self, value):
        self._vault_directory = value
        self._save()

    @use_default_editor.setter
    def use_default_editor(self, value):
        self._use_default_editor = value
        self._save()

    def _load(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                config_dto = json.load(f)
                self._vault_directory = config_dto.get("VAULT", "")
                self._use_default_editor = config_dto.get("DEFAULT_EDITOR", False)
                logging.info(f"Loaded config: {config_dto}")
        except FileNotFoundError:
            logging.info("No config found")

    def _save(self):
        with open(CONFIG_FILE, "w") as f:
            config_dto = {
                "VAULT": self._vault_directory,
                "DEFAULT_EDITOR": self._use_default_editor,
            }
            json.dump(config_dto, f)
