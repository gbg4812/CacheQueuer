from __future__ import annotations
from os import path

from PySide2.QtWidgets import QStyleOptionViewItem, QStyleOptionButton, QApplication, QStyle, QLineEdit, QWidget, QPushButton, QStyleOption 
from PySide2.QtCore import Qt, QModelIndex, QRect, QAbstractItemModel, QSize, QMargins, QLine
from PySide2.QtGui import QPainter, QMouseEvent , QPixmap, QColor, QPainterPath, QPen

from global_enums import *
from delegate_subitems import WidgetState, IconButton, RailLayout, TextItem

wrkdir, _ = path.split(__file__)
wrkdir += "/"

#TaskItemWidget is a class that paints and handles events of a task item
class TaskItemWidget():
    def __init__(self):
        super(TaskItemWidget, self).__init__()

        self.button_size = QSize(30, 30)
        self.content_margins = QMargins(5, 5, 20, 5)

        self.remove = IconButton(
            QPixmap(wrkdir + "res/icons/remove.png"), WidgetState.ENABLED)
        self.remove.addStateIcon(WidgetState.CLICKED, QPixmap(
            wrkdir +"res/icons/remove_shunken.png"))
        self.render = IconButton(QPixmap(wrkdir +"res/icons/render.png"), WidgetState.ENABLED)
        self.render.addStateIcon(WidgetState.CLICKED, QPixmap(
            wrkdir +"res/icons/render_shunken.png"))
        self.enable = IconButton(QPixmap(wrkdir +"res/icons/enable_on.png"), WidgetState.ENABLED)
        self.enable.addStateIcon(WidgetState.DISABLED, QPixmap(wrkdir +"res/icons/enable_off.png"))

        self.name = TextItem(text_size=12)
        
        self.layout = RailLayout(5, 5) 
        self.layout.addLItem(self.enable)
        self.layout.addLItem(self.name)
        
        self.layout.addRItem(self.remove)
        self.layout.addRItem(self.render)
        self.layout.computeLayout()


    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        rect : QRect = option.rect.marginsRemoved(self.content_margins)

        primary3 = QColor('#7ec0d1')
        border1 = QColor('#6b98a5')

        
        if (option.state & QStyle.State_Selected):
            TaskItemWidget.paintBackground(painter, rect, border1, primary3)
        else:
            TaskItemWidget.paintBackground(painter, rect, border1, primary3)
            
            


        # Prepare paint region
        painter.save()
        self.name.setText(index.data(CustomRoles.TaskName))

        # Layout and  paint enabled checkbox
        self.enable.setCurrentState(index.data(CustomRoles.EnableState))

        # Layout and  paint remove button
        self.remove.setCurrentState(index.data(CustomRoles.RemoveState))

        # Layout and  paint render button
        self.render.setCurrentState(index.data(CustomRoles.RenderState))

        # Compute items positions
        self.layout.computeLayout(rect.topLeft())
        self.layout.setWidth(rect.width())

        # Layout and paint name
        self.layout.draw(painter)
        painter.restore()
        
            

    def eventHandler(self, event: QMouseEvent, model: QAbstractItemModel, option: QStyleOptionViewItem, index: QModelIndex) -> TaskEvent:
        rect : QRect = option.rect.marginsRemoved(self.content_margins)

        pos = event.pos()
        self.name.setText(index.data(CustomRoles.TaskName))

        self.layout.computeLayout(rect.topLeft())
        self.layout.setWidth(rect.width())
        enable_state = index.data(CustomRoles.EnableState)
        render_state = index.data(CustomRoles.RenderState)
        remove_state = index.data(CustomRoles.RemoveState)


        # Handle mouse button press
        if event.type() == QMouseEvent.Type.MouseButtonPress:

            # Handle remove button
            if self.remove.contains(pos):
                model.setData(index, WidgetState.CLICKED,
                              CustomRoles.RemoveState)
            elif self.render.contains(pos):
                model.setData(index, WidgetState.CLICKED,
                              CustomRoles.RenderState)
            return TaskEvent.NONE

        # Handle mouse button release
        elif event.type() == QMouseEvent.Type.MouseButtonRelease:

            if remove_state == WidgetState.CLICKED:
                model.setData(index, WidgetState.ENABLED, CustomRoles.RemoveState)
                return TaskEvent.DELETE

            elif render_state == WidgetState.CLICKED:
                model.setData(index, WidgetState.ENABLED, CustomRoles.RenderState)
                return TaskEvent.RENDER
            # Handle checkboxes

            if self.enable.contains(pos):
                if enable_state & WidgetState.ENABLED:
                    model.setData(index, WidgetState.DISABLED,
                                  CustomRoles.EnableState)
                elif enable_state & WidgetState.DISABLED:
                    model.setData(index, WidgetState.ENABLED,
                                  CustomRoles.EnableState)

        elif event.type() == QMouseEvent.Type.MouseButtonDblClick:

            # Default button state
            model.setData(index, WidgetState.ENABLED, CustomRoles.RemoveState)
            model.setData(index, WidgetState.ENABLED, CustomRoles.RenderState)

            if self.name.contains(pos):
                model.setData(index, True, CustomRoles.EditName)
            else:
                model.setData(index, False, CustomRoles.EditName)
        
        # Default button state
        model.setData(index, WidgetState.ENABLED, CustomRoles.RemoveState)
        model.setData(index, WidgetState.ENABLED, CustomRoles.RenderState)

        return TaskEvent.DATACHANGED

    def sizeHint(self, option: QStyleOption, index: QModelIndex) -> QSize:
        self.name.setText(index.data(CustomRoles.TaskName))
        self.layout.computeLayout()
        return self.layout.sizeHint().grownBy(self.content_margins)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        if index.data(CustomRoles.EditName):
            editor = QLineEdit(parent)
            return editor
        else:
            return None
    
    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        rect : QRect = option.rect.marginsRemoved(self.content_margins)
        editor.setGeometry(rect)
    
    def paintBackground(painter: QPainter, rect: QRect, border_col: QColor, fill_col: QColor):
        painter.save()

        #Paint Background
        painter.setPen(Qt.NoPen)
        painter.fillRect(rect, fill_col)

        #Paint Borders
        topLine = QLine(rect.topLeft(), rect.topRight())
        bottLine = QLine(rect.bottomLeft(), rect.bottomRight())

        borderPen = QPen(border_col, 3)
        borderPen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(borderPen)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawLine(topLine)
        painter.drawLine(bottLine)

        painter.restore()

