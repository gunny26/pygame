#!/usr/bin/python3
import math
# non std modules
import pygame
# own modules
from RgbColorGradient import get_rgb_color_gradient


FPS = 60
DIM = (320, 200)  # initial window size
SIN = [math.sin(math.radians(degree)) for degree in range(0, 360, 1)]
PALETTE = get_rgb_color_gradient((50, 140, 70, 255), (240, 0, 70, 255), 256)


class RotatingLines(object):
    """ some rotating line """

    def __init__(self, dim: tuple, center: tuple = (160, 100), radius: int = 100, factor: int = 2, anglecount: int = 1):
        """
        drawing rotating lines

        :param dim: dimension of surface to draw on
        :param center: tuple of center lines are moving around
        :param radius: radius of rotation
        :param factor: factor between degrees
        :param anglecount: angle in degree to add every frame
        """
        self.surface = pygame.Surface(dim)
        self.radius = radius
        self.center = center
        self.factor = factor
        self.anglecount = anglecount
        self.angle = 0  # starting angle

    def update(self):
        """ update every frame """
        self.surface.fill((0, 0, 0, 255))
        points = []
        for afterglow in range(1, 16):
            angle = self.angle + 2 * afterglow  # this amount of degrees back
            x1 = self.center[0] + int(self.radius * SIN[int((angle + 90) * self.factor) % 360])
            y1 = self.center[1] + int(self.radius * SIN[int(angle) % 360])
            x2 = self.center[0] + int(self.radius * SIN[int((angle + 135) * self.factor) % 360])
            y2 = self.center[1] + int(self.radius * SIN[int(angle + 45) % 360])
            color = PALETTE[afterglow * 16]
            points.append(((x1, y1, color), (x2, y2, color)))
        for point1, point2 in points:
            pygame.draw.line(self.surface, point1[2], (point1[0], point1[1]), (point2[0], point2[1]), 2)
        self.angle += self.anglecount
        return self.surface


def main():
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        clock = pygame.time.Clock()
        effects = [
            RotatingLines(DIM, (160, 100), 100, 3, 0.9),
            RotatingLines(DIM, (160, 100), 100, 5, 1.1),
            RotatingLines(DIM, (160, 100), 100, 2, 1.2),
            RotatingLines(DIM, (160, 100), 100, 5, 1.3),
        ]
        for effect in effects:
            effect.update()
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
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except (KeyboardInterrupt, pygame.error):
        pygame.quit()


if __name__ == '__main__':
    main()
