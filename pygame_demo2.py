#!/usr/bin/python

# import the relevant libraries
import sys
import time
import pygame
import random
import os
import math
# from pygame.locals import *
from Vec2d import Vec2d as Vec2d
from Vector2d import Vector2d as Vector2d

# define screen size
SCREEN = (640, 480)
# control Frame Rate
CLOCK = pygame.time.Clock()
FPS = 50000
# define background musicfile
BACKGROUND_MUSIC = "monkey_island_theme.mp3"


class GameObject(object):
    """Abstract class definition"""
    
    def __init__(self, surface, game_engine):
        self.surface = surface
        self.game_engine = game_engine

    def update(self):
        """update every step"""
        pass

    def initialize(self):
        """set initial state"""
        pass

    def move(self):
        """move something"""
        pass

    def draw(self):
        """draw on screen"""
        pass

class StarField(GameObject):

    def __init__(self, surface, game_engine, direction=(1, 0), color=(255, 255, 255), amplitude=10):
        GameObject.__init__(self, surface, game_engine)
        rand_x = [random.random() * self.surface.get_width() for x in xrange(200)]
        rand_y = [random.random() * self.surface.get_height() for y in xrange(200)]
        self.points = zip(rand_x, rand_y)
        self.color = color
        self.direction = direction
        self.amplitude = amplitude
        self.degree = math.pi / 360

    def update(self):
        newpoints = []
        for x, y in self.points:
            # boundary check
            if 0 > x : 
                x = self.surface.get_width()
            if x > self.surface.get_width() : 
                x = 0
            if 0 > y : 
                y = self.surface.get_height()
            if y > self.surface.get_height() : 
                y = 0
            # directioon
            point = (x + self.direction[0], y + math.sin(self.degree * x) * self.amplitude  + self.direction[1])
            newpoints.append(point)
        self.points = newpoints
        self.draw()

    def draw(self):
        for point in self.points:
            pygame.draw.line(self.surface, self.color, point, point)

class BouncingHline(GameObject):

    def __init__(self, surface, game_engine, speed, color=(255, 255, 255), amplitude=10, start=0):
        GameObject.__init__(self, surface, game_engine)
        self.color = color
        self.speed = speed
        self.amplitude = amplitude
        self.y = None
        self.degree = speed * math.pi / 360
        self.angle = start * self.degree

    def update(self):
        self.y = self.surface.get_height() / 2 + self.amplitude * math.sin(self.angle)
        self.angle += self.degree
        self.draw()

    def draw(self):
        pygame.draw.line(self.surface, self.color, (0, self.y), (self.surface.get_width(), self.y))


class RotatingLine(GameObject):
    
    def __init__(self, surface, game_engine):
        self.surface = surface
        self.game_engine = game_engine
        self.initialize()
        self.origin = Vec2d(self.surface.get_width() / 2, self.surface.get_height() /2)
        self.origin1 = Vec2d(self.surface.get_width() / 3, self.surface.get_height() /2)
        self.color = (255, 0, 0)
        self.vector = None
        self.initialize()

    def update(self):
        """update every step"""
        self.move()
        self.draw()

    def initialize(self):
        """set initial state"""
        self.vector = Vec2d(100, 0)
        self.diffvector = Vec2d(50, 0.1)

    def move(self):
        """move something"""
        self.vector.rotate(1)
        self.origin.rotate(1)
        self.origin1.rotate(3)

    def draw(self):
        """draw on screen"""
        pygame.draw.line(self.surface, self.color, self.origin, self.origin + self.vector)
        pygame.draw.line(self.surface, self.color, self.origin1, self.origin1 + self.vector.perpendicular())


class GameEngine(object):
    """Controls Life of many GameObjects"""

    def __init__(self, surface, gamestat):
        """just __init__"""
        self.surface = surface
        self.gamestat = gamestat
        # create initial set of character
        self.game_objects = []
        self.generate()

    def update(self):
        """ handle all characters an generate more if to less on screen"""
        # update characters
        for game_object in self.game_objects:
            game_object.update()
        return("running")
        
    def generate(self):
        """ generates a new character and put it on the list """
        self.game_objects.append(RotatingLine(self.surface, self))
        self.game_objects.append(StarField(self.surface, self, direction=(1, 3), color=(128, 128, 128), amplitude=2))
        self.game_objects.append(StarField(self.surface, self, direction=(2, 2), color=(200, 200, 200), amplitude=1))
        self.game_objects.append(StarField(self.surface, self, direction=(3, 1), color=(255, 255, 255), amplitude=2))
        self.game_objects.append(BouncingHline(self.surface, self, speed=1, color=(255, 0, 0), amplitude=100, start=0))
        self.game_objects.append(BouncingHline(self.surface, self, speed=1, color=(250, 0, 0), amplitude=99, start=5))
        self.game_objects.append(BouncingHline(self.surface, self, speed=1, color=(245, 0, 0), amplitude=98, start=10))
        self.game_objects.append(BouncingHline(self.surface, self, speed=1, color=(240, 0, 0), amplitude=97, start=15))
        self.game_objects.append(BouncingHline(self.surface, self, speed=1, color=(235, 0, 0), amplitude=96, start=20))

    def delete(self, child, clicked):
        """deletes child from list"""
        for item in self.game_objects:
            if item == child:
                self.game_objects.remove(item)


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
        pygame.display.set_caption("frame rate: %.2f frames per second" % CLOCK.get_fps())
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

    while True:
        # main logic of game
        game_engine = GameEngine(screen, None)
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
