import random
import pygame
from world import World

class Bob:
    def __init__(self, energy = 100, velocity = 1, mass = 1, perception = 0, max_energy = 200, position = (x,y), world):
        self.energy = energy
        self.velocity = velocity
        self.mass = mass
        self.perception = perception
        self.memory_space = []
        self.max_energy = max_energy
        self.position = position
        self.en_fuite = False
        self.world = world

        #(random.randrange(1,100), random.randrange(1,100) : pour la position


  
    def __str__(self):
        return f"Bob {self.position} {self.velocity} {self.mass} {self.energy} {self.perception} {self.memory_space} {self.en_fuite} {self.world} {self.max_energy}"
    

    def move(self): #fonction de déplacement du bob

    def eat(self):


    def die(self):
        
    def self_reproduction(self):
        
    def reproduction(self):

    