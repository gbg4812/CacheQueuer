# PySide2 imports
from PySide2.QtCore import QRect, QSize, QPoint

class DelegateSubItem(QRect):
    def __init__(self, pos: QPoint, size: QSize):
        super().__init__(pos, size)
    
    def draw(self, painter) -> None:
        pass
    
    def initRect(self, rect: QRect) -> None:
        self.setRect(rect.x(), rect.y(), rect.width(), rect.height())
