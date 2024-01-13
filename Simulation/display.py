import pygame
from sprite import Sprite, Sprite_UI, Tile
import os
import matplotlib.pyplot as plt
import random
import threading 



from Utility.occlusion_utility import hide_behind_terrain_image, tile_to_array
from Utility.time_function_utility import execute_function_during_it, execute_function_after_it

# Global variables:

GEN_NULL = iter(())
BLUE_SKY = (135,206,250)
BLACK = (0,0,0)


class Display:
	def __init__(self, api):
		self.api = api

		self.screen_width = 800
		self.screen_height = 600
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),pygame.RESIZABLE)
	

		self.data = self.api.get_shared_data()
		self.world_size = self.data["world_size"]
		self.floor_display = pygame.Surface((32 * self.world_size, 16 * self.world_size + 250))
		self.sprite_display = pygame.Surface((32 * self.world_size, 16 * self.world_size + 250))
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
			"full_bob" : pygame.image.load(os.path.join("assets/Sprites","bob.png")).convert(),
			"foods_banana" : pygame.image.load(os.path.join("assets/Sprites","food.png")).convert()
		}

		for k in range(0, 12):
			self.assets["plants"].append(pygame.image.load(os.path.join("assets/tiles", f"tile_0{k+41}.png")))
			self.assets["plants"][k].set_colorkey(BLACK)

		for l in range(0, 11):
			self.assets["rocks"].append(pygame.image.load(os.path.join("assets/tiles", f"tile_0{l+70}.png")))
			self.assets["rocks"][l].set_colorkey(BLACK)
		
		for key in self.assets:
			if key != "plants" and key != "rocks":
				self.assets[key].set_colorkey(BLACK)


		self.bobs_occlusion_cache = {}
		self.foods_occlusion_cache = {}
		self.sprite_occlusion_cache = {}
	


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
		if grid[i][j] <= 1:
			y = start_y + (i + j) * 32 / 4 - 9 * grid[i][j] - 16 
			tile = Tile(x,y, self.assets["sand"])
		else:
			y = start_y + (i + j) * 32 / 4 - 9 * grid[i][j] - 16
			tile = Tile(x,y, self.assets["grass"])

		self.floor.add(tile)
		
   
	def draw_water_surface_world(self,start_x,start_y,i,j,grid):
		x = start_x + (i - j) * 32 / 2 - 16
		if grid[i][j] <= self.data["water_level"]:
			y = start_y + (i + j) * 32 / 4 - 9 * (self.data["water_level"] + 1) - 16
			tile = Tile(x,y, self.assets["water"])
			self.floor.add(tile)
   
	def draw_decoration_world(self,start_x,start_y,i,j,grid,decoration_to_add):
		x = start_x + (i - j) * 32 / 2 - 16
		if decoration_to_add[i][j] == 1 and grid[i][j] > 2:
			y = start_y + (i + j) * 32 / 4 - 9 * (grid[i][j]+1) - 16
			plant = Tile(x,y, self.assets["plants"][random.randint(0,11)])
			self.floor.add(plant)
		elif decoration_to_add[i][j] == 2 and self.data["water_level"] == 0:
			y = start_y + (i + j) * 32 / 4 - 8 - 16
			rock = Tile(x,y, self.assets["rocks"][random.randint(0,10)])
			self.floor.add(rock)


	

	def draw_better_world(self, load_bar):
		
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

			
			self.screen.fill(BLUE_SKY)
			LOADING_BG = pygame.image.load(os.path.join("assets/UI", "Loading Bar Background.png"))
			LOADING_BG_RECT = LOADING_BG.get_rect(center=(self.screen_width/2, self.screen_height/2))
			loading_bar = pygame.image.load(os.path.join("assets/UI", "Loading Bar.png"))
			load_text = pygame.font.Font(None, 40).render(f"{message}", True, BLACK)
			load_text_rect = load_text.get_rect(center=(self.screen_width/2, self.screen_height/2 - 150))
			

			loading_bar_width = 765 * load_percentage / 100
			loading_bar = pygame.transform.scale(loading_bar, (int(loading_bar_width), 200))
			loading_bar_rect = loading_bar.get_rect(midleft=(self.screen_width/2 - 380, self.screen_height/2))
   
			self.screen.blit(load_text, load_text_rect)
			self.screen.blit(loading_bar, loading_bar_rect)
			self.screen.blit(LOADING_BG, LOADING_BG_RECT)
		
			pygame.display.flip()
		size = self.api.get_shared_data()["world_size"]
		self.floor.empty()


		start_x = self.floor_display.get_size()[0] // 2
		start_y = self.floor_display.get_size()[1] - 16 * (size+1)

		terrain = self.api.get_shared_data()["terrain"]

		world_loader(0,"Génération de l'affichage du monde en cours ...") if load_bar else None
		if terrain:
			grid = terrain.get_terrain()
			decoration_to_add = terrain.get_decoration_to_add()
			self.tile_array = tile_to_array(self.assets["grass"])
		
			for i in range(size):
				for j in range(size):
					self.draw_empty_world(start_x,start_y,i,j,grid)
					self.draw_surface_world(start_x,start_y,i,j,grid)
					self.draw_water_surface_world(start_x,start_y,i,j,grid)
					self.draw_decoration_world(start_x,start_y,i,j,grid,decoration_to_add)
				world_loader(int((i)/(size)*100),"Génération de l'affichage du monde en cours ...") if load_bar else None


		else:
			for i in range(size):
				for j in range(size):
					tile = Tile(start_x + (i - j) * 32 / 2 - 16, start_y + (i + j) * 32 / 4 - 16, self.assets["clean_grass"])
					self.floor.add(tile)
				world_loader(int((i)/(size)*100),"Génération de l'affichage du monde en cours ...") if load_bar else None

		world_loader(100,"Chargement de l'affichage du monde en cours ...") if load_bar else None

		self.floor_display.fill(BLACK)
		self.floor.draw(self.floor_display)
		self.needs_rescaling = True


	def draw_sprite(self, sprite_type):

		def add_sprite_to_group_occlusion(key, sprite_mass):
			i,j = key
			base = grid_of_height[i][j]

			size = sprite_mass ** (1/3)
			x = start_x + (i - j) * 16 - 8 
			y = start_y + (i + j) * 8 - 15 - 9 * base
	
			right_tile_cord = min(self.world_size - 1, max(0 , i + 1))
			left_tile_cord = min(self.world_size - 1, max(0 , j + 1))
			
			rc = max(grid_of_height[right_tile_cord][j] - base, 0)
			lc = max(grid_of_height[i][left_tile_cord] - base, 0)
			bc = max(grid_of_height[right_tile_cord][left_tile_cord] - base, 0)

			
			sprite = Sprite(x, y, sprite_image, size)
			if any([rc, lc, bc]):
				if (rc, lc, bc, sprite_type) in self.sprite_occlusion_cache.keys():
					sprite.set_image(self.sprite_occlusion_cache[(rc, lc, bc, sprite_type)])
				else:
					self.sprite_occlusion_cache[(rc, lc, bc, sprite_type)] = hide_behind_terrain_image(sprite, self.tile_array, [rc, lc, bc])
					sprite.set_image(self.sprite_occlusion_cache[(rc, lc, bc, sprite_type)])

		
			sprite_group.add(sprite)

		def add_sprite_to_group(key, sprite_mass):
			i,j = key
			size = sprite_mass ** (1/3)
			x = start_x + (i - j) * 16 - 8 * size
			y = start_y + (i + j) * 8 - 15 * size
			sprite_group.add(Sprite(x,y, sprite_image, size))

		sprite_group = pygame.sprite.Group()

		start_x = self.sprite_display.get_size()[0] // 2
		start_y = self.sprite_display.get_size()[1] - 16 * (self.data['world_size']+1)

		terrain = self.data["terrain"]

		match sprite_type:
			case "bob":
				sprite_dict = self.data["bobs"]
				sprite_image = self.assets["full_bob"]

			case "food":
				sprite_dict = self.data["foods"]
				sprite_image = self.assets["foods_banana"]
		

		if not terrain:
			for key, sprites in sprite_dict.items():
				if sprite_type == "bob":
					for bob in sprites:
						add_sprite_to_group(key, bob.get_mass())
				else:
					add_sprite_to_group(key, 1)
		else:
			grid_of_height = terrain.get_terrain()
			for key, sprites in sprite_dict.items():
				if sprite_type == "bob":
					for bob in sprites:
						add_sprite_to_group_occlusion(key, bob.get_mass())
				else:
					add_sprite_to_group_occlusion(key, 1)

					

		sprite_group.draw(self.sprite_display)

	def zooming_render(self):
		scale_x = 6*self.zoom_factor
		scale_y = 3*self.zoom_factor
				
		if self.needs_rescaling:
			self.needs_rescaling = False
				
			self.floor_display_temp = pygame.Surface((scale_x, scale_y))
			self.floor_display_temp.set_colorkey(BLACK)
			pygame.transform.scale(self.floor_display, (scale_x, scale_y), self.floor_display_temp)


			self.sprite_display_temp = pygame.Surface((scale_x, scale_y))
			self.sprite_display_temp.set_colorkey(BLACK)
		pygame.transform.scale(self.sprite_display, (scale_x, scale_y), self.sprite_display_temp)

	
	def render(self):
		
		self.sprite_display.fill(BLACK)
  

		self.draw_sprite("bob")
		self.draw_sprite("food")
  
		self.zooming_render()
  

		grid_x = -self.camera_x + (self.screen_width - self.floor_display_temp.get_size()[0]) // 2
		grid_y = -self.camera_y + (self.screen_height - self.floor_display_temp.get_size()[1]) // 2

		
		self.screen.blit(self.floor_display_temp, ( grid_x , grid_y))
		self.screen.blit(self.sprite_display_temp, ( grid_x , grid_y))
		
	
	
	def gif_generator(self, gif_name, nb_total_image, nb_imame_start, extention, kroma_key):
		nb_image = nb_imame_start

		while True:
			nom_fichier = f"{gif_name}{nb_image}{extention}"
			image = pygame.image.load(os.path.join("assets/gif", nom_fichier))
			image.set_colorkey(kroma_key)
			image = pygame.transform.scale(image, (self.screen_width, self.screen_height))

			yield image
			nb_image += 1
			if nb_image == nb_total_image:
				nb_image = nb_imame_start
	
	def draw_gif(self, gif_generator, pos):
		self.screen.blit(next(gif_generator), pos)

		
	def main_loop(self):
		"""
		Main loop of the game
		"""

		def blit_text_info():
			self.screen.blit(pygame.font.Font(None, 20).render(f"Days : {self.data['tick']//self.data['argDict']['dayTick']}", True, BLACK),(20,20))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Ticks : {self.data['tick']}", True, BLACK),(20,40))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Game Ticks : {self.api.get_tick_interval()} ms", True, BLACK),(20,60))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Real Ticks : {self.data['real_tick_time']*1000:.1f} ms", True, BLACK),(20,80))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Bobs : {self.data['nb_bob']}", True, BLACK),(20,100))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Foods : {self.data['nb_food']}", True, BLACK),(20,120))


		def change_color_all_ui():
			pause_button.change_color()
			play_button.change_color()
			fastforward.change_color()
			backforward.change_color()
   
		def ui_tick_modification(pos):
			"""
			Handle the click on the UI elements
			"""
			x,y = pos
			if pause_button.get_rect().collidepoint(x,y):
				self.api.pause()
				pause_button.set_active(True)
				play_button.set_active(False)
				change_color_all_ui()

			elif play_button.get_rect().collidepoint(x,y):
				self.api.resume()
				pause_button.set_active(False)
				play_button.set_active(True)
				change_color_all_ui()
			elif fastforward.get_rect().collidepoint(x,y):
				fastforward.set_active(True)
				fastforward.change_color()

				self.fastforward_active = execute_function_after_it(lambda : (fastforward.set_active(False), fastforward.change_color()), nb_iter = 5)

				if self.api.get_tick_interval() > 100:
					self.api.set_tick_interval(self.api.get_tick_interval() - 100)
				elif self.api.get_tick_interval() > 10:
					self.api.set_tick_interval(self.api.get_tick_interval() - 10)
				elif self.api.get_tick_interval() > 1:
					self.api.set_tick_interval(self.api.get_tick_interval() - 1)
			elif backforward.get_rect().collidepoint(x,y):
				backforward.set_active(True)
				backforward.change_color()

				self.backforward_active = execute_function_after_it(lambda : (backforward.set_active(False), backforward.change_color()), nb_iter = 5)

				if self.api.get_tick_interval() < 10:
					self.api.set_tick_interval(self.api.get_tick_interval() + 1)
				elif self.api.get_tick_interval() < 100:
					self.api.set_tick_interval(self.api.get_tick_interval() + 10)
				elif self.api.get_tick_interval() < 1000:
					self.api.set_tick_interval(self.api.get_tick_interval() + 100)
				else:
					self.api.set_tick_interval(self.api.get_tick_interval() + 500)
			
					
    
    
		pygame.init()
		pygame.display.set_caption("Simulation of Bobs")
		self.screen.fill(BLUE_SKY)
		clock = pygame.time.Clock()

		backforward = Sprite_UI(self.screen_width - 160, 10, pygame.image.load(os.path.join("assets/UI", "backforward.png")))
		backforward.set_active(False)
		fastforward = Sprite_UI(self.screen_width - 40, 10, pygame.image.load(os.path.join("assets/UI", "fastforward.png")))
		fastforward.set_active(False)
		pause_button = Sprite_UI(self.screen_width - 120, 10, pygame.image.load(os.path.join("assets/UI", "pause.png")))
		pause_button.set_active(False)
		play_button = Sprite_UI(self.screen_width - 80, 10, pygame.image.load(os.path.join("assets/UI", "play.png")))
		change_color_all_ui()

		self.fastforward_active = GEN_NULL
		self.backforward_active = GEN_NULL

		rain_gif = self.gif_generator('rain_gif/rain-gif-', 20, 2, ".gif", (43,247,255))
		solar_gif = self.gif_generator('sun_gif/solar-gif-frame-', 34, 1, ".gif", BLACK)
		flood_gif_active = GEN_NULL
		drought_gif_active = GEN_NULL

  
		ui_element = pygame.sprite.Group()
		ui_element.add(pause_button)
		ui_element.add(play_button)
		ui_element.add(backforward)
		ui_element.add(fastforward)

		self.draw_better_world(True)
		self.api.start()


		rendering = True
		running = True

		while running:
			self.data = self.api.get_shared_data()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.api.stop()
					pygame.quit()
					quit()

				elif event.type == pygame.VIDEORESIZE:
					self.screen_height = event.size[1]
					self.screen_width = event.size[0]
					pause_button.update_position((self.screen_width - 120, 10))
					play_button.update_position((self.screen_width - 80, 10))
					fastforward.update_position((self.screen_width - 40, 10))
					backforward.update_position((self.screen_width - 160, 10))

				elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
					if rendering:
						rendering = False
					else:
						rendering = True

				elif event.type == pygame.MOUSEBUTTONDOWN:
					ui_tick_modification(event.pos)

				self.zoom(event)
				self.start_drag(event)

			# Event management
			if self.data["event"] == "flood":				
				regeneration_thread = threading.Thread(target=self.draw_better_world, args=(False,))
				regeneration_thread.start()
				flood_gif_active = execute_function_during_it(self.draw_gif, rain_gif, (0,0), nb_iter = 200)
				self.api.set_event(None)
				
			elif self.data["event"] == "drought":
				regeneration_thread = threading.Thread(target=self.draw_better_world, args=(False,))
				regeneration_thread.start()
				drought_gif_active = execute_function_during_it(self.draw_gif, solar_gif, (0,0), nb_iter = 140)
				self.api.set_event(None)


			
			self.camera()
			self.screen.fill(BLUE_SKY)

			


			# Drawing the world and the sprites
			if rendering:
				self.render()

			# all fonction that need to be executed after or during a certain number of iteration
			next(flood_gif_active,None)
			next(drought_gif_active,None)
			next(self.fastforward_active,None)
			next(self.backforward_active,None)

			# UI and text
			blit_text_info()
			ui_element.draw(self.screen)

			
			# Updating the display
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

