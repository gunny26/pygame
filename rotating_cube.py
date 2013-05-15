#!/usr/bin/python

import pygame
import sys
import math
from Vec2d import Vec2d
from Vec3d import Vec3d

FPS = 50

class Cube(object):
    """Object represents a cube of 6 faces, and 8 points"""

    def __init__(self, surface, color, center=Vec3d(0, 0, 0), size=Vec3d(1, 1, 1)):
        self.surface = surface
        self.color = color
        # 8 points, raw, should be constant
        self.raw_points = (
            Vec3d(-1, 1, -1),
            Vec3d(1, 1, -1),
            Vec3d(1, -1, -1),
            Vec3d(-1, -1, -1),
            Vec3d(-1, 1, 1), 
            Vec3d(1, 1, 1),
            Vec3d(1, -1, 1),
            Vec3d(-1, -1, 1),
            )
        self.points = None
        self.size = size
        self.center = center
        self.resize_and_center()
        # the 6 faces of the cube
        self.faces = (
            (0, 1, 2, 3), 
            (1, 5, 6, 2), 
            (4, 5, 6, 7), 
            (4, 0, 3, 7),
            (0, 1, 5, 4),
            (2, 3, 7, 6),)

    def resize_and_center(self):
         self.points = (
            self.raw_points[0] * self.size + self.center,
            self.raw_points[1] * self.size + self.center,
            self.raw_points[2] * self.size + self.center,
            self.raw_points[3] * self.size + self.center,
            self.raw_points[4] * self.size + self.center, 
            self.raw_points[5] * self.size + self.center,
            self.raw_points[6] * self.size + self.center,
            self.raw_points[7] * self.size + self.center,
            )

    def set_color(self, color):
        self.color = color

    def set_size(self, size=Vec3d(1, 1, 1)):
        self.size = size
        self.resize_and_center()

    def set_center(self, center=Vec3d(0, 0, 0)):
        self.center = center
        self.resize_and_center()

    def rotate(self, dx, dy, dz, offset2d=Vec2d(0,0), offset3d=Vec3d(0, 0, 0)):
        # rotate and project every point to 2d
        self.transformed = []
        for p3d in self.points:
            # rotating the cube
            np3d = p3d.rotated_around_x(dx).rotated_around_y(dy).rotated_around_z(dz)
            t = np3d.project(surface.get_width(), surface.get_height(), 256, 6)
            # add offset2d after rotating the cube
            self.transformed.append((t.x + offset2d.x, t.y + offset2d.y))

    def update(self, center):
        # draw every face of the cube
        for f in self.faces:
            # four lines for every face, some will, be double
            pygame.draw.aaline(self.surface, self.color, self.transformed[f[0]], self.transformed[f[1]])
            pygame.draw.aaline(self.surface, self.color, self.transformed[f[1]], self.transformed[f[2]])
            pygame.draw.aaline(self.surface, self.color, self.transformed[f[2]], self.transformed[f[3]])
            pygame.draw.aaline(self.surface, self.color, self.transformed[f[3]], self.transformed[f[0]])


class ColorGradient(object):


    def __init__(self, rstep, gstep, bstep):
        self.rstep = float(rstep)
        self.gstep = float(gstep)
        self.bstep = float(bstep)
        self.red = 0.0
        self.green = 0.0
        self.blue = 0.0
        self.degree = float(math.pi / 360)

    def get_color(self):
        self.red += 256 * math.sin(self.degree * self.rstep)
        self.green += 256 * math.sin(self.degree * self.gstep)
        self.blue += 256 * math.sin(self.degree * self.bstep)
        color = (self.red % 256, self.green % 256, self.blue % 256)
        return(color) 


class BackgroundGradient(object):


    def __init__(self, surface):
        self.surface = surface
        self.cg = ColorGradient(0.1, 0.1, 0.0)
        self.colors = []
        for y in xrange(self.surface.get_height()):
            self.colors.append(self.cg.get_color())

    def update(self):
        for y in xrange(self.surface.get_height()):
            pygame.draw.line(self.surface, self.colors[y], (0, y), (self.surface.get_width(), y))


if __name__=='__main__':

    try:
        surface = pygame.display.set_mode((600,600))
        pygame.init()
        origin = (surface.get_width() / 2, surface.get_height() / 2)
        theta = 1
        step = math.pi / 180
        center_x = surface.get_width() / 2
        center_y = surface.get_height() / 2
        # Cube( surface, color, center3d, size)
        cubes = (
            # Z = -2
            Cube(surface, (100, 0, 0), Vec3d(-2, -2, -2), Vec3d(1, 1, 1)),
            Cube(surface, (100, 100, 0), Vec3d(0, -2, -2), Vec3d(1, 1, 1)),
            Cube(surface, (200, 100, 0), Vec3d(2, -2, -2), Vec3d(1, 1, 1)),
            Cube(surface, (0, 200, 0), Vec3d(-2, 0, -2), Vec3d(1, 1, 1)),
            Cube(surface, (100, 200, 0), Vec3d(0, 0, -2), Vec3d(1, 1, 1)),
            Cube(surface, (100, 200, 0), Vec3d(2, 0, -2), Vec3d(1, 1, 1)),
            Cube(surface, (0, 200, 0), Vec3d(-2, 2, -2), Vec3d(1, 1, 1)),
            Cube(surface, (100, 200, 0), Vec3d(0, 2, -2), Vec3d(1, 1, 1)),
            Cube(surface, (100, 200, 0), Vec3d(2, 2, -2), Vec3d(1, 1, 1)),
            # Z = 0
            Cube(surface, (100, 0, 0), Vec3d(-2, -2, 0), Vec3d(1, 1, 1)),
            Cube(surface, (100, 100, 0), Vec3d(0, -2, 0), Vec3d(1, 1, 1)),
            Cube(surface, (200, 100, 0), Vec3d(2, -2, 0), Vec3d(1, 1, 1)),
            Cube(surface, (0, 200, 0), Vec3d(-2, 0, 0), Vec3d(1, 1, 1)),
            Cube(surface, (100, 200, 0), Vec3d(0, 0, 0), Vec3d(1, 1, 1)),
            Cube(surface, (100, 200, 0), Vec3d(2, 0, 0), Vec3d(1, 1, 1)),
            Cube(surface, (0, 200, 0), Vec3d(-2, 2, 0), Vec3d(1, 1, 1)),
            Cube(surface, (100, 200, 0), Vec3d(0, 2, 0), Vec3d(1, 1, 1)),
            Cube(surface, (100, 200, 0), Vec3d(2, 2, 0), Vec3d(1, 1, 1)),
            # Z = 2
            Cube(surface, (100, 0, 0), Vec3d(-2, -2, 2), Vec3d(1, 1, 1)),
            Cube(surface, (100, 100, 0), Vec3d(0, -2, 2), Vec3d(1, 1, 1)),
            Cube(surface, (200, 100, 0), Vec3d(2, -2, 2), Vec3d(1, 1, 1)),
            Cube(surface, (0, 200, 0), Vec3d(-2, 0, 2), Vec3d(1, 1, 1)),
            Cube(surface, (100, 200, 0), Vec3d(0, 0, 2), Vec3d(1, 1, 1)),
            Cube(surface, (100, 200, 0), Vec3d(2, 0, 2), Vec3d(1, 1, 1)),
            Cube(surface, (0, 200, 0), Vec3d(-2, 2, 2), Vec3d(1, 1, 1)),
            Cube(surface, (100, 200, 0), Vec3d(0, 2, 2), Vec3d(1, 1, 1)),
            Cube(surface, (100, 200, 0), Vec3d(2, 2, 2), Vec3d(1, 1, 1)),
            )
        clock = pygame.time.Clock()       
 
        size_angle = 0
        size_angle_step = math.pi / 720
        cg = ColorGradient(0.0, 0.05, 0.05)
        background_gradient = BackgroundGradient(surface)
        while True:
            clock.tick(FPS)
            events = pygame.event.get()  
            for event in events:  
                if event.type == pygame.QUIT:  
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    sys.exit(1)
                #if keyinput[pygame.K_z]:
                #    theta[2] += math.pi / 180
                #if keyinput[pygame.KMOD_SHIFT | pygame.K_z]:
                #    theta[2] -= math.pi / 180
                #if keyinput[pygame.K_x]:
                #    theta[0] += math.pi / 180
                #if keyinput[pygame.KMOD_SHIFT | pygame.K_x]:
                #    theta[0] -= math.pi / 180
                #if keyinput[pygame.K_y]:
                #    theta[1] += math.pi / 180
                #if keyinput[pygame.KMOD_SHIFT | pygame.K_y]:
                #    theta[1] -= math.pi / 180
                #if keyinput[pygame.K_UP]:
                #    camera[2] += 1
                #if keyinput[pygame.K_DOWN]:
                #    camera[2] -= 1
                #if keyinput[pygame.K_LEFT]:
                #    camera[0] += 1
                if keyinput[pygame.K_RIGHT]:
                    p3d.rotate_around_y(step)
                    theta += step
            surface.fill(0)
            background_gradient.update()
            for cube in cubes:
                # rotate
                cube.rotate(theta, theta, 0.0, Vec2d(0, 0), Vec3d(1,1,1))
                theta += 0.1
                # size wobbling
                cube.set_size(0.5 + math.sin(size_angle) * 0.125)
                color = cg.get_color()
                cube.set_color(color)
                size_angle += size_angle_step
                # draw
                cube.update((0, 0))
            pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'
        print address
