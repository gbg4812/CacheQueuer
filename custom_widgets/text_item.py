from PySide2.QtGui import QPainter, QFont, QColor, QPen
from .delegate_sub_item import DelegateSubItem
from PySide2.QtCore import Qt, QPoint, QSize



class TextItem(DelegateSubItem):
    def __init__(self, pos: QPoint = QPoint(0, 0), text_size: int = 10, text_color: QColor = Qt.black):
        super().__init__(pos, QSize(0, 0))
        self.font = QFont('Arial', text_size, QFont.Normal)
        self.pen = QPen(text_color)
        self.text = ""
    
    def draw(self, painter: QPainter) -> None:
        painter.setPen(self.pen)
        painter.setFont(self.font)
        
        painter.drawText(self, self.text)
    
    def setText(self, text: str) -> None:
        self.text = text
        painter = QPainter()
        rect = painter.boundingRect(self, Qt.AlignRight | Qt.AlignCenter, self.text)
        self.initRect(rect)