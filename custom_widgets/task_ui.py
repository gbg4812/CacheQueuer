# std imports
from os import path
from enum import IntEnum
from typing import Any

# local imports
from delegate_subitems import DelegateUi, IconButton

# vendor imports
from PySide2.QtGui import QBrush, QColor, QPen, QPixmap, QPainter
from PySide2.QtCore import (
    QMargins,
    QPoint,
    QSize,
    QModelIndex,
    Qt,
    QEvent,
    QRect,
    QLine,
)
from PySide2.QtWidgets import QStyleOption, QStyle


class TaskUi(DelegateUi):
    # The value is only a key, it doesn't mather so, 1+ values are fore general
    # roles and 100+ values for ui especific roles.
    class DataRoles(IntEnum):
        RENDER = 100
        REMOVE = 101
        ENABLE = 102
        DEPENDENT = 103

    class UiEvents(IntEnum):
        NONE = 0
        REMOVE = 1
        RENDER = 2
        DATACHANGED = 3

    def __init__(self) -> None:
        super().__init__()

        wrkdir, _ = path.split(__file__)
        wrkdir += "/"

        # Define State Palette
        state_colors = {
            IconButton.ButtonStates.NORMAL: "#FFFFFF00",
            IconButton.ButtonStates.HOVERED: "#FFFFFF7F",
            IconButton.ButtonStates.CLICKED: "#FFFFFFB2",
        }

        self.content_margins = QMargins(5, 5, 20, 5)

        # Create Layout:
        self.layout.margin = 10
        self.layout.spacing = 10

        # Create Buttons:
        # Render Button:
        self.render = IconButton(QSize(36, 36), paint_rect=True, radius=5)
        self.render.onReleaseReturn(self.UiEvents.RENDER)
        self.render.addStateColors(state_colors)
        self.render.addIcon(
            "render", QPixmap(wrkdir + "res/icons/render.png")
        )
        self.render.setIcon("render")
        # Remove Button:
        self.remove = IconButton(QSize(36, 36), paint_rect=True, radius=5)
        self.remove.onReleaseReturn(self.UiEvents.REMOVE)
        self.remove.addStateColors(state_colors)
        self.remove.addIcon("remove", QPixmap(wrkdir + "res/icons/trash.png"))
        self.remove.setIcon("remove")

        self.layout.addRItem(self.render)
        self.layout.addRItem(self.remove)
        self.layout.computeLayout()

    def draw(self, painter: QPainter, option: QStyleOption, index: QModelIndex):
        rect: QRect = option.rect.marginsRemoved(self.content_margins)
        pos = rect.topLeft()

        TextColor1_disabled = QColor("#698181")
        Primary3_disabled = QColor("#8cb2be")
        Primary3_selected = QColor("#c9e7ed")
        Primary3_hover = QColor("#a4d5df")
        TextColor1 = QColor("#1a2122")
        Border2 = QColor("#354558")
        Border1 = QColor("#6b98a5")
        Accent1 = QColor("#57a773")
        Primary3 = QColor("#7ec0d1")
        Primary2 = QColor("#476d86")
        Primary1 = QColor("#3d4e63")

        if option.state & QStyle.State_Selected:
            self.paintBackground(painter, rect, Border1, Primary3_selected)
        else:
            self.paintBackground(painter, rect, Border1, Primary3)

        self.initItems(index, pos)
        self.layout.draw(painter)

    def sizeHint(self, option: QStyleOption, index: QModelIndex):
        pos = option.rect.topLeft()
        self.layout.computeLayout(pos)
        return self.layout.sizeHint().grownBy(self.content_margins)

    def handleEvents(
        self, event: QEvent, option: QStyleOption, index: QModelIndex
    ) -> Any:
        rect: QRect = option.rect.marginsRemoved(self.content_margins)
        pos = rect.topLeft()
        print("handling task ui events")

        self.initItems(index, pos)
        tevent = self.layout.handleEvent(event)
        self.endItems(index)
        return tevent

    def initItems(self, index: QModelIndex, pos: QPoint):

        model = index.model()

        if not self.render.init(index.data(self.DataRoles.RENDER)):
            model.setData(index, self.render.end(), self.DataRoles.RENDER)

        if not self.remove.init(index.data(self.DataRoles.REMOVE)):
            model.setData(index, self.render.end(), self.DataRoles.RENDER)

        self.layout.computeLayout(pos)

    def endItems(self, index: QModelIndex):
        model = index.model()
        model.setData(index, self.render.end(), self.DataRoles.RENDER)

    @staticmethod
    def paintBackground(
        painter: QPainter, rect: QRect, border_col: QColor, fill_col: QColor
    ):
        painter.save()

        # Paint Background
        painter.setPen(Qt.NoPen)
        painter.fillRect(rect, fill_col)

        # Paint Borders
        topLine = QLine(rect.topLeft(), rect.topRight())
        bottLine = QLine(rect.bottomLeft(), rect.bottomRight())

        borderPen = QPen(border_col, 3)
        borderPen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(borderPen)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawLine(topLine)
        painter.drawLine(bottLine)

        painter.restore()
