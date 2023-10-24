import random
import pygame

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

	#getters

	def get_pos(self):
		return self.position
	def get_energy(self):
		return self.energy
	def get_mass(self):
		return self.mass


	def __str__(self):
		return f"Bob {self.position} {self.velocity} {self.mass} {self.energy} {self.perception} {self.memory_space} {self.en_fuite} {self.world} {self.max_energy}"
	

	def move(self): #fonction de déplacement du bob
		pass

	def eat(self):
		pass

	def in_case(self):
		pass

	def die(self):
		pass
		
	def self_reproduction(self):
		pass
		
	def reproduction(self):
		pass

	