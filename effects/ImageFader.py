#!/usr/bin/python
# flake8: E501
import random
# non std modules
import pygame

FPS = 50
DIM = (320, 200)  # initial window size


class ImageFaderHorizontal:
    """ interfering colors """

    def __init__(self, dim, filename, slices=10):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.dim = dim
        self.surface = pygame.image.load(open(filename, "rb")).convert()
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


class ImageFaderVertical:
    """ interfering colors """

    def __init__(self, dim, filename, slices=20):
        """
        (pygame.Surface) surface - surface to draw on
        """
        self.dim = dim
        self.surface = pygame.image.load(open(filename, "rb")).convert()
        print(self.surface.get_width(), self.surface.get_height())
        self.height = self.surface.get_height()
        self.width = self.surface.get_width() // slices
        self.s_surfaces = []
        for i in range(slices):
            # left top width height
            area_to_blit = (i * self.width, 0, self.width, self.height)
            s_surface = self.surface.subsurface(area_to_blit).copy()
            self.s_surfaces.append(s_surface)
        self.framecount = 0

    def update(self):
        """ blit on background surface """
        direction = 1  # left or right
        for index, s_surface in enumerate(self.s_surfaces):
            self.surface.blit(s_surface, (index * self.width, 0 + direction * self.framecount))
            direction *= -1  # toggle direction
        self.framecount += 1
        return self.surface


class ImageFaderDisappear:
    """ randomly black out image pixel by pixel """

    def __init__(self, dim, filename, pixels=1000):
        """
        :param dim: dimesion of surface to draw on
        :param filename: filanme of image to load
        :param pixel: how many pixel per frame to delete
        """
        self.dim = dim
        self.surface = pygame.image.load(open(filename, "rb")).convert()
        self.pixels = pixels
        self.frames_to_finish = self.surface.get_width() * self.surface.get_height() // pixels
        print(f"Fade will be finished in {self.frames_to_finish}")
        self.framecount = 0

    def update(self):
        """ blit on background surface """
        if self.framecount < self.frames_to_finish:
            height = self.surface.get_height()
            width = self.surface.get_width()
            with pygame.PixelArray(self.surface) as p_array:
                for pixel in range(self.pixels):
                    x = random.randint(0, width - 1)
                    y = random.randint(0, height - 1)
                    while p_array[x, y] == 0:
                        x += 1
                        y += 1
                        x %= width
                        y %= height
                    p_array[x, y] = 0
        else:
            print("Fade is finished")
        self.framecount += 1
        return self.surface


def main():
    try:
        pygame.display.init()  # only initialize display, no other modules
        surface = pygame.display.set_mode(DIM)
        effects = [
            ImageFaderHorizontal(DIM, "images/157042.png"),
            ImageFaderVertical(DIM, "images/157042.png"),
            ImageFaderDisappear(DIM, "images/157042.png")
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

