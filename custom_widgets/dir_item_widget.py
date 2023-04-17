
from __future__ import annotations
import copy
from PySide2.QtWidgets import QStyleOptionViewItem, QStyleOptionButton, QApplication, QStyle, QLineEdit, QWidget, QPushButton, QStyleOption
from PySide2.QtCore import Qt, QModelIndex, QRect, QAbstractItemModel, QSize, QMargins, QPoint
from PySide2.QtGui import QPainter, QMouseEvent, QIcon, QPainter, QPixmap, QPainterPath, QPen, QColor, QFontMetrics, QFont

from global_enums import *
from .icon_button import IconButton
from .text_item import TextItem
from .rail_layout import RailLayout

# TaskItemWidget is a class that paints and handles events of a dir item


class DirItemWidget():
    def __init__(self):
        super(DirItemWidget, self).__init__()

        self.button_size = QSize(30, 30)
        self.content_margins = QMargins(5, 5, 5, 5)

        self.remove = IconButton(
            QPixmap("res/icons/remove.png"))
        self.remove.addStateIcon(WidgetState.CLICKED, QPixmap(
            "res/icons/remove_shunken.png"))
        self.render = IconButton(QPixmap("res/icons/render.png"))
        self.render.addStateIcon(WidgetState.CLICKED, QPixmap(
            "res/icons/render_shunken.png"))
        self.enable = IconButton(QPixmap("res/icons/enable_on.png"))
        self.enable.addStateIcon(WidgetState.DISABLED, QPixmap("res/icons/enable_off.png"))
        self.dependent = IconButton(QPixmap("res/icons/dependent_on.png"))
        self.dependent.addStateIcon(WidgetState.DISABLED, QPixmap("res/icons/dependent_off.png"))
        self.name = TextItem(text_size=12)
        
        self.layout = RailLayout() 
        self.layout.addItemLeft(self.enable)
        self.layout.addItemLeft(self.dependent)
        self.layout.addItemLeft(self.name)


    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        option.rect.adjust(5, 5, -5, -5)

        # Paint focus (selection) rect
        fillColor = QColor('#4b5469')
        borderColor = QColor('#65708c')
        if (option.state & QStyle.State_Selected):
            fillColor = fillColor.lighter(120)
            borderColor = borderColor.lighter(120)

        painter.save()
        path = QPainterPath()
        path.addRoundRect(option.rect, 20)
        pen = QPen(borderColor, 3)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillPath(path, fillColor)
        painter.drawPath(path)
        painter.restore()

        # Prepare paint region
        painter.save()
        painter.translate(option.rect.topLeft())

        self.name.setText(index.data(CustomRoles.TaskName))
        self.layout.updateFromContents()
        self.layout.adaptToWidth(option.rect.width())

        # Layout and  paint enabled checkbox
        self.enable.draw(index.data(CustomRoles.EnableState), painter)

        # Layout and  paint dependent checkbox
        self.dependent.draw(index.data(CustomRoles.DependentState), painter)

        # Layout and  paint remove button
        self.remove.draw(index.data(CustomRoles.RemoveState), painter)

        # Layout and  paint render button
        self.render.draw(index.data(CustomRoles.RenderState), painter)

        # Layout and paint name
        self.name.draw(painter)
        painter.restore()

    def eventHandler(self, event: QMouseEvent, model: QAbstractItemModel, option: QStyleOptionViewItem, index: QModelIndex) -> TaskEvent:
        option.rect.adjust(5, 5, -5, -5)

        pos = event.pos()
        pos -= option.rect.topLeft()
        enable_state = index.data(CustomRoles.EnableState)
        dependent_state = index.data(CustomRoles.DependentState)

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

            # Handle buttons
            model.setData(index, WidgetState.ENABLED, CustomRoles.RemoveState)
            model.setData(index, WidgetState.ENABLED, CustomRoles.RenderState)

            if self.remove.contains(pos):
                return TaskEvent.DELETE
            elif self.render.contains(pos):
                return TaskEvent.RENDER

            # Handle checkboxes

            if self.enable.contains(pos):
                if enable_state & WidgetState.ENABLED:
                    model.setData(index, WidgetState.DISABLED,
                                  CustomRoles.EnableState)
                elif enable_state & WidgetState.DISABLED:
                    model.setData(index, WidgetState.ENABLED,
                                  CustomRoles.EnableState)

            if self.dependent.contains(pos):
                if dependent_state & WidgetState.ENABLED:
                    model.setData(index, WidgetState.DISABLED,
                                  CustomRoles.DependentState)
                elif dependent_state & WidgetState.DISABLED:
                    model.setData(index, WidgetState.ENABLED,
                                  CustomRoles.DependentState)

            return TaskEvent.NONE

        elif event.type() == QMouseEvent.Type.MouseButtonDblClick:

            if self.name.contains(pos):
                model.setData(index, True, CustomRoles.EditName)
            else:
                model.setData(index, False, CustomRoles.EditName)

        return TaskEvent.NONE

    def divideHRect(self, rect: QRect, chunks: int, spawns: list = None) -> list:
        result = []
        size = QSize(rect.width()/chunks, rect.height())
        for i in range(chunks):
            pos = rect.topLeft()
            pos.setX(pos.x() + size.width() * i)
            result.append(QRect(pos, size))
        return result

    def sizeHint(self) -> QSize:
        return self.layout.sizeHint()
    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        if index.data(CustomRoles.EditName):
            editor = QLineEdit(parent)
            editor.setGeometry(self.text_rect)
            return editor
        else:
            return None