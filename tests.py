class Object:
    def __init__(self, name):
        self.name = name

    def Print(self) -> None:
        print("".format(self.name))



class Entity():
    def __init__(self):
        self.objects = []
    
    def addObject(self, object: Object):
        self.objects.append(object)
        
    def printObjectsInfo(self):
        for obj in self.objects:
            obj.Print()

    def setObjectName(self, index, name: str):
        self.objects[index].name = name
        
        
e1 = Entity()
ob1 = Object("Guillem")
ob2 = Object("Anna")
e1.addObject(ob1)
e1.addObject(ob2)

e1.setObjectName(0, "Isaac")
ob1.Print()
input("...")

