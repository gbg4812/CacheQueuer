from PySide2.QtWidgets import (QStyledItemDelegate, QLabel, QPushButton, QStyleOptionViewItem,
                               QHBoxLayout, QWidget, QStyleOptionButton, QStyle, QApplication, QStyleOptionComboBox, QComboBox, QCheckBox, QStyleOptionFocusRect, QLineEdit)
from PySide2.QtCore import QModelIndex, QPoint, Qt, QJsonValue, QSize, QRect, QAbstractItemModel, QEvent, Signal
from PySide2.QtGui import QPainter, QRegion, QMouseEvent, QPixmap


from .task_item_widget import TaskItemWidget
from .dir_item_widget import DirItemWidget
from global_enums import *
from utils import ThreadingUtils

class TaskDelegate(QStyledItemDelegate):
    render_dir = Signal(QModelIndex)
    render_task = Signal(QModelIndex)
    def __init__(self, parent=None):
        super(TaskDelegate, self).__init__(parent)
        self.DirWidget = DirItemWidget()
        self.TaskWidget = TaskItemWidget()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        
        #Paint focus (selection) rect
        focus_rect = QStyleOptionViewItem()
        focus_rect.rect = option.rect
        focus_rect.state = option.state
        QApplication.style().drawControl(QStyle.CE_ItemViewItem, option, painter)

        if index.data(CustomRoles.ItemType) == ItemTypes.TaskItem:
            self.TaskWidget.paint(painter, option, index)
        elif index.data(CustomRoles.ItemType) == ItemTypes.DirItem:
            self.DirWidget.paint(painter, option, index)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        if index.data(CustomRoles.ItemType) == ItemTypes.TaskItem:
            return self.TaskWidget.sizeHint()
        elif index.data(CustomRoles.ItemType) == ItemTypes.DirItem:
            return self.DirWidget.sizeHint()
        elif index.data(CustomRoles.ItemType) == ItemTypes.HeaderItem:
            return super().sizeHint(option, index)

    def editorEvent(self, event: QEvent, model: QAbstractItemModel, option: QStyleOptionViewItem, index: QModelIndex) -> bool:

        task_event = None
        if index.data(CustomRoles.ItemType) == ItemTypes.TaskItem:
            task_event = self.TaskWidget.eventHandler(event, model, option, index)
            if task_event == TaskEvent.DELETE:
                return model.removeRow(index.row(), index.parent())
            
            elif task_event == TaskEvent.RENDER:
                self.render_task.emit(index) 
        elif index.data(CustomRoles.ItemType) == ItemTypes.DirItem:
            task_event = self.DirWidget.eventHandler(event, model, option, index)
            if task_event == TaskEvent.DELETE:
                return model.removeRow(index.row(), index.parent())
            
            elif task_event == TaskEvent.RENDER:
                self.render_dir.emit(index)
                return True
        return super().editorEvent(event, model, option, index)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        return self.DirWidget.createEditor(parent, option, index)