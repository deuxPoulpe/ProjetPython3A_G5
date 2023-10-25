import os
import pygame
import pickle
from terrain import Terrain
from bob import Bob
from food import Food
import random


class World:
	def __init__(self,argDict,terrain_config_dict):
		self.argDict = argDict
		self.terrain_config = terrain_config_dict
		self.bobs = {}
		self.foods = {}
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
	def get_terrain_config(self):
		return self.terrain_config
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
	def move_bob(self,bob,old_x,old_y):
		pass
	
	def kill_bob(self,bob):
		self.bobs[bob.get_pos()].remove(bob)
		pass

	def kill_food(self,food):
		pass

	def update_tick(self):
		pass

	def spawn_bob(self,num_bobs):
		for _ in range(num_bobs):
			x = random.randint(0,self.argDict["size"]-1)  # Génération aléatoire de la coordonnée X
			y = random.randint(0,self.argDict["size"]-1)  # Génération aléatoire de la coordonnée Y
			bob=Bob(x, y, self)
			if (x,y) not in self.bobs:
				self.bobs[(x,y)]=[]
			self.bobs[(x,y)].append(bob)	

	def spawn_food(self,num_food):
		for _ in range(num_food):
			x = random.randint(0,self.argDict["size"]-1)  # Génération aléatoire de la coordonnée X
			y = random.randint(0,self.argDict["size"]-1)  # Génération aléatoire de la coordonnée Y
			food=Food(x, y, self)
			if (x,y) not in self.foods:
				self.foods[(x,y)]=[]
			self.foods[(x,y)].append(food)             


	def spawn_reproduce(self,mother_bob):
		new_born = Bob(mother_bob.get_pos()[0],mother_bob.get_pos()[1],self.world,energy = mother_bob.get_energy()*1/4)
		new_born_pos = new_born.get_pos()
		if not new_born_pos in self.bobs:
			self.bobs[new_born_pos] = []
		self.bobs[new_born_pos].append(new_born)


	def save(self,filename,*args):
		with open(filename, 'wb') as output:
			for i in args:
				pickle.dump(i, output, pickle.HIGHEST_PROTOCOL)
				print("saved",i)
		output.close()