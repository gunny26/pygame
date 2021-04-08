#!/usr/bin/python
import math
# non std modules
import pygame
from pygame import gfxdraw
# own modules
from RgbColorGradient import get_rgb_color_gradient

FPS = 60
DIM = (320, 200)  # initial window size
SIN = [math.sin(math.radians(degree)) for degree in range(0, 360, 1)]
PALETTE = get_rgb_color_gradient((50, 140, 70, 255), (240, 0, 70, 255), 256)


def mapto(value: float, min1: float, max1: float, min2 : float, max2: float):
    """ map some value to a different scale """
    try:
        assert min1 <= value <= max1
        len1 = max1 - min1
        len2 = max2 - min2
        return value * len2 / len1
    except AssertionError as exc:
        print(f"value {value} not in range [{min1}, {max1}]")
        raise exc


class MandelbrotZoom:
    """ interfering colors """

    def __init__(self, dim: tuple, middle: complex, magnify: float, maxiter: int = 100, palette: list=PALETTE):
        """
        :param dim: dimension of output surface in (x, y)
        :param middle: complex number to zoom in
        :param magnify: factor to zoom in every frame
        :param maxiter: maximum interation of mandelbrot algorithm
        :param palette: color palette to use
        """
        self.dim = dim
        self.middle = middle
        self.magnify = magnify
        self.maxiter = maxiter
        self.palette = palette
        # dimension of drawing surface, smaller than output surface
        self.scale = 4  # scale of smaller calculation surface
        self.surface = pygame.Surface((dim[0] // self.scale, dim[1] // self.scale))
        # zooming constants
        self.step = 0.04375
        self.framecount = 0

    def update(self) -> pygame.Surface:
        """
        blit on background surface

        thats a clean pythonic mandelbrot set algorithm
        readable but not fast

        probably not very useful for effects
        """
        # calculating corners in complex plane
        left = self.middle.real - self.surface.get_width() * self.step / 2
        bottom = self.middle.imag - self.surface.get_height() * self.step / 2
        color = pygame.PixelArray(self.surface)
        # starting value
        for y, imag in [(i, bottom + i * self.step) for i in range(self.surface.get_height())]:
            for x, real in [(i, left + i * self.step) for i in range(self.surface.get_width())]:
                constant = complex(real, imag)
                value = constant
                n = 0
                while n < self.maxiter:
                    if abs(value) > 2.0:
                        break
                    value = value ** 2 + constant
                    n += 1
                if n == self.maxiter:
                    color[x, y] = (0, 0, 0, 255)
                else:
                    color[x, y] = self.palette[int(mapto(n, 0.0, self.maxiter, 0, 255))]
        color.close()
        self.step *= self.magnify  # zoom in
        self.maxiter = int(self.maxiter * 1.01)
        self.framecount += 1
        return pygame.transform.scale(self.surface, self.dim)


def main():
    try:
        pygame.display.init()  # only initialize display, no other modules
        surface = pygame.display.set_mode(DIM)
        effects = [
            MandelbrotZoom(DIM, middle=complex(-0.8115312340458353, 0.2014296112433656), magnify=0.9)
        ]
        clock = pygame.time.Clock()
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
                if keyinput[pygame.K_f]:  # go to FULLSCREEN
                    pygame.display.quit()
                    pygame.display.init()
                    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            if pause is not True:
                surface.fill((0, 0, 0))
                for background in effects:
                    b_surface = background.update()
                    pygame.transform.scale(b_surface, (surface.get_width(), surface.get_height()), surface)  # blit and scale to display
                pygame.display.flip()
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()

