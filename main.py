import sys
import psutil
import hou
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
    QTreeWidgetItem 
)
from PySide2.QtCore import Qt

#Class that represents the main application window
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Cache Queuer")
        
        userdir = hou.getenv("HOUDINI_USER_PREF_DIR")
        self.data_file = userdir + "/Scripts/CacheQueuer/" + "res/task_data.json"
        self.field_names = ("name", "rop_path", "state", "hip_file")

        
        #Init UI
        central_w = QWidget()
        gridl = QGridLayout(central_w)
        
        
        #Task Tree
        self.task_tree = TasksTree()
        gridl.addWidget(self.task_tree, 1, 0, 1, 2)

       
        #Utils Bar. Render and Reload buttons + system info
        utilsl = QHBoxLayout()
        gridl.addLayout(utilsl, 0, 0, 1, 3)
        
        reload_bttn = QPushButton("Reload")
        reload_bttn.clicked.connect(self.reload)
        utilsl.addWidget(reload_bttn)
        
        render_bttn = QPushButton("Render")
        render_bttn.clicked.connect(self.render)
        utilsl.addWidget(render_bttn)

        utilsl.addSpacing(50)
        
        syslab = QLabel("Memory: {mem}% Cpu: {cpu}%".format(mem=psutil.virtual_memory()[2], cpu=psutil.cpu_percent(1)))
        utilsl.addWidget(syslab)
        
        #Parameters
        self.parms = ParmsWidget()
        gridl.addLayout(self.parms, 1, 2)

        self.task_tree.itemSelectionChanged.connect(self.parms.itemSelected)
        
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

            #os.remove(self.data_file)

        except FileNotFoundError:
            print("We couldn't find any tasks")      

    def render(self):
        tasks_list = self.task_tree.flatten_tree(self.task_tree.rootIndex())
        ThreadingUtils.startThread(ThreadNames.RENDER_THREAD, RenderHelpers.render_list, (tasks_list, ), True)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()      