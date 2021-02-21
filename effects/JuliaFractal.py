#!/usr/bin/python
#

import sys
import pygame
import random


class JuliaFractal(object):
    """Classical Julia Set Fractal, realy slow on python, so have some patience"""

    def __init__(self, surface):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.surface = surface
        # set some values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.array2d = pygame.surfarray.array2d(self.surface)
        self.initialize()

    def initialize(self, xa=-2.0, xb=2.0, ya=-1.5, yb=1.5, maxiter=255):
        """Base code was from http://code.activestate.com/recipes/577120-julia-fractals/"""
        # find a good Julia set point using the Mandelbrot set
        while True:
            cx = random.random() * (xb - xa) + xa
            cy = random.random() * (yb - ya) + ya
            c = cx + cy * 1j
            z = c
            for i in range(maxiter):
                if abs(z) > 2.0:
                    break
                z = z * z + c
            if i > 10 and i < 100:
                break
        # draw the Julia set
        for y in range(self.height):
            zy = y * (yb - ya) / (self.height - 1) + ya
            for x in range(self.width):
                zx = x * (xb - xa) / (self.width - 1) + xa
                z = zx + zy * 1j
                for i in range(maxiter):
                    if abs(z) > 2.0:
                        break
                    z = z * z + c
                self.array2d[x][y] = pygame.Color(i % 8 * 32, i % 16 * 16, i % 32 * 8)

    def update(self):
        """blit pixelarray to surface"""
        pygame.surfarray.blit_array(self.surface, self.array2d)


def main():
    try:
        fps = 1
        surface = pygame.display.set_mode((320, 200))
        pygame.init()
        effects = [
            JuliaFractal(surface)
        ]
        clock = pygame.time.Clock()
        pause = False
        while True:
            clock.tick(fps)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit(1)
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                for effect in effects:
                    effect.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()
