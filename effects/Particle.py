#!/usr/bin/python
import sys
import math
import random
# non std modules
import pygame

FPS = 50

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        return Vector(self.x * other.x, self.y * other.y)

    def __imul__(self, other):
        self.x *= other.x
        self.y *= other.y
        return self

    def __div__(self, other):
        return Vector(self.x / other.x, self.y / other.y)

    def __idiv__(self, other):
        self.x /= other.x
        self.y /= other.y
        return self

    def distance(self, other):
        """ return distance between self and other """
        return Vector(other.x - self.x, other.y - self.x)

    def length(self):
        """ return lenght of vector """
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Particle(object):
    """ Paticle in 2D space """

    def __init__(self, surface:pygame.Surface, pos:Vector, direction:Vector, size:int, color:tuple):
        """
        a particle in 2D space

        :param surface: surface to draw on
        :param pos: position to set particle, center of particle
        :param size: size of particle
        :param color: color of particle
        :param direction: initial direction of particle in m/s aka pixel/frame
        :param gravity: gravity vector 9.81 m/s aka 9.81 pixel/frame
        :param drag: decrease in direction per frame 
        """
        self.surface = surface
        self.pos = pos  # initial position
        self.direction = direction  # move direction
        self.size = size
        self.color = color
        # garivty is 9.81 m/s
        self.gravity = Vector(0, 9.81 / FPS)  # force to the ground aka bottom side
        self.drag = Vector(1.0, 0.999)  # decrease in speed per FPS

    def _bounce(self):
        """ bounce from surface borders """
        right = self.surface.get_width() - self.size
        left = self.size
        top = self.size
        bottom = self.surface.get_height() - self.size
        if self.pos.x > right:  # right border
            self.pos.x = right
            self.direction *= Vector(-1.0, 1.0)
        elif self.pos.x < left:  # left border
            self.pos.x = left
            self.direction *= Vector(-1.0, 1.0)
        if self.pos.y > bottom:  # bottom border
            self.pos.y = bottom
            self.direction *= Vector(1.0, -1.0)
        elif self.pos.y < top:  # top border
            self.pos.y = top
            self.direction *= Vector(1.0, -1.0)

    def _move(self):
        """ move particle in space """
        self.pos += self.direction  # add direction vector
        self.direction += self.gravity  # add gravity to direction
        self.direction *= self.drag  # apply drag to direction

    def update(self, **kwds):
        """ update every frame """
        self._bounce()
        self._move()
        pygame.draw.circle(self.surface, self.color, (int(self.pos.x), int(self.pos.y)), self.size, 1)


class Particles(object):

    def __init__(self, surface:pygame.Surface, count:int):
        """
        clas to draw some particles

        :param surface: surface to draw on
        :param count: number of particles
        """
        self.surface = surface
        self.count = count
        # initialize
        self.particles = []
        self.elasticity = 0.1  # bounciness
        self.drag = 0.2  # speed of movement
        self.gravity = Vector(2.0, math.pi)  # gravity to the ground
        # initialize
        for counter in range(self.count):
            pos = Vector(random.randint(0, self.surface.get_width()), random.randint(0, self.surface.get_height()))
            direction = Vector(10 * (random.random() - 0.5), 10 * (random.random() - 0.5))
            color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
            size = 5 + random.randint(0, 10)
            particle = Particle(self.surface, pos, direction, size, color)
            self.particles.append(particle)

    def update(self):
        """
        update every frame
        """
        for particle in self.particles:
            particle.update()
        #for index, particle in enumerate(self.particles):
        #    for other_particle in self.particles[index+1:]:
        #        particle, other_particle)
        #return(dirtyrects)

    def collide(self, p1, p2):
        """
        Collission detection and handling method

        :param p1: Vec2d of Particle 1
        :param p2: Vec2d of Particle 2
        """
        distance = p1.pos.distance(p2.pos)  # distance between to particles
        if distance.length() < (p1.size + p2.size):
            pass
            # total_mass = p1.mass + p2.mass

            #p1.direction = Vector(p1.direction.length * (p1.mass - p2.mass) / total_mass, p1.direction.angle) \
            #    + Vector(2 * p2.direction.length * p2.mass / total_mass, angle)
            #p2.direction = Vector(p2.direction.length * (p2.mass - p1.mass) / total_mass, p2.direction.angle) \
            #    + Vector(2 * p1.direction.length * p1.mass / total_mass, angle)
            #p1.direction.length *= self.elasticity
            #p2.direction.length *= self.elasticity
#
            #tangent = Vector.angle_between(p1.pos, p2.pos)
            # bounce on tangent
            #p1.direction.bounce(2 * tangent)
            #p2.direction.bounce(2 * tangent)
            # change speed
            #(p1.direction.length, p2.direction.length) = (p2.direction.length, p1.direction.length)
            #avoid sticky problem
            #angle = 0.5 * math.pi + tangent
            #overlap = 0.5 * (p1.size + p2.size - distance + 1)
            #p1.pos.x += math.sin(angle) + overlap
            #p1.pos.y -= math.cos(angle) + overlap
            #p2.pos.x -= math.sin(angle) + overlap
            #p2.pos.y += math.cos(angle) + overlap


def main():

    try:
        surface = pygame.display.set_mode((320, 200))
        pygame.init()
        things = (
            Particles(surface, 20),
            )
        clock = pygame.time.Clock()
        # mark pause state
        pause = False
        # fill background
        surface.fill((0, 0, 0, 255))
        clicked = None
        while True:
            # limit to FPS
            clock.tick(FPS)
            # Event Handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
                if keyinput[pygame.K_p]:
                    pause = not pause
            # Update Graphics
            dirtyrects = []
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                for thing in things:
                    thing.update()
                pygame.display.update()
                # pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()

if __name__=='__main__':
    main()

