from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPixmap, QIcon

import sys




app = QApplication(sys.argv)
w = QMainWindow()
w.setBaseSize(QSize(200, 200))

tree = QTreeWidget()
tree.setHeaderLabel("Items")
tree.setDragEnabled(True)
tree.setDragDropMode(tree.InternalMove)
tree.setColumnCount(1)
tree_items = []
for i in range(5):
    tree_items.append(QTreeWidgetItem(None, f"hello {i}"))

tree_items[3].addChild(QTreeWidgetItem(None, "Children"))

print(tree_items[1].parent())
print(tree_items[3].child(0))

tree.addTopLevelItems(tree_items)
w.setCentralWidget(tree)
w.show()
app.exec_()