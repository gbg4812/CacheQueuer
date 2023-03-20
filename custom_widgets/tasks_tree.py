from __future__ import annotations


from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItemIterator, QWidget, QPushButton, QLabel, QHBoxLayout, QTreeWidgetItem
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QDropEvent
from .task_item import TaskItem, TaskState
from .dir_item import DirItem
from .hou_task_renderer import HouRenderer
#Subclass Of The TreeWidget 
class TasksTree(QTreeWidget):

    render_task = Signal(TaskItem)
    
    def __init__(self):
        super(TasksTree, self).__init__()

        self.setColumnCount(1)
        
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
        self.addTopLevelItem(header_item)
        self.setHeaderHidden(True)
        self.setItemWidget(header_item, 0, header_w)

        
        #Enable Drag And Drop
        self.setDragEnabled(True)
        self.setDragDropMode(self.InternalMove)
        
    def dropEvent(self, event: QDropEvent) -> None:
        
        #Item where user drops and its parent
        current_item  = self.currentItem()
        tg_item  = self.itemAt(event.pos())
        tg_parent : DirItem = tg_item.parent()
        drop_pos = self.dropIndicatorPosition()

        
        #nitem.setFlags(nitem.flags() ^ Qt.ItemIsDropEnabled)
        DIP = QTreeWidget.DropIndicatorPosition            
        if isinstance(current_item, TaskItem):

            nitem = TaskItem(current_item.getTaskDict())
            if drop_pos == DIP.OnItem and tg_item != current_item.parent():
                tg_item.addChild(nitem)
                
            elif drop_pos == DIP.AboveItem:
                if tg_parent:
                    tg_parent.insertChild(tg_parent.indexOfChild(tg_item), nitem)
                else:
                    self.insertTopLevelCustomItem(self.indexOfTopLevelItem(tg_item), nitem)
                
            elif drop_pos == DIP.BelowItem:
                if tg_parent:
                    tg_parent.insertChild(tg_parent.indexOfChild(tg_item) + 1, nitem)
                elif tg_item.isExpanded():
                    tg_item.addChild(nitem)
                else:
                    self.insertTopLevelCustomItem(self.indexOfTopLevelItem(tg_item) + 1, nitem)
            else:
                event.ignore()
                return None

        elif isinstance(current_item, DirItem):

            nitem = DirItem(current_item.getName(), current_item.getDependent())
            if drop_pos == DIP.OnItem:
                event.ignore()
                return None
                
            elif drop_pos == DIP.AboveItem:
                if tg_parent:
                    event.ignore()
                    return None
                else:
                    self.insertTopLevelCustomItem(self.indexOfTopLevelItem(tg_item), nitem)
                
            elif drop_pos == DIP.BelowItem:
                if tg_parent:
                    event.ignore()
                    return None
                else:
                    self.insertTopLevelCustomItem(self.indexOfTopLevelItem(tg_item) + 1, nitem)
            
            #Move directory contents 
            for index in range(current_item.childCount()):
                item : TaskItem = current_item.child(index)
                nchild_item = TaskItem(item.getTaskDict())
                nitem.addChild(nchild_item)
       
        #accept event       
        event.accept()
    
    def addTopLevelCustomItem(self, item: TaskItem) -> None:
        super().addTopLevelItem(item)
        self.setItemWidget(item, 0, item.widget)

    
    def insertTopLevelCustomItem(self, index: int, item: TaskItem) -> None:
        super().insertTopLevelItem(index, item)
        self.setItemWidget(item, 0, item.widget)

    def add_dir(self):
        dir = DirItem()
        self.addTopLevelCustomItem(dir)

    #renders all the tasks
    def render(self):
        it = QTreeWidgetItemIterator(self)
        dependent = False
        success = True
        while it.value():
            #Select Task Folders With dependency disabled
            item = it.value()
            
            if type(item) == DirItem:
                item : DirItem
                dependent = item.getDependent()
                success = True
                
            #Selects Tasks
            elif type(item) == TaskItem:
                item : TaskItem
                if item.state == TaskState.WAITING:
                    item.setState(TaskState.RENDERING)
                    #Handles dependent tasks
                    if item.parent() == None:
                        success = HouRenderer.render_task(item)
                        
                    elif dependent == True and success == True:
                        success = HouRenderer.render_task(item)
                    
                    #Handles independent tasks
                    elif dependent == False:
                        success = HouRenderer.render_task(item)

                    #Sets state after rendering
                    if success:
                        item.setState(TaskState.SUCCESFUL)
                    else:
                        item.setState(TaskState.FAILED)
            it+=1

    def render_dir(self, item: DirItem):
        it = QTreeWidgetItemIterator(item)
        success = True
        dependent = item.getDependent()

        while it.value():
            #Handles dependent tasks
            child_item : TaskItem = it.value()
            if child_item.state == TaskState.WAITING:
                
                if dependent == True and success == True:
                    success = HouRenderer.render_task(item)
                
                #Handles independent tasks
                elif dependent == False:
                    success = HouRenderer.render_task(item)

                #Sets state after rendering
                if success:
                    child_item.setState(TaskState.SUCCESFUL)
                else:
                    child_item.setState(TaskState.FAILED)
            it+=1
