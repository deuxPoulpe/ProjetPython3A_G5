class Food:
	"""
    Class representing a food object in the game world.

    Attributes:
        value (int): Nutritional value of the food.
        pos (tuple): Position of the food (x, y) in the world.
        world (World): Reference to the world where the food is located.
        type (str): Type of the food (e.g., "banana").
    """

	def __init__(self, x, y, world, type="banane", value=100):
		"""
        Initializes a new instance of food.

        Parameters:
            x (int): X-axis position of the food.
            y (int): Y-axis position of the food.
            world (World): Reference to the world where the food is located.
            type (str, optional): Type of the food. Default is "banana".
            value (int, optional): Nutritional value of the food. Default is 100.
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
        Method called when a 'Bob' object eats this food. Decreases the nutritional value of the food 
        and removes it from the world if it is entirely consumed.

        Parameters:
            value (int): Amount of food consumed.

        Returns:
            int: Amount of food actually consumed.
        """
		if self.value - value <= 0:
			self.world.kill_food(self)
			return self.value
		else:
			self.value -= value
			return value
		