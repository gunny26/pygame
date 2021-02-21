#!/usr/bin/python3

import pygame
import sys
import time
# own modules
from Vec2d import Vec2d as Vec2d


class InfoRenderer(object):
    """Infobox to show some information like FPS"""

    def __init__(self, surface, color, pos, size):
        """
        (pygame.Surface) surface - surface to draw on
        (Vec2d) pos - position of text
        (int) size - size of font
        (pygame.Color) - color of font
        """
        self.surface = surface
        self.color = color
        self.pos = pos
        self.size = size
        # initialize
        self.font = pygame.font.SysFont('mono', self.size, bold=True)
        self.last_tick = time.time()

    def update(self, lines):
        """update every frame"""
        fps = 1 / (time.time()-self.last_tick)
        self.draw_text("Frames per second %f" % fps, offset=Vec2d(0, 0))
        counter = 1
        for line in lines:
            self.draw_text(line, offset=Vec2d(0, self.size * counter))
            counter += 1
        self.last_tick = time.time()

    def draw_text(self, text, offset):
        """Center text in window"""
        font_surface = self.font.render(text, True, self.color)
        self.surface.blit(font_surface, self.pos + offset)


def test():
    try:
        fps = 50
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        spheres = (
            InfoRenderer(surface, pygame.Color(0, 255, 0), pos=Vec2d(100, 100), size=10),
            )
        clock = pygame.time.Clock()
        fov = 0
        viewer_distance = 0
        pause = False
        while True:
            clock.tick(fps)
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
                for thing in spheres:
                    thing.update(lines=("viewer_distance : %f" % viewer_distance, "fov: %f" % fov, "use up/down/+/-"))
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == '__main__':
    test()

