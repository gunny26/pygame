#!/usr/bin/python
#
import random
import math
# non std modules
import pygame
from pygame import gfxdraw
# own modules
from RgbColorGradient import get_rgb_color_gradient

FPS = 50
DIM = (640, 480)
SINS = [math.sin(math.radians(degree)) for degree in range(360)]
PALETTE = get_rgb_color_gradient((200, 180, 130, 10), (128, 90, 130, 10), 256)
PALETTE_GLOW = get_rgb_color_gradient((0, 0, 100, 255), (255, 255, 0, 100), 256)


def draw_path(surface, points, palette, skipzero=True):
    """
    draw some fading line
    """
    start = points[0]
    l_palette = len(palette)
    for index, point in enumerate(points[1:]):
        if skipzero and point == pygame.Vector2(0, 0):
            continue
        pygame.draw.line(surface, palette[index % l_palette], start, point)
        start = point


class Fourier:
    """ Fourier Animation, left side showing some oscillating vector, right side timelines of x,y,radius,phi """

    def __init__(self, dim: tuple, parts=1):
        """
        :param surface: surface to draw on
        :param center: center of calculations in (x, y)
        :param amplitude: maximum amplitude of single part
        :param pats: number of parts to generate
        """
        self.dim = dim
        self.parts = parts
        self.surface = pygame.Surface(dim)
        # set some values
        self.width, self.height = dim
        # create some random set of amplitudes and frequencies
        self.parts = self._initialize_parts(parts)
        # maximum radius and center of oscillator
        self.radius = self.height // 2
        self.center = pygame.Vector2(self.width // 4, self.height // 2)
        # timeserie stuff
        self.timeseries_x = self.width // 2
        self.timeseries = [0.0] * 512  # storing the timeseries data
        # path of points, some sort of afterglow
        self.path = [self.center] * 256  # storing latest points in (x, y)
        # standard framecounter
        self.framecount = 0

    def _initialize_parts(self, parts):
        """
        initialize vectors
        """
        # create some random set of amplitudes and frequencies
        _parts = []
        length = 1.0 / 2  # maximum length by 2 for the first segment
        for i in range(parts):
            # random length of vector would be aso an alternative
            vector = pygame.Vector2(length, 0.0)  # vector starting position
            velocity = 16 * (random.random() - 0.5)  # angle velocity
            _parts.append((vector, velocity))
            length /= 2
        # if sum of all length is above 1, the vectors must be scaled to fit on screen
        total_length = sum([vector.length() for vector, _  in _parts])  # total length
        factor = 1 / total_length
        # total_length will be scaled to 1, and any vector in it will be downscaled
        _parts = [(vector * factor, velocity) for vector, velocity in _parts]
        return _parts

    def update(self):
        """blit pixelarray to surface"""
        self.surface.fill(0)
        center = self.center
        radius = self.radius
        for vector, velocity in self.parts:
            target = center + vector.rotate(self.framecount * velocity) * radius
            pygame.draw.line(self.surface, (255, 255, 255, 255), center, target)
            center = target
        self.timeseries.append(center)  # add last y
        self.timeseries.pop(0)  # pop first entry
        self.path.append(center)
        self.path.pop(0)
        graph_y =  self.height // 12
        # drawing timeseries for imaginary part
        points = [(self.timeseries_x + index, graph_y + vector.y // 4) for index, vector in enumerate(self.timeseries[::2]) if vector]
        if len(points) > 2:
            pygame.draw.lines(self.surface, (255, 0, 0, 255), False, points)
        # drawing timeseries for real part
        points = [(self.timeseries_x + index, 3 * graph_y + vector.x // 4) for index, vector in enumerate(self.timeseries[::2]) if vector]
        if len(points) > 2:
            pygame.draw.lines(self.surface, (0, 255, 0, 255), False, points)
        # drawing timeseries for polar radius
        points = [(self.timeseries_x + index, 6 * graph_y + vector.as_polar()[0] // 4) for index, vector in enumerate(self.timeseries[::2]) if vector]
        if len(points) > 2:
            pygame.draw.lines(self.surface, (0, 150, 150, 255), False, points)
        # drawing timeseries for phi angle
        points = [(self.timeseries_x + index, 8 * graph_y + vector.as_polar()[1] // 4) for index, vector in enumerate(self.timeseries[::2]) if vector]
        if len(points) > 2:
            pygame.draw.lines(self.surface, (150, 150, 0, 255), False, points)
        # draw path of circle
        draw_path(self.surface, self.path[1:], PALETTE_GLOW)
        # pygame.draw.lines(self.surface, (0, 255, 0, 100), False, self.path)
        self.framecount += 1
        return self.surface


def main():
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        effects = [
            Fourier(DIM, 10),
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
            if pause is not True:
                surface.fill((0, 0, 0))
                for effect in effects:
                    surface.blit(effect.update(), (0, 0))
                pygame.display.flip()
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()

