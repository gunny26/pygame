#!/usr/bin/python3
import sys
import random
# non std modules
import pygame

FPS = 50
DIM =(800, 600)


class GameOfLife(object):
    """ simple Cellular Automata - Conways Game of Life"""

    def __init__(self, dim: tuple, scale=2, density=15):
        """
        :param dim: dimension of surface to draw on
        :param ruleset: ruleset to use
        """
        self.dim = dim
        self.scale = scale
        self.density = density
        self.width = dim[0] // scale
        self.height = dim[1] // scale
        self.surface = pygame.Surface(dim)
        self.cells = [[0 for x in range(self.width)] for y in range(self.height)]
        for i in range((self.width * self.height) // density):
            x = random.randint(1, self.width - 1)
            y = random.randint(1, self.height -1)
            self.cells[y][x] = 1

    def update(self) -> pygame.Surface:
        """ every frame a new generation """
        p_array = pygame.PixelArray(self.surface)
        cells = self.cells  # shortcut
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                color = (0, 0, 0, 255)
                old_state = cells[y][x]
                neighbors = (
                    cells[y-1][x-1],    cells[y-1][x],  cells[y-1][x+1],
                    cells[y][x-1],      0,              cells[y][x+1],
                    cells[y+1][x-1],    cells[y+1][x],  cells[y+1][x+1]
                )
                s_neighbors = sum(neighbors)
                if cells[y][x]:  # actual state alive
                    if s_neighbors < 2:  # loneliness
                        cells[y][x] = 0
                        color = (0, 0, 0, 255)
                    elif s_neighbors > 3:  # overcrouded
                        cells[y][x] = 0
                        color = (0, 0, 0, 255)
                    else:  # stay alive
                        color = (255, 255, 255, 255)
                else:  # actual state death
                    if s_neighbors == 3:  # rebirth
                        cells[y][x] = 1
                        color = (255, 255, 255, 255)
                # to surface
                p_array[x, y] = color
        p_array.close()
        return pygame.transform.scale2x(self.surface)


def test():
    """ test """
    pygame.display.init()
    surface = pygame.display.set_mode(DIM)
    clock = pygame.time.Clock()
    effect = GameOfLife(DIM, 2, 15)
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
