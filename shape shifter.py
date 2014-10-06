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

	def __init__(self, name, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("media/obstacles/%s.png"%name).convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.name = name
		print(position)
		self.rect.x = int(position[0])	# Still in str format from reading into the file. This seams like the easiest place to convert them.
		self.rect.y = int(position[1])



class Player(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)	# Be sure to initialize the parent class as well.
		self.image = pygame.image.load("media/player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()

		self.clock = pygame.time.Clock()
		self.stop = False
		self.step = 1

		self.vector = [0,0]	# [x speed, y speed]
		self.speed = 1

		self.rect.x = 325 #int(WIDTH/2)
		self.rect.y = 325 #int(HEIGHT/2)


	def update(self, path=""):
		if self.vector[0] == 1:			# RIGHT
			self.rect.x += self.speed
		elif self.vector[0] == -1:		# LEFT
			self.rect.x -= self.speed
		if self.vector[1] == -1:		# UP
			self.rect.y += self.speed
		elif self.vector[1] == 1:		# DOWN
			self.rect.y -= self.speed

		if path != "" and not self.stop:
			if self.step == 1:
				self.image = pygame.image.load("media/%s/player.png"%path).convert()
			elif self.step == 2:
				self.image = pygame.image.load("media/%s/player2.png"%path).convert()
			elif self.step == 3:
				self.image = pygame.image.load("media/%s/player3.png"%path).convert()
			elif self.step == 4:
				self.image = pygame.image.load("media/%s/player4.png"%path).convert()
				self.stop = True
				self.step = 1
			pygame.time.delay(300)
			self.step += 1



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
		with open("data/{0}/level_{1}.data".format(self.path,self.level)) as f:	# Read from the file specified by the path the game has taken and the level.
			for line in f:
				lines.append(line.strip().split(';'))
		obstacles_number = 0	# Used for counting how many of each kind of thing there are.
		code_number = 0
		data_number = 0
		for line in lines:
			if line[0] == "obstacles":
				obstacles.append([])	# Creates a spot in the list for a new obstacle.
				obstacles[obstacles_number].append(line[1])			# Sprite name
				obstacles[obstacles_number].append(line[2].split(','))		# Position
				obstacles_number += 1
			elif line[0] == "code":
				code.append([])
				code[code_number].append(line[1])
				code_number += 1
			elif line[0] == "data":
				data.append([])
				data[data_number].append(line[1])
				data_number += 1

		for obstacle in obstacles:	# For each obstacle in the level, create a new obstacle object.
			name = obstacle[0]
			position = obstacle[1]
			newObstacle = Obstacle(name, position)
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
		self.allSprites.update(self.path)

		collisions = pygame.sprite.spritecollide(self.player, self.obstacles, True)

		for obstacle in collisions:
			if obstacle.name == "orange_square":
				self.level = "two"
				self.path = "programming"
				for sprite in self.obstacles:
					self.allSprites.remove(sprite)
				self.obstacles.empty()
				self.get_state()
			elif obstacle.name == "purple_circle":
				self.level = "two"
				self.path = "physics"
				for sprite in self.obstacles:
					self.allSprites.remove(sprite)
				self.obstacles.empty()
				self.get_state()
			elif obstacle.name == "green_triangle":
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
