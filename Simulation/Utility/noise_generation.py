import numpy as np
import random
from perlin_noise import PerlinNoise




def perlin_noise(size, z_min, z_max, scale, seed):
	"""
    Génère un terrain en utilisant une variante du bruit de Perlin.

    :param size: Taille du terrain.
    :param z_min: Valeur minimale de la hauteur du terrain.
    :param z_max: Valeur maximale de la hauteur du terrain.
    :param scale: Échelle du bruit de Perlin.
    :param seed: Graine pour la génération aléatoire.
    :return: Un tableau numpy représentant les hauteurs du terrain.
    """
	
	if seed is None:
		seed = random.randint(0, 1024)

	noise = PerlinNoise(octaves=4, seed=seed)
	additionnal_noise = PerlinNoise(octaves=10, seed=seed)
	terrain = np.zeros((size, size))

	for i in range(size):
		for j in range(size):
			x = i*scale
			y = j*scale
			terrain[i][j] = noise([x, y])
			terrain[i][j] += 0.2 * additionnal_noise([x, y])
	terrain = np.interp(terrain, (terrain.min(), terrain.max()), (z_min, z_max))
	terrain = np.add(terrain, 2)
	terrain = np.round(terrain).astype(int)


	return terrain