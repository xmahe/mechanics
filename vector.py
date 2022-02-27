from math import sin, cos

class Vector:
    class TooShort(Exception):
        pass
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def scale(self, factor):
        return Vector(self.x*factor, self.y*factor)
    def length(self):
        return (self.x**2 + self.y**2)**0.5
    def normalise(self):
        l = self.length()
        if l < 1e-5:
            raise Vector.TooShort()
        return self.scale(1/l)
    def __str__(self):
        return f"({self.x:.3f}, {self.y:.3f})"
    def dot(self, other):
        return self.x*other.x + self.y*other.y
    def cross(self, other):
        return self.x*other.y - self.y*other.x
    def rotate90CCW(self):
        return Vector(-self.y, self.x)
    def rotate90CW(self):
        return Vector(self.y, -self.x)
    def rotate(self, Θ):
        c = cos(Θ)
        s = sin(Θ)
        return Vector(self.x*c - self.y*s, self.x*s + self.y*c)
    def as_tuple(self):
        return (self.x, self.y)
