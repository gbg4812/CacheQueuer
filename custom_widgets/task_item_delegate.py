from PySide2.QtWidgets import QStyledItemDelegate, QLabel, QPushButton, QStyleOptionViewItem, QHBoxLayout, QWidget, QStyleOptionButton, QStyle, QApplication, QStyleOptionComboBox
from PySide2.QtCore import QModelIndex, QPoint, Qt, QJsonValue, QSize, QRect, QAbstractItemModel, QEvent
from PySide2.QtGui import QPainter, QRegion, QMouseEvent

class TaskDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(TaskDelegate, self).__init__(parent)
        self.rm_button = QStyleOptionButton()
        self.rm_button.text = "Remove"
        self.rm_button.state = QStyle.State_Enabled
        self.state_menu = QStyleOptionComboBox()
        self.state_menu.state = QStyle.State_Enabled
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        rect : QRect = option.rect
        data : dict = index.model().data(index, Qt.DisplayRole)
        painter.save()
        self.rm_button.rect = rect.adjusted(2,2,-2, -2)
        self.rm_button.state |= QStyle.State_Enabled
        self.rm_button.text = "Remove"

        self.state_menu.rect = rect.adjusted(2, 2, -2, -2)

        #QApplication.style().drawControl(QStyle.CE_PushButton, self.rm_button, painter)
        QApplication.style().drawComplexControl(QStyle.CC_ComboBox, self.state_menu, painter)

        painter.restore()
    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return QSize(200, 40) 

    def editorEvent(self, event: QEvent, model: QAbstractItemModel, option: QStyleOptionViewItem, index: QModelIndex) -> bool:
        rm_rect : QRect = option.rect.adjusted(2, 2, -2, -2)
        if event.type() == QEvent.Type.MouseButtonPress:
            press_e : QMouseEvent = event
            if rm_rect.contains(press_e.pos()):
                self.rm_button.state = QStyle.State_Sunken
        elif event.type() == QEvent.Type.MouseButtonRelease:
            release_e : QMouseEvent = event
            if rm_rect.contains(release_e.pos()):
                self.rm_button.state = QStyle.State_Enabled
        else:
            self.rm_button.state = QStyle.State_Enabled
            
        return True