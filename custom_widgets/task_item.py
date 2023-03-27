from __future__ import annotations
import copy

from PySide2.QtWidgets import QStyleOptionViewItem, QStyleOptionButton, QApplication, QStyle
from PySide2.QtCore import Qt, Signal, QModelIndex, QRect, QPoint, QObject
from PySide2.QtGui import  QPainter, QMouseEvent
from .name_label_widget import NameLabelWidget

import enum

#Class defining the state of a task
class TaskState(enum.IntEnum):
    WAITING = 0
    RENDERING = 1
    SUCCESFUL = 2
    FAILED = 3
    DISABLED = 4


class TaskItemWidget(QObject):
    remove_clicked = Signal()
    render_clicked = Signal()
    def __init__(self):
        super(TaskItemWidget, self).__init__()

        self._enable = QStyleOptionButton()
        self._enable.state = QStyle.State_Enabled
        self._enable.state = QStyle.State_Off
        self._render = QStyleOptionButton()
        self._remove = QStyleOptionButton()
        self._name = ""

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        rect : QRect = copy.copy(option.rect)
        style = QApplication.style()
        painter.save()
        painter.translate(rect.topLeft())
        rect.moveTo(QPoint(0, 0))
        rect.adjust(rect.height()/2, 0, rect.height()/2, 0)
        
        #Layout and  paint _enabled checkbox
        self._enable.rect = rect.adjusted(0, 0, - rect.width()/3, 0)
        state = index.model().data(index, Qt.DisplayRole).get("state") 

        if state == TaskState.WAITING or state == TaskState.FAILED or state == TaskState.RENDERING:
            self._enable.state = QStyle.State_On | QStyle.State_Enabled
        elif state == TaskState.DISABLED or state == TaskState.SUCCESFUL:
            self._enable.state = QStyle.State_Off
        style.drawControl(QStyle.CE_CheckBox, self._enable, painter)
        
        #Layout and  paint render button
        self._render.rect = rect.adjusted(rect.width()/3, 0, - rect.width()/3, 0)
        style.drawControl(QStyle.CE_PushButton, self._render, painter)
        
        painter.restore()
    
    def setName(self, name: str) -> None:
        self._name = name 

    def mousePressEvent(self, event: QMouseEvent, option: QStyleOptionViewItem) -> bool:
        pos = event.pos()
        pos -= option.rect.topLeft()
        if self._remove.rect.contains(pos):
            self._remove.state = QStyle.State_Sunken
            self.remove_clicked.emit()
            return True
        elif self._render.rect.contains(pos):
            self._render.state = QStyle.State_Sunken
            self.render_clicked.emit()
            return True
        else:
            return False

    def mouseReleaseEvent(self, event: QMouseEvent, option: QStyleOptionViewItem, index: QModelIndex) -> bool:
        pos = event.pos()
        pos -= option.rect.topLeft()
        self._remove.state = QStyle.State_Enabled
        self._render.state = QStyle.State_Enabled

        task = index.data(Qt.DisplayRole)
        state =  task.get("state")

        enable_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxClickRect, self._enable)
        if enable_rect.contains(pos):
            print("Mouse Included")
            if state == TaskState.WAITING or state == TaskState.FAILED or state == TaskState.RENDERING:
                print("State Toggled")
                task["state"] = TaskState.DISABLED
            elif state == TaskState.DISABLED or state == TaskState.SUCCESFUL:
                print("State Toggled")
                task["state"] = TaskState.WAITING

            index.model().setData(index, task, Qt.DisplayRole)
            return True
        
        else:
            return False