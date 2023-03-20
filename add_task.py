import json
import hou

#Global Variables
userdir = hou.getenv("HOUDINI_USER_PREF_DIR")
data_file = userdir + "/Scripts/CacheQueuer/" + "res/task_data.json"
field_names = ("name", "rop_path", "state")
        
nodes = hou.selectedNodes()

try:
    with open(data_file, "r") as file:
        tasks = json.laod(file, fieldnames=field_names)
        for node in nodes:
            task = {
                "name" : node.name(),
                "rop_path" : node.path(),
                "state" : 0
            }
            
            tasks.append(task)

        file.close()

    with open(data_file, 'w') as file:
        jsonstr = json.dump(tasks, file)
except FileNotFoundError:
    tasks = []
    for node in nodes:
        task = {
            "name" : node.name(),
            "rop_path" : node.path(),
            "state" : 0
        }
        
        tasks.append(task)

    with open(data_file, 'x') as file:
        jsonstr = json.dump(tasks, file)