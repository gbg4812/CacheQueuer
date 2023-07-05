from __future__ import annotations
from typing import List, Dict, NoReturn, Any
from subprocess import Popen, PIPE
import json

from PySide2.QtCore import QRunnable, QThreadPool, Signal, QObject, QModelIndex, Slot
from global_enums import TaskStates, DataRoles


class RenderManager(QObject):
    progress_update = Signal(dict)
    render_finished = Signal()

    def __init__(self, parent=None) -> None:
        super(RenderManager, self).__init__(parent)
        self.is_rendering = False
        self.thread_pool = QThreadPool()
        self.task_list: List[dict] = []

    def render(self, task_list: list) -> None:
        if not self.is_rendering:
            self.task_list = task_list
            self.is_rendering = True
            renderWorker = RenderWorker(task_list)
            renderWorker.progress_updated.connect(self.progressUpdate)
            renderWorker.finished.connect(self.renderFinished)
            self.thread_pool.start(renderWorker)
        else:
            pass

    def progressUpdate(self, progress):
        self.progress_update.emit(progress)

    def renderFinished(self):
        self.is_rendering = False


class RenderWorker(QObject, QRunnable):
    finished = Signal()
    progress_updated = Signal(dict)

    def __init__(self, task_list: list):
        super(RenderWorker, self).__init__()
        self.task_list: List[Dict] = task_list

    @Slot()
    def run(self) -> None:
        for bundle in self.task_list:
            dependent = bundle.get("dependent")
            indexes: List[QModelIndex] = bundle["indexes"]
            success = True
            for index in indexes:
                index.model().setData(index, TaskStates.WAITING, DataRoles.TASKSTATE)

            for index in indexes:
                if dependent and not success:
                    continue
                else:
                    index.model().setData(
                        index, TaskStates.RENDERING, DataRoles.TASKSTATE
                    )

                    task: dict = index.data(DataRoles.DATA)
                    success = self.renderTask(task)

                    if success:
                        index.model().setData(
                            index, TaskStates.SUCCESSFUL, DataRoles.TASKSTATE
                        )
                    else:
                        index.model().setData(
                            index, TaskStates.FAILED, DataRoles.TASKSTATE
                        )

    def renderTask(self, task: Dict[str, str]):
        script = task["shell_script"]
        prog, arg = script.split(" ")
        task_str = json.dumps(task)
        subp = Popen([prog, arg, task_str], stdout=PIPE)

        objdata = dict()
        while True:
            if self.kill_render:
                subp.kill()
                break

            data = subp.stdout.readline()
            data = data.rstrip(b"\r\n")

            if data:
                try:
                    objdata: dict = json.loads(data)
                    self.progress_updated.emit(objdata)
                except json.JSONDecodeError:
                    print(data.decode("utf-8"))

            if subp.poll() is not None:
                break

        return 1 - subp.returncode
    
    @Slot()
    def killRender(self):
        self.kill_render = True


