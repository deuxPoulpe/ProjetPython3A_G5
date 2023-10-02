import numpy as np
import matplotlib.pyplot as plt
import random
from noise import snoise2



def generate_terrain(size, scale=0.02, octaves=6, persistence=0.3, lacunarity=2.0, z_min=0, z_max=10):

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
    terrain = np.round(terrain).astype(int)

    return terrain


def display_terrain(terrain):
    plt.imshow(terrain, cmap='terrain')
    plt.colorbar()
    plt.show()

terrain = generate_terrain(100)
display_terrain(terrain)
