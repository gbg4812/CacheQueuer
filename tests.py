import typing
from PySide2.QtCore import Signal, QObject, QCoreApplication

class Person(QObject):
    speaked = Signal(str)
    def __init__(self, name, age):
        super(Person, self).__init__()
        self.name = name
        self.age = age
    
    def speak(words: str): 
        Person.speaked.emit(words)



class Manager(QObject):
    person_speaked = Signal(str)
    def startConversation():
        person = Person("guillem", 18)
        person.speaked.connect(Manager.personSpeaked)
        Person.speak("hello")
        
    def personSpeaked(self, words: str):
        self.person_speaked.emit(words)
   
   
def printWords(words: str):
    print(words)

    

app = QCoreApplication()
manager = Manager()
manager.person_speaked.connect(printWords) 
Manager.startConversation()
app.exec_()

