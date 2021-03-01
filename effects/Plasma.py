#!/usr/bin/python
#
import random
import math
# non std modules
import pygame
from pygame import gfxdraw
# own modules
from RgbColorGradient import get_rgb_color_gradient

class Plasma:
    """Plasma Generator"""

    def __init__(self, surface):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.surface = surface
        # set some values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        # self.array2d = pygame.surfarray.array2d(self.surface)
        # factor will between 0.0 and 2.0 depending on framecount
        self.framecount = 0
        self.sins = [math.sin(math.radians(degree)) for degree in range(360)]
        self.colors = get_rgb_color_gradient((255, 0, 128), (128, 255, 32), 256)

    def update(self):
        """blit pixelarray to surface"""
        factor = 1.0 + math.sin(math.radians(self.framecount))
        width = self.width
        colors = self.colors
        sins = self.sins
        f_sin = sins[self.framecount % 360]
        for y in range(self.height):
            y_sin = sins[(y + self.framecount) % 360]
            for x in range(width):
                x_sin = sins[(x - self.framecount) * y % 360]
                value = 127 + int(127 * (y_sin * x_sin * f_sin))
                pygame.gfxdraw.pixel(self.surface, x, y, colors[value])
        self.framecount += 1


def main():
    try:
        fps = 50
        pygame.init()
        surface = pygame.display.set_mode((320, 200))
        effects = [
            Plasma(surface)
        ]
        clock = pygame.time.Clock()
        pause = False
        while True:
            clock.tick(fps)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
            if pause is not True:
                surface.fill((0, 0, 0))
                for effect in effects:
                    effect.update()
                pygame.display.flip()
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()

