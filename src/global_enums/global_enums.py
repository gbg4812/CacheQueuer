import enum
from PySide6.QtCore import Qt
Qt.ItemDataRole

class DataRoles(enum.IntEnum):
    TYPE = 0
    DATA = 1
    NAME = 5
    TASKSTATE = 3


class TaskStates(enum.IntEnum):
    NORMAL = 0,
    WAITING = 1,
    RENDERING = 2,
    STOPPED = 3,
    SUCCESSFUL = 4,
    FAILED = 5,


