from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QTreeWidgetItem

from PySide2.QtCore import Signal, QModelIndex
from global_enums import CustomRoles

class ParmsWidget(QWidget):
    def __init__(self):
        super(ParmsWidget, self).__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name = QLabel()
        self.info = QLabel()
        
        layout.addWidget(self.name)
        layout.addWidget(self.info)        


    def itemSelected(self, item: QTreeWidgetItem):
        self.name.setText(item.data(0, CustomRoles.TaskName))

