from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPixmap, QIcon, QDropEvent

import sys

class TasksTree(QTreeWidget):
    def __init__(self):
        super(TasksTree, self).__init__()
        
    def dropEvent(self, event: QDropEvent) -> None:
        if self.currentItem().data(0, Qt.UserRole) < 0 and self.dropIndicatorPosition() == QTreeWidget.DropIndicatorPosition.OnItem:
            event.ignore()
        else:
            return super().dropEvent(event)

def print_userRole(item, column):
    print(item.data(0, Qt.UserRole))

app = QApplication(sys.argv)

tree = TasksTree()
tree.setHeaderLabel("Items")
tree.setDragEnabled(True)
tree.setDragDropMode(tree.InternalMove)
tree.setColumnCount(1)
tree_items = []
for i in range(5):
    item = QTreeWidgetItem()
    item.setText(0, f"Item {i}")
    item.setData(0, Qt.UserRole, -1)
    tree_items.append(item)

tree_items[3].addChild(QTreeWidgetItem(None, "Children"))
tree_items[3].child(0).setData(0, Qt.UserRole, 0)
tree_items[3].child(0).setFlags(tree_items[3].child(0).flags() ^ Qt.ItemIsDropEnabled)

tree.itemClicked.connect(print_userRole)

print(tree_items[1].parent())
print(tree_items[3].child(0))

tree.addTopLevelItems(tree_items)



w = QMainWindow()
w.setBaseSize(QSize(200, 200))

w.setCentralWidget(tree)
w.show()
app.exec_()