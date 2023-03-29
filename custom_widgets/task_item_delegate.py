from PySide2.QtWidgets import (QStyledItemDelegate, QLabel, QPushButton, QStyleOptionViewItem,
                               QHBoxLayout, QWidget, QStyleOptionButton, QStyle, QApplication, QStyleOptionComboBox, QComboBox, QCheckBox, QStyleOptionFocusRect, QLineEdit)
from PySide2.QtCore import QModelIndex, QPoint, Qt, QJsonValue, QSize, QRect, QAbstractItemModel, QEvent
from PySide2.QtGui import QPainter, QRegion, QMouseEvent, QPixmap


from .task_item_widget import TaskItemWidget

class TaskDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(TaskDelegate, self).__init__(parent)
        self.widget = TaskItemWidget()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:

        focus_rect = QStyleOptionViewItem()
        focus_rect.rect = option.rect
        focus_rect.state = option.state
        QApplication.style().drawControl(QStyle.CE_ItemViewItem, option, painter)

        self.widget.paint(painter, option, index)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return self.widget.sizeHint()        

    def editorEvent(self, event: QEvent, model: QAbstractItemModel, option: QStyleOptionViewItem, index: QModelIndex) -> bool:

        self.widget.eventHandler(event, model, option, index)

        return super().editorEvent(event, model, option, index)
    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        return self.widget.createEditor(parent, option, index)