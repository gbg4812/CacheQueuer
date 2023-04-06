from .hou_renderer import HouRenderer
from global_enums import *
class RenderHelpers:
    def render_task(task_data: dict) -> bool:
        HouRenderer.render_task(task_data)

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
                    HouRenderer.render_task(task)
                
        
