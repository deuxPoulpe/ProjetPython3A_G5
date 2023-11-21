class Food:
	"""
	Classe représentant un objet nourriture dans le monde du jeu.

	Attributs:
		value (int): Valeur nutritive de la nourriture.
		pos (tuple): Position de la nourriture (x, y) dans le monde.
		world (World): Référence au monde dans lequel la nourriture est située.
		type (str): Type de la nourriture (par exemple, "banane").
	"""

	def __init__(self, x, y, world, type="banane", value=100):
		"""
		Initialise une nouvelle instance de nourriture.

		Paramètres:
			x (int): Position en x de la nourriture.
			y (int): Position en y de la nourriture.
			world (World): Référence au monde dans lequel la nourriture est située.
			type (str, optionnel): Type de la nourriture. Par défaut à "banane".
			value (int, optionnel): Valeur nutritive de la nourriture. Par défaut à 100.
		"""
		self.value = value
		self.pos = (x, y)
		self.world = world
		self.type = type

	def get_value(self):
		return self.value

	def add_value(self, value):
		self.value += value

	def get_pos(self):
		return self.pos

	def be_eaten(self, value):
		"""
		Méthode appelée lorsqu'un objet 'Bob' mange cette nourriture. Diminue la valeur nutritive de la nourriture 
		et la supprime du monde si elle est entièrement consommée.

		Paramètres:
			value (int): Quantité de nourriture consommée.

		Retourne:
			int: Quantité de nourriture réellement consommée.
		"""
		if self.value - value <= 0:
			self.world.kill_food(self)
			return self.value
		else:
			self.value -= value
			return value
