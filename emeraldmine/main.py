#!python
# coding: utf8

import pygame
from pygame.locals import *
import random
import time

def load_spritemap(filename, width_count=15, height_count=12):
    sheet = pygame.image.load(filename) #Load the sheet
    print "loaded spritemap dimesion : %s / %s" % (sheet.get_width(), sheet.get_height())
    x_step = sheet.get_width() / width_count
    y_step = sheet.get_height() / height_count
    print "single sprite dimension %s x %s" % (x_step, y_step)
    sprite_array = []
    for y in range(0, sheet.get_height(), y_step):
        for x in range(0, sheet.get_width(), x_step):
            sheet.set_clip(pygame.Rect(x, y, x_step, y_step)) #Locate the sprite you want
            sprite = sheet.subsurface(sheet.get_clip())
            #print sprite.get_width(), sprite.get_height()
            sprite_array.append(sheet.subsurface(sheet.get_clip())) #Extract the sprite you want
            #backdrop = pygame.Rect(0, 0, SCREEN_X, SCREEN_Y) #Create the whole screen so you can draw on it
            #screen.blit(draw_me,backdrop) #'Blit' on the backdrop
    return sprite_array


class LoopSequence(object):

    def __init__(self, sequence):
        self.__sequence = sequence
        self.__position = 0

    def __iter__(self):
        return self

    def next(self):
        self.__position += 1
        if self.__position > (len(self.__sequence) - 1):
            self.__position = 0
        return self.__sequence[self.__position - 1]


class Player(object):

    left = LoopSequence(range(7, 12))
    right = LoopSequence(range(1, 5))
    up = LoopSequence(range(36, 40))

    def __init__(self, surface, spritemap, pos):
        self.__surface = surface
        self.__spritemap = spritemap
        self.__x = pos[0]
        self.__y = pos[1]
        self.__direction = 0
        self.__seq_pos = self.right.next()
        self.__step_x = TILE_SIZE
        self.__step_y = TILE_SIZE

    @property
    def rect(self):
        return pygame.Rect(self.__x, self.__y, TILE_SIZE, TILE_SIZE)

    def update(self, events):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.__x -= self.__step_x
                    self.__seq_pos = self.right.next()
                elif event.key == K_RIGHT:
                    self.__x += self.__step_x
                    self.__seq_pos = self.left.next()
                elif event.key == K_UP:
                    self.__y -= self.__step_y
                    self.__seq_pos = self.up.next()
                elif event.key == K_DOWN:
                    self.__y += self.__step_y
                    self.__seq_pos = self.up.next()
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_RIGHT):
                    self.x = 0
                elif event.key in (K_UP, K_DOWN):
                    self.y = 0
            #print self.__x, self.__y

    def draw(self):
        self.__surface.blit(self.__spritemap[self.__seq_pos], (self.__x + 2, self.__y + 2))


class Bomb(object):

    def __init__(self, surface, spritemap, pos):
        self.__surface = surface
        self.__spritemap = spritemap
        self.__x = pos[0]
        self.__y = pos[1]
        self.__sequence = LoopSequence(range(31, 36))
        self.__seq_pos = self.__sequence.next()
        self.__time_left = 100

    @property
    def time_left(self):
        return self.__time_left

    def add_time(self, value):
        self.__time_left += value

    @property
    def rect(self):
        return pygame.Rect(self.__x, self.__y, TILE_SIZE, TILE_SIZE)

    def update(self, events):
        self.__seq_pos = self.__sequence.next()
        if self.__time_left > 0:
            self.__time_left -= 1

    def draw(self):
        self.__surface.blit(self.__spritemap[self.__seq_pos], (self.__x + 2, self.__y))


class TimeBank(object):

    def __init__(self, surface, spritemap, pos):
        self.__surface = surface
        self.__spritemap = spritemap
        self.__x = pos[0]
        self.__y = pos[1]
        self.__sequence = LoopSequence(range(52, 53))
        self.__seq_pos = self.__sequence.next()
        self.__value = 100

    @property
    def value(self):
        return self.__value

    @property
    def rect(self):
        return pygame.Rect(self.__x, self.__y, TILE_SIZE, TILE_SIZE)

    def update(self, events):
        self.__seq_pos = self.__sequence.next()

    def draw(self):
        self.__surface.blit(self.__spritemap[self.__seq_pos], (self.__x + 2, self.__y))


class Grid(object):

    def __init__(self, surface, x_width, y_width):
        self.__surface = surface
        self.__x_width = x_width
        self.__y_width = y_width
        self.__color = pygame.Color(255, 255, 255, 0)

    def update(self, events):
        pass

    def draw(self):
        for x in range(0, self.__surface.get_width(), self.__x_width):
            pygame.draw.line(self.__surface, self.__color, (x, 0), (x, self.__surface.get_height()))
        for y in range(0, self.__surface.get_height(), self.__y_width):
            pygame.draw.line(self.__surface, self.__color, (0, y), (self.__surface.get_width(), y))


class Highscore(object):

    def __init__(self, surface):
        self.__surface = surface
        self.__score = 0
        #self.__font = pygame.font.SysFont("Times New Roman",25)
        self.__font = pygame.font.Font("fonts/Completely Nonsense.ttf", 25)

    @property
    def score(self):
        return self.__score

    def update(self, events):
        pass

    def add(self, thing):
        if isinstance(thing, Bomb):
            self.__score += 1

    def draw(self):
        text_img = self.__font.render("Score : %d" % self.__score, True, (255, 255, 255))
        self.__surface.blit(text_img, (5, 5))


class Status(object):

    def __init__(self, surface, things):
        self.__surface = surface
        self.__things = things
        self.__starttime = time.time()
        self.__font = pygame.font.Font("fonts/Completely Nonsense.ttf", 25)

    def update(self, events):
        pass

    def draw(self):
        number_bombs = len([thing for thing in self.__things if isinstance(thing, Bomb)])
        time_left = max([thing.time_left for thing in self.__things if isinstance(thing, Bomb)])
        duration = int(time.time() - self.__starttime)
        text_img = self.__font.render("Time : %d Bombs left : %s" % (time_left, number_bombs), True, (255, 255, 255))
        self.__surface.blit(text_img, (5, 5))


def _message_screen(screen, message):
    screen.fill((120,30,66))
    #font = pygame.font.SysFont("Times New Roman",25)
    font = pygame.font.Font("fonts/Completely Nonsense.ttf", 25)
    text_img = font.render(message, True, (255, 255, 255))
    middle_pos = (screen.get_width() / 2 - text_img.get_width() / 2, screen.get_height() / 2 - text_img.get_height() / 2)
    screen.blit(text_img, middle_pos)
    clock = pygame.time.Clock()
    while True:
        # maximal 40 fpsok
        clock.tick(1)
        # events bearbeiten
        events = pygame.event.get()
        for event in events:
        # um möglichst einfach Positionen für die Spielobjekte zu sammeln:
            if event.type == KEYDOWN:
                return
            if event.type == MOUSEBUTTONDOWN:
                print event.pos
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
        pygame.display.flip()

def welcome(screen):
    _message_screen(screen, "Catch the Bomb\npress any key to start")

def winner(screen):
    _message_screen(screen, "you won, press any key to restart")

def looser(screen):
    _message_screen(screen, "you lost, press any key to restart")

def timed_message(screen, message, duration):
    font = pygame.font.Font("fonts/CuppaJoe.ttf", 25)
    clock = pygame.time.Clock()
    while True:
        screen.fill((120,30,66))
        clock.tick(1)
        text_img = font.render("%s in %d" % (message, duration), True, (255, 255, 255))
        middle_pos = (screen.get_width() / 2 - text_img.get_width() / 2, screen.get_height() / 2 - text_img.get_height() / 2)
        screen.blit(text_img, middle_pos)
        pygame.display.flip()
        duration -= 1
        if duration == 0:
            return

def main(screen, num_bombs, num_timebanks):
    head = screen.subsurface(0, 0, screen.get_width(), TILE_SIZE)
    bottom = screen.subsurface(0, screen.get_height() - TILE_SIZE, screen.get_width(), TILE_SIZE)
    game = screen.subsurface(0, TILE_SIZE, screen.get_width(), screen.get_height() - 2 * TILE_SIZE)
    tiles_x = 20
    tiles_y = 18
    tiles = range(tiles_x * tiles_y)
    sprite_array = load_spritemap('gfx/Qnp2o.png')
    # generate universe of things
    things = []
    bombs = []
    player = Player(game, sprite_array, (10 * TILE_SIZE, 10 * TILE_SIZE))
    things.append(player)
    things.append(Grid(game, TILE_SIZE, TILE_SIZE))
    for i in range(num_bombs):
        pos = int(random.random() * len(tiles))
        x = (tiles[pos] % tiles_x) * TILE_SIZE
        y = (int(tiles[pos] / tiles_y)) * TILE_SIZE
        print "positioned BOMB at index %d position %s, %s" % (pos, x, y)
        bomb = Bomb(game, sprite_array, (x, y))
        things.append(bomb)
        bombs.append(bomb)
        tiles.remove(pos)
    for i in range(num_timebanks):
        pos = int(random.random() * len(tiles))
        x = (tiles[pos] % tiles_x) * TILE_SIZE
        y = (int(tiles[pos] / tiles_y)) * TILE_SIZE
        print "positioned TimeBank at index %d position %s, %s" % (pos, x, y)
        timebank = TimeBank(game, sprite_array, (x, y))
        things.append(timebank)
    highscore = Highscore(head)
    things.append(highscore)
    status = Status(bottom, things)
    things.append(status)
    clock = pygame.time.Clock()
    while True:
        # maximal 40 fpsok
        clock.tick(10)
        # events bearbeiten
        events = pygame.event.get()
        for event in events:
        # um möglichst einfach Positionen für die Spielobjekte zu sammeln:
            if event.type == MOUSEBUTTONDOWN:
                print event.pos
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
        # blank
        screen.fill((100, 100, 100))
        # update events
        for thing in things:
            thing.update(events)
        # collision detection and status updates
        for bomb in [thing for thing in things if isinstance(thing, Bomb)]:
            if bomb.time_left == 0:
                print "bomb at %s explodes" % str(bomb.rect)
                bombs.remove(bomb)
                things.remove(bomb)
            if bomb.rect.colliderect(player.rect):
                print "player intersects with bomb at %s, remove this" % str(bomb.rect)
                highscore.add(bomb)
                bombs.remove(bomb)
                things.remove(bomb)
                print "there are %d bombs left" % len(bombs)
        for timebank in [thing for thing in things if isinstance(thing, TimeBank)]:
            if timebank.rect.colliderect(player.rect):
                print "player intersects with timebank at %s, remove this" % str(bomb.rect)
                [bomb.add_time(timebank.value) for bomb in things if isinstance(bomb, Bomb)]
                things.remove(timebank)
        if len(bombs) == 0:
            print "all bombs are removed, score %s " % highscore.score
            if highscore.score == num_bombs:
                return "winner"
            else:
                return "looser"
        # draw everything
        for thing in things:
            thing.draw()
        # flip
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("catch the bombs")
    TILE_SIZE = 29
    TILES_X = 20
    TILES_Y = 20
    size = (TILE_SIZE * TILES_X, TILE_SIZE * TILES_Y)
    print "screen size %s" % str(size)
    screen = pygame.display.set_mode(size)
    welcome(screen)
    num_bombs = 5
    num_timebanks = 5
    timed_message(screen, "Get ready for start", 5)
    result = main(screen, num_bombs, num_timebanks)
    while result == "winner":
        winner(screen)
        timed_message(screen, "Get Ready for next level", 5)
        num_bombs += 1
        num_timebanks -= 1
        result = main(screen, num_bombs, num_timebanks)
    looser(screen)
