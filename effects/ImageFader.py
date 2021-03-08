#!/usr/bin/python
import math
# non std modules
import pygame
from pygame import gfxdraw
# own modules
from RgbColorGradient import get_rgb_color_gradient

FPS = 60
DIM = (320, 200)  # initial window size
SIN = [math.sin(math.radians(degree)) for degree in range(0, 360, 1)]
PALETTE = get_rgb_color_gradient((50, 140, 70, 255), (240, 0, 70, 255), 256)


class ImageFader:
    """ interfering colors """

    def __init__(self, dim, palette=PALETTE, sin=SIN):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.dim = dim
        self.palette = palette
        self.sin = sin
        self.surface = pygame.image.load(open("images/172133.png", "rb")).convert()
        self.p_array = pygame.PixelArray(self.surface)
        self.p_array.transpose()
        self.p_array.close()
        self.framecount = 0

    def update(self):
        """ blit on background surface """
        # surface = pygame.Surface(self.dim)
        # surface.blit(self.p_array, (0, 0))
        #surface.blit(self.pixel_surface, (x - 100, y - 100), special_flags=pygame.BLEND_MAX)
        return self.surface


def main():
    try:
        pygame.display.init()  # only initialize display, no other modules
        surface = pygame.display.set_mode(DIM)
        effects = [
            ImageFader(DIM)
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

