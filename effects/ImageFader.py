#!/usr/bin/python
# flake8: E501
# non std modules
import pygame

FPS = 60
DIM = (320, 200)  # initial window size


class ImageFader:
    """ interfering colors """

    def __init__(self, dim):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.dim = dim
        self.surface = pygame.image.load(open("images/172133.png", "rb")).convert()
        print(self.surface.get_width(), self.surface.get_height())
        slices = 10  # number of vertical slices
        self.height = self.surface.get_height() // slices
        self.width = self.surface.get_width()
        self.s_surfaces = []
        for i in range(slices):
            # left top width height
            area_to_blit = (0, i * self.height, self.width, self.height)
            s_surface = self.surface.subsurface(area_to_blit).copy()
            self.s_surfaces.append(s_surface)
        self.framecount = 0

    def update(self):
        """ blit on background surface """
        direction = 1  # left or right
        for index, s_surface in enumerate(self.s_surfaces):
            self.surface.blit(s_surface, (0 + direction * self.framecount, index * self.height))
            direction *= -1  # toggle direction
        self.framecount += 1
        return self.surface


def main():
    try:
        pygame.display.init()  # only initialize display, no other modules
        surface = pygame.display.set_mode(DIM)
        effects = [
            ImageFader(DIM)
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
                if keyinput[pygame.K_f]:  # go to FULLSCREEN
                    pygame.display.quit()
                    pygame.display.init()
                    surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            if pause is not True:
                surface.fill((0, 0, 0))
                for background in effects:
                    b_surface = background.update()
                    pygame.transform.scale(b_surface, (surface.get_width(), surface.get_height()), surface)  # blit and scale to display
                pygame.display.flip()
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except KeyboardInterrupt:
        pygame.quit()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()

