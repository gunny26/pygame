#!/usr/bin/python3
import random
import math
# non std modules
import pygame

class SpiralText(object):
    """Text scrlling up in spiral, if text is long enougth"""

    def __init__(self, surface, text, color, size=30, speed=1):
        """
        (pygame.Surface) surface to draw on
        (string) text - text to draw
        (int) hpos - horizontal position on y axis
        (int) amplitude - amplitude of sinus wave
        (int) frequency - frequency of sinus wave
        (pygame.Color) color - color of font
        (int) size - size of font
        """
        self.surface = surface
        self.text = text
        self.color = color
        self.size = size
        self.speed = speed
        self.font = pygame.font.SysFont("mono", self.size, bold=True)
        self.characters = []
        self.center = surface.get_width() // 2
        self.width = surface.get_width() // 4
        self.angle = 0
        for index, character in enumerate(self.text):
            self.characters.append({
                "x": self.center + int(self.width * math.sin(math.radians(self.angle + 10 * index))),
                "y": surface.get_height() + 2 * index * size,
                "surface": self.font.render(character, True, self.color)
            })
        self.angle += 1


    def update(self):
        """
        update every frame
        (int)hpos y axis offset
        """
        for index, character in enumerate(self.characters):
            self.surface.blit(
                character["surface"],
                (character["x"], character["y"]),
            )
            character["x"] = self.center + int(self.width * math.sin(math.radians(self.angle + 10 * index)))
            if character["y"] > 0 :
                character["y"] -= self.speed
            else:
                character["y"] = self.surface.get_height()
        self.angle += 1


def main():
    try:
        fps = 50
        surface = pygame.display.set_mode((600, 600))
        pygame.init()
        effects = [
            SpiralText(surface, "vertical scroling text, goind up and up and up and ...", pygame.Color(0, 255, 255), 30, 2)
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
