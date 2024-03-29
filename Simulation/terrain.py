import numpy as np
import random
from Utility.noise_generation import perlin_noise
from Utility.geometry_utility import *


class Terrain:
	"""
		Represents the terrain of the simulation.
		This class is responsible for generating and managing the terrain of the game world,
		including features like rivers and lakes.
    """
	def __init__(self,size,config_dict):
		'''
        Initializes the terrain with a given size and configuration.

        Parameters:
            size (int): The size of the terrain.
            config_dict (dict): A dictionary containing terrain configuration like rivers, lakes, seed, etc.
        '''
		self.size = size
		self.generate_river	= config_dict["generate_river"]
		self.number_of_river = config_dict["number_of_river"]
		self.generate_lake = config_dict["generate_lake"]
		self.number_of_lake = config_dict["number_of_lake"]
		self.size_of_lake = config_dict["size_of_lake"]
		self.seed = config_dict["seed"]
		self.height = config_dict["max_height"]
  
		self.new_generation = False
		self.generation_point = {}
			
		random.seed(self.seed)

		self.decoration_to_add = np.zeros((size, size))#permet d'ajouter des décorations sur le terrain 
		self.terrain = np.zeros((size, size))

		self.generate_terrain(size, self.height)	
		random.seed()
		

	def generate_terrain(self ,size, z_max, z_min=0):
		'''
        Generates the terrain using Perlin noise and additional features like rivers and lakes.

        Parameters:
            size (int): Size of the terrain to generate.
            z_max (float): The maximum elevation of the terrain.
            z_min (float): The minimum elevation of the terrain, default is 0.
        '''

		#si la seed n'exitse pas alors on en créer une aléatoirement 
		if self.seed is None:
			self.seed = random.randint(0, 1024)
		
		self.terrain = perlin_noise(size, z_min, z_max, 0.01, self.seed)

		#point de génération spécifique (emplacement des éléments géographique )
		#génère des décoration aléatoie sur le terrain pour chaque coordonnées x et y 
		for _ in range(random.randint(size , size*2)):
			x = random.randint(0,size-1)
			y = random.randint(0,size-1)
			self.decoration_to_add[x][y] = 1

		#nouvelle génération  rivières/lacs est nécéssaire (spécifié par user) . donc on parcourt tous éléments stocké dans le dictionnaire des points de génération 
		if self.new_generation:
			for key, value in self.generation_point.items():
				if key.split("_")[0] == "river": #si le type est rivière a la clé alors on la créer avec la valeur stocker dans value 
					self.create_river(*value)
				elif key.split("_")[0] == "lake":# de meme avec les lacs 
					self.create_lake(value, size)
		
		#pas spécifié donc --> génération aléatoire
		else:

			if self.generate_river:
				for k in range(self.number_of_river):
					p0 = (random.randint(0, size-1), random.randint(0, size-1))
					p1 = (random.randint(0, size-1), random.randint(0, size-1))  # Point de contrôle
					p2 = (random.randint(0, size-1), random.randint(0, size-1))
					p3 = (random.randint(0, size-1), random.randint(0, size-1))
					#pour chaque rivière , génère aléatoirement des points de controle 
					#les points de controle sont utilisés pour definir une courbe cubique de bezier 
					#p0 et p3 sont les extremités de la courbe et p1 et p2 sont les points de controles 
					self.generation_point[f"river_{k}"] = (p0,p1,p2,p3)#stock les points de controle dans self.generation_point
		
					self.create_river(p0,p1,p2,p3)#en fonction des points de controle  créer chaque rivière 
					

			#genere un nombre specifie de riviere aleatoirement sur la map 
			if self.generate_lake:
				for k in range(self.number_of_lake):
					
					#va generer aleatoirement les caractèristiques du lac (centre , extremités)
					center_lake = (random.randint(0, size-1), random.randint(0, size-1))
					extend_lake_x = min(size - 1 , max(0 , center_lake[0]+random.randint(-2,2)))
					extend_lake_y = min(size - 1 , max(0 , center_lake[1]+random.randint(-2,2)))
					lake = (center_lake, (extend_lake_x,extend_lake_y))#création des données du lac 
					self.generation_point[f"lake_{k}"] = lake #ajout du lac au dicitonnaire a la clé associé lake_k
					
					self.create_lake(lake, size)#appelle la methode creat_lake qui va créer le lac avece les dimensions associé
					
						
	#creation de la rivière 
	def create_river(self, p0, p1, p2, p3):

		'''
        Creates a river in the terrain.

        Parameters:
            p0, p1, p2, p3 (tuple): Control points to define the path of the river.
        '''
		courbe = trace_courbe_cubic_bezier(p0, p1, p2, p3)#trajectoire de la rivière tracé avec une courbe de bezier cubique 
		courbe = ondulation(courbe)	#ajout d'irrégularité a la courbe 	
		courbe = add_points(add_points(add_points(courbe)))
		#parcours chaque point de la courbe générée et modifie les valeurs correspondante dans la matrice du terrain 
		for x, y in courbe:
			try:
				self.terrain[int(x)][int(y)] = 0#met les valeurs a 0 , permet d'avoir une meilleur vision sur la trajectoire de la rivière
			except:
				pass
		#enfin lisse le terrain autour de la riviere 
		self.terrain = smooth_around_line(self.terrain.copy(), courbe, radius=4)
  
	def create_lake(self, lake, size_terrain):
		'''
        Creates a lake in the terrain.

        Parameters:
            lake (tuple): Tuple containing the center and extent of the lake.
            size_terrain (int): Size of the terrain to ensure the lake fits within bounds.
        '''
		for x, y in lake:
			self.terrain[int(x)][int(y)] = 0

		self.terrain = smooth_around_line(self.terrain.copy(), lake, self.size_of_lake)
		#ajout des décorations autour du lac aléatoirement random ... -> nombre aleatoire en 1 et taille du lac inclus
		for k in range(random.randint(1, self.size_of_lake)):
			#k numero de la decoration dans la boucle 
			#min permet de garantir que la décoration soit dans les limites du terrain
			deco_x = min(size_terrain - 1, max(0 , random.randint(-1,1)*k + lake[0][0]))
			deco_y = min(size_terrain - 1, max(0 , random.randint(-1,1)*k + lake[0][1]))

			#si une decoration est une zone d'eau on lui ajoute 2(taille minimal different zone eau )
			if self.terrain[deco_x][deco_y] == 0:
				self.decoration_to_add[deco_x][deco_y] = 2


	def get_terrain(self):
		return self.terrain
	def get_decoration_to_add(self):
		return self.decoration_to_add
	def get_generation_point(self):
		return self.generation_point
	def get_height(self):
		return self.height

	def set_new_generation(self, bool):
		self.new_generation = bool
  
	def change_terrain_size(self, new_size):
		self.size = new_size
		self.generate_terrain(new_size, self.height)