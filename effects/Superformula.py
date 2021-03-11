#!/usr/bin/python
import math
# non std modules
import pygame
# own modules
from RgbColorGradient import get_rgb_color_gradient


FPS = 50
PALETTE = get_rgb_color_gradient((50, 140, 70), (240, 0, 70), 256)


class Superformula(object):
    """ Draw Superformula Object, most basic form static drawing """

    def __init__(self, surface: pygame.Surface, pos: pygame.Vector2, size: int, color: tuple, params: list):
        """
        a particle in 2D space

        :param surface: surface to draw on
        :param pos: position to set particle, center of particle
        :param size: size of particle
        :param color: color of particle
        :param parms: tuple oof four (m, n1, n2, n3)
        """
        self.surface = surface
        self.pos = pos  # initial position
        self.size = size
        self.color = color
        self.params = params
        # split up parameters
        self.m, self.n1, self.n2, self.n3 = params
        self.a = 1.0  # fixed to one
        self.b = 1.0
        self.framecount = 0
        self._draw()

    def _radius(self, theta: float) -> float:
        """
        calculate radius - unscaled

        :param theta: value in radians
        """
        return pow(pow(abs(math.cos(self.m * theta / 4.0) / self.a), self.n2) + pow(abs(math.sin(self.m * theta / 4) / self.b), self.n3), -1 / self.n1)

    def _draw(self):
        """
        draw suoperformula based on current parameters
        """
        points = []
        step = math.pi / 180.0  # step by 1 degree
        # get local
        framecount = self.framecount
        size = self.size
        pos_x = self.pos.x
        pos_y = self.pos.y
        for degree in range(0, 720):
            radius = self._radius(step * (degree + framecount))
            x = pos_x + math.cos(step * (degree + framecount)) * radius * size
            y = pos_y + math.sin(step * (degree + framecount)) * radius * size
            points.append((int(x), int(y)))
        pygame.draw.lines(self.surface, PALETTE[self.framecount % 256], False, points, 3)

    def update(self, params=None):
        """ update every frame """
        if params and self.params != params:  # if something changed
            self.m, self.n1, self.n2, self.n3 = params
        self._draw()
        self.framecount += 1


class SuperformulaAnimation(object):
    """ Draw Superformula Object and vary some parameters on every frame """

    def __init__(self, surface: pygame.Surface, pos: pygame.Vector2, size: int, color: tuple):
        """
        animated superformula figure in 2D, altering some parameters every frame

        :param surface: surface to draw on
        :param pos: position to set particle, center of particle
        :param size: size of particle
        :param color: color of particle
        :param parms: tuple oof four (m, n1, n2, n3)
        """
        self.surface = surface
        self.pos = pos  # initial position
        self.size = size
        self.color = color
        # initial set of values
        self.m, self.n1, self.n2, self.n3 = (3.0, 4.5, 10.0, 10.0)
        self.a = self.b = 1.0  # fixed to one
        self.framecount = 0
        self.params = None
        self._calculate()
        self.sf = Superformula(surface, pygame.Vector2(320, 240), 100, (255, 255, 255), list(self.params.values()))

    def _calculate(self):
        """ calculate new parameter dependin on framerate """
        self.params = {
            "m": (1.1 + math.sin(math.radians(self.framecount))) * 5,
            "n1": (1.1 + math.sin(math.radians(self.framecount * 2))) * 1.1,
            "n2": (1.1 + math.sin(math.radians(self.framecount * 4))) * 1.2,
            "n3": (1.5 + math.sin(math.radians(self.framecount * 8))) * 1.3
        }

    def update(self):
        """ update every frame """
        self._calculate()
        self.sf.update(list(self.params.values()))
        self.framecount += 1


def main():

    try:
        surface = pygame.display.set_mode((640, 480))
        pygame.init()
        things = (
            SuperformulaAnimation(surface, pygame.Vector2(320, 240), 100, (255, 255, 255)),
            )
        clock = pygame.time.Clock()
        # mark pause state
        pause = False
        # fill background
        surface.fill((0, 0, 0, 255))
        while True:
            # limit to FPS
            clock.tick(FPS)
            # Event Handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
                if keyinput[pygame.K_p]:
                    pause = not pause
            # Update Graphics
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                for thing in things:
                    thing.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()

