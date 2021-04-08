#!/usr/bin/python
#
import pygame
import random


FPS = 50
DIM = (320, 200)


class JuliaFractal(object):
    """ Classical Julia Set Fractal, really slow on python, so have some patience """

    def __init__(self, dim, frames=500):
        """
        :param dim: dimension of surface to draw on
        :param frames: after this number of frames the image will be redrawn
        """
        self.surface = pygame.Surface(dim)
        self.frames = frames
        # set some values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.array2d = pygame.surfarray.array2d(self.surface)
        self.initialize()
        self.framecount = 0

    def initialize(self, xa=-2.0, xb=2.0, ya=-1.5, yb=1.5, maxiter=255):
        """
        Base code was from http://code.activestate.com/recipes/577120-julia-fractals/
        """
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
        factor_y = (yb - ya) / (self.height - 1)
        factor_x = (xb - xa) / (self.width - 1)
        for y in range(self.height):
            zy = y * factor_y + ya
            for x in range(self.width):
                zx = x * factor_x + xa
                z = zx + zy * 1j
                for i in range(maxiter):
                    if abs(z) > 2.0:
                        break
                    z = z * z + c
                self.array2d[x][y] = pygame.Color(i % 8 * 32, i % 16 * 16, i % 32 * 8)

    def update(self):
        """blit pixelarray to surface"""
        pygame.surfarray.blit_array(self.surface, self.array2d)
        if (self.framecount % self.frames) == 0:
            self.initialize()
        self.framecount += 1
        return self.surface


def main():
    try:
        surface = pygame.display.set_mode(DIM)
        pygame.init()
        effects = [
            JuliaFractal(DIM)
        ]
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
                surface.fill(0)
                for effect in effects:
                    surface.blit(effect.update(), (0, 0))
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()
