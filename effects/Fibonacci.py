#!/usr/bin/python
#
import random
import math
import collections
# non std modules
import pygame
from pygame import gfxdraw
# own modules
from RgbColorGradient import get_rgb_color_gradient


def get_fibonacci(a: int = 0, b: int = 1):
    """
    fibonacci number generator
    Fn = Fn-1 + Fn-2
    https://en.wikipedia.org/wiki/Fibonacci_number
    """
    values = [a, b]
    def inner():
        result = values[0] + values[1]
        values[0] = values[1]
        values[1] = result
        return result
    return inner


class FibonacciSpiral:
    """ draw fibonacci spiral """

    def __init__(self, dim):
        """
        (pygame.Surface) surface - surface to draw on
        :param surface: surface to draw on
        """
        self.surface = pygame.Surface(dim)
        # set some values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        # start in center of surface
        self.center = (self.width // 2, self.height // 2)
        self.fibonacci = get_fibonacci()
        self.framecount = 0
        self.initialize()

    def initialize(self):
        """ draw spiral """
        pos = self.center
        color = (255, 255, 255)
        angles = collections.deque([0, math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi])
        for i in range(10):
            radius = self.fibonacci()
            target = (self.center[0] + radius * math.cos(angles[0]), self.center[1] + radius * math.sin(angles[0]))
            pygame.gfxdraw.pixel(self.surface, int(target[0]), int(target[1]), (255, 255, 255))
            pygame.draw.line(self.surface, color, pos, target)
            pos = target
            angles.rotate()

    def update(self):
        return self.surface




def main():
    try:
        fps = 50
        width = 320
        height = 200
        pygame.init()
        surface = pygame.display.set_mode((width, height))
        backgrounds = [
            FibonacciSpiral((width, height))
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
                for background in backgrounds:
                    surface.blit(background.update(), (0,0))
                pygame.display.flip()
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()

