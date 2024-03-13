from typing import Any, Optional
from PySide6.QtGui import QPainter
from PySide6.QtCore import QEvent, QModelIndex 
from PySide6.QtWidgets import QStyleOption, QWidget, QStyleOptionViewItem

from .rail_layout import RailLayout


class DelegateUi:
    def __init__(self) -> None:
        self.layout = RailLayout(50, 10)

    def draw(self, painter: QPainter, option: QStyleOption, index: QModelIndex):
        pass

    def handleEvents(
        self, event: QEvent, option: QStyleOption, index: QModelIndex
    ) -> Any:
        pass

    def sizeHint(self, option: QStyleOption, index: QModelIndex):
        pass

    def initItems(self, option: QStyleOption, index: QModelIndex):
        pass

    def createEditor(
        self, parent: QWidget, option: QStyleOption, index: QModelIndex
    ) -> Optional[QWidget]:
        pass

    def updateEditorGeometry(
        self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        editor.setGeometry(option.rect)
        return

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
       pass
