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

		self.terrain = terrain.copy()

		if self.generate_river:
			co1 = (random.randint(0,size-1),random.randint(0,size-1))
			co2 = (random.randint(0,size-1),random.randint(0,size-1))
			ligne = self.trace_line(co1,co2)
			for i in ligne:
				terrain[i[0]][i[1]] = 0
			self.terrain = self.smooth_around_line(terrain, ligne)

		for i in range(random.randint(size , size*2)):
			x = random.randint(0,size-1)
			y = random.randint(0,size-1)
			self.plant_to_add[x][y] = 1


		

	def smooth_around_line(self, terrain, ligne, depth=3):
		smoothed_terrain = terrain.copy()
		
		for x, y in ligne:
			for dx in range(-depth, depth+1):
				for dy in range(-depth, depth+1):
					dist = np.sqrt(dx*dx + dy*dy)
					if dist == 0:
						continue
					
					xi, yi = x + dx, y + dy
					if 0 <= xi < terrain.shape[0] and 0 <= yi < terrain.shape[1]:
						factor = (dist / depth)**2
						smoothed_terrain[xi, yi] = min(smoothed_terrain[xi, yi], terrain[xi, yi] * factor)
		
		return smoothed_terrain


	def trace_line(self, start, end):
		x1, y1 = start
		x2, y2 = end
		dx = x2 - x1
		dy = y2 - y1

		pente = abs(dy) > abs(dx)
		if pente:
			x1, y1 = y1, x1
			x2, y2 = y2, x2
			dx, dy = dy, dx

		if x2 < x1:
			x1, x2 = x2, x1
			y1, y2 = y2, y1

		delta_error = abs(dy)
		error = 0
		y = y1
		y_step = 1 if y1 < y2 else -1

		line = []
		for x in range(x1, x2 + 1):
			if pente:
				line.extend([(x, y), (x, y+1), (x, y-1), (x+1, y), (x-1, y)])

			else:
				line.extend([(x, y), (x, y+1), (x, y-1), (x+1, y), (x-1, y)])


			error += delta_error
			if (error << 1) > dx:
				y += y_step
				error -= dx

		return line
	

	def get_terrain(self):
		return self.terrain
	def get_plant_to_add(self):
		return self.plant_to_add
