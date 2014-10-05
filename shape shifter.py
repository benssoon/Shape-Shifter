#!/usr/bin/python3.3

import pygame
from pygame.locals import *
pygame.init()

# Name of the game
NAME = __file__

# Colors
WHITE	= (255,255,255)
BLACK	= (  0,  0,  0)
ORANGE	= (255, 127, 0)
PURPLE	= (128, 0, 128)
GREEN	= (  0,255,  0)

# Screen info
WIDTH = 720
HEIGHT = 720
FPS = 60

class Obstacle(pygame.sprite.Sprite):

	def __init__(self, shape, color, width, position, spriteSize, rect=0, center=0, radius=0, vertices=0):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface(spriteSize)
		self.image.fill(WHITE)
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()

		if shape == "rect":
			pygame.draw.rect(self.image, color, rect, width)
			pygame.draw.rect(self.image, BLACK, self.rect, 1)
			self.rect.x = int(position[0])
			self.rect.y = int(position[1])
		elif shape == "circle":
			pygame.draw.circle(self.image, color, center, radius, width)
			pygame.draw.circle(self.image, BLACK, center, radius, 1)
			self.rect.x = int(position[0])
			self.rect.y = int(position[1])
		elif shape == "triangle":
			pygame.draw.polygon(self.image, color, vertices, width)
			pygame.draw.polygon(self.image, BLACK, vertices, 1)
			self.rect.x = int(position[0])
			self.rect.y = int(position[1])



class Player(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)	# Be sure to initialize the parent class as well.
		self.image = pygame.Surface([10,10])
		self.image.fill(WHITE)
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		pygame.draw.circle(self.image, BLACK, [5,5], 5, 0)

		self.vector = [0,0]	# [x speed, y speed]
		self.speed = 3


	def update(self):
		if self.vector[0] == 1:			# RIGHT
			self.rect.x += self.speed
		elif self.vector[0] == -1:		# LEFT
			self.rect.x -= self.speed
		if self.vector[1] == -1:		# UP
			self.rect.y += self.speed
		elif self.vector[1] == 1:		# DOWN
			self.rect.y -= self.speed



class Game:

	# Initialize the game
	def __init__(self):
		self.end = False

		self.allSprites = pygame.sprite.Group()

		self.player = Player()
		self.player.rect.x = int(WIDTH/2)
		self.player.rect.y = int(HEIGHT/2)
		self.allSprites.add(self.player)

		#### Get game state ####
		lines = []
		with open("data/levelOne.data") as f:
			for line in f:
				lines.append(line.strip().split(';'))
		for line in lines:
			for i in range(len(line)):
				line[i]=eval(line[i])

		for obstacle in lines:
			shape,color,width,position,spriteSize,rect,center,radius,vertices = obstacle
			newObstacle = Obstacle(shape,color,width,position,spriteSize,rect,center,radius,vertices)
			self.allSprites.add(newObstacle)
		########################


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


	# Draw
	def draw(self, screen):
		screen.fill(WHITE)

		if not self.end:
			self.allSprites.draw(screen)

		pygame.display.flip()



def main():

	window = (WIDTH,HEIGHT)
	screen = pygame.display.set_mode(window)
	pygame.display.set_caption(NAME)	# Sets the title of the window.
	done = False	# For ending the main loop.
	clock = pygame.time.Clock()	# An object used for tracking time in the game.
	game = Game() # An instance of the game.

	while not done:
		# Update the game state in the proper order.
		done = game.events()
		game.logic()
		game.draw(screen)

		clock.tick(FPS)	# Set the framerate to 60 fps

	pygame.quit()	# Quits the game when the loop ends.

# Call main function
if __name__ == "__main__":
	main()
