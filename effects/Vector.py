#!/usr/bin/python
import math


class Vector:
    """ 2D Vector Class """

    def __init__(self, x: float, y: float):
        """
        2 Column vector in form

        | x |
        | y |
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

    def distance(self, other):
        """ return distance between self and other """
        return Vector(other.x - self.x, other.y - self.x)

    def length(self) -> float:
        """ return lenght of vector """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


