import enum
from PySide2.QtCore import Qt


class TaskState(enum.IntEnum):
    READY = 0
    WAITING = 1
    RENDERING = 2
    STOPPED = 3
    SUCCESSFUL = 4
    FAILED = 5


class TaskEvent(enum.IntEnum):
    RENDER = 0,
    DELETE = 1,
    NONE = 2,
    DATACHANGED = 3,


class CustomRoles(enum.IntEnum):
    TaskName = Qt.DisplayRole,
    TaskData = Qt.UserRole,
    EnableState = Qt.UserRole + 1,
    RemoveState = Qt.UserRole + 2,
    RenderState = Qt.UserRole + 3,
    EditName = Qt.UserRole + 4,
    ItemType = Qt.UserRole + 5,
    DependentState = Qt.UserRole + 6,
    TaskState = Qt.UserRole + 7


class ItemTypes(enum.IntEnum):
    HeaderItem = 0,
    TaskItem = 1,
    DirItem = 2
