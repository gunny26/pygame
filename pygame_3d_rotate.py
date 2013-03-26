#!/usr/bin/env python2

import pygame
import sys
import string
import time
import numpy
import math


class vec3d(object):

    def __init__(self, x, y, z):
        self.array = numpy.array((x, y, z))

    def project(self, camera, theta, viewer):
        """
        camera numpy.array((x, y, z))
        theta is numpy.array((tx, ty, tz))
        viewer numpy.array((x, y, z))
        """
        cos = math.cos
        sin = math.sin
        print "self", self.array
        print "camera", camera
        print "theta", theta
        print "viewer", viewer
        m1 = numpy.array((
            (1, 0, 0),
            (0, cos(theta[0]), -sin(theta[0])),
            (0, sin(theta[0]), cos(theta[0]))
            ))
        m2 = numpy.array((
            (cos(theta[1]), 0, sin(theta[1])),
            (0, 1, 0),
            (-sin(theta[1]), 0, cos(theta[1]))
            ))
        m3 = numpy.array((
            (cos(theta[2]), -sin(theta[2]), 0),
            (sin(theta[2]), cos(theta[2]), 0),
            (0, 0, 1)
            ))
        d = m1.dot(m2.dot(m3.dot((self.array - camera))))
        print d
        bx = (d[0] - viewer[0]) * (viewer[2] / d[2])
        by = (d[1] * viewer[1]) * (viewer[2] / d[2])
        return(bx, by)

if __name__=='__main__':

    try:
        surface = pygame.display.set_mode((600,600))
        pygame.init()
        v = vec3d(100.0, 100.0, 100.0)
        origin = (surface.get_width() / 2, surface.get_height() / 2)
        theta = numpy.array((0.0, 0.0, 0.0))
        camera = numpy.array((0.0, 0.0, -50.0))
        while True:
            events = pygame.event.get()  
            for event in events:  
                if event.type == pygame.QUIT:  
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    sys.exit(1)
                if keyinput[pygame.K_z]:
                    theta[2] += math.pi / 180
                if keyinput[pygame.KMOD_SHIFT | pygame.K_z]:
                    theta[2] -= math.pi / 180
                if keyinput[pygame.K_x]:
                    theta[0] += math.pi / 180
                if keyinput[pygame.KMOD_SHIFT | pygame.K_x]:
                    theta[0] -= math.pi / 180
                if keyinput[pygame.K_y]:
                    theta[1] += math.pi / 180
                if keyinput[pygame.KMOD_SHIFT | pygame.K_y]:
                    theta[1] -= math.pi / 180
                if keyinput[pygame.K_UP]:
                    camera[2] += 1
                if keyinput[pygame.K_DOWN]:
                    camera[2] -= 1
                if keyinput[pygame.K_LEFT]:
                    camera[0] += 1
                if keyinput[pygame.K_RIGHT]:
                    camera[0] -= 1
            surface.fill(0)
            pygame.draw.line(surface, (0, 100, 100), origin, (100, 100))
            (x, y) = v.project(camera, theta, camera) 
            print (x, y)
            pygame.draw.line(surface, (0, 100, 100), origin, (x, y))
            pygame.display.update()
    except KeyboardInterrupt:
        print 'shutting down'
