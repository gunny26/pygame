#!/usr/bin/python
import random
# non std modules
import pygame

FPS = 50
DIM = (320, 200)


class Particle(object):
    """ Paticle in 2D space """

    def __init__(self, surface: pygame.Surface, pos: pygame.Vector2, direction: pygame.Vector2, size: int, color: tuple):
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
        self.gravity = pygame.Vector2(0, 9.81 / FPS)  # force to the ground aka bottom side
        self.drag = pygame.Vector2(1.0, 0.999)  # decrease in speed per FPS

    def _bounce(self):
        """ bounce from surface borders """
        right = self.surface.get_width() - self.size
        left = self.size
        top = self.size
        bottom = self.surface.get_height() - self.size
        if self.pos.x > right:  # right border
            self.pos.x = right
            self.direction = self.direction.elementwise() * pygame.Vector2(-1.0, 1.0)
        elif self.pos.x < left:  # left border
            self.pos.x = left
            self.direction = self.direction.elementwise() * pygame.Vector2(-1.0, 1.0)
        if self.pos.y > bottom:  # bottom border
            self.pos.y = bottom
            self.direction = self.direction.elementwise() * pygame.Vector2(1.0, -1.0)
        elif self.pos.y < top:  # top border
            self.pos.y = top
            self.direction = self.direction.elementwise() * pygame.Vector2(1.0, -1.0)

    def _move(self):
        """ move particle in space """
        self.pos += self.direction  # add direction vector
        self.direction += self.gravity  # add gravity to direction
        self.direction = self.direction.elementwise() * self.drag  # apply drag to direction

    def update(self, **kwds):
        """ update every frame """
        self._bounce()
        self._move()
        pygame.draw.circle(self.surface, self.color, (int(self.pos.x), int(self.pos.y)), self.size, 1)


class Particles(object):

    def __init__(self, dim: tuple, count: int):
        """
        clas to draw some particles

        :param surface: surface to draw on
        :param count: number of particles
        """
        self.surface = pygame.Surface(dim)
        # initialize
        self.particles = []
        # initialize
        for counter in range(count):
            pos = pygame.Vector2(random.randint(0, self.surface.get_width()), random.randint(0, self.surface.get_height()))
            direction = pygame.Vector2(10 * (random.random() - 0.5), 10 * (random.random() - 0.5))
            color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
            size = 5 + random.randint(0, 10)
            particle = Particle(self.surface, pos, direction, size, color)
            self.particles.append(particle)

    def update(self):
        """
        update every frame
        """
        self.surface.fill(0)
        for particle in self.particles:
            particle.update()
        return self.surface

    def collide(self, p1, p2):
        """
        Collission detection and handling method

        :param p1: Vector2 of Particle 1
        :param p2: Vector2 of Particle 2
        """
        distance = p1.pos.distance(p2.pos)  # distance between to particles
        if distance.length() < (p1.size + p2.size):
            pass


def main():
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        things = (
            Particles(DIM, 20),
        )
        clock = pygame.time.Clock()
        # mark pause state
        pause = False
        # fill background
        surface.fill((0, 0, 0, 255))
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
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                for thing in things:
                    surface.blit(thing.update(), (0, 0))
                pygame.display.update()
    except (KeyboardInterrupt, pygame.error):
        pygame.quit()


if __name__ == '__main__':
    main()
