#!python
# coding: utf8

import pygame
from pygame.locals import *


def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

	
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):	
	pygame.sprite.Sprite.__init__(self)
	self.image, self.rect  = load_image("player.png", -1)
	self.rect.center = pos
	self.start_pos = pos
	self.step_size = 10
	self.x = self.y = 0
	self.cherries = 0
	self.screenrect = pygame.display.get_surface().get_rect()
	
    def update(self, events):
	
	for event in events:
		if event.type == KEYDOWN:
			if event.key == K_LEFT:
				self.x += -1 * self.step_size
			elif event.key == K_RIGHT:
				self.x += 1 * self.step_size
			elif event.key == K_UP:
				self.y += -1 * self.step_size
			elif event.key == K_DOWN:
				self.y += 1 * self.step_size
		elif event.type == KEYUP:
			if event.key in (K_LEFT, K_RIGHT):
				self.x = 0
			elif event.key in (K_UP, K_DOWN):
				self.y = 0
	if self.x and not self.screenrect.contains(self.rect.move(self.x, 0)):
		self.x = 0
	if self.y and not self.screenrect.contains(self.rect.move(0, self.y)):
		self.y = 0
	self.rect.move_ip(self.x, self.y)
	
    def reset_position(self):
	    self.rect.center = self.start_pos
	
class Cherry(pygame.sprite.Sprite):
    def __init__(self, pos):	
	pygame.sprite.Sprite.__init__(self)
	self.image, self.rect  = load_image("kirsche.png", -1)
	self.rect.center=pos

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos):	
	pygame.sprite.Sprite.__init__(self)
	self.image, self.rect  = load_image("bombe.png", -1)
	self.rect.center=pos
	
		
def main():
    pygame.init()
    screen = pygame.display.set_mode((500,300))
    pygame.display.set_caption("Pygame ist toll")
    clock = pygame.time.Clock()
    font = font = pygame.font.SysFont("Times New Roman",25)
    
    all_sprites = pygame.sprite.Group()
    cherries = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    player = Player((50, 50))
    all_sprites.add(player)
    
    for pos in ((172, 133),(71, 259),(210, 207),(338, 48),(427, 196),(317, 278),(452, 23)):
	c = Cherry(pos)
	all_sprites.add(c)
	cherries.add(c)
    for pos in ((61, 124),(124, 202),(315, 194),(266, 102),(152, 31),(461, 86)):
	b = Bomb(pos)
	all_sprites.add(b)
	bombs.add(b)
    
    while True:
	# maximal 40 fpsok
	clock.tick(40)
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
	
	for cherry in pygame.sprite.spritecollide(player, cherries, True):
		player.cherries += 1
        for bomb in pygame.sprite.spritecollide(player, bombs, False):
		player.cherries -= 1
		player.reset_position()
	
	# den Bildschirm mit einer Hintergrundfarbe füllen und so 
	# gleichzeitig das alte Bild löschen
	screen.fill((120,30,66))
	
	## Über die Gruppe alle Sprites updaten und dann blitten
	all_sprites.update(events)
	all_sprites.draw(screen)
	text_img = font.render("cherries: %i"%player.cherries, True, (255,255,255))
	screen.blit(text_img, (5,5))
	
	# alles aufs Fenster flippen
	pygame.display.flip()

if __name__ == '__main__': main()
