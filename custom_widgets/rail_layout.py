# std imports:
import logging
from typing import List
logging.disable(level=logging.WARNING)

# PySide2 imports:
from PySide2.QtCore import QSize,QMargins

# local imports:
from .delegate_sub_item import DelegateSubItem

# RailLayout is a tool class usefull to stack QRects in the left and rigth of a bounding QRect:
class RailLayout():
    def __init__(self):
        # Tracker Variables
        self.right_pile : List[DelegateSubItem] = []
        self.left_pile : List[DelegateSubItem] = []
        self.rWidth_ptr = 0
        self.lWidth_ptr = 0
        self.height = 0
        self.width = 0
        
        # margins between items and with the bounding rect
        self.margins = QMargins(5, 5, 5, 5)

    # add and item to the left pile and increment the with and maybe the height 
    def addItemLeft(self, item: DelegateSubItem):
        # increment the height
        if(self.height < item.height()):
            self.height = item.height()

        # add item to the pile
        self.left_pile.append(item)

    def addItemRight(self, item: DelegateSubItem):
        if(self.height < item.height()):
            self.height = item.height()
        self.right_pile.append(item)
    
    def sizeHint(self) -> QSize:
        return QSize(self.width, self.height)


    def adaptToWidth(self, width: int):
        for ritem in self.right_pile:
            ritem : DelegateSubItem
            logging.debug("The Button Old PositionRight is: {} and the Item Old width: {}".format(ritem.topRight(), self.width))
            dx = width - self.width
            ritem.moveRight(ritem.right() + dx)
            logging.debug("The Button New PositionRight is: {} and the Item New width: {}".format(ritem.topRight(), width))
        self.width = width

    def updateFromContents(self) -> None:
        self.width = 0
        self.height = 0
        self.lWidth_ptr = 0
        self.rWidth_ptr = 0
        
        #Compute max height and total width
        for item in self.left_pile:
            self.height = max(self.height, item.height())
            self.width += item.width() + self.margins.left()

        for item in self.right_pile:
            self.height = max(self.height, item.height())
            self.width += item.width() + self.margins.left()
            
        self.height += self.margins.top() * 2
        self.width += self.margins.left()
        self.lWidth_ptr += self.margins.left()
        self.rWidth_ptr += self.margins.left()

        # Move items into position
        for litem in self.left_pile:
            litem.moveLeft(self.lWidth_ptr)
            self.lWidth_ptr += litem.width() + self.margins.left()
            
            litem.moveBottom(self.height - ((self.height - litem.height()) / 2))

        for ritem in self.right_pile:
            ritem.moveRight(self.width - self.rWidth_ptr)
            self.rWidth_ptr += ritem.width() + self.margins.left()
            
            ritem.moveBottom(self.height - ((self.height - ritem.height()) / 2))

        print("adapted from contents")

    def drawItems(self, painter):
        for item in self.right_pile:
            item : DelegateSubItem
            item.draw(painter)

        for item in self.left_pile:
            item : DelegateSubItem
            item.draw(painter)