from typing import Optional
# PySide6 imports
from PySide6.QtCore import QRect, QSize, QPoint, QEvent


class DelegateSubItem(QRect):


    def __init__(self, size: QSize):
        super().__init__(QPoint(0, 0), size)
        self.state = {}

    def draw(self, painter) -> None:
        pass

    def initRect(self, rect: QRect) -> None:
        self.setRect(rect.x(), rect.y(), rect.width(), rect.height())

    def init(self, state: dict) -> Optional[bool]:
        pass

    def end(self) -> dict:
        return dict()

    def handleEvent(self, event: QEvent):
        pass
