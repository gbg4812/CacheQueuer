from .delegate_sub_item import DelegateSubItem
from PySide2.QtCore import QPoint, QRect, QSize

class Spacer(DelegateSubItem):
    def __init__(self, width: int, height: int = 0):
        super().__init__(QPoint(0, 0), QSize(width, height))
    
    