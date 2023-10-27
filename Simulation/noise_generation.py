import numpy as np
from noise import snoise2
import random
from perlin_noise import PerlinNoise


def perlin_noise1(size, z_min, z_max, scale, octaves, persistence, lacunarity, seed=None):
    	
    if seed is None:
        seed = random.randint(0, 1024)
    terrain = np.zeros((size, size))
    
    for x in range(size):
        for y in range(size):
            terrain[x][y] = snoise2(x*scale + seed, 
                                    y*scale + seed,
                                    octaves=octaves, 
                                    persistence=persistence, 
                                    lacunarity=lacunarity
            )

    terrain = np.interp(terrain, (terrain.min(), terrain.max()), (z_min, z_max))
    terrain = np.add(terrain, 2)
    terrain = np.round(terrain).astype(int)

    return terrain


def perlin_noise2(size, z_min, z_max, seed=None):
    
    if seed is None:
        seed = random.randint(0, 1024)

    noise = PerlinNoise(octaves=4, seed=seed)
    additionnal_noise = PerlinNoise(octaves=10, seed=seed)
    terrain = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            terrain[i][j] = noise([i/size, j/size])
            terrain[i][j] += 0.2 * additionnal_noise([i/size, j/size])

    terrain = np.interp(terrain, (terrain.min(), terrain.max()), (z_min, z_max))
    terrain = np.add(terrain, 2)
    terrain = np.round(terrain).astype(int)

    return terrain