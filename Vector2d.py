#!/usr/bin/python

class Vector2d(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        print type(other)
        if type(other) == Vector2d:
            return(self.x * other.x, self.y * other.y)
        elif type(other) in(int, float):
            return(self.x * other, self.y * other)

    def __floordiv__(self, other):
        pass

    def __mod__(self, other):
        pass

    def __divmod__(self, other):
        pass

    def __pow__(self, other, modulo=None):
        pass

    def __lshift__(self, other):
        pass

    def __rshift__(self, other):
        pass

    def __and__(self, other):
        pass

    def __xor__(self, other):
        pass

    def __or__(self, other):
        pass

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return(self)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return(self)

    def __imul__(self, other):
        self.x *= other.x
        self.y *= other.y
        return(self)

    def __str__(self):
        return("(%s, %s)" % (self.x, self.y))

    def __repr__(self):
        return("Vector2d(%s, %s)" % (self.x, self.y))

if __name__ == "__main__":
    v1 = Vector2d(100, 100)
    print v1
    v2 = Vector2d(10, 10)
    print v2
    c = v1 + v2
    assert c == (110, 110)
    print c
    c = v1 - v2
    assert c == (90, 90)
    print c
    c = v1 * v2
    assert c == (1000, 1000)
    print c
    c = v1 * 2
    assert c == (200, 200)
    print c
    v1 += v2
    c = v1
    print v1
    assert c == (110, 110)
    
