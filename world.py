import os
import pygame
from terrain import Terrain



class World:
	def __init__(self,argDict,terrain_config_dict):
		self.argDict = argDict
		self.terrain_config = terrain_config_dict
		self.bobs = {}
		self.foods = {}
		self.spriteBob = pygame.image.load(os.path.join("assets","bob.png"))
		self.spriteFood = pygame.image.load(os.path.join("assets","food.png"))
		self.tick = 0
		self.population_bob = []
		self.population_food = []
		if self.argDict["custom_terrain"]:
			self.terrain = Terrain(self.argDict["size"], self.terrain_config)
		else:
			self.terrain = None


		assert all([type(argDict["size"]) == int ,
		type(argDict["nbFood"]) == int ,
		type(argDict["dayTick"]) == int
		])
	#exemple argDict:

	# argDict = {
	# 	"size" : size (100),
	# 	"nbFood" : nbFood (200),
	# 	"dayTick" : dayTick (100),
	# 	"custom_terrain" : True,   #si True ajoute un bruite a la generation de terrain
	# }


	#getters
	def get_size(self):
		return self.argDict["size"]
	def get_populationBob(self):
		return self.population_bob
	def get_populationFood(self):
		return self.population_food
	def get_tick(self):
		return self.tick
	def get_argDict(self):
		return self.argDict
	def get_bobs(self):
		return self.bobs
	def get_foods(self):
		return self.foods
	def get_argDict(self):
		return self.argDict
	def get_terrain(self):
		return self.terrain

	#setter
	def setArgDict(self,newArgDict):
		self.argDict = newArgDict


	#methods

	def kill_bob(self,bob):
		pass

	def kill_food(self,food):
		pass

	def update_tick(self):
		pass

	def spawn_bob(self,nb):
		pass

	def spawn_food(self,nb):
		pass

	def spawn_reproduce(self,mother_bob):
		pass

	def save(self):
		pass