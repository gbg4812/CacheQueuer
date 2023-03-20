import hou
from .task_item import TaskItem


#renders a single task given a id
class HouRenderer():   
    def render_task(task: TaskItem):
        print("RENDERIRNG::TASK {}".format(task.name))

        hou.hipFile.load(task.hip_file)
        node : hou.RopNode = hou.node(task.rop_path)

        if type(node) == hou.RopNode:
            try:
                node.render(verbose=True, output_probress=True)
            except hou.OperationFailed:
                return False
        elif type(node) == hou.SopNode:
            try:
                rop_node = node.node('render')
                rop_node.render(verbose=True, output_process = True)
            except hou.OperationFailed:
                return False
        else:    
            print('the node is not of the correct type')
        
        return True
