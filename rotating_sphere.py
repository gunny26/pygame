#!/usr/bin/python

import pygame
import sys
import math
from Vec2d import Vec2d
from Vec3d import Vec3d

FPS = 50

def generator(start, stop, step):
    value = start
    while value <= stop:
        yield value
        value += step

def step_generator(start, stop, steps):
    distance = stop - start
    step = float(distance) / float(steps)
    value = float(start)
    while value <= stop:
        yield value
        value += step

class Sphere(object):
    """Object represents a cube of 6 faces, and 8 points"""

    def __init__(self, surface, color, center=Vec3d(0, 0, 0), size=Vec3d(1, 1, 1), steps=10.0):
        self.surface = surface
        self.color = color
        self.size = size
        self.center = center
        self.steps = steps
        # 20 circle
        self.sphere_raw_points = []
        self.generate()
        self.sphere_point = None
        self.sphere_transformed = None
        self.resize_and_center()

    def generate(self):
        radius = 0.0
        radius_angle = 0
        radius_step = float(math.pi / self.steps)
        for y in step_generator(-1, 1, self.steps):
            print y
            circle = []
            radius = math.sin(radius_angle)
            radius_angle += radius_step
            for angle in step_generator(0, 2 * math.pi, self.steps):
                print angle
                x = math.cos(angle) * radius
                z = math.sin(angle) * radius
                circle.append(Vec3d(x, y, z))
            self.sphere_raw_points.append(circle)
        

    def resize_and_center(self):
        self.sphere_points = []
        for circle in self.sphere_raw_points:
            new_circle = []
            for point in circle:
                new_circle.append(point * self.size + self.center)
            self.sphere_points.append(new_circle)

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
        self.transformed_sphere = []
        for circle in self.sphere_points:
            transformed_circle = []
            for point in circle:
                new_point = point.rotated_around_x(dx).rotated_around_y(dy).rotated_around_z(dz)
                transformed = new_point.project(surface.get_width(), surface.get_height(), 256, 4)
                transformed_circle.append((transformed.x + offset2d.x, transformed.y + offset2d.y))
            self.transformed_sphere.append(transformed_circle)
                
    def update(self, center):
        # draw every face of the cube
        for circle in self.transformed_sphere:
            pygame.draw.polygon(self.surface, self.color, circle, 1)
        for point_index in range(len(self.transformed_sphere[0])):
            points = []
            for circle_index in range(len(self.transformed_sphere)):
                points.append(self.transformed_sphere[circle_index][point_index])
            pygame.draw.polygon(self.surface, self.color, points, 1)


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
        spheres = ( 
            Sphere(surface, (100, 0, 0), Vec3d(-1.5, -1.5, -1.5), Vec3d(1, 1, 1)),
            Sphere(surface, (100, 0, 0), Vec3d(0, 0, 0), Vec3d(1, 1, 1)),
            Sphere(surface, (100, 0, 0), Vec3d(1.5, 1.5, 1.5), Vec3d(1, 1, 1)),
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
            for sphere in spheres:
                # rotate
                sphere.rotate(theta, theta, 0.0, Vec2d(0, 0), Vec3d(1,1,1))
                theta += step * 16
                # size wobbling
                # sphere.set_size(0.5 + math.sin(size_angle) * 0.125)
                color = cg.get_color()
                sphere.set_color(color)
                size_angle += size_angle_step
                # draw
                sphere.update((0, 0))
            pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'
