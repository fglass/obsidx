import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLineEdit, QListWidget
from pynput.keyboard import HotKey, Listener
from file_helper import load_files, parse_file
from result_item import ResultItem
from src.config import TOGGLE_KEYBIND, BACKGROUND_COLOUR, DARK_COLOUR, ACCENT_COLOUR, TEXT_COLOUR
from src.tray_icon import TrayIcon

UI_WIDTH = 672
UI_HEIGHT = 250
INITIAL_WINDOW_HEIGHT = 60
SEARCH_BAR_HEIGHT = 40
RESULT_ITEM_HEIGHT = 56
MAX_N_RESULTS = 3


class MainWindow(QMainWindow):
    toggle_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self._database = _create_database()
        self._result_item_pool = []

        self.toggle_signal.connect(self.toggle)
        self.setFixedSize(UI_WIDTH, UI_HEIGHT)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedHeight(INITIAL_WINDOW_HEIGHT)
        self.setStyleSheet(f"background-color: {BACKGROUND_COLOUR}; color: {TEXT_COLOUR}; border-radius: 5px")

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self._add_search_bar(layout)
        self._add_results_list(layout)

    def toggle(self):
        if self.isVisible():
            self.close()
        else:
            self.show()  # TODO: take focus

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            event.accept()

    def _add_search_bar(self, layout: QVBoxLayout):
        search_bar = QLineEdit()
        search_bar.setFixedHeight(SEARCH_BAR_HEIGHT)
        search_bar.setStyleSheet(
            f"background-color: {DARK_COLOUR}; padding-left: 5px; border: 1px solid {ACCENT_COLOUR}; border-radius: 5px"
        )

        search_bar.setPlaceholderText("Search...")
        search_bar.textChanged.connect(self._on_search)
        layout.addWidget(search_bar)

    def _add_results_list(self, layout: QVBoxLayout):  # TODO: transparent pressed colour?
        self._results_list = QListWidget()
        self._results_list.setStyleSheet(
            "QListWidget::item:hover:!active { background: transparent } QListWidget::item { background: transparent; }"
        )
        self._hide_results_list()
        layout.addWidget(self._results_list)
        layout.addStretch(1)
        [self._add_result_item() for _ in range(MAX_N_RESULTS)]

    def _add_result_item(self):
        item = ResultItem(self._results_list)
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
        search_input = search_input.lower()

        for file, (title, description) in self._database.items():
            if idx == MAX_N_RESULTS:
                break

            if search_input in title.lower() or search_input in description.lower():
                item = self._result_item_pool[idx]
                item.set(file, title, description)
                idx += 1

        results_height = RESULT_ITEM_HEIGHT * idx
        self._results_list.setFixedHeight(results_height)
        self.setFixedHeight(INITIAL_WINDOW_HEIGHT + results_height)

    def _hide_results_list(self):
        self._results_list.setFixedHeight(0)
        self.setFixedHeight(INITIAL_WINDOW_HEIGHT)


def _create_database() -> dict:
    database = {}

    for file in load_files():
        database[file] = parse_file(file)

    return database


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()

    hotkey = HotKey(HotKey.parse(TOGGLE_KEYBIND), window.toggle_signal.emit)
    hotkey_listener = Listener(on_press=hotkey.press, on_release=hotkey.release)
    hotkey_listener.start()

    tray_icon = TrayIcon()
    tray_icon.open_action.triggered.connect(window.show)
    tray_icon.quit_action.triggered.connect(app.quit)
    tray_icon.show()

    app.exec()


if __name__ == "__main__":
    main()
