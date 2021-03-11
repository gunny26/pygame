#!/usr/bin/python
import math
# non std modules
import pygame


FPS = 50
DIM = (320, 200)


def get_circle_points(radius, freq_x, freq_y, center):
    """
    return list of points form 0 to 360 degrees

    :param radius: in pixel
    :param freq_x: frequency factor in x direction
    :param freq_y: frequency factor in y direction
    :param center: tuple (x, y)
    """
    points = []
    step = math.pi / 180.0  # degree to radians
    for degree in range(0, 360):
        radians = step * degree
        x = math.cos(radians * freq_x) * radius
        y = math.sin(radians * freq_y) * radius
        points.append((center[0] + x, center[1] + y))
    return points


class MorphingPixels:
    """ Morph/move point in a set to another place """

    def __init__(self, dim: tuple, color=(255, 255, 255, 255)):
        """
        :param dim: <tuple> dimension of surface to draw on like (x, y)
        """
        self.surface = pygame.Surface(dim)
        self.color = color
        self.objects = [
            # object 1 - circle
            get_circle_points(100, 1.0, 1.0, (80, 100)),
            # object 2 - lissajous
            get_circle_points(100, 2.0, 4.0, (240, 100))
        ]
        # actual working set
        self.points = list(self.objects[0])
        self.framecount = 0

    def update(self):
        """ draw something """
        self.surface.fill((0, 0, 0))
        target = self.objects[1]  # object to morph to
        max_distance = 0  # holding maximum distance of any point
        for index in range(len(self.points)):
            source_v = pygame.Vector2(*self.points[index])
            target_v = pygame.Vector2(*target[index])
            direction = target_v - source_v  # vector from source to target
            max_distance = max(max_distance, direction.length())  # maximum distance of any point
            if direction.length():  # otherwise this point is finished
                point = source_v + direction.normalize()  # move by length=1
                self.points[index] = list(point)
        if max_distance <= 1.0:  # move back if target is reached
            self.objects.reverse()
            self.points = list(self.objects[0])
        pygame.draw.polygon(self.surface, self.color, self.points, 1)
        self.framecount += 1
        return self.surface


def main():
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        backgrounds = [
            MorphingPixels(DIM)
        ]
        clock = pygame.time.Clock()
        pause = False
        while True:
            clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
            if pause is not True:
                surface.fill((0, 0, 0))
                for background in backgrounds:
                    surface.blit(background.update(), (0, 0))
                pygame.display.flip()
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()
