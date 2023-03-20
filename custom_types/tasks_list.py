#class that controls the tasks list
class TaskList():
    def __init__(self):
        self.tasks = []
        self.ids = []
        self.maxId = 0
        
    def get(self, index) -> dict:
        return self.tasks[index]
    
    def getFromID(self, id) -> dict:
        return self.tasks[self.ids.index(id)]
    
    def rmTask(self, id) -> None:
        self.tasks
        del self.tasks[self.ids.index(id)]
        self.ids.remove(id)
    
    def addTask(self, task) -> int:
        self.tasks.append(task)
        self.ids.append(self.maxId)
        self.maxId += 1
        
        return self.maxId - 1
            
    def setTaskValue(self, id, key, value):
        self.tasks[self.ids.index(id)][key] = value
        
    def getTaskValue(self, id, key):
        index = self.ids.index(id)
        task : dict = self.tasks[index]
        return task.get(key)
     