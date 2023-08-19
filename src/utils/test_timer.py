import time


class TestTimer:
    def __init__(self, name: str):
        self.startT = time.time()
        self.name = name
    
    def __del__(self):
        duration = time.time() - self.startT

        print("TIMER::{} DURATION -> {} s".format(self.name.capitalize(), duration))