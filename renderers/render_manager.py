from typing import List, Dict
from subprocess import Popen, PIPE
import json

from PySide2.QtCore import Signal, QObject, QThread, QModelIndex
from global_enums import *

class RenderManager(QObject):
    progress_update = Signal(dict)
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
            self.renderThread.start()
        else:
            pass

    def progressUpdate(self, progress):
        self.progress_update.emit(progress)
    
    def renderFinished(self):
        self.is_rendering = False
        

class RenderThread(QThread):
    progress_updated = Signal(dict)

    def __init__(self, task_list: list = None, parent=None):
        super(RenderThread, self).__init__(parent)
        self.task_list: List[dict] = task_list
    
    def run(self) -> None:
        for bundle in self.task_list:
            dependent = bundle.get("dependent")
            indexes : List[QModelIndex] = bundle.get("indexes")
            success = True
            for index in indexes:
                if dependent and not success: 
                    continue
                else:

                    index.model().setData(index, TaskState.RENDERING, CustomRoles.TaskState)

                    task : dict = index.data(CustomRoles.TaskData)
                    success = self.renderTask(task)

                    if success:
                        index.model().setData(index, TaskState.SUCCESFUL, CustomRoles.TaskState)
                    else:
                        index.model().setData(index, TaskState.FAILED, CustomRoles.TaskState)
                    
    def renderTask(self, task: dict):
        script : str = task.get("shell_script")
        prog, arg = script.split(" ")
        task_str = json.dumps(task)
        subp = Popen([prog, arg, task_str], stdout=PIPE)

        objdata = dict()
        while True:
            data = subp.stdout.readline()
            data = data.rstrip(b'\r\n')

            if data:
                try:
                    objdata: dict = json.loads(data)
                    self.progress_updated.emit(objdata)
                except json.JSONDecodeError:
                    print(data.decode("utf-8"))

            if subp.poll() is not None:
                break

        return objdata.get("State")== "SUCCESFUL"

    def setTaskList(self, task_list : list):
        self.task_list = task_list
        
    def progressUpdated(self, progress):
        self.progress_updated.emit(progress)