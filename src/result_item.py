from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidgetItem, QListWidget
from src.config import DARK_COLOUR
from src.file_helper import open_file

STYLESHEET = "QWidget:hover { background-color: %s } QLabel { background-color: transparent }" % DARK_COLOUR


class ResultItem(QListWidgetItem):
    def __init__(self, parent: QListWidget = None):
        super().__init__(parent)
        self._filename = ""
        self.setHidden(True)

        self.widget = QWidget()
        self.widget.setStyleSheet(STYLESHEET)
        self.widget.mouseReleaseEvent = lambda _: open_file(self._filename)

        layout = QVBoxLayout()
        self.widget.setLayout(layout)

        self._title_label = QLabel()
        self._title_label.setMargin(0)
        self._title_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._title_label)

        self._description_label = QLabel()
        layout.addWidget(self._description_label)

    def init(self):
        self.setSizeHint(self.widget.sizeHint())

    def set(self, filename: str, title: str, description: str):
        self._filename = filename
        self._title_label.setText(title)
        self._description_label.setText(description)
        self.setHidden(False)
