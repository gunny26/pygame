#!/usr/bin/python
import math
# non std modules
import pygame
# own modules
from RgbColorGradient import get_rgb_color_gradient

FPS = 60
DIM = (320, 200)  # initial window size
SIN = [math.sin(math.radians(degree)) for degree in range(0, 360, 1)]
PALETTE = get_rgb_color_gradient((50, 140, 70, 255), (240, 0, 70, 255), 256)


class HorizontalRasterBar:
    """ some simple horizontal raster bar """

    def __init__(self, dim: tuple, y_pos: int, bars: int = 5, speed: int = 2, palette: list = PALETTE, sin: list = SIN):
        """
        :param dim: dimensio of surface to draw on
        :param y_pos: central y position
        :param bars: how many bars to draw
        :param speed: speed per frame, 1 euqal one pixel per frame
        :param palette: palette to use 256 colors
        :param sin: pre calculated sins for 360 degrees
        """
        self.dim = dim
        self.y_pos = y_pos
        self.bars = bars
        self.speed = speed
        self.palette = palette
        self.sin = sin
        self.surface = pygame.Surface((dim[0], dim[1]), flags=pygame.SRCALPHA)
        bar_height = 10  # height of individual bar
        self.bar_surface = pygame.Surface((dim[0], bar_height), flags=pygame.SRCALPHA)
        for index, degree in enumerate(range(0, 180, bar_height)):
            color = palette[128 + int(127 * sin[degree])]
            pygame.draw.line(self.bar_surface, color, (0, index), (dim[0], index))
        self.framecount = 0

    def update(self) -> pygame.Surface:
        """ blit bars on surface """
        self.surface.fill((0, 0, 0, 255))
        for index in range(self.bars):
            y_pos = int(self.y_pos + 50 * self.sin[(self.speed * self.framecount + index * 20) % 360])
            self.surface.blit(self.bar_surface, (0, y_pos), special_flags=pygame.BLEND_MAX)
        self.framecount += 1
        return self.surface


class VerticalRasterBar:
    """ some simple vertical raster bar """

    def __init__(self, dim: tuple, x_pos: int, bars: int = 5, speed: int = 2, palette: list = PALETTE, sin: list = SIN):
        """
        :param dim: dimensio of surface to draw on
        :param x_pos: central x position
        :param bars: how many bars to draw
        :param speed: speed per frame, 1 euqal one pixel per frame
        :param palette: palette to use 256 colors
        :param sin: pre calculated sins for 360 degrees
        """
        self.dim = dim
        self.x_pos = x_pos
        self.bars = bars
        self.speed = speed
        self.palette = palette
        self.sin = sin
        self.surface = pygame.Surface((dim[0], dim[1]), flags=pygame.SRCALPHA)
        bar_width = 10  # width of individual bar
        self.bar_surface = pygame.Surface((bar_width, dim[1]), flags=pygame.SRCALPHA)
        for index, degree in enumerate(range(0, 180, bar_width)):
            color = palette[128 + int(127 * sin[degree])]
            pygame.draw.line(self.bar_surface, color, (index, 0), (index, dim[1]))
        self.framecount = 0

    def update(self) -> pygame.Surface:
        """ blit bars on surface """
        self.surface.fill((0, 0, 0, 255))
        for index in range(self.bars):
            x_pos = int(self.x_pos + 50 * self.sin[(self.speed * self.framecount + index * 20) % 360])
            self.surface.blit(self.bar_surface, (x_pos, 0), special_flags=pygame.BLEND_MAX)
        self.framecount += 1
        return self.surface


def main():
    try:
        pygame.display.init()  # only initialize display, no other modules
        surface = pygame.display.set_mode(DIM)
        effects = [
            HorizontalRasterBar(DIM, 150),
            HorizontalRasterBar(DIM, 50, speed=4),
            VerticalRasterBar(DIM, 240),
            VerticalRasterBar(DIM, 80, speed=4),
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
                surface.fill(0)
                for effect in effects:
                    e_surface = effect.update()
                    surface.blit(e_surface, (0, 0), special_flags=pygame.BLEND_ADD)
                    # pygame.transform.scale(e_surface, (surface.get_width(), surface.get_height()), surface)  # blit and scale to display
                pygame.display.flip()
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
