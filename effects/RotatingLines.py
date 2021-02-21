#!/usr/bin/python3

import pygame
import sys
import math

class RotatingLines(object):
    """Sinus wave scroll text"""

    def __init__(self, surface, center=(160, 100), radius=100, factor=2, anglecount=1):
        """
        (pygame.Surface) surface to draw on
        """
        self.surface = surface
        self.radius = radius
        self.center = center
        self.factor = factor
        self.anglecount = anglecount
        self.angle = 0  # starting angle

    def update(self):
        """
        update every frame
        (int)hpos y axis offset
        """
        points = []
        for afterglow in range(1, 16):
            angle = self.angle + 2 * afterglow# this amount of degrees back
            x1 = self.center[0] + int(self.radius * math.cos(math.radians(angle * self.factor)))
            y1 = self.center[1] + int(self.radius * math.sin(math.radians(angle)))
            x2 = self.center[0] + int(self.radius * math.cos(math.radians((angle + 45) * self.factor)))
            y2 = self.center[1] + int(self.radius * math.sin(math.radians(angle + 45)))
            color = (255 // afterglow, 0, 0)
            points.append(((x1, y1, color), (x2, y2, color)))
        for point1, point2 in points:
            pygame.draw.line(self.surface, point1[2], (point1[0], point1[1]), (point2[0], point2[1]), 2)
        self.angle += self.anglecount


def main():
    try:
        fps = 60
        surface = pygame.display.set_mode((320, 200))
        pygame.init()
        clock = pygame.time.Clock()
        effects = [
            RotatingLines(surface, (160, 100), 100, 3, 0.9),
            RotatingLines(surface, (160, 100), 100, 5, 1.1),
            RotatingLines(surface, (160, 100), 100, 2, 1.2),
            RotatingLines(surface, (160, 100), 100, 5, 1.3),
        ]
        for effect in effects:
            effect.update()
        pause = False
        while True:
            clock.tick(fps)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    sys.exit(1)
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                for effect in effects:
                    effect.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        print('shutting down')

if __name__ == '__main__':
    main()
