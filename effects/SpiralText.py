#!/usr/bin/python3
import math
# non std modules
import pygame


class SpiralText(object):
    """Text scrolling up in spiral, if text is long enough it look like 3D"""

    def __init__(self, surface: pygame.Surface, text: str, color: tuple, size: int = 30, speed: int = 1):
        """

        :param surface: <pygame.Surface> surface to draw on
        :param text: <str> String to render
        :param color: <tuple> in (r, g, b) color of text
        :param size: <int> size of font
        :param speed: <int> speed of rotation
        """
        self.surface = surface
        self.text = text
        self.color = color
        self.size = size
        self.speed = speed
        # set font to render
        self.font = pygame.font.SysFont("mono", self.size, bold=True)
        self.center = surface.get_width() // 2  # center of rotation
        self.width = surface.get_width() // 4  # width in left and right of center
        self.angle = 0  # starting angle
        self.characters = []  # individual character information
        # initial placing
        for index, character in enumerate(text):
            self.characters.append({
                "x": self.center + int(self.width * math.sin(math.radians(self.angle + 10 * index))),
                "y": surface.get_height() + 2 * index * size,
                "surface": self.font.render(character, True, self.color)
            })
        self.angle += 1

    def update(self):
        """ update every frame """
        # local variables to speed up
        center = self.center
        speed = self.speed
        height = self.surface.get_height()
        width = self.width
        angle = self.angle
        surface = self.surface
        # do the work
        for index, character in enumerate(self.characters):
            surface.blit(
                character["surface"],
                (character["x"], character["y"]),
            )
            character["x"] = center + int(width * math.sin(math.radians(angle + 10 * index)))
            if character["y"] > 0:
                character["y"] -= speed
            else:
                character["y"] = height
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
