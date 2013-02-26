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
FPS = 50
# define background musicfile
BACKGROUND_MUSIC = "monkey_island_theme.mp3"

class FinishedException(Exception):

    def __init__(self, msg):
        self.msg = msg


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
            point = (int(x + self.direction[0]), int(y + math.sin(self.degree * x) * self.amplitude  + self.direction[1]))
            newpoints.append(point)
        self.points = newpoints
        self.draw()

    def draw(self):
        for point in self.points:
            self.surface.set_at(point, self.color)

class WormHole(GameObject):

    def __init__(self, surface, game_engine, color=(255, 255, 255)):
        GameObject.__init__(self, surface, game_engine)
        self.color = color
        self.middle = Vec2d(self.surface.get_width() / 2, self.surface.get_height() / 2)
        self.circles = []
        self.initialize()
        self.angle = 0

    def initialize(self):
        for index in range(10):
            circle = []
            first = Vec2d(20 * index * 1.2, 0)
            for degree in xrange(0, 360, 5):
                circle.append(first.rotated(degree))
            self.circles.append(circle)

    def run(self):
        angle = self.angle
        index = 1
        for circle in self.circles:
            origin = self.middle + Vec2d(10 * index * 1.2, 0).rotated(angle)
            for point in circle:
                point.rotate(5)
                draw_point = origin + point
                self.surface.set_at((int(draw_point.x), int(draw_point.y)), self.color)
            # rotate for next circle
            angle += 10
            index += 1 
        self.angle += 10
        #self.draw()

    def draw(self):
        pass

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
        self.game_objects.append(StarField(self.surface, self, direction=(1, 3), color=100, amplitude=2))
        self.game_objects.append(StarField(self.surface, self, direction=(2, 2), color=150, amplitude=1))
        self.game_objects.append(StarField(self.surface, self, direction=(3, 1), color=160, amplitude=2))
        self.game_objects.append(BouncingHline(self.surface, self, speed=1, color=255, amplitude=100, start=0))
        self.game_objects.append(BouncingHline(self.surface, self, speed=1, color=225, amplitude=99, start=5))
        self.game_objects.append(BouncingHline(self.surface, self, speed=1, color=205, amplitude=98, start=10))
        self.game_objects.append(BouncingHline(self.surface, self, speed=1, color=185, amplitude=97, start=15))
        self.game_objects.append(BouncingHline(self.surface, self, speed=1, color=165, amplitude=96, start=20))

    def delete(self, child, clicked):
        """deletes child from list"""
        for item in self.game_objects:
            if item == child:
                self.game_objects.remove(item)

class SetPalette(object):
    """simple sets palette"""

    def __init__(self, surface, palette):
        self.surface = surface
        self.palette = palette

    def run(self):
        self.surface.set_palette(self.palette)
        raise FinishedException("job done, delete me")

class FlashEffect(object):
    """Flashes Surface, fade all colors to white"""

    def __init__(self, surface, beat, repeat, amount):
        self.surface = surface
        self.beat = beat
        self.repeat = repeat
        self.amount = amount
        # current timestamp
        self.timestamp = time.time() + beat
        # how long will the surface be white
        self.flash_active = 0
        # white palette
        self.white = []
        for x in xrange(255):
            self.white.append((255, 255, 255))
        self.old_palette = None

    def run(self):
        if self.flash_active == 1:
            # reset to old palette
            self.surface.set_palette(self.old_palette)
            self.flash_active = 0
        elif self.flash_active > 0:
            # surface was flashed
            self.flash_active -= 1
        elif time.time() >= self.timestamp:
            # trigger for new flash was reached
            self.old_palette = self.surface.get_palette()
            self.surface.set_palette(self.white)
            self.timestamp = time.time() + self.beat
            # flash will last 5 Frames
            self.flash_active = 5
            self.amount -= 1
        if self.amount == 0:
            raise FinishedException("finished work, delete me")

class FadeEffect(object):
    """Flashes Surface, fade all colors to white"""

    def __init__(self, surface, counter=7):
        self.surface = surface
        self.palette = self.surface.get_palette()
        # fade to black in counter Frames
        self.counter = counter

    def run(self):
        newpalette = []
        for (red, green, blue) in self.surface.get_palette():
            red = int(red / 1.2)
            green = int(green / 1.2 )
            blue = int(blue / 1.2 )
            newpalette.append((red, green, blue))
        self.counter -= 1
        self.surface.set_palette(newpalette)
        print self.counter
        if self.counter == 0:
            raise FinishedException("finished work, delete me")

class TimeLine(object):
    """Controls Postprocessing Effects"""

    def __init__(self, surface):
        """just __init__"""
        self.surface = surface
        self.effects = []
        self.initialize()

    def update(self):
        try:
            effect = self.effects[0]
            try:
                effect.run()
            except FinishedException:
                print "%s ended" % effect.__class__.__name__
                del self.effects[0]
        except IndexError:
            print "No more effekts to do"
            pass

    def initialize(self):
        """generate list of effects"""
        self.effects.append(FlashEffect(self.surface, beat=2, repeat=True, amount=5))
        self.effects.append(FadeEffect(self.surface))
        self.effects.append(SetPalette(self.surface, PALETTE))
        self.effects.append(WormHole(self.surface, self, 255))


def ingame_loop(surface, game_engine, post_processor):
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
        surface.fill(0)
        # update everything
        pygame.display.set_caption("frame rate: %.2f frames per second" % CLOCK.get_fps())
        state = game_engine.update()
        post_processor.update()
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
    screen = pygame.display.set_mode(SCREEN, 0, 8)
    global PALETTE
    PALETTE = []
    for index in xrange(255):
        PALETTE.append((index, 0,0))
    old_palette = screen.get_palette()
    screen.set_palette(PALETTE)
    
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(BACKGROUND_MUSIC)
    pygame.mixer.music.play(-1) # endless background music

    while True:
        # main logic of game
        game_engine = GameEngine(screen, None)
        post_processor = TimeLine(screen)
        # start game loop
        state = ingame_loop(screen, game_engine, post_processor)
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
