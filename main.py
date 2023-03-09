from PySide2.QtWidgets import (QMainWindow, QApplication, QListWidget, QVBoxLayout)
import hou
import sys

class CacheQueuer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.BoxLayout = QVBoxLayout()
        self.list = QListWidget()
        self.BoxLayout.addWidget(self.list)
        self.setLayout(self.BoxLayout)


class Task():
    def __init__(self, name, roppath):
        self.name = name
        self.roppath = roppath
    def render(self):
        node = hou.node(self.roppath)
        try:
            node.render()
        except AttributeError:
            child = node.node("render")
            child.render()
        else:
            print("The node is invalid")




if __name__=="__main__":
    app = QApplication(sys.argv)

    mw = CacheQueuer()
    mw.show()

    sys.exit(app.exec_())


