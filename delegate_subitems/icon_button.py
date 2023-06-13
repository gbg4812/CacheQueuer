# std imports:
import logging

# PySide2 imports:
from PySide2.QtCore import QSize
from PySide2.QtGui import QPainter, QPixmap, QColor, QPainterPath, QBrush

# local imports:
from enum import IntEnum
from .delegate_sub_item import DelegateSubItem


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class IconButton(DelegateSubItem):
    def __init__(self,
                 size: QSize = QSize(30, 30),
                 paint_rect: bool = False):

        self.icons = {}
        self.bg_colors = {IntEnum(0): QColor(0, 0, 0, 0)}
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
                color = self.bg_colors[self.state.get('view_state')]
                brush = QBrush(color)
                painter.fillPath(path, brush)
            except KeyError:
                print("ERROR::KEY::{} Colors are: {}".format(
                    self.state.get('view_state'), self.bg_colors))

        try:
            painter.drawPixmap(self, self.icons[self.state.get('view_state')])
        except KeyError:
            print("ERROR::KEY::{} Icons are: {}"
                  .format(self.state.get('view_state'), self.icons))

    def setViewState(self, state: IntEnum) -> None:
        self.state['view_state'] = state
