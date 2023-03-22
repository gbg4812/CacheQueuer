from __future__ import annotations


from .name_label_widget import NameLabelWidget
from .task_item import TaskItem
from PySide2.QtWidgets import  QTreeWidgetItem, QWidget, QHBoxLayout, QPushButton, QCheckBox, QTreeWidgetItemIterator
from PySide2.QtCore import Signal

class DirItemWidget(QWidget):

    render_clicked = Signal()
    remove_clicked = Signal()

    dependency_changed = Signal(bool)
    
    def __init__(self, name, is_dependent):
        super(DirItemWidget, self).__init__()
        
        layout = QHBoxLayout(self)
        
        #Label Name
        self._label = NameLabelWidget(name)
        self.dep_check = QCheckBox("Make tasks dependent")
        self.dep_check.setChecked(is_dependent)
        self.dep_check.toggled.connect(self.dep_changed)

        #Buttons
        renderButton = QPushButton("Render")
        renderButton.clicked.connect(self.rndr_dir)
        rmButton = QPushButton("Remove")
        rmButton.clicked.connect(self.rm_dir)
        
        layout.addWidget(self._label)
        layout.addWidget(self.dep_check)
        layout.addWidget(renderButton)
        layout.addWidget(rmButton)
        
    def rndr_dir(self):
        self.render_clicked.emit()
        
    def rm_dir(self):
        self.remove_clicked.emit()
    
    def dep_changed(self):
        self.dependency_changed.emit(self.dep_check.isChecked())

    def getName(self) -> str:
        return self._label.getText()
    def getChecked(self) -> bool:
        return self.dep_check.isChecked()


class DirItem(QTreeWidgetItem):

    render_clicked = Signal(QTreeWidgetItem)

    def __init__(self, name="New Directory", dependent=False):
        super(DirItem, self).__init__()

        self.dependent = dependent

        self.widget = DirItemWidget(name, dependent)

        self.widget.render_clicked.connect(self.rndr_clicked)
        self.widget.remove_clicked.connect(self.self_remove)
        self.widget.dependency_changed.connect(self.set_dependency)

        self.setSizeHint(0, self.widget.sizeHint())

    def rndr_clicked(self):
        self.render_clicked.emit(self)

    def self_remove(self):
        it = QTreeWidgetItemIterator(self)

        while it.value():
            child : TaskItem = it.value()
            self.removeChild(child)
            it+=1
        
        tree_w = self.treeWidget()
        tree_w.removeItemWidget(tree_w.indexOfTopLevelItem(self))

    def set_dependency(self, is_dependent: bool):
        self.dependent = is_dependent

    def addChild(self, child: TaskItem) -> None:
        super().addChild(child)
        self.treeWidget().setItemWidget(child, 0, child.widget)

    def insertChild(self, index: int, child: TaskItem) -> None:
        super().insertChild(index, child)
        self.treeWidget().setItemWidget(child, 0, child.widget)

    def getName(self) -> str:
        return self.widget.getName()
    
    def getDependent(self) -> bool:
        return self.widget.getChecked()

        

        