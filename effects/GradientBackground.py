#!/usr/bin/python3

import sys
import pygame
# own modules
from ColorGradient import ColorGradient as ColorGradient


FPS = 50
DIM = (320, 200)


class BackgroundGradient(object):
    """draws gradient background"""

    def __init__(self, dim: tuple):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.surface = pygame.Surface(dim)
        # initialize values
        self.colors = []
        color_gradient = ColorGradient(0.3, 0.2, 0.1)
        for y in range(self.surface.get_height()):
            self.colors.append(color_gradient.get_color())

    def update(self):
        """update every frame"""
        for y in range(self.surface.get_height()):
            pygame.draw.line(self.surface, self.colors[y], (0, y), (self.surface.get_width(), y))
        return self.surface


def main():
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        clock = pygame.time.Clock()
        background_gradient = BackgroundGradient(DIM)
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
                surface.blit(background_gradient.update(), (0, 0))
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == '__main__':
    main()

