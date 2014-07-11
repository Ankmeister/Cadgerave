import time
from pygame.locals import *
import pygame, math, sys, random

pygame.init()
font = pygame.font.SysFont("Comic Sans MS", 400)
healthfont = pygame.font.SysFont("Comic Sans MS", 40)
WIDTH = 1920
HEIGHT = 1200
BLACK = (0,0,0)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
background = pygame.image.load('wallp.jpg')
clock = pygame.time.Clock()
caves = pygame.sprite.Group()
ducks = pygame.sprite.Group()

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
		self.speed = max(10,  speed + 40)
		rad = self.direction * math.pi/180
		self.src_image = self.images[random.randint(0,1)]
		self.position = position
		x = -200 * math.sin(rad)
		y = -200 * math.cos(rad)
		self.position = (self.position[0] + x, self.position[1] + y)
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
		ducks.add(duck)
	

class Cave(pygame.sprite.Sprite):
	MAX_FORWARD_SPEED = 10
	MAX_REVERSE_SPEED = 10
	ACCELERATION = 2
	TURN_SPEED = 15

	def __init__(self, playernumber, images, position, health):
		pygame.sprite.Sprite.__init__(self)
		#For animation
		self.images = []
		self.index = 0
		for i in images:
			self.images.append(pygame.image.load(i))

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


	def ducklol(self):
		global ducks,duck
		duck = Duck(self.position, self.direction, self.speed)
		ducks.add(duck)

class wall(pygame.sprite.Sprite):
	def __init__(self, position):
		self.rect = pygame.Rect(position[0], position[1])

	
def main():
	start_game()


def start_game():

	rect = screen.get_rect()
	cave1 = Cave(1,['c1.png', 'c2.png', 'c3.png', 'c2.png'], (WIDTH/2, 0), 100)
	cave2 = Cave(2,['d1.png', 'd2.png', 'd3.png', 'd2.png'], (WIDTH/2, HEIGHT/2), 100)
	caves.add(cave1)
	caves.add(cave2)



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
		caves.update(30)
		caves.draw(screen)
		ducks.update(30)
		ducks.draw(screen)
		hits = pygame.sprite.groupcollide(caves,ducks,False, True)
		for item in hits.keys():
			item.hit()

		pygame.display.flip()

if __name__ == "__main__":
	main()
