#!/usr/bin/python
#
import random
import math
import collections
# non std modules
import pygame
#from pygame import gfxdraw
# own modules
from RgbColorGradient import get_rgb_color_gradient


def get_fibonacci(a: int = 0, b: int = 1):
    """
    fibonacci number generator
    Fn = Fn-1 + Fn-2
    https://en.wikipedia.org/wiki/Fibonacci_number
    """
    values = [a, b]
    result = 0
    def inner():
        nonlocal result
        if not result:
            result = 1
            return result
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
        self.p_array = pygame.PixelArray(self.surface)
        self.p_array[0, 0] = (255, 255, 255)
        print(self.p_array.shape)
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
        pos = self.center  # starting point
        color = (255, 255, 255)
        # pygame.gfxdraw.pixel(self.surface, pos[0], pos[1], (255, 255, 255))
        self.p_array[pos[0], pos[1]] = (255, 255, 255)
        angles = collections.deque([1, 1, -1, 1, -1, -1, 1, -1])
        for i in range(7):
            radius = self.fibonacci() * 10
            diff = (int(radius * angles[0]), int(radius * angles[1]))
            target = (pos[0] + diff[0], pos[1] + diff[1])
            pygame.draw.rect(self.surface, color, pos + diff, 1)
            # pygame.gfxdraw.pixel(self.surface, int(target[0]), int(target[1]), (255, 0, 0))
            # pygame.draw.line(self.surface, color, pos, target, 1)
            # pygame.draw.arc(self.surface, color, pos + (radius, radius), angles[0], angles[1])
            print("-" * 40)
            print(f"position : {pos}")
            print(f"radius   : {radius}")
            print(f"angles   : {angles[0]}, {angles[1]}")
            print(f"target   : {target[0]}, {target[1]}")
            print("-" * 40)
            if 0 < target[0] < self.surface.get_width() - 1 and 0 < target[1] < self.surface.get_height() - 1:
                self.p_array[target[0], target[1]] = (255, 0, 0)
            pos = target
            angles.rotate(-2)
        self.p_array.close()

    def update(self):
        return self.surface




def main():
    try:
        fps = 10
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

