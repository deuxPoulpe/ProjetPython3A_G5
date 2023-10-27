import numpy as np
import random
from math import sin
from noise_generation import perlin_noise1
from noise_generation import perlin_noise2


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

		

		# self.terrain = perlin_noise1(size, z_min, z_max, scale=0.02, octaves=10, persistence=0.3, lacunarity=2.0, seed)
		self.terrain = perlin_noise2(size, z_min, z_max, 0.01, seed)


		def bezier_curve(p0, p1, p2, t):
			x = int(round((1 - t) * (1 - t) * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]))
			y = int(round((1 - t) * (1 - t) * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
			return x, y
		
		def trace_courbe_bezier(p0, p1, p2):
			return [bezier_curve(p0, p1, p2, t) for t in np.linspace(0, 1, 100)]
		
		def ondulation(courbe, amplitude=9, frequence=0.2):
			return [(x, int(y + amplitude * sin(frequence * x))) for x, y in courbe]
			# return [( int(x + amplitude * sin(frequence * y)), int(y + amplitude * sin(frequence * x))) for x, y in courbe]

		
		def add_points(courbe):
			
			new_courbe = [courbe[0]]
			for i in range(1, len(courbe)):
				previous_point  = courbe[i - 1]
				current_point  = courbe[i]
				
				x = (previous_point[0] + current_point[0]) // 2
				y = (previous_point[1] + current_point[1]) // 2
				mid_point = (x, y)
				
				new_courbe.extend([mid_point, current_point])

			return new_courbe
		
		for _ in range(random.randint(size , size*2)):
			x = random.randint(0,size-1)
			y = random.randint(0,size-1)
			self.decoration_to_add[x][y] = 1

		if self.generate_river:
			for k in range(self.number_of_river):
				p0 = (random.randint(0, size-1), random.randint(0, size-1))
				p1 = (random.randint(0, size-1), random.randint(0, size-1))  # Point de contrôle
				p2 = (random.randint(0, size-1), random.randint(0, size-1))

				self.generation_point[f"river_{k}"] = [p0,p1,p2]
				
				courbe = trace_courbe_bezier(p0, p1, p2)
				courbe = ondulation(courbe)		
				courbe = add_points(add_points(add_points(courbe)))
				for x, y in courbe:
					try:
						self.terrain[int(x)][int(y)] = 0
					except:
						pass
			
				self.terrain = self.smooth_around_line(self.terrain.copy(), courbe, depth=4)

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
		

				self.terrain = self.smooth_around_line(self.terrain.copy(), lake, self.size_of_lake)

				for k in range(random.randint(1, self.size_of_lake)):
					rand_x = random.randint(-1,1)*k
					rand_y = random.randint(-1,1)*k
					try:
						if self.terrain[lake[0][0]+rand_x][lake[0][1]+rand_y] == 0:
							self.decoration_to_add[lake[0][0]+rand_x][lake[0][1]+rand_y] = 2
					except:
						pass


		


		

	def smooth_around_line(self, terrain, ligne, depth=4):
		smoothed_terrain = terrain.copy()
		
		for x, y in ligne:
			for dx in range(-depth, depth+1):
				for dy in range(-depth, depth+1):
					dist = np.sqrt(dx*dx + dy*dy)
				
					xi, yi = x + dx, y + dy
					if 0 <= xi < terrain.shape[0] and 0 <= yi < terrain.shape[1]:
						factor = (dist / depth)**2
						smoothed_terrain[xi, yi] = min(smoothed_terrain[xi, yi], terrain[xi, yi] * factor)
		
		return smoothed_terrain


	def get_terrain(self):
		return self.terrain
	def get_decoration_to_add(self):
		return self.decoration_to_add
	def get_generation_point(self):
		return self.generation_point
