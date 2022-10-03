#!/usr/bin/python3
import sys

# non std modules
import pygame

# own modules
from Vec2d import Vec2d

DIM = (600, 600)
FPS = 50

class Origin(object):
    def __init__(self, center: Vec2d = Vec2d(0, 0)):
        """ sudo parent pendulum """
        self.center = center

    def get_pos(self):
        """ return position in float """
        return self.center

    def get_pos_i(self):
        """ return position in int """
        pos = self.get_pos()
        return Vec2d(int(pos[0]), int(pos[1]))


class Pendulum(object):
    """ a single pendulum """

    def __init__(
        self, radius: int, rot_speed: int, parent: object, start_angle: int = 0
    ):
        """
        radius - radius in pixels
        rot_speed - rotation speed in angle per iteration
        parent - parent pendulum
        start_angle - startin angle in degree
        """
        self.radius = radius  # radius
        self.parent = parent  # parent to get position from
        self.vector = Vec2d(radius, 0)  # 0-degrees
        self.rot_speed = rot_speed  # rotation speed in degree / iteration
        if start_angle:
            self.angle = start_angle  # parent to get position frome
            self.vector.rotate(start_angle)
        else:
            self.angle = 0
        self.center = parent.get_pos()  # origin position

    def get_pos(self) -> tuple:
        """ returning position of tip of pendulum """
        return self.parent.get_pos() + self.vector

    def get_pos_i(self) -> tuple:
        """ return integer position of tip of pendulum """
        pos = self.get_pos()
        return Vec2d(int(pos[0]), int(pos[1]))

    def update(self):
        """ update position, call this every iteration """
        self.vector.rotate(self.rot_speed)


class Pendulums(object):
    """ a bunch of pendulums """

    def __init__(
        self,
        dim: tuple,
        color: pygame.Color,
        origin=Origin(),
        num_pendulums=3,
        max_length=10,
    ):
        self.surface = pygame.Surface(dim)
        self.color = color
        self.origin = origin
        self.iteration = 0  # frame counter, to make some color effect
        parent = origin  # the initial origin
        self.pendulums = []
        for i in (2, 3, 7, 11, 17, 19, 29, 31, 37, 41, 47):
            pendulum = Pendulum(max_length // i, i, parent, 360 // i)
            self.pendulums.append(pendulum)
            parent = pendulum

    def update(self):
        """ update all positions, call this very iteration """
        self.surface.fill((0, 0, 0, 255))
        parent = self.origin
        for pendulum in self.pendulums:
            pendulum.update()
            pygame.draw.line(
                self.surface, self.color, parent.get_pos_i(), pendulum.get_pos_i()
            )
            parent = pendulum
        color = pygame.Color(
            (self.color[0] * self.iteration) % 255, self.color[1], self.color[2]
        )
        pygame.draw.circle(self.surface, color, self.pendulums[-1].get_pos_i(), 10, 1)
        self.iteration += 1
        return self.surface

    def get_pos(self) -> tuple:
        """ get position of least pendulum in float """
        return self.pendulums[-1].get_pos()

    def get_pos_i(self) -> tuple:
        """ get position of least pendulum in int """
        pos = self.get_pos()
        return Vec2d(int(pos[0]), int(pos[1]))


def test():
    """test"""
    try:
        surface = pygame.display.set_mode(DIM)  # main surface
        surface_path = pygame.Surface(DIM)  # only the path
        pygame.init()
        origin = Origin(Vec2d(300, 300))
        pendulums = Pendulums(DIM, (100, 0, 0), origin, 5, 150)
        clock = pygame.time.Clock()
        pause = False
        last_pos = None
        frame = 0  # frame counter
        path_color = (255, 100, 100)
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
                if keyinput[pygame.K_p]:
                    pause = not pause
            if pause is not True:

                surface.fill((0, 0, 0, 255))
                surface.blit(pendulums.update(), (0, 0), special_flags=pygame.BLEND_ADD)
                if last_pos is None:
                    last_pos = pendulums.get_pos_i()
                else:
                    # change color with frame counter
                    color = (
                        (path_color[0] + frame) % 255,
                        (path_color[1] + 2 * frame) % 255,
                        (path_color[2] + 4 * frame) % 255,
                    )
                    pygame.draw.line(
                        surface_path, color, last_pos, pendulums.get_pos_i()
                    )
                    last_pos = pendulums.get_pos_i()
                surface.blit(surface_path, (0, 0), special_flags=pygame.BLEND_ADD)
                pygame.display.flip()
                frame += 1

    except KeyboardInterrupt:
        print("shutting down")


if __name__ == "__main__":
    test()
