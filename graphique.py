import pygame
import matplotlib.pyplot as plt

camera_x = 0
camera_y = 0
zoom_factor = 100
zoom_speed = 50


class Affichage_graphique:
	def __init__(self,world):
		self.world = world
		
	
		
	def affichage_bob_food(self, screen):

		cell_width = 1.5*4
		cell_height = 1.5*2

		start_x = 1280 // 2 
		start_y = 720 * (1/10)	

		# Calculez le coin supérieur gauche de la grille en fonction de la caméra
		grid_start_x = start_x - camera_x
		grid_start_y = start_y - camera_y

		const_x = cell_width * zoom_factor / 100 
		const_y = cell_height * zoom_factor / 100

	
		for bob in self.world.getBobs():

			i,j = bob.getPos()

			x = grid_start_x + (i - j) * const_x
			y = grid_start_y + (i + j) * const_y

			if x < screen.get_width() and y < screen.get_height():

				sprite_x = x - const_x / 3
				sprite_y = y + const_y / 4

				sprite_width = bob.getSprite().get_width() * zoom_factor / 400
				sprite_height = bob.getSprite().get_height() * zoom_factor / 400

				screen.blit(pygame.transform.scale(bob.getSprite(), (int(sprite_width), int(sprite_height))), (sprite_x, sprite_y))


		for food in self.world.getFoods():
			i,j = food.getPos()

			x = grid_start_x + (i - j) * const_x
			y = grid_start_y + (i + j) * const_y

			if x < screen.get_width() and y < screen.get_height():

				food_x = x 
				food_y = y + const_y
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

		const_x = cell_width * zoom_factor / 100 
		const_y = cell_height * zoom_factor / 100

		#cree a base for the grid
		offset = const_y * size / 3

		base = [
			(grid_start_x, grid_start_y),
			(grid_start_x + const_x * size, grid_start_y + const_y * size),
			(grid_start_x + const_x * size, grid_start_y + const_y * size + offset),
			(grid_start_x , grid_start_y + const_y * size * 2 + offset),
			(grid_start_x - const_x * size, grid_start_y + const_y * size + offset),
			(grid_start_x - const_x * size, grid_start_y + const_y * size),
		]

		floor = [
			(grid_start_x, grid_start_y),
			(grid_start_x + const_x * size, grid_start_y + const_y * size),
			(grid_start_x , grid_start_y + const_y * size * 2),
			(grid_start_x - const_x * size, grid_start_y + const_y * size),
		]


		pygame.draw.polygon(screen, (26, 13, 0), base, 0)
		pygame.draw.polygon(screen, (0, 120, 51), floor, 0)

		for k in range(size+1):
			#cree les lignes de la grille
			pygame.draw.line(screen, (0, 51, 51), (grid_start_x + const_x*k, grid_start_y + const_y*k), (grid_start_x - const_x*(size - k), grid_start_y + const_y*k + const_y*size), 2)
			pygame.draw.line(screen, (0, 51, 51), (grid_start_x - const_x*k, grid_start_y + const_y*k), (grid_start_x + const_x*(size - k), grid_start_y + const_y*k + const_y*size), 2)

	def input_box(self, screen):
		pygame.init()
		clock = pygame.time.Clock()
		
		# Configuration de la boîte de saisie
		  # Centrez la boîte de texte		base_font = pygame.font.Font(None, 32)
		base_font = pygame.font.Font(None, 32)		

		user_text = ''
		# Texte descriptif
		description_text = f"Entrez une nouvelle taille de grille (actuelle: {self.world.getSize()}):"
		erreur_text = "Erreur: la taille doit être un entier positif"
		description_surface = base_font.render(description_text, True, (0, 0, 0))
		erreur_text_surface = base_font.render(erreur_text, True, (255, 0, 0))
		

		erreur = False
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				elif event.type == pygame.VIDEORESIZE:
					screen = pygame.display.set_mode((event.size[0], event.size[1]), pygame.RESIZABLE)
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					return None
		
		
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						try:
							user_input = int(user_text)
							return user_input  # Renvoie l'entier saisi
						except ValueError:
							user_text = ''
							erreur = True
							pass  # Ne fait rien si la saisie n'est pas un entier
		
					elif event.key == pygame.K_BACKSPACE:
						user_text = user_text[:-1]
					elif len(user_text) < 8:
						user_text += event.unicode
			input_rect = pygame.Rect((screen.get_width()) // 2 - 55 , screen.get_height()//2.5, 110, 32)
			description_rect = description_surface.get_rect(center=(screen.get_width() // 2, screen.get_height()//3))
			erreur_text_rect = erreur_text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height()//2))

			screen.fill((135,206,250))
			self.affichage_grid_iso(screen)
			self.affichage_bob_food(screen)
			#color with opacity
			pygame.draw.rect(screen, (200,200,200), input_rect,border_radius=10)
		
		
			text_surface = base_font.render(user_text, True, (0, 0, 0))
			screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

			
		
			# Afficher le texte descriptif
			screen.blit(description_surface, description_rect)
			if erreur:
				screen.blit(erreur_text_surface, erreur_text_rect)
		
			pygame.display.flip()
			clock.tick(60)




				




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

		rendering = True
		pause = False
		
		while running:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					if pause:
						pause = False
					else:
						pause = True
	
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

				#desactive l'affichage si tab est pressé
				if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
					if rendering:
						rendering = False
					else:
						rendering = True

				if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
					new_size = self.input_box(screen)
					if new_size:
						self.world.change_size(new_size)
						
				

			if dragging and pygame.mouse.get_pressed()[0]:  # Clic gauche de la souris enfoncé
				current_mouse_pos = pygame.mouse.get_pos()
				if drag_start:
					new_x = drag_start[0] - current_mouse_pos[0] 
					new_y = drag_start[1] - current_mouse_pos[1]
					camera_x += new_x
					camera_y += new_y
					drag_start = current_mouse_pos


		
				
		
			screen.fill((135,206,250))

			if rendering:
				self.affichage_grid_iso(screen)
				self.affichage_bob_food(screen)
			

			screen.blit(font.render(f"FPS: {int(clock.get_fps())}", True, black), (10, 10))
			screen.blit(font.render(f"TICK: {self.world.getTick()}", True, black), (10, 30))
			screen.blit(font.render(f"DAYS: {self.world.getTick()//100}", True, black), (10, 50))
			screen.blit(font.render(f"TICK TIME: {tick_interval/1000}s", True, black), (10, 70))
			screen.blit(font.render(f"POPULATION: {len(self.world.getBobs())}", True, black), (10, 90))
			screen.blit(font.render(f"TIME: {pygame.time.get_ticks()/1000}s", True, black), (10, 110))
			
			

			pygame.display.flip()

			if not pause:
				current_time = pygame.time.get_ticks()
				if current_time - last_update_time >= tick_interval:
					self.world.tick_update()
					last_update_time = current_time

	
			clock.tick()


		pygame.quit()



	def graph(self):
		fig , ax = plt.subplots()
		ax.plot(range(len(self.world.getPopulationData())), self.world.getPopulationData(), label = "Population")
		ax.plot(range(len(self.world.getFoodData())), self.world.getFoodData(), label = "Food")
		ax.legend()
		plt.xlabel('Ticks')
		plt.title('Bob Population / Food evolution Over Time')
		plt.grid(True)
		plt.show()

