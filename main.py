# Std library Imports
import sys
from os import path
import json
import logging

# PySide2 Imports
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QMainWindow, QApplication,
    QPushButton,
    QHBoxLayout, QVBoxLayout, QWidget,
    QTreeWidgetItem, QSplitter
)
from custom_widgets import ItemDelegate

# Local Imports
from renderers import RenderManager
from global_enums import DataRoles
from custom_widgets import TasksTree, ParmsWidget, SysInfoWidget 


# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Configure env variables
class env:
    wrkdir, _ = path.split(__file__)

# Class that represents the main application window
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Cache Queuer")

        self.data_file = f"{env.wrkdir}/data/task_data.json"
        self.renderManager = RenderManager()

        # Init UI
        central_w = QWidget()
        layout = QVBoxLayout(central_w)
        splitter = QSplitter(Qt.Horizontal)

        # Task Tree
        self.task_tree = TasksTree()
        self.task_tree.render_tasks.connect(self.renderManager.render)
        splitter.addWidget(self.task_tree)

        # Utils Bar. Render and Reload buttons + system info
        utilsl = QHBoxLayout()
        layout.addLayout(utilsl, stretch=0)

        reload_bttn = QPushButton("Reload")
        reload_bttn.clicked.connect(self.reload)
        utilsl.addWidget(reload_bttn)

        render_bttn = QPushButton("Render")
        render_bttn.clicked.connect(self.renderTree)
        utilsl.addWidget(render_bttn)
        utilsl.addStretch(1)

        sysinfo = SysInfoWidget()
        utilsl.addWidget(sysinfo, alignment=Qt.AlignRight | Qt.AlignVCenter)

        # Parameters
        self.parms = ParmsWidget()

        self.renderManager.progress_update.connect(self.parms.update_handler)
        splitter.addWidget(self.parms)
        self.task_tree.itemSelectionChanged.connect(self.itemSelectionChanged)

        layout.addWidget(splitter, stretch=1)

        self.setCentralWidget(central_w)

    def reload(self):
        try:
            with open(self.data_file, 'r') as f:
                tasks = json.load(f)
                for task in tasks:
                    task: dict
                    item = QTreeWidgetItem()
                    item.setData(0, DataRoles.TYPE, ItemDelegate.UiTypes.TASK_ITEM)
                    item.setData(0, DataRoles.NAME, task.get("name"))
                    item.setData(0, DataRoles.DATA, task)
                    item.setFlags((item.flags() | Qt.ItemIsEditable)
                                  ^ Qt.ItemIsDropEnabled)
                    self.task_tree.addTopLevelItem(item)
                    self.task_tree.resizeColumnToContents(0)

            # os.remove(self.data_file)

        except FileNotFoundError:
            print("We couldn't find any tasks")

    def itemSelectionChanged(self) -> None:
        if self.task_tree.topLevelItemCount() > 0:
            self.parms.itemSelected(self.task_tree.currentItem())

    def renderTree(self):
        self.task_tree.render_dir(self.task_tree.rootIndex())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open(f"{env.wrkdir}/style/style.qss", 'r') as f:
        app.setStyleSheet(f.read())
    w = MainWindow()
    w.setWindowTitle("CacheQueuer")
    w.setGeometry(0, 0, 1000, 500)
    w.show()
    sys.exit(app.exec_())

    def helloWorld():
        print("hello world!!!")
        for i in (1, 1, 2 ,3 ):
            print(i)

