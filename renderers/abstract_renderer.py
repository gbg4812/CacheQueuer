from typing import Callable
from PySide2.QtCore import Signal, QObject

#This is a standard type to output task render information
class RendererInfo():
    def __init__(self, label1: str = "", label2: str = "", frame_range: list = (0, 0)):
        self.label1 = label1
        self.label2 = label2
        self.frame_range = frame_range

class AbstractRenderer(QObject):
    progress_updated = Signal(float)
    """
    Update Handler is a callable with a single argument, the progress in form of a float form 0 to 1
    """
    def getInfo(task: dict) -> RendererInfo:
        pass
    def renderTask(task: dict) -> bool:
        pass


        