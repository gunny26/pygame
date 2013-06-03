#!/usr/bin/python

import pygame
from pygame import gfxdraw
import sys
import os
import math
import random
import numpy
from scipy.weave import converters
import time
from Vec2d import Vec2d
from Vec3d import Vec3d

FPS = 5000
RES = (400, 225)


class Plasma(object):
    """Plasma Effect on Surface"""

    def __init__(self, surface, scale=1):
        self.parent_surface = surface
        self.scale = scale
        # initialize things
        self.tick = 0
        self.upsize = surface.get_size()
        self.parent = surface
        self.surface = pygame.Surface(self.upsize)
        self.surface = pygame.transform.scale(self.surface, (self.surface.get_width() / scale, self.surface.get_height() / scale))
        self.array2d = pygame.surfarray.array2d(self.surface)
        self.initialize()

    def initialize(self):
        max_x = self.surface.get_width()
        max_y = self.surface.get_height()
        # self.data = numpy.zeros((max_y * max_x, 6))
        self.data = []
        t = self.tick
        color = pygame.Color(0, 0, 0, 255)
        counter = 0
        for height in range(max_y):
            for width in range(max_x):
                x = width * math.pi / 180
                y = height * math.pi / 180
                xx = width
                yy = height
                self.data.append((x, y, width, height, xx, yy))
                counter += 1
        self.sins = []
        self.steps = int(2000 * math.pi)
        step = 2 * math.pi / self.steps
        radian = 0.0
        for i in range(self.steps):
            self.sins.append(math.sin(radian))
            radian += step
        assert abs(self.sin(math.pi/4) - 1.0) <= .1

    def sin(self, radian):
        return(self.sins[int(radian * 2000) % self.steps])

    def calculate(self, data):
        t = self.tick
        (x, y, width, height, xx, yy) = data
        v = math.sin(x * 10 + t)
        v += math.sin((y * 10 + t) / 2.0)
        v += math.sin((x * 10 + y * 10 + t) / 2.0)
        cx = x + .5 * math.sin(t / 5.0)
        cy = y + .5 * math.cos(t / 3.0)
        v += math.sin(math.sqrt(100 * (cx * cx + cy * cy) + 1) + t)
        v /= 2.0

        # get to color up your life
        h = int(180 + math.sin(v) * 180)
        # s = int(50 + math.cos(v) * 50)
        color = pygame.Color(0, 0, 0, 255)
        color.hsla = (h, 100, 50, 50)
        self.array2d[xx][yy] = color
 
    def calculate2(self, data):
        t = self.tick
        (x, y, width, height, xx, yy) = data
        x10 = x * 10
        y10 = y * 10
        v = self.sin(x10 + t)
        v += self.sin((y10 + t) / 2.0)
        v += self.sin((x10 + y10 + t) / 2.0)
        cx = x + .5 * self.sin(t / 5.0)
        cy = y + .5 * self.sin(t / 3.0 + math.pi / 4)
        v += self.sin(math.sqrt(100 * (cx * cx + cy * cy) + 1) + t)
        v /= 2.0

        # get to color up your life
        h = int(180 + self.sin(v) * 180)
        # s = int(50 + math.cos(v) * 50)
        color = pygame.Color(0, 0, 0, 255)
        color.hsla = (h, 100, 50, 50)
        self.array2d[xx][yy] = color
 
    def update(self, **kwds):
        map(self.calculate2, self.data)
        pygame.surfarray.blit_array(self.surface, self.array2d)
        pygame.transform.scale(self.surface, self.parent.get_size(), self.parent) 
        self.tick += 5 * math.pi / 180
                

def main():
    try:
        surface = pygame.display.set_mode(RES)
        pygame.init()
        things = (
            Plasma(surface),
            )
        clock = pygame.time.Clock()       
        # mark pause state 
        pause = False
        # fill background
        surface.fill((0, 0, 0, 255))
        clicked = None
        running = True
        while True:
            # limit to FPS
            clock.tick(FPS)
            # Event Handling
            events = pygame.event.get()  
            for event in events:  
                if event.type == pygame.QUIT:  
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    clicked = Vec2d(mouseX, mouseY)
                elif event.type == pygame.MOUSEBUTTONUP:
                    clicked = None
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    running = False
                if keyinput[pygame.K_UP]:
                    viewer_distance += 1
                if keyinput[pygame.K_DOWN]:
                    viewer_distance -= 1
                if keyinput[pygame.K_PLUS]:
                    fov += .1
                if keyinput[pygame.K_MINUS]:
                    fov -= .1
                if keyinput[pygame.K_p]:
                    pause = not pause
                if keyinput[pygame.K_r]:
                    viewer_distance = 256
                    fov = 2
            # Update Graphics
            dirtyrects = []
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                for thing in things:
                    if type(thing) == Plasma:
                        thing.update(clicked=clicked)
                        continue
                    else:
                        dirtyrects.extend(thing.update())
                pygame.display.update()
                # pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == "__main__":
    import pstats
    import cProfile
    profile = "Plasma.profile"
    cProfile.runctx( "main()", globals(), locals(), filename=profile)
    s = pstats.Stats(profile)
    s.sort_stats('time')
    s.print_stats(1.0)
    os.unlink(profile)
