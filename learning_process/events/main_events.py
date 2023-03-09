from PySide2.QtWidgets import QMainWindow, QApplication, QListWidget, QVBoxLayout, QPushButton, QLabel
from PySide2.QtCore import Qt, QSize
import hou
import sys

#Any top level widget is redy to create a window on its one, but they can be parented inside layouts.
class CacheQueuer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Configure Main Window
        self.setWindowTitle("My App")
        self.setFixedSize(QSize(600, 400))
        
        self.label = QLabel("Not events called")
        
        self.setMouseTracking(True) #Trigger mouseMoveEvent when it is not clicked
        
        self.setCentralWidget(self.label)
        
    # When the mouse is clicked a QMouseEvent (e) is sent to the mousePressEvent event handler and the handler is called
    def mouseMoveEvent(self, e):
        self.label.setText("mouseMoveEvent")
        print(e.globalPos())

    def mousePressEvent(self, e):
        self.label.setText("mousePressEvent")
        print(e.button())

    def mouseReleaseEvent(self, e):
        self.label.setText("mouseReleaseEvent")

    def mouseDoubleClickEvent(self, e):
        self.label.setText("mouseDoubleClickEvent")


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
    #QApplication holds the event loop
    app = QApplication(sys.argv)

    mw = CacheQueuer()
    mw.show()
    
    #start event loop
    sys.exit(app.exec_())


