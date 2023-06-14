# std imports:
from __future__ import annotations
import logging

# PySide2 imports:
from PySide2.QtCore import QSize, QEvent
from PySide2.QtGui import QPainter, QPixmap, QColor, QPainterPath, QBrush

# local imports:
from enum import IntEnum
from .delegate_sub_item import DelegateSubItem


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class IconButton(DelegateSubItem):

    class ButtonStates(IntEnum):
        NORMAL = 0
        HOVERED = 1
        CLICKED = 2

    def __init__(self,
                 size: QSize = QSize(30, 30),
                 paint_rect: bool = False,
                 radius: int = 5):

        self.icons = {}
        self.bg_colors = {IntEnum(0): QColor(0, 0, 0, 0)}
        self.paint_rect = paint_rect
        self.current_icon = QPixmap()

    def addIcon(self, name: str, icon: QPixmap) -> None:
        self.icons[name] = icon

    def addStateColor(self, state: IconButton.ButtonStates,
                      color: QColor) -> None:

        self.bg_colors[state] = color

    def addIcons(self, icons: {str: QPixmap}) -> None:
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

    def setIcon(self, name: str) -> None:
        self.current_icon = self.icons[name]

    def handleEvent(event: QEvent):
        pos = event.pos()
