#!/usr/bin/python
import math
import random
# non std modules
import pygame
import noise
# own modules
from RgbColorGradient import get_rgb_color_gradient

FPS = 60
DIM = (320, 200)  # initial window size
SIN = [math.sin(math.radians(degree)) for degree in range(0, 360, 1)]
PALETTE = get_rgb_color_gradient((50, 140, 70, 255), (240, 0, 70, 255), 256)


class Fluid:
    """ interfering colors """

    def __init__(self, dim: tuple, palette: list=PALETTE):
        """
        (pygame.Surface) surface - surface to draw on
        :param dim: dimension of output surface in (x, y)
        :param middle: complex number to zoom in
        :param magnify: factor to zoom in every frame
        :param maxiter: maximum interation of mandelbrot algorithm
        :param palette: color palette to use
        """
        self.dim = dim
        self.palette = palette
        self.width = dim[0]
        self.height = dim[1]
        self.surface = pygame.Surface(dim)
        print(self.surface)
        self.data = []
        self.octaves = 4
        for index in range(dim[0] * dim[1]):
            x = index % self.width
            y = index // self.width
            freq = 16.0 / self.octaves
            noise1 = noise.pnoise1(index / freq, octaves=self.octaves)
            noise2 = noise.snoise2(x / freq, y / freq, octaves=self.octaves)
            noise3 = noise.snoise2(x / freq, y / freq, octaves=self.octaves)
            self.data.append([
                noise1,  # random density
                pygame.Vector2(noise2, noise3),  # random velocity vector
            ])
        self.framecount = 0

    def update(self) -> pygame.Surface:
        """
        blit on background surface

        thats a clean pythonic mandelbrot set algorithm
        readable but not fast

        probably not very useful for effects
        """
        p_array = pygame.PixelArray(self.surface)
        width = self.width
        for index, entry in enumerate(self.data):
            x = index % width
            y = index // width
            p_array[x, y] = PALETTE[int(255 * entry[0])]  # render density
        p_array.close()
        self.framecount += 1
        return self.surface


def main():
    try:
        pygame.display.init()  # only initialize display, no other modules
        surface = pygame.display.set_mode(DIM)
        effects = [
            Fluid(DIM)
        ]
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
                if keyinput[pygame.K_f]:  # go to FULLSCREEN
                    pygame.display.quit()
                    pygame.display.init()
                    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            if pause is not True:
                surface.fill((0, 0, 0))
                for background in effects:
                    b_surface = background.update()
                    pygame.transform.scale(b_surface, (surface.get_width(), surface.get_height()), surface)  # blit and scale to display
                pygame.display.flip()
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()

