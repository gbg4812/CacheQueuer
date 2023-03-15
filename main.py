import sys
import psutil
import hou
import csv
import enum

from PySide2.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider, QGridLayout, QPushButton, 
    QHBoxLayout, QVBoxLayout, QWidget, QSpacerItem, QListWidgetItem, QSizePolicy, QTreeWidget, QTreeWidgetItem
)
from PySide2.QtCore import Qt, Signal, QSize
from PySide2.QtGui import QPixmap, QIcon

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Cache Queuer")
        
        #Global Variables
        self.data_file = "res/task_data.csv"
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
        self.task_list = QTreeWidget()
        gridl.addWidget(self.task_list, 1, 0, 1, 2)
        
        #Parameters
        parmsl = QVBoxLayout()
        gridl.addLayout(parmsl, 1, 2)
        
        name_lab = QLabel("Task 1")
        name_lab.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        parmsl.addWidget(name_lab)

        self.setCentralWidget(central_w)
        
    def render_task(self, row):
        task = self.tasks[row]
        hou.hipFile.load(task['hip_file'])
        node = hou.node(task['rop_path'])
        try:
            node.render()
        except AttributeError:
            child = node.node("render")
            child.render()
        else:
            print("The node is invalid")
            
    def render(self):
    
        for i, task in enumerate(self.tasks):
            self.render_task(i)

    def remove_task(self, index):
        del self.tasks[index]
        self.task_list.removeItemWidget(index)
        self.task_list.takeTopLevelItem(index)
            
    def reload(self):
        try:
            with open(self.data_file, 'r') as file:
                newTasks = list(csv.DictReader(file, fieldnames=self.field_names))
                self.tasks += newTasks
                for i, task in enumerate(newTasks):
                    item = QTreeWidgetItem()
                    item.setData(Qt.UserRole, i+len(self.tasks))
                    self.task_list.addTopLevelItem(item)
                    item_widget = ItemWidget(task.get("name"), item)
                    item_widget.render_clicked.connect(self.render_task)
                    item_widget.remove_clicked.connect(self.remove_task)

                    self.task_list.setItemWidget(item, 0, item_widget)
                    item.setSizeHint(0, item_widget.sizeHint())

                file.close()

            #os.remove(self.data_file)

        except FileNotFoundError:
            print("We couldn't find any tasks")
    
class ItemWidget(QWidget):

    #First Int => index_from_parent, Second Int => index in the tasks list
    render_clicked = Signal(int, int)
    remove_clicked = Signal(int, int)

    def __init__(self, label, item):
        super(ItemWidget, self).__init__()
        self.item = item
        self.state = 0

        layout = QHBoxLayout()
        
        #Label Name
        label = QLabel(label)

        #Buttons
        renderButton = QPushButton("Render")
        renderButton.clicked.connect(self.rndr_task)
        rmButton = QPushButton("Remove")
        rmButton.clicked.connect(self.rm_task)
        
        #Label State
        stateMenu = QComboBox()
        stateItems = ((QPixmap("res/clock.svg").scaled(QSize(30, 30), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation), "Waiting"),
                      (QPixmap("res/clock.svg").scaled(QSize(30, 30), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation), "Rendering"),
                      (QPixmap("res/clock.svg").scaled(QSize(30, 30), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation), "Complete"),
                      (QPixmap("res/clock.svg").scaled(QSize(30, 30), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation), "Failed"))
        for pixmap, lab in stateItems: 
            stateMenu.addItem(QIcon(pixmap), lab)
        
        layout.addWidget(label)
        layout.addWidget(renderButton)
        layout.addWidget(rmButton)
        layout.addWidget(stateMenu)


        
        self.setLayout(layout)
    
    def rm_task(self):
        tree_w = self.item.treeWidget()
        self.remove_clicked.emit(tree_w.indexFromItem(self.item).row())
    def rndr_task(self):
        tree_w = self.item.treeWidget()
        self.render_clicked.emit(tree_w.indexFromItem(self.item).row())
class TaskState(enum.Enum):
    WAITING = 0
    RENDERING = 1
    SUCCESFUL = 2
    FAILED = 3

            

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()