from typing import List, Dict
from PySide2.QtCore import Signal, QObject, QThread, QModelIndex
from .hou_renderer import HouRenderer
from global_enums import *

class RenderManager(QObject):
    progress_update = Signal(float)
    render_finished = Signal()

    def __init__(self, parent=None) -> None:
        super(RenderManager, self).__init__(parent)
        self.is_rendering = False
        self.renderThread = RenderThread()
        self.task_list : List[dict] = []

    def render(self, task_list: list) -> None:

        if not self.is_rendering:
            self.task_list = task_list
            self.is_rendering = True
            self.renderThread.setTaskList(self.task_list)
            self.renderThread.progress_updated.connect(self.progressUpdate)
            self.renderThread.finished.connect(self.renderFinished)
            self.renderThread.task_ended.connect(self.taskEnded)
            self.renderThread.start()
        else:
            pass

    def progressUpdate(self, progress):
        self.progress_update.emit(progress)
    
    def renderFinished(self):
        self.is_rendering = False
        
    def taskEnded(self, index: int, success: bool):
        itemIndex = self.task_indexes[index]
        model = itemIndex.model()
        
        if success:
            model.setData(index, TaskState.SUCCESFUL, CustomRoles.TaskState)
        else:
            model.setData(index, TaskState.FAILED, CustomRoles.TaskState)
        
        

class RenderThread(QThread):
    progress_updated = Signal(float)
    task_ended = Signal(int, bool)

    def __init__(self, task_list: list = None, parent=None):
        super(RenderThread, self).__init__(parent)
        self.task_list = task_list
    
    def run(self) -> None:
        dependent = False
        success = True
        for i, task in enumerate(self.task_list):
            task : dict
            if task.get("dependent") != None:
                dependent = task.get("dependent")
                success = True
            else:
                if dependent and not success: 
                    continue
                else:
                    HouRenderer.progress_handler = self.progressUpdated
                    success = HouRenderer.renderTask(task)
                    self.task_ended.emit(i, success)
                    

    def setTaskList(self, task_list : list):
        self.task_list = task_list
        
    def progressUpdated(self, progress):
        self.progress_updated.emit(progress)