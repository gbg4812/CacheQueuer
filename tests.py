from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPixmap, QIcon, QDropEvent

import sys

app = QApplication(sys.argv)

tree = QTreeWidget()
tree.setDragDropMode(tree.DragDropMode.InternalMove)
tree.setDragEnabled(True)
tree_item1 = QTreeWidgetItem('item 1')
tree_item2 = QTreeWidgetItem('item 2')
tree_item3 = QTreeWidgetItem('item 3')
tree_item4 = QTreeWidgetItem('item 4')
tree.addTopLevelItem(tree_item1)
tree.addTopLevelItem(tree_item3)
tree.addTopLevelItem(tree_item2)
tree_item3.insertChild(0, tree_item4)
w = QMainWindow()
w.setCentralWidget(tree)

w.show()
app.exec_()