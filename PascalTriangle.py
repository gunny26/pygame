#!/usr/bin/python3

import sys
import pygame
import math


class PascalTriangle(object):
    """Draw Pascal Triangle on surface, not moving"""

    def __init__(self, surface, base, radius, numrows):
        """
        (pygame.Surface) surface - surface to draw on
        (int) base - color modulo value
        (float) radius - size of circles
        (int) numrows - how many rows should be calculated
        """
        self.surface = surface
        self.base = base
        self.radius = radius
        self.num_rows = numrows

    def update(self):
        """ draw something """
        dy = math.sqrt(2) * self.radius
        row_above_colors = None
        for row in xrange(self.num_rows):
            current_row_colors = []
            for col in xrange(row + 1):
                current_color = None
                color = None
                if (col == 0) or (col == row):
                    current_color = 1
                else:
                    left_color = row_above_colors[col - 1]
                    right_color = row_above_colors[col]
                    current_color = (left_color + right_color) % self.base
                if current_color == 0:
                    color = pygame.Color(255, 0, 0)
                elif current_color == 1:
                    color = pygame.Color(255, 255, 255);
                elif current_color == 2:
                    color = pygame.Color(0, 255, 0)
                elif current_color == 3:
                    color = pygame.Color(0, 115, 255)
                elif current_color == 4:
                    color = pygame.Color(255, 132, 0)
                elif current_color == 5:
                    color = pygame.Color(0, 247, 255)
                else:
                    color = pygame.Color(255, 255, 255)
                rect = pygame.Rect(200 + self.radius * (2 * col - row), dy * (row + 1), self.radius * 2, self.radius * 2)
                pygame.draw.ellipse(self.surface, color, rect, 1)
                current_row_colors.append(current_color)
            row_above_colors = current_row_colors


def test():
    """ test """
    fps = 1
    surface = pygame.display.set_mode((600, 400))
    pygame.init()
    clock = pygame.time.Clock()
    game_object = PascalTriangle(surface, 4, 4, 60)
    while True:
        clock.tick(fps)
        events = pygame.event.get()  
        for event in events:  
            if event.type == pygame.QUIT:  
                sys.exit(0)
        pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
        game_object.update()
        pygame.display.update()

if __name__ == "__main__" :
    test()
