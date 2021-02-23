#!/usr/bin/python3
""" foreground effect """
import math
# non std modules
import pygame


class SinusText(object):
    """Sinus wave scroll text"""

    def __init__(self, surface: pygame.Surface, text: str, hpos: int, amplitude:int, frequency:int, color: tuple, size: int = 30):
        """
        :param surface: surface to draw on
        :param text: text to draw
        :param hpos: horizontal position on y axis
        :param amplitude: amplitude of sinus wave
        :param frequency: frequency of sinus wave
        :param color: color of font
        :param size: size of font
        """
        self.surface = surface
        # prepend an append some spaces
        appendix = " " * (self.surface.get_width() // size)
        self.text = appendix + text + appendix
        self.hpos = hpos
        self.amplitude = amplitude
        self.frequency = frequency
        self.color = color
        self.size = size
        # position in rendered string
        self.position = 0
        # generate initial position
        self.font = pygame.font.SysFont("mono", self.size, bold=True)
        self.text_surface = self.font.render(self.text, True, self.color)

    def update(self, hpos=None):
        """
        update every frame
        :param hpos: set new horizontal position
        """
        if hpos is not None:
            self.hpos = hpos
        for offset in range(self.text_surface.get_width()):
            self.surface.blit(
                self.text_surface,
                (0 + offset, self.hpos + int(math.sin(math.radians(offset * self.frequency)) * self.amplitude)),
                (self.position + offset, 0, 1, self.size)
            )
        if self.position < self.text_surface.get_width():
            self.position += 3
        else:
            self.position = 0


def main():
    try:
        fps = 50
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        effects = [
            SinusText(surface, "Basis scrolling sinus text demo with pure python and pygame, woohooo...", 200, 30, 2, pygame.Color(0, 255, 255))
            ]
        clock = pygame.time.Clock()
        pause = False
        while True:
            clock.tick(fps)
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
                    effect.update()
                pygame.display.flip()
    except KeyboardInterrupt:
        pygame.quit()


if __name__ == '__main__':
    main()
