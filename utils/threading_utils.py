import threading
from typing import Callable, Iterable
class ThreadingUtils():
    def startThread(name: str, func: Callable, args: Iterable, check_if_isrunning: bool) -> bool:
        if check_if_isrunning:
            if ThreadingUtils.threadIsRuning(name):
                return False
        try:
            thread = threading.Thread(target=func, name=name, args=args)
            thread.start()
        except:
            return False

    def threadIsRuning(name: str) -> bool:
        for thread in threading.enumerate():
            if thread.name == name:
                return True
        return False
    