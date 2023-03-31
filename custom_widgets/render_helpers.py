from PySide2.QtCore import QModelIndex, QAbstractItemModel
from .hou_task_renderer import HouRenderer
import threading
from .global_enums import *

class RenderHelpers:
    def render_task(index: QModelIndex, model: QAbstractItemModel) -> bool:

        for thread in threading.enumerate():
            if thread.getName() == "RenderThread":
                print("alredy rendering")
                return False

        render_thread = threading.Thread(target=HouRenderer.render_task, name="RenderThread", args=(index.data(CustomRoles.TaskData),))
        render_thread.start()

        return True

    def render_dir(index: QModelIndex, model: QAbstractItemModel) -> bool:
        dependent = index.data(CustomRoles.DependentState)
        child_data = []
        for child in range(model.rowCount(index)):
            child_index = model.index(child, 0, index)
            child_data.append(model.data(child_index, CustomRoles.TaskData))

        for thread in threading.enumerate():
            if thread.getName() == "RenderThread":
                print("alredy rendering")
                return False

        render_thread = threading.Thread(target=HouRenderer.render_task, name="RenderThread", args=(child_data,))
        render_thread.start()
        return True 