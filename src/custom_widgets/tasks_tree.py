# std imports
from __future__ import annotations

# PySide6 imports
from PySide6.QtWidgets import QTreeWidget, QWidget, QPushButton, QLabel, QHBoxLayout, QTreeWidgetItem
from PySide6.QtCore import Qt, Signal, QModelIndex, QItemSelectionModel
from PySide6.QtGui import QDropEvent

# local imports
from .item_delegate import ItemDelegate 
from .task_ui import TaskUi
from delegate_subitems import IconButton
from global_enums import DataRoles

#Subclass Of The TreeWidget 
class TasksTree(QTreeWidget):
    render_tasks = Signal(list)

    def __init__(self):
        super(TasksTree, self).__init__()

        self.setColumnCount(1)
        self.setIndentation(0)
        
        self.setHorizontalScrollMode(QTreeWidget.ScrollPerPixel)
        self.setVerticalScrollMode(QTreeWidget.ScrollPerPixel)
        
        self.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self.model().rowsInserted.connect(self.consistent_selection)
        
        #Create Header
        header_item = QTreeWidgetItem()
        header_item.setData(0,DataRoles.TYPE, ItemDelegate.UiTypes.HEADER_ITEM)
    
        #Header Widget
        header_w = QWidget()
        header_l = QHBoxLayout(header_w)
        
        ndir_bttn = QPushButton("New Dependency Directory")
        ndir_bttn.clicked.connect(self.add_dir)
        header_lab = QLabel("Tasks")
        header_lab.setAlignment(Qt.AlignCenter)
        
        header_l.addWidget(header_lab, alignment=Qt.AlignCenter)
        header_l.addWidget(ndir_bttn, alignment=Qt.AlignCenter)

        #Configure item
        header_item.setSizeHint(0, header_w.sizeHint())
        header_item.setFlags(Qt.NoItemFlags)
        
        #Assign Header Item to tree
        self.addTopLevelItem(header_item)
        self.setHeaderHidden(True)
        self.setItemWidget(header_item, 0, header_w)

        #Enable Drag And Drop
        self.setDragEnabled(True)
        self.setDragDropMode(self.DragDropMode.InternalMove)

        #Enable Item Editing and se Correct Delegate
        self.setEditTriggers(QTreeWidget.EditTrigger.DoubleClicked)
        self.delegate = ItemDelegate()
        self.delegate.render_task.connect(self.render_task)
        self.delegate.render_dir.connect(self.render_dir)
        self.delegate.data_changed.connect(self.data_changed)
        self.setItemDelegate(self.delegate)

        
    def dropEvent(self, event: QDropEvent) -> None:
        
        #Item where user drops and its parent
        current_item  = self.currentItem()
        tg_item  = self.itemAt(event.pos())
        drop_pos = self.dropIndicatorPosition()
        
        if not tg_item:
            event.ignore()
            return

        
        DIP = QTreeWidget.DropIndicatorPosition            
        if current_item.data(0, DataRoles.TYPE) == ItemDelegate.UiTypes.DIR_ITEM:
            if tg_item.parent():
                event.ignore()
                return

        if drop_pos == DIP.OnItem:
            if current_item.data(0, DataRoles.TYPE) == ItemDelegate.UiTypes.DIR_ITEM:
                event.ignore()
                return
        return super().dropEvent(event) 
    
    def render_dir(self, parent_index: QModelIndex) -> None:
        data = self.flatten_tree(parent=parent_index)
        self.render_tasks.emit(data)
        
        
    def render_task(self, index: QModelIndex) -> None:
        data = [{"dependent":False, "indexes":[index,]},]
        self.render_tasks.emit(data)
    
    def data_changed(self):
        self.itemSelectionChanged.emit()
    
        
    def add_dir(self):
        item = QTreeWidgetItem()
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        self.addTopLevelItem(item)
        self.resizeColumnToContents(0)
    

    def flatten_tree(self, parent: QModelIndex) -> list:
        result = []
        bundle = {"dependent": False, "indexes":[]}
        model = self.model()
        if parent.data(TaskUi.DataRoles.ENABLE) == IconButton.ButtonStates.CLICKED:
            bundle['dependent'] = True

        if model.hasChildren(parent):
            for row in range(model.rowCount(parent)):
                child_index = model.index(row, 0, parent)
                if child_index.data(TaskUi.DataRoles.ENABLE) == IconButton.ButtonStates.CLICKED:

                    if child_index.data(DataRoles.TYPE) == ItemDelegate.UiTypes.TASK_ITEM:
                        bundle['indexes'].append(child_index)

                    elif child_index.data(DataRoles.TYPE) == ItemDelegate.UiTypes.DIR_ITEM:
                        bundlecpy = dict(bundle)
                        result.append(bundlecpy)
                        result.extend(self.flatten_tree(child_index))
                        bundle["indexes"] = []
                        bundle["dependent"] = False

            result.append(bundle)

        
        return result

    def consistent_selection(self, parent: QModelIndex, first, last):
        sm = self.selectionModel()
        idx = self.model().index(first, 0, parent)
        sm.select(idx, QItemSelectionModel.Select)

