from typing import List
import json
import hou

# Global Variables
userdir = hou.getenv("HOUDINI_USER_PREF_DIR")
data_file = userdir + "/Scripts/CacheQueuer/" + "data/task_data.json"
field_names = ("name", "rop_path", "frame_range",
               "shell_script", "hip_file", "houdini_v")
shell_script = "python {}".format(
    userdir + "/Scripts/CacheQueuer/renderers/hou_render.py")

nodes: List[hou.Node] = hou.selectedNodes()

try:
    with open(data_file, "r") as file:
        tasks: List[dict] = json.load(file, fieldnames=field_names)
        for node in nodes:
            task = {
                "name": node.name(),
                "rop_path": node.path(),
                "frame_range": [node.parm("f1").evalAsFloat(), node.parm("f2").evalAsFloat(), node.parm("f3").evalAsFloat()],
                "hip_file": hou.hipFile.path(),
                "shell_script": shell_script,
                "houdini_v": hou.applicationVersionString()
            }

            tasks.append(task)

        file.close()

    with open(data_file, 'w') as file:
        jsonstr = json.dump(tasks, file)
except FileNotFoundError:
    tasks = []
    for node in nodes:
        task = {
            "name": node.name(),
            "rop_path": node.path(),
            "frame_range": [node.parm("f1").evalAsFloat(), node.parm("f2").evalAsFloat(), node.parm("f3").evalAsFloat()],
            "hip_file": hou.hipFile.path(),
            "shell_script": shell_script,
            "houdini_v": hou.applicationVersionString()
        }

        tasks.append(task)

    with open(data_file, 'x') as file:
        jsonstr = json.dump(tasks, file)
