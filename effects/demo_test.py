#!/usr/bin/python3
import sys
import math
# non std modules
import pygame
# owm modules
from Lissajous import Lissajou
from RotatingLines import RotatingLines
from SinusText import SinusText
from ScrollText import ScrollText
from Fire import Fire
from CoffeeBean import CoffeeDraw
# background effects
from PerlinNoise import PerlinNoise
from PlasmaFractal import PlasmaFractal
from PascalTriangle import PascalTriangle
from JuliaFractal import JuliaFractal
from SimpleBackgrounds import GradientBackground

def main():
    try:
        fps = 50  # framerate maximum
        frames = 0  # frame counter
        width = 320  # width of display
        height = 200  # height of display
        start_rgb = (255, 0, 0)
        target_rgb = (0, 255, 255)
        surface = pygame.display.set_mode((width, height))  # main foreground surface
        b_surface = pygame.Surface((width, height))  # surface to place bacground on
        pygame.init()
        clock = pygame.time.Clock()
        # pre initialize Backgrounds
        backgrounds = [
           # PerlinNoise(b_surface),
           # PlasmaFractal(b_surface),
           # PascalTriangle(b_surface, 4, 4, 60),
           JuliaFractal((width, height))
        ]
        for background in backgrounds:
            background.update()
        # pre initialize effects
        effects = [
            Lissajou(surface, (160, 100), 100, 3, 1),
            RotatingLines(surface, (160, 100), 100, 7, 0.9),
            SinusText(surface, "Basic scrolling sinus text demo with pure python and pygame, woohooo...", 100, 20, 2, pygame.Color(0, 255, 255)),
            ScrollText(surface, "Simple straight scrolling text", 150, pygame.Color(255, 255, 0)),
            Fire(surface, pygame.Rect(0, 0, 320, 200), 4),
            CoffeeDraw(surface),
        ]
        scenes = [
            {
                "backgrounds": [
                    PascalTriangle((width, height), 4, 4, 60)
                ],
                "effects": [
                    effects[0],
                    effects[1],
                ]
            }, {
                 "backgrounds": [
                    PerlinNoise((width, height))
                ],
                "effects": [
                    effects[1],
                    effects[2],
                ]
            }, {
                "backgrounds" : [JuliaFractal((width, height))],
                "effects" : [
                    effects[2],
                    effects[3],
                ],
            }, {
                "backgrounds": [GradientBackground((width, height), start_rgb, target_rgb)],
                "effects": [
                    effects[4],
                    effects[3],
                ]
            }, {
                "backgrounds": [PlasmaFractal((width, height))],
                "effects": [
                    effects[5],
                ]
            }, {
                "backgrounds": [GradientBackground((width, height), start_rgb, target_rgb)],
                "effects": [
                    effects[5],
                    effects[3],
                ]
            }
        ]
        pause = False
        while True:
            clock.tick(fps)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput:
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit(1)
                if keyinput[pygame.K_SPACE]:
                    pause = not pause is True
            if not pause:
                surface.fill((0, 0, 0, 255))  # black out screen
                for background in scenes[frames // 500 % len(scenes)]["backgrounds"]:
                    # every background wil return surface object while calling udate()
                    surface.blit(background.update(), (0,0))  # blit background surface on x=0, y=0
                for effect in scenes[frames // 500 % len(scenes)]["effects"]:
                    effect.update()
                pygame.display.flip()
            frames += 1
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == '__main__':
    main()
