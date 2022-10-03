#!/usr/bin/python3
import sys
import math
# non std modules
import pygame
# own modules
from Lissajous import Lissajou
from RotatingLines import RotatingLines
from SinusText import SinusText
from ScrollText import ScrollText
from Fire import Fire
from CoffeeBean import CoffeeDraw
from SpiralText import SpiralText
from Starfield import Starfield
from Plasma import Plasma
from Particle import Particles
from Pendulum import Pendulums, Origin
# background effects
from PerlinNoise import PerlinNoise
from PlasmaFractal import PlasmaFractal
from PascalTriangle import PascalTriangle
from JuliaFractal import JuliaFractal
from SimpleBackgrounds import GradientBackground
from Spectrographs import SpectrumBar, SpectrumCircle
from Superformula import SuperformulaAnimation
from CircleArcs import ArcAnimation
from Interference import ColorInterference, CircleInterference
# some utilities
# from Vector import Vector
from RgbColorGradient import get_rgb_color_gradient


FPS = 50
DIM = (640, 400)
SIN = [math.sin(math.radians(degree)) for degree in range(0, 360, 1)]
PALETTE = get_rgb_color_gradient((50, 140, 70, 255), (240, 0, 70, 255), 256)


def main():
    try:
        frames = 0  # frame counter
        start_rgb = (255, 0, 0)
        target_rgb = (0, 255, 255)
        pygame.init()
        surface = pygame.display.set_mode(DIM)  # main foreground surface
        b_surface = pygame.Surface(DIM)  # surface to place bacground on
        # some music
        pygame.mixer.init()
        pygame.mixer.music.load("music/2019-01-10_-_Land_of_8_Bits_-_Stephen_Bennett_-_FesliyanStudios.com.mp3")
        pygame.mixer.music.play(-1)  # endless background music
        # synchronize with framerate
        clock = pygame.time.Clock()
        # pre initialize Backgrounds
        backgrounds = [
           # PerlinNoise(b_surface),
           # PlasmaFractal(b_surface),
           # PascalTriangle(b_surface, 4, 4, 60),
           JuliaFractal(DIM)
        ]
        for background in backgrounds:
            background.update()
        # pre initialize effects
        effects = [
            Lissajou(DIM, DIM, 100, 3, 1),
            RotatingLines(DIM, DIM, 100, 7, 0.9),
            SinusText(DIM, "Basic scrolling sinus text demo with pure python and pygame, woohooo...", 100, 20, 2, pygame.Color(0, 255, 255)),
            ScrollText(DIM, "Simple straight scrolling text", 150, pygame.Color(255, 255, 0)),
            Fire(DIM, pygame.Rect(0, 0, 320, 200), 4),
            Pendulums(DIM, (100, 0, 0), Origin((300, 300)), 5, 150),
            CoffeeDraw(DIM),
        ]
        scenes = [
            {
                "backgrounds": [
                    PascalTriangle(DIM, 4, 4, 60)
                ],
                "effects": [
                    effects[0],
                    effects[1],
                ]
            }, {
                 "backgrounds": [
                    PerlinNoise(DIM)
                ],
                "effects": [
                    effects[1],
                    effects[2],
                ]
            }, {
                "backgrounds" : [JuliaFractal(DIM)],
                "effects" : [
                    effects[2],
                    effects[3],
                ],
            }, {
                "backgrounds": [GradientBackground(DIM, start_rgb, target_rgb)],
                "effects": [
                    effects[4],
                    effects[3],
                ]
            }, {
                "backgrounds": [PlasmaFractal(DIM)],
                "effects": [
                    effects[5],
                    SpiralText(DIM, "vertical scroling text, goind up and up and up and ...", pygame.Color(0, 255, 255), 30, 2),
                ]
            }, {
                "backgrounds": [GradientBackground(DIM, start_rgb, target_rgb)],
                "effects": [
                    effects[5],
                    effects[3],
                ]
            }, {
                "backgrounds": [GradientBackground(DIM, (0, 0, 0), (128, 50, 50))],
                "effects": [Starfield(DIM, stars=100, depth=10, speed=0.01)],
            }, {
                "backgrounds": [SpectrumCircle(DIM, 44100)],
                "effects": [Starfield(DIM, stars=100, depth=10, speed=0.01)],
            }, {
                "backgrounds": [SpectrumBar(DIM, 44100)],
                "effects": [
                    Plasma(DIM),
                    ScrollText(DIM, "so, yeah thats not great, have to work on it", 150, pygame.Color(255, 255, 0))
                ]
            }, {
                "backgrounds" : [GradientBackground(DIM, start_rgb, target_rgb)],
                "effects": [
                    Particles(DIM, 10),
                    ScrollText(DIM, "some bouncing particles, basic physics", 150, pygame.Color(255, 255, 0))
                ]
            }, {
                "backgrounds" :[ColorInterference(DIM, PALETTE, SIN)],
                "effects": [
                    SuperformulaAnimation(DIM, pygame.Vector2(160, 120), 100, (255, 255, 255)),
                    ScrollText(DIM, "superformula in action", 180, PALETTE[-1])
                ]
            }, {
                "backgrounds" : [CircleInterference(DIM, PALETTE, SIN)],
                "effects": [
                    ArcAnimation(DIM, pygame.Vector2(160, 120), 100, (0x74, 0x54, 0x6a)),
                    ScrollText(DIM, "moving circle arcs", 180, PALETTE[0])
                ]
            }
        ]
        pause = False
        while True:
            clock.tick(FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            keyinput = pygame.key.get_pressed()
            if keyinput:
                if keyinput[pygame.K_ESCAPE]:
                    pygame.quit()
                    return
                if keyinput[pygame.K_SPACE]:
                    pause = not pause is True  # invert pause
            if not pause:
                surface.fill((0, 0, 0, 255))  # black out screen
                for background in scenes[frames // 500 % len(scenes)]["backgrounds"]:
                    # every background wil return surface object while calling udate()
                    surface.blit(background.update(), (0, 0), special_flags=pygame.BLEND_ADD)  # blit background surface on x=0, y=0
                for effect in scenes[frames // 500 % len(scenes)]["effects"]:
                    surface.blit(effect.update(), (0, 0), special_flags=pygame.BLEND_ADD)  # blit foreground
                pygame.display.flip()
            frames += 1
            pygame.display.set_caption("frame rate: %.2f frames per second" % clock.get_fps())
    except (KeyboardInterrupt, pygame.error):
        pygame.quit()

if __name__ == '__main__':
    main()
