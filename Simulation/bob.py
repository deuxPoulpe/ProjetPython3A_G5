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

	def __init__(self, x, y, world, energy=100, velocity=1, mass=1, perception=0, max_energy=200):
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

	
	def eat_food(self):
		"""
		Permet à Bob de manger. Augmente l'énergie de Bob si de la nourriture est disponible à sa position.

		Retourne:
			bool: True si Bob a mangé, False sinon.
		"""
		if self.get_pos() in self.world.get_foods().keys() and self.energy != self.max_energy:
			food = self.world.get_foods()[self.get_pos()]
			self.energy += food.be_eaten(min(food.get_value(), self.max_energy - self.energy))
			return True
		else:
			return False

	def loose_energy(self, mode):
		if mode == "move":
			self.energy -= self.mass * self.velocity**2
		elif mode == "stand":
			self.energy -= 0.5
			
		

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
		self.loose_energy("move")
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
		actions = [self.die, self.reproduce, self.move]
		sub_actions = [self.eat_food]
		for action in actions:
			if action():
				if action.__name__ == "move":
					for sub_action in sub_actions:
						sub_action()
						break

				break
