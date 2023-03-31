import hou
import time

#renders a single task given a id
class HouRenderer():   
    def render_task(task: dict or list, dependent=False):
        if isinstance(task, dict):
            print("rendering a sigle task...")
            time.sleep(3)
            print("complete")
        elif isinstance(task, list):
            print("rendering a list of tasks...")
            time.sleep(5)
            print("complete")
        # hou.hipFile.load(task["hip_file"])
        # node : hou.RopNode = hou.node(task["rop_path"])

        # if type(node) == hou.RopNode:
        #     try:
        #         node.render(verbose=True, output_probress=True)
        #     except hou.OperationFailed:
        #         return False
        # elif type(node) == hou.SopNode:
        #     try:
        #         rop_node = node.node('render')
        #         rop_node.render(verbose=True, output_process = True)
        #     except hou.OperationFailed:
        #         return False
        # else:    
        #     print('the node is not of the correct type')
        
        return True
