import pygame
import os

 #create a sub class to a sprite class

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def set_pos(self,x,y):
        self.rect.center = (x,y)

    def get_size(self):
        return self.image.get_size()
    
    

