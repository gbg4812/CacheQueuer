from PySide2.QtWidgets import (QStyledItemDelegate, QLabel, QPushButton, QStyleOptionViewItem, 
                               QHBoxLayout, QWidget, QStyleOptionButton, QStyle, QApplication, QStyleOptionComboBox, QComboBox, QCheckBox)
from PySide2.QtCore import QModelIndex, QPoint, Qt, QJsonValue, QSize, QRect, QAbstractItemModel, QEvent
from PySide2.QtGui import QPainter, QRegion, QMouseEvent, QPixmap


from .task_item import TaskItemWidget 
class TaskDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(TaskDelegate, self).__init__(parent)
        self.widget = TaskItemWidget()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        rect : QRect = option.rect
        data : dict = index.model().data(index, Qt.DisplayRole)

        self.widget.setName(data.get("name"))
        self.widget.paint(painter, option, index)
        super().paint(painter, option, index)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return QSize(200, 40) 
    
    def editorEvent(self, event: QEvent, model: QAbstractItemModel, option: QStyleOptionViewItem, index: QModelIndex) -> bool:
        if event.type() == QEvent.Type.MouseButtonPress:
            self.widget.mousePressEvent(event, option)

        elif event.type()== QEvent.Type.MouseButtonRelease:
            self.widget.mouseReleaseEvent(event, option, index)

        return super().editorEvent(event, model, option, index)

