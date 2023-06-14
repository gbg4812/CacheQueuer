# PySide2 imports
from PySide2.QtCore import QRect, QSize, QPoint


class DelegateSubItem(QRect):
    def __init__(self, pos: QPoint, size: QSize):
        super().__init__(pos, size)
        self.state = {}

    def draw(self, painter) -> None:
        pass

    def initRect(self, rect: QRect) -> None:
        self.setRect(rect.x(), rect.y(), rect.width(), rect.height())

    def init(self, state: dict) -> None:
        self.state = state

    def end(self) -> dict:
        state = dict(self.state)
        self.state = {}
        return state

    def handleEvent(event: QEvent):
        pass
