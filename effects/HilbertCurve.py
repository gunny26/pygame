#!/usr/bin/python3
import math
# non std modules
import pygame


FPS = 60
DIM = (600, 600)


class HilbertCurve(object):
    """ Basic Hilbert Curve Algorithm """

    def __init__(self, dim:tuple, iteration: int = 8, length: int = 6):
        """
        good to use for background, not really an animation
        best used with quadratic dimension

        :param dim: dimension of surface to draw on
        :param iteration: how many iterations to calculate
        :param length: length of individual segment
        """
        self.surface = pygame.Surface(dim)
        # Which iteration of the Hilbert curve to draw
        self.iteration = iteration
        # Length of each line in the Hilbert curve
        self.length = length
        self.pos = pygame.Vector2(self.surface.get_width(), 0)
        self.color = pygame.Color(238, 255, 0)
        self.angle = 0
        self.leftHilbert(self.iteration, self.length)

    def forward(self, distance):
        myangle = math.radians(self.angle)  # convert to radians
        dest = self.pos + pygame.Vector2(int(math.cos(myangle)), int(math.sin(myangle))) * (-distance)
        pygame.draw.line(self.surface, self.color, self.pos, dest)
        self.pos = dest

    def right(self, angle):
        self.angle -= angle

    def left(self, angle):
        self.right(-angle)

    def leftHilbert(self, l, w):
        if l == 0:
            return
        self.right(90)
        self.rightHilbert(l - 1, w)
        self.forward(w)
        self.left(90)
        self.leftHilbert(l - 1, w)
        self.forward(w)
        self.leftHilbert(l - 1, w)
        self.left(90)
        self.forward(w)
        self.rightHilbert(l - 1, w)
        self.right(90)

    def rightHilbert(self, l, w):
        if l == 0:
            return
        self.left(90)
        self.leftHilbert(l - 1, w)
        self.forward(w)
        self.right(90)
        self.rightHilbert(l - 1, w)
        self.forward(w)
        self.rightHilbert(l - 1, w)
        self.right(90)
        self.forward(w)
        self.leftHilbert(l - 1, w)
        self.left(90)

    def update(self):
        return self.surface


def main():
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        pygame.init()
        effects = [
            HilbertCurve(DIM)
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
                surface.fill((0, 0, 0, 255))
                for effect in effects:
                    surface.blit(effect.update(), (0, 0))
                pygame.display.flip()
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == "__main__" :
    main()
