# Std Imports
import logging
from math import floor

# Local Imports
from .delegate_sub_item import DelegateSubItem

# PySide6 imports
from PySide6.QtGui import QPainter, QFont, QColor, QPen, QFontMetrics
from PySide6.QtCore import Qt, QPoint, QSize, QEvent



class TextItem(DelegateSubItem):
    def __init__(
        self,
        pos: QPoint = QPoint(0, 0),
        text_size: int = 10,
        text_color: QColor = Qt.black,
        min_letters: int = 5,
    ):
        super().__init__(QSize(0, 0))
        self.font = QFont("Arial", text_size, QFont.Normal)
        self.color = text_color
        self.text = ""
        self.min_letters = min_letters + 4
        self.editing = False

    def init(self, state: dict) -> bool:
        if state:
            try:
                self.text = state["text"]
                self.color = state["color"]
                return True
            except KeyError:
                return False
        else:
            return False

    def end(self) -> dict:
        state = {"text" : self.text, "color": self.color}
        return state

    def draw(self, painter: QPainter) -> None:
        painter.save()
        painter.setPen(QPen(self.color))
        painter.setFont(self.font)
        fm = QFontMetrics(self.font)
        allowed_len = floor(self.width() / fm.averageCharWidth()) - 4
        def_text = self.text
        if allowed_len < len(self.text):
            def_text = self.text[0:allowed_len]
            def_text += "..."
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawText(self, def_text)
        painter.restore()

    def setText(self, text: str) -> None:
        self.text = text
        f_metrics = QFontMetrics(self.font)
        self.setWidth(f_metrics.averageCharWidth() * self.min_letters)
        self.setHeight(f_metrics.height())

    def setTextColor(self, color: QColor):
        self.color = color

    def handleEvent(self, event: QEvent):
        if self.contains(event.pos()):
            self.editing = True
