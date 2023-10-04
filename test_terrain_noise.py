import numpy as np
import matplotlib.pyplot as plt
import random
from noise import snoise2
from math import sin
from math import cos



def generate_terrain(size, scale=0.02, octaves=6, persistence=0.3, lacunarity=2.0, z_min=0, z_max=20):

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
				
				courbe = trace_courbe_bezier(p0, p1, p2)	
				courbe = ondulation(courbe)		
				for x, y in courbe:
					try:
						terrain[int(x)][int(y)] = 0
					except:
						pass
			
				terrain = smooth_around_line(terrain, courbe, depth=7)

	return terrain



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

terrain = generate_terrain(100)
display_terrain(terrain)
