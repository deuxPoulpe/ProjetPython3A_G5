import pygame
import pygame_menu
from sprite import Tile
from sprite import Sprite_bob
import os
import matplotlib.pyplot as plt
import random
from math import sqrt



from Utility.occlusion_utility import hide_behind_terrain_image
from Utility.occlusion_utility import tile_to_array




class Display:
	def __init__(self, api):
		self.api = api

		self.screen_width = 800
		self.screen_height = 600
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),pygame.RESIZABLE)

		self.floor_display = pygame.Surface((32 * api.get_data_world_size(), 16 * api.get_data_world_size() + 250))
		self.sprite_display = pygame.Surface((32 * api.get_data_world_size(), 16 * api.get_data_world_size() + 250))
		self.floor_display_temp = pygame.Surface((0,0))
		self.sprite_display_temp = pygame.Surface((0,0))
		
		self.zoom_factor = 100
		self.zoom_speed = 50
		self.previous_zoom_factor = self.zoom_factor 
		self.needs_rescaling = True

		self.camera_x = 0
		self.camera_y = 0
		self.dragging = False
		self.drag_pos = None

		self.floor = pygame.sprite.Group()

		self.assets = {
			"grass": pygame.image.load(os.path.join("assets/tiles", "tile_028.png")),
			"dirt": pygame.image.load(os.path.join("assets/tiles", "tile_003.png")).convert(),
			"close_water": pygame.image.load(os.path.join("assets/tiles", "tile_019.png")),
			"water": pygame.image.load(os.path.join("assets/tiles", "tile_094.png")).convert(),
			"clean_grass" : pygame.image.load(os.path.join("assets/tiles", "tile_040.png")),
			"stone" : pygame.image.load(os.path.join("assets/tiles", "tile_063.png")),
			"sand" : pygame.image.load(os.path.join("assets/tiles", "tile_115.png")),
			"plants": [],
			"rocks" : [],
			"full_bob" : pygame.image.load(os.path.join("assets","bob.png")).convert(),
			"foods_banana" : pygame.image.load(os.path.join("assets","food.png")).convert()
		}

		for k in range(0, 12):
			self.assets["plants"].append(pygame.image.load(os.path.join("assets/tiles", f"tile_0{k+41}.png")))
			self.assets["plants"][k].set_colorkey((0, 0, 0))

		for l in range(0, 11):
			self.assets["rocks"].append(pygame.image.load(os.path.join("assets/tiles", f"tile_0{l+70}.png")))
			self.assets["rocks"][l].set_colorkey((0, 0, 0))
		
		for key in self.assets:
			if key != "plants" and key != "rocks":
				self.assets[key].set_colorkey((0, 0, 0))


		self.bobs_occlusion_cache = {}
		self.foods_occlusion_cache = {}
	


	def zoom(self,event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 or pygame.key.get_pressed()[pygame.K_PAGEUP]:
			self.zoom_factor += self.zoom_speed
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 or pygame.key.get_pressed()[pygame.K_PAGEDOWN]:
			self.zoom_factor -= self.zoom_speed
			if self.zoom_factor < 10:  
				self.zoom_factor = 10

		if self.previous_zoom_factor != self.zoom_factor:
			self.needs_rescaling = True
			self.previous_zoom_factor = self.zoom_factor

	def start_drag(self,event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			self.dragging = True
			self.drag_pos = pygame.mouse.get_pos()
		elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			self.dragging = False
			self.drag_pos = None

	def camera(self):
		if self.dragging and pygame.mouse.get_pressed()[0]:  # Clic gauche de la souris enfoncé
			current_mouse_pos = pygame.mouse.get_pos()
			if self.drag_pos:
				self.camera_x += self.drag_pos[0] - current_mouse_pos[0] 
				self.camera_y += self.drag_pos[1] - current_mouse_pos[1]
				self.drag_pos = current_mouse_pos
    
	def test_in_screen(self, x, y):
		return True
		# return x >= 0 and x < self.screen_width and y >= 0 and y < self.screen_height
    
    

	def draw_empty_world(self,start_x,start_y,i,j,grid):
		for k in range(grid[i][j] + 1):
			x = start_x + (i - j) * 32 / 2 - 16
			y = start_y + (i + j) * 32 / 4 - 9 * (k - 1) - 16
			if k < grid[i][j] - 1:
				under_tile = Tile(x,y, self.assets["stone"])
			else:
				under_tile = Tile(x,y, self.assets["dirt"])
			self.floor.add(under_tile)

	def draw_surface_world(self,start_x,start_y,i,j,grid):
		x = start_x + (i - j) * 32 / 2 - 16
		if grid[i][j] == 0:
			y = start_y + (i + j) * 32 / 4 - 7 - 16
			tile = Tile(x,y, self.assets["water"])
		elif grid[i][j] == 1:
			y = start_y + (i + j) * 32 / 4 - 9 - 16
			tile = Tile(x,y, self.assets["sand"])
		else:
			y = start_y + (i + j) * 32 / 4 - 9 * grid[i][j] - 16
			tile = Tile(x,y, self.assets["grass"])

		self.floor.add(tile)

	def draw_decoration_world(self,start_x,start_y,i,j,grid,decoration_to_add):
		x = start_x + (i - j) * 32 / 2 - 16
		if decoration_to_add[i][j]== 1 and grid[i][j] > 2:
			y = start_y + (i + j) * 32 / 4 - 9 * (grid[i][j]+1) - 16
			plant = Tile(x,y, self.assets["plants"][random.randint(0,11)])
			self.floor.add(plant)
		elif decoration_to_add[i][j] == 2:
			y = start_y + (i + j) * 32 / 4 - 8 - 16
			rock = Tile(x,y, self.assets["rocks"][random.randint(0,10)])
			self.floor.add(rock)


	

	def draw_better_world(self):
		
		def world_loader(load_percentage, message):
			"""Fonction qui affiche le chargement du monde et gere l'affichage de la fenetre et des evenements seulement pendant le chargement du monde
   
			ps: afficher le chargement du monde prend plus de temps que de charger le monde lui meme sad
			Args:
				load (int): Pourcentage de chargement du monde
			"""
			
			for event in pygame.event.get():
				if event.type == pygame.VIDEORESIZE:
						self.screen_height = event.size[1]
						self.screen_width = event.size[0]
				elif event.type == pygame.QUIT:
					pygame.quit()
					quit()

			
			self.screen.fill((135,206,250))
			LOADING_BG = pygame.image.load(os.path.join("assets", "Loading Bar Background.png"))
			LOADING_BG_RECT = LOADING_BG.get_rect(center=(self.screen_width/2, self.screen_height/2))
			loading_bar = pygame.image.load(os.path.join("assets", "Loading Bar.png"))
			load_text = pygame.font.Font(None, 40).render(f"{message}", True, (0,0,0))
			load_text_rect = load_text.get_rect(center=(self.screen_width/2, self.screen_height/2 - 150))
			

			loading_bar_width = 765 * load_percentage / 100
			loading_bar = pygame.transform.scale(loading_bar, (int(loading_bar_width), 200))
			loading_bar_rect = loading_bar.get_rect(midleft=(self.screen_width/2 - 380, self.screen_height/2))
   
			self.screen.blit(load_text, load_text_rect)
			self.screen.blit(loading_bar, loading_bar_rect)
			self.screen.blit(LOADING_BG, LOADING_BG_RECT)
		
			pygame.display.flip()
		size = self.api.get_data_world_size()
		self.floor.empty()


		start_x = self.floor_display.get_size()[0] // 2
		start_y = self.floor_display.get_size()[1] - 16 * (self.api.get_data_world_size()+1)

		terrain = self.api.get_data_terrain()

		world_loader(0,"Génération de l'affichage du monde en cours ...")
		if terrain:
			grid = terrain.get_terrain()
			decoration_to_add = terrain.get_decoration_to_add()
			self.tile_array = tile_to_array(self.assets["grass"])
		
			for i in range(size):
				for j in range(size):
					self.draw_empty_world(start_x,start_y,i,j,grid)
					self.draw_surface_world(start_x,start_y,i,j,grid)
					self.draw_decoration_world(start_x,start_y,i,j,grid,decoration_to_add)
				world_loader(int((i)/(size)*100),"Génération de l'affichage du monde en cours ...")


		else:
			for i in range(size):
				for j in range(size):
					tile = Tile(start_x + (i - j) * 32 / 2 - 16, start_y + (i + j) * 32 / 4 - 16, self.assets["clean_grass"])
					self.floor.add(tile)
				world_loader(int((i)/(size)*100),"Génération de l'affichage du monde en cours ...")

		world_loader(100,"Chargement de l'affichage du monde en cours ...")
		self.floor.draw(self.floor_display)	


	def draw_bobs(self):
		bobs = pygame.sprite.Group()

		start_x = self.sprite_display.get_size()[0] // 2
		start_y = self.sprite_display.get_size()[1] - 16 * (self.api.get_data_world_size()+1)

		terrain = self.api.get_data_terrain()

		all_bobs = self.api.get_data_bobs()
		

		if not terrain:
			for key in all_bobs:
				for bob in all_bobs[key]:
					i,j = key
					
					size = sqrt(bob.get_mass())
					x = start_x + (i - j) * 16 - 8 * size
					y = start_y + (i + j) * 8 - 15 * size
					if self.test_in_screen(x,y):
						bob_s = Sprite_bob(x,y, self.assets["full_bob"], size)
						bobs.add(bob_s)
		else:
			grid_of_height = terrain.get_terrain()
			for key in all_bobs:
				for bob in all_bobs[key]:
					i,j = key
					
					base = grid_of_height[i][j]
					size = sqrt(bob.get_mass())

					x = start_x + (i - j) * 16 - 8 * size
					y = start_y + (i + j) * 8 - 15 * size - 9 * base
					if self.test_in_screen(x,y):
						
						try:
							rc = grid_of_height[i+1][j] - base
						except:
							rc = 0
						try:
							lc = grid_of_height[i][j+1] - base
						except:
							lc = 0
						try:
							bc = grid_of_height[i+1][j+1] - base
						except:
							bc = 0
						
						bob_s = Sprite_bob(x,y,self.assets["full_bob"] , size)
						if rc > 0 or lc > 0 or bc > 0:
							try:
								bob_s.set_image(self.bobs_occlusion_cache[(rc, lc, bc)])
							except:
								self.bobs_occlusion_cache[(rc, lc, bc)] = hide_behind_terrain_image(bob_s, self.tile_array, [rc, lc, bc])
								bob_s.set_image(self.bobs_occlusion_cache[(rc, lc, bc)])
					
						bobs.add(bob_s)


		
		bobs.draw(self.sprite_display)		

	def draw_foods(self):
		foods = pygame.sprite.Group()

		start_x = self.sprite_display.get_size()[0] // 2
		start_y = self.sprite_display.get_size()[1] - 16 * (self.api.get_data_world_size()+1)

		terrain = self.api.get_data_terrain()

		all_foods = self.api.get_data_foods()
		

		if not terrain:
			for key in all_foods:
				i,j = key
				x = start_x + (i - j) * 16 - 8
				y = start_y + (i + j) * 8 - 15
				if self.test_in_screen(x,y):
					food_s = Sprite_bob(x,y, self.assets["foods_banana"], 1)
					foods.add(food_s)
		else:
			grid_of_height = terrain.get_terrain()
			for key in all_foods:
				i,j = key
				base = grid_of_height[i][j]

				x = start_x + (i - j) * 16 - 8 
				y = start_y + (i + j) * 8 - 15 - 9 * base

				if self.test_in_screen(x,y):
					try:
						rc = grid_of_height[i+1][j] - base
					except:
						rc = 0
					try:
						lc = grid_of_height[i][j+1] - base
					except:
						lc = 0
					try:
						bc = grid_of_height[i+1][j+1] - base
					except:
						bc = 0
					
					food_s = Sprite_bob(x,y,self.assets["foods_banana"] , 1)
					if rc > 0 or lc > 0 or bc > 0:
						try:
							food_s.set_image(self.foods_occlusion_cache[(rc, lc, bc)])
						except:
							self.foods_occlusion_cache[(rc, lc, bc)] = hide_behind_terrain_image(food_s, self.tile_array, [rc, lc, bc])
							food_s.set_image(self.foods_occlusion_cache[(rc, lc, bc)])
				
					foods.add(food_s)


		
		foods.draw(self.sprite_display)
              

	def zooming_render(self):
		scale_x = 6*self.zoom_factor
		scale_y = 3*self.zoom_factor
				
		if self.needs_rescaling:
			self.needs_rescaling = False
				
			self.floor_display_temp = pygame.Surface((scale_x, scale_y))
			self.floor_display_temp.set_colorkey((0, 0, 0))
			pygame.transform.scale(self.floor_display, (scale_x, scale_y), self.floor_display_temp)


			self.sprite_display_temp = pygame.Surface((scale_x, scale_y))
			self.sprite_display_temp.set_colorkey((0, 0, 0))
		pygame.transform.scale(self.sprite_display, (scale_x, scale_y), self.sprite_display_temp)

	
	def render(self):
		
		self.sprite_display.fill((0,0,0))
  

		self.draw_bobs()
		self.draw_foods()
  
		self.zooming_render()
  

		grid_x = -self.camera_x + (self.screen_width - self.floor_display_temp.get_size()[0]) // 2
		grid_y = -self.camera_y + (self.screen_height - self.floor_display_temp.get_size()[1]) // 2

		
		self.screen.blit(self.floor_display_temp, ( grid_x , grid_y))
		self.screen.blit(self.sprite_display_temp, ( grid_x , grid_y))
		


	def main_loop(self):
		pygame.init()
		pygame.display.set_caption("Simulation of Bobs")
		self.screen.fill((135,206,250))
		clock = pygame.time.Clock()
		font = pygame.font.Font(None, 20)

		
		self.draw_better_world()
		self.api.start()


		rendering = True
		running = True

		while running:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.api.stop()
					pygame.quit()
					quit()

				elif event.type == pygame.VIDEORESIZE:
					self.screen_height = event.size[1]
					self.screen_width = event.size[0]

				elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
					if rendering:
						rendering = False
					else:
						rendering = True
	
				
				self.zoom(event)
				self.start_drag(event)



			self.camera()
			self.screen.fill((135,206,250))
			if rendering:
				self.render()
			self.screen.blit(pygame.font.Font(None, 20).render(f"Days : {self.api.get_data_tick()//self.api.get_date_argDict()['dayTick']}", True, (0,0,0)),(20,20))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Ticks : {self.api.get_data_tick()}", True, (0,0,0)),(20,40))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Bobs : {self.api.get_data_nb_bob()}", True, (0,0,0)),(20,60))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Foods : {self.api.get_data_nb_food()}", True, (0,0,0)),(20,80))
				

			pygame.display.set_caption(f"Simulation of Bobs\tFPS: {int(clock.get_fps())}")


			pygame.display.flip()


			
			clock.tick()






	def graph(self):
		fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

		# Premier graphique
		ax1.plot(range(len(self.world.get_population_Bob())), self.world.get_population_Bob(), label="Population")
		ax1.legend()
		ax1.set_ylabel('Population')
		ax1.set_title('Bob Population Over Time')
		ax1.grid(True)

		# Deuxième graphique
		ax2.plot(range(len(self.world.get_population_Food())), self.world.get_population_Food(), label="Food", color='orange')
		ax2.legend()
		ax2.set_xlabel('Ticks')
		ax2.set_ylabel('Food')
		ax2.set_title('Bob Food Over Time')
		ax2.grid(True)

		plt.tight_layout()
		plt.show()

