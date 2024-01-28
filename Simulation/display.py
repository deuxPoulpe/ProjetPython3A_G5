import pygame
from sprite import Sprite, Sprite_UI, Tile
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from bob import Bob
from food import Food

from Utility.occlusion_utility import hide_behind_terrain_image, tile_to_array
from Utility.time_function_utility import execute_function_during_it, execute_function_after_it

# Global variables:

GEN_NULL = iter(())
BLUE_SKY = (135,206,250)
BLACK = (0,0,0)
WHITE = (255,255,255)


class Display:
	'''
		Class representing the display of the game.

		Attributes:
			in_game_menu (InGameMenu): InGameMenu object.
			api (API): API object.
	'''
	def __init__(self, api, ig_menu):
		'''
			Initializes a new instance of the display.

			Parameters:
				api (API): API object.
				ig_menu (InGameMenu): InGameMenu object.
			
			
			game_paused (bool): Boolean representing the state of the game.
			screen_width (int): Width of the screen.
			screen_height (int): Height of the screen.
			screen (pygame.Surface): Surface of the screen.
			data (dict): Dictionary of shared data.
			world_size (int): Size of the world.
			max_height (int): Maximum height of the terrain.
			floor_display (pygame.Surface): Surface of the floor display.
			sprite_display (pygame.Surface): Surface of the sprite display.
			floor_display_temp (pygame.Surface): Temporary surface of the floor display.
			sprite_display_temp (pygame.Surface): Temporary surface of the sprite display.
			zoom_factor (float): Zoom factor of the display.
			zoom_speed (float): Zoom speed of the display.
			previous_zoom_factor (float): Previous zoom factor of the display.
			needs_rescaling (bool): Boolean representing if the display needs to be rescaled.
			camera_x (int): X coordinate of the camera.
			camera_y (int): Y coordinate of the camera.
			dragging (bool): Boolean representing if the user is dragging the camera.
			drag_pos (tuple): Tuple representing the position of the mouse when the user started dragging the camera.
			floor (pygame.sprite.Group): Group of floor objects.
			object_stats (list): List of objects stats.
			assets (dict): Dictionary of assets.
			tile_array (numpy.ndarray): Array of tiles.
			bob_array_base (numpy.ndarray): Array of bob base.
			sprite_occlusion_cache (dict): Dictionary of sprite occlusion cache.
			sprite_color_cache (dict): Dictionary of sprite color cache.
			sprite_group (pygame.sprite.Group): Group of sprites.

		'''
		self.in_game_menu = ig_menu
		self.api = api
		self.game_paused = True

		self.screen_width = 800
		self.screen_height = 600
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),pygame.RESIZABLE)
	


		self.data = self.api.get_shared_data()
		self.world_size = self.data["world_size"]
		self.max_height = self.api.get_shared_data()["terrain"].get_height() if self.data["argDict"]["custom_terrain"] else 0
		self.floor_display = pygame.Surface((32 * self.world_size, 24 * self.world_size + 9*self.max_height))
		self.sprite_display = pygame.Surface((32 * self.world_size, 24 * self.world_size + 9*self.max_height))
		self.floor_display_temp = pygame.Surface((0,0))
		self.sprite_display_temp = pygame.Surface((0,0))
		
		self.zoom_factor = 1
		self.zoom_speed = 0.1
		self.previous_zoom_factor = self.zoom_factor 
		self.needs_rescaling = True

		self.camera_x = 0
		self.camera_y = 0
		self.dragging = False
		self.drag_pos = None

		self.floor = pygame.sprite.Group()
		self.object_stats = []
		

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
			"dead_bob" : pygame.image.load(os.path.join("assets/Sprites","dead_bob.png")).convert(),
			"foods_banana" : pygame.image.load(os.path.join("assets/Sprites","food.png")).convert(),
			"pause" : pygame.image.load(os.path.join("assets/UI", "pause.png")),
			"play" : pygame.image.load(os.path.join("assets/UI", "play.png")),
			"backforward" : pygame.image.load(os.path.join("assets/UI", "backforward.png")),
			"fastforward" : pygame.image.load(os.path.join("assets/UI", "fastforward.png")),
			"option" : pygame.image.load(os.path.join("assets/UI", "option.png")),
			"playmusic" : pygame.image.load(os.path.join("assets/UI", "music_play.png")),
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
		
		self.tile_array = tile_to_array(self.assets["clean_grass"], 32, 48)
		self.bob_array_base = pygame.surfarray.array2d(self.assets["full_bob"])


		self.sprite_occlusion_cache = {}
		self.sprite_color_cache = {}
		
		pygame.mixer.init()	
        
		self.chanson = pygame.mixer.Sound(os.path.join("assets", f"music.mp3"))
		pygame.mixer.pause()
		

	def convert_sub_surface_coords_to_screen(self, x, y):
		'''
			Converts the coordinates of a sub surface to the coordinates of the screen.
			
			Parameters:
				x (int): X coordinate of the sub surface.
				y (int): Y coordinate of the sub surface.
				
			Returns:
				screen_x (int): X coordinate of the screen.
				screen_y (int): Y coordinate of the screen.
		'''
		grid_x = -self.camera_x + (self.screen_width - self.floor_display_temp.get_size()[0]) // 2
		grid_y = -self.camera_y + (self.screen_height - self.floor_display_temp.get_size()[1]) // 2

		screen_x = int(x / self.zoom_factor) + grid_x
		screen_y = int(y / self.zoom_factor) + grid_y

		return screen_x, screen_y
	
	def is_mouse_on_sprite(self, sprite_pos, sprite_size):
		'''
			Checks if the mouse is on a sprite.
			
			Parameters:
				sprite_pos (tuple): Tuple representing the position of the sprite.
				sprite_size (int): Size of the sprite.
				
			Returns:
				(bool): Boolean representing if the mouse is on the sprite.
		'''
		mouse_x, mouse_y = pygame.mouse.get_pos()
		sprite_x, sprite_y = sprite_pos
		screen_x, screen_y = self.convert_sub_surface_coords_to_screen(sprite_x, sprite_y)

		return screen_x <= mouse_x <= screen_x + int((16*sprite_size)/self.zoom_factor) and screen_y <= mouse_y <= screen_y + int((16*sprite_size)/self.zoom_factor)
	

	def zoom(self,event):
		'''
			Manages the zoom of the display.
			
			Parameters:
				event (pygame.event): Event of the display.
		'''
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 or pygame.key.get_pressed()[pygame.K_PAGEUP]:
			self.zoom_factor -= self.zoom_speed
			if self.zoom_factor < 0.3 and self.data["world_size"] > 40:  
				self.zoom_factor = 0.3
			elif self.zoom_factor < 0.1:
				self.zoom_factor = 0.1
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 or pygame.key.get_pressed()[pygame.K_PAGEDOWN]:
			self.zoom_factor += self.zoom_speed

		if self.previous_zoom_factor != self.zoom_factor:
			self.needs_rescaling = True
			self.previous_zoom_factor = self.zoom_factor

	def start_drag(self,event):
		'''
			Manages the start of the drag of the display.
			
			Parameters:
				event (pygame.event): Event of the display.
		'''
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			self.dragging = True
			self.drag_pos = pygame.mouse.get_pos()
		elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
			self.dragging = False
			self.drag_pos = None

	def camera(self):
		'''
			Manages the camera of the display by moving the camera according to the mouse position.
		'''
		if self.dragging and pygame.mouse.get_pressed()[0]:  # Clic gauche de la souris enfoncé
			current_mouse_pos = pygame.mouse.get_pos()
			if self.drag_pos:
				self.camera_x += self.drag_pos[0] - current_mouse_pos[0] 
				self.camera_y += self.drag_pos[1] - current_mouse_pos[1]
				self.drag_pos = current_mouse_pos
    

	def draw_empty_world(self,start_x,start_y,i,j,grid,height):
		'''
			Draws an empty world by adding stone tiles to the floor group.	
			
			Parameters:
				start_x (int): X coordinate of the start of the world.
				start_y (int): Y coordinate of the start of the world.
				i (int): X coordinate of the tile.
				j (int): Y coordinate of the tile.
				grid (list): List representing the grid of the world.
				height (int): Height of the tile.		
		'''
    
		for k in range(height, grid[i][j]):
			x = start_x + (i - j) * 32 / 2 - 16
			y = start_y + (i + j) * 32 / 4 - 9 * k
			if k < grid[i][j] - 1:
				under_tile = Tile(x,y, self.assets["stone"])
				self.floor.add(under_tile)

	def draw_surface_world(self,start_x,start_y,i,j,grid):
		'''
			Draws the surface of the world by adding grass tiles to the floor group.

			Parameters:
				start_x (int): X coordinate of the start of the world.
				start_y (int): Y coordinate of the start of the world.
				i (int): X coordinate of the tile.
				j (int): Y coordinate of the tile.
				grid (list): List representing the grid of the world.
		'''

		x = start_x + (i - j) * 32 / 2 - 16
		if grid[i][j] <= 1:
			y = start_y + (i + j) * 32 / 4 - 9 * grid[i][j]
			tile = Tile(x,y, self.assets["sand"])
		else:
			y = start_y + (i + j) * 32 / 4 - 9 * grid[i][j]
			tile = Tile(x,y, self.assets["clean_grass"])
			dirt = Tile(x,y + 9, self.assets["dirt"])
			self.floor.add(dirt)

		self.floor.add(tile)
		
   
	def draw_water_surface_world(self,start_x,start_y,i,j,grid):
		'''
			Draws the water surface of the world by adding water tiles to the floor group.

			Parameters:
				start_x (int): X coordinate of the start of the world.
				start_y (int): Y coordinate of the start of the world.
				i (int): X coordinate of the tile.
				j (int): Y coordinate of the tile.
				grid (list): List representing the grid of the world.
		'''
		x = start_x + (i - j) * 32 / 2 - 16
		if grid[i][j] <= self.data["water_level"]:
			y = start_y + (i + j) * 32 / 4 - 9 * (self.data["water_level"] + 1)
			tile = Tile(x,y, self.assets["water"])
			self.floor.add(tile)
   
	def draw_decoration_world(self,start_x,start_y,i,j,grid,decoration_to_add):
		'''
			Draws the decoration of the world by adding plants and rocks tiles to the floor group.
		'''
		x = start_x + (i - j) * 32 / 2 - 16
		if decoration_to_add[i][j] == 1 and grid[i][j] > 2:
			y = start_y + (i + j) * 32 / 4 - 9 * (grid[i][j]+1)
			plant = Tile(x,y, self.assets["plants"][random.randint(0,11)])
			self.floor.add(plant)
		elif decoration_to_add[i][j] == 2 and self.data["water_level"] == 0:
			y = start_y + (i + j) * 32 / 4 - 8
			rock = Tile(x,y, self.assets["rocks"][random.randint(0,10)])
			self.floor.add(rock)




	def draw_better_world(self, load_bar):
		'''
			Draws the world by adding tiles to the floor group.

			Parameters:
				load_bar (bool): Boolean representing if the load bar is displayed.
		'''

		
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
		
			for i in range(size):
				for j in range(size):
					if i == (size - 1)  or j == (size - 1):
						self.draw_empty_world(start_x,start_y,i,j,grid,0)
					else:
						terrain_height = grid[i][j]
						rc = min(size - 1, max(0, i + 1))
						lc = min(size - 1, max(0, j + 1))
						if terrain_height > grid[rc][j] or terrain_height > grid[i][lc] or terrain_height > grid[rc][lc]: # if the tile is a border tile or a tile that is higher than its neighbours
							self.draw_empty_world(start_x,start_y,i,j,grid,min(grid[rc][j], grid[i][lc], grid[rc][lc]))
     
					self.draw_surface_world(start_x,start_y,i,j,grid)
					self.draw_water_surface_world(start_x,start_y,i,j,grid)
					self.draw_decoration_world(start_x,start_y,i,j,grid,decoration_to_add)

				world_loader(int((i)/(size)*100),"Génération de l'affichage du monde en cours ...") if load_bar else None



		else:
			# If there is no terrain, we draw a flat world
			for i in range(size):
				for j in range(size):
					tile = Tile(start_x + (i - j) * 32 / 2 - 16, start_y + (i + j) * 32 / 4, self.assets["clean_grass"])
					self.floor.add(tile)

				world_loader(int((i)/(size)*100),"Génération de l'affichage du monde en cours ...") if load_bar else None

		world_loader(100,"Chargement de l'affichage du monde en cours ...") if load_bar else None

		self.floor_display.fill(BLACK)
		self.floor2 = self.floor.copy()
		self.floor.draw(self.floor_display)
		self.needs_rescaling = True


	def update_bob_color(self, velocity, bob_image):
		'''
			Updates the color of a bob according to its velocity.

			Parameters:
				velocity (int): Velocity of the bob.
				bob_image (pygame.Surface): Surface of the bob.
				
			Returns:
				bob_color_modified (pygame.Surface): Modified surface of the bob.
		'''
		x = max(0, min(velocity, 100))

		red_amount = int((x - 40) * 2.55) if x > 40 else 10
		green_amount = int(x * 2.55) if x <= 50 else max(0, 127 - int(((x - 50) / 40) * 255))
		sub_green_amount = int((x - 80)/20 * 70) if x > 80 else 0
		blue_amount = int(x * 2.55)

		add_color_surface = pygame.Surface((16, 16))
		sub_color_surface = pygame.Surface((16, 16))

		add_color_surface.fill((red_amount, green_amount, 0))
		sub_color_surface.fill((0, sub_green_amount, blue_amount))

		bob_color_modified = bob_image.copy().convert_alpha()
		bob_color_modified.blit(add_color_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
		bob_color_modified.blit(sub_color_surface, (0, 0), special_flags=pygame.BLEND_RGB_SUB)

		return bob_color_modified.convert_alpha()

	def draw_sprite(self, sprite_type):

		'''
			Draws the sprites of the world by adding sprites to the sprite group.
			
			Parameters:
				sprite_type (str): Type of the sprite.
		'''

		def add_sprite_to_group_occlusion(sprite_obj, sprite_mass, velocity, sprite_image):
			'''
				Adds a sprite to the sprite group with occlusion.
				occlusion is the fact that a sprite can be hidden behind a tile.
				
				Parameters:
					sprite_obj (Bob or Food): Sprite object.
					sprite_mass (int): Mass of the sprite.
					velocity (int): Velocity of the sprite.
					sprite_image (pygame.Surface): Surface of the sprite.
					sprite_type (str): Type of the sprite.
			'''
			i,j = sprite_obj.get_pos()
   
			base = grid_of_height[i][j]

			size = sprite_mass ** (1/3)
			x = start_x + (i - j) * 16 - 8 
			y = start_y + (i + j) * 8 - 9 * base
	
			right_tile_cord = min(self.world_size - 1, max(0 , i + 1))
			left_tile_cord = min(self.world_size - 1, max(0 , j + 1))
			
			rc = max(grid_of_height[right_tile_cord][j] - base, 0)
			lc = max(grid_of_height[i][left_tile_cord] - base, 0)
			bc = max(grid_of_height[right_tile_cord][left_tile_cord] - base, 0)

			if sprite_type == "bob": # if the sprite is a bob, we update its color according to its velocity
				if velocity in self.sprite_color_cache.keys():
					sprite_image = self.sprite_color_cache[velocity, sprite_obj.is_dead()] # if the sprite is already in the cache, we use the cached image
				else:
					sprite_image = self.update_bob_color(velocity, sprite_image) # if the sprite is not in the cache, we update its color and add it to the cache
					self.sprite_color_cache[velocity, sprite_obj.is_dead()] = sprite_image
				
			sprite = Sprite(x, y, sprite_image, size)
			if any([rc, lc, bc]):
				if (rc, lc, bc, sprite_type) in self.sprite_occlusion_cache.keys():
					sprite.set_image(self.sprite_occlusion_cache[(rc, lc, bc, sprite_type)]) # if the sprite is already in the cache, we use the cached image
				else:
					self.sprite_occlusion_cache[(rc, lc, bc, sprite_type)] = hide_behind_terrain_image(sprite, self.tile_array, [rc, lc, bc], self.bob_array_base) # if the sprite is not in the cache, we hide it behind the terrain and add it to the cache
					sprite.set_image(self.sprite_occlusion_cache[(rc, lc, bc, sprite_type)])
     
			sprite_group.add(sprite)

			if self.game_paused and self.is_mouse_on_sprite(sprite.rect.topleft, size): # if the game is paused and the mouse is on the sprite, we add it to the object stats
				self.object_stats.append(sprite_obj)

		def add_sprite_to_group(sprite_obj, sprite_mass, velocity, sprite_image):
			'''
				Adds a sprite to the sprite group.
				
				Parameters:
					sprite_obj (Bob or Food): Sprite object.
					sprite_mass (int): Mass of the sprite.
					velocity (int): Velocity of the sprite.
					sprite_image (pygame.Surface): Surface of the sprite.
			'''
			i,j = sprite_obj.get_pos()
			old_i, old_j = sprite_obj.get_old_pos() if sprite_type == "bob" else (0,0)

			size = sprite_mass ** (1/3)
			x = start_x + (i - j) * 16 - 8 * size
			y = start_y + (i + j) * 8 - 15 * (size - 1)
			old_x = start_x + (old_i - old_j) * 16 - 8 * size
			old_y = start_y + (old_i + old_j) * 8 - 15 * (size - 1)
   
   
	
			if sprite_type == "bob": # if the sprite is a bob, we update its color according to its velocity
				if velocity in self.sprite_color_cache.keys():
					sprite_image = self.sprite_color_cache[velocity, sprite_obj.is_dead()] # if the sprite is already in the cache, we use the cached image
				else:
					sprite_image = self.update_bob_color(velocity, sprite_image) # if the sprite is not in the cache, we update its color and add it to the cache
					self.sprite_color_cache[velocity, sprite_obj.is_dead()] = sprite_image 
	
			if sprite_type == "bob" and not sprite_obj.is_dead(): # if the bob is not dead, we interpolate its position show is path
				for t in range(1, 10):
					interpolated_x = old_x + (x - old_x) * t / 10
					interpolated_y = old_y + (y - old_y) * t / 10

					sprite = Sprite(interpolated_x, interpolated_y, sprite_image, size)
					sprite.image.set_alpha(255 * (10 - t) / 20)
					sprite_group.add(sprite)
     
			sprite = Sprite(x,y, sprite_image, size)

			sprite_group.add(sprite)

			if self.game_paused and self.is_mouse_on_sprite(sprite.rect.topleft, size): # if the game is paused and the mouse is on the sprite, we add it to the object stats
				self.object_stats.append(sprite_obj)
			

		sprite_group = pygame.sprite.Group()

		start_x = self.sprite_display.get_size()[0] // 2
		start_y = self.sprite_display.get_size()[1] - 16 * (self.data['world_size']+1)

		terrain = self.data["terrain"]

		if sprite_type == "bob":
			sprite_dict = self.data["bobs"]
			sprite_image = self.assets["full_bob"]

		elif sprite_type == "food":
			sprite_dict = self.data["foods"]
			sprite_image = self.assets["foods_banana"]
    
		vel_list = [bob.get_velocity() for bobs in sprite_dict.values() for bob in bobs] if sprite_type == "bob" else []
		vel_list.append(1)
		velocity_max = max(vel_list) if sprite_type == "bob" else 1
  
    
		with ThreadPoolExecutor(max_workers=10) as threading_pool: # we use a thread pool to add the sprites to the sprite group in parallel to improve performance 
			pool = []

			if not terrain: # if there is no terrain, we don't use occlusion
				for key, sprites in sprite_dict.items():
					if sprite_type == "bob":
						for bob in sprites:
							if bob.is_dead():
								new_sprite_image = self.assets["dead_bob"]
								pool.append(threading_pool.submit(add_sprite_to_group, bob, bob.get_mass(), (bob.get_velocity()/velocity_max)*100, new_sprite_image))
							else:
								pool.append(threading_pool.submit(add_sprite_to_group, bob, bob.get_mass(), (bob.get_velocity()/velocity_max)*100, sprite_image))
					else:
						pool.append(threading_pool.submit(add_sprite_to_group, sprites, 1, 1, sprite_image))
		
			else: # if there is a terrain, we use occlusion
				grid_of_height = terrain.get_terrain()
				for key, sprites in sprite_dict.items():
					if sprite_type == "bob":
						for bob in sprites:
							if bob.is_dead():
								new_sprite_image = self.assets["dead_bob"]
								pool.append(threading_pool.submit(add_sprite_to_group_occlusion, bob, bob.get_mass(), (bob.get_velocity()/velocity_max)*100, new_sprite_image))
							else:
								pool.append(threading_pool.submit(add_sprite_to_group_occlusion, bob, bob.get_mass(), (bob.get_velocity()/velocity_max)*100, sprite_image))
					else:
						pool.append(threading_pool.submit(add_sprite_to_group_occlusion, sprites, 1, 1, sprite_image))

			for _ in as_completed(pool): # we wait for the threads to finish before continuing
				pass			

		sprite_group.draw(self.sprite_display)

	def zooming_render(self):
		'''
			Manages the zooming of the display.
			by rescaling the display if needed.
		'''
		scale_x = 32 * self.world_size // self.zoom_factor
		scale_y = (24 * self.world_size + 9*self.max_height) // self.zoom_factor
				
		if self.needs_rescaling:
			self.needs_rescaling = False
				
			self.floor_display_temp = pygame.Surface((scale_x, scale_y))
			self.floor_display_temp.set_colorkey(BLACK)
			pygame.transform.scale(self.floor_display, (scale_x, scale_y), self.floor_display_temp)


			self.sprite_display_temp = pygame.Surface((scale_x, scale_y))
			self.sprite_display_temp.set_colorkey(BLACK)
		pygame.transform.scale(self.sprite_display, (scale_x, scale_y), self.sprite_display_temp)

	
	def render(self):
		'''
			Renders the display, draws the sprites and the floor and blits them on the screen according to the camera position.

		'''
		self.sprite_display.fill(BLACK)
  
		self.draw_sprite("food")
		self.draw_sprite("bob")
  
		self.zooming_render()
  

		grid_x = -self.camera_x + (self.screen_width - self.floor_display_temp.get_size()[0]) // 2
		grid_y = -self.camera_y + (self.screen_height - self.floor_display_temp.get_size()[1]) // 2

		self.screen.blit(self.floor_display_temp, ( grid_x , grid_y))
		self.screen.blit(self.sprite_display_temp, ( grid_x , grid_y))
		
	
	
	def gif_generator(self, gif_name, nb_total_image, nb_imame_start, extention, kroma_key):
		'''
			Generates a gif by loading images from the assets/gif folder.
				
			Parameters:
				gif_name (str): Name of the gif.
				nb_total_image (int): Total number of images.
				nb_imame_start (int): Number of the first image.
				extention (str): Extention of the images.
				kroma_key (tuple): Tuple representing the kroma key.
		'''
		nb_image = nb_imame_start

		while True:
			nom_fichier = f"{gif_name}{nb_image}{extention}"
			image = pygame.image.load(os.path.join("assets/gif", nom_fichier))
			image.set_colorkey(kroma_key)
			image = pygame.transform.scale(image, (self.screen_width, self.screen_height))

			yield image # we use a generator to improve performance and avoid loading all the images at once
			nb_image += 1
			if nb_image == nb_total_image:
				nb_image = nb_imame_start
	
	def draw_gif(self, gif_generator, pos):
		'''
			Draws a gif.
				
			Parameters:
				gif_generator (generator): Generator of the gif.
				pos (tuple): Tuple representing the position of the gif.
		'''
		self.screen.blit(next(gif_generator), pos) # we draw the gif by blitting the next image of the generator
  
  		
	def change_api_option(self,options):
		'''
			Changes the options of the api.
			
			Parameters:
				options (list): List of options.
		'''
		self.api.change_options(options[0], options[1])
		self.world_size = options[0]["size"]
		self.floor_display = pygame.Surface((32 * self.world_size, 24 * self.world_size + 9*self.max_height)) # we resize the floor display according to the new world size
		self.sprite_display = pygame.Surface((32 * self.world_size, 24 * self.world_size + 9*self.max_height)) # we resize the sprite display according to the new world size
		while self.api.is_changed_option(): # we wait for the api to change the options
			pass
		self.data = self.api.get_shared_data()
		self.draw_better_world(True)

		
	def main_loop(self):
		"""
			Main loop of the game.
    		This function is responsible for running the game loop, handling events, updating the game state, and rendering the game world and UI.
		"""

		def blit_text_info():
			'''
				Renders the text information on the screen.
        		This includes game statistics like days, ticks, game tick interval, and various toggles for game functions.
			'''

			self.screen.blit(pygame.font.Font(None, 20).render(f"Days : {self.data['tick']//self.data['argDict']['dayTick']}", True, BLACK),(20,20))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Ticks : {self.data['tick']}", True, BLACK),(20,40))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Game Ticks : {self.api.get_tick_interval()} ms", True, BLACK),(20,60))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Real Ticks : {self.data['real_tick_time']*1000:.1f} ms", True, BLACK),(20,80))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Bobs : {self.data['nb_bob']}", True, BLACK),(20,100))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Foods : {self.data['nb_food']}", True, BLACK),(20,120))
			self.screen.blit(pygame.font.Font(None, 20).render(f"_________________", True, BLACK),(20,140))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Function enable :", True, BLACK),(20,160))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Move smart : {self.data['argDict']['toggle_fonction']['move_smart']}", True, BLACK),(20,180))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Reproduce : {self.data['argDict']['toggle_fonction']['reproduce']}", True, BLACK),(20,200))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Sexual reproduction : {self.data['argDict']['toggle_fonction']['sexual_reproduction']}", True, BLACK),(20,220))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Perception : {self.data['argDict']['toggle_fonction']['perception']}", True, BLACK),(20,240))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Memory : {self.data['argDict']['toggle_fonction']['memory']}", True, BLACK),(20,260))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Custom event : {self.data['argDict']['toggle_fonction']['custom_event']}", True, BLACK),(20,280))
			self.screen.blit(pygame.font.Font(None, 20).render(f"Eat bob : {self.data['argDict']['toggle_fonction']['eat_bob']}", True, BLACK),(20,300))
			self.screen.blit(pygame.font.Font(None, 20).render(f"_________________", True, BLACK),(20,310))		

		def change_color_all_ui():
			'''
			Changes the color of all UI elements.
        	This function is used to update the UI elements' color based on their current state.
			'''
			
			pause_button.change_color()
			play_button.change_color()
			fastforward.change_color()
			backforward.change_color()
			option_button.change_color()
			play_buttonmusic.change_color()
   
		def ui_tick_modification(pos):
			"""
			Handles the interaction with UI elements.
			This function is triggered by mouse clicks and manages the behavior of various buttons like play, pause, fastforward, etc.
			"""
			x,y = pos
			if pause_button.get_rect().collidepoint(x,y):
				self.api.pause()
				self.game_paused = True 
				pause_button.set_active(True)
				play_button.set_active(False)
				change_color_all_ui()		

			elif play_button.get_rect().collidepoint(x,y):
				self.api.resume()
				self.game_paused = False 
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
     
			elif option_button.get_rect().collidepoint(x,y) and os.name == 'nt': # os.name == 'nt' is for windows only because the click on the option button is not working on linux
				self.api.pause()
				self.in_game_menu.main_loop()
				if self.in_game_menu.is_option_changed():
					self.change_api_option(self.in_game_menu.get_options())
				self.api.resume()


		pygame.init()
		pygame.display.set_caption("Simulation of Bobs")
		self.screen.fill(BLUE_SKY)
		clock = pygame.time.Clock()

		backforward = Sprite_UI(self.screen_width - 160, 10, self.assets["backforward"])
		backforward.set_active(False)
		fastforward = Sprite_UI(self.screen_width - 40, 10, self.assets["fastforward"])
		fastforward.set_active(False)
		pause_button = Sprite_UI(self.screen_width - 120, 10, self.assets["pause"])
		pause_button.set_active(True)
		play_button = Sprite_UI(self.screen_width - 80, 10, self.assets["play"])
		play_button.set_active(False)
		play_buttonmusic = Sprite_UI(self.screen_width - 240, 10, self.assets["playmusic"])
		play_buttonmusic.set_active(True)
		music_playing = False
		

		option_button = Sprite_UI(self.screen_width - 200, 10, self.assets["option"])
		option_button.set_active(False)
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
		ui_element.add(option_button)
		ui_element.add(play_buttonmusic)

		self.draw_better_world(True)
		self.api.start()


		rendering = True
		self.running = True

		while self.running:
			self.data = self.api.get_shared_data()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.api.resume() 
					self.api.stop()
					self.running = False
				elif event.type == pygame.VIDEORESIZE:
					self.screen_height = event.size[1]
					self.screen_width = event.size[0]
					pause_button.update_position((self.screen_width - 120, 10))
					play_button.update_position((self.screen_width - 80, 10))
					play_buttonmusic.update_position((self.screen_width - 240, 10))
					fastforward.update_position((self.screen_width - 40, 10))
					backforward.update_position((self.screen_width - 160, 10))
					option_button.update_position((self.screen_width - 200, 10))

				elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
					if rendering:
						rendering = False
					else:
						rendering = True

				elif event.type == pygame.MOUSEBUTTONDOWN:
					ui_tick_modification(event.pos)
					if play_buttonmusic.get_rect().collidepoint(event.pos):
           				 # Inverser l'état de la musique
						music_playing = not music_playing

            			# En fonction de l'état, démarrer ou arrêter la musique
						if music_playing:
							play_buttonmusic.set_active(False)
							play_buttonmusic.change_color()
							pygame.mixer.unpause()
						else:
							pygame.mixer.pause()
							play_buttonmusic.set_active(True)
							play_buttonmusic.change_color()

				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.api.pause()
						self.in_game_menu.main_loop()
						if self.in_game_menu.is_option_changed():
							self.change_api_option(self.in_game_menu.get_options())
						self.api.resume()

					elif event.key == pygame.K_SPACE:
						if self.game_paused:
							self.api.resume()
							self.game_paused = False
							pause_button.set_active(False)
							play_button.set_active(True)
							change_color_all_ui()
						else:
							self.api.pause()
							self.game_paused = True
							pause_button.set_active(True)
							play_button.set_active(False)
							change_color_all_ui()

  
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
			self.show_bob_stats()
			
			# Updating the display
			pygame.display.set_caption(f"Simulation of Bobs\tFPS: {int(clock.get_fps())}")
			pygame.display.flip()
			clock.tick()

	def close_display(self):
		'''
		Closes the game display and stops the game.
		This function is called to properly exit the game, ensuring all resources are released.
		'''
		self.running = False
		self.api.stop()
		pygame.quit()
	


	def show_bob_stats(self):
		"""
		Displays statistics of Bobs and Food.
		This function shows detailed information like position, energy, mass, etc., when hovering over game objects.
		"""
		nb_bob = 0
		nb_food = 0
		mouse_x, mouse_y = pygame.mouse.get_pos()

		rect_width = 150
		height_coef_bob = 140
		height_coef_food = 70
  
		rect_height = 0
    
		for _ in self.object_stats:
			if isinstance(_, Bob):
				rect_height += height_coef_bob
			elif isinstance(_, Food):
				rect_height += height_coef_food
    
		rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)

		rect_color = (0, 0, 0, 128)
		pygame.draw.rect(rect_surface, rect_color, rect_surface.get_rect(), border_radius=18)

		self.screen.blit(rect_surface, (mouse_x - 150, mouse_y))

		for obj in self.object_stats:
			if isinstance(obj, Bob):
				self.screen.blit(pygame.font.Font(None, 25).render(f"Bob {obj.get_name()} :", True, WHITE), (mouse_x - 140, mouse_y + nb_bob * height_coef_bob + 10 + nb_food * height_coef_food))
				self.screen.blit(pygame.font.Font(None, 20).render(f"- Position {obj.get_pos()}", True, WHITE), (mouse_x - 130, mouse_y + nb_bob * height_coef_bob + 30 + nb_food * height_coef_food))
				self.screen.blit(pygame.font.Font(None, 20).render(f"- Energy {obj.get_energy()}", True, WHITE), (mouse_x - 130, mouse_y + nb_bob * height_coef_bob + 45 + nb_food * height_coef_food))
				self.screen.blit(pygame.font.Font(None, 20).render(f"- Mass {obj.get_mass()}", True, WHITE), (mouse_x - 130, mouse_y + nb_bob * height_coef_bob + 60 + nb_food * height_coef_food))
				self.screen.blit(pygame.font.Font(None, 20).render(f"- Velocity {obj.get_velocity()}", True, WHITE), (mouse_x - 130, mouse_y + nb_bob * height_coef_bob + 75 + nb_food * height_coef_food))
				self.screen.blit(pygame.font.Font(None, 20).render(f"- Perception {obj.get_perception()}", True, WHITE), (mouse_x - 130, mouse_y + nb_bob * height_coef_bob + 90 + nb_food * height_coef_food))
				self.screen.blit(pygame.font.Font(None, 20).render(f"- Memory point {obj.get_memory_points()}", True, WHITE), (mouse_x - 130, mouse_y + nb_bob * height_coef_bob + 105 + nb_food * height_coef_food))
				self.screen.blit(pygame.font.Font(None, 20).render(f"- Height {obj.get_world().get_terrain().get_terrain()[obj.get_pos()[0]][obj.get_pos()[1]]}", True, WHITE), (mouse_x - 130, mouse_y + nb_bob * height_coef_bob + 120 + nb_food * height_coef_food)) if self.data["terrain"] else None
				nb_bob += 1
			elif isinstance(obj, Food):
				self.screen.blit(pygame.font.Font(None, 25).render(f"Food {nb_food + 1} :", True, WHITE), (mouse_x - 140, mouse_y + nb_food * height_coef_food + 10 + nb_bob * height_coef_bob))
				self.screen.blit(pygame.font.Font(None, 20).render(f"- Position {obj.get_pos()}", True, WHITE), (mouse_x - 130, mouse_y + nb_food * height_coef_food + 30 + nb_bob * height_coef_bob))
				self.screen.blit(pygame.font.Font(None, 20).render(f"- Energy {obj.get_value()}", True, WHITE), (mouse_x - 130, mouse_y + nb_food * height_coef_food + 45 + nb_bob * height_coef_bob))
				nb_food += 1

		self.object_stats = []
