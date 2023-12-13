import pygame
import os

 #create a sub class to a sprite class

class Tile(pygame.sprite.Sprite):
    """
    Class representing a tile object in the game world.
    
    """
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        
    def get_size(self):
        return self.image.get_size()
    

class Sprite(pygame.sprite.Sprite):
    """
    Class representing a Sprite object in the game world.

    """
    def __init__(self, x, y, image, size):
        super().__init__()
        self.size = size
        self.x = x
        self.y = y
        self.image = image
        self.image = pygame.transform.scale_by(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)



    def get_size(self):
        return self.size
    def get_image(self):
        return self.image
    
    def set_image(self, image):
        self.image = image
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale_by(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
    
    

