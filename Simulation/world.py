
import pickle
from terrain import Terrain
from bob import Bob
from food import Food
import random


class World:
	"""
	Classe représentant le monde dans lequel les objets 'Bob' et 'Food' interagissent.

	Attributs:
		argDict (dict): Dictionnaire d'arguments de configuration du monde.
		terrain_config (dict): Dictionnaire de configuration du terrain.
		bobs (dict): Dictionnaire des 'Bob' présents dans le monde.
		foods (dict): Dictionnaire de nourriture présente dans le monde.
		tick (int): Compteur de ticks dans le monde.
		population_bob (list): Liste de la population de 'Bob'.
		population_food (list): Liste de la population de nourriture.
		nb_bob (int): Nombre de 'Bob' dans le monde.
		nb_food (int): Nombre d'éléments de nourriture dans le monde.
		terrain (Terrain): Objet représentant le terrain du monde.
	"""
	def __init__(self,argDict,terrain_config_dict):
		"""
		Initialise une nouvelle instance du monde.

		Paramètres:
			argDict (dict): Dictionnaire d'arguments de configuration du monde.
			terrain_config_dict (dict): Dictionnaire de configuration du terrain.
		"""
		self.argDict = argDict
		self.terrain_config = terrain_config_dict
		self.bobs = {}
		self.foods = {}
		self.tick = 0
		self.population_bob = []
		self.population_food = []
		self.nb_bob = 0
		self.nb_food = 0
		if self.argDict["custom_terrain"]:
			self.terrain = Terrain(self.argDict["size"], self.terrain_config)
		else:
			self.terrain = None


		assert all([type(argDict["size"]) == int ,
		type(argDict["nbFood"]) == int ,
		type(argDict["dayTick"]) == int
		])
	#exemple argDict:

	# argDict = {
	# 	"size" : size (100),
	# 	"nbFood" : nbFood (200),
	# 	"dayTick" : dayTick (100),
	# 	"custom_terrain" : True,   #si True ajoute un bruite a la generation de terrain
	# }


	#getters
	def get_size(self):
		return self.argDict["size"]
	def get_terrain_config(self):
		return self.terrain_config
	def get_population_Bob(self):
		return self.population_bob
	def get_population_Food(self):
		return self.population_food
	def get_tick(self):
		return self.tick
	def get_argDict(self):
		return self.argDict
	def get_bobs(self):
		return self.bobs
	def get_foods(self):
		return self.foods
	def get_argDict(self):
		return self.argDict
	def get_terrain(self):
		return self.terrain

	#setter
	def setArgDict(self,newArgDict):
		self.argDict = newArgDict


	#methods
	def move_bob(self,bob,old_x,old_y):
		"""
		Déplace un 'Bob' dans le monde.

		Paramètres:
			bob (Bob): L'instance de 'Bob' à déplacer.
			old_x (int): Ancienne position en x.
			old_y (int): Ancienne position en y.
		"""
		self.bobs[(old_x,old_y)].remove(bob)
		if self.bobs[(old_x,old_y)] == []:
			self.bobs.pop((old_x,old_y))
		if not bob.get_pos() in self.bobs:
			self.bobs[bob.get_pos()] = []
		self.bobs[bob.get_pos()].append(bob)

	
	def kill_bob(self,bob):
		"""
		Supprime un 'Bob' du monde.

		Paramètres:
			bob (Bob): L'instance de 'Bob' à supprimer.
		"""
		self.bobs[bob.get_pos()].remove(bob)
		if self.bobs[bob.get_pos()] == []:
			self.bobs.pop(bob.get_pos())

		self.nb_bob -= 1

	def kill_food(self,food):
		"""
		Supprime un élément de nourriture du monde.

		Paramètres:
			food (Food): L'élément de nourriture à supprimer.
		"""
		self.foods[food.get_pos()].remove(food)
		if self.foods[food.get_pos()] == []:
			self.foods.pop(food.get_pos())

		self.nb_food -= 1


	def spawn_bob(self,num_bobs):
		"""
		Génère un nombre spécifié de 'Bob' dans le monde.

		Paramètres:
			num_bobs (int): Nombre de 'Bob' à générer.
		"""
		for _ in range(num_bobs):
			x = random.randint(0,self.argDict["size"]-1)  # Génération aléatoire de la coordonnée X
			y = random.randint(0,self.argDict["size"]-1)  # Génération aléatoire de la coordonnée Y
			bob=Bob(x, y, self)
			if (x,y) not in self.bobs:
				self.bobs[(x,y)]=[]
			self.bobs[(x,y)].append(bob)

		self.nb_bob += num_bobs

	def spawn_food(self,num_food):
		"""
		Génère un nombre spécifié d'éléments de nourriture dans le monde.

		Paramètres:
			num_food (int): Nombre d'éléments de nourriture à générer.
		"""
		for _ in range(num_food):
			x = random.randint(0,self.argDict["size"]-1)  # Génération aléatoire de la coordonnée X
			y = random.randint(0,self.argDict["size"]-1)  # Génération aléatoire de la coordonnée Y
			food=Food(x, y, self, value=self.argDict["Food_energy"])
			if (x,y) not in self.foods:
				self.foods[(x,y)] = food
			else:
				self.foods[(x,y)].add_value(food.get_value())

		self.nb_food += num_food

	def spawn_reproduce(self,mother_bob):
		"""
		Gère la reproduction des 'Bob'. Crée un nouveau 'Bob' à partir d'un 'Bob' existant.

		Paramètres:
			mother_bob (Bob): Le 'Bob' qui se reproduit.
		"""
		new_born = Bob(mother_bob.get_pos()[0],mother_bob.get_pos()[1],self,energy = mother_bob.get_energy()*1/4)
		new_born_pos = new_born.get_pos()
		if not new_born_pos in self.bobs:
			self.bobs[new_born_pos] = []
		self.bobs[new_born_pos].append(new_born)

		self.nb_bob += 1


	def save(self,filename,*args):
		"""
		Enregistre l'état actuel du monde dans un fichier.

		Paramètres:
			filename (str): Nom du fichier dans lequel enregistrer l'état.
			*args: Arguments supplémentaires ou objets à enregistrer.
		"""
		with open(filename, 'wb') as output:
			for i in args:
				pickle.dump(i, output, pickle.HIGHEST_PROTOCOL)
				print("saved",i)
		output.close()

	

	def update_tick(self):
		"""
		Met à jour l'état du monde à chaque tick. Cela inclut la mise à jour de tous les 'Bob' et la génération de nourriture.
		"""
		
		#une journée en fonction des ticks 
		
		
		#update tick for all bobs
		all_bobs_dict = self.bobs.copy()
		for bobs in all_bobs_dict.values():
			for bob in bobs :
				bob.update_tick()
		
		#journee passé
		if self.tick % self.argDict["dayTick"] == 0 :
			self.foods = {}
			self.spawn_food(self.argDict["nbFood"])
			self.nb_food = self.argDict["nbFood"]		
			
		#ajouter la population de bobs et de food dans des listes pour le graphique final
		self.population_bob.append(self.nb_bob)
		self.population_food.append(self.nb_food)

		self.tick += 1

		