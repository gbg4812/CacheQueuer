# std imports
import psutil
import time

# PySide imports
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import QThread, Signal

class SysInfoThread(QThread):
    update_info = Signal(str)
    def run(self) -> None:
        data = "Memory: {mem}% Cpu: {cpu}%".format(mem=psutil.virtual_memory()[2], cpu=psutil.cpu_percent(1))
        self.update_info.emit(data)
        time.sleep(0.5)
        self.run()

class SysInfoWidget(QWidget):
    def __init__(self, parent=None):
        super(SysInfoWidget, self).__init__(parent)

        layout = QHBoxLayout(self)

        label = QLabel()
        layout.addWidget(label)

        self.updateThread = SysInfoThread()
        self.updateThread.update_info.connect(label.setText)

    
