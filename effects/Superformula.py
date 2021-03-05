#!/usr/bin/python
import sys
import math
import random
# non std modules
import pygame

FPS = 50

class Vector:

    def __init__(self, x, y):
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

    def length(self):
        """ return lenght of vector """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Superformula(object):
    """ Draw Superformula Object, most basic form static drawing """

    def __init__(self, surface:pygame.Surface, pos:Vector, size:int, color:tuple, params):
        """
        a particle in 2D space

        :param surface: surface to draw on
        :param pos: position to set particle, center of particle
        :param size: size of particle
        :param color: color of particle
        :param parms: tuple oof four (m, n1, n2, n3)
        """
        self.surface = surface
        self.pos = pos  # initial position
        self.size = size
        self.color = color
        self.params = params
        self.m, self.n1, self.n2, self.n3 = params
        self.a = self.b = 1.0  # fixed to one
        self.framecount = 0
        self._draw()

    def _radius(self, theta):
        """
        calculate radius - unscaled

        :param theta: value in radians
        """
        return pow(pow(abs(math.cos(self.m * theta / 4) / self.a), self.n2) + pow(abs(math.sin(self.m * theta / 4) / self.b), self.n3), -1 / self.n1)

    def _draw(self):
        """
        draw suoperformula based on current parameters
        """
        points = []
        step = math.pi / 180.0  # step by 1 degree
        for degree in range(0, 360):
            radius = self._radius(step * degree)
            x = self.pos.x + math.cos(step * (degree + self.framecount)) * radius * self.size
            y = self.pos.y + math.sin(step * (degree + self.framecount)) * radius * self.size
            points.append((int(x), int(y)))
        pygame.draw.lines(self.surface, self.color, True, points)

    def update(self, params=None):
        """ update every frame """
        if params and self.params != params:  # if something changed
            self.m, self.n1, self.n2, self.n3 = params
        self._draw()
        self.framecount += 1


class SuperformulaAnimation(object):
    """ Draw Superformula Object and vary some parameters on every frame """

    def __init__(self, surface:pygame.Surface, pos:Vector, size:int, color:tuple):
        """
        a particle in 2D space

        :param surface: surface to draw on
        :param pos: position to set particle, center of particle
        :param size: size of particle
        :param color: color of particle
        :param parms: tuple oof four (m, n1, n2, n3)
        """
        self.surface = surface
        self.pos = pos  # initial position
        self.size = size
        self.color = color
        # initial set of values
        self.m, self.n1, self.n2, self.n3 = (3.0, 4.5, 10.0, 10.0)
        self.a = self.b = 1.0  # fixed to one
        self.framecount = 0
        self.params = None
        self._calculate()
        self.sf = Superformula(surface, Vector(320, 240), 100, (255, 255, 255), list(self.params.values()))

    def _calculate(self):
        self.params = {
            "m": (1.1 + math.sin(math.radians(self.framecount))) * 10,
            "n1": (1.1 + math.sin(math.radians(self.framecount * 1.1))) * 3,
            "n2": (1.1 + math.sin(math.radians(self.framecount * 1.2))) * 4,
            "n3": (1.5 + math.sin(math.radians(self.framecount * 1.3))) * 10
        }

    def update(self, params=None):
        """ update every frame """
        self._calculate()
        self.sf.update(list(self.params.values()))
        self.framecount += 1


def main():

    try:
        surface = pygame.display.set_mode((640, 480))
        pygame.init()
        things = (
            SuperformulaAnimation(surface, Vector(320, 240), 100, (255, 255, 255)),
            )
        clock = pygame.time.Clock()
        # mark pause state
        pause = False
        # fill background
        surface.fill((0, 0, 0, 255))
        clicked = None
        while True:
            # limit to FPS
            clock.tick(FPS)
            # Event Handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
                if keyinput[pygame.K_p]:
                    pause = not pause
            # Update Graphics
            dirtyrects = []
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                for thing in things:
                    thing.update()
                #pygame.display.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()

if __name__=='__main__':
    main()

