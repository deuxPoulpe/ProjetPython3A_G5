import random
import pygame

class Bob:
    def __init__(self, energy = 100, velocity = 1, mass = 1, perception = 0, memory_space = 0, max_energy = 200, position = (random.randrange(1,100), random.randrange(1,100)), world, en_fuite = False):
        self.energy = energy
        self.velocity = velocity
        self.mass = mass
        self.perception = perception
        self.memory_space = memory_space
        self.max_energy = max_energy
        self.position = position
        self.en_fuite = en_fuite
        self.world = world


  
    def __str__(self):
        return f"Bob {self.position} {self.velocity} {self.mass} {self.energy} {self.perception} {self.memory_space} {self.en_fuite} {self.world} {self.max_energy}"
    

    def move(self)