from typing import List
from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QTreeWidgetItem, QProgressBar, QLineEdit 

from PySide2.QtCore import Signal, QModelIndex, QItemSelection, Qt
from global_enums import CustomRoles, ItemTypes
class ParmsWidget(QWidget):
    def __init__(self):
        super(ParmsWidget, self).__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name = QLabel()
        self.name.setAlignment(Qt.AlignCenter)
        self.labels : List[QLabel] = []

        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.name)
        layout.addWidget(self.progress)        
        layout.addStretch(1)


    def itemSelected(self, item: QTreeWidgetItem):
        for lab in self.labels:
            self.layout().removeWidget(lab)
            lab.deleteLater()
        
        self.labels.clear()
        
        if item:
            if item.data(0, CustomRoles.ItemType) == ItemTypes.TaskItem:
                data : dict = item.data(0, CustomRoles.TaskData)
                self.name.setText(item.data(0, CustomRoles.TaskName))
                for key, val in data.items():
                    newLab = QLabel("{}: {}".format(key, val))
                    self.layout().addWidget(newLab)
                    self.labels.append(newLab)

            elif item.data(0, CustomRoles.ItemType) == ItemTypes.DirItem:
                self.name.setText(item.data(0, CustomRoles.TaskName))
                newLab = QLabel("Dependent: {}".format(item.data(0,CustomRoles.DependentState)))
                self.layout().addWidget(newLab)
                self.labels.append(newLab)
        
        else: 
            self.name.clear()
    
    def update_handler(self, progress: float):
            self.progress.setValue(progress * 100)
