import pygame
import os

class Tile(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets/tile.png'))
		self.image = pygame.transform.scale(self.image, (size, size//2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y



