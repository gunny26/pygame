#!/usr/bin/python3
import sys
import random
# non std modules
import pygame

FPS = 50
DIM =(640, 480)
RULESET = 195  # chaotic
#RULESET = 110
#RULESET = 199

class WolframElementary(object):
    """ simple Cellular Automata - Wolfram Elementary"""

    def __init__(self, dim: tuple, ruleset: int):
        """
        :param dim: dimension of surface to draw on
        :param ruleset: ruleset to use
        """
        self.width, self.height = dim  # (width, height) tuple
        self.width = self.width // 2
        self.height = self.height // 2
        self.ruleset = ruleset
        self.surface = pygame.Surface(dim)
        self.generation = [0] + [random.randint(0, 1) for i in range(self.width - 1)] + [0]  # actual generation

    def rule(self, left: int, center: int, right: int) -> int:
        """ apply ruleset """
        number = left * 4 + center * 2 + right
        if number == 7:
            if self.ruleset & 0b10000000:
                return 1
        if number == 6:
            if self.ruleset & 0b01000000:
                return 1
        if number == 5:
            if self.ruleset & 0b00100000:
                return 1
        if number == 4:
            if self.ruleset & 0b00010000:
                return 1
        if number == 3:
            if self.ruleset & 0b00001000:
                return 1
        if number == 2:
            if self.ruleset & 0b00000100:
                return 1
        if number == 1:
            if self.ruleset & 0b00000010:
                return 1
        if number == 0:
            if self.ruleset & 0b00000001:
                return 1
        return 0

    def update(self, ruleset=None) -> pygame.Surface:
        """ every fram a new generation """
        if ruleset:
            self.ruleset = ruleset  # change to new ruleset
        surface = self.surface.copy()
        self.surface.blit(surface, (0, -1))  # move one pixel up
        g = self.generation  # shortcut
        self.generation = [0] + [self.rule(g[i-1], g[i], g[i+1]) for i in range(1, len(self.generation) - 1)] + [0]  # next generation
        p_array = pygame.PixelArray(self.surface)  # draw next generation
        for x in range(self.width):
            if self.generation[x]:
                p_array[x, self.height - 1] = (255, 255, 255, 255)
            else:
                p_array[x, self.height - 1] = (0, 0, 0, 255)
        p_array.close()
        return pygame.transform.scale2x(self.surface)


def test():
    """ test """
    pygame.display.init()
    surface = pygame.display.set_mode(DIM)
    clock = pygame.time.Clock()
    effect = WolframElementary(DIM, RULESET)
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
