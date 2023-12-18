import random

class Bob:
	"""
    Class representing a character 'Bob' in a simulated world.

    Attributes:
        energy (int): Bob's current energy.
        velocity (int): Bob's movement speed.
        mass (int): Bob's mass.
        perception (int): Bob's perception ability.
        memory_space (list): Bob's memory space.
        max_energy (int): The maximum energy Bob can accumulate.
        position (tuple): Bob's current position in the world (x, y).
        en_fuite (bool): Indicates whether Bob is fleeing.
        world (World): Reference to the world in which Bob exists.
    """

	def __init__(self, x, y, world, energy=100, velocity=1, mass=1, perception=0, max_energy=200):
		"""
        Initializes a new instance of Bob.

        Parameters:
            x (int): Initial position of Bob in the x-axis.
            y (int): Initial position of Bob in the y-axis.
            world (World): Reference to the world in which Bob exists.
            energy (int, optional): Initial energy of Bob. Default is 100.
            velocity (int, optional): Initial velocity of Bob. Default is 1.
            mass (int, optional): Initial mass of Bob. Default is 1.
            perception (int, optional): Initial perception of Bob. Default is 0.
            max_energy (int, optional): Maximum energy of Bob. Default is 200.
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
        Allows Bob to eat. Increases Bob's energy if food is available at his position.

        Returns:
            bool: True if Bob ate, False otherwise.
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
        Moves Bob to a new random position.

        Returns:
            bool: True after Bob's movement.
        """
		old_x, old_y = self.position
		dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
		new_x, new_y = old_x + dx, old_y + dy
		self.position = (max(0, min(new_x, self.world.get_size() - 1)),
						max(0, min(new_y, self.world.get_size() - 1)))
		self.world.move_bob(self, old_x, old_y)
		self.loose_energy("move")
		return True

	def die(self):
		"""
        Handles Bob's death. Bob dies if his energy is less than or equal to 0.

        Returns:
            bool: True if Bob dies, False otherwise.
        """
		if self.energy <= 0:
			self.world.kill_bob(self)
			return True
		else:
			return False

	def reproduce(self):
		"""
        Handles Bob's reproduction. Reproduction occurs if Bob's energy is sufficient.

        Returns:
            bool: True if reproduction occurs, False otherwise.
        """
		if self.energy >= self.max_energy:
			self.energy = 3 * self.energy // 4
			self.world.spawn_reproduce(self)
			return True
		else:
			return False

	def update_tick(self):
		"""
        Updates Bob's state at each 'tick' or time interval. Manages various actions like dying, eating, reproducing, and moving.

        Returns:
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
