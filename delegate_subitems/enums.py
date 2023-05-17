import enum

class WidgetState(enum.IntEnum):
    ENABLED = 1,
    DISABLED = 2,
    CLICKED = 3,
    FOCUSED = 4,
    EDITING = 5