#!/usr/bin/python3
# non std modules
import pygame


FPS = 2
DIM = (600, 600)


class PrimeSpiral(object):
    """ Prime Spiral """

    def __init__(self, dim:tuple):
        """
        good to use for background, not really an animation

        :param dim: dimension of surface to draw on
        :param iteration: how many iterations to calculate
        :param length: length of individual segment
        """
        self.dim = dim
        self.surface = pygame.Surface(dim)
        self.center_x = dim[0] // 2
        self.center_y = dim[1] // 2
        self.center = pygame.Vector2(dim[0] // 2, dim[1] // 2)
        self.max = min(self.center_y, self.center_x)
        self._draw()

    def _is_prime(self, number):
        """
        checking if number is prime

        taken from https://www.rosettacode.org/wiki/Extensible_prime_generator#PureBasic
        """
        if not number % 2:
            return False
        i = 5
        while i * i <= number:
            if not number % i:
                return False
            i += 2
            if not number % i:
                return False
            i += 4
        return True

    def _prime_generator(self):
        """ generates prime numbers, starting at 1 """
        first_primes = [1, 2, 3, 5, 7, 11]
        for number in first_primes:
            yield number
        number += 1
        while True:
            if self._is_prime(number):
                yield number
            number += 1

    def _draw(self):
        p_array = pygame.PixelArray(self.surface)
        for counter, prime in enumerate(self._prime_generator()):
            vector = pygame.Vector2()
            vector.from_polar((prime / 50, prime))
            if vector.length() > self.max:
                break
            point = self.center + vector
            p_array[int(point.x), int(point.y)] = pygame.Color(255, 255, 255, 255)
        p_array.close()

    def update(self):
        return self.surface


def main():
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        effects = [
            PrimeSpiral(DIM)
        ]
        clock = pygame.time.Clock()
        pause = False
        while True:
            clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
                    return
            if pause is not True:
                surface.fill(0)
                for effect in effects:
                    surface.blit(effect.update(), (0, 0))
                pygame.display.flip()
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == "__main__" :
    main()
