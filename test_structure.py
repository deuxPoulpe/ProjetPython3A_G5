import random
import pygame
camera_x = 0
camera_y = 0
zoom_factor = 100
zoom_speed = 10

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

	def move_all_bobs(self): 	#Fonction qui appelle la fonction .move() de tout les bobs dans world
		for bob in self.bobs:
			bob.move()

	def tick_update(self): #Fonction appelé a chaque tick (tick_interval en seconde) 
		self.move_all_bobs()
		


	def affichage_grid_iso(self, screen, start_x, start_y, cell_width, cell_height, ratio):
		green = (0, 102, 51)
		black = (0, 0, 0)
		red = (255, 0, 0)
		sprite_image = pygame.image.load("assets/bob.png")
		sprite_image = pygame.transform.scale(sprite_image, (ratio * 5, ratio * 5))

		# Calculez le coin supérieur gauche de la grille en fonction de la caméra
		grid_start_x = start_x - camera_x
		grid_start_y = start_y - camera_y

		for i in range(self.size):
			for j in range(self.size):
				# Calcul des coordonnées isométriques
				x = grid_start_x + (i - j) * (cell_width * zoom_factor / 100)
				y = grid_start_y + (i + j) * (cell_height * zoom_factor / 100)

				# Dessine une case vide
				lozenge_points = [
					(x + cell_width * zoom_factor / 100 / 2, y + cell_height * zoom_factor / 100 * 1.5),
					(x + cell_width * zoom_factor / 100 * 1.5, y + cell_height * zoom_factor / 100 / 2,),
					(x + cell_width * zoom_factor / 100 / 2, y - cell_height * zoom_factor / 100 / 2),
					(x - cell_width * zoom_factor / 100 / 2, y + cell_height * zoom_factor / 100 / 2,),
				]
				# Dessine les Bobs s'ils sont présents dans la case
				if any(isinstance(element, Bob) for element in self.grid[i][j]):
					bob = next((element for element in self.grid[i][j] if isinstance(element, Bob)), None)
					if bob:
						sprite_x = x 
						sprite_y = y - cell_height * zoom_factor / 200

						sprite_width = sprite_image.get_width() * zoom_factor / 100
						sprite_height = sprite_image.get_height() * zoom_factor / 100

						screen.blit(pygame.transform.scale(sprite_image, (int(sprite_width), int(sprite_height))), (sprite_x, sprite_y))

				pygame.draw.polygon(screen, black, lozenge_points, 1)




def pygame_screen(world , tick_interval):

	global zoom_factor, camera_x, camera_y

	dragging = False  
	drag_start = None

	# Dimensions de la fenêtre
	window_width = 1280
	window_height = 720

	# Initialisation de Pygame
	pygame.init()
	screen = pygame.display.set_mode((window_width, window_height))
	pygame.display.set_caption("Simulation of Bobs")

	green = (0, 102, 51)

	ratio = 100 // world.size

	cell_width = 1.5*ratio*4
	cell_height = 1.5*ratio*2

	# Position de départ pour dessiner la grille
	start_x = window_width // 2 
	start_y = window_height * (1/10)

	running = True
	clock = pygame.time.Clock()
	last_update_time = pygame.time.get_ticks()

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  #zoom avant
				zoom_factor += zoom_speed
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  #zoom arrière
				zoom_factor -= zoom_speed
				if zoom_factor < 10:  
					zoom_factor = 10

			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				dragging = True
				drag_start = pygame.mouse.get_pos()
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				dragging = False
				drag_start = None

		if dragging and pygame.mouse.get_pressed()[0]:  # Clic gauche de la souris enfoncé
			current_mouse_pos = pygame.mouse.get_pos()
			if drag_start:
				new_x = current_mouse_pos[0] - drag_start[0]
				new_y = current_mouse_pos[1] - drag_start[1]
				camera_x += new_x
				camera_y += new_y
				drag_start = current_mouse_pos

		screen.fill(green)

		world.affichage_grid_iso(screen , start_x , start_y , cell_width , cell_height , ratio)

		pygame.display.flip()

		current_time = pygame.time.get_ticks()
		if current_time - last_update_time >= tick_interval:
			world.tick_update()
			last_update_time = current_time
		clock.tick(60)


	pygame.quit()

#####################################################################################
#																					#
#									Zone de Teste									#
#																					#
#####################################################################################

if __name__ == "__main__":


	world1 = World(50)
	for i in range(10):
		world1.spawn("bob")

	pygame_screen(world1 , 100)