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
# backgrounds
from PerlinNoise import PerlinNoise
from JuliaFractal import JuliaFractal

def main():
    try:
        fps = 50
        frames = 0  # frame counter
        width = 320
        height = 200
        surface = pygame.display.set_mode((width, height))
        pygame.init()
        clock = pygame.time.Clock()
        # cycle thru every efefcts set after 500 frames
        background_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        backgrounds = [
            # PerlinNoise(background_surface).update(),
            JuliaFractal(background_surface).update()
        ]
        effects = [
            Lissajou(surface, (160, 100), 100, 3, 1),
            RotatingLines(surface, (160, 100), 100, 7, 0.9),
            SinusText(surface, "Basic scrolling sinus text demo with pure python and pygame, woohooo...", 100, 20, 2, pygame.Color(0, 255, 255)),
            ScrollText(surface, "Simple straight scrolling text", 150, pygame.Color(255, 255, 0)),
            Fire(surface, pygame.Rect(0, 0, 320, 200), 4),
            CoffeeDraw(surface),
        ]
        scenes = [
            [
                effects[0],
                effects[1],
                effects[5],
            ], [
                effects[1],
                effects[2],
                effects[5],
            ], [
                effects[2],
                effects[3],
                effects[5],
            ], [
                effects[4],
                effects[3],
                effects[5],
            ], [
                effects[5],
            ]
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
                surface.fill((0, 0, 0, 255))
                surface.blit(background_surface, (0, 0))
                for effect in scenes[frames // 500 % len(scenes)]:
                    effect.update()
                pygame.display.flip()
            frames += 1
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == '__main__':
    main()
