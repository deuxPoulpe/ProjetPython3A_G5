import os
import pygame
import pickle
from terrain import Terrain
from bob import Bob



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

	

	def update_tick(self ):
		
		#une journée en fonction des ticks 
		
		journe = 100 * tick
		
		#tick
		for bob in self.bobs.values():
				for b in bob :
					b.updtate.tick
		
		
		for bob in self.bobs.values():
			for b in bob:
				if b == 0 :
					kill_bob(b)	
		
		#journee passé
		if self.tick % 100 == 0 :
			for food in self.foods.values():
				for f in food:
					f.spaw()
		
			
			


		
		
		
		tick += 1

		