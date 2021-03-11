#!/usr/bin/python3
import sys
import time
# non std modules
import pygame


FPS = 50
DIM = (640, 400)


class InfoRenderer(object):
    """Infobox to show some information like FPS"""

    def __init__(self, dim: tuple, color: pygame.Color, pos: pygame.Vector2, size: int):
        """
        :param dim: dimesion of surface to draw on
        :param pos: position of text
        :param size: - size of font
        :param color: color of font
        """
        self.surface = pygame.Surface(dim)
        self.color = color
        self.pos = pos
        self.size = size
        # initialize
        self.font = pygame.font.SysFont('mono', self.size, bold=False)
        self.last_tick = time.time()

    def _draw_text(self, text, offset):
        """Center text in window"""
        font_surface = self.font.render(text, True, self.color)
        self.surface.blit(font_surface, self.pos + offset)

    def update(self, lines) -> pygame.Surface:
        """update every frame"""
        fps = 1 / (time.time()-self.last_tick)
        self._draw_text(f"Frames per second {fps}", offset=pygame.Vector2(0, 0))
        counter = 1
        for counter, line in enumerate(lines):
            self._draw_text(line, offset=pygame.Vector2(0, self.size * (counter+1)))
        self.last_tick = time.time()
        return self.surface


def main():
    try:
        pygame.display.init()
        surface = pygame.display.set_mode(DIM)
        pygame.init()
        spheres = (
            InfoRenderer(DIM, pygame.Color(0, 255, 0), pos=pygame.Vector2(100, 100), size=12),
            )
        clock = pygame.time.Clock()
        fov = 0
        viewer_distance = 0
        pause = False
        while True:
            clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
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
                    lines = [
                        f"viewer_distance : {viewer_distance}",
                        f"fov: {fov}",
                        "use up/down/+/-"
                    ]
                    surface.blit(thing.update(lines), (0, 0))
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == '__main__':
    main()

