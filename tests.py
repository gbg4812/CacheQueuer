from PySide2.QtWidgets import QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout
from PySide2.QtCore import Qt


app = QApplication()

mw = QWidget()


mw.setWindowTitle("Test")
layout = QVBoxLayout()
tree_widget = QTreeWidget()
tree_widget.setEditTriggers(QTreeWidget.DoubleClicked)

names = ["Anna", "Isaac", "Guillem"]
for name in names:
    item = QTreeWidgetItem(name)
    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
    tree_widget.addTopLevelItem(item)
layout.addWidget(tree_widget)
mw.setLayout(layout)
mw.show()

app.exec_()