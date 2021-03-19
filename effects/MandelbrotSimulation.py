#!/usr/bin/python
import math
# non std modules
import pygame
from pygame import gfxdraw
# own modules
from RgbColorGradient import get_rgb_color_gradient
from FastMath import mandelbrot_complex, mandelbrot_noncomplex, mapto, mandelbrot_path


FPS = 50
DIM = (1024, 768)  # initial window size
SIN = [math.sin(math.radians(degree)) for degree in range(0, 360, 1)]
PALETTE = get_rgb_color_gradient((0, 0, 0, 255), (240, 0, 70, 255), 256)


class MandelbrotPath:
    """ Madelbrot Set with Overlay to draw iteration points in set """

    def __init__(self, dim: tuple, middle: complex, maxiter: int = 100, palette: list=PALETTE):
        """
        (pygame.Surface) surface - surface to draw on
        :param dim: dimension of output surface in (x, y)
        :param middle: complex number to zoom in
        :param maxiter: maximum interation of mandelbrot algorithm
        :param palette: color palette to use
        """
        self.dim = dim
        self.middle = middle
        self.maxiter = maxiter
        self.palette = palette
        # dimension of drawing surface, smaller than output surface
        self.b_surface = pygame.Surface(dim)
        self.surface = pygame.Surface(dim)
        # zooming constants
        self.step = 0.005
        self.last_pos = (0, 0)
        self.framecount = 0
        self.initialize()

    def initialize(self) -> pygame.Surface:
        """
        draw basic mandelbrot set on background surface
        """
        data = mandelbrot_noncomplex(self.middle, self.step.real, self.surface.get_width(), self.surface.get_height(), int(self.maxiter))
        color = pygame.PixelArray(self.b_surface)
        for index, point in enumerate(data):
            x = index % self.surface.get_width()
            y =  index // self.surface.get_width()
            color[x, y] = self.palette[127 + point % 2 * 127]
        color.close()

    def update(self):
        if self.last_pos != pygame.mouse.get_pos():  # if something changed
            left = self.middle.real - self.surface.get_width() * self.step / 2
            right = self.middle.real + self.surface.get_width() * self.step / 2
            bottom = self.middle.imag - self.surface.get_height() * self.step / 2
            top = self.middle.imag + self.surface.get_height() * self.step / 2
            width = self.surface.get_width()
            height = self.surface.get_height()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            real = mapto(mouse_x, 0, DIM[0], left, right)
            imag = mapto(mouse_y, 0, DIM[1], bottom, top)
            self.framecount += 1
            points = mandelbrot_path(complex(real, imag), 255)
            s_points = []
            for index, point in enumerate(points):
                c_r, c_i = point
                s_x = self.dim[0] // 2 + mapto(c_r, left, right, 0, DIM[0])
                s_y = self.dim[1] // 2 + mapto(c_i, bottom, top, 0, DIM[1])
                s_points.append((s_x, s_y))
            # draw on surface
            self.surface = self.b_surface.copy()
            if len(s_points) > 2:
                pygame.draw.lines(self.surface, (255,255,255,255), False, s_points, 1)
        return self.surface


def main():
    try:
        pygame.display.init()  # only initialize display, no other modules
        surface = pygame.display.set_mode(DIM)
        effects = [
            # MandelbrotPath(DIM, middle=complex(-0.8115312340458353, 0.2014296112433656))
            MandelbrotPath(DIM, middle=complex(0, 0))
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
                    pygame.transform.scale(b_surface, DIM, surface)  # blit and scale to display
                pygame.display.flip()
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()

