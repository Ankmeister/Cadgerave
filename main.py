import time
from pygame.locals import *
import pygame, math, sys

WIDTH = 1920
HEIGHT = 1200
BLACK = (0,0,0)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
caves = pygame.sprite.RenderPlain()
ducks = pygame.sprite.RenderPlain()

class Duck(pygame.sprite.Sprite):
	def __init__(self, position, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 50
		self.direction = direction
		self.src_image = pygame.image.load('ammo.png')
		self.position = position
		self.k_left = self.k_right = 0
		
	def update(self, deltat):
		x,y = self.position
		rad = self.direction * math.pi/180
		x += -self.speed * math.sin(rad)
		y += -self.speed * math.cos(rad)
		self.position = (x,y)
		self.rect = self.src_image.get_rect()
		self.rect.center = self.position
		self.image = pygame.transform.rotate(self.src_image, self.direction)
		ducks.add(duck)
	

class Cave(pygame.sprite.Sprite):
	MAX_FORWARD_SPEED = 10
	MAX_REVERSE_SPEED = 10
	ACCELERATION = 2
	TURN_SPEED = 5

	def __init__(self,image, position):
		pygame.sprite.Sprite.__init__(self)
		#For animation
		self.images = []
		self.index = 0
		self.images.append(pygame.image.load('c1.png'))
		self.images.append(pygame.image.load('c2.png'))
		self.images.append(pygame.image.load('c3.png'))
		self.images.append(pygame.image.load('c2.png'))
		self.image = self.images[self.index]

		self.src_image = pygame.image.load(image)
		self.position = position
		self.speed = self.direction = 0
		self.k_up = self.k_down = self.k_left = self.k_right = 0
	
	def update(self,deltat):
		#for animation
		self.index = (self.index + 1) % len(self.images)

		self.speed += self.k_up - self.k_down
		x,y = self.position
		rad = self.direction * math.pi / 180
		x += -self.speed * math.sin(rad)
		y += -self.speed * math.cos(rad)
		self.direction +=self.k_right + self.k_left
		self.position = (x % WIDTH,y % HEIGHT)
		self.image = pygame.transform.rotate(self.images[self.index], self.direction)
		self.rect = self.image.get_rect()
		self.rect.center = self.position

	def ducklol(self):
		global ducks,duck
		duck = Duck(self.position, self.direction)
		ducks.add(duck)

rect = screen.get_rect()
cave1 = Cave('cave.png', (50,100))
cave2 = Cave('cave.png', rect.center)
caves.add(cave1)
caves.add(cave2)

while 1:
	clock.tick(30)
	for event in pygame.event.get():
		if not hasattr(event,'key'): continue
		down = event.type == KEYDOWN
		if event.key == K_RIGHT: 
			cave1.k_right = down * -5
		elif event.key == K_b: 
			cave1.ducklol()
		elif event.key == K_LEFT:
			cave1.k_left = down * 5
		elif event.key == K_UP:
			cave1.k_up = down * 2
		elif event.key == K_DOWN:
			cave1.k_down = down * 2
		elif event.key == K_i: 
			cave2.k_right = down * -5
		elif event.key == K_e:
			cave2.k_left = down * 5
		elif event.key == K_p:
			cave2.k_up = down * 2
		elif event.key == K_u:
			cave2.k_down = down * 2
		elif event.key == K_ESCAPE: sys.exit(0)	 # quit the game
	screen.fill(BLACK)

	caves.update(30)
	caves.draw(screen)
	ducks.update(30)
	ducks.draw(screen)
	pygame.display.flip()
