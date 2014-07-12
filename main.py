import time
from pygame.locals import *
import pygame, math, sys, random

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

pygame.init()
#This is so ugly
caves1 = pygame.sprite.Group()
caves2 = pygame.sprite.Group()
ducks1 = pygame.sprite.Group()
ducks2 = pygame.sprite.Group()
walls = pygame.sprite.Group()
font = pygame.font.SysFont("Comic Sans MS", 280)
playerfont = pygame.font.SysFont("Comic Sans MS", 40)
WIDTH = 1280
HEIGHT = 800
BLACK = (0,0,0)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
background = pygame.image.load('wallp.jpg')
clock = pygame.time.Clock()

#pygame.mixer.music.load('mus1.wav')#load music
quack = pygame.mixer.Sound('kvack.ogg')
saab = pygame.mixer.Sound('rajula.ogg')
aj = pygame.mixer.Sound('tordead.ogg')
#pygame.mixer.music.play(-1)
def win(player):
		label = font.render("Player " + str(player) + " wins", 1, (255,128,197))
		print WIDTH - font.get_linesize()
		screen.blit(label, (((WIDTH - label.get_width())/ 2), (HEIGHT - label.get_height())/2))
		pygame.display.flip()
		time.sleep(5000)
		pygame.quit()

class Duck(pygame.sprite.Sprite):
	images = []
	images.append(pygame.image.load('raju1.png'))
	images.append(pygame.image.load('a1.png'))
	def __init__(self, position, direction, speed, owner):
		pygame.sprite.Sprite.__init__(self)
		self.direction = direction
		self.speed = max(10,  speed + 10)
		self.owner = owner
		rad = self.direction * math.pi/180
		self.src_image = self.images[self.owner.playernumber - 1]
		self.position = position
		self.k_left = self.k_right = 0

		
	def update(self, deltat):
		x,y = self.position
		rad = self.direction * math.pi/180
		x += -self.speed * math.sin(rad)
		y += -self.speed * math.cos(rad)
		if (x < 0 or y < 0 or x >= WIDTH or y > HEIGHT):
			self.kill()
			self.owner.changeAmmo(1)
		self.position = (x,y)
		self.rect = self.src_image.get_rect()
		self.rect.center = self.position
		self.image = pygame.transform.rotate(self.src_image, self.direction)

	def bounce(self):
		self.direction = random.randint(0,360)
	

class Cave(pygame.sprite.Sprite):
	MAX_FORWARD_SPEED = 10
	MAX_REVERSE_SPEED = -10
	ACCELERATION = 2
	TURN_SPEED = 10

	def __init__(self, playernumber, images, position, health):
		pygame.sprite.Sprite.__init__(self)
		#For animation
		self.images = []
		self.index = 0
		for i in images:
			self.images.append(pygame.image.load(i))

		self.ammo = 7
		self.playernumber = playernumber
		self.health = health

		self.image = self.images[0]
		self.position = position
		self.speed = self.direction = 0
		self.k_up = self.k_down = self.k_left = self.k_right = 0

		self.healthbar = playerfont.render(str(self.health),1, (255,0,0))
		self.ammobar = playerfont.render(str(self.ammo),1, (0,255,0))
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
		screen.blit(self.healthbar, (self.position[0] - 30, self.position[1] - 50))
		screen.blit(self.ammobar, (self.position[0] + 30, self.position[1] - 50))


	def hit(self):
		aj.play()
		self.health -= 10
		self.healthbar = playerfont.render(str(self.health),1, (255,0,0))
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
		duck = Duck(self.position, self.direction, self.speed, self)
		if self.playernumber == 1:
			ducks1.add(duck)
			saab.play()
		else:
			ducks2.add(duck)
			quack.play()
		self.changeAmmo(-1)
	
	def changeAmmo(self,n):
		self.ammo += n
		self.ammobar = playerfont.render(str(self.ammo),1, (0,255,0))
	

class Wall(pygame.sprite.Sprite):
	def __init__(self, position, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(position[0], position[1], width,height)
		walls.add(self)

	
def main():
	for t in range(50,0,-1):
		introPlayerOne = []
		introPlayerTwo = []
		rand = random.randint(0,255)
		introPlayerOne.append(playerfont.render("Player one:",1,(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
		introPlayerOne.append(playerfont.render("Move up: W",1,(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
		introPlayerOne.append(playerfont.render("Move left: A",1,(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
		introPlayerOne.append(playerfont.render("Move down: S",1,(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
		introPlayerOne.append(playerfont.render("Move right: D",1,(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
		introPlayerOne.append(playerfont.render("Shoot: F",1,(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
		introPlayerTwo.append(playerfont.render("Player two:",1,(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
		introPlayerTwo.append(playerfont.render("Move up: Up-arrow",1,(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
		introPlayerTwo.append(playerfont.render("Move left: Left-arrow",1,(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
		introPlayerTwo.append(playerfont.render("Move down: Down-arrow",1,(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
		introPlayerTwo.append(playerfont.render("Move right: Right-arrow",1,(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
		introPlayerTwo.append(playerfont.render("Shoot: CTRL",1,(random.randint(0,255), random.randint(0,255), random.randint(0,255))))
		screen.fill(BLACK)
		a = 100
		for i in introPlayerOne:
			screen.blit(i, (100,a))
			a += 40
		a = 100
		for i in introPlayerTwo:
			screen.blit(i, (700,a))
			a += 40
		screen.blit(playerfont.render("Game starts in " + str(t/10.0),1, (random.randint(0,255),
																	random.randint(0,255),
																	random.randint(0,255))),
																	 (400,600))
		time.sleep(0.1)
		pygame.display.flip()
	
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
			if event.key == K_RCTRL: 
				cave2.ducklol()
			elif event.key == K_RIGHT: 
				cave2.k_right = down * -cave2.TURN_SPEED
			elif event.key == K_LEFT:
				cave2.k_left = down * cave2.TURN_SPEED
			elif event.key == K_UP:
				cave2.k_up = down * 2
			elif event.key == K_DOWN:
				cave2.k_down = down * 2
			elif event.key == K_f: 
				cave1.ducklol()
			elif event.key == K_d: 
				cave1.k_right = down * -cave1.TURN_SPEED
			elif event.key == K_a:
				cave1.k_left = down * cave1.TURN_SPEED
			elif event.key == K_w:
				cave1.k_up = down * 2
			elif event.key == K_s:
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
		hits = pygame.sprite.groupcollide(caves1,ducks2,False, False)
		hits2 = pygame.sprite.groupcollide(caves2,ducks1,False, False)

		for h in [hits,hits2]:
			for cave in h.keys():
				cave.hit()
			for d in h.values():
				for duck in d:
					duck.owner.changeAmmo(1)
					duck.kill()
		for d in [FiredDucks1, FiredDucks2]:
			for duck in d:
				duck.bounce()
		for w in walls:
			pygame.draw.rect(screen, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), w.rect)


		Wall((random.randint(0,WIDTH),random.randint(0,HEIGHT)),random.randint(0,10),random.randint(1,10))
		pygame.display.flip()

if __name__ == "__main__":
	main()
