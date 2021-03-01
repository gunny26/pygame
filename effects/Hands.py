#!/usr/bin/python
#
import random
import math
# non std modules
import pygame
from pygame import gfxdraw
# own modules
from RgbColorGradient import get_rgb_color_gradient

class Hands:
    """Plasma Generator"""

    def __init__(self, surface: pygame.Surface, center: tuple, amplitude: int = 256, num_parts: int = 16):
        """
        :param surface: surface to draw on
        :param center: center of calculations in (x, y)
        :param amplitude: maximum amplitude of single part
        :param pats: number of parts to generate
        """
        self.surface = surface
        self.center = center
        # set some values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        # create some random set of amplitudes and frequencies
        self.parts = []
        for i in range(num_parts):
            # random length of vector, random angle velocity, and actual
            # angle position
            self.parts.append((random.random(), random.random() - 0.5, amplitude // 2))
            amplitdue = amplitude // 2 + 5
        self.sins = [math.sin(math.radians(degree)) for degree in range(360)]
        self.colors = get_rgb_color_gradient((200, 180, 130, 10), (128, 90, 130, 10), 256)
        self.points = pygame.Surface((self.width, self.height))  # surface to draw endpoints on
        self.last_target = None
        self.framecount = 0

    def update(self):
        """blit pixelarray to surface"""
        self.surface.blit(self.points, (0, 0))  # blit background
        start = self.center
        first = True  # skipping first part in drawing
        for index, part in enumerate(self.parts):
            length, angle, amplitude = part
            target = (
                int(start[0] + amplitude * length * math.sin(math.radians(self.framecount * angle))),
                int(start[1] + amplitude * length * math.cos(math.radians(self.framecount * angle)))
            )
            if not first:  # skipping first part, beacuase this will always be a circle
                pygame.draw.line(self.surface, (100, 100, 100), start, target)
                pygame.gfxdraw.pixel(self.points, target[0], target[1], self.colors[self.framecount % 256])
            else:
                first = False
            start = target
        # draw only point or line from point to point
        pygame.gfxdraw.pixel(self.points, target[0], target[1], self.colors[self.framecount % 256])
        #if not self.last_target:
        #    self.last_target = target
        #pygame.draw.line(self.points, self.colors[self.framecount % 256], self.last_target, target)
        #self.last_target = target  # new position
        self.framecount += 1


class Hands2:
    """Plasma Generator"""

    def __init__(self, surface: pygame.Surface, center: tuple, amplitude: int = 256, num_parts: int = 16):
        """
        :param surface: surface to draw on
        :param center: center of calculations in (x, y)
        :param amplitude: maximum amplitude of single part
        :param pats: number of parts to generate
        """
        self.surface = surface
        self.center = center
        # set some values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        # create some random set of amplitudes and frequencies
        self.parts = []
        for i in range(num_parts):
            # random length of vector, random angle velocity, and actual
            # angle position
            self.parts.append((random.random(), random.random() - 0.5, amplitude // 2))
            amplitdue = amplitude // 2 + 5
        self.sins = [math.sin(math.radians(degree)) for degree in range(360)]
        self.colors = get_rgb_color_gradient((200, 180, 130, 10), (128, 90, 130, 10), 256)
        self.points = pygame.Surface((self.width, self.height))  # surface to draw endpoints on
        self.last_target = None
        self.framecount = 0

    def update(self):
        """blit pixelarray to surface"""
        self.surface.blit(self.points, (0, 0))  # blit background
        start = self.center
        first = True  # skipping first part in drawing
        for index, part in enumerate(self.parts):
            length, angle, amplitude = part
            target = (
                int(start[0] + amplitude * length * math.sin(math.radians(self.framecount * angle))),
                int(start[1] + amplitude * length * math.cos(math.radians(self.framecount * angle)))
            )
            if not first:  # skipping first part, beacuase this will always be a circle
                pygame.draw.line(self.surface, (100, 100, 100), start, target)
                pygame.gfxdraw.pixel(self.points, target[0], target[1], self.colors[self.framecount % 256])
            else:
                first = False
            start = target
        # draw only point or line from point to point
        pygame.gfxdraw.pixel(self.points, target[0], target[1], self.colors[self.framecount % 256])
        #if not self.last_target:
        #    self.last_target = target
        #pygame.draw.line(self.points, self.colors[self.framecount % 256], self.last_target, target)
        #self.last_target = target  # new position
        self.framecount += 1


def main():
    try:
        fps = 50
        pygame.init()
        surface = pygame.display.set_mode((1024, 768))
        effects = [
            Hands(surface, (512, 350), 200, 10),
        ]
        # clock = pygame.time.Clock()
        pause = False
        while True:
            # clock.tick(fps)
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
            #pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()

