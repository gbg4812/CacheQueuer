from PySide2.QtCore import QSize, QPoint, QRect
from PySide2.QtGui import QPainter, QPixmap 
from global_enums import *
from .delegate_sub_item import DelegateSubItem

class IconButton(DelegateSubItem):
    def __init__(self, icon: QPixmap, size: QSize = None, pos: QPoint = QPoint(0, 0)):
        if not size:
            size = icon.size()
        super(IconButton, self).__init__(pos, size)
        self.icon = {WidgetState.ENABLED: icon, }

    def addStateIcon(self, state: WidgetState, icon: QPixmap) -> None:
        self.icon[state] = icon

    def addStateIcons(self, icons: dict) -> None:
        for key in icons.keys():
            self.icon[key] = icons[key]

    def draw(self, state: WidgetState, painter: QPainter) -> QPixmap:
        try:
            icon = self.icon[state]
        except KeyError:
            icon = self.icon[WidgetState.ENABLED]

        rect = self
        #rect.moveTo(rect.center())
        #rect.setSize(icon.size())
        #rect.translate(-rect.width() / 2, -rect.height() / 2)
        print("Size: {} Pos: {}".format(rect.size(), rect.topLeft()))
        painter.drawPixmap(rect, icon)

    def getIconSize(self, state: WidgetState) -> QSize:
        return self.icon.get(state).size()