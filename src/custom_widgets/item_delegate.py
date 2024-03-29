# std imports
from enum import IntEnum

# PySide imports
from PySide6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QWidget
from PySide6.QtCore import QModelIndex, QSize, QAbstractItemModel, QEvent, Signal 
from PySide6.QtGui import QPainter, QStandardItemModel 

# local imports
from .task_ui import TaskUi
from global_enums import DataRoles
from utils import Logger, Level

flog = Logger(__name__, Level.ERROR)



class ItemDelegate(QStyledItemDelegate):
    render_dir = Signal(QModelIndex)
    render_task = Signal(QModelIndex)
    data_changed = Signal()

    class UiTypes(IntEnum):
        TASK_ITEM = 0
        DIR_ITEM = 1
        HEADER_ITEM = 2


    def __init__(self, parent=None):
        super(ItemDelegate, self).__init__(parent)
        self.task_ui = TaskUi()

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        if index.data(DataRoles.TYPE) == self.UiTypes.TASK_ITEM:

            flog.debug("Painting a Task")
            self.task_ui.draw(painter, option, index)

        elif index.data(DataRoles.TYPE) == self.UiTypes.DIR_ITEM:
            pass


    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        if index.data(DataRoles.TYPE) == self.UiTypes.TASK_ITEM:
            return self.task_ui.sizeHint(option, index)

        elif index.data(DataRoles.TYPE) == self.UiTypes.DIR_ITEM:
            pass

        return super().sizeHint(option, index)

    def editorEvent(
        self,
        event: QEvent,
        model: QAbstractItemModel,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> bool:
        task_event = None
        if index.data(DataRoles.TYPE) == self.UiTypes.TASK_ITEM:
            task_event = self.task_ui.handleEvents(event, option, index)
            if task_event == TaskUi.UiEvents.REMOVE:
                super().editorEvent(event, model, option, index)
                return model.removeRow(index.row(), index.parent())

            elif task_event == TaskUi.UiEvents.RENDER:
                super().editorEvent(event, model, option, index)
                self.render_task.emit(index)
                return True

        # elif index.data(TaskUi.DataRoles.TYPE) == self.UiTypes.DIR_ITEM:
        #     if task_event == TaskUi.UiEvents.DELETE:
        #         return model.removeRow(index.row(), index.parent())
        #
        #     elif task_event == TaskUi.UiEvents.RENDER:
        #         super().editorEvent(event, model, option, index)
        #         self.render_dir.emit(index)
        #         return True
        #
        #     elif task_event == TaskUi.UiEvents.DATACHANGED:
        #         self.data_changed.emit()
        return False
        
    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        return self.task_ui.createEditor(parent, option, index)

    def updateEditorGeometry(
        self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        editor.setGeometry(option.rect)  # type: ignore

    def setModelData(self, editor: QWidget, model: QStandardItemModel, index: QModelIndex) -> None:
        flog.debug("Setting data")
        self.task_ui.setEditorData(editor, model, index)
        self.data_changed.emit()
