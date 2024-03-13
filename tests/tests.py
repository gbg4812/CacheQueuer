from typing import Optional
from PySide6.QtCore import (
    QThread,
    QCoreApplication,
    Slot,
    Signal,
    QObject,
    QMutex,
    QMutexLocker,
    QWaitCondition,
    QTimer
)
from time import sleep

class ControlThread(QThread):
    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self.mutex = QMutex

    @Slot()
    def printMessage():




class RenderThread(QThread):
    finished = Signal()
    progress = Signal(int)
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.rendering = False
        self.name = "Default"
        self.mutex = QMutex()
        self.condition = QWaitCondition()

    def run(self):

        while True:
            i = 0
            while True:
                if not self.rendering:
                    break
                i+=1
                sleep(0.2)
                print("Hello " + self.name)
                self.progress.emit(i)

            self.finished.emit()
            self.mutex.lock()
            self.condition.wait(self.mutex)
            self.mutex.unlock()


    @Slot()
    def kill(self):
        locker = QMutexLocker(self.mutex)
        self.rendering = False 

    @Slot()
    def render(self, name: str):
        locker = QMutexLocker(self.mutex)
        if not self.rendering:
            self.rendering = True
            self.name = name
            if not self.isRunning():
                self.start()
            else:
                self.condition.wakeOne()



@Slot()
def workFinished():
    print("Work Finished")


if __name__ == "__main__":
    app = QCoreApplication()
    
    thread = RenderThread()
    thread.finished.connect(workFinished)
    thread.progress.connect(print)
    thread.render("Guillem")
    sleep(1)
    thread.kill()
    thread.render("Anna")
    sleep(3)
    thread.kill()
    sleep(2)
    thread.render("Isaac")
    sleep(1)
    thread.kill()
    

    app.exec_()
