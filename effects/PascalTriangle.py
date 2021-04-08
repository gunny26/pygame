#!/usr/bin/python3
import math
# non std modules
import pygame


FPS = 50
DIM = (320, 200)


class PascalTriangle(object):
    """Draw Pascal Triangle on surface, not moving"""

    def __init__(self, dim: tuple, base: int, radius: int, numrows: int):
        """
        :param dim    : surface - surface to draw on
        :param base   : color modulo value
        :param radius : size of circles
        :param numrows: how many rows should be calculated
        """
        self.surface = pygame.Surface(dim)
        self.width, self.height = dim  # (width, height) tuple
        self.base = base
        self.radius = radius
        self.num_rows = numrows
        self.initialize()

    def initialize(self):
        """ draw something """
        dy = math.sqrt(2) * self.radius
        row_above_colors = None
        for row in range(self.num_rows):
            current_row_colors = []
            for col in range(row + 1):
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
                    color = pygame.Color(255, 255, 255)
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
                rect = pygame.Rect(self.width // 2 + self.radius * (2 * col - row), dy * (row + 1), self.radius * 2, self.radius * 2)
                pygame.draw.ellipse(self.surface, color, rect, 1)
                current_row_colors.append(current_color)
            row_above_colors = current_row_colors

    def update(self) -> pygame.Surface:
        return self.surface


def test():
    """ test """
    surface = pygame.display.set_mode(DIM)
    pygame.init()
    clock = pygame.time.Clock()
    effect = PascalTriangle(DIM, 4, 4, 60)
    while True:
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
        surface.blit(effect.update(), (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    test()
