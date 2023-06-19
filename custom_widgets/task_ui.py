# std imports
from os import path
from enum import IntEnum
from typing import Any

# local imports
from delegate_subitems import DelegateUi, IconButton, RailLayout
from global_enums import TaskEvent

# vendor imports
from PySide2.QtGui import QPixmap, QPainter
from PySide2.QtCore import QPoint, QSize, QModelIndex, Qt, QEvent
from PySide2.QtWidgets import QStyleOption


class TaskUi(DelegateUi):
    class DataRoles(IntEnum):
        RENDER = Qt.UserRole + 2

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

        # Create Layout:
        self.layout.margin = 10
        self.layout.spacing = 10

        # Create Buttons:
        self.render = IconButton(QSize(36, 36), paint_rect=True, radius=5)
        self.render.onReleaseReturn(TaskEvent.RENDER)
        self.render.addStateColors(state_colors)
        self.render.addIcon(
            "self.render", QPixmap(wrkdir + "res/icons/self.render.png")
        )
        self.layout.addLItem(self.render)

    def draw(self, painter: QPainter, option: QStyleOption, index: QModelIndex):
        pos = option.rect.topLeft()  # type: ignore
        self.initItems(index, pos)
        self.layout.draw(painter)

    def sizeHint(self, option: QStyleOption, index: QModelIndex):
        pos = option.rect.topLeft()  # type: ignore
        self.initItems(index, pos)
        return self.layout.sizeHint()

    def handleEvents(self, event: QEvent, option: QStyleOption, index: QModelIndex) -> Any:
        pos = option.rect.topLeft()  # type: ignore
        self.initItems(index, pos)
        return self.layout.handleEvent(event)

    def initItems(self, index: QModelIndex, pos: QPoint):
        if not self.render.init(index.data(self.DataRoles.RENDER)):
            model = index.model()
            model.setData(index, self.render.end(), self.DataRoles.RENDER)

    
        self.layout.computeLayout(pos)
