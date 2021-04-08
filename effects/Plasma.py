#!/usr/bin/python
#
import random
import math
# non std modules
import pygame
# own modules
from RgbColorGradient import get_rgb_color_gradient


FPS = 50
DIM = (320, 200)
SINS = [math.sin(math.radians(degree)) for degree in range(360)]
PALETTE = get_rgb_color_gradient((255, 0, 128), (128, 255, 32), 256)


class Plasma:
    """Plasma Generator"""

    def __init__(self, dim):
        """
        :param dim: dimension of surface to draw on
        """
        self.surface = pygame.Surface(dim)
        # set some values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        # factor will between 0.0 and 2.0 depending on framecount
        self.framecount = 0

    def update(self):
        """blit pixelarray to surface"""
        factor = 1.0 + math.sin(math.radians(self.framecount))
        width = self.width
        #colors = self.colors
        sins = SINS
        f_sin = SINS[self.framecount % 360]
        p_array = pygame.PixelArray(self.surface)
        for y in range(self.height):
            y_sin = sins[(y + self.framecount) % 360]
            for x in range(width):
                x_sin = sins[(x - self.framecount) * y % 360]
                value = 127 + int(127 * (y_sin * x_sin * f_sin))
                p_array[x, y] = PALETTE[value]
        p_array.close()
        self.framecount += 1
        return self.surface


def main():
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        effects = [
            Plasma(DIM)
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
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()

