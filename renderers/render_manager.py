from __future__ import annotations
from typing import List, Dict, NoReturn, Any
from subprocess import Popen, PIPE
import json

from PySide2.QtCore import (
    QThread,
    QMutex,
    QMutexLocker,
    QWaitCondition,
    Signal,
    QObject,
    QModelIndex,
    Slot,
)
from global_enums import TaskStates, DataRoles
from utils import Logger
from utils.logger import Level

flog = Logger(__name__, Level.DEBUG)


class RenderThread(QThread):
    finished = Signal()
    progress_updated = Signal(dict)

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.task_list: List[Dict] = [{}]
        self.rendering = False
        self.mutex = QMutex()
        self.condition = QWaitCondition()

    def run(self) -> None:
        while True:
            self.mutex.lock()
            task_list = self.task_list
            self.mutex.unlock()

            for bundle in task_list:
                dependent = bundle.get("dependent")
                indexes: List[QModelIndex] = bundle["indexes"]
                success = True
                for index in indexes:
                    index.model().setData(
                        index, TaskStates.WAITING, DataRoles.TASKSTATE
                    )

                for index in indexes:
                    if dependent and not success:
                        continue
                    else:
                        index.model().setData(
                            index, TaskStates.RENDERING, DataRoles.TASKSTATE
                        )

                        task: dict = index.data(DataRoles.DATA)
                        success = self._renderTask(task)

                        if success:
                            flog.debug("Task rendered succesfully")
                            index.model().setData(
                                index, TaskStates.SUCCESSFUL, DataRoles.TASKSTATE
                            )
                        else:
                            index.model().setData(
                                index, TaskStates.FAILED, DataRoles.TASKSTATE
                            )

            self.finished.emit()

            self.mutex.lock()
            self.rendering = False
            self.mutex.unlock()

            self.mutex.lock()
            flog.debug("Thread Waiting...")
            self.condition.wait(self.mutex)
            flog.debug("Thread awaken")
            self.mutex.unlock()

            flog.debug("checking for interruptions")
            if self.isInterruptionRequested():
                flog.debug("Abort is true")
                break

    def _renderTask(self, task: Dict[str, str]):
        script = task["shell_script"]
        prog, arg = script.split(" ")
        task_str = json.dumps(task)
        subp = Popen([prog, arg, task_str], stdout=PIPE)

        objdata = dict()
        while True:
            self.mutex.lock()
            rendering = self.rendering
            self.mutex.unlock()

            if not rendering:
                flog.debug("Rendering should stop")
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
                flog.debug("Process ended")
                break

        return 1 - subp.returncode

    @Slot()
    def render(self, task_list: List[Dict]):
        locker = QMutexLocker(self.mutex)
        if not self.rendering:
            self.rendering = True
            self.task_list = task_list
            if not self.isRunning():
                self.start()
            else:
                self.condition.wakeAll()
        else:
            flog.info("Task is still rendering, kill it to start a new render")

    @Slot()
    def killRender(self):
        locker = QMutexLocker(self.mutex)
        self.rendering = False

    @Slot()
    def killThread(self):
        flog.debug("Thread about to be killed")
        self.killRender()
        self.requestInterruption()

        self.mutex.lock()
        self.condition.wakeAll()
        self.mutex.unlock()

        flog.debug("Waiting for thread to dye...")
        self.wait()
