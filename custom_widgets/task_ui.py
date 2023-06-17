# std imports
from os import path

# local imports
from delegate_subitems import DelegateUi, IconButton, RailLayout
from global_enums import TaskEvent

# vendor imports
from PySide2.QtGui import QPixmap, QPainter
from PySide2.QtCore import QSize, QModelIndex


class TaskUi(DelegateUi):
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

    def draw(self, painter: QPainter, index: QModelIndex):
        self.layout.initItems(index)
        return super().draw(painter)
