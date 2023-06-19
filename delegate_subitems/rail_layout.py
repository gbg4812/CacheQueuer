# std imports:
import logging
from typing import List, Optional

# PySide2 imports:
from PySide2.QtCore import QModelIndex, QSize, QPoint, QEvent, Qt

from global_enums import TaskState

# local imports:
from .delegate_sub_item import DelegateSubItem
from custom_types import Vec2


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# RailLayout is a tool class usefull to stack QRects in the left and rigth of a bounding QRect:
class RailLayout:
    def __init__(self, margin, spacing):
        # Tracker Variables
        self.right_pile: List[DelegateSubItem] = []
        self.left_pile: List[DelegateSubItem] = []
        self.size = Vec2(0, 0)
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
        return QSize(self.size.x, self.size.y)

    def setWidth(self, width: int):
        if width > self.size.x:
            dx = 0
            for ritem in self.right_pile:
                dx = width - self.size.x
                ritem.moveRight(ritem.right() + dx)
            self.size.x = width
            self.left_pile[len(self.left_pile) - 1].adjust(0, 0, dx, 0)

    def computeLayout(self, pos: QPoint = QPoint(0, 0)) -> None:
        l_ptr = self.margin
        r_ptr = 0
        self.size.x = 0
        self.size.y = 0
        if pos.x or pos.y:
            self.pos.x = pos.x()
            self.pos.y = pos.y()

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

        r_ptr = self.size.x - self.margin

        # Move items into position
        for litem in self.left_pile:
            litem.moveLeft(l_ptr)
            l_ptr += litem.width() + self.spacing
            litem.moveBottom(self.size.y - ((self.size.y - litem.height()) / 2))
            litem.translate(pos)

        for ritem in self.right_pile:
            ritem.moveRight(r_ptr)
            r_ptr -= ritem.width() + self.spacing
            ritem.moveBottom(self.size.y - ((self.size.y - ritem.height()) / 2))
            ritem.translate(pos)

    def draw(self, painter):
        for item in self.right_pile:
            item.draw(painter)

        for item in self.left_pile:
            item.draw(painter)

    def handleEvent(self, event: QEvent) -> Optional[TaskState]: 
        result_ev = None
        for item in self.right_pile:
            result_ev = item.handleEvent(event)
            if result_ev:
                return result_ev
        for item in self.left_pile:
            result_ev = item.handleEvent(event)
            if result_ev:
                return result_ev
         
