from __future__ import annotations

from PySide2.QtWidgets import QTreeWidgetItem, QWidget, QHBoxLayout, QPushButton, QComboBox, QTreeWidget
from PySide2.QtCore import Qt, Signal, QSize
from PySide2.QtGui import QPixmap, QIcon
from .name_label_widget import NameLabelWidget

import enum

#Class defining the state of a task
class TaskState(enum.IntEnum):
    WAITING = 0
    RENDERING = 1
    SUCCESFUL = 2
    FAILED = 3

#Custom Widget For the TreeWidgetItems that has controls to manipulate every task separately.
#It emits rm_task and rndr_task signals
class TaskItemWidget(QWidget):

    #First Int => TaskId
    render_clicked = Signal()
    remove_clicked = Signal()
    
    #Second the new state of the task
    state_changed = Signal(TaskState)
    name_changed = Signal(str)

    def __init__(self, name: str):
        super(TaskItemWidget, self).__init__()

        layout = QHBoxLayout()
        
        #Label Name
        self.label = NameLabelWidget(name)

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
        
        layout.addWidget(self.label)
        layout.addWidget(renderButton)
        layout.addWidget(rmButton)
        layout.addWidget(self.stateMenu)

        self.setLayout(layout)
    
    #<---- SLOTS ---->

    def rm_task(self):
        self.remove_clicked.emit()      
        self.deleteLater()
        
    def rndr_task(self):
        self.render_clicked.emit()
        
    def st_changed(self, index):
        self.state_changed.emit(index)

    def nm_chaged(self,  name: str):
        self.name_changed.emit(name)
    
    #<---- Getters and Setters ---->

    def setState(self, state: TaskState):
        self.stateMenu.setCurrentIndex(state)
    
    def getState(self) -> TaskState:
        return TaskState(self.stateMenu.currentIndex())
    
    def setName(self, name: str):
        self.label.setText(name)

    def getName(self) -> str:
        return self.label.getText()
    


# <---- Task Item Class ---->
class TaskItem(QTreeWidgetItem):

    render_clicked = Signal()

    def __init__(self, task: dict):
        super(TaskItem, self).__init__()

        self.setFlags(self.flags() ^ Qt.ItemFlag.ItemIsDropEnabled)

        self.name = task.get("name")
        self.rop_path = task.get("rop_path")
        self.hip_file = task.get("hip_file")

        self.widget = TaskItemWidget(self.name)

        self.setState(task.get('state'))

        self.widget.render_clicked.connect(self.rndr_clicked)
        self.widget.remove_clicked.connect(self.self_remove)
        self.widget.state_changed.connect(self.setState)

    def updateWidget(self):
        self.widget.setState(self.state)
        self.widget.setName(self.name)
    
    def updateDataFromWidget(self):
        self.name = self.widget.getName()
        self.state = self.widget.getState()

    def rndr_clicked(self):
        self.render_clicked.emit()
    
    def self_remove(self):
        tree_w = self.treeWidget()
        parent = self.parent()
        tree_w.removeItemWidget(self, 0)
        if parent:
            parent.takeChild(parent.indexOfChild(self))

        else:
            tree_w.takeTopLevelItem(tree_w.indexOfTopLevelItem(self))
    
    def setState(self, state: TaskState):
        self.state = state
        self.widget.setState(state)

    def getTaskDict(self) -> dict:
        return dict(name=self.name, state=self.state, rop_path=self.rop_path, hip_file=self.hip_file)
        

