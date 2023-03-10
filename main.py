import sys
import psutil
import hou
import csv

from PySide2.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QSpacerItem, QListWidgetItem
)
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Cache Queuer")
        
        #Global Variables
        self.data_file = "task_data.csv"
        self.field_names = ("name", "rop_path", "state", "hip_file")
        self.tasks = []

        
        #Init UI
        central_w = QWidget()
        gridl = QGridLayout(central_w)
        
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
        
        #Task List
        self.task_list = QListWidget()
        gridl.addWidget(self.task_list, 1, 0, 1, 2)
        
        
        
        #Parameters
        parmsl = QVBoxLayout()
        gridl.addLayout(parmsl, 1, 2)
        
        name_lab = QLabel("Task 1")
        name_lab.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        parmsl.addWidget(name_lab)

        self.setCentralWidget(central_w)
        
    def render_task(self, task):
        node = hou.node(task['rop_path'])
        try:
            node.render()
        except AttributeError:
            child = node.node("render")
            child.render()
        else:
            print("The node is invalid")
            
    def render(self):
    
        for task in self.tasks:
            self.render_task(task)
            
    def reload(self):
        self.task_list.clear()
        try:
            with open(self.data_file, 'r') as file:
                self.tasks = list(csv.DictReader(file, fieldnames=self.field_names))
                
                for task in self.tasks:
                    item = QListWidgetItem(task["name"])
                    self.task_list.addItem(item)

        except FileNotFoundError:
            print("We couldn't find any tasks")
    
    
        
        

            

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
