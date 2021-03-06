#!/usr/bin/python
#

import sys
import pygame
import numpy
# from numpy import *

class Mandelbrot2(object):
    """Vectorized Mandelbrot Function, realy fast even on python"""

    def __init__(self, surface):
        """
        (pygame.Surface) surface - surface to blit on
        """
        self.surface = surface
        # set some values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.img = None
        self.initialize(self.width, self.height, 100, -2.1, 0.7, -1.2, 1.2)
        print "done new version"
        print self.img[0, 0]

    def initialize(self, n, m, itermax, xmin, xmax, ymin, ymax):
        """vectorized version, remebers escaped pixels"""
        ix, iy = numpy.mgrid[0:n, 0:m]
        x = numpy.linspace(xmin, xmax, n)[ix]
        y = numpy.linspace(ymin, ymax, m)[iy]
        c = x + complex(0, 1) * y
        del x, y # save a bit of memory, we only need z
        self.img = numpy.zeros(c.shape, dtype=int)
        ix.shape = n * m
        iy.shape = n * m
        c.shape = n * m
        z = numpy.copy(c)
        for i in xrange(itermax):
            if not len(z): 
                break # all points have escaped
            numpy.multiply(z, z, z)
            numpy.add(z, c, z)
            rem = abs(z) > 2.0
            self.img[ix[rem], iy[rem]] = i + 1
            rem = -rem
            z = z[rem]
            ix, iy = ix[rem], iy[rem]
            c = c[rem]
           
    def update(self):
        """blit every frame"""
        pygame.surfarray.blit_array(self.surface, self.img)

def test():
    try:
        fps = 1
        surface = pygame.display.set_mode((800, 600))
        pygame.init()
        mandelbrot = Mandelbrot2(surface)
        clock = pygame.time.Clock()       
        pause = False
        while True:
            clock.tick(fps)
            events = pygame.event.get()  
            for event in events:  
                if event.type == pygame.QUIT:  
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    sys.exit(0)
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                mandelbrot.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'


if __name__ == '__main__':
    test()

