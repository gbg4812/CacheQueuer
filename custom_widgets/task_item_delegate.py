from PySide2.QtWidgets import (QStyledItemDelegate, QLabel, QPushButton, QStyleOptionViewItem,
                               QHBoxLayout, QWidget, QStyleOptionButton, QStyle, QApplication, QStyleOptionComboBox, QComboBox, QCheckBox, QStyleOptionFocusRect, QLineEdit)
from PySide2.QtCore import QModelIndex, QPoint, Qt, QJsonValue, QSize, QRect, QAbstractItemModel, QEvent, Signal
from PySide2.QtGui import QPainter, QRegion, QMouseEvent, QPixmap


from .task_item_widget import TaskItemWidget
from .dir_item_widget import DirItemWidget
from .global_enums import CustomRoles, TaskEvent, ItemTypes, WidgetState, TaskState
from .hou_task_renderer import HouRenderer

import threading


class TaskDelegate(QStyledItemDelegate):
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

    def editorEvent(self, event: QEvent, model: QAbstractItemModel, option: QStyleOptionViewItem, index: QModelIndex) -> bool:

        task_event = None
        if index.data(CustomRoles.ItemType) == ItemTypes.TaskItem:
            task_event = self.TaskWidget.eventHandler(event, model, option, index)
            if task_event == TaskEvent.DELETE:
                return model.removeRow(index.row(), index.parent())
            
            elif task_event == TaskEvent.RENDER:
                for thread in threading.enumerate():
                    if thread.getName() == "RenderThread":
                        print("alredy rendering")
                        return False

                render_thread = threading.Thread(target=HouRenderer.render_task, name="RenderThread", args=(index.data(CustomRoles.TaskData),))
                render_thread.start()

                return True
        elif index.data(CustomRoles.ItemType) == ItemTypes.DirItem:
            task_event = self.DirWidget.eventHandler(event, model, option, index)
            if task_event == TaskEvent.DELETE:
                return model.removeRow(index.row(), index.parent())
            
            elif task_event == TaskEvent.RENDER:
                dependent = index.data(CustomRoles.DependentState)
                child_data = []
                for child in range(model.rowCount(index)):
                    child_index = model.index(child, 0, index)
                    child_data.append(model.data(child_index, CustomRoles.TaskData))
                
                for thread in threading.enumerate():
                    if thread.getName() == "RenderThread":
                        print("alredy rendering")
                        return False

                render_thread = threading.Thread(target=HouRenderer.render_task, name="RenderThread", args=(child_data,))
                render_thread.start()
                return True 
        return super().editorEvent(event, model, option, index)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        return self.DirWidget.createEditor(parent, option, index)