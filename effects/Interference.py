#!/usr/bin/python
import math
# non std modules
import pygame
from pygame import gfxdraw
# own modules
from RgbColorGradient import get_rgb_color_gradient


FPS = 50
DIM = (320, 200)  # initial window size
SIN = [math.sin(math.radians(degree)) for degree in range(0, 360, 1)]
PALETTE = get_rgb_color_gradient((50, 140, 70, 255), (240, 0, 70, 255), 256)


class ColorInterference:
    """ interfering colors """

    def __init__(self, dim, palette=PALETTE, sin=SIN):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.dim = dim
        self.palette = palette
        self.sin = sin
        self.width = dim[0]
        self.height = dim[1]
        self.pixel_surface = pygame.Surface((dim[0] * 2, dim[1] * 2))
        # set some values
        for y in range(self.pixel_surface.get_height()):
            for x in range(self.pixel_surface.get_width()):
                value = 128 + int(127 * sin[y % 360] * sin[x % 360])
                pygame.gfxdraw.pixel(self.pixel_surface, x, y, palette[value])
        self.framecount = 0

    def update(self):
        """ blit on background surface """
        surface = pygame.Surface((self.width, self.height))
        self.framecount += 1
        x = -100 + int(100 * self.sin[(self.framecount + 30) % 360])
        surface.blit(self.pixel_surface, (x, -100), special_flags=pygame.BLEND_MAX)
        y = -100 + int(100 * self.sin[(self.framecount) % 360])
        surface.blit(self.pixel_surface, (-100, y), special_flags=pygame.BLEND_MAX)
        x = -100 + int(100 * self.sin[(self.framecount + 70) % 360])
        y = -100 + int(100 * self.sin[(self.framecount // 2) % 180])
        surface.blit(self.pixel_surface, (x - 100, y - 100), special_flags=pygame.BLEND_MAX)
        return surface


class CircleInterference:
    """ interfering circles """

    def __init__(self, dim, palette=PALETTE, sin=SIN):
        """
        (pygame.Surface) surface - surface to draw on

        :param dim: dimesion of surface to generate in (x, y)
        :param palette: 256 color palette
        """
        self.dim = dim
        self.palette = palette
        self.sin = sin
        self.width = dim[0]
        self.height = dim[1]
        self.pixel_surface = pygame.Surface((dim[0] * 2, dim[1] * 2))
        center = (dim[0], dim[1])  # center of cirle in the middle of surface
        # prepare surface with color circle
        for y in range(self.pixel_surface.get_height()):
            for x in range(self.pixel_surface.get_width()):
                x_dist = x - center[0]
                y_dist = y - center[1]
                radius = int(math.sqrt(x_dist * x_dist + y_dist * y_dist))
                value = 128 + int(127 * sin[10 * radius % 360])
                pygame.gfxdraw.pixel(self.pixel_surface, x, y, palette[value])
        self.framecount = 0

    def update(self):
        """ blit on background surface """
        surface = pygame.Surface((self.width, self.height))
        center = (-self.width // 2, -self.height // 2)  # circle will be in the middle of screen
        wobble_x = 16 + 32 * self.sin[(self.framecount + 90) % 360]
        wobble_y = 16 + 32 * self.sin[self.framecount % 360]
        pos = (center[0] + wobble_x, center[1] - wobble_y)
        surface.blit(self.pixel_surface, pos, special_flags=pygame.BLEND_MAX)
        pos = (center[0] - wobble_x, center[1] + wobble_y)
        surface.blit(self.pixel_surface, pos, special_flags=pygame.BLEND_MAX)
        self.framecount += 1
        return surface


def main():
    try:
        pygame.display.init()  # only initialize display, no other modules
        surface = pygame.display.set_mode(DIM)
        effects = [
            # CircleInterference(DIM)
            ColorInterference(DIM)
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

