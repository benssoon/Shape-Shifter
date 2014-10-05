#!/usr/bin/python3.3

import pygame
from pygame.locals import *
pygame.init()

# Name of the game
NAME = __file__

# Colors
WHITE	= (255, 255, 255)
BLACK	= (  0,   0,   0)
ORANGE	= (180,  80,   0)
PURPLE	= (110,  20, 128)
GREEN	= ( 38, 128,  20)

# Screen info
WIDTH = 720
HEIGHT = 720
FPS = 60

class Obstacle(pygame.sprite.Sprite):

	def __init__(self, name, shape, color, width, position, spriteSize, rect=0, center=0, radius=0, vertices=0):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface(spriteSize)
		self.image.fill(BLACK)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.name = name
		self.shape = {"name":name,"shape":shape,"color":color,"width":width,"position":position,"spriteSize":spriteSize,"rect":rect,"center":center,"radius":radius,"vertices":vertices}

		if shape == "rect":
			pygame.draw.rect(self.image, color, rect, width)
			pygame.draw.rect(self.image, WHITE, self.rect, 1)
			self.rect.x = int(position[0])
			self.rect.y = int(position[1])
		elif shape == "circle":
			pygame.draw.circle(self.image, color, center, radius, width)
			pygame.draw.circle(self.image, WHITE, center, radius, 1)
			self.rect.x = int(position[0])
			self.rect.y = int(position[1])
		elif shape == "triangle":
			pygame.draw.polygon(self.image, color, vertices, width)
			pygame.draw.polygon(self.image, WHITE, vertices, 1)
			self.rect.x = int(position[0])
			self.rect.y = int(position[1])



class Player(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)	# Be sure to initialize the parent class as well.
		self.image = pygame.Surface([10,10])
		self.image.fill(BLACK)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		pygame.draw.circle(self.image, WHITE, [5,5], 5, 0)

		self.vector = [0,0]	# [x speed, y speed]
		self.speed = 1

		self.rect.x = 325 #int(WIDTH/2)
		self.rect.y = 325 #int(HEIGHT/2)


	def update(self):
		if self.vector[0] == 1:			# RIGHT
			self.rect.x += self.speed
		elif self.vector[0] == -1:		# LEFT
			self.rect.x -= self.speed
		if self.vector[1] == -1:		# UP
			self.rect.y += self.speed
		elif self.vector[1] == 1:		# DOWN
			self.rect.y -= self.speed


	def change(self, shape):
		if shape["name"] == "orange rectangle":
			pygame.draw.rect(self.image, shape["color"], shape["rect"], shape["width"])
			pygame.draw.rect(self.image, WHITE, self.rect, 1)
			self.rect.x = int(shape["position"][0])
			self.rect.y = int(shape["position"][1])



class Game:

	# Initialize the game
	def __init__(self, screen):
		self.end = False
		self.screen = screen

		# Sprites
		self.allSprites = pygame.sprite.Group()
		self.obstacles = pygame.sprite.Group()
		#########

		self.player = Player()
		self.allSprites.add(self.player)

		self.level = "one"
		self.path = ""
		self.get_state()


	def get_state(self):
		lines = []
		obstacles = []
		code = []
		data = []
		with open("data/{0}/level_{1}.data".format(self.path,self.level)) as f:
			for line in f:
				lines.append(line.strip().split(';'))
		line_number = 0
		for line in lines:
			eval("%s.append([])"%line[0])
			for i in range(1,len(line)):
				eval("%s[line_number].append(eval(line[i]))"%line[0])
			line_number += 1

		for obstacle in obstacles:
			name,shape,color,width,position,spriteSize,rect,center,radius,vertices = obstacle
			newObstacle = Obstacle(name,shape,color,width,position,spriteSize,rect,center,radius,vertices)
			self.allSprites.add(newObstacle)
			self.obstacles.add(newObstacle)



	# Events
	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
				return True
		pressed = pygame.key.get_pressed()
		if pressed[K_RIGHT]:			# RIGHT
			self.player.vector[0] = 1
		if pressed[K_LEFT]:			# LEFT
			self.player.vector[0] = -1
		if pressed[K_UP]:			# UP
			self.player.vector[1] = 1
		if pressed[K_DOWN]:			# DOWN
			self.player.vector[1] = -1
		if not (pressed[K_RIGHT] or pressed[K_LEFT] or pressed[K_UP] or pressed[K_DOWN]):
			self.player.vector = [0,0]
		return False


	# Logic
	def logic(self):
		self.allSprites.update()

		collisions = pygame.sprite.spritecollide(self.player, self.obstacles, True)

		for obstacle in collisions:
			if obstacle.name == "orange rectangle":
				self.level = "two"
				self.path = "programming"
				#self.player.change(obstacle.shape)
				for sprite in self.obstacles:
					self.allSprites.remove(sprite)
				self.obstacles.empty()
				self.get_state()
			elif obstacle.name == "purple circle":
				self.level = "two"
				self.path = "physics"
				for sprite in self.obstacles:
					self.allSprites.remove(sprite)
				self.obstacles.empty()
				self.get_state()
			elif obstacle.name == "green triangle":
				self.level = "two"
				self.path = "geometry"
				for sprite in self.obstacles:
					self.allSprites.remove(sprite)
				self.obstacles.empty()
				self.get_state()


	# Draw
	def draw(self):
		self.screen.fill(BLACK)

		if not self.end:
			self.allSprites.draw(self.screen)

		pygame.display.flip()



def main():

	window = (WIDTH,HEIGHT)
	screen = pygame.display.set_mode(window)
	pygame.display.set_caption(NAME)	# Sets the title of the window.
	done = False	# For ending the main loop.
	clock = pygame.time.Clock()	# An object used for tracking time in the game.
	game = Game(screen) # An instance of the game.

	while not done:
		# Update the game state in the proper order.
		done = game.events()
		game.logic()
		game.draw()

		clock.tick(FPS)	# Set the framerate to 60 fps

	pygame.quit()	# Quits the game when the loop ends.

# Call main function
if __name__ == "__main__":
	main()
