from __future__ import annotations
from enum import IntEnum
import time as t


class Level(IntEnum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    DISABLED = 4


class Logger:
    def __init__(self, name: str, level: Level = Level.DEBUG):
        self.name = name
        self._level = level

    def setLevel(self, level: Level):
        self._level = level

    def log(self, message: str, time=False, level: Level = Level.DEBUG):
        if time:
            print(t.process_time(),end=" ")
        if self._level <= level:
            print(level.name, self.name, message, sep="::")

    def debug(self, message: str, time=False):
        if time:
            print(t.process_time(),end=" ")
        if self._level <= Level.DEBUG:
            print(Level.DEBUG.name, self.name, message, sep="::")

    def info(self, message: str, time=False):
        if time:
            print(t.process_time(),end=" ")
        if self._level <= Level.INFO:
            print(Level.INFO.name, self.name, message, sep="::")

    def warning(self, message: str, time=False):
        if time:
            print(t.process_time(),end=" ")
        if self._level <= Level.WARNING:
            print(Level.WARNING.name, self.name, message, sep="::")

    def error(self, message: str, time=False):
        if time:
            print(t.process_time(),end=" ")
        if self._level <= Level.ERROR:
            print(Level.ERROR.name, self.name, message, sep="::")
