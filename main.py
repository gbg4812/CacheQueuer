import sys
import psutil
import json
import os

from custom_widgets import TasksTree, ParmsWidget
from global_enums import *
from utils import ThreadingUtils
from renderers import *


from PySide2.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QGridLayout, QPushButton, 
    QHBoxLayout, QVBoxLayout, QWidget,
    QTreeWidgetItem, QSplitter, QSizePolicy
)
from PySide2.QtCore import Qt, QTimer

#Class that represents the main application window
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Cache Queuer")
        
        self.data_file = "res/task_data.json"
        
        #Init UI
        central_w = QWidget()
        layout = QVBoxLayout(central_w)
        splitter = QSplitter(Qt.Horizontal)
        
        
        #Task Tree
        self.task_tree = TasksTree()
        splitter.addWidget(self.task_tree)
       
        #Utils Bar. Render and Reload buttons + system info
        utilsl = QHBoxLayout()
        layout.addLayout(utilsl, stretch=0)
        
        reload_bttn = QPushButton("Reload")
        reload_bttn.clicked.connect(self.reload)
        utilsl.addWidget(reload_bttn)
        
        render_bttn = QPushButton("Render")
        render_bttn.clicked.connect(self.render)
        utilsl.addWidget(render_bttn)

        utilsl.addSpacing(50)
        
        self.syslab = QLabel()
        timer = QTimer()
        timer.timeout.connect(self.updateSysLab)
        timer.setInterval(500)
        timer.start()
        utilsl.addWidget(self.syslab)
        
        #Parameters
        self.parms = ParmsWidget()
        RenderHelpers.update_handler = self.parms.update_handler
        splitter.addWidget(self.parms)
        self.task_tree.itemSelectionChanged.connect(self.itemSelectionChanged)


        layout.addWidget(splitter, stretch=1)
        
        self.setCentralWidget(central_w)

            
    def reload(self):
        try:
            with open(self.data_file, 'r') as f:
                tasks = json.load(f)
                for task in tasks:
                    task: dict
                    item = QTreeWidgetItem()
                    item.setData(0, Qt.DisplayRole, task.pop("name"))
                    item.setData(0, CustomRoles.DependentState,  WidgetState.ENABLED)
                    item.setData(0, CustomRoles.EnableState,  WidgetState.ENABLED)
                    item.setData(0, CustomRoles.ItemType, ItemTypes.TaskItem)   
                    item.setData(0, Qt.UserRole, task)
                    item.setFlags( (item.flags() | Qt.ItemIsEditable) ^ Qt.ItemIsDropEnabled)
                    self.task_tree.addTopLevelItem(item)
                    self.task_tree.resizeColumnToContents(0)

            os.remove(self.data_file)

        except FileNotFoundError:
            print("We couldn't find any tasks")      

    def render(self):
        tasks_list = self.task_tree.flatten_tree(self.task_tree.rootIndex())
        ThreadingUtils.startThread(ThreadNames.RENDER_THREAD, RenderHelpers.render_list, (tasks_list, ), True)
    
    def itemSelectionChanged(self) -> None:
        if self.task_tree.topLevelItemCount() > 0:
            self.parms.itemSelected(self.task_tree.currentItem())

    def updateSysLab(self) -> None:
        self.syslab.setText("Memory: {mem}% Cpu: {cpu}%".format(mem=psutil.virtual_memory()[2], cpu=psutil.cpu_percent(1)))

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())     