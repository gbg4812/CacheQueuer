# std imports:
import enum
from typing import List, Optional

# PySide6 imports:
from PySide6.QtCore import QModelIndex, QSize, QPoint, QEvent, Qt
from utils import Logger , Level

# local imports:
from .delegate_sub_item import DelegateSubItem
from custom_types import Vec2

flog = Logger(__name__, Level.ERROR)


# RailLayout is a tool class usefull to stack QRects in the left and rigth of a bounding QRect:
class RailLayout:
    def __init__(self, margin, spacing):
        # Tracker Variables
        self.right_pile: List[DelegateSubItem] = []
        self.left_pile: List[DelegateSubItem] = []
        self.size: Vec2[int] = Vec2(0, 0)
        self.pos = Vec2(0, 0)

        # margins between items and with the bounding rect
        self.margin = margin
        self.spacing = spacing

    # add and item to the left pile and increment the with and maybe the height
    def addLItem(self, item: DelegateSubItem):
        # increment the height
        if self.size.y < item.height():
            self.size.y = item.height()

        # add item to the pile
        self.left_pile.append(item)

    def addRItem(self, item: DelegateSubItem):
        # increment the height
        if self.size.y < item.height():
            self.size.y = item.height()

        # add item to the pile
        self.right_pile.append(item)

    def sizeHint(self) -> QSize:
        flog.debug("Size Hint Called: {}x, {}y".format(self.size.x, self.size.y))
        return QSize(self.size.x, self.size.y)

    def setWidth(self, width: int):
        flog.debug("layout size: {}, new size: {}".format(self.size.x, width))
        if width > self.size.x:
            dx = 0
            for ritem in self.right_pile:
                dx = width - self.size.x
                ritem.moveRight(ritem.right() + dx)
            self.size.x = width

    def computeLayout(self, width: int = 0, pos: QPoint = QPoint(0, 0)) -> None:
        l_ptr = self.margin
        r_ptr = 0
        self.size.x = 0
        self.size.y = 0
        if pos.x or pos.y:
            self.pos.x = pos.x()
            self.pos.y = pos.y()
        flog.debug("Position is: {}, {}".format(self.pos.x, self.pos.y))

        # Compute max height and total width
        self.size.x += self.margin

        for item in self.left_pile:
            self.size.y = max(self.size.y, item.height())
            self.size.x += item.width() + self.spacing

        self.size.x += self.margin

        for i, item in enumerate(self.right_pile):
            self.size.y = max(self.size.y, item.height())
            self.size.x += item.width()
            if i != len(self.right_pile) - 1:
                self.size.x += self.spacing

        self.size.y += 2 * self.margin
        flog.debug("Item size is: {}, {}".format(self.size.x, self.size.y))

        r_ptr = self.size.x - self.margin

        # Move items into position
        for litem in self.left_pile:
            litem.moveLeft(l_ptr)
            l_ptr += litem.width() + self.spacing
            litem.moveBottom(int(self.size.y - ((self.size.y - litem.height()) / 2)))
            litem.translate(pos)

        for ritem in self.right_pile:
            ritem.moveRight(r_ptr)
            r_ptr -= ritem.width() + self.spacing
            ritem.moveBottom(int(self.size.y - ((self.size.y - ritem.height()) / 2)))
            ritem.translate(pos)

        if width:
            self.setWidth(width)

    def draw(self, painter):
        for item in self.right_pile:
            item.draw(painter)

        for item in self.left_pile:
            item.draw(painter)

    def handleEvent(self, event: QEvent) -> Optional[enum.IntEnum]:
        result_ev = None
        for item in self.right_pile:
            result_ev = item.handleEvent(event)
            if result_ev:
                return result_ev
        for item in self.left_pile:
            result_ev = item.handleEvent(event)
            if result_ev:
                return result_ev
