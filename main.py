import sys
import psutil
import hou
import csv
import enum

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

#Class defining the state of a task
class TaskState(enum.Enum):
    WAITING = 0
    RENDERING = 1
    SUCCESFUL = 2
    FAILED = 3

#Class that represents the main application window
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Cache Queuer")
        
        #Global Variables
        self.data_file = "res/task_data.csv"
        self.field_names = ("name", "rop_path", "state", "hip_file")
        self.tasksList = TaskList()

        
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
        self.task_tree = TasksTree()
        self.task_tree.setColumnCount(1)
        
        #Create Header
        header_item = QTreeWidgetItem()
        #Header Widget
        header_w = QWidget()
        header_l = QHBoxLayout(header_w)
        
        ndir_bttn = QPushButton("New Dependency Directory")
        ndir_bttn.clicked.connect(self.add_dir)
        header_lab = QLabel("Tasks")
        
        header_l.addWidget(header_lab)
        header_l.addWidget(ndir_bttn)
        #Configure item
        header_item.setSizeHint(0, header_w.sizeHint())
        header_item.setFlags(Qt.NoItemFlags)
        
        #Assign Header Item to tree
        self.task_tree.addTopLevelItem(header_item)
        self.task_tree.setHeaderHidden(True)
        self.task_tree.setItemWidget(header_item, 0, header_w)

        
        #Enable Drag And Drop
        self.task_tree.setDragEnabled(True)
        self.task_tree.setDragDropMode(self.task_tree.InternalMove)
        self.task_tree.task_moved.connect(self.recreate_task)
        self.task_tree.dir_moved.connect(self.recreate_dir)
        gridl.addWidget(self.task_tree, 1, 0, 1, 2)
        
        #Parameters
        parmsl = QVBoxLayout()
        gridl.addLayout(parmsl, 1, 2)
        
        name_lab = QLabel("Task 1")
        name_lab.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        parmsl.addWidget(name_lab)

        self.setCentralWidget(central_w)

    #renders a single task given a id   
    def render_task(self, id):
        task = self.tasksList.getFromID(id)
        self.tasksList.setTaskValue(id, "state", TaskState.RENDERING)
        hou.hipFile.load(task['hip_file'])
        node = hou.node(task['rop_path'])
        try:
            node.render()
        except AttributeError:
            child = node.node("render")
            child.render()
        else:
            self.tasksList.setTaskValue(id, "state", TaskState.FAILED)
            return False
        
        self.tasksList.setTaskValue(id, "state", TaskState.SUCCESFUL)
        return True

    #renders all the tasks
    def render(self):
        it = QTreeWidgetItemIterator(self.task_tree)
        dependent = False
        success = True
        while it:
            #Select Task Folders With dependency disabled
            itemData = it.value().data(0, Qt.UserRole)
            if itemData == -1:
                dependent = False
                
            #Selects Task Folders With dependency enabled
            if itemData == -2:
                dependent = True
                success = True
                
            #Selects Tasks
            else:
                #Handles dependent tasks
                taskState = self.tasksList.getTaskValue(itemData, "state")
                if it.value().parent() == None:
                    self.render_task(it.value().data(0, Qt.UserRole))
                    
                elif dependent == True and success == True and taskState == TaskState.WAITING:
                    success = self.render_task(it.value().data(0, Qt.UserRole))
                
                #Handles independent tasks
                elif dependent == False and taskState == TaskState.WAITING:
                    self.render_task(it.value().data(0, Qt.UserRole))
            

    def remove_task(self, id):
        self.tasksList.rmTask(id)

            
    def reload(self):
        try:
            with open(self.data_file, 'r') as file:
                newTasks = list(csv.DictReader(file, fieldnames=self.field_names))
                for task in newTasks:
                    #Create Item
                    item = QTreeWidgetItem()
                    #Disable Drop Target
                    item.setFlags(item.flags() ^ Qt.ItemIsDropEnabled)
                    #Pass the Task Id to the Item User Role For later Use and add the task to the tasksList
                    item.setData(0, Qt.UserRole, self.tasksList.addTask(task))
                    #Add Item to the tree
                    self.task_tree.addTopLevelItem(item)
                    #Set Item Widget and connect its signals
                    item_widget = ItemWidget(task.get("name"), item)
                    item_widget.render_clicked.connect(self.render_task)
                    item_widget.remove_clicked.connect(self.remove_task)
                    item_widget.state_changed.connect(self.change_task_state)

                    self.task_tree.setItemWidget(item, 0, item_widget)
                    item.setSizeHint(0, item_widget.sizeHint())

                file.close()

            #os.remove(self.data_file)

        except FileNotFoundError:
            print("We couldn't find any tasks")
            
    #When tasks are reordered the item widgets need to be reconstructed
    def recreate_task(self, item: QTreeWidgetItem):
        #Set Item Widget and connect its signals
        task = self.tasksList.getFromID(item.data(0, Qt.UserRole))
        item_widget = ItemWidget(task.get("name"), item)
        print(task.get("state"))
        item_widget.set_state(int(task.get("state")))
        item_widget.render_clicked.connect(self.render_task)
        item_widget.remove_clicked.connect(self.remove_task)

        self.task_tree.setItemWidget(item, 0, item_widget)
        item.setSizeHint(0, item_widget.sizeHint())
        
    def recreate_dir(self, item: QTreeWidgetItem):
        dir_widget = DirItemWidget(item)
        item.setSizeHint(0, dir_widget.sizeHint())
        
        self.task_tree.setItemWidget(item, 0, dir_widget)
    
    def change_task_state(self, id, state: TaskState):
        self.tasksList.setTaskValue(id, "state", state)
        
    def add_dir(self):
        dir_item = QTreeWidgetItem()
        dir_item.setData(0, Qt.UserRole, -1)
        self.task_tree.addTopLevelItem(dir_item)
        
        dir_widget = DirItemWidget(dir_item)
        dir_item.setSizeHint(0, dir_widget.sizeHint())
        
        self.task_tree.setItemWidget(dir_item, 0, dir_widget)
        
#Custom Widget For the TreeWidgetItems that has controls to manipulate every task separately.
#It emits rm_task and rndr_task signals
class ItemWidget(QWidget):

    #First Int => TaskId
    render_clicked = Signal(int)
    remove_clicked = Signal(int)
    
    #Second the new state of the task
    state_changed = Signal(int, TaskState)

    def __init__(self, label: str, item: QTreeWidgetItem):
        super(ItemWidget, self).__init__()
        self.item = item
        self.state = TaskState.WAITING

        layout = QHBoxLayout()
        
        #Label Name
        label = QLabel(label)

        #Buttons
        renderButton = QPushButton("Render")
        renderButton.clicked.connect(self.rndr_task)
        rmButton = QPushButton("Remove")
        rmButton.clicked.connect(self.rm_task)
        
        #Label State
        self.stateMenu = QComboBox()
        stateItems = ((QPixmap("res/clock.svg").scaled(QSize(30, 30), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation), "Waiting"),
                      (QPixmap("res/clock.svg").scaled(QSize(30, 30), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation), "Rendering"),
                      (QPixmap("res/clock.svg").scaled(QSize(30, 30), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation), "Complete"),
                      (QPixmap("res/clock.svg").scaled(QSize(30, 30), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation), "Failed"))
        for pixmap, lab in stateItems: 
            self.stateMenu.addItem(QIcon(pixmap), lab)
        self.stateMenu.currentIndexChanged.connect(self.st_changed)
        
        layout.addWidget(label)
        layout.addWidget(renderButton)
        layout.addWidget(rmButton)
        layout.addWidget(self.stateMenu)

        self.setLayout(layout)
    
    def rm_task(self):
        self.remove_clicked.emit(self.item.data(0, Qt.UserRole))
        parent = self.item.parent()
        if parent:
            parent.takeChild(parent.indexOfChild(self.item))
        else:
            tree_w = self.item.treeWidget()
            tree_w.takeTopLevelItem(tree_w.indexOfTopLevelItem(self.item))
            
        self.deleteLater()
        
    def rndr_task(self):
        self.render_clicked.emit(self.item.data(0, Qt.UserRole))
        
    def st_changed(self, index):
        self.state_changed.emit(self.item.data(0, Qt.UserRole), index)
        
    def set_state(self, state: TaskState):
        self.state = state
        self.stateMenu.setCurrentIndex(state)
        
class DirItemWidget(QWidget):
    
    #First QTreeWidgetItem => Dir Item
    render_clicked = Signal(QTreeWidgetItem)
    
    def __init__(self, item: QTreeWidgetItem):
        super(DirItemWidget, self).__init__()
        
        self.item = item
        layout = QHBoxLayout(self)
        
        #Label Name
        label = QLineEdit("New Directory")
        

        #Buttons
        renderButton = QPushButton("Render")
        renderButton.clicked.connect(self.rndr_dir)
        rmButton = QPushButton("Remove")
        rmButton.clicked.connect(self.rm_dir)
        
        layout.addWidget(label)
        layout.addWidget(renderButton)
        layout.addWidget(rmButton)
        
    def rndr_dir(self):
        self.render_clicked.emit(self.item)
        
    def rm_dir(self):
        tree_w = self.item.treeWidget()
        for child in self.item.takeChildren():
            tree_w.removeItemWidget(child, 0)
        tree_w.takeTopLevelItem(tree_w.indexOfTopLevelItem(self.item))
        self.deleteLater()
        
        
        
        

#class that controls the tasks list
class TaskList():
    def __init__(self):
        self.tasks = []
        self.ids = []
        self.maxId = 0
        
    def get(self, index) -> dict:
        return self.tasks[index]
    
    def getFromID(self, id) -> dict:
        return self.tasks[self.ids.index(id)]
    
    def rmTask(self, id) -> None:
        self.tasks
        del self.tasks[self.ids.index(id)]
        self.ids.remove(id)
    
    def addTask(self, task) -> int:
        self.tasks.append(task)
        self.ids.append(self.maxId)
        self.maxId += 1
        
        return self.maxId - 1
            
    def setTaskValue(self, id, key, value):
        self.tasks[self.ids.index(id)][key] = value
        
    def getTaskValue(self, id, key):
        return self.tasks[self.ids.index(id)][key]



#Subclass Of The TreeWidget 
class TasksTree(QTreeWidget):
    #The new item created in the new place
    task_moved = Signal(QTreeWidgetItem)
    dir_moved = Signal(QTreeWidgetItem)
    
    def __init__(self):
        super(TasksTree, self).__init__()
        
    def dropEvent(self, event: QDropEvent) -> None:
        
        #Item where user drops and its parent
        current_item = self.currentItem()
        tg_item = self.itemAt(event.pos())
        tg_parent = tg_item.parent()
        drop_pos = self.dropIndicatorPosition()
        
        #New item created
        nitem = QTreeWidgetItem()
        nitem_taskid = current_item.data(0, Qt.UserRole)
        nitem.setData(0, Qt.UserRole, nitem_taskid)
        
        #nitem.setFlags(nitem.flags() ^ Qt.ItemIsDropEnabled)
        DIP = QTreeWidget.DropIndicatorPosition            
        if nitem_taskid >= 0:
            if drop_pos == DIP.OnItem:
                tg_item.addChild(nitem)
                
            elif drop_pos == DIP.AboveItem:
                if tg_parent:
                    tg_parent.insertChild(tg_parent.indexOfChild(tg_item), nitem)
                else:
                    self.insertTopLevelItem(self.indexOfTopLevelItem(tg_item), nitem)
                
            elif drop_pos == DIP.BelowItem:
                if tg_parent:
                    tg_parent.insertChild(tg_parent.indexOfChild(tg_item) + 1, nitem)
                else:
                    self.insertTopLevelItem(self.indexOfTopLevelItem(tg_item) + 1, nitem)
            
            self.task_moved.emit(nitem)

        else:
            if drop_pos == DIP.OnItem:
                event.ignore()
                return None
                
            elif drop_pos == DIP.AboveItem:
                if tg_parent:
                    event.ignore()
                    return None
                else:
                    self.insertTopLevelItem(self.indexOfTopLevelItem(tg_item), nitem)
                
            elif drop_pos == DIP.BelowItem:
                if tg_parent:
                    event.ignore()
                    return None
                else:
                    self.insertTopLevelItem(self.indexOfTopLevelItem(tg_item) + 1, nitem)
                    
            self.dir_moved.emit(nitem)
            
            #Move directory contents 
            for indx in range(current_item.childCount()):
                nchild_item = QTreeWidgetItem()
                nchild_item.setData(0, Qt.UserRole, current_item.child(indx).data(0, Qt.UserRole))
                nitem.addChild(nchild_item)
                self.task_moved.emit(nchild_item)
        
        #accept event       
        event.accept()   
            
                    
            

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()