# std imports
from typing import List, Union, Optional, Dict

# PySide2 imports
from PySide2.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTreeWidgetItem,
    QProgressBar,
    QFormLayout,
    QFrame,
    QLineEdit,
)
from PySide2.QtCore import Signal, QModelIndex, QItemSelection, Qt, Slot
from custom_widgets.item_delegate import ItemDelegate
from custom_widgets.task_ui import TaskUi
from utils import Logger

# Local imports
from global_enums import DataRoles, TaskStates

flog = Logger(__name__)


class ParmsWidget(QFrame):
    def __init__(self):
        super(ParmsWidget, self).__init__()
        self.setObjectName("Parms")

        self.current_item = None

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name = QLabel()
        self.name.setObjectName("Title")
        self.name.setAlignment(Qt.AlignCenter)

        self.lab_frame = QFrame()
        self.lab_layout = QFormLayout()
        self.lab_layout.setLabelAlignment(Qt.AlignRight)
        self.lab_frame.setLayout(self.lab_layout)

        self.labels: List[Union[QLineEdit, QLabel]] = []

        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.lab_frame, stretch=1)
        layout.addWidget(self.progress, alignment=Qt.AlignBottom)

    def itemSelected(self, item: QTreeWidgetItem):
        self.current_item = item
        self.update_handler()
        self.itemChanged(item)

    @Slot()
    def itemChanged(self, item: Union[QTreeWidgetItem, None]):
        if item:
            if item.isSelected():
                # Clear Tab
                for lab in self.labels:
                    self.lab_layout.removeWidget(lab)
                    lab.deleteLater()

                self.labels.clear()

                if item:
                    if item.data(0, DataRoles.TYPE) == ItemDelegate.UiTypes.TASK_ITEM:
                        data: dict = item.data(0, DataRoles.DATA)
                        self.name.setText(item.data(0, DataRoles.NAME))
                        self.lab_layout.addRow(self.name)

                        for key, val in data.items():
                            # Label Side
                            key: str
                            key = key.replace("_", " ")
                            key = key.capitalize()
                            lab = QLabel("{}:".format(key))
                            lab.setObjectName("Label")

                            # Info Side
                            info = QLineEdit("{}".format(val))
                            info.setReadOnly(True)
                            info.setObjectName("Info")
                            info.setMinimumWidth(50)

                            self.lab_layout.addRow(lab, info)
                            self.labels.append(lab)
                            self.labels.append(info)

                    elif item.data(0, DataRoles.TYPE) == ItemDelegate.UiTypes.DIR_ITEM:
                        self.name.setText(item.data(0, DataRoles.NAME))
                        newLab = QLabel(
                            "Dependent: {}".format(
                                item.data(0, TaskUi.DataRoles.DEPENDENT)
                            )
                        )
                        self.layout().addWidget(newLab)
                        self.labels.append(newLab)

                else:
                    self.name.clear()

    @Slot()
    def update_handler(self, progress: Optional[Dict] = None):
        if self.current_item:
            itemstate = self.current_item.data(0, DataRoles.TASKSTATE)

            if itemstate == TaskStates.RENDERING:
                flog.debug("Current Item is rendering so we update the progress")
                if progress:
                    percent = progress.get("Progress") / (
                        progress.get("Range")[1] - progress.get("Range")[0]
                    )
                    percent *= 100
                    self.progress.setValue(percent)
                return

            elif itemstate == TaskStates.SUCCESSFUL:
                self.progress.setValue(100)

            else:
                self.progress.setValue(0)
        else:
            self.progress.setValue(0)
