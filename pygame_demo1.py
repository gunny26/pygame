#!/usr/bin/python

# import the relevant libraries
import sys
import time
import pygame
import random
import os
import math
# from pygame.locals import *

# define screen size
SCREEN = (640, 480)
# control Frame Rate
CLOCK = pygame.time.Clock()
FPS = 50
# define background musicfile
BACKGROUND_MUSIC = "monkey_island_theme.mp3"


class Vector:

    def __init__(self, x, y, center_x, center_y):
        self.x = x
        self.y = y
        self.center_x = center_x
        self.center_y = center_y

    def rotate(self, angle_degrees):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = self.x * cos - self.y * sin
        y = self.x * sin + self.y * cos
        self.x = x
        self.y = y

    def rotate_around(self, angle_degrees, point_set):
        radians = math.radians(angle_degrees)
        cos = math.cos(radians)
        sin = math.sin(radians)
        x = (self.x + point_set[0]) * cos - (self.y + point_set[1]) * sin
        y = (self.x + point_set[0]) * sin + (self.y + point_set[1]) * cos
        self.x = x - point_set[0]
        self.y = y - point_set[1]

    def __len__(self):
        "to implement set features"
        return(2)

    def __getitem__(self, key):
        "to implement set features"
        if key == 0:
            return self.x + self.center_x
        elif key == 1:
            return self.y + self.center_y
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")

    def __setitem__(self, key, value):
        "to implement set features"
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")

    def __add__(self, point_set):
        self.x += point_set[0]
        self.y += point_set[1]

    def set_center(self, point_set):
        self.center_x = point[0]
        self.center_y = point[1]


class GameStat:
    """Holds game statistics"""

    def __init__(self):
        """ just __init__ """
        self.score = 0
        self.lifes = 50
        self.level = 1
        self.interval = 5
        self.maxtime = 50
        self.minchars = 3

class GameObject:
    """Controls Life of one GameObject"""

    def __init__(self, surface, game_engine):
        """just __init__"""
        self.surface = surface
        self.game_engine = game_engine
        self.size_x = random.randint(0,50)
        self.size_y = random.randint(0,50)
        self.speed = random.randint(-3, 3)
        self.center_x = random.random() * self.surface.get_width()
        self.center_y = random.random() * self.surface.get_height()
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.initialize()

    def update(self):
        """update every step"""
        self.move()

    def initialize(self):
        self.points = (
            Vector(self.size_x, self.size_y, self.center_x, self.center_y),
            Vector(-self.size_x, self.size_y, self.center_x, self.center_y),
            Vector(-self.size_x, -self.size_y, self.center_x, self.center_y),
            Vector(self.size_x, -self.size_y, self.center_x, self.center_y))
        
    def move(self):
        """rotate by step degrees and move"""
        for point in self.points:
            point.rotate(self.speed)
            point.rotate_around(self.speed, (self.surface.get_width() / 2, self.surface.get_height() / 2))
        pygame.draw.polygon(self.surface, self.color, self.points, 1)


class GameEngine:
    """Controls Life of many characters"""

    def __init__(self, surface, gamestat):
        """just __init__"""
        self.surface = surface
        self.gamestat = gamestat
        # create initial set of characters
        self.game_objects = []
        for i in range(200):
            self.generate()

    def update(self):
        """ handle all characters an generate more if to less on screen"""
        # update characters
        for game_object in self.game_objects:
            game_object.update()
        return("running")
        
    def generate(self):
        """ generates a new character and put it on the list """
        self.game_objects.append(GameObject(self.surface, self))

    def delete(self, child, clicked):
        """deletes child from list"""
        for item in self.game_objects:
            if item == child:
                self.game_objects.remove(item)


def grayscale_image(surface):
    darker = 0.5
    width, height = surface.get_size()
    for x in range(width):
        for y in range(height):
            red, green, blue, alpha = surface.get_at((x, y))
            L = (0.3 * red + 0.59 * green + 0.11 * blue) * darker
            gs_color = (L, L, L, alpha)
            surface.set_at((x, y), gs_color)
    return surface

def ingame_loop(surface, game_engine):
    """ main ingame loop """
    while True:
        events = pygame.event.get()  
        for event in events:  
            if event.type == pygame.QUIT:  
                sys.exit(0)
        keyinput = pygame.key.get_pressed()
        if keyinput is not None:
            # print keyinput
            if keyinput[pygame.K_ESCAPE]:
                return("lost")
        # sleep between every frame
        CLOCK.tick(FPS)
        # time.sleep( sleeptime__in_seconds )
        # blank screen
        surface.fill([100, 100, 100])
        # update everything
        state = game_engine.update()
        # state of engine could be
        # running
        # finished - player reached end of game
        # lost - player lost game
        if state != "running" :
            return(state)
        # update the screen to show the latest screen image
        pygame.display.update()

def main():
    """just __main__"""
    # this is where one sets how long the script
    # sleeps for, between frames.sleeptime__in_seconds = 0.05
    # initialise the display window
    screen = pygame.display.set_mode(SCREEN)
    pygame.init()
    #pygame.mixer.init()
    #pygame.mixer.music.load(BACKGROUND_MUSIC)
    #pygame.mixer.music.play(-1) # endless background music

    # object to hold game statistics
    gamestat = GameStat()
    while True:
        # main logic of game
        game_engine = GameEngine(screen, gamestat)
        # start game loop
        state = ingame_loop(screen, game_engine)
        # state could be
        # finished - player finished level
        # lost - player lost
        # if player click, restart will be true
        if state == "lost":
            sys.exit(0)
        elif state == "finished":
            sys.exit(0)

if __name__ == "__main__" :
    main()
