#!/usr/bin/python3
import sys
import pygame


FPS = 50
DIM = (320, 200)


class ScrollText(object):
    """Simple 2d Scrolling Text"""

    def __init__(self, dim: tuple, text: str, hpos: int, color: pygame.Color, size: int = 30):
        """
        (pygame.Surface) surface - surface to draw on
        (string) text - text to draw
        (int) hpos - horizontal position on y axis
        (pygame.Color) color - color of font
        (int) size - size of font
        """
        self.surface = pygame.Surface(dim)
        # prepend and append some blanks
        appendix = " " * (self.surface.get_width() // size)
        self.text = appendix + text + appendix
        self.hpos = hpos
        self.color = color
        self.size = size
        # initialize
        self.position = 0
        self.font = pygame.font.SysFont("mono", self.size, bold=True)
        self.text_surface = self.font.render(self.text, True, self.color)

    def update(self, hpos=None):
        """update every frame"""
        self.surface.fill(0)
        if hpos is not None:
            self.hpos = hpos
        self.surface.blit(
            self.text_surface,
            (0, self.hpos),
            (self.position, 0, self.surface.get_width(), self.size)
        )
        if self.position < self.text_surface.get_width():
            self.position += 3
        else:
            self.position = 0
        return self.surface


def main():
    try:
        pygame.display.init()
        pygame.font.init()
        surface = pygame.display.set_mode(DIM)
        effects = (
            ScrollText(DIM, "Dolor Ipsum Dolor uswef", 100, pygame.Color(255, 255, 0, 255)),
        )
        clock = pygame.time.Clock()
        pause = False
        while True:
            clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                if keyinput[pygame.K_ESCAPE]:
                    sys.exit(1)
            if pause is not True:
                surface.fill(0)
                for effect in effects:
                    surface.blit(effect.update(), (0, 0))
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()
