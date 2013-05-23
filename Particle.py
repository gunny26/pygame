#!/usr/bin/python

import pygame
from pygame import gfxdraw
import sys
import math
import random
import numpy
import time
from Vec2d import Vec2d
from Vec3d import Vec3d

FPS = 50


class Vector(object):
    """Vector Class represents length and angle"""

    def __init__(self, length, angle):
        self.length = length
        self.angle = angle

    def __add__(self, other):
        x  = math.sin(self.angle) * self.length + math.sin(other.angle) * other.length
        y  = math.cos(self.angle) * self.length + math.cos(other.angle) * other.length
        length = math.hypot(x, y)
        angle = 0.5 * math.pi - math.atan2(y, x)
        return(Vector(length, angle))
    __radd__ = __add__

    def __iadd__(self, other):
        x  = math.sin(self.angle) * self.length + math.sin(other.angle) * other.length
        y  = math.cos(self.angle) * self.length + math.cos(other.angle) * other.length
        self.length = math.hypot(x, y)
        self.angle = 0.5 * math.pi - math.atan2(y, x)
        return(self)

    def __mul__(self, other):
        return(Vector(self.length * other, angle))

    def __imul__(self, other):
        self.length *= other
        return(self)

    def bounce(self, tangent=0):
        """reverse direction"""
        self.angle = tangent - self.angle

    def addpos(self, position):
        """add position to current vector and returns new position"""
        x = position.x + math.sin(self.angle) * self.length
        y = position.y - math.cos(self.angle) * self.length
        return(Vec2d(x, y))

    @staticmethod
    def vector_between(pos1, pos2):
        """return vector between two points"""
        dx = (pos1.x - pos2.x)
        dy = (pos1.y - pos2.y)
        dist = math.hypot(dx, dy)
        theta = math.atan2(dy, dx)
        return(Vector(dist, theta))

    @staticmethod
    def distance_between(pos1, pos2):
        """return vector between two points"""
        dx = (pos1.x - pos2.x)
        dy = (pos1.y - pos2.y)
        dist = math.hypot(dx, dy)
        return(dist)

    @staticmethod
    def angle_between(pos1, pos2):
        """return vector between two points"""
        dx = (pos1.x - pos2.x)
        dy = (pos1.y - pos2.y)
        theta = math.atan2(dy, dx)
        return(theta)


class Particle(object):
    """Paticle like Object"""

    def __init__(self, surface, pos, size, color, direction, gravity, drag=0.999, elasticity=0.75, density=1):
        self.surface = surface
        self.pos = pos
        self.size = size
        self.color=color
        self.direction = direction
        self.gravity = gravity
        self.drag = drag
        self.elasticity = elasticity
        # density and mass
        self.density = 1
        self.mass = self.density * self.size ** 2
        # set color according to mass
        self.color = pygame.Color(200 - density * 10, 200 - density * 10, 255)
        # initialize things


    def bounce(self):
        width = self.surface.get_width()
        height = self.surface.get_height()
        # right border
        if self.pos.x > width - self.size:
            self.pos.x = 2*(width - self.size) - self.pos.x
            self.direction.bounce(0)
            self.direction *= self.elasticity
        # left border
        elif self.pos.x < self.size:
            self.pos.x = 2*self.size - self.pos.x
            self.direction.bounce(0)
            self.direction *= self.elasticity
        # lower border
        if self.pos.y > height - self.size:
            self.pos.y = 2*(height - self.size) - self.pos.y
            # TODO why
            self.direction.bounce(math.pi)
            #self.direction.angle = math.pi - self.direction.angle
            self.direction *= self.elasticity
        # upper border
        elif self.pos.y < self.size:
            self.pos.y = 2*self.size - self.pos.y
            # TODO why
            self.direction.bounce(math.pi)
            #self.direction.angle = math.pi - self.direction.angle
            self.direction *= self.elasticity

    def move(self):
        self.pos = self.direction.addpos(self.pos)
        # add gravity
        self.direction += self.gravity
        # add drag
        self.direction *= self.drag

    def update(self, **kwds):
        self.move()
        self.bounce()
        pygame.draw.circle(self.surface, self.color, Vec2d(int(self.pos.x), int(self.pos.y)), self.size, 1)

    def __repr__(self):
        return("Particle(%(surface)s, %(pos)s, %(size)s, %(color)s)" % self.__dict__)


class Particles(object):

    def __init__(self, surface, count):
        self.surface = surface
        self.count = count
        # initialize
        self.particles = []
        self.elasticity = 0.75
        self.drag = 0.999
        self.gravity = Vector(0.004, math.pi)
        self.initialize()

    def initialize(self):
        for counter in xrange(self.count):
            pos = Vec2d(random.randint(0, self.surface.get_width()), random.randint(0, self.surface.get_height()))
            color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
            size = 10 + random.randint(0, 20)
            speed = random.randint(0, 10)
            angle = random.uniform(0, math.pi * 2)
            density = random.randint(0, 20)
            self.particles.append(Particle(self.surface, pos, size, color, Vector(speed, angle), self.gravity, self.drag, self.elasticity, density))

    def update(self):
        for i, particle in enumerate(self.particles):
            particle.update()
            for other_particle in self.particles[i+1:]:
                self.collide(particle, other_particle)

    def collide(self, p1, p2):
        distance = Vector.distance_between(p1.pos, p2.pos)
        if distance < p1.size + p2.size:

            angle = Vector.angle_between(p1.pos, p2.pos) + 0.5 * math.pi
            total_mass = p1.mass + p2.mass

            p1.direction = Vector(p1.direction.length * (p1.mass - p2.mass) / total_mass, p1.direction.angle) \
                + Vector(2 * p2.direction.length * p2.mass / total_mass, angle)
            p2.direction = Vector(p2.direction.length * (p2.mass - p1.mass) / total_mass, p2.direction.angle) \
                + Vector(2 * p1.direction.length * p1.mass / total_mass, angle)
            p1.direction.length *= self.elasticity
            p2.direction.length *= self.elasticity

            tangent = Vector.angle_between(p1.pos, p2.pos)
            # bounce on tangent
            #p1.direction.bounce(2 * tangent)
            #p2.direction.bounce(2 * tangent)
            # change speed
            #(p1.direction.length, p2.direction.length) = (p2.direction.length, p1.direction.length) 
            #avoid sticky problem
            angle = 0.5 * math.pi + tangent
            overlap = 0.5 * (p1.size + p2.size - distance + 1)
            p1.pos.x += math.sin(angle) + overlap
            p1.pos.y -= math.cos(angle) + overlap
            p2.pos.x -= math.sin(angle) + overlap
            p2.pos.y += math.cos(angle) + overlap

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
        things = (
            Particles(surface, 20),
            )
        clock = pygame.time.Clock()       

        # mark pause state 
        pause = False
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
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                for thing in things:
                    if type(thing) == Particles:
                        thing.update()
                        continue
                    else:
                        thing.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'
