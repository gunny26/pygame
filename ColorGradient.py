#!/usr/bin/python3

import pygame
import sys
import math

class ColorGradient(object):
    """Simple Class to give back gradient colors"""

    def __init__(self, rstep, gstep, bstep):
        """
        (float) rstep - red color step width
        (float) gstep - green color step width
        (float) bstep - blue color step width
        """
        self.rstep = float(rstep)
        self.gstep = float(gstep)
        self.bstep = float(bstep)
        # initial values
        self.red = 0.0
        self.green = 0.0
        self.blue = 0.0
        self.step = float(math.pi / 180)
        self.degree = 0.0

    def get_color(self):
        """returns next color"""
        self.red += 256 * math.sin(self.degree * self.rstep)
        self.green += 256 * math.sin(self.degree * self.gstep)
        self.blue += 256 * math.sin(self.degree * self.bstep)
        color = (self.red % 256, self.green % 256, self.blue % 256)
        self.degree += self.step
        return(color) 


def test():
    try:
        fps = 50
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        clock = pygame.time.Clock()       
        cg = ColorGradient(0.0, 0.05, 0.05)
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
                surface.fill(cg.get_color())
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == '__main__':
    test()

