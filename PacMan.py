#!/usr/bin/python

import pygame
import sys

FPS = 10
TILESIZE = 20
RES = (800, 425)

class GameObjects(object):

    def __init__(self, surface):
        self.surface = surface
        self.things = []

    def add(self, game_object):
        self.things.append(game_object)

    def remove(self, game_object):
        self.things.remove(game_object)

    def has(self, game_object):
        return(self.things.has(game_object))

    def empty(self):
        self.things = []

    def objects(self):
        return(self.things)

    def others(self, game_object):
        others = []
        for thing in self.things:
            if thing != game_object:
                others.append(thing)
        return(others)

    def update(self, events):
        for thing in self.things:
            thing.update(events)
            thing.move(self.others(thing))
            thing.draw(self.surface)

    def collide(self, rect, remove=False):
        collision = False
        for thing in self.things:
            if rect.colliderect(thing.rect):
                if remove:
                    self.things.remove(thing)
                collision = True
        return(collision)


class PacMan(object):
    """PacMan Vector Art"""

    def __init__(self, center):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.center = (center[0] * TILESIZE + TILESIZE / 2, center[1] * TILESIZE + TILESIZE /2)
        self.startpos = self.rect
        self.direction = (0, 0)
        self.radius = TILESIZE / 2
        self.step = TILESIZE
        self.food = 0
        self.lifes = 5

    def draw(self, surface):
        self.rect = pygame.draw.circle(surface, (0,255,255), self.rect.center, self.radius, 0)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = (-self.step, 0)
                elif event.key == pygame.K_RIGHT:
                    self.direction = (self.step, 0)
                elif event.key == pygame.K_UP:
                    self.direction = (0, -self.step)
                elif event.key == pygame.K_DOWN:
                    self.direction = (0, self.step)
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    self.direction = (0, 0)
        newpos = self.rect.move(self.direction)
        # calculate new position
        return(newpos)

    def move(self, newpos):
        self.rect = newpos

    def reset(self):
        self.rect = self.startpos
        self.lifes -= 1


class Enemy(object):
    """Enemy Vector Art"""

    def __init__(self, center):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.center = (center[0] * TILESIZE + TILESIZE / 2, center[1] * TILESIZE + TILESIZE /2)
        self.startpos = self.rect
        self.direction = (0, 0)
        self.radius = TILESIZE / 2
        self.step = TILESIZE
        # since no player ist set, random walk
        self.player = None
        self.walls = None
        # set possible directions
        self.directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
        

    def set_player(self, player):
        """set player as target"""
        self.player = player

    def set_walls(self, walls):
        """set walls as boundaries"""
        self.walls = walls

    def draw(self, surface):
        self.rect = pygame.draw.circle(surface, (255, 255, 255), self.rect.center, self.radius, 0)

    def update(self, events):
        if self.player is not None:
            target = self.player.rect
            dx = target.x - self.rect.x
            dy = target.y - self.rect.y
            # normalized direction
            if abs(dx) > abs(dy):
                self.direction = (dx/abs(dx), 0)
            else:
                self.direction = (0, dy/abs(dy))
            return(newpos)
        return(self.rect)

    def move(self, others):
        index = self.directions.index(self.direction)
        alternatives = list(self.directions[index:] + self.directions[:index])[::-1]
        newpos = self.rect
        free_way = False
        while not free_way:
            print "Trying Direction %d : %s" % (index, self.direction)
            direction =  alternatives.pop()
            newpos = self.rect.move((direction[0] * TILESIZE, direction[1] * TILESIZE))
            if self.walls.collide(newpos) is not True:
                free_way = True
                print "free_way found"
            else:
                print "There is a wall"
        self.rect = newpos

    def reset(self):
        pass


class Wall(object):
    """Wall Vector Art"""

    def __init__(self, center):
        self.surface = surface
        self.rect = pygame.Rect(0, 0, TILESIZE, TILESIZE)
        self.rect.center = (center[0] * TILESIZE + TILESIZE / 2, center[1] * TILESIZE + TILESIZE /2)

    def draw(self, surface):
        self.rect = pygame.draw.rect(surface, (100,255,100), self.rect, 0)

    def update(self, events):
        pass

    def move(self, others):
        pass

    def collides(self, other):
        return(self.rect.colliderect(other))


class Food(object):
    """Food Vector Art"""

    def __init__(self, center):
        self.surface = surface
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.center = (center[0] * TILESIZE + TILESIZE / 2, center[1] * TILESIZE + TILESIZE /2)
        self.size = TILESIZE / 4

    def draw(self, surface):
        self.rect = pygame.draw.circle(surface, (100, 0, 100), self.rect.center, self.size, 0)

    def update(self, events):
        pass

    def move(self, others):
        pass

    def collides(self, other):
        return(self.rect.colliderect(other))


class Bomb(object):
    """Bomb Vector Art"""

    def __init__(self, center):
        self.surface = surface
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.center = (center[0] * TILESIZE + TILESIZE / 2, center[1] * TILESIZE + TILESIZE /2)
        self.size = TILESIZE / 2

    def draw(self, surface):
        self.rect = pygame.draw.circle(surface, (0, 0, 100), self.rect.center, self.size, 0)

    def update(self, events):
        pass

    def move(self, others):
        pass

    def collides(self, other):
        return(self.rect.colliderect(other))


class Score(object):
    """Draws Score on surface"""
    
    def __init__(self, player, surface):
        self.player = player
        self.surface = surface
        self.font = pygame.font.SysFont("Times New Roman", 25)

    def draw(self):
        text = "%5d Points %2d Lifes" % (self.player.food, self.player.lifes)
        text_img = self.font.render(text, True, (100, 100, 0))
        self.surface.blit(text_img, (0, 0))

    def update(self):
        self.surface.fill((0, 0, 0, 255))
        self.draw()

    def move(self):
        pass


if __name__=='__main__':

    try:
        screen = pygame.display.set_mode(RES)
        surface = screen.subsurface(0, 25, 800, 400)
        score_surface = screen.subsurface(0, 0, 800, 25)
        pygame.init()
        
        all_objects = GameObjects(surface)
        players = GameObjects(surface)
        walls = GameObjects(surface)
        foods = GameObjects(surface)
        bombs = GameObjects(surface)
        enemies = GameObjects(surface)
        player = None

        y = 0
        for line in open("PacMan.map", "rb"):
            thing = None
            x = 0
            for char in line:
                if char == "w":
                    thing = Wall((x, y))
                    walls.add(thing)
                if char == "f":
                    thing = Food((x, y))
                    foods.add(thing)
                if char == "b":
                    thing = Bomb((x, y))
                    bombs.add(thing)
                if char == "p":
                    player = PacMan((x, y))
                    thing = player
                if char == "e":
                    thing = Enemy((x,y))
                    enemies.add(thing)
                all_objects.add(thing)
                x += 1
            y += 1

        score = Score(player, score_surface)
        # set target for enemies
        for enemy in enemies.things:
            enemy.set_player(player)
            enemy.set_walls(walls)

        clock = pygame.time.Clock()       
        # mark pause state 
        pause = False
        # fill background
        surface.fill((0, 0, 0, 255))
        clicked = None
        while True:
            # limit to FPS
            clock.tick(FPS)
            # Event Handling
            events = pygame.event.get()  
            for event in events:  
                if event.type == pygame.QUIT:  
                    sys.exit(0)
            keyinput = pygame.key.get_pressed()
            if keyinput is not None:
                # print keyinput
                if keyinput[pygame.K_ESCAPE]:
                    sys.exit(1)
                if keyinput[pygame.K_p]:
                    pause = not pause
            # Update Graphics
            dirtyrects = []
            if pause is not True:
                surface.fill((0, 0, 0, 255))
                newpos = player.update(events)
                # collides player with wall -> dont move
                if not walls.collide(newpos):
                    player.move(newpos)
                # collides player with food -> eat them
                if foods.collide(newpos, True):
                    player.food += 1
                # collides player with bomb -> reset player
                if bombs.collide(newpos, True):
                    player.reset()
                player.draw(surface)
                walls.update(events)
                foods.update(events)
                bombs.update(events)
                enemies.update(events)
                score.update()
                pygame.display.update()
                # pygame.display.flip()
    except KeyboardInterrupt:
        print 'shutting down'
