#!/usr/bin/python
"""Vector Module, something with length and angle"""

import math
from Vec2d import Vec2d


class Vector(object):
    """Vector Class represents length and angle"""

    def __init__(self, length, angle):
        self.length = length
        self.angle = angle

    def __add__(self, other):
        if isinstance(other, Vector):
            # other is Vector object
            x  = math.sin(self.angle) * self.length + math.sin(other.angle) * other.length
            y  = math.cos(self.angle) * self.length + math.cos(other.angle) * other.length
            length = math.hypot(x, y)
            angle = 0.5 * math.pi - math.atan2(y, x)
            return(Vector(length, angle))
        elif hasattr(other, "__getitem__"):
            # other is type sequence
            x  = math.sin(self.angle) * self.length + math.sin(other[1]) * other[0]
            y  = math.cos(self.angle) * self.length + math.cos(other[1]) * other[0]
            length = math.hypot(x, y)
            angle = 0.5 * math.pi - math.atan2(y, x)
            return(Vector(length, angle))
        else:
            # TODO does this make sense, only lenght
            return(Vector(self.length + other, self.angle))
    __radd__ = __add__

    def __iadd__(self, other):
        if isinstance(other, Vector):
            # other is Vector object
            x  = math.sin(self.angle) * self.length + math.sin(other.angle) * other.length
            y  = math.cos(self.angle) * self.length + math.cos(other.angle) * other.length
            self.length = math.hypot(x, y)
            self.angle = 0.5 * math.pi - math.atan2(y, x)
            return(self)
        elif hasattr(other, "__getitem__"):
            # other is type sequence
            x  = math.sin(self.angle) * self.length + math.sin(other[1]) * other[0]
            y  = math.cos(self.angle) * self.length + math.cos(other[1]) * other[0]
            self.length = math.hypot(x, y)
            self.angle = 0.5 * math.pi - math.atan2(y, x)
            return(self)
        else:
            # TODO does this make sense, only lenght
            self.length += other
            return(self)
    __iradd__ = __iadd__

    def __mul__(self, other):
        return(Vector(self.length * other, self.angle))

    def __imul__(self, other):
        self.length *= other
        return(self)

    def bounce(self, tangent=0):
        """reverse direction"""
        self.angle = tangent - self.angle

    def addpos(self, position):
        """add position to current vector and returns new position"""
        x = position.x + math.sin(self.angle) * self.length
        y = position.y - math.cos(self.angle) * self.length
        return(Vec2d(x, y))

    @staticmethod
    def vector_between(pos1, pos2):
        """return vector between two points"""
        dx = (pos1.x - pos2.x)
        dy = (pos1.y - pos2.y)
        dist = math.hypot(dx, dy)
        theta = math.atan2(dy, dx)
        return(Vector(dist, theta))

    @staticmethod
    def distance_between(pos1, pos2):
        """return vector between two points"""
        dx = (pos1.x - pos2.x)
        dy = (pos1.y - pos2.y)
        dist = math.hypot(dx, dy)
        return(dist)

    @staticmethod
    def angle_between(pos1, pos2):
        """return vector between two points"""
        dx = (pos1.x - pos2.x)
        dy = (pos1.y - pos2.y)
        theta = math.atan2(dy, dx)
        return(theta)
