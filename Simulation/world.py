
import pickle
from terrain import Terrain
from bob import *
from food import Food
import random

from Utility.time_function_utility import execute_function_after_it


class World:
	
	"""
    Class representing the world in which 'Bob' and 'Food' objects interact.

    Attributes:
        argDict (dict): Dictionary of world configuration arguments.
        terrain_config (dict): Dictionary of terrain configuration.
        bobs (dict): Dictionary of 'Bob' objects present in the world.
        foods (dict): Dictionary of food items present in the world.
        tick (int): Tick counter in the world.
        population_bob (list): List of 'Bob' population.
        population_food (list): List of food population.
        nb_bob (int): Number of 'Bob' in the world.
        nb_food (int): Number of food items in the world.
        terrain (Terrain): Object representing the world's terrain.
    """
	def __init__(self,argDict,terrain_config_dict):
		"""
        Initializes a new instance of the world.

        Parameters:
            argDict (dict): Dictionary of world configuration arguments.
            terrain_config_dict (dict): Dictionary of terrain configuration.
        """
		self.argDict = argDict
		self.terrain_config = terrain_config_dict
		self.bobs = {}
		self.foods = {}
		self.tick = 0
		self.population_bob = []
		self.population_food = []
		self.nb_bob = 0
		self.nb_food = 0
		self.mutation = self.argDict["bob_mutation"]
		self.water_level = terrain_config_dict["water_level"]
		if self.argDict["custom_terrain"]:
			self.terrain = Terrain(self.argDict["size"], self.terrain_config)
		else:
			self.terrain = None

		self.enable_function = self.argDict["toggle_fonction"]
		self.enabled_event = 0
		self.event_timer_day_tick = self.argDict["event_days_rate"]

		self.event_type = ["flood","drought"]


	#getters
	def get_water_level(self):
		return self.water_level
	def get_size(self):
		return self.argDict["size"]
	def get_terrain_config(self):
		return self.terrain_config
	def get_population_Bob(self):
		return self.population_bob
	def get_population_Food(self):
		return self.population_food
	def get_tick(self):
		return self.tick
	def get_argDict(self):
		return self.argDict
	def get_bobs(self):
		return self.bobs
	def get_foods(self):
		return self.foods
	def get_terrain(self):
		return self.terrain
	def get_nb_bob(self):
		return self.nb_bob
	def get_nb_food(self):
		return self.nb_food
	def get_mutation(self):
		return self.mutation

	#setter
	def setArgDict(self,newArgDict):
		self.argDict = newArgDict


	#methods
	
	def move_bob(self,bob,old_x,old_y):
		"""
        Moves a 'Bob' in the world.

        Parameters:
            bob (Bob): The instance of 'Bob' to move.
            old_x (int): Old x-coordinate.
            old_y (int): Old y-coordinate.
        """
  
		self.bobs[(old_x,old_y)].remove(bob)
		if self.bobs[(old_x,old_y)] == []:
			self.bobs.pop((old_x,old_y))
   
		if not bob.get_pos() in self.bobs:
			self.bobs[bob.get_pos()] = []
		self.bobs[bob.get_pos()].append(bob)

	
	def kill_bob(self,bob):
		"""
        Removes a 'Bob' from the world.

        Parameters:
            bob (Bob): The instance of 'Bob' to remove.
        """
		self.bobs[bob.get_pos()].remove(bob)
		if self.bobs[bob.get_pos()] == []:
			self.bobs.pop(bob.get_pos())

		self.nb_bob -= 1

	def kill_food(self,food):
		"""
        Removes a food item from the world.

        Parameters:
            food (Food): The food item to remove.
        """
		
		self.foods.pop(food.get_pos())

		self.nb_food -= 1


	def spawn_bob(self, num_bobs, energy=-1, velocity=-1, mass=-1, perception=-1, memory_points=-1, max_energy=-1):
		"""
        Generates a specified number of 'Bob' in the world.

        Parameters:
            num_bobs (int): Number of 'Bob' to generate.
        """
		# If no value is specified, use the default value
		energy = self.argDict["bob_energy"] if energy == -1 else energy
		velocity = self.argDict["bob_velocity"] if velocity == -1 else velocity
		mass = self.argDict["bob_mass"] if mass == -1 else mass
		perception = self.argDict["bob_perception"] if perception == -1 else perception
		memory_points = self.argDict["bob_memory_point"] if memory_points == -1 else memory_points
		max_energy = self.argDict["bob_max_energy"] if max_energy == -1 else max_energy


		for _ in range(num_bobs):
			x = random.randint(0,self.argDict["size"]-1)  # Génération aléatoire de la coordonnée X
			y = random.randint(0,self.argDict["size"]-1)  # Génération aléatoire de la coordonnée Y
			bob=Bob(x, y, self, velocity=velocity, mass = mass, perception = perception, memory_points = memory_points, energy=energy, max_energy=max_energy)

			if (x,y) not in self.bobs:
				self.bobs[(x,y)]=[]
			self.bobs[(x,y)].append(bob)

		self.nb_bob += num_bobs
  
	

	def spawn_food(self,num_food):
		"""
        Generates a specified number of food items in the world.

        Parameters:
            num_food (int): Number of food items to generate.
        """
		for _ in range(num_food):
			x = random.randint(0,self.argDict["size"]-1)  # Génération aléatoire de la coordonnée X
			y = random.randint(0,self.argDict["size"]-1)  # Génération aléatoire de la coordonnée Y
			food=Food(x, y, self, value=self.argDict["Food_energy"])

			 

			if (x,y) not in self.foods:
				self.foods[(x,y)] = food
			else:
				self.foods[(x,y)].add_value(food.get_value())

		self.nb_food += num_food

	def spawn_reproduce(self,mother_bob):
		"""
        Manages the reproduction of 'Bob'. Creates a new 'Bob' from an existing 'Bob'.

        Parameters:
            mother_bob (Bob): The 'Bob' that is reproducing.
        """
		if random.random() < self.mutation :
	
			child_velocity = random.uniform(1 - self.mutation, 1 + self.mutation)
		
		child_velocity = 1
		
		mutation = random.choice([-1, 0, 1])
		child_perception = mother_bob.get_perception() + mutation
		child_perception = max(0, child_perception)

		memory_points = random.choice([-1, 0, 1])
		child_memory = mother_bob.get_memory_points() + memory_points
		child_memory = max(0, child_memory)


		new_born = Bob(mother_bob.get_pos()[0],mother_bob.get_pos()[1],self,energy = 50, velocity = child_velocity, perception= child_perception, memory_points=child_memory)
		
		new_born_pos = new_born.get_pos()
		if not new_born_pos in self.bobs:
			self.bobs[new_born_pos] = []
		self.bobs[new_born_pos].append(new_born)

		self.nb_bob += 1
		
		
	def spawn_sexuelreproduction(self,mother_bob,dad_bob):
		new_born= Bob(mother_bob.get_pos()[0],mother_bob.get_pos()[1],self,energy=100,mass=round(((mother_bob.get_mass()+dad_bob.get_mass())/2)),perception=round(((mother_bob.get_perception()+dad_bob.get_perception())/2)))
		new_born_pos = new_born.get_pos()
		if not new_born_pos in self.bobs:
			self.bobs[new_born_pos] = []
		self.bobs[new_born_pos].append(new_born)

		self.nb_bob += 1

	def event_update(self):
		event_type_choice = random.choice(self.event_type)


		match event_type_choice:
			case "flood":
				self.water_level += 1
				bobs = self.bobs.copy()
				for pos in bobs:
					x,y = pos
					if self.terrain.get_terrain()[x][y] == self.water_level:
						for bob in bobs[pos]:
							self.kill_bob(bob)

			case "drought":
				if self.water_level >= 0:
					self.water_level -= 1
					
		return event_type_choice
				
	

	def update_tick(self):
		"""
		Updates the state of the world on each tick
		"""
		event = None
		
		#update tick for all bobs
		all_bobs_dict = self.bobs.copy()
		for bobs in all_bobs_dict.values():
			for bob in bobs :
				bob.update_tick()
		
		#journee passé
		if self.tick % self.argDict["dayTick"] == 0 :
			self.foods = {}
			self.spawn_food(self.argDict["nbFood"])
			self.nb_food = self.argDict["nbFood"]	
			if random.randint(0,10) == 1 and self.terrain and self.enable_function["custom_event"] and self.enabled_event == 0:
				event = self.event_update()
				self.enabled_event = self.event_timer_day_tick * self.argDict["dayTick"]
				
			
		#ajouter la population de bobs et de food dans des listes pour le graphique final
		self.population_bob.append(self.nb_bob)
		self.population_food.append(self.nb_food)
		
		if self.enabled_event > 0:
			self.enabled_event -= 1


		self.tick += 1

		return event
					

	def change_options(self, arg_dict, terrain_config_dict):
		"""
		Changes the configuration of the world.

		Parameters:
			arg_dict (dict): Dictionary of world configuration arguments.
			terrain_config_dict (dict): Dictionary of terrain configuration.
		"""
		
		if self.argDict["bob_max_energy"] != arg_dict["bob_max_energy"]:
			for key, bobs in self.get_bobs().items():
				for bob in bobs:
					bob.set_max_energy(arg_dict["bob_max_energy"])

		self.enable_function = arg_dict["toggle_fonction"]
		self.argDict = arg_dict
		self.terrain_config = terrain_config_dict
		if self.argDict["custom_terrain"]:
			self.terrain = Terrain(self.argDict["size"], self.terrain_config)
		else:
			self.terrain = None
		self.water_level = terrain_config_dict["water_level"]

		for key, bobs in self.get_bobs().items():
			for bob in bobs:
				if bob.get_pos()[0] >= self.argDict["size"] or bob.get_pos()[1] >= self.argDict["size"]:
					self.kill_bob(bob)



    

	