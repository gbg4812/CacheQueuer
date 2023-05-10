from __future__ import annotations

class Vec2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def vTranslate(self, offset : Vec2):
        self.x += offset.x
        self.y += offset.y
    
    def length(self):
        return pow(self.x^2 + self.y^2, 0.5)

    def dot(self, other : Vec2):
        return self.x * other.y + self.y * other.x
    
    def __add__(self, other):
        self.x += other
        self.y += other

    def __sub__(self, other):
        self.x -= other
        self.y -= other

    def __str__(self) -> str:
        return "({} ,{} )".format(self.x, self.y)
    
    def __mul__(self, other):
        self.x *= other
        self.y *= other

    def __truediv__(self, other):
        self.x /= other
        self.y /= other
            