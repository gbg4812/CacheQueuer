## Introduction

CacheQueuer Is a tool to Queue tasks easily and user friendly.

I got the motivation to do this project after countless hours spend trying to automatize tasks inside SideFx Houdini. The first plan was to make a Houdini specific "plugin" to manage the tasks but I realized that the program would be easy to make generic. So I designed the code with flexibility and scalability in mind and i hope that some day it will be may loyal companion whenever i need to automatize a process.

## Index
```dataview
list where file != this.file
```

## Integration

When a task is added, the data is stored in a dict on the `item.data(CustomRoles.TaskData)` and it has to contain at least a **"shell_script"** key.

Then when the render manager wants to render the data it starts a render thread that starts the shell_script passing as first argument the task data.

```bash
#Example shell script
python C:/Users/Documents/Scripts/hou_render.py #Here the TaskData will be inserted as a string
```

The render thread will capture the output of the process that must have the next format:
```json

	{"Progress":5.0, "Range":[1.0, 30.0]}
	
```

Any other format won't be used and will be printed into the console.
Every time a `dict` is readed from the render process output, the `QThread` will fire a signal to update the progress bar.

When the Process ends, it sends a returncode:
- 0 ⇒ Successful
- 1 ⇒ Failed 

## Parms Tab 
The parms for each key in the Task Data `dict` will create a Label to print its value.
Also a progress bar will be prepared to show the progress, of the current render independently of the task selected.


**Task:** 1 call to a render script, it has its own data and script command.
**Task Dir:** It is a group of task that share the same dependent property.


## Delegate Sub Items
Delegate sub items are widgets to build complex `QStyleItemDelegate` subclasses. They act like tools not like objects, their state must be stored in the model because a single `DelegateSubItem` is responsible to paint multiple items.

They have `init()` and `end()` methods that should be called in the beginning and end of each use. They set and return the state respectively.  

### Button subitem
The Button delegate sub item is the base for any button, it can render a icon or/and a background plain color. Each icon/bg_color is associated with a view state. View states are used to paint de button in diferent ways depending on the user interaction. Every time a color or an icon is added to the subitem, it is associated with a state represented as a `enum.IntEnum`. 






