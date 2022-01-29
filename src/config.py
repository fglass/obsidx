import os
import win32con
from PyQt5 import QtCore

# App constants
from PyQt5.QtCore import QObject

WINDOW_NAME = u"obsidx – app.py"
RESOURCE_PATH = rf"{os.path.dirname(os.path.dirname((os.path.abspath(__file__))))}\res"

# UI constants
BACKGROUND_COLOUR = "#202020"
DARK_COLOUR = "#161616"
ACCENT_COLOUR = "#483699"
TEXT_COLOUR = "#d1d2d3"


class Config(QObject):
    vault_change_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self._toggle_hotkey = (win32con.VK_F8, win32con.MOD_ALT)
        self._vault_directory = ""
        self._use_default_editor = False
        self.load()

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
        self.save()
        self.vault_change_signal.emit()

    @use_default_editor.setter
    def use_default_editor(self, value):
        self._use_default_editor = value
        self.save()

    def load(self):
        pass

    def save(self):
        pass
