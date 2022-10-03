#!/usr/bin/python
#
import random
import math
# non std modules
import pygame
from pygame import gfxdraw
# own modules
from RgbColorGradient import get_rgb_color_gradient

FPS = 500
DIM = (640, 480)


@dataclass
class Pendulum:
    """Class for keeping track of an item in inventory."""
    center: pygame.Vector2  # initial position at framecount = 0
    rod: pygame.Vector2  # length of rod, from center, mass on the other hand
    mass: pygame.Vector2  # mass of blob
    gravity: pygame.Vector2  # unit vector of gravity

    def update(self):
        self.pos = self.center + self.rod * self.mass * self.gravity


class Pendulums:
    """Plasma Generator"""

    def __init__(self, dim: tuple):
        """
        :param surface: surface to draw on
        """
        self.surface = pygame.Surface(dim)
        center = pygame.Vector2(dim[0] // 2, 50)
        pendulums = [
            center, Pendulum(
                pygame.Vector2(100, 100),
                pygame.Vector2(
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
        return self.surface


class Hands2:
    """Plasma Generator"""

    def __init__(self, dim:tuple, center: tuple, amplitude: int = 256, num_parts: int = 16):
        """
        :param surface: surface to draw on
        :param center: center of calculations in (x, y)
        :param amplitude: maximum amplitude of single part
        :param pats: number of parts to generate
        """
        self.surface = pygame.Surface(dim)
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
        return self.surface


def main():
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        effects = [
            Hands2(surface, DIM, 200, 10),
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

