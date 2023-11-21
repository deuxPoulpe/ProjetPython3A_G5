import random

class Bob:
	"""
	Classe représentant un personnage 'Bob' dans un monde simulé.

	Attributs:
		energy (int): Énergie actuelle de Bob.
		velocity (int): Vitesse de déplacement de Bob.
		mass (int): Masse de Bob.
		perception (int): Capacité de perception de Bob.
		memory_space (list): Espace mémoire de Bob.
		max_energy (int): Énergie maximale que Bob peut accumuler.
		position (tuple): Position actuelle de Bob dans le monde (x, y).
		en_fuite (bool): État indiquant si Bob est en fuite.
		world (World): Référence au monde dans lequel Bob évolue.
	"""

	def __init__(self, x, y, world, energy=100, velocity=1, mass=1, perception=0, max_energy=200,velocity_buffer=0,case_to_move=0):
		"""
		Initialise une nouvelle instance de Bob.

		Paramètres:
			x (int): Position initiale en x de Bob.
			y (int): Position initiale en y de Bob.
			world (World): Référence au monde dans lequel Bob évolue.
			energy (int, optionnel): Énergie initiale de Bob. Par défaut à 100.
			velocity (int, optionnel): Vitesse initiale de Bob. Par défaut à 1.
			mass (int, optionnel): Masse initiale de Bob. Par défaut à 1.
			perception (int, optionnel): Perception initiale de Bob. Par défaut à 0.
			max_energy (int, optionnel): Énergie maximale de Bob. Par défaut à 200.
		"""
		self.energy = energy
		self.velocity = velocity
		self.mass = mass
		self.perception = perception
		self.memory_space = []
		self.max_energy = max_energy
		self.position = (x, y)
		self.en_fuite = False
		self.world = world

	def __str__(self):
		return f"Bob {self.position} {self.velocity} {self.mass} {self.energy} {self.perception} {self.memory_space} {self.en_fuite} {self.world} {self.max_energy}"


	def get_pos(self):
		return self.position

	def get_energy(self):
		return self.energy

	def get_mass(self):
		return self.mass

	
	def eat(self):
		"""
		Permet à Bob de manger. Augmente l'énergie de Bob si de la nourriture est disponible à sa position.

		Retourne:
			bool: True si Bob a mangé, False sinon.
		"""
		if self.get_pos() in self.world.get_foods() and self.energy != self.max_energy:
			food = max(self.world.get_foods()[self.get_pos()], key=lambda x: x.get_value())
			self.energy += food.be_eaten(min(food.get_value(), self.max_energy - self.energy))
			return True
		else:
			return False

	def move(self):
		"""
		Déplace Bob dans une nouvelle position aléatoire.

		Retourne:
			bool: True après le déplacement de Bob.
		"""
		old_x, old_y = self.position
		dx, dy = random.randint(-1, 1), random.randint(-1, 1)
		new_x, new_y = old_x + dx, old_y + dy
		self.position = (max(0, min(new_x, self.world.get_size() - 1)),
						max(0, min(new_y, self.world.get_size() - 1)))
		self.world.move_bob(self, old_x, old_y)
		self.energy -= 1
		return True

	def die(self):
		"""
		Gère la mort de Bob. Bob meurt si son énergie est inférieure ou égale à 0.

		Retourne:
			bool: True si Bob meurt, False sinon.
		"""
		if self.energy <= 0:
			self.world.kill_bob(self)
			return True
		else:
			return False

	def reproduce(self):
		"""
		Gère la reproduction de Bob. La reproduction a lieu si l'énergie de Bob est suffisante.

		Retourne:
			bool: True si la reproduction a lieu, False sinon.
		"""
		if self.energy >= self.max_energy:
			self.energy = 3 * self.energy // 4
			self.world.spawn_reproduce(self)
			return True
		else:
			return False

	def update_tick(self):
		"""
		Met à jour l'état de Bob à chaque 'tick' ou intervalle de temps. Gère diverses actions comme mourir, manger, se reproduire et se déplacer.

		Retourne:
			None
		"""
		actions = [self.die, self.eat, self.reproduce, self.move]
		for action in actions:
			if action():
				break
	
	def velocity_manager(self):

		self.case_to_move += abs(self.velocity)
		self.velocity_buffer += self.velocity-abs(self.velocity)
		if self.velocity_buffer > 0:
			self.velocity_buffer -= 1
			case_to_move += 1
	
	def eat_bob(self):
		copy_bobs = self.world.get_bobs()[self.get_pos()].remove(self).copy()
		mass_bob_list = [x.get_mass() for x in copy_bobs]
		bob=copy_bobs[mass_bob_list.index(min(mass_bob_list))]

		if (bob.get_mass()/self.get_mass())<(2/3):
			if (self.energy + bob.get_energy()/2*(1-bob.get_mass()/self.get_mass())) >= self.max_energy:
				self.energy = self.max_energy
			else:
				self.energy += bob.get_energy()/2*(1-bob.get_mass()/self.get_mass())
			self.world.kill_bob(bob)
			return True
		return False
	
	def bob_perception(self):
		"""
		Permet à Bob de percevoir son environnement. Retourne une liste d'objets autour de lui.
		"""
		
		#Génération d'une matrice carré de taille perception-1
		perception_list = []
		for x in range(self.get_pos()[0]-(self.perception-1),self.get_pos()[0]+self.perception):
			for y in range(self.get_pos()[1]-(self.perception-1),self.get_pos()[1]+self.perception):
				if (x,y) in self.world.get_foods():
					perception_list.append(self.world.get_foods()[(x,y)])
				if (x,y) in self.world.get_bobs():
					perception_list.append(self.world.get_bobs()[(x,y)])
		
		#Ajout des bords manquants
		y=self.get_pos()[1]
		for x in range(self.get_pos()[0]-(self.perception),self.get_pos()[0]+self.perception+1,2*self.perception):
			if (x,self.y) in self.world.get_foods():
					perception_list.append(self.world.get_foods()[(x,y)])
			if (x,self.y) in self.world.get_bobs():
					perception_list.append(self.world.get_bobs()[(x,y)])
		
		x=self.get_pos()[0]
		for y in range(self.get_pos()[1]-(self.perception),self.get_pos()[1]+self.perception+1,2*self.perception):
			if (x,self.y) in self.world.get_foods():
					perception_list.append(self.world.get_foods()[(x,y)])
			if (x,self.y) in self.world.get_bobs():
					perception_list.append(self.world.get_bobs()[(x,y)])

		return perception_list

