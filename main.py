import sys
import psutil
import json
import os
import time

from custom_widgets import TasksTree, ParmsWidget, SysInfoWidget
from global_enums import *
from utils import TestTimer, ThreadingUtils
from renderers import *


from PySide2.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QGridLayout, QPushButton, 
    QHBoxLayout, QVBoxLayout, QWidget,
    QTreeWidgetItem, QSplitter, QSizePolicy
)
from PySide2.QtCore import Qt, QThread

#Class that represents the main application window
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Cache Queuer")
        
        self.data_file = "res/task_data.json"
        self.renderManager = RenderManager()
        #Init UI
        central_w = QWidget()
        layout = QVBoxLayout(central_w)
        splitter = QSplitter(Qt.Horizontal)
        
        
        #Task Tree
        self.task_tree = TasksTree()
        self.task_tree.render_tasks.connect(self.renderManager.render)
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

        sysinfo = SysInfoWidget() 
        utilsl.addWidget(sysinfo, alignment=Qt.AlignRight | Qt.AlignVCenter)
        #Parameters
        self.parms = ParmsWidget()
        self.renderManager.progress_update.connect(self.parms.update_handler)
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

    def itemSelectionChanged(self) -> None:
        if self.task_tree.topLevelItemCount() > 0:
            self.parms.itemSelected(self.task_tree.currentItem())

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    with open("style/style.qss", 'r') as f:
        app.setStyleSheet(f.read())
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())     