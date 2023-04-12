from .hou_renderer import HouRenderer
from global_enums import *
from PySide2.QtCore import Signal, QObject, QThread

class RenderManager(QObject):
    progress_update = Signal(float)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.is_rendering = False

    def render(self, task_list: list) -> None:
        if not self.is_rendering:
            self.is_rendering = True
            self.renderThread = RenderThread(task_list)
            self.renderThread.progress_updated.connect(self.progressUpdate)
            self.renderThread.finished.connect(self.renderFinished)
            self.renderThread.start()
        else:
            pass

    def progressUpdate(self, progress):
        self.progress_update.emit(progress)
    
    def renderFinished(self):
        self.is_rendering = False
        

class RenderThread(QThread):
    progress_updated = Signal(float)

    def __init__(self, task_list: list, parent=None):
        super(RenderThread, self).__init__(parent)
        self.task_list = task_list
    
    def run(self) -> None:
        dependent = False
        success = True
        for task in self.task_list:
            task : dict
            if task.get("dependent") != None:
                dependent = task.get("dependent")
                success = True
            else:
                if dependent and not success: 
                    continue
                else:
                    HouRenderer.progress_handler = self.progressUpdated
                    HouRenderer.renderTask(task)

        
    def progressUpdated(self, progress):
        self.progress_updated.emit(progress)