import random
import pygame
import time

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


	def affichage_iso(self , update_interval):
		# Dimensions de la fenêtre
		window_width = 900
		window_height = 700

		# Initialisation de Pygame
		pygame.init()
		screen = pygame.display.set_mode((window_width, window_height))
		pygame.display.set_caption("Grille Isométrique")

		green = (0, 102, 51)
		black = (0, 0, 0)
		red = (255, 0, 0)

		
		cell_width = 4
		cell_height = 2

		# Position de départ pour dessiner la grille
		start_x = 450 
		start_y = 150

		running = True
		clock = pygame.time.Clock()

		last_update_time = pygame.time.get_ticks() 

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			screen.fill(green)

			for i in range(self.size):
				for j in range(self.size):
					# Calcul des coordonnées isométriques
					x = start_x + (i - j) * cell_width
					y = start_y + (i + j) * cell_height

					# Dessine une case vide
					pygame.draw.rect(screen, black, (x, y, cell_width, cell_height), 1)

					# Dessine les Bobs s'ils sont présents dans la case
					if any(isinstance(element, Bob) for element in self.grid[i][j]):
						pygame.draw.circle(screen, red, (x + cell_width // 2, y + cell_height // 2), 1)

			pygame.display.flip()

			current_time = pygame.time.get_ticks()
			if current_time - last_update_time >= update_interval:
				for bob in self.bobs:
					bob.move()
				last_update_time = current_time
			clock.tick(60)


	pygame.quit()

#####################################################################################
#																					#
#									Zone de Teste									#
#																					#
#####################################################################################




world1 = World(100)
for i in range(10):
	world1.spawn("bob")

world1.affichage_iso(100)