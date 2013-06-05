#!/usr/bin/python

import pygame
import sys
import math
from Vec2d import Vec2d
from Vec3d import Vec3d

class Cube(object):
    """Object represents a cube of 6 faces, and 8 points"""

    def __init__(self, surface, color, center=Vec3d(0, 0, 0), size=Vec3d(1, 1, 1)):
        """
        (pygame.Surface) surface - surface to draw on
        (pygame.Color) color - color of cube
        (Vec3d) center - center of cube
        (Vec3d) size - size of cube
        """
        self.surface = surface
        self.color = color
        self.center = center
        self.size = size
        # initialize
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
        self.transformed = None
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
        """bring cube to size"""
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
        """set color"""
        self.color = color

    def set_size(self, size):
        """set size and resize cube"""
        self.size = size
        self.resize_and_center()

    def set_center(self, center):
        """set center and recenter cube"""
        self.center = center
        self.resize_and_center()

    def rotate(self, dx, dy, dz, offset2d=Vec2d(0, 0)):
        """rotate and project every point to 2d"""
        self.transformed = []
        for p3d in self.points:
            # rotating the cube
            np3d = p3d.rotated_around_x(dx).rotated_around_y(dy).rotated_around_z(dz)
            t = np3d.project(self.surface.get_width(), self.surface.get_height(), 256, 6)
            # add offset2d after rotating the cube
            self.transformed.append((t.x + offset2d.x, t.y + offset2d.y))

    def update(self):
        """draw every face of the cube every frame"""
        for f in self.faces:
            # four lines for every face, some will, be double
            pygame.draw.aaline(self.surface, self.color, self.transformed[f[0]], self.transformed[f[1]])
            pygame.draw.aaline(self.surface, self.color, self.transformed[f[1]], self.transformed[f[2]])
            pygame.draw.aaline(self.surface, self.color, self.transformed[f[2]], self.transformed[f[3]])
            pygame.draw.aaline(self.surface, self.color, self.transformed[f[3]], self.transformed[f[0]])


def test():
    try:
        fps = 40
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        theta = 1
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
        background_gradient = GradientBackground(surface)
        while True:
            clock.tick(fps)
            events = pygame.event.get()  
            for event in events:  
                if event.type == pygame.QUIT:  
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    sys.exit(1)
            surface.fill(0)
            background_gradient.update()
            for cube in cubes:
                # rotate
                cube.rotate(theta, theta, 0.0, Vec2d(0, 0))
                theta += 0.1
                # size wobbling
                cube.set_size(0.5 + math.sin(size_angle) * 0.125)
                size_angle += size_angle_step
                # draw
                cube.update()
            pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'

if __name__ == '__main__':
    from GradientBackground import GradientBackground as GradientBackground
    test()

