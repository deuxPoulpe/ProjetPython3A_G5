import numpy as np
from noise import snoise2
import random
from perlin_noise import PerlinNoise


def perlin_noise1(size, z_min, z_max, scale, octaves, persistence, lacunarity, seed):
	"""
    Génère un terrain en utilisant le bruit de Perlin.

    :param size: Taille du terrain (nombre de points en largeur et en hauteur).
    :param z_min: Valeur minimale de la hauteur du terrain.
    :param z_max: Valeur maximale de la hauteur du terrain.
    :param scale: Échelle du bruit de Perlin.
    :param octaves: Nombre d'octaves utilisées pour le bruit de Perlin.
    :param persistence: Persistance du bruit de Perlin.
    :param lacunarity: Lacunarité du bruit de Perlin.
    :param seed: Graine pour la génération aléatoire.
    :return: Un tableau numpy représentant les hauteurs du terrain.
    """

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


def perlin_noise2(size, z_min, z_max, scale, seed):
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