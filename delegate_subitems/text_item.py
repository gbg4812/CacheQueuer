# Std Imports
import logging
from math import floor
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Local Imports
from .delegate_sub_item import DelegateSubItem

# vendor.PySide2 imports
from vendor.PySide2.QtGui import QPainter, QFont, QColor, QPen, QFontMetrics
from vendor.PySide2.QtCore import Qt, QPoint, QSize

class TextItem(DelegateSubItem):
    def __init__(self, pos: QPoint = QPoint(0, 0), text_size: int = 10, text_color: QColor = Qt.black, min_letters : int = 5):
        super().__init__(pos, QSize(0, 0))
        self.font = QFont('Arial', text_size, QFont.Normal)
        self.pen = QPen(text_color)
        self.text = ""
        self.min_letters = min_letters + 4
    
    def draw(self, painter: QPainter) -> None:
        painter.setPen(self.pen)
        painter.setFont(self.font)
        fm = QFontMetrics(self.font)
        allowed_len = floor(self.width() / fm.averageCharWidth()) - 4
        def_text = self.text
        if allowed_len < len(self.text):
            def_text = self.text[0:allowed_len]
            def_text += "..."
        painter.drawText(self, def_text)
    
    def setText(self, text: str) -> None:
        self.text = text
        f_metrics = QFontMetrics(self.font)
        self.setWidth(f_metrics.averageCharWidth()*self.min_letters)
        self.setHeight(f_metrics.height())