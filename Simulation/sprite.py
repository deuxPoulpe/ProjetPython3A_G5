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
    
    def get_image(self):
        return self.image
    

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
    def get_rect(self):
        self.rect
    
    def set_image(self, image):
        self.image = image
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale_by(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)
    
class Sprite_UI(pygame.sprite.Sprite):
    """
    Class representing a Sprite UI object in the game world.
    """
    def __init__(self, x, y, image):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.base_image = image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.active = True
        
        
    def get_rect(self):
        return self.rect   
    
    def set_active(self, bool):
        self.active = bool
    def update_position(self, pos):
        self.rect.topleft = pos
                
    def change_color(self):
        if not self.active:
            gray_image = pygame.Surface(self.image.get_size())
            gray_image.fill((0,0,0))
            self.image = self.base_image.copy()
            self.image.blit(gray_image, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        else:
            gray_image = pygame.Surface(self.image.get_size())
            gray_image.fill((100,100,100))
            self.image = self.base_image.copy()
            self.image.blit(gray_image, (0,0), special_flags=pygame.BLEND_RGBA_MULT)


