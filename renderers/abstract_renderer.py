from typing import Callable

#This is a standard type to output task render information
class RendererInfo():
    def __init__(self, label1: str = "", label2: str = "", frame_range: list = (0, 0)):
        self.label1 = label1
        self.label2 = label2
        self.frame_range = frame_range
    def __str__(self):
        return f"label1: {self.label1} \nlabel2: {self.label2} \nframe range: {self.frame_range}"

class AbstractRenderer():
    progress_handler : Callable = None

    """
    Update Handler is a callable with a single argument, the progress in form of a float form 0 to 1
    """
    def getInfo(task: dict) -> RendererInfo:
        pass
    def renderTask(task: dict) -> bool:
        pass


        