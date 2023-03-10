import sys
from time import sleep
from PySide2.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        
        #QLabel
        self.label = QLabel("Hello")
        self.label.setText("Bye")
        font = self.label.font()
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        """
        Other alignament flags:
            Qt.AlignLeft	Aligns with the left edge.
            Qt.AlignRight	Aligns with the right edge.
            Qt.AlignHCenter	Centers horizontally in the available space.
            Qt.AlignJustify	Justifies the text in the available space.
            
            Qt.AlignTop	Aligns with the top.
            Qt.AlignBottom	Aligns with the bottom.
            Qt.AlignVCenter	Centers vertically in the available space.
            
            Qt.AlignCenter	Centers horizontally and vertically
        """        
        
        
        #QCheckBox
        cbox = QCheckBox()
        cbox.setCheckState(Qt.Checked)
        
        cbox.stateChanged.connect(self.show_state)
        
        #QComboBox
        cbbox = QComboBox()
        cbbox.addItems(["one", "two", "three"])
        cbbox.currentIndexChanged.connect(self.show_state)
        cbbox.currentTextChanged.connect(self.show_state)
        
        #QLineEdit
        
        #QDial
        
        #QSlider
        
        #QListWidget
        
        #QTabWidget
        
        list = QListWidget()
        list.addItems(["one", "two", "three"])
        
        list.currentItemChanged.connect(self.show_state)
        
        
        
        self.setCentralWidget(cbbox)
        
        
        
    def mousePressEvent(self, e):
        self.label.setPixmap(QPixmap("res/image.jpg"))
        
    def show_state(self, s):
        print(s)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
