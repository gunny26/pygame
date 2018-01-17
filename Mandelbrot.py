#!/usr/bin/python
#
from __future__ import print_function
import sys
import time
import pygame

class Mandelbrot(object):
    """Clasical Mandelbrot Function, realy slow on python, so have some patience"""

    def __init__(self, surface):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.surface = surface
        # set some values
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.array2d = pygame.surfarray.array2d(self.surface)
        starttime = time.time()
        self.version3()
        print("done in %0.3f" % (time.time() - starttime))

    def version1(self, left=-2.1, right=0.7, bottom=-1.2, top=1.2, maxiter=30):
        """
        initialize pixelarray with color value,
        classical approach, really, really slow
        """
        x = xx = y = cx = cy = betrag = x2 = y2 = None
        iteration = hx = hy = None
        itermax = 255		# how many iterations to do
        magnify = 1.0		# no magnification
        stepy = (top - bottom) / self.height
        stepx = (right - left) / self.width
        cy = bottom
        for hy in xrange(self.height):
            cx = left
            for hx in xrange(self.width):
                x = cx
                y = cy
                iteration = 0
                betrag = 0
                while (iteration < itermax) and (betrag < maxiter):
                    x2 = x * x
                    y2 = y * y
                    betrag = x2 + y2
                    y = 2.0 * x * y + cy
                    x = x2 - y2 + cx
                    # x = xx
                    iteration += 1
                self.array2d[hx][hy] = pygame.Color(iteration, iteration, iteration)
                cx = cx + stepx
            cy = cy + stepy

    def version2(self, left=-2.1, right=0.7, bottom=-1.2, top=1.2, maxiter=30):
        """
        initialize pixelarray with color value,
        classical approach, really, really slow

        new approach, interate up to max_interations
        skip points who are above interation
        """
        itermax = 255		# how many iterations to do
        stepy = (top - bottom) / float(self.height)
        stepx = (right - left) / float(self.width)
        length = self.height * self.width
        workmap = [] # state after avery interation
        starttime = time.time()
        cy = bottom
        index = 0
        for y in range(self.height):
            cx = left
            for x in range(self.width):
                workmap.append([cx, cy, 0.0, cx, cy, 255, index])
                pixelmap.append(255)
                cx += stepx
                index += 1
            cy += stepy
        print("initializing in %0.3f" % (time.time() - starttime))
        starttime = time.time()
        worklist = range(length)
        for iteration in range(itermax):
            newmap = []
            for value in workmap:
                cx, cy, _, x, y, _, idx = value
                # cx, cy, _, x, y, _, index = workmap[idx]
                x2 = x * x
                y2 = y * y
                newmap.append([cx, cy, x2 + y2, x2 - y2 + cx, 2.0 * x * y + cy, iteration, idx])
                #workmap[idx][2] = x2 + y2
                #workmap[idx][3] = x2 - y2 + cx
                #workmap[idx][4] = 2.0 * x * y + cy
                #workmap[idx][5] = iteration
            # filter
            workmap = [value for value in newmap if value[2] < 31]
            if len(workmap) == 0:
                break
        print("calculation in %0.3f" % (time.time() - starttime))
        starttime = time.time()
        for index, data in enumerate(workmap):
            x = index % self.width
            y = int(index / self.width)
            iteration = data[5]
            self.array2d[x][y] = pygame.Color(iteration, iteration, iteration)
        print("to screen in %0.3f" % (time.time() - starttime))

    def version3(self, left=-2.1, right=0.7, bottom=-1.2, top=1.2, maxiter=30):
        """
        initialize pixelarray with color value,
        classical approach, really, really slow

        new approach, interate up to max_interations
        skip points who are above interation
        """
        itermax = 255		# how many iterations to do
        stepy = (top - bottom) / float(self.height)
        stepx = (right - left) / float(self.width)
        length = self.height * self.width
        workmap = [] # state after avery interation
        starttime = time.time()
        cx_map = [left + stepx * i for i in range(length)]
        x_map = [left + stepx * i for i in range(length)]
        cy_map = [bottom + stepy * i for i in range(length)]
        y_map = [bottom + stepy * i for i in range(length)]
        value_map = None
        iter_map = None
        index_map = None
        pixel_map = None
        print("initializing in %0.3f" % (time.time() - starttime))
        starttime = time.time()
        for iteration in range(itermax):
            # x2 = x * x
            x2 = [x * x for x in x_map]
            # y2 = y * y
            y2 = [y * y for y in y_map]
            # betrag = x2 + y2
            value_map = [a[0] + a[1] for a in zip(x2, y2)]
            print([value for value in value_map if value > 31.0])
            # x = x2 - y2 + cx
            x_map = [a[0] - a[1] + a[2] for a in zip(x2, y2, cx_map)]
            # y = 2.0 * x * y + cy
            y_map = [2.0 * a[0] * a[1] + a[2] for a in zip(x_map, y_map, cy_map)]
        print("calculation in %0.3f" % (time.time() - starttime))
        #starttime = time.time()
        #for index, data in enumerate(workmap):
        #    x = index % self.width
        #    y = int(index / self.width)
        #    iteration = data[5]
        #    self.array2d[x][y] = pygame.Color(iteration, iteration, iteration)
        print("to screen in %0.3f" % (time.time() - starttime))


    def update(self):
        """blit pixelarray to surface"""
        pygame.surfarray.blit_array(self.surface, self.array2d)

def main():
    try:
        fps = 25
        surface = pygame.display.set_mode((10, 10))
        # pygame.init()
        mandelbrot = Mandelbrot(surface)
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
                    sys.exit(1)
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                mandelbrot.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        print("shutting down")


if __name__ == '__main__':
    main()

