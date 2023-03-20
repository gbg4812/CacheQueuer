from PySide2.QtWidgets import QLineEdit, QLabel, QStackedWidget
from PySide2.QtGui import QMouseEvent
from PySide2.QtCore import Signal


class NameLabelWidget(QStackedWidget):
    name_changed = Signal(str)

    def __init__(self, text):
        super(NameLabelWidget, self).__init__()

        self.setAcceptDrops(False)

        self.label = QLabel(text)
        self.line_edit = QLineEdit(text)
        self.addWidget(self.line_edit)
        self.addWidget(self.label)

        self.setCurrentWidget(self.label)

        self.line_edit.editingFinished.connect(self.show_label)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.setCurrentWidget(self.line_edit)

    def show_label(self):
        self.label.setText(self.line_edit.text())
        self.setCurrentWidget(self.label)

    def nm_changed(self):
        self.name_changed.emit(self.line_edit.text())

    def setText(self, text: str):
        self.label.setText(text)

    def getText(self) -> str:
        return self.label.text()



        
