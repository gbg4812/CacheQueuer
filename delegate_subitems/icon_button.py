# std imports:
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# PySide2 imports:
from PySide2.QtCore import QPoint 
from PySide2.QtGui import QPainter, QPixmap, QColor, QPainterPath, QBrush

# local imports:
from enum import IntEnum
from .delegate_sub_item import DelegateSubItem

class IconButton(DelegateSubItem):
    def __init__(self, icon: QPixmap, state : IntEnum = 0, pos: QPoint = QPoint(0, 0), paint_rect: bool = False, bg_color : QColor = QColor(0,0,0,0)):
        super(IconButton, self).__init__(pos, icon.size())
        self.icons = {state : icon}
        self.bg_colors = {state : bg_color}
        self._state = state
        self.paint_rect = paint_rect

    def addStateIcon(self, state: IntEnum, icon: QPixmap) -> None:
        self.icons[state] = icon
    
    def addStateColor(self, state: IntEnum, color: QColor) -> None:
        self.bg_colors[state] = color

    def addStateIcons(self, icons: dict) -> None:
        for key in icons.keys():
            self.icons[key] = icons[key]

    def draw(self, painter: QPainter):
        if self.paint_rect:
            painter.setRenderHint(QPainter.Antialiasing)
            path = QPainterPath()
            path.addRoundedRect(self, 5, 5)
            try:
                color = self.bg_colors[self._state]
                brush = QBrush(color)
                painter.fillPath(path, brush)
            except KeyError:
                print("ERROR::KEY::{} Colors are: {}".format(self._state, self.bg_colors))

        try:
            painter.drawPixmap(self, self.icons[self._state])
        except KeyError:
            print("ERROR::KEY::{} Icons are: {}".format(self._state, self.icons))


    
    def setCurrentState(self, state: IntEnum) -> None:
        try:
            size = self.icons[state].size()
            self.setSize(size)
            self._state = state

        except KeyError:
            logging.warning("There is no icon for this state")

