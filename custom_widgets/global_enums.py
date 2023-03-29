import enum
from PySide2.QtCore import Qt

class TaskState(enum.IntEnum):
    WAITING = 0
    RENDERING = 1
    SUCCESFUL = 2
    FAILED = 3
    DISABLED = 4


class WidgetState(enum.IntEnum):
    ENABLED = 1,
    DISABLED = 2,
    CLICKED = 3,
    FOCUSED = 4,
    EDITING = 5


class TaskEvent(enum.IntEnum):
    RENDER = 0,
    DELETE = 1,


class CustomRoles(enum.IntEnum):
    TaskName = Qt.DisplayRole,
    TaskData = Qt.UserRole,
    EnableState = Qt.UserRole + 1,
    RemoveState = Qt.UserRole + 2,
    RenderState = Qt.UserRole + 3,
    EditName = Qt.UserRole + 4,
    ItemType = Qt.UserRole + 5