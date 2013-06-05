#!/usr/bin/python3

import sys
import pygame
# own modules
from ColorGradient import ColorGradient as ColorGradient

class GradientBackground(object):
    """draws gradient background"""

    def __init__(self, surface):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.surface = surface
        # initialize values
        self.colors = []
        color_gradient = ColorGradient(0.3, 0.2, 0.1)
        for y in xrange(self.surface.get_height()):
            self.colors.append(color_gradient.get_color())

    def update(self):
        """update every frame"""
        for y in xrange(self.surface.get_height()):
            pygame.draw.line(self.surface, self.colors[y], (0, y), (self.surface.get_width(), y))


def test():
    try:
        fps = 25
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        clock = pygame.time.Clock()       
        background_gradient = BackgroundGradient(surface)
        pause = False
        while True:
            clock.tick(fps)
            events = pygame.event.get()  
            for event in events:  
                if event.type == pygame.QUIT:  
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    sys.exit(1)
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                background_gradient.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == '__main__':
    test()

