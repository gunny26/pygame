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

def main():
    try:
        fps = 50
        frames = 0  # frame counter
        surface = pygame.display.set_mode((320, 200))
        pygame.init()
        clock = pygame.time.Clock()
        # cycle thru every efefcts set after 500 frames
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
            ], [
                effects[1],
                effects[2],
            ], [
                effects[2],
                effects[3],
            ], [
                effects[4],
                effects[3],
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
                for effect in scenes[frames // 500 % len(scenes)]:
                    effect.update()
                pygame.display.flip()
            frames += 1
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == '__main__':
    main()
