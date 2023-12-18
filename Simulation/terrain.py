import numpy as np
import random
from math import sin
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

		self.generation_point = {}


		self.decoration_to_add = np.zeros((size, size))
		self.terrain = np.zeros((size, size))

		self.generate_terrain(size,z_max = config_dict["max_height"])	
		

	def generate_terrain(self ,size, z_min=0, z_max=9, seed = None):

		
		self.terrain = perlin_noise(size, z_min, z_max, 0.01, seed)

		
		
		for _ in range(random.randint(size , size*2)):
			x = random.randint(0,size-1)
			y = random.randint(0,size-1)
			self.decoration_to_add[x][y] = 1

		if self.generate_river:
			for k in range(self.number_of_river):
				p0 = (random.randint(0, size-1), random.randint(0, size-1))
				p1 = (random.randint(0, size-1), random.randint(0, size-1))  # Point de contrôle
				p2 = (random.randint(0, size-1), random.randint(0, size-1))
				p3 = (random.randint(0, size-1), random.randint(0, size-1))

		
				self.generation_point[f"river_{k}"] = [p0,p1,p2]
				
				courbe = trace_courbe_cubic_bezier(p0, p1, p2, p3)
				courbe = ondulation(courbe)		
				courbe = add_points(add_points(add_points(courbe)))
				for x, y in courbe:
					try:
						self.terrain[int(x)][int(y)] = 0
					except:
						pass
			
				self.terrain = smooth_around_line(self.terrain.copy(), courbe, depth=4)

		if self.generate_lake:
			for k in range(self.number_of_lake):
				center_lake = (random.randint(0, size-1), random.randint(0, size-1))
				lake = [center_lake, (center_lake[0]+random.randint(-2,2), center_lake[1]+random.randint(-2,2))]
				self.generation_point[f"lake_{k}"] = lake
				try:
					for x, y in lake:
						self.terrain[int(x)][int(y)] = 0
				except:
					pass
		

				self.terrain = smooth_around_line(self.terrain.copy(), lake, self.size_of_lake)

				for k in range(random.randint(1, self.size_of_lake)):
					rand_x = random.randint(-1,1)*k
					rand_y = random.randint(-1,1)*k
					try:
						if self.terrain[lake[0][0]+rand_x][lake[0][1]+rand_y] == 0:
							self.decoration_to_add[lake[0][0]+rand_x][lake[0][1]+rand_y] = 2
					except:
						pass
				





	def get_terrain(self):
		return self.terrain
	def get_decoration_to_add(self):
		return self.decoration_to_add
	def get_generation_point(self):
		return self.generation_point
