from typing import Any
from PySide2.QtGui import QPainter
from PySide2.QtCore import QEvent

from delegate_subitems import RailLayout


class DelegateUi:
    def __init__(self) -> None:
        self.layout = RailLayout(5, 10)

    def draw(self, painter: QPainter):
        self.layout.computeLayout()
        self.layout.draw(painter)

    def handleEvents(self, event: QEvent) -> Any:
        self.layout.handleEvent(event)
