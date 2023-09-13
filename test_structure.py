import random

# Classe représentant un Bob
class Bob:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.velocity = 1
		self.mass = 1
		self.perception = 0
		self.memory_space = 0
		self.energy = 100
		self.remembered_food = []

	def move(self):
		pass

	def eat(self, food):
		pass

	def reproduce(self):
		pass

	
# Classe représentant le monde
class World:
	def __init__(self, size=100):
		self.size = size
		self.grid = [[[None] for i in range(size)] for i in range(size)]
		self.bobs = []

	def affichage(self):   #Fonction pour faire un affichage du world dans un terminal
		for i in range(self.size):
			for j in range(self.size):
				
				if any(isinstance(element, Bob) for element in self.grid[i][j]):
					print(sum(1 for element in self.grid[i][j] if isinstance(element, Bob)), end=" ")
				else:
					print(".", end=" ")
			print()  

	def spawn(self):  #Fonction qui fait spawn de maniere aléatoire un Bob

		x = random.randint(0,self.size-1)
		y = random.randint(0,self.size-1)
		bob = Bob(x,y)
		self.bobs.append(bob)   #Ajoute le Bob créé dans la liste de tout les Bobs
		self.grid[x][y].append(bob)     #Place le Bob dans le world

#####################################################################################
#																					#
#									Zone de Teste									#
#																					#
#####################################################################################


world1 = World(30)
for i in range(50):
	world1.spawn()

world1.affichage()


