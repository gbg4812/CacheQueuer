from PySide2.QtCore import QSize, QPoint, QRect
from PySide2.QtGui import QPainter
from .delegate_sub_item import DelegateSubItem


class RailLayout():
    def __init__(self):
        self.right_pile = []
        self.left_pile = []
        self.rWidth_ptr = 0
        self.lWidth_ptr = 0
        self.height = 0
        self.width = 0
        self.margins = (5, 5)
    
    def addItemLeft(self, item: DelegateSubItem):
        if(self.height < item.height()):
            self.height = item.height()
            print("The object {} is higher".format(len(self.left_pile)))
        item.moveLeft(self.lWidth_ptr)

        self.lWidth_ptr += item.size().width()
        self.width += item.size().width()
        
        for litem in self.left_pile:
            bottom = self.height - ((self.height - litem.height()) / 2)
            litem.moveBottom(bottom)

        self.left_pile.append(item)

    def addItemRight(self, item: DelegateSubItem):
        if(self.height < item.height()):
            self.height = item.height()
        item.moveRight(self.width - self.rWidth_ptr)
        self.width += item.width()
        self.rWidth_ptr += item.width()
        
        for ritem in self.right_pile:
            bottom = self.height - ((self.height - ritem.height()) / 2)
            ritem.moveBottom(bottom)

        self.right_pile.append(item)
    
    def sizeHint(self) -> QSize:
        print("size hint: {},{}".format(self.width, self.height))
        return QSize(self.width, self.height)

    def adaptToWidth(self, width: int):
        for litem in self.right_pile:
            litem.translate(width - self.width, 0)
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