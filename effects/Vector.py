#!/usr/bin/python
import math


class Vector:
    """ 2D Vector Class """

    def __init__(self, x: float, y: float):
        """
        2 Column vector in this form

        | x | type <float>
        | y | type <float>
        """
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        return Vector(self.x * other.x, self.y * other.y)

    def __imul__(self, other):
        self.x *= other.x
        self.y *= other.y
        return self

    def __div__(self, other):
        return Vector(self.x / other.x, self.y / other.y)

    def __idiv__(self, other):
        self.x /= other.x
        self.y /= other.y
        return self

    def __getitem__(self, key):
        """ to convert in list """
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError(f"Invalid subscript {key} to Vector")

    def distance(self, other):
        """ return distance between self and other """
        return Vector(other.x - self.x, other.y - self.x)

    def length(self) -> float:
        """ return lenght of vector """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y

    def normalize(self):
        """ normalize Vector to length == 1 """
        length = self.length()
        if length:
            return Vector(self.x / length, self.y / length)
        else:
            return Vector(self.x, self.y)  # TODO: is this corrects??

    def inormalize(self):
        """ normalize Vector inplace to length == 1 """
        length = self.length()
        self.x /= length
        self.y /= length
        return self

    def theta(self):
        """
        return angle theta in radians

        tan theta = y/x fpr x != 0
        theta = arctan (y/x) for x != 0
        """
        return math.atan2(self.y, self.x)

    def to_point(self):
        """
        return tuple of integers (int(x), int(y))
        """
        return (int(self.y), int(self.x))

    def __str__(self):
        return f"({self.x}, {self.y})"


if __name__ == "__main__":
    v1 = Vector(1, 0)
    v2 = Vector(0, 1)  # perpendicular angle
    print(f"dot product of v2 on v1: {v2.dot(v1)}")
    print(f"dot product of v1 on v2: {v2.dot(v1)}")
    v1 = Vector(1, 0)
    v2 = Vector(0.5, 0.707106781)  # 45 degree angle
    print(f"dot product of v2 on v1: {v2.dot(v1)}")
    print(f"dot product of v1 on v2: {v2.dot(v1)}")
    v1 = Vector(0.5, 0.707106781)  # 45 degree angle
    v2 = Vector(0.5, 0.707106781)  # 45 degree angle
    print(f"dot product of v2 on v1: {v2.dot(v1)}")
    print(f"dot product of v1 on v2: {v2.dot(v1)}")
    print(f"length of v1, v2       : {v1.length()}")
    print(f"theta of v1            : {v1.theta()} radians")
    print(f"theta of v2            : {v2.theta()} radians")

