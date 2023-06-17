from os import path
from PySide2.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QWidget
                             
from PySide2.QtCore import QModelIndex, QSize, QAbstractItemModel, QEvent, Signal
from PySide2.QtGui import QPainter, QPixmap
from delegate_subitems import IconButton, RailLayout 


from global_enums import CustomRoles, ItemTypes,TaskState, TaskEvent

class TaskDelegate(QStyledItemDelegate):
    render_dir = Signal(QModelIndex)
    render_task = Signal(QModelIndex)
    data_changed = Signal()

    def __init__(self, parent=None):
        super(TaskDelegate, self).__init__(parent)
        self.dir_layout = self.dirLayout()
        self.task_layout = self.taskLayout()



    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:


        if index.data(CustomRoles.ItemType) == ItemTypes.TaskItem:
            layout = self.taskLayout(index)

        elif index.data(CustomRoles.ItemType) == ItemTypes.DirItem:
            layout = self.dirLayout(index)

        layout.draw(painter)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        if index.data(CustomRoles.ItemType) == ItemTypes.TaskItem:
            layout = self.taskLayout(index)
            return layout.sizeHint()

        elif index.data(CustomRoles.ItemType) == ItemTypes.DirItem:
            layout = self.dirLayout(index) 
            return layout.sizeHint()

        return super().sizeHint(option, index)

    def editorEvent(self, event: QEvent, model: QAbstractItemModel, option: QStyleOptionViewItem, index: QModelIndex) -> bool:

        task_event = None
        if index.data(CustomRoles.ItemType) == ItemTypes.TaskItem:
            task_event = self.taskLayout(index).handleEvent(event)
            if task_event == TaskEvent.DELETE:
                return model.removeRow(index.row(), index.parent())
            
            elif task_event == TaskEvent.RENDER:
                super().editorEvent(event, model, option, index)
                self.render_task.emit(index) 
                return True

            elif task_event == TaskEvent.DATACHANGED:
                self.data_changed.emit()
        
        elif index.data(CustomRoles.ItemType) == ItemTypes.DirItem:
            task_event = self.dirLayout(index).handleEvent(event) 
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
        return super().createEditor(parent, option, index)
    
    def updateEditorGeometry(self, editor: QWidget,
                             option: QStyleOptionViewItem, index: QModelIndex) -> None:

        editor.setGeometry(option.rect) #type: ignore
        return super().updateEditorGeometry(editor, option, index)

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        self.data_changed.emit()
        return super().setEditorData(editor, index)
    



