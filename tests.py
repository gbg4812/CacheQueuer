import json
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, QSize, QJsonValue
from PySide2.QtGui import QPixmap, QIcon, QDropEvent
from custom_widgets import TaskDelegate, WidgetState, CustomRoles, ItemTypes
import sys

app = QApplication(sys.argv)

tree = QTreeWidget()
tree.setDragDropMode(tree.DragDropMode.InternalMove)
tree.setDragEnabled(True)
tree.setEditTriggers(tree.EditTrigger.DoubleClicked)

tree.setItemDelegate(TaskDelegate())
with open('res/tasks_data.json', 'r') as f:
    tasks = json.load(f)
    for task in tasks:
        task: dict
        item = QTreeWidgetItem()
        item.setData(0, Qt.DisplayRole, task.pop("name"))
        item.setData(0, CustomRoles.DependentState,  WidgetState.ENABLED)
        item.setData(0, CustomRoles.EnableState,  WidgetState.ENABLED)
        item.setData(0, CustomRoles.ItemType, ItemTypes.TaskItem)   
        item.setData(0, Qt.UserRole, task)
        item.setFlags( item.flags() | Qt.ItemIsEditable)
        tree.addTopLevelItem(item)
w = QMainWindow()
w.setCentralWidget(tree)

w.show()
sys.exit(app.exec_())
