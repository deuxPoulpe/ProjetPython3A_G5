import numpy as np
import matplotlib.pyplot as plt
import random
from noise import snoise2
from perlin_noise import PerlinNoise


from math import sin

def noise(size ,z_min , z_max):
	terrain = np.random.uniform(z_min,z_max,size=(size,size))
	# terrain = np.convolve(terrain, np.ones((3,3)), mode='same')
	return terrain

def generate_terrain(size, scale=0.02, octaves=2, persistence=0.3, lacunarity=2.0, z_min=0, z_max=9):

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

	# ligne aleatoire
	for _ in range(1):
				p0 = (random.randint(0, size-1), random.randint(0, size-1))
				p1 = (random.randint(0, size-1), random.randint(0, size-1))  # Point de contrôle
				p2 = (random.randint(0, size-1), random.randint(0, size-1))

				lake = [(random.randint(0, size-1), random.randint(0, size-1))]

				courbe = lake
				courbe = trace_courbe_bezier(p0, p1, p2)	
				courbe = ondulation(courbe)	
				courbe = add_points(add_points(add_points(courbe)))	
				for x, y in courbe:
					try:
						terrain[int(x)][int(y)] = 0
					except:
						pass
			
				terrain = smooth_around_line(terrain, courbe, depth=4)

	return terrain

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

def bezier_curve(p0, p1, p2, t):
			x = int(round((1 - t) * (1 - t) * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]))
			y = int(round((1 - t) * (1 - t) * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
			return x, y
		
def trace_courbe_bezier(p0, p1, p2):
	return [bezier_curve(p0, p1, p2, t) for t in np.linspace(0, 1, 100)]

def ondulation(courbe, amplitude=10, frequence=0.2):
	return [(x, int(y + amplitude * sin(frequence * x))) for x, y in courbe]



def smooth_around_line(terrain, ligne, depth=4):
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




def display_terrain(terrain):
	plt.imshow(terrain, cmap='terrain')
	plt.colorbar()
	plt.show()


def perlin_noise(size):

	seed = random.randint(0, 1024)
	noise = PerlinNoise(octaves=4, seed=seed)
	additionnal_noise = PerlinNoise(octaves=13, seed=seed)
	grid = np.zeros((size, size))

	for i in range(size):
		for j in range(size):
			grid[i][j] = noise([i/size, j/size])
			grid[i][j] += 0.1 * additionnal_noise([i/size, j/size])

	grid = np.interp(grid, (grid.min(), grid.max()), (0, 10))
	grid = np.add(grid, 2)
	grid = np.round(grid).astype(int)

	return grid

# terrain = generate_terrain(100)
# display_terrain(terrain)
# display_terrain(noise(100,0, 10))


display_terrain(perlin_noise(100))

