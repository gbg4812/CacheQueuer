from .hou_renderer import HouRenderer
from global_enums import *
from PySide2.QtCore import Signal, QObject
class RenderHelpers(QObject):
    progress_updated = Signal(float)

    def render_task(task_data: dict) -> bool:
        renderer = HouRenderer()
        renderer.progress_updated.connect()
        HouRenderer.renderTask(task_data)

    def render_list(task_list: list) -> bool:
        print("Rendering list: {}".format(task_list))
        dependent = False
        success = True
        for task in task_list:
            task : dict
            if task.get("dependent") != None:
                dependent = task.get("dependent")
                success = True
            else:
                if dependent and not success: 
                    continue
                else:
                    HouRenderer.renderTask(task)
    def progressUpdated(self, progress):
        self.progress_updated.emit(progress)
                
        
