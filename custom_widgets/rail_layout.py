# std imports:
import logging


# PySide2 imports:
from PySide2.QtCore import QSize, QPoint, QRect
from PySide2.QtGui import QPainter

# local imports:
from .delegate_sub_item import DelegateSubItem

# RailLayout is a tool class usefull to stack QRects in the left and rigth of a bounding QRect:
class RailLayout():
    def __init__(self):
        # Tracker Variables
        self.right_pile = []
        self.left_pile = []
        self.rWidth_ptr = 0
        self.lWidth_ptr = 0
        self.height = 0
        self.width = 0
        
        # margins between items and with the bounding rect
        self.margins = (5, 5)

    # add and item to the left pile and increment the with and maybe the height 
    def addItemLeft(self, item: DelegateSubItem):
        # increment the height
        if(self.height < item.height()):
            self.height = item.height()

            # adjust the y position of the other items in the pile
            for litem in self.left_pile:
                litem : DelegateSubItem
                bottom = self.height - ((self.height - litem.height()) / 2)
                litem.moveBottom(bottom)

            logging.debug("The object {} is higher".format(len(self.left_pile)))

        # move item to the top of the pile
        item.moveLeft(self.lWidth_ptr)

        # increment the total width of the bounds and the pile poninter
        self.lWidth_ptr += item.width()
        self.width += item.width()

        # add item to the pile
        self.left_pile.append(item)

    def addItemRight(self, item: DelegateSubItem):
        if(self.height < item.height()):
            self.height = item.height()
        self.width += item.width()
        item.moveRight(self.width - self.rWidth_ptr)
        print("New Right button position is: {} and the item width is: {}".format(item.topRight(), self.width))
        self.rWidth_ptr += item.width()
        
        for ritem in self.right_pile:
            ritem : DelegateSubItem
            bottom = self.height - ((self.height - ritem.height()) / 2)
            ritem.translate(item.width(), 0)
            ritem.moveBottom(bottom)

        self.right_pile.append(item)
    
    def sizeHint(self) -> QSize:
        print("size hint: {},{}".format(self.width, self.height))
        return QSize(self.width, self.height)

    def adaptToWidth(self, width: int):
        for ritem in self.right_pile:
            ritem : DelegateSubItem
            print("The Button Old PositionRight is: {} and the Item Old width: {}".format(ritem.topRight(), self.width))
            dx = width - self.width
            ritem.moveRight(ritem.right() + dx)
            print("The Button New PositionRight is: {} and the Item New width: {}".format(ritem.topRight(), width))
        self.width = width

    def updateFromContents(self) -> None:
        self.width = 0
        self.height = 0
        self.lWidth_ptr = 0
        self.rWidth_ptr = 0
        for item in self.left_pile:
            item : DelegateSubItem
            self.height = max(self.height, item.height())
            self.width += item.width()

        for item in self.right_pile:
            item : DelegateSubItem
            self.height = max(self.height, item.height())
            self.width += item.width()

        for litem in self.left_pile:
            litem : DelegateSubItem
            litem.moveLeft(self.lWidth_ptr)
            self.lWidth_ptr += litem.width()
            
            litem.moveBottom((self.height - litem.height() ) / 2)

        for ritem in self.right_pile:
            ritem : DelegateSubItem
            ritem.moveRight(self.width - self.rWidth_ptr)
            self.rWidth_ptr += ritem.width()
            
            ritem.moveBottom((self.height - ritem.height() ) / 2)
    def drawItems(self, painter):
        for item in self.right_pile:
            item : DelegateSubItem
            item.draw(painter)

        for item in self.left_pile:
            item : DelegateSubItem
            item.draw(painter)