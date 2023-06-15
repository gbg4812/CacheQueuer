from __future__ import annotations
from os import path

from PySide2.QtWidgets import (
    QStyleOptionViewItem,
    QStyle,
    QLineEdit,
    QWidget,
    QStyleOption,
)
from PySide2.QtCore import (
    Qt,
    QModelIndex,
    QRect,
    QAbstractItemModel,
    QSize,
    QMargins,
    QLine,
)
from PySide2.QtGui import QPainter, QMouseEvent, QPixmap, QColor, QPen

from global_enums import TaskState, TaskEvent, CustomRoles
from delegate_subitems import WidgetState, IconButton, RailLayout, TextItem

wrkdir, _ = path.split(__file__)
wrkdir += "/"

# TaskItemWidget is a class that paints and handles events of a task item


class TaskItemWidget:
    def __init__(self):
        super(TaskItemWidget, self).__init__()

        self.button_size = QSize(30, 30)
        self.content_margins = QMargins(5, 5, 20, 5)

        self.remove = IconButton(
            QPixmap(wrkdir + "res/icons/trash.png"), WidgetState.ENABLED
        )

        self.render = IconButton(
            QPixmap(wrkdir + "res/icons/render.png"), WidgetState.ENABLED
        )
        self.render.addStateIcon(
            WidgetState.DISABLED, QPixmap(wrkdir + "res/icons/render_disabled.png")
        )

        self.enable = IconButton(
            QPixmap(wrkdir + "res/icons/enable_on.png"),
            WidgetState.ENABLED,
            paint_rect=True,
        )
        self.enable.addStateIcon(
            WidgetState.DISABLED, QPixmap(wrkdir + "res/icons/enable_off.png")
        )
        self.enable.addStateColor(WidgetState.CLICKED, QColor(255, 255, 255, 255))

        self.name = TextItem(text_size=12)
        self.statelab = TextItem(text_size=12, min_letters=len("State: Successful"))

        self.layout = RailLayout(10, 20)
        self.layout.addLItem(self.enable)
        self.layout.addLItem(self.name)

        self.layout.addRItem(self.remove)
        self.layout.addRItem(self.render)
        self.layout.addRItem(self.statelab)
        self.layout.computeLayout()

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ):
        rect: QRect = option.rect.marginsRemoved(self.content_margins)

        TextColor1_disabled = QColor("#698181")
        Primary3_disabled = QColor("#8cb2be")
        Primary3_selected = QColor("#c9e7ed")
        Primary3_hover = QColor("#a4d5df")
        TextColor1 = QColor("#1a2122")
        Border2 = QColor("#354558")
        Border1 = QColor("#6b98a5")
        Accent1 = QColor("#57a773")
        Primary3 = QColor("#7ec0d1")
        Primary2 = QColor("#476d86")
        Primary1 = QColor("#3d4e63")

        if option.state & QStyle.State_Selected:
            TaskItemWidget.paintBackground(painter, rect, Border1, Primary3_selected)
        else:
            TaskItemWidget.paintBackground(painter, rect, Border1, Primary3)

        self.statelab.setTextColor(TextColor1)
        self.name.setTextColor(TextColor1)

        # Set text for the state label
        text = "State: "
        if index.data(CustomRoles.TaskState) == TaskState.READY:
            text += "Ready"
        elif index.data(CustomRoles.TaskState) == TaskState.RENDERING:
            self.statelab.setTextColor("#204885")
            text += "Rendering"
        elif index.data(CustomRoles.TaskState) == TaskState.WAITING:
            self.statelab.setTextColor("#c09b2d")
            text += "Waiting"
        elif index.data(CustomRoles.TaskState) == TaskState.STOPPED:
            self.statelab.setTextColor("#c09b2d")
            text += "Stopped"
        elif index.data(CustomRoles.TaskState) == TaskState.SUCCESSFUL:
            self.statelab.setTextColor(Accent1)
            text += "Successful"
        elif index.data(CustomRoles.TaskState) == TaskState.FAILED:
            self.statelab.setTextColor(QColor("#a72727"))
            text += "Failed"

        self.statelab.setText(text)

        # Set Style if the task is disabled
        if index.data(CustomRoles.EnableState) == WidgetState.DISABLED:
            self.name.setTextColor(TextColor1_disabled)
            self.statelab.setTextColor(TextColor1_disabled)

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

    def eventHandler(
        self,
        event: QMouseEvent,
        model: QAbstractItemModel,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> TaskEvent:
        rect: QRect = option.rect.marginsRemoved(self.content_margins)

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
                model.setData(index, WidgetState.CLICKED, CustomRoles.RemoveState)
            elif self.render.contains(pos) and enable_state is not WidgetState.DISABLED:
                model.setData(index, WidgetState.CLICKED, CustomRoles.RenderState)
            elif self.enable.contains(pos):
                model.setData(index, WidgetState.CLICKED, CustomRoles.EnableState)
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
                    model.setData(index, WidgetState.DISABLED, CustomRoles.EnableState)
                    model.setData(index, WidgetState.DISABLED, CustomRoles.RenderState)
                elif enable_state & WidgetState.DISABLED:
                    model.setData(index, WidgetState.ENABLED, CustomRoles.EnableState)
                    model.setData(index, WidgetState.ENABLED, CustomRoles.RenderState)

        elif event.type() == QMouseEvent.Type.MouseButtonDblClick:
            # Default button state
            model.setData(index, WidgetState.ENABLED, CustomRoles.RemoveState)
            model.setData(index, WidgetState.ENABLED, CustomRoles.RenderState)

            if self.name.contains(pos):
                model.setData(index, True, CustomRoles.EditName)
            else:
                model.setData(index, False, CustomRoles.EditName)

        return TaskEvent.DATACHANGED

    def sizeHint(self, option: QStyleOption, index: QModelIndex) -> QSize:
        self.name.setText(index.data(CustomRoles.TaskName))
        self.layout.computeLayout()
        return self.layout.sizeHint().grownBy(self.content_margins)

    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        if index.data(CustomRoles.EditName):
            editor = QLineEdit(parent)
            return editor
        else:
            return None

    def updateEditorGeometry(
        self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> None:
        rect: QRect = option.rect.marginsRemoved(self.content_margins)
        editor.setGeometry(rect)

    def paintBackground(
        painter: QPainter, rect: QRect, border_col: QColor, fill_col: QColor
    ):
        painter.save()

        # Paint Background
        painter.setPen(Qt.NoPen)
        painter.fillRect(rect, fill_col)

        # Paint Borders
        topLine = QLine(rect.topLeft(), rect.topRight())
        bottLine = QLine(rect.bottomLeft(), rect.bottomRight())

        borderPen = QPen(border_col, 3)
        borderPen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(borderPen)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawLine(topLine)
        painter.drawLine(bottLine)

        painter.restore()
