#!/usr/bin/python3
""" foreground effect """
import random
# non std modules
import pygame
# own modules
from Vec3d import Vec3d


FPS = 50
DIM = (320, 200)


class Starfield(object):
    """ Starfield with 3D Points """

    def __init__(self, dim: tuple, stars: int, depth: int, speed: float = 0.01):
        """
        :param dim: dimension of surface
        :param stars: amount of stars to create
        :param depth: z axis depth from 0 to 0 + depth
        :param speed: how fast should stars travel
        """
        self.surface = pygame.Surface(dim)
        self.stars = stars
        self.depth = depth
        self.speed = speed
        # set initial variables
        self.color = pygame.Color(255, 255, 255, 255)
        # initialize array
        depth_count = self.stars / self.depth
        self.stars = []
        # generates 3d starfield in between z=0 to z=depth """
        for index in range(int(depth_count ** 3)):
            star_x = random.random() * 4 - 2
            star_y = random.random() * 4 - 2
            star_z = random.random() * 4 - 2
            self.stars.append(Vec3d(star_x, star_y, star_z))

    def update(self, fov: float = 3.0, viewer_distance: int = 256):
        """
        update every frame

        :param fov: field of view
        :param viewer_distance: z distance of viewer to screen
        """
        # local variables to speed up
        surface = self.surface
        surface.fill(0)
        width = surface.get_width()
        height = surface.get_height()
        color = self.color
        speed = self.speed
        p_array = pygame.PixelArray(surface)
        for star in self.stars:
            tstar = star.project(width, height, viewer_distance, fov)
            p_array[int(tstar.x) % width, int(tstar.y) % height] = color
            star.x -= speed
            if star.x < -2:
                star.x = 2
        p_array.close()
        return self.surface


def main():
    """main loop"""
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        effects = (
            Starfield(DIM, stars=100, depth=10, speed=0.01),
            )
        clock = pygame.time.Clock()
        # for 3d projection
        fov = 3.0
        viewer_distance = 256
        pause = False
        changed = False
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
                if keyinput[pygame.K_UP]:
                    viewer_distance += 1
                    changed = True
                if keyinput[pygame.K_DOWN]:
                    viewer_distance -= 1
                    changed = True
                if keyinput[pygame.K_PLUS]:
                    fov += .1
                    changed = True
                if keyinput[pygame.K_MINUS]:
                    fov -= .1
                    changed = True
                if keyinput[pygame.K_p]:
                    pause = not pause
                if keyinput[pygame.K_r]:
                    viewer_distance = 256
                    fov = 3.0
                    changed = True
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                for effect in effects:
                    surface.blit(effect.update(viewer_distance=viewer_distance, fov=fov), (0, 0))
                pygame.display.flip()
            if changed:  # if something has changed, print it
                print(f"fov      : {fov}")
                print(f"distance : {viewer_distance}")
                changed = False
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == "__main__":
    main()
