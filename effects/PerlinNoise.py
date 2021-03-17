#!/usr/bin/python
#
import sys
import random
import math
# non std modules
import pygame


FPS = 50
DIM = (320, 200)

class PerlinNoise(object):
    """ Perlin Noise generated 2d surface """

    def __init__(self, dim):
        """
        Basic python Perlin Noise surface generator

        :param dim: dimension of surface to produce
        """
        self.surface = pygame.Surface(dim)
        # set some values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.initialize()

    def initialize(self):
        """
        generate surface

        http://code.activestate.com/recipes/578470/ (r2)

        Perlin Noise Generator
        http://en.wikipedia.org/wiki/Perlin_noise
        http://en.wikipedia.org/wiki/Bilinear_interpolation
        FB36 - 20130222
        """
        octaves = int(math.log(max(self.width, self.height), 2.0))
        imgAr = [[0.0 for i in range(self.width)] for j in range(self.height)]  # image array
        persistence = random.random()
        totAmp = 0.0
        # how many layers
        for k in range(octaves):
            freq = 2 ** k
            amp = persistence ** k
            totAmp += amp
            # create an image from n by m grid of random numbers (w/ amplitude)
            # using Bilinear Interpolation
            n = freq + 1 # grid size
            m = freq + 1 # grid size
            ar = [[random.random() * amp for i in range(n)] for j in range(m)]
            nx = self.width / (n - 1.0)
            ny = self.height / (m - 1.0)
            nxny = nx * ny
            for ky in range(self.height):
                j = int(ky / ny)
                for kx in range(self.width):
                    i = int(kx / nx)
                    dx0 = kx - i * nx
                    dx1 = nx - dx0
                    dy0 = ky - j * ny
                    dy1 = ny - dy0
                    z = ar[j][i] * dx1 * dy1
                    z += ar[j][i + 1] * dx0 * dy1
                    z += ar[j + 1][i] * dx1 * dy0
                    z += ar[j + 1][i + 1] * dx0 * dy0
                    z /= nxny
                    imgAr[ky][kx] += z # add layers
        # and put result to surface
        p_array = pygame.PixelArray(self.surface)
        for ky in range(self.height):
            for kx in range(self.width):
                    c = int(imgAr[ky][kx] / totAmp * 255)
                    p_array[kx, ky] = pygame.Color(c, c, c, 255) # add image layers together
        p_array.close()

    def update(self):
        """ return surface """
        return self.surface


def main():
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        thing = PerlinNoise(DIM)
        clock = pygame.time.Clock()
        pause = False
        while True:
            clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                surface.blit(thing.update(), (0, 0))
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()

