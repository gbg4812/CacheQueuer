
from __future__ import annotations
import copy
from PySide2.QtWidgets import QStyleOptionViewItem, QStyleOptionButton, QApplication, QStyle, QLineEdit, QWidget, QPushButton
from PySide2.QtCore import Qt, QModelIndex, QRect, QAbstractItemModel, QSize, QMargins
from PySide2.QtGui import QPainter, QMouseEvent 

from global_enums import *

#TaskItemWidget is a class that paints and handles events of a dir item
class DirItemWidget():
    def __init__(self):
        super(DirItemWidget, self).__init__()

        self.button_size = QSize(100, 20)
        self.content_margins = QMargins(5, 5, 5, 5)
        self.separation = 5
        
        self.remove = QStyleOptionButton()
        self.render = QStyleOptionButton()
        self.enable = QStyleOptionButton()
        self.dependent = QStyleOptionButton()
        self.text_rect = QRect()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        rect: QRect = copy.copy(option.rect)
        rect.moveTo(0, 0)
        style = QApplication.style()
        painter.save()
        painter.translate(option.rect.topLeft())
        
        # Layout and  paint _enabled checkbox
        enable_rect = QRect(0, rect.top(), rect.height(), rect.height())
        sub_rect = style.subElementRect(
            QStyle.SE_CheckBoxClickRect, self.enable)

        self.enable.rect = QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight, Qt.AlignCenter, sub_rect.size(), enable_rect)

        state = index.data(CustomRoles.EnableState)
        if state == WidgetState.ENABLED:
            self.enable.state = QStyle.State_Enabled | QStyle.State_On
        elif state == WidgetState.DISABLED:
            self.enable.state = QStyle.State_Off
        style.drawControl(QStyle.CE_CheckBox, self.enable, painter)

        # Layout and  paint dependent checkbox
        dependent_rect = QRect(enable_rect.topRight(), enable_rect.size())
        sub_rect = style.subElementRect(
            QStyle.SE_CheckBoxClickRect, self.dependent)
        self.dependent.rect = QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight, Qt.AlignCenter, sub_rect.size(), dependent_rect)
        state = index.data(CustomRoles.DependentState)
        if state == WidgetState.ENABLED:
            self.dependent.state = QStyle.State_Enabled | QStyle.State_On
        elif state == WidgetState.DISABLED:
            self.dependent.state = QStyle.State_Off
        style.drawControl(QStyle.CE_CheckBox, self.dependent, painter)

        # Layout and  paint remove button
        remove_rect = QRect(rect.right() - self.button_size.grownBy(self.content_margins).width(), rect.top(),
                            self.button_size.grownBy(self.content_margins).width(), self.button_size.grownBy(self.content_margins).height())
        self.remove.rect = QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight,  Qt.AlignCenter, self.button_size, remove_rect)
        self.remove.text = "Remove"
        if index.data(CustomRoles.RemoveState) == WidgetState.CLICKED:
            self.remove.state = QStyle.State_Sunken
        else:
            self.remove.state = QStyle.State_Enabled
        style.drawControl(QStyle.CE_PushButton, self.remove, painter)

        # Layout and  paint render button
        render_rect = remove_rect.translated(
            - self.button_size.grownBy(self.content_margins).width(), 0)
        self.render.rect = QStyle.alignedRect(
            Qt.LayoutDirection.LeftToRight,  Qt.AlignCenter, self.button_size, render_rect)
        self.render.text = "Render"
        if index.data(CustomRoles.RenderState) == WidgetState.CLICKED:
            self.render.state = QStyle.State_Sunken
        else:
            self.render.state = QStyle.State_Enabled
        style.drawControl(QStyle.CE_PushButton, self.render, painter)

        # Layout and paint name
        name = index.data(Qt.DisplayRole)
        self.text_rect = QRect(dependent_rect.topRight(), QSize(
            rect.width() - enable_rect.width(), rect.height()))
        self.text_rect = style.itemTextRect(
            option.fontMetrics, self.text_rect, Qt.AlignLeft | Qt.AlignVCenter, QStyle.State_Enabled, name)
        style.drawItemText(painter, self.text_rect, Qt.AlignVCenter |
                           Qt.AlignLeft, option.palette, QStyle.State_Enabled, name)
        painter.restore()

    def eventHandler(self, event: QMouseEvent, model: QAbstractItemModel, option: QStyleOptionViewItem, index: QModelIndex) -> TaskEvent:
        style = QApplication.style()

        pos = event.pos()
        pos -= option.rect.topLeft()
        enable_state = index.data(CustomRoles.EnableState)
        dependent_state = index.data(CustomRoles.DependentState)
        # Handle mouse button press
        if event.type() == QMouseEvent.Type.MouseButtonPress:

            # Handle remove button

            if self.remove.rect.contains(pos):
                model.setData(index, WidgetState.CLICKED,
                              CustomRoles.RemoveState)
                return TaskEvent.DELETE
            elif self.render.rect.contains(pos):
                model.setData(index, WidgetState.CLICKED,
                              CustomRoles.RenderState)
                return TaskEvent.RENDER
            else:
                return TaskEvent.NONE

        # Handle mouse button release
        elif event.type() == QMouseEvent.Type.MouseButtonRelease:

            # Handle buttons
            model.setData(index, WidgetState.ENABLED, CustomRoles.RemoveState)
            model.setData(index, WidgetState.ENABLED, CustomRoles.RenderState)

            # Handle checkbox
            enable_rect = style.subElementRect(
                QStyle.SE_CheckBoxClickRect, self.enable)
            dependent_rect = style.subElementRect(
                QStyle.SE_CheckBoxClickRect, self.dependent)

            if enable_rect.contains(pos):
                if enable_state & WidgetState.ENABLED:
                    model.setData(index, WidgetState.DISABLED,
                                  CustomRoles.EnableState)
                elif enable_state & WidgetState.DISABLED:
                    model.setData(index, WidgetState.ENABLED,
                                  CustomRoles.EnableState)



            if dependent_rect.contains(pos):
                if dependent_state & WidgetState.ENABLED:
                    model.setData(index, WidgetState.DISABLED,
                                  CustomRoles.DependentState)
                elif dependent_state & WidgetState.DISABLED:
                    model.setData(index, WidgetState.ENABLED,
                                  CustomRoles.DependentState)


        elif event.type() == QMouseEvent.Type.MouseButtonDblClick:

            if self.text_rect.contains(pos):
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
        return QSize(350, self.button_size.grownBy(self.content_margins).height())

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        if index.data(CustomRoles.EditName):
            editor = QLineEdit(parent)
            editor.setGeometry(self.text_rect)
            return editor
        else:
            return None
