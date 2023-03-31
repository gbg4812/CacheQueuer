import sys
import psutil
import hou
import json
import os

from custom_widgets import TaskState, TaskDelegate, CustomRoles, WidgetState, ItemTypes, RenderHelpers

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
        
        userdir = hou.getenv("HOUDINI_USER_PREF_DIR")
        self.data_file = userdir + "/Scripts/CacheQueuer/" + "res/task_data.json"
        self.field_names = ("name", "rop_path", "state", "hip_file")

        
        #Init UI
        central_w = QWidget()
        gridl = QGridLayout(central_w)
        
        
        #Task Tree
        self.task_tree = QTreeWidget()
        self.task_tree.setHeaderHidden(True)
        self.task_tree.setDragDropMode(self.task_tree.DragDropMode.InternalMove)
        self.task_tree.setDragEnabled(True)
        self.task_tree.setEditTriggers(self.task_tree.EditTrigger.DoubleClicked)

        self.task_tree.setItemDelegate(TaskDelegate())
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

        addDir_bttn = QPushButton("Add directory")
        addDir_bttn.clicked.connect(self.addDir)
        utilsl.addWidget(addDir_bttn)

        
        
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
        for topitem in range(self.task_tree.topLevelItemCount()):
            model = self.task_tree.model()
            item_index = model.index(topitem, 0, self.task_tree.rootIndex())

            if item_index.data(CustomRoles.ItemType) == ItemTypes.TaskItem:
                RenderHelpers.render_task(item_index, model)
            elif item_index.data(CustomRoles.ItemType) == ItemTypes.DirItem:
                RenderHelpers.render_dir(item_index, model)
    def addDir(self):
        item = QTreeWidgetItem()
        item.setData(0, CustomRoles.TaskName, "New Directory")
        item.setData(0, CustomRoles.EnableState, WidgetState.ENABLED)
        item.setData(0, CustomRoles.DependentState, WidgetState.DISABLED)
        item.setData(0, CustomRoles.ItemType, ItemTypes.DirItem)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.task_tree.addTopLevelItem(item)
        self.task_tree.resizeColumnToContents(0)


                

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()      