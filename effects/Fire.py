#!/usr/bin/python3
import random
# non std modules
import pygame
import numpy


FPS = 50
DIM = (320, 200)


class Fire(object):
    """
    Simulated Fire, 2d effect
    idea and basic algorithm from
    http://lodev.org/cgtutor/fire.html
    """

    def __init__(self, dim, rect, scale=4):
        """
        (pygame.surface) surface - to draw on
        (pygame.Rect) dest - rect to blit fire on
        (int) width - width of fire
        (int) height - height of fire
        (int) scale - scale fire
        """
        self.surface = pygame.Surface(dim)
        self.rect = rect
        self.width = dim[0] // scale
        self.height = dim[1] // scale
        self.scale = scale
        # initialize values
        # scaled down surface
        self.drawsurface = pygame.Surface((self.width, self.height))
        self.drawsurface.fill((0, 0, 0))
        self.array2d = None
        self.fire = None
        self.palette = None
        self.initialize()

    def initialize(self):
        """generate palette and surface to draw intermdiate fire, also array"""
        # self.drawsurface.fill((0, 0, 0))
        self.array2d = pygame.surfarray.array2d(self.drawsurface)
        self.fire = numpy.zeros((self.width, self.height))
        # generate palette
        self.palette = numpy.zeros(255)
        # aplette should be something from black to yellow red
        self.palette[0] = pygame.Color(0, 0, 0, 255)
        for index in range(1, 255):
            color = pygame.Color(0, 0, 0, 255)
            # original C Comments
            # Hue goes from 0 to 85: red to yellow
            # Saturation is always the maximum: 255
            # Lightness is 0..100 for x=0..128, and 255 for x=128..255
            # color = HSLtoRGB(ColorHSL(x / 3, 255, std::min(255, x * 2)));
            color.hsla = (index, 100, index / 2.55, 10)
            self.palette[index] = color

    def update(self):
        """update every frame"""
        w = self.width
        h = self.height
        # random baseline
        for x in range(w):
            self.fire[x][h - 1] = abs(32768 + random.randint(0, 32768)) % 256
        # calculate each pixel according to neighbours
        for y in range(h - 1):
            for x in range(w):
                # every new point depends on O Points
                #    N
                #   OOO
                #    O
                self.fire[x][y] = (
                    (
                        self.fire[(x - 1) % w][(y + 1) % h] +
                        self.fire[(x) % w][(y + 2) % h] +
                        self.fire[(x + 1) % w][(y + 1) % h] +
                        self.fire[(x) % w][(y + 3) % h]
                    ) * 16
                ) / 65
                # the last factor 16/65 should be slightly larger than 4
                # and lesser than 5
                # closer to 4 will make flames higher
                self.array2d[x][y] = self.palette[int(self.fire[x][y])]
        pygame.surfarray.blit_array(self.drawsurface, self.array2d)
        # scale fire surface up to given size
        blitsurface = pygame.transform.scale(self.drawsurface, (self.width * self.scale, self.height * self.scale))
        self.surface.blit(blitsurface, self.rect)
        return self.surface


def main():
    try:
        pygame.init()
        surface = pygame.display.set_mode(DIM)
        effects = (
            Fire(DIM, pygame.Rect(0, 0, 320, 200), 8),
        )
        clock = pygame.time.Clock()
        pause = False
        surface.fill(0)
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
                for effect in effects:
                    surface.blit(effect.update(), (0, 0))
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()
