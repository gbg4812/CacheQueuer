# std imports:
import logging

# PySide2 imports:
from PySide2.QtCore import QSize, QPoint, QRect
from PySide2.QtGui import QPainter, QPixmap 

# local imports:
from global_enums import *
from .delegate_sub_item import DelegateSubItem

class IconButton(DelegateSubItem):
    def __init__(self, icon: QPixmap, pos: QPoint = QPoint(0, 0)):

        super(IconButton, self).__init__(pos, icon.size())
        self.icons = {WidgetState.ENABLED: icon}
        self._state = WidgetState.ENABLED

    def addStateIcon(self, state: WidgetState, icon: QPixmap) -> None:
        self.icons[state] = icon

    def addStateIcons(self, icons: dict) -> None:
        for key in icons.keys():
            self.icons[key] = icons[key]

    def draw(self, painter: QPainter) -> QPixmap:
        painter.drawPixmap(self, self.icons[self._state])
    
    def setCurrentState(self, state: WidgetState) -> None:

        try:
            size = self.icons[state].size()
            self.setSize(size)
            self._state = state

        except KeyError:
            logging.warning("There is no icon for this state")

        