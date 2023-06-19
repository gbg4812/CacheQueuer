from typing import Any
from PySide2.QtGui import QPainter
from PySide2.QtCore import QEvent, QModelIndex
from PySide2.QtWidgets import QStyleOption

from delegate_subitems import RailLayout


class DelegateUi:
    def __init__(self) -> None:
        self.layout = RailLayout(5, 10)

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
