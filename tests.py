from PySide2.QtCore import (
    QThread,
    QRunnable,
    QThreadPool,
    QCoreApplication,
    Slot,
    Signal,
    QObject,
)
from time import sleep


class Worker(QObject):
    finished = Signal()

    @Slot()
    def run(self):
        sleep(1)
        print("Hello")
        self.finished.emit()


@Slot()
def exitApp():
    print("Work Finished")


if __name__ == "__main__":
    app = QCoreApplication()

    th = QThread()

    obj = Worker()
    obj.finished.connect(exitApp)
    obj.moveToThread(th)
    th.started.connect(obj.run)
    th.start()
    sleep(2)
    th.start()


    app.exec_()
