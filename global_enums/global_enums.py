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
    TaskData = Qt.UserRole,
    ItemType = Qt.UserRole + 1,


class ItemTypes(enum.IntEnum):
    HeaderItem = 0,
    TaskItem = 1,
    DirItem = 2
