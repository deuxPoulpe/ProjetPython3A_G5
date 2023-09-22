import random
from bob import Bob
from food import Food



# Classe représentant le monde
class World:
	def __init__(self, size=100):
		self.size = size
		self.grid = [[[] for _ in range(size)] for _ in range(size)]
		self.bobs = []
		self.foods = []
		self.tick = 0
		self.bobtokill = []

		self.population_data = []
		self.food_data = []

	# Getters
	def getGrid(self):
		return self.grid
	def getSize(self):
		return self.size
	def getBobs(self):
		return self.bobs
	def getFoods(self):
		return self.foods


	def addBobtokill(self,bob):
		self.bobtokill.append(bob)

	def kill_bob(self,bob):
		self.bobs.remove(bob)
		self.grid[bob.getPos()[0]][bob.getPos()[1]].remove(bob)

	def kill_food(self,food):
		self.foods.remove(food)
		self.grid[food.getPos()[0]][food.getPos()[1]].remove(food)


	def change_size(self, new_size):
		del_list = []

		for bob in self.bobs:
			if bob.getPos()[0] >= new_size or bob.getPos()[1] >= new_size:
				del_list.append(bob)

		for food in self.foods:
			if food.getPos()[0] >= new_size or food.getPos()[1] >= new_size:
				del_list.append(food)
			
		for element in del_list:
			if isinstance(element, Bob):
				self.kill_bob(element)
			elif isinstance(element, Food):
				self.kill_food(element)
		


		self.grid = [[[] for _ in range(new_size)] for _ in range(new_size)]
		self.size = new_size 
		for bob in self.bobs:
			self.grid[bob.getPos()[0]][bob.getPos()[1]].append(bob)
		for food in self.foods:
			self.grid[food.getPos()[0]][food.getPos()[1]].append(food)

	def spawn(self,mob,nb):  #Fonction qui fait spawn de maniere aléatoire un Bob
		if mob == "bob":
			for _ in range(nb):
				x = random.randint(0,self.size-1)
				y = random.randint(0,self.size-1)
				bob = Bob(x,y,self)
				self.bobs.append(bob)   #Ajoute le Bob créé dans la liste de tout les Bobs
				self.grid[x][y].append(bob)     #Place le Bob dans le world
		elif mob == "food":
			for _ in range(nb):
				x = random.randint(0,self.size-1)
				y = random.randint(0,self.size-1)
				food = Food(x,y,self)
				self.grid[x][y].append(food)
				self.foods.append(food)
		elif mob == "self_reproduce":
			x = nb[0]
			y = nb[1]
			bob = Bob(x,y,self,int((1/4)*self.bobs[0].getMaxEnergy()))
			self.bobs.append(bob)
			self.grid[x][y].append(bob)


	def tick_update(self): #Fonction appelé a chaque tick (tick_interval en seconde) 
		
		for bob in self.bobs:
			bob.update_tick()

		for bob in self.bobtokill:
			self.kill_bob(bob)
		self.bobtokill = []

		if self.tick % 100 == 0:
			foodtoremove = []
			for food in self.foods:
				foodtoremove.append(food)
			for food in foodtoremove:
				self.kill_food(food)		
			self.spawn("food",120)

		self.population_data.append(len(self.bobs))
		self.food_data.append(len(self.foods))	

		self.tick += 1
		


	
