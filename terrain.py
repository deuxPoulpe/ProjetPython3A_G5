import numpy as np
import matplotlib.pyplot as plt
import random
from noise import snoise2

class Terrain:

	def __init__(self,size,bool_river):
		self.size = size
		self.generate_river	= bool_river
		self.plant_to_add = np.zeros((size, size))
		self.terrain = np.zeros((size, size))
		self.generate_terrain(size)	
		

	def generate_terrain(self ,size, scale=0.02, octaves=10, persistence=0.3, lacunarity=2.0, z_min=0, z_max=10):

		terrain = np.zeros((size, size))
		random_seed = random.randint(0, 1024)
		
		for x in range(size):
			for y in range(size):
				terrain[x][y] = snoise2(x*scale + random_seed, 
										y*scale + random_seed,
										octaves=octaves, 
										persistence=persistence, 
										lacunarity=lacunarity
				)

		terrain = np.interp(terrain, (terrain.min(), terrain.max()), (z_min, z_max))
		terrain = np.add(terrain, 2)
		terrain = np.round(terrain).astype(int)


		def bezier_curve(p0, p1, p2, t):
			x = int(round((1 - t) * (1 - t) * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]))
			y = int(round((1 - t) * (1 - t) * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
			return x, y
		
		def trace_courbe_bezier(p0, p1, p2):
			return [bezier_curve(p0, p1, p2, t) for t in np.linspace(0, 1, 100)]
		

		if self.generate_river:
			p0 = (random.randint(0, size-1), random.randint(0, size-1))
			p1 = (random.randint(0, size-1), random.randint(0, size-1))  # Point de contrôle
			p2 = (random.randint(0, size-1), random.randint(0, size-1))
			
			courbe = trace_courbe_bezier(p0, p1, p2)			
			for x, y in courbe:
				terrain[int(x)][int(y)] = 0
			
			self.terrain = self.smooth_around_line(terrain, courbe)
		else:
			self.terrain = terrain.copy()

		for i in range(random.randint(size , size*2)):
			x = random.randint(0,size-1)
			y = random.randint(0,size-1)
			self.plant_to_add[x][y] = 1


		

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
	def get_plant_to_add(self):
		return self.plant_to_add
