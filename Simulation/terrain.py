import numpy as np
import random
from Utility.noise_generation import perlin_noise
from Utility.geometry_utility import *


class Terrain:

	def __init__(self,size,config_dict):
		self.size = size
		self.generate_river	= config_dict["generate_river"]
		self.number_of_river = config_dict["number_of_river"]
		self.generate_lake = config_dict["generate_lake"]
		self.number_of_lake = config_dict["number_of_lake"]
		self.size_of_lake = config_dict["size_of_lake"]
		self.seed = config_dict["seed"]
		self.height = config_dict["max_height"]
  
		self.new_generation = False
		self.generation_point = {}
			
		random.seed(self.seed)

		self.decoration_to_add = np.zeros((size, size))
		self.terrain = np.zeros((size, size))

		self.generate_terrain(size, self.height)	
		

	def generate_terrain(self ,size, z_max, z_min=0):

		if self.seed is None:
			self.seed = random.randint(0, 1024)
		
		self.terrain = perlin_noise(size, z_min, z_max, 0.01, self.seed)

		
		
		for _ in range(random.randint(size , size*2)):
			x = random.randint(0,size-1)
			y = random.randint(0,size-1)
			self.decoration_to_add[x][y] = 1
   
		if self.new_generation:
			for key, value in self.generation_point.items():
				if key.split("_")[0] == "river":
					self.create_river(*value)
				elif key.split("_")[0] == "lake":
					self.create_lake(value, size)
		else:

			if self.generate_river:
				for k in range(self.number_of_river):
					p0 = (random.randint(0, size-1), random.randint(0, size-1))
					p1 = (random.randint(0, size-1), random.randint(0, size-1))  # Point de contrôle
					p2 = (random.randint(0, size-1), random.randint(0, size-1))
					p3 = (random.randint(0, size-1), random.randint(0, size-1))

			
					self.generation_point[f"river_{k}"] = (p0,p1,p2,p3)
		
					self.create_river(p0,p1,p2,p3)
					
					

			if self.generate_lake:
				for k in range(self.number_of_lake):

					center_lake = (random.randint(0, size-1), random.randint(0, size-1))
					extend_lake_x = min(size - 1 , max(0 , center_lake[0]+random.randint(-2,2)))
					extend_lake_y = min(size - 1 , max(0 , center_lake[0]+random.randint(-2,2)))
					lake = (center_lake, (extend_lake_x,extend_lake_y))
					self.generation_point[f"lake_{k}"] = lake
					
					self.create_lake(lake, size)
					
						
  
	def create_river(self, p0, p1, p2, p3):
		courbe = trace_courbe_cubic_bezier(p0, p1, p2, p3)
		courbe = ondulation(courbe)		
		courbe = add_points(add_points(add_points(courbe)))
		for x, y in courbe:
			try:
				self.terrain[int(x)][int(y)] = 0
			except:
				pass
	
		self.terrain = smooth_around_line(self.terrain.copy(), courbe, radius=4)
  
	def create_lake(self, lake, size_terrain):
		for x, y in lake:
			self.terrain[int(x)][int(y)] = 0

		self.terrain = smooth_around_line(self.terrain.copy(), lake, self.size_of_lake)

		for k in range(random.randint(1, self.size_of_lake)):
			deco_x = min(size_terrain - 1, max(0 , random.randint(-1,1)*k + lake[0][0]))
			deco_y = min(size_terrain - 1, max(0 , random.randint(-1,1)*k + lake[0][1]))
			if self.terrain[deco_x][deco_y] == 0:
				self.decoration_to_add[deco_x][deco_y] = 2


	def get_terrain(self):
		return self.terrain
	def get_decoration_to_add(self):
		return self.decoration_to_add
	def get_generation_point(self):
		return self.generation_point

	def set_new_generation(self, bool):
		self.new_generation = bool
  
	def change_terrain_size(self, new_size):
		self.size = new_size
		self.generate_terrain(new_size, self.height)
