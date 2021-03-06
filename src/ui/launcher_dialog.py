import logging
import os
import time
import win32api
import win32gui
import win32process
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QLineEdit, QListWidget
from src.config import BACKGROUND_COLOUR, DARK_COLOUR, ACCENT_COLOUR, TEXT_COLOUR, WINDOW_NAME, WINDOW_ICON_PATH, Config
from src.file_helper import load_files
from src.ui.result_item import ResultItem

UI_WIDTH = 672
BASE_UI_HEIGHT = 60
SEARCH_BAR_HEIGHT = 40
RESULT_ITEM_HEIGHT = 56
MAX_N_RESULTS = 4


class LauncherDialog(QMainWindow):
    toggle_signal = QtCore.pyqtSignal()

    def __init__(self, config: Config):
        super().__init__()
        self._config = config
        self._vault = []
        self._result_item_pool = []
        self._attached_thread_input = False

        self.toggle_signal.connect(self.toggle)
        self.setFixedSize(UI_WIDTH, BASE_UI_HEIGHT)
        self.setWindowIcon(QIcon(WINDOW_ICON_PATH))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.StrongFocus)

        self.setStyleSheet(
            "QWidget#LauncherDialog { border-radius: 5px } QWidget { background-color: %s; color: %s } "
            % (BACKGROUND_COLOUR, TEXT_COLOUR)
        )

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        widget.setObjectName("LauncherDialog")
        self.setCentralWidget(widget)

        self._add_search_bar(layout)
        self._add_results_list(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            event.accept()

    def changeEvent(self, event: QEvent):
        super().changeEvent(event)
        if event.type() == QEvent.ActivationChange:
            if not self.isActiveWindow():
                self.close()

    def toggle(self):
        if self.isVisible():
            self.close()
        else:
            self._load_vault()
            self.show()

    def _load_vault(self):
        start = time.time()
        self._vault = load_files(self._config.vault_directory)
        logging.debug(f"Loaded {len(self._vault)} files in {time.time() - start:.3f}s")

    def show(self):
        super().show()
        self._set_window_focus()
        self.activateWindow()

    def _set_window_focus(self):
        handle = win32gui.FindWindow(None, WINDOW_NAME)

        if handle == 0:
            return

        if not self._attached_thread_input:
            self._attach_thread_input(handle)

        win32gui.SetFocus(handle)

    def _attach_thread_input(self, handle: int):
        remote_thread, _ = win32process.GetWindowThreadProcessId(handle)
        win32process.AttachThreadInput(win32api.GetCurrentThreadId(), remote_thread, True)
        self._attached_thread_input = True

    def _add_search_bar(self, layout: QVBoxLayout):
        search_bar = QLineEdit()
        search_bar.setFixedHeight(SEARCH_BAR_HEIGHT)
        search_bar.setStyleSheet(
            f"background-color: {DARK_COLOUR}; padding-left: 5px; border: 1px solid {ACCENT_COLOUR}; border-radius: 5px"
        )

        search_bar.setPlaceholderText("Search...")
        search_bar.textChanged.connect(self._on_search)
        layout.addWidget(search_bar)

    def _add_results_list(self, layout: QVBoxLayout):
        self._results_list = QListWidget()
        self._results_list.setStyleSheet("QListWidget { border: none }")
        self._hide_results_list()
        layout.addWidget(self._results_list)
        layout.addStretch(1)
        [self._add_result_item() for _ in range(MAX_N_RESULTS)]

    def _add_result_item(self):
        item = ResultItem(self._results_list, self._config)
        item.init()
        self._results_list.addItem(item)
        self._results_list.setItemWidget(item, item.widget)
        self._result_item_pool.append(item)

    def _on_search(self, search_input: str):
        [item.setHidden(True) for item in self._result_item_pool]

        if search_input == "":
            self._hide_results_list()
            return

        idx = 0

        for (name, path) in self._get_matching_files(search_input):
            if idx >= MAX_N_RESULTS:
                break

            item = self._result_item_pool[idx]
            item.set(name, path)
            idx += 1

        results_height = RESULT_ITEM_HEIGHT * idx
        self._results_list.setFixedHeight(results_height)
        self.setFixedHeight(BASE_UI_HEIGHT + results_height)

    def _get_matching_files(self, search_input: str) -> list:
        matches = []
        search_input = search_input.lower()

        for path in self._vault:
            name = os.path.basename(path).replace(".md", "")
            if search_input in name.lower():
                matches.append((name, path))

        return sorted(matches, key=lambda file: 0 if file[0].lower().startswith(search_input) else 1)

    def _hide_results_list(self):
        self._results_list.setFixedHeight(0)
        self.setFixedHeight(BASE_UI_HEIGHT)
