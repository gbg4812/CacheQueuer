# Std library Imports
import sys
import json

# PySide6 Imports
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QMessageBox,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QTreeWidgetItem,
    QSplitter,
)
from PySide6.QtGui import QCloseEvent
from custom_widgets import ItemDelegate

# Local Imports
import config
from renderers import RenderThread
from global_enums import DataRoles
from custom_widgets import TasksTree, ParmsWidget, SysInfoWidget
from utils import Logger


# Configure logger
flog = Logger(__name__)


# Class that represents the main application window
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Cache Queuer")

        self.data_file = f"{config.ROOT_DIR}/data/task_data.json"
        self.render_thread = RenderThread()

        # Init UI
        central_w = QWidget()
        layout = QVBoxLayout(central_w)
        splitter = QSplitter(Qt.Horizontal)

        # Task Tree
        self.task_tree = TasksTree()
        self.task_tree.render_tasks.connect(self.render_thread.render)
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

        self.render_thread.progress_updated.connect(self.parms.update_handler)
        splitter.addWidget(self.parms)
        self.task_tree.itemSelectionChanged.connect(self.itemSelectionChanged)

        layout.addWidget(splitter, stretch=1)

        self.setCentralWidget(central_w)

    def reload(self):
        try:
            with open(self.data_file, "r") as f:
                tasks = json.load(f)
                for task in tasks:
                    task: dict
                    item = QTreeWidgetItem()
                    item.setData(0, DataRoles.TYPE, ItemDelegate.UiTypes.TASK_ITEM)
                    item.setData(0, DataRoles.NAME, task.get("name"))
                    item.setData(0, DataRoles.DATA, task)
                    item.setFlags(
                        (item.flags() | Qt.ItemIsEditable) ^ Qt.ItemIsDropEnabled
                    )
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

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.render_thread.rendering:
            replay = QMessageBox.question(
                self,
                "Close",
                "If you close the window now, the current render will be killed!!!",
                QMessageBox.Yes,
                QMessageBox.No,
            )

            if replay == QMessageBox.No:
                event.ignore()
        else:
            self.render_thread.killThread()
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open(f"{config.ROOT_DIR}/style/style.qss", "r") as f:
        app.setStyleSheet(f.read())

    w = MainWindow()
    w.setWindowTitle("CacheQueuer")
    w.setGeometry(0, 0, 1000, 500)
    w.show()
    sys.exit(app.exec_())
