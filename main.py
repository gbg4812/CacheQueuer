import sys
import psutil
import hou
import json
import os

from custom_widgets import TaskState, TasksTree, TaskItem, DirItem
from custom_types import TaskList
"""
TODO
1. Revise State Property Type
2. State Property doesn't remain after drag drop
3. Directory Name doesn't remain after drag drop
4. Change From Csv to Json
"""

from PySide2.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QGridLayout, QPushButton, 
    QHBoxLayout, QVBoxLayout, QWidget, QSpacerItem, QSizePolicy, QTreeWidget, 
    QTreeWidgetItem, QTreeWidgetItemIterator, QHeaderView
)
from PySide2.QtCore import Qt, Signal, QSize
from PySide2.QtGui import QPixmap, QIcon, QDragEnterEvent, QDropEvent

#Class that represents the main application window
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Cache Queuer")
        self.tasksList = TaskList()
        
        userdir = hou.getenv("HOUDINI_USER_PREF_DIR")
        self.data_file = userdir + "/Scripts/CacheQueuer/" + "res/task_data.json"
        self.field_names = ("name", "rop_path", "state", "hip_file")

        
        #Init UI
        central_w = QWidget()
        gridl = QGridLayout(central_w)
        
        
        #Task List
        self.task_tree = TasksTree()
        gridl.addWidget(self.task_tree, 1, 0, 1, 2)

       
        #Utils Bar. Render and Reload buttons + system info
        utilsl = QHBoxLayout()
        gridl.addLayout(utilsl, 0, 0, 1, 3)
        
        reload_bttn = QPushButton("Reload")
        reload_bttn.clicked.connect(self.reload)
        utilsl.addWidget(reload_bttn)
        
        render_bttn = QPushButton("Render")
        render_bttn.clicked.connect(self.task_tree.render)
        utilsl.addWidget(render_bttn)
        
        
        utilsl.addSpacing(50)
        
        syslab = QLabel("Memory: {mem}% Cpu: {cpu}%".format(mem=psutil.virtual_memory()[2], cpu=psutil.cpu_percent(1)))
        utilsl.addWidget(syslab)
        
        #Parameters
        parmsl = QVBoxLayout()
        gridl.addLayout(parmsl, 1, 2)
        
        name_lab = QLabel("Task 1")
        name_lab.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        parmsl.addWidget(name_lab)

        self.setCentralWidget(central_w)

            
    def reload(self):
        try:
            with open(self.data_file, 'r') as file:
                newTasks = json.load(file)
                for task in newTasks:
                    #Create Item
                    item = TaskItem(task)
                    #Add Item to the tree
                    self.task_tree.addTopLevelCustomItem(item)
                file.close()

            os.remove(self.data_file)

        except FileNotFoundError:
            print("We couldn't find any tasks")      
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()      