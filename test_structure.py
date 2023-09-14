import random

# Classe représentant un Bob
class Bob:
	def __init__(self, x, y,world):
		self.x = x
		self.y = y
		self.velocity = 1
		self.mass = 1
		self.perception = 0
		self.memory_space = 0
		self.energy = 100
		self.remembered_food = []
		self.world = world

	def move(self):
		while True:
			r = random.randint(1,4)

			new_x, new_y = self.x, self.y  # Initialise les nouvelles coordonnées avec les coordonnées actuelles

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
				break
		

	def eat(self, food):
		pass

	def reproduce(self):
		pass

	def kill(self):
		# Retirer le Bob de la liste des Bobs dans le monde
		self.world.grid[self.x][self.y].remove(self)
        # Le supprimer de la liste des Bobs
		self.world.bobs.remove(self)

	def getPos(self):
		return (self.x,self.y) #Retourne la position du Bob

	
# Classe représentant le monde
class World:
	def __init__(self, size=100):
		self.size = size
		self.grid = [[[] for i in range(size)] for i in range(size)]
		self.bobs = []

	def affichage(self):   #Fonction pour faire un affichage du world dans un terminal
		for i in range(self.size):
			for j in range(self.size):
				if any(isinstance(element, Bob) for element in self.grid[i][j]):
					print(sum(1 for element in self.grid[i][j] if isinstance(element, Bob)), end=" ")
				else:
					print(".", end=" ")
			print()  

	def spawn(self,mob):  #Fonction qui fait spawn de maniere aléatoire un Bob
		if mob == "bob":
			x = random.randint(0,self.size-1)
			y = random.randint(0,self.size-1)
			bob = Bob(x,y,self)
			self.bobs.append(bob)   #Ajoute le Bob créé dans la liste de tout les Bobs
			self.grid[x][y].append(bob)     #Place le Bob dans le world

#####################################################################################
#																					#
#									Zone de Teste									#
#																					#
#####################################################################################


world1 = World(20)
for i in range(20):
	world1.spawn("bob")

# world1.affichage()

# world1.bobs[random.randint(0,len(world1.bobs)-1)].kill()

# print("=======================================")
# world1.affichage()

while True:
	
	world1.affichage()
	print("=======================================")
	for bob in world1.bobs:
		bob.move()
	input()