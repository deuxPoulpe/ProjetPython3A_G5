import random
from food import Food

class Bob:
	def __init__(self, x, y,world, velocity=1, mass=1, perception=0, memory_space=0, energy=100, maxEnergy=200):
		self.x = x
		self.y = y
		self.velocity = velocity
		self.mass = mass
		self.perception = perception
		self.memory_space = memory_space
		self.energy = energy
		self.remembered_food = []
		self.world = world
		self.maxEnergy = maxEnergy

	def __str__(self):
		return str(print("Bob", self.x, self.y, self.velocity, self.mass, self.perception, self.memory_space, self.energy))

	def move(self):
		while True:
			r = random.randint(1,4)

			new_x, new_y = self.x, self.y

			if r == 1:  # Nord
				new_x -= 1
			elif r == 2:  # Ouest
				new_y -= 1
			elif r == 3:  # Sud
				new_x += 1
			elif r == 4:  # Est
				new_y += 1

			# Vérifie si les nouvelles coordonnées sont valides dans la grille
			if 0 <= new_x < len(self.world.grid) and 0 <= new_y < len(self.world.grid[0]):
				# Déplace le Bob en mettant à jour les coordonnées
	
				self.world.grid[self.x][self.y].remove(self)
				self.x = new_x
				self.y = new_y
				self.world.grid[new_x][new_y].append(self)
				self.energy -= 1
				break
		

	def eat(self):
		if any(isinstance(_, Food) for _ in self.world.grid[self.x][self.y]):
			for food in self.world.grid[self.x][self.y]:
				if isinstance(food, Food):
					if self.energy + food.food_value > self.maxEnergy:
						self.energy += food.beEaten(self.maxEnergy - self.energy)
					else:
						self.energy += food.beEaten(food.getFoodValue())



					break

	def self_reproduce(self):
		self.world.spawn("self_reproduce",(self.x,self.y))


	def getPos(self):
		return (self.x,self.y) #Retourne la position du Bob
	def getMaxEnergy(self):
		return self.maxEnergy
	
	def update_tick(self):
		if self.move():
			self.energy -= 1
		
		self.eat()

		if self.energy >= self.maxEnergy:
			self.self_reproduce()
			self.energy -= (1/4)*self.getMaxEnergy()

		if self.energy <= 0:
			self.world.addBobtokill(self)

