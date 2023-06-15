# std imports:
from __future__ import annotations
from typing import Dict, Optional 
import logging

# PySide2 imports:
from PySide2.QtCore import QSize, QEvent
from PySide2.QtGui import QPainter, QPixmap, QColor, QPainterPath, QBrush, QMouseEvent

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

        self.icons : Dict[str, QPixmap] = {}
        self.setSize(size)
        self.bg_colors : Dict[IconButton.ButtonStates, QColor] = {}
        self.paint_rect = paint_rect
        self.rect_radius = radius
        self.current_icon = ""
        self.view_state = IconButton.ButtonStates.NORMAL

    def addIcon(self, name: str, icon: QPixmap) -> None:
        self.icons[name] = icon

    def addStateColor(self, state: IconButton.ButtonStates,
                      color: QColor) -> None:

        self.bg_colors[state] = color

    def addStateColors(self, colors: Dict[IconButton.ButtonStates, str]):

        for key, value in colors.items():
            self.bg_colors[key] = QColor(value)

    def addIcons(self, icons: Dict[str, str]) -> None:
        for key in icons.keys():
            pixmap = QPixmap(icons[key])
            self.icons[key] = pixmap

    def draw(self, painter: QPainter):

        if self.paint_rect:
            try:
                color = self.bg_colors[self.view_state]
                brush = QBrush(color)

                path = QPainterPath()
                path.addRoundedRect(self, self.rect_radius, self.rect_radius) # type: ignore

                painter.setRenderHint(QPainter.Antialiasing)
                painter.fillPath(path, brush)

            except KeyError:
                pass


        if self.current_icon:
            painter.drawPixmap(self, self.icons[self.current_icon])


    def setIcon(self, name: str) -> None:
        try:
            self.icons.get(name)
            self.current_icon = name

        except KeyError:
            print("no icon for this name")

    def handleEvent(self, event: QMouseEvent):
        if isinstance(event, QMouseEvent):
            pos = event.pos()

            if self.contains(pos):

                if event.type == QMouseEvent.Type.MouseButtonPress:
                    self.view_state = self.ButtonStates.CLICKED
                    return

        self.view_state = self.ButtonStates.NORMAL


