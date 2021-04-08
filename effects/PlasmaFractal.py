#!/usr/bin/python
#
import random
import math
# non std modules
import pygame


FPS = 50
DIM = (320, 200)


class PlasmaFractal(object):
    """ Plasma Generator """

    def __init__(self, dim: tuple):
        """
        :param dim: dimension of surface
        """
        self.surface = pygame.Surface(dim)
        # set some values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.roughness = random.randint(2, 5)
        self.data = [[0 for y in range(self.height)] for x in range(self.width)]
        self.initialize()

    def adjust(self, xa: float, ya: float, x: float, y: float, xb: float, yb: float):
        if (self.data[x][y] == 0):
            d = math.fabs(xa - xb) + math.fabs(ya - yb)
            v = (self.data[xa][ya] + self.data[xb][yb]) / 2.0 + \
                (random.random() - 0.5) * d * self.roughness
            c = int(math.fabs(v) % 256)
            self.data[x][y] = c

    def subdivide(self, x1: float, y1: float, x2: float, y2: float):
        if (not ((x2 - x1 < 2.0) and (y2 - y1 < 2.0))):
            x = int((x1 + x2) / 2.0)
            y = int((y1 + y2) / 2.0)
            self.adjust(x1, y1, x, y1, x2, y1)
            self.adjust(x2, y1, x2, y, x2, y2)
            self.adjust(x1, y2, x, y2, x2, y2)
            self.adjust(x1, y1, x1, y, x1, y2)
            if(self.data[x][y] == 0):
                v = int(
                    (self.data[x1][y1] + self.data[x2][y1]) + \
                    self.data[x2][y2] + self.data[x1][y2]
                ) / 4.0
                self.data[x][y] = v
            self.subdivide(x1, y1, x, y)
            self.subdivide(x, y1, x2, y)
            self.subdivide(x, y, x2, y2)
            self.subdivide(x1, y, x, y2)

    def initialize(self):
        """
        http://code.activestate.com/recipes/577113/ (r1)
        plasma.py
        plasma fractal
        FB - 201003147
        """
        with pygame.PixelArray(self.surface) as p_array:
            self.data[0][0] = random.randint(0, 255)
            self.data[self.width - 1][0] = random.randint(0, 255)
            self.data[self.width - 1][self.height - 1] = random.randint(0, 255)
            self.data[0][self.height - 1] = random.randint(0, 255)
            self.subdivide(0, 0, self.width - 1, self.height - 1)
            for y in range(self.height):
                for x in range(self.width):
                    p_array[x, y] = pygame.Color(0, int(self.data[x][y]), 100)

    def update(self) -> pygame.Surface:
        """blit pixelarray to surface"""
        return self.surface


def test():
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        thing = PlasmaFractal(DIM)
        clock = pygame.time.Clock()
        pause = False
        while True:
            clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
                    return
            if pause is not True:
                surface.fill((0, 0, 0))
                surface.blit(thing.update(), (0, 0))
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    test()
