import pygame
import os
import matplotlib.pyplot as plt
from bob import Bob
from food import Food
from tiles import Tile

camera_x = 0
camera_y = 0
zoom_factor = 100
zoom_speed = 50


class Affichage_graphique:
	def __init__(self,world):
		self.world = world
		
	def affichage_grid_iso_sprite(self, screen):
		size = self.world.getSize()
		grid = self.world.getGrid()

		window_width = 1280
		window_height = 720

		cell_size = 40



		grid_start_x = window_width // 2 - camera_x
		grid_start_y = window_height * (1/10) - camera_y

		floor = pygame.sprite.Group()
		for i in range(size):
			for j in range(size):
				x = grid_start_x + (i - j) * cell_size // 2 * zoom_factor / 100
				y = grid_start_y + (i + j) * cell_size // 4 * zoom_factor / 100
				floor.add(Tile(x, y, cell_size* zoom_factor / 100))

		floor.update()
		floor.draw(screen)

		
	def affichage_bob_food(self, screen):

		

		cell_width = 1.5*4
		cell_height = 1.5*2

		start_x = 1280 // 2 
		start_y = 720 * (1/10)	

		# Calculez le coin supérieur gauche de la grille en fonction de la caméra
		grid_start_x = start_x - camera_x
		grid_start_y = start_y - camera_y

	
		for bob in self.world.getBobs():

			i,j = bob.getPos()

			x = grid_start_x + (i - j) * (cell_width * zoom_factor / 100)
			y = grid_start_y + (i + j) * (cell_height * zoom_factor / 100)

			sprite_x = x + cell_width / 1.5 * zoom_factor / 400
			sprite_y = y - cell_height * zoom_factor / 400

			sprite_width = bob.getSprite().get_width() * zoom_factor / 400
			sprite_height = bob.getSprite().get_height() * zoom_factor / 400

			screen.blit(pygame.transform.scale(bob.getSprite(), (int(sprite_width), int(sprite_height))), (sprite_x, sprite_y))


		for food in self.world.getFoods():
			i,j = food.getPos()

			x = grid_start_x + (i - j) * (cell_width * zoom_factor / 100)
			y = grid_start_y + (i + j) * (cell_height * zoom_factor / 100)

			food_x = x + 2*cell_width * zoom_factor / 400
			food_y = y + 2* cell_height * zoom_factor / 400
			pygame.draw.circle(screen, (0,0,0), (int(food_x), int(food_y)), 8*zoom_factor / 400)
			


				


	def affichage_grid_iso(self, screen):

		size = self.world.getSize()

	
		cell_width = 1.5*4
		cell_height = 1.5*2
		start_x = 1280 // 2 
		start_y = 720 * (1/10)	

		# Calculez le coin supérieur gauche de la grille en fonction de la caméra
		grid_start_x = start_x - camera_x
		grid_start_y = start_y - camera_y

		size_grid = size - 1

		#cree a base for the grid
		base = [
			(grid_start_x + cell_width * zoom_factor / 100 / 2, grid_start_y + cell_height * zoom_factor / 100 * 1.5),
			(grid_start_x + size_grid * cell_width * zoom_factor / 100 + cell_width * zoom_factor / 100 * 1.5, grid_start_y + cell_height * zoom_factor / 100 / 2 + size_grid * cell_height * zoom_factor / 100),
			(grid_start_x + size_grid * cell_width * zoom_factor / 100 + cell_width * zoom_factor / 100 * 1.5, grid_start_y + cell_height * zoom_factor / 100 / 2 + size_grid * cell_height * zoom_factor / 100 + cell_height * size_grid * zoom_factor / 300),
			(grid_start_x + cell_width * zoom_factor / 100 / 2 , grid_start_y + size_grid * 2 * cell_height * zoom_factor / 100  + cell_height * size_grid * zoom_factor / 300),
			(grid_start_x - cell_width * zoom_factor / 100 / 2 - size_grid * cell_width * zoom_factor / 100, grid_start_y + size_grid * cell_height * zoom_factor / 100 + cell_height * zoom_factor / 100 / 2 + cell_height * size_grid * zoom_factor / 300),
			(grid_start_x - cell_width * zoom_factor / 100 / 2 - size_grid * cell_width * zoom_factor / 100, grid_start_y + size_grid * cell_height * zoom_factor / 100 + cell_height * zoom_factor / 100 / 2)
			
		]


		pygame.draw.polygon(screen, (0, 0, 0), base, 0)

		grid_to_draw = []


		for i in range(size):
			for j in range(size):
				# Calcul des coordonnées isométriques
				x = grid_start_x + (i - j) * (cell_width * zoom_factor / 100)
				y = grid_start_y + (i + j) * (cell_height * zoom_factor / 100)		

				# Dessine une case vide

				const_x = cell_width * zoom_factor / 100 / 2
				const_y = cell_height * zoom_factor / 100 / 2

				case = [
					(x + const_x, y + cell_height * zoom_factor / 100 * 1.5),
					(x + cell_width * zoom_factor / 100 * 1.5, y + const_y),
					(x + const_x, y - const_y),
					(x - const_x, y + const_y)
				]

				pygame.draw.polygon(screen, (0, 120, 51), case, 0)
				pygame.draw.polygon(screen, (0, 51, 51), case, 1)



				




	def run(self , tick_interval):
		global zoom_factor, camera_x, camera_y, zoom_speed

		dragging = False  
		drag_start = None


		# Initialisation de Pygame
		pygame.init()
		screen = pygame.display.set_mode((1280, 720),pygame.RESIZABLE)
		pygame.display.set_caption("Simulation of Bobs")

		black = (0, 0, 0)	

		running = True
		clock = pygame.time.Clock()
		last_update_time = pygame.time.get_ticks()

		font = pygame.font.Font(None, 20)



		while running:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					pause = True
					while pause:
						for event in pygame.event.get():
							if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
								pause = False
								break
							elif event.type == pygame.QUIT:
								pause = False
								running = False
								break
							elif event.type == pygame.VIDEORESIZE:
								screen = pygame.display.set_mode((event.size[0], event.size[1]), pygame.RESIZABLE)

				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.VIDEORESIZE:
					screen = pygame.display.set_mode((event.size[0], event.size[1]), pygame.RESIZABLE)


				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  #zoom avant
					zoom_factor += zoom_speed
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  #zoom arrière
					zoom_factor -= zoom_speed
					if zoom_factor < 10:  
						zoom_factor = 10
			
				if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
					if tick_interval > 100:
						tick_interval -= 100
					elif tick_interval > 10:
						tick_interval -= 10
					elif tick_interval > 1:
						tick_interval -= 1
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
					if tick_interval < 10:
						tick_interval += 1
					elif tick_interval < 100:
						tick_interval += 10
					elif tick_interval < 1000:
						tick_interval += 100

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					dragging = True
					drag_start = pygame.mouse.get_pos()
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					dragging = False
					drag_start = None

			if dragging and pygame.mouse.get_pressed()[0]:  # Clic gauche de la souris enfoncé
				current_mouse_pos = pygame.mouse.get_pos()
				if drag_start:
					new_x = drag_start[0] - current_mouse_pos[0] 
					new_y = drag_start[1] - current_mouse_pos[1]
					camera_x += new_x
					camera_y += new_y
					drag_start = current_mouse_pos

			

			screen.fill((135,206,250))

			self.affichage_grid_iso(screen)
			self.affichage_bob_food(screen)
			


			screen.blit(font.render(f"FPS: {int(clock.get_fps())}", True, black), (10, 10))
			screen.blit(font.render(f"TICK: {self.world.tick}", True, black), (10, 30))
			screen.blit(font.render(f"DAYS: {self.world.tick//100}", True, black), (10, 50))
			screen.blit(font.render(f"TICK TIME: {tick_interval/1000}s", True, black), (10, 70))
			screen.blit(font.render(f"POPULATION: {len(self.world.bobs)}", True, black), (10, 90))
			screen.blit(font.render(f"TIME: {pygame.time.get_ticks()/1000}s", True, black), (10, 110))
			
			

			pygame.display.flip()

			current_time = pygame.time.get_ticks()
			if current_time - last_update_time >= tick_interval:
				self.world.tick_update()
				last_update_time = current_time

	
			clock.tick()


		pygame.quit()



	def graph(self):
		fig , ax = plt.subplots()
		ax.plot(range(len(self.world.population_data)), self.world.population_data, label = "Population")
		ax.plot(range(len(self.world.food_data)), self.world.food_data, label = "Food")
		ax.legend()
		plt.xlabel('Ticks')
		plt.title('Bob Population / Food evolution Over Time')
		plt.grid(True)
		plt.show()

