import random
import pygame
from world import World

class Bob:
    def __init__(self, x, y, world ,energy = 100, velocity = 1, mass = 1, perception = 0, max_energy = 200,):
        self.energy = energy
        self.velocity = velocity
        self.mass = mass
        self.perception = perception
        self.memory_space = []
        self.max_energy = max_energy
        self.position = (x,y)
        self.en_fuite = False
        self.world = world

        #(random.randrange(1,100), random.randrange(1,100) : pour la position


  
    def __str__(self):
        return f"Bob {self.position} {self.velocity} {self.mass} {self.energy} {self.perception} {self.memory_space} {self.en_fuite} {self.world} {self.max_energy}"
    

    def move(self): #fonction de déplacement du bob
        pass

    def eat(self):
        pass


    def die(self):
        pass
        
    def self_reproduction(self):
        pass
        
    def reproduction(self):
        pass

    