#!python
# coding: utf8

import pygame
from pygame.locals import *
import random


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
        self.__step_x = 29
        self.__step_y = 29

    def rect(self):
        return pygame.Rect(self.__x, self.__y, 29, 29)

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

    def rect(self):
        return pygame.Rect(self.__x, self.__y, 29, 29)

    def update(self, events):
        self.__seq_pos = self.__sequence.next()
        self.__time_left -= 1
        if self.__time_left == 0:
            print "Bomb explodes"

    def draw(self):
        self.__surface.blit(self.__spritemap[self.__seq_pos], (self.__x + 2, self.__y))


class Grid(object):

    def __init__(self, surface, x_width, y_width):
        self.__surface = surface
        self.__x_width = x_width
        self.__y_width = y_width
        self.__color = pygame.Color(255,255,255,0)

    def update(self, events):
        pass

    def draw(self):
        for x in range(0, self.__surface.get_width(), 29):
            pygame.draw.line(self.__surface, self.__color, (x, 0), (x, self.__surface.get_height()))
        for y in range(0, self.__surface.get_height(), 29):
            pygame.draw.line(self.__surface, self.__color, (0, y), (self.__surface.get_width(), y))

def _message_screen(screen, message):
    screen.fill((120,30,66))
    font = pygame.font.SysFont("Times New Roman",25)
    text_img = font.render(message, True, (255,255,255))
    middle_pos = (screen.get_width() / 2 - text_img.get_width() / 2, screen.get_height() / 2 - text_img.get_height() / 2)
    screen.blit(text_img, middle_pos)
    clock = pygame.time.Clock()
    while True:
        # maximal 40 fpsok
        clock.tick(10)
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
    _message_screen(screen, "press any key to start")

def winner(screen):
    _message_screen(screen, "you won, press any key to restart")

def looser(screen):
    _message_screen(screen, "you lost, press any key to restart")

def main(screen):
    head = screen.subsurface(0, 0, screen.get_width(), 29)
    bottom = screen.subsurface(0, screen.get_height() - 29, screen.get_width(), 29)
    game = screen.subsurface(0, 29, screen.get_width(), screen.get_height() - 2 * 29)
    pygame.display.set_caption("Emerald Mine")
    sprite_array = load_spritemap('Qnp2o.png')
    things = []
    bombs = []
    player = Player(game, sprite_array, (10*29, 10*29))
    things.append(player)
    things.append(Grid(game, 29, 29))
    for i in range(5):
        bomb = Bomb(game, sprite_array, (int(random.random() * 19) * 29, int(random.random() * 19) *29))
        things.append(bomb)
        bombs.append(bomb)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Times New Roman",25)
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
        # den Bildschirm mit einer Hintergrundfarbe füllen und so
        # gleichzeitig das alte Bild löschen
        screen.fill((120,30,66))
        ## Über die Gruppe alle Sprites updaten und dann blitten
        text_img = font.render("This is header line", True, (255,255,255))
        head.blit(text_img, (5,5))
        text_img = font.render("This is bottom line", True, (255,255,255))
        bottom.blit(text_img, (5,5))
        for thing in things:
            thing.update(events)
        for bomb in bombs:
            if bomb.rect().colliderect(player.rect()):
                print "player intersects with bomb, remove this bomb"
                bombs.remove(bomb)
                things.remove(bomb)
                print "there are %d bombs left" % len(bombs)
        if len(bombs) == 0:
            print "all bombs are removed, you win"
            return "winner"
        # is player on bomb
        for thing in things:
            thing.draw()
        # alles aufs Fenster flippen
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Emerald Mine")
    screen = pygame.display.set_mode((29 * 20, 29 * 20))
    welcome(screen)
    result = main(screen)
    if result == "winner":
        winner(screen)
    else:
        looser(screen)
