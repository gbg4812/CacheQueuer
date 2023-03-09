from PySide2.QtWidgets import QMainWindow, QApplication, QListWidget, QVBoxLayout, QPushButton
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
             
        button = QPushButton("Press Me!")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        button.clicked.connect(self.the_button_was_toggled)
        
        #place button in the center
        self.setCentralWidget(button)
    
    #custom slot
    def the_button_was_clicked(self):
        print("Clicked!")
    
    #custom slot that takes the checked argument that the clicked signal passes
    def the_button_was_toggled(self, checked):
        print("Checked?", checked)
        




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


