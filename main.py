import time
from pygame.locals import *
import pygame, math, sys, random

pygame.init()
#This is so ugly
caves1 = pygame.sprite.Group()
caves2 = pygame.sprite.Group()
ducks1 = pygame.sprite.Group()
ducks2 = pygame.sprite.Group()
walls = pygame.sprite.Group()
font = pygame.font.SysFont("Comic Sans MS", 400)
healthfont = pygame.font.SysFont("Comic Sans MS", 40)
WIDTH = 1920
HEIGHT = 1200
BLACK = (0,0,0)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
background = pygame.image.load('wallp.jpg')
clock = pygame.time.Clock()

def win(player):
		label = font.render("Player " + str(player) + " wins", 1, (255,128,197))
		print WIDTH - font.get_linesize()
		screen.blit(label, (((WIDTH - label.get_width())/ 2), (HEIGHT - label.get_height())/2))
		pygame.display.flip()
		time.sleep(5000)

class Duck(pygame.sprite.Sprite):
	images = []
	images.append(pygame.image.load('raju1.png'))
	images.append(pygame.image.load('a1.png'))
	def __init__(self, position, direction, speed):
		pygame.sprite.Sprite.__init__(self)
		self.direction = direction
		self.speed = max(10,  speed + 20)
		rad = self.direction * math.pi/180
		self.src_image = self.images[random.randint(0,1)]
		self.position = position
		self.k_left = self.k_right = 0

		
	def update(self, deltat):
		x,y = self.position
		rad = self.direction * math.pi/180
		x += -self.speed * math.sin(rad)
		y += -self.speed * math.cos(rad)
		if (x < 0 or y < 0 or x >= WIDTH or y > HEIGHT):
			self.kill()

		self.position = (x,y)
		self.rect = self.src_image.get_rect()
		self.rect.center = self.position
		self.image = pygame.transform.rotate(self.src_image, self.direction)

	def bounce(self):
		self.direction = random.randint(0,360)
	

class Cave(pygame.sprite.Sprite):
	MAX_FORWARD_SPEED = 20
	MAX_REVERSE_SPEED = -20
	ACCELERATION = 2
	TURN_SPEED = 10

	def __init__(self, playernumber, images, position, health):
		pygame.sprite.Sprite.__init__(self)
		#For animation
		self.images = []
		self.index = 0
		for i in images:
			self.images.append(pygame.image.load(i))

		self.ammo = 10
		self.playernumber = playernumber
		self.health = health

		self.image = self.images[0]
		self.position = position
		self.speed = self.direction = 0
		self.k_up = self.k_down = self.k_left = self.k_right = 0

		self.healthbar = healthfont.render(str(self.health),1, (255,0,0))
		screen.blit(self.healthbar, self.position)
	
	def update(self,deltat):
		#for animation
		self.index = (self.index + 1) % len(self.images)

		self.speed += self.k_up - self.k_down
		if self.speed > self.MAX_FORWARD_SPEED:
			self.speed = self.MAX_FORWARD_SPEED
		if self.speed < self.MAX_REVERSE_SPEED:
			self.speed = self.MAX_REVERSE_SPEED
		x,y = self.position
		rad = self.direction * math.pi / 180
		x += -self.speed * math.sin(rad)
		y += -self.speed * math.cos(rad)
		self.direction +=self.k_right + self.k_left
		self.position = (x % WIDTH,y % HEIGHT)
		self.image = pygame.transform.rotate(self.images[self.index], self.direction)
		tjenna = pygame.transform.scale(self.image, (self.image.get_width()/2, self.image.get_height()/2))
		self.rect = tjenna.get_rect()
		self.rect.center = self.position
		screen.blit(self.healthbar, (self.position[0], self.position[1] - 50))


	def hit(self):
		self.health -= 10
		self.healthbar = healthfont.render(str(self.health),1, (255,0,0))
		if self.health <= 0:
			self.kill()
			winner =  1 + (self.playernumber % 2)
			win(winner)

	def bounce(self):
		self.k_up = self.k_down
		self.k_down = self.k_up
		self.speed = -self.speed

	def ducklol(self):
		global ducks1,ducks2,duck
		if self.ammo <= 0:
			return
		duck = Duck(self.position, self.direction, self.speed)
		if self.playernumber == 1:
			ducks1.add(duck)
		else:
			ducks2.add(duck)
		self.ammo -=1

class Wall(pygame.sprite.Sprite):
	def __init__(self, position, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(position[0], position[1], width,height)
		walls.add(self)

	
def main():
	start_game()


def start_game():

	rect = screen.get_rect()
	cave1 = Cave(1,['c1.png', 'c2.png', 'c3.png', 'c2.png'], (100, 100), 100)
	cave2 = Cave(2,['d1.png', 'd2.png', 'd3.png', 'd2.png'], (WIDTH - 100, 100), 100)
	caves1.add(cave1)
	caves2.add(cave2)


	while 1:
		clock.tick(60)
		for event in pygame.event.get():
			if not hasattr(event,'key'): continue
			down = event.type == KEYDOWN
			if event.key == K_s: 
				cave2.ducklol()
			elif event.key == K_RIGHT: 
				cave2.k_right = down * -cave2.TURN_SPEED
			elif event.key == K_LEFT:
				cave2.k_left = down * cave2.TURN_SPEED
			elif event.key == K_UP:
				cave2.k_up = down * 2
			elif event.key == K_DOWN:
				cave2.k_down = down * 2
			elif event.key == K_d: 
				cave1.ducklol()
			elif event.key == K_i: 
				cave1.k_right = down * -cave1.TURN_SPEED
			elif event.key == K_e:
				cave1.k_left = down * cave1.TURN_SPEED
			elif event.key == K_p:
				cave1.k_up = down * 2
			elif event.key == K_u:
				cave1.k_down = down * 2
			elif event.key == K_ESCAPE: sys.exit(0)	 # quit the game
		screen.blit(background, [0,0])

		#this is so ugly
		caves1.update(30)
		caves1.draw(screen)
		caves2.update(30)
		caves2.draw(screen)
		ducks1.update(30)
		ducks1.draw(screen)
		ducks2.update(30)
		ducks2.draw(screen)
		FiredDucks1 = pygame.sprite.groupcollide(ducks1, walls, False, True)
		FiredDucks2 = pygame.sprite.groupcollide(ducks2, walls, False, True)
		hits = pygame.sprite.groupcollide(caves1,ducks2,False, True)
		hits2 = pygame.sprite.groupcollide(caves2,ducks1,False, True)

		for cave in hits.keys():
			cave.hit()
		for cave in hits2.keys():
			cave.hit()
		for duck1 in FiredDucks1:
			duck1.bounce()
		for duck2 in FiredDucks2:
			duck2.bounce()
		for w in walls:
			pygame.draw.rect(screen, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), w.rect)


		Wall((random.randint(0,WIDTH),random.randint(0,HEIGHT)),random.randint(0,10),random.randint(1,10))
		pygame.display.flip()

if __name__ == "__main__":
	main()
