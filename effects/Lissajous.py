#!/usr/bin/python3
""" Foreground effect """
import sys
import math
# non std modules
import pygame


class Lissajou(object):
    """ Lines moving on Lissajous paths around """

    def __init__(self, surface: pygame.Surface, center: tuple = (160, 100), radius: int = 100, factor: int = 2, anglecount: int = 1):
        """
        :param surface: surface to draw on
        :param center: center the lines are moving around
        :param radius: radius of waves
        :param factor: factor between X- and Y-wave
        :param anglecount: anglestep per update
        """
        self.surface = surface
        self.radius = radius
        self.center = center
        self.factor = factor
        self.anglecount = anglecount
        self.angle = 0  # starting angle

    def update(self):
        """ update every frame """
        points = []
        for afterglow in range(1, 20):
            angle = self.angle - afterglow  # this amount of degrees back
            x = self.center[0] + int(self.radius * math.cos(math.radians(angle * self.factor)))
            y = self.center[1] + int(self.radius * math.sin(math.radians(angle)))
            color = (255 // afterglow, 255, 255)
            points.append((x, y, color))
        for index, point in enumerate(points[:-1]):
            pygame.draw.line(self.surface, point[2], (point[0], point[1]), (points[index+1][0], points[index+1][1]), 2)
        self.angle += self.anglecount


def main():
    try:
        fps = 50
        surface = pygame.display.set_mode((320, 200))
        pygame.init()
        clock = pygame.time.Clock()
        effects = [
            Lissajou(surface, (160, 100), 100, 3, 1),
            Lissajou(surface, (160, 100), 80, 5, 1.5),
            Lissajou(surface, (160, 100), 60, 7, 2),
            Lissajou(surface, (160, 100), 40, 11, 2.5),
            Lissajou(surface, (160, 100), 20, 13, 3),
        ]
        for effect in effects:
            effect.update()
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
                surface.fill((0, 0, 0, 255))
                for effect in effects:
                    effect.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()
