# std imports
from os import path
from enum import IntEnum
from typing import Any, Optional

# local imports
from delegate_subitems import DelegateUi, IconButton, TextItem
from global_enums import DataRoles
from utils import Logger, Level
import config

# vendor imports
from PySide6.QtGui import QBrush, QColor, QPen, QPixmap, QPainter, QStandardItemModel
from PySide6.QtCore import (
    QMargins,
    QPoint,
    QSize,
    QModelIndex,
    Qt,
    QEvent,
    QRect,
    QLine,
)
from PySide6.QtWidgets import QLineEdit, QStyleOption, QStyle, QWidget

flog = Logger(__name__, level=Level.ERROR)


class TaskUi(DelegateUi):
    # The value is only a key, it doesn't mather so, 1+ values are fore general
    # roles and 100+ values for ui especific roles.
    class DataRoles(IntEnum):
        RENDER = 100
        REMOVE = 101
        ENABLE = 102
        DEPENDENT = 103
        NAME = 104

    class UiEvents(IntEnum):
        NONE = 0
        REMOVE = 1
        RENDER = 2
        DATACHANGED = 3

    def __init__(self) -> None:
        super().__init__()

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
        self.render = IconButton(QSize(40, 40), paint_rect=True, radius=5)
        self.render.onReleaseReturn(self.UiEvents.RENDER)
        self.render.addStateColors(state_colors)
        self.render.addIcon("render", QPixmap(config.ROOT_DIR + "/icons/render.png"))
        self.render.manualInit(IconButton.ButtonStates.NORMAL, "render")

        # Remove Button:
        self.remove = IconButton(QSize(40, 40), paint_rect=True, radius=5)
        self.remove.onReleaseReturn(self.UiEvents.REMOVE)
        self.remove.addStateColors(state_colors)
        self.remove.addIcon("remove", QPixmap(config.ROOT_DIR + "/icons/trash.png"))
        self.remove.manualInit(IconButton.ButtonStates.NORMAL, "remove")

        # Name
        self.name = TextItem(min_letters=10)
        self.name.setText("New Task")

        self.layout.addRItem(self.remove)
        self.layout.addRItem(self.render)
        self.layout.addLItem(self.name)
        self.layout.computeLayout()

    def draw(self, painter: QPainter, option: QStyleOption, index: QModelIndex):
        rect: QRect = option.rect.marginsRemoved(self.content_margins)

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

        self.initItems(index, rect)
        flog.debug("Width: {}".format(rect.width()))
        self.layout.draw(painter)

    def sizeHint(self, option: QStyleOption, index: QModelIndex):
        self.layout.computeLayout()
        return self.layout.sizeHint().grownBy(self.content_margins)

    def handleEvents(
        self, event: QEvent, option: QStyleOption, index: QModelIndex
    ) -> Any:
        rect: QRect = option.rect.marginsRemoved(self.content_margins)
        flog.debug("handling task ui events")

        self.initItems(index, rect)
        tevent = self.layout.handleEvent(event)
        self.endItems(index)
        return tevent

    def initItems(self, index: QModelIndex, rect: QRect):
        pos = rect.topLeft()
        model = index.model()

        if not self.render.init(index.data(self.DataRoles.RENDER)):
            model.setData(index, self.render.end(), self.DataRoles.RENDER)

        if not self.remove.init(index.data(self.DataRoles.REMOVE)):
            model.setData(index, self.remove.end(), self.DataRoles.REMOVE)

        if not self.name.init(index.data(self.DataRoles.NAME)):
            model.setData(index, self.name.end(), self.DataRoles.NAME)

        self.name.setText(index.data(DataRoles.NAME))
        self.layout.computeLayout(rect.width(), pos)

    def endItems(self, index: QModelIndex):
        model = index.model()
        model.setData(index, self.render.end(), self.DataRoles.RENDER)
        model.setData(index, self.remove.end(), self.DataRoles.REMOVE)
        model.setData(index, self.name.end(), self.DataRoles.NAME)

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

    def createEditor(self, parent: QWidget, option: QStyleOption, index: QModelIndex) -> Optional[QWidget]:
        editor = QLineEdit(parent)
        editor.setText(index.data(DataRoles.NAME))
        return editor

    def setEditorData(self, editor: QWidget, model: QStandardItemModel, index: QModelIndex) -> None:
        line_edit : QLineEdit = editor
        model.setData(index, line_edit.text(), DataRoles.NAME)
