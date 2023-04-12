from PySide2.QtWidgets import QWidget, QVBoxLayout, QLabel, QTreeWidgetItem, QProgressBar, QLineEdit 

from PySide2.QtCore import Signal, QModelIndex, QItemSelection, Qt
from global_enums import CustomRoles, ItemTypes
from renderers import HouRenderer, RendererInfo 
class ParmsWidget(QWidget):
    def __init__(self):
        super(ParmsWidget, self).__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name = QLabel()
        self.name.setAlignment(Qt.AlignCenter)
        self.label1 = QLabel()
        self.label1.setWordWrap(True)
        self.frame_range = QLabel()
        self.label2 = QLabel()
        self.label2.setWordWrap(True)

        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.name)
        layout.addWidget(self.label1)        
        layout.addWidget(self.frame_range)        
        layout.addWidget(self.label2)        
        layout.addWidget(self.progress)        
        layout.addStretch(1)


    def itemSelected(self, item: QTreeWidgetItem):
        if item:
            if item.data(0, CustomRoles.ItemType) == ItemTypes.TaskItem:
                data : dict = item.data(0, CustomRoles.TaskData)
                info : RendererInfo = HouRenderer.getInfo(data)

                self.name.setText(item.data(0, CustomRoles.TaskName))
                self.label1.setText("Render Node: " + info.label1)
                self.frame_range.setText("Frame Range: {f1}-{f2}".format(f1=info.frame_range[0], f2=info.frame_range[1]))
                self.label2.setText("Output Path: " + info.label2)

            elif item.data(0, CustomRoles.ItemType) == ItemTypes.DirItem:
                self.name.setText(item.data(0, CustomRoles.TaskName))
                self.label1	.setText("IsDependent: {}".format(item.data(0, CustomRoles.DependentState)))
                self.frame_range.setText("")
                self.label2.setText("")
        
        else: 
            self.name.clear()
            self.label1.clear()
            self.frame_range.clear()
            self.label2.clear()
    
    def update_handler(self, progress: float):
            self.progress.setValue(progress * 100)
