#!/usr/bin/python3
import sys
import random
# non std modules
import pygame

FPS = 50
DIM =(800, 600)


class GameOfLife(object):
    """ simple Cellular Automata - Wolfram Elementary"""

    def __init__(self, dim: tuple, scale=2, density=15):
        """
        :param dim: dimension of surface to draw on
        :param ruleset: ruleset to use
        """
        self.dim = dim
        self.scale = scale
        self.density = density
        self.width, self.height = dim  # (width, height) tuple
        self.width = self.width // scale
        self.height = self.height // scale
        self.surface = pygame.Surface(dim)
        self.cells = [[0 for x in range(self.width)] for y in range(self.height)]
        for i in range((self.width * self.height) // density):
            x = random.randint(1, self.width - 1)
            y = random.randint(1, self.height -1)
            self.cells[y][x] = 1

    def update(self) -> pygame.Surface:
        """ every fram a new generation """
        p_array = pygame.PixelArray(self.surface)
        cells = self.cells  # shortcut
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                old_state = cells[y][x]
                neighbors = (
                    cells[y-1][x-1], cells[y-1][x], cells[y-1][x+1],
                    cells[y][x-1], 0, cells[y][x+1],
                    cells[y+1][x-1], cells[y+1][x], cells[y+1][x+1]
                )
                if cells[y][x]:  # actual state alive
                    if sum(neighbors) < 2:  # loneliness
                        cells[y][x] = 0
                    elif sum(neighbors) > 3:  # overcrouded
                        cells[y][x] = 0
                else:  # actual state death
                    if sum(neighbors) == 3:  # rebirth
                        cells[y][x] = 1
                # to surface
                cell = cells[y][x]
                if cell:
                    if cell == old_state:
                        p_array[x, y] = (0, 255, 0, 255)
                    else:
                        p_array[x, y] = (0, 128, 0, 255)
                else:
                    if cell == old_state:
                        p_array[x, y] = (0, 0, 0, 255)
                    else:
                        p_array[x, y] = (0, 128, 255, 255)
        p_array.close()
        return pygame.transform.scale(self.surface, (self.dim[0] * self.scale, self.dim[1] * self.scale))


def test():
    """ test """
    pygame.display.init()
    surface = pygame.display.set_mode(DIM)
    clock = pygame.time.Clock()
    effect = GameOfLife(DIM, 4, 30)
    while True:
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
        surface.blit(effect.update(), (0, 0))
        pygame.display.update()

if __name__ == "__main__" :
    test()
