from PySide2.QtWidgets import QMainWindow, QApplication, QListWidget, QVBoxLayout, QPushButton, QLabel, QMenu, QAction
from PySide2.QtCore import Qt, QSize
import hou
import sys

#Any top level widget is redy to create a window on its one, but they can be parented inside layouts.
class CacheQueuer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Configure Main Window
        self.setWindowTitle("My App")
        
        #self.customContextMenuRequested.connect(self.on_context_menu) the signal/slot aproach
    
    # This event is triggered when the mouse is right clicked in the main window
    def contextMenuEvent(self, e):
        #create de menu
        context = QMenu(self)
        
        #add actions
        action = QAction("test 1", self)
        action.triggered.connect(self.action_triggered)
        context.addAction(action)
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.addAction(QAction("test 4", self))
        

        
        #execute de menu to show it and place it in the position of the mouse
        #if the parent widget isn't the top widget the position has to be relative
        context.exec_(e.globalPos())
    def action_triggered(self):
        print("Action Text 1 was triggered")

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


