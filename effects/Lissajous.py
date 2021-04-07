#!/usr/bin/python3
""" Foreground effect """
import math
# non std modules
import pygame


FPS = 50
DIM = (320, 200)


class Lissajou(object):
    """ Lines moving on Lissajous paths around """

    def __init__(self, dim: tuple, center: tuple = (160, 100), radius: int = 100, factor: int = 2, anglecount: int = 1):
        """
        :param surface: surface to draw on
        :param center: center the lines are moving around
        :param radius: radius of waves
        :param factor: factor between X- and Y-wave
        :param anglecount: anglestep per update
        """
        self.surface = pygame.Surface(dim)
        self.radius = radius
        self.center = center
        self.factor = factor
        self.anglecount = anglecount
        self.angle = 0  # starting angle

    def update(self):
        """ update every frame """
        self.surface.fill((0, 0, 0, 0))
        points = []
        for afterglow in range(1, 20):
            angle = self.angle - afterglow  # this amount of degrees back
            x = self.center[0] + int(self.radius * math.cos(math.radians(angle * self.factor)))
            y = self.center[1] + int(self.radius * math.sin(math.radians(angle)))
            color = (255 // afterglow, 255, 255)
            points.append((x, y, color))
        for index, point in enumerate(points[:-1]):
            pygame.draw.line(self.surface, point[2], (point[0], point[1]), (points[index + 1][0], points[index + 1][1]), 2)
        self.angle += self.anglecount
        return self.surface


def main():
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        clock = pygame.time.Clock()
        size = (DIM[0] // 2, DIM[1] // 2)
        effects = [
            Lissajou(DIM, size, 100, 3, 1),
            Lissajou(DIM, size, 80, 5, 1.5),
            Lissajou(DIM, size, 60, 7, 2),
            Lissajou(DIM, size, 40, 11, 2.5),
            Lissajou(DIM, size, 20, 13, 3),
        ]
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
                surface.fill((0, 0, 0, 255))
                for effect in effects:
                    surface.blit(effect.update(), (0, 0), special_flags=pygame.BLEND_ADD)
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()
