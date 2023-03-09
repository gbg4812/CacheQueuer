from PySide2.QtWidgets import QMainWindow, QApplication, QListWidget, QVBoxLayout, QPushButton
from PySide2.QtCore import Qt, QSize
import hou
import sys

#Any top level widget is redy to create a window on its one, but they can be parented inside layouts.
class CacheQueuer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.button_is_checked = True
        
        #Configure Main Window
        self.setWindowTitle("My App")
        self.setFixedSize(QSize(600, 400))
             
        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.the_button_was_clicked)
        
        #place button in the center
        self.setCentralWidget(self.button)
    
    #custom slot that takes the checked argument that the clicked signal passes
    def the_button_was_clicked(self):
        self.button.setText("You alredy clicked me")
        self.button.setEnabled(False)
        
        self.setWindowTitle("The button has been clicked")
        




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


