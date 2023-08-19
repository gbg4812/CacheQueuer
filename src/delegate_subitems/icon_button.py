# std imports:
from __future__ import annotations
from typing import Dict, Optional

# Third party imports
from PySide2.QtCore import QPoint, QRect, QSize, QEvent
from PySide2.QtGui import QPainter, QPixmap, QColor, QPainterPath, QBrush, QMouseEvent

from utils import Logger, Level

# local imports:
from enum import IntEnum
from .delegate_sub_item import DelegateSubItem

flog = Logger(__name__, Level.DEBUG)

class IconButton(DelegateSubItem):
    class ButtonStates(IntEnum):
        NORMAL = 0
        HOVERED = 1
        CLICKED = 2

    def __init__(
        self,
        size: QSize = QSize(36, 36),
        paint_rect: bool = False,
        radius: int = 5,
    ):

        super().__init__(size)

        self.icons: Dict[str, QPixmap] = {}
        self.current_icon = ""
        self.setSize(size)

        self.bg_colors: Dict[IconButton.ButtonStates, QColor] = {}
        self.paint_rect = paint_rect
        self.rect_radius = radius

        self.view_state = IconButton.ButtonStates.NORMAL
        self.release_return = None
        self.initialized = False

    def manualInit(self, view_state: IconButton.ButtonStates, current_icon: str):
        if self.initialized:
            flog.error("Initializing initialized button")

        self.view_state = view_state
        self.current_icon = current_icon
        self.initialized = True

    def init(self, state: Dict[str, str | IconButton.ButtonStates]) -> bool:
        if self.initialized:
            flog.error("Initializing initialized button")

        if state:
            try:
                self.view_state = state["view_state"]
                self.current_icon = state["current_icon"]
                self.initialized = True
            except KeyError:
                return False
            return True

        else:
            return False

    def end(self) -> dict:
        state = {"view_state": self.view_state, "current_icon": self.current_icon}
        self.initialized = False
        return state

    def addIcon(self, name: str, icon: QPixmap) -> None:
        self.icons[name] = icon

    def addStateColor(self, state: IconButton.ButtonStates, color: QColor) -> None:
        self.bg_colors[state] = color

    def addStateColors(self, colors: Dict[IconButton.ButtonStates, str]):
        for key, value in colors.items():
            self.bg_colors[key] = QColor(value)

    def addIcons(self, icons: Dict[str, str]) -> None:
        for key in icons.keys():
            pixmap = QPixmap(icons[key])
            self.icons[key] = pixmap

    def draw(self, painter: QPainter):
        painter.save()
        if not self.initialized:
            flog.error("Painting uninitialized button")
            return

        flog.debug("drawing button with state {}".format(self.view_state))
        if self.paint_rect:
            try:
                color = self.bg_colors[self.view_state]
                brush = QBrush(color)

                path = QPainterPath()
                path.addRoundedRect(self, self.rect_radius, self.rect_radius)

                painter.setRenderHint(QPainter.Antialiasing)
                painter.fillPath(path, brush)

            except KeyError:
                flog.error("Button Color Missing")

        if self.current_icon:
            icon = self.icons[self.current_icon]
            posx = self.x() + ((self.width() - icon.width()) >> 1)
            posy = self.y() + ((self.height() - icon.height()) >> 1)
            painter.drawPixmap(posx, posy, icon)

        painter.restore()

    def setIcon(self, name: str) -> None:
        try:
            self.icons.get(name)
            self.current_icon = name

        except KeyError:
            flog.error("no icon for this name")

    def handleEvent(self, event: QMouseEvent):
        if not self.initialized:
            flog.error("Handeling uninitialized button")
            return
        if isinstance(event, QMouseEvent):
            pos = event.pos()

            if self.contains(pos):
                flog.debug("Contained By Button")
                if event.type() == QMouseEvent.Type.MouseButtonPress:
                    flog.debug("Button Clicked")
                    self.view_state = self.ButtonStates.CLICKED
                    return None

                elif event.type() == QMouseEvent.Type.MouseButtonRelease:
                    flog.debug("Button Released")
                    self.view_state = self.ButtonStates.NORMAL
                    return self.release_return


    def onReleaseReturn(self, value) -> None:
        self.release_return = value

