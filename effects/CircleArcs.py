#!/usr/bin/python
import math
import random
# non std modules
import pygame
# own modules
from RgbColorGradient import get_rgb_color_gradient


FPS = 50
DIM = (640, 480)


class Arc(object):
    """ Draw Superformula Object, most basic form static drawing """

    def __init__(self, surface: pygame.Surface, pos: pygame.Vector2, color: tuple, params: list):
        """
        a particle in 2D space

        :param dim: dimensio of surface to draw on
        :param pos: position to set particle, center of particle
        :param size: size of particle
        :param color: color of particle
        :param width of circle arc
        """
        self.surface = surface
        self.pos = pos  # initial position
        self.color = color
        self.params = params
        # inner radius
        # outher radius will be radius + width
        # start_angle stop_angle -> where the arc will be drawn
        # direction - if positiv counter clockwise, otherwise clockwise
        self.radius, self.start_angle, self.stop_angle, self.width, self.speed = params
        self.framecount = 0
        self._draw()

    def _draw(self):
        """
        draw thick arc from start_angle to stop_angle
        """
        step = math.pi / 180
        direction = 1
        if self.stop_angle < self.start_angle:
            direction = -1
        inner = []
        outer = []
        for degree in range(int(self.start_angle), int(self.stop_angle), direction):
            x = self.pos.x + self.radius * math.cos(degree * step)
            y = self.pos.y + self.radius * math.sin(degree * step)
            outer.append((x, y))
            x = self.pos.x + (self.radius - self.width) * math.cos(degree * step)
            y = self.pos.y + (self.radius - self.width) * math.sin(degree * step)
            inner.append((x, y))
        self.start_angle += (direction * self.speed)
        self.stop_angle += (direction * self.speed)
        pygame.draw.polygon(self.surface, self.color, outer + inner[::-1], 1)

    def update(self, params=None):
        """ update every frame """
        if params and self.params != params:  # if something changed
            self.radius, self.start_angle, self.stop_angle, self.width, self.speed = params
        self._draw()
        self.framecount += 1
        return self.surface


class ArcAnimation(object):
    """ Draw Superformula Object and vary some parameters on every frame """

    def __init__(self, dim: tuple, pos: pygame.Vector2, size: int, color: tuple):
        """
        animated superformula figure in 2D, altering some parameters every frame

        :param dim: dimension of surface to draw on
        :param pos: position to set particle, center of particle
        :param size: size of particle
        :param color: color of particle
        :param parms: tuple oof four (m, n1, n2, n3)
        """
        self.surface = pygame.Surface(dim)
        self.pos = pos  # initial position
        self.size = size
        self.color = color
        # initial set of values
        self.arcs = []
        count = 10
        palette = get_rgb_color_gradient((50, 140, 70), (240, 0, 70), count)
        for i in range(count):
            start_angle = random.randint(-360, 360)
            stop_angle = random.randint(-360, 360)
            width = 10
            speed = 1.5 - random.random()
            self.arcs.append(Arc(self.surface, pos, palette[i], (size - i * 20, start_angle, stop_angle, width, speed)))
        self.framecount = 0

    def update(self):
        """ update every frame """
        self.surface.fill(0)
        for arc in self.arcs:
            arc.update()
        self.framecount += 1
        return self.surface


def main():

    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        things = (
            ArcAnimation(DIM, pygame.Vector2(320, 240), 200, (0x74, 0x54, 0x6a)),
        )
        clock = pygame.time.Clock()
        # mark pause state
        pause = False
        # fill background
        surface.fill(0)
        while True:
            # limit to FPS
            clock.tick(FPS)
            # Event Handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
                    return
                if keyinput[pygame.K_p]:
                    pause = not pause
            # Update Graphics
            if pause is not True:
                surface.fill(0)
                for thing in things:
                    surface.blit(thing.update(), (0, 0))
                pygame.display.flip()
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()
