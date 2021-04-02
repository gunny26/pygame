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
        draw grid on surface
        """
        surface = self.b_surface
        data = mandelbrot_noncomplex(self.middle, self.step.real, surface.get_width(), surface.get_height(), int(self.maxiter))
        color = pygame.PixelArray(surface)
        for index, point in enumerate(data):
            x = index % surface.get_width()
            y =  index // surface.get_width()
            color[x, y] = self.palette[127 + point % 2 * 127]
        color.close()
        # draw grid
        grid_color = (0, 0, 0, 255)
        grid_width = 20
        for y in range(0, surface.get_height(), grid_width):
            pygame.draw.line(surface, grid_color, (0, y), (surface.get_width(), y))
        for x in range(0, surface.get_width(), grid_width):
            pygame.draw.line(surface, grid_color, (x, 0), (x, surface.get_height()))

    def complex_to_surface(self, c_point):
        """
        translate complex plane to surface plane
        """
        left = self.middle.real - self.surface.get_width() * self.step / 2
        right = self.middle.real + self.surface.get_width() * self.step / 2
        bottom = self.middle.imag - self.surface.get_height() * self.step / 2
        top = self.middle.imag + self.surface.get_height() * self.step / 2
        width = self.surface.get_width()
        height = self.surface.get_height()
        s_point = (
            mapto(c_point[0], left, right, 0, width),
            mapto(c_point[1], bottom, top, 0, height)
        )
        return s_point

    def surface_to_complex(self, s_point):
        """
        translate surface plane to complex plane
        """
        left = self.middle.real - self.surface.get_width() * self.step / 2
        right = self.middle.real + self.surface.get_width() * self.step / 2
        c_span_real = right - left
        bottom = self.middle.imag - self.surface.get_height() * self.step / 2
        top = self.middle.imag + self.surface.get_height() * self.step / 2
        c_span_imag = top - bottom
        width = self.surface.get_width()
        height = self.surface.get_height()
        c_to_s = (
            c_span_real / width,
            c_span_imag / height
        )
        s_to_c = (
            1 / c_to_s[0],
            1 / c_to_s[1]
        )
        c_point = complex(
            s_point[0] * c_to_s[0],
            s_point[1] * c_to_s[1]
        )
        #c_point = complex(
        #    mapto(s_point[0], 0, width, left, right),
        #    mapto(s_point[1], 0, height, bottom, top)
        #)
        return c_point

    def update(self):
        if self.last_pos != pygame.mouse.get_pos():  # if something changed
            left = self.middle.real - self.surface.get_width() * self.step / 2
            right = self.middle.real + self.surface.get_width() * self.step / 2
            bottom = self.middle.imag - self.surface.get_height() * self.step / 2
            top = self.middle.imag + self.surface.get_height() * self.step / 2
            width = self.surface.get_width()
            height = self.surface.get_height()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            c_pos = self.surface_to_complex(pygame.mouse.get_pos())
            print(c_pos)
            points = mandelbrot_path(c_pos, 255)
            s_points = []
            for index, point in enumerate(points):
                c_r, c_i = point
                s_point = self.complex_to_surface(point)
                print(s_point)
                s_x = self.dim[0] // 2 + mapto(c_r, left, right, 0, DIM[0])
                s_y = self.dim[1] // 2 + mapto(c_i, bottom, top, 0, DIM[1])
                s_points.append((s_x, s_y))
                #s_points.append(s_point)
            # draw on copy of background surface
            self.surface = self.b_surface.copy()
            if len(s_points) > 2:
                pygame.draw.lines(self.surface, (255,255,255,255), False, s_points, 1)
            # remember last position
            self.last_pos = pygame.mouse.get_pos()
        self.framecount += 1
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

