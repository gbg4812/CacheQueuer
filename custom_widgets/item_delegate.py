from PySide2.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QWidget
                             
from PySide2.QtCore import QModelIndex, QSize, QAbstractItemModel, QEvent, Signal
from PySide2.QtGui import QPainter 


from .task_item_widget import TaskItemWidget
from .dir_item_widget import DirItemWidget
from global_enums import CustomRoles, ItemTypes,TaskState, TaskEvent

class TaskDelegate(QStyledItemDelegate):
    render_dir = Signal(QModelIndex)
    render_task = Signal(QModelIndex)
    data_changed = Signal()

    def __init__(self, parent=None):
        super(TaskDelegate, self).__init__(parent)
        self.DirWidget = DirItemWidget()
        self.TaskWidget = TaskItemWidget()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:

        if index.data(CustomRoles.ItemType) == ItemTypes.TaskItem:
            self.TaskWidget.paint(painter, option, index)
        elif index.data(CustomRoles.ItemType) == ItemTypes.DirItem:
            self.DirWidget.paint(painter, option, index)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        if index.data(CustomRoles.ItemType) == ItemTypes.TaskItem:
            return self.TaskWidget.sizeHint(option, index)

        elif index.data(CustomRoles.ItemType) == ItemTypes.DirItem:
            return self.DirWidget.sizeHint(option, index)

        return super().sizeHint(option, index)

    def editorEvent(self, event: QEvent, model: QAbstractItemModel, option: QStyleOptionViewItem, index: QModelIndex) -> bool:

        task_event = None
        if index.data(CustomRoles.ItemType) == ItemTypes.TaskItem:
            task_event = self.TaskWidget.eventHandler(event, model, option, index)
            if task_event == TaskEvent.DELETE:
                return model.removeRow(index.row(), index.parent())
            
            elif task_event == TaskEvent.RENDER:
                super().editorEvent(event, model, option, index)
                self.render_task.emit(index) 
                return True

            elif task_event == TaskEvent.DATACHANGED:
                self.data_changed.emit()
        
        elif index.data(CustomRoles.ItemType) == ItemTypes.DirItem:
            task_event = self.DirWidget.eventHandler(event, model, option, index)
            if task_event == TaskEvent.DELETE:
                return model.removeRow(index.row(), index.parent())
            
            elif task_event == TaskEvent.RENDER:
                super().editorEvent(event, model, option, index)
                self.render_dir.emit(index)
                return True

            elif task_event == TaskEvent.DATACHANGED:
                self.data_changed.emit()

        return super().editorEvent(event, model, option, index)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        if index.data(CustomRoles.ItemType) == ItemTypes.DirItem: 
            return self.DirWidget.createEditor(parent, option, index)

        elif index.data(CustomRoles.ItemType) == ItemTypes.TaskItem: 
            return self.TaskWidget.createEditor(parent, option, index)

        else:
            return super().createEditor(parent, option, index)
    
    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        if index.data(CustomRoles.ItemType) == ItemTypes.DirItem:
            return self.DirWidget.updateEditorGeometry(editor, option, index)

        elif index.data(CustomRoles.ItemType) == ItemTypes.TaskItem:
            return self.TaskWidget.updateEditorGeometry(editor, option, index)

        return super().updateEditorGeometry(editor, option, index)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        self.data_changed.emit()
        return super().setEditorData(editor, index)
