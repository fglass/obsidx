from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidgetItem, QListWidget
from src.config import DARK_COLOUR, VAULT_DIRECTORY
from src.file_helper import open_file

STYLESHEET = "QWidget:hover { background-color: %s } QLabel { background-color: transparent }" % DARK_COLOUR


class ResultItem(QListWidgetItem):
    def __init__(self, parent: QListWidget = None):
        super().__init__(parent)
        self._file_path = ""
        self.setHidden(True)

        self.widget = QWidget()
        self.widget.setStyleSheet(STYLESHEET)
        self.widget.mouseReleaseEvent = self._on_click

        layout = QVBoxLayout()
        self.widget.setLayout(layout)

        self._title_label = QLabel()
        self._title_label.setMargin(0)
        self._title_label.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._title_label)

        self._description_label = QLabel()
        self._description_label.setStyleSheet("color: gray")
        layout.addWidget(self._description_label)

    def init(self):
        self.setSizeHint(self.widget.sizeHint())

    def set(self, filename: str, file_path: str):
        self._title_label.setText(filename)

        location = file_path.replace(VAULT_DIRECTORY, "").replace(f"\\{filename}.md", "") or "\\"
        self._description_label.setText(location)

        self._file_path = file_path
        self.setHidden(False)

    def _on_click(self, _: QMouseEvent):
        open_file(self._file_path)
        self.widget.window().close()
