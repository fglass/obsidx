import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLineEdit, QListWidget
from file_helper import load_files, parse_file
from result_item import ResultItem

UI_WIDTH = 672
UI_HEIGHT = 250
SEARCH_BAR_HEIGHT = 70
RESULT_ITEM_HEIGHT = 56
MAX_N_RESULTS = 3
BACKGROUND_COLOR = "#171717"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._database = _create_database()
        self._result_item_pool = []

        self.setFixedSize(UI_WIDTH, UI_HEIGHT)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self._add_search_bar(layout)
        self._add_results_list(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.deleteLater()
            sys.exit()
        else:
            event.accept()

    def _add_search_bar(self, layout: QVBoxLayout):
        search_bar = QLineEdit()
        search_bar.setFixedHeight(SEARCH_BAR_HEIGHT)
        search_bar.setStyleSheet(f"background-color: {BACKGROUND_COLOR}; color: white; padding-left: 5px;")

        search_bar.setPlaceholderText("Search...")
        search_bar.textChanged.connect(self._on_search)
        layout.addWidget(search_bar)

    def _add_results_list(self, layout: QVBoxLayout):
        self._results_list = QListWidget()
        self._results_list.setStyleSheet("QListWidget { background-color: %s; }" % BACKGROUND_COLOR)
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

        for file, (title, description) in self._database.items():
            if idx == MAX_N_RESULTS:
                break

            if search_input.lower() in title.lower():
                item = self._result_item_pool[idx]
                item.set(file, title, description)
                idx += 1

        self._results_list.setFixedHeight(RESULT_ITEM_HEIGHT * idx)

    def _hide_results_list(self):
        self._results_list.setFixedHeight(0)


def _create_database() -> dict:
    database = {}

    for file in load_files():
        database[file] = parse_file(file)

    return database


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
