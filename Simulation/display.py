import sys
import pygame
import pygame_menu
from sprite import Tile
from sprite import Sprite_bob
import os
import matplotlib.pyplot as plt
import random
from math import sqrt



from occlusion_utility import hide_behind_terrain_image
from occlusion_utility import tile_to_array
from occlusion_utility import show_time



class Display:
	def __init__(self,world):
		self.world = world

		self.screen_width = 800
		self.screen_height = 600
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),pygame.RESIZABLE)

		self.floor_display = pygame.Surface((32 * world.get_size(), 16 * world.get_size() + 250))
		self.sprite_display = pygame.Surface((32 * world.get_size(), 16 * world.get_size() + 250))
		
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
	

	def draw_world(self):
		
		size = self.world.getSize()
		start_x = self.screen_width // 2 - self.camera_x
		start_y = self.screen_height // 10 - self.camera_y

		iso_size_x =self.zoom_factor / 25
		iso_size_y =self.zoom_factor / 50

		floor = [
			(start_x, start_y),
			(start_x + iso_size_x * size, start_y + iso_size_y * size),
			(start_x , start_y + iso_size_y * size * 2),
			(start_x - iso_size_x * size, start_y + iso_size_y * size),
		]

		base = [
			(start_x, start_y),
			(start_x + iso_size_x * size, start_y + iso_size_y * size),
			(start_x + iso_size_x * size, start_y + iso_size_y * size + iso_size_y * size / 3),
			(start_x , start_y + iso_size_y * size * 2 + iso_size_y * size / 3),
			(start_x - iso_size_x * size, start_y + iso_size_y * size + iso_size_y * size / 3),
			(start_x - iso_size_x * size, start_y + iso_size_y * size),
		]

		pygame.gfxdraw.filled_polygon(self.screen, base, (26, 13, 0))
		pygame.gfxdraw.filled_polygon(self.screen, floor, (25, 102, 8))

		for k in range(size + 1):
			pygame.gfxdraw.line(self.screen, 
								int(start_x + iso_size_x*k), int(start_y + iso_size_y*k),
								int(start_x - iso_size_x*(size - k)), int(start_y + iso_size_y*(size+k)),
								(0, 51, 51))

			pygame.gfxdraw.line(self.screen,
								int(start_x - iso_size_x*k), int(start_y + iso_size_y*k),
								int(start_x + iso_size_x*(size - k)), int(start_y + iso_size_y*(size+k)),
								(0, 51, 51))

			

	def zoom(self,event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
			self.zoom_factor += self.zoom_speed
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
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
		if grid[i][j] == 0:
			y = start_y + (i + j) * 32 / 4 - 7 - 16
			tile = Tile(x,y, self.assets["water"])
		elif grid[i][j] == 1:
			y = start_y + (i + j) * 32 / 4 - 9 - 16
			tile = Tile(x,y, self.assets["close_water"])
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
		size = self.world.get_size()
		self.floor.empty()


		start_x = self.floor_display.get_size()[0] // 2
		start_y = self.floor_display.get_size()[1] - 16 * (self.world.get_size()+1)

		terrain = self.world.get_terrain()

		self.screen.blit(pygame.font.Font(None, 20).render(f"Génération du terrain en cours ...", True, (255,255,255)),
					 (self.screen_width/2 - 100, self.screen_height/2))
		pygame.display.flip()

		if terrain:
			grid = terrain.get_terrain()
			decoration_to_add = terrain.get_decoration_to_add()
			self.tile_array = tile_to_array(self.assets["grass"])
		
			for i in range(size):
				for j in range(size):
					self.draw_empty_world(start_x,start_y,i,j,grid)
					self.draw_surface_world(start_x,start_y,i,j,grid)
					# self.draw_decoration_world(start_x,start_y,i,j,grid,decoration_to_add)

		else:
			for i in range(size):
				for j in range(size):
					tile = Tile(start_x + (i - j) * 32 / 2 - 16, start_y + (i + j) * 32 / 4 - 16, self.assets["clean_grass"])
					self.floor.add(tile)

		self.floor.draw(self.floor_display)	


	def draw_bobs(self):
		bobs = pygame.sprite.Group()

		start_x = self.sprite_display.get_size()[0] // 2
		start_y = self.sprite_display.get_size()[1] - 16 * (self.world.get_size()+1)

		terrain = self.world.get_terrain()

		all_bobs = self.world.get_bobs()
		

		if not terrain:
			for key in all_bobs:
				for bob in all_bobs[key]:
					i,j = key
					size = sqrt(bob.get_mass())
					x = start_x + (i - j) * 16 - 8 * size
					y = start_y + (i + j) * 8 - 15 * size
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
		start_y = self.sprite_display.get_size()[1] - 16 * (self.world.get_size()+1)

		terrain = self.world.get_terrain()

		all_foods = self.world.get_foods()
		

		if not terrain:
			for key in all_foods:
				for food in all_foods[key]:
					i,j = key
					x = start_x + (i - j) * 16 - 8
					y = start_y + (i + j) * 8 - 15
					food_s = Sprite_bob(x,y, self.assets["foods_banana"], 1)
					foods.add(food_s)
		else:
			grid_of_height = terrain.get_terrain()
			for key in all_foods:
				for food in all_foods[key]:
					i,j = key
					base = grid_of_height[i][j]

					x = start_x + (i - j) * 16 - 8 
					y = start_y + (i + j) * 8 - 15 - 9 * base
					
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
				
			self.floor_display_temp = pygame.Surface((scale_x, scale_y))
			self.floor_display_temp.set_colorkey((0, 0, 0))
			pygame.transform.scale(self.floor_display, (scale_x, scale_y), self.floor_display_temp)
			# self.floor_display_temp = pygame.transform.chop(self.floor_display_temp, (0, 0, 20, 20)) 


			self.needs_rescaling = False
			self.sprite_display_temp = pygame.Surface((scale_x, scale_y))
			self.sprite_display_temp.set_colorkey((0, 0, 0))
			pygame.transform.scale(self.sprite_display, (scale_x, scale_y), self.sprite_display_temp)

	
	def render(self):
		self.screen.fill((135,206,250))
		self.sprite_display.fill((0,0,0))

		show_time(self.draw_bobs)
		self.draw_foods()


		self.zooming_render()

		grid_x = -self.camera_x + self.screen_width // 2 - self.floor_display_temp.get_size()[0] // 2
		grid_y = -self.camera_y + self.screen_height // 2 - self.floor_display_temp.get_size()[1] // 2

		
		self.screen.blit(self.floor_display_temp, ( grid_x , grid_y))
		self.screen.blit(self.sprite_display_temp, ( grid_x , grid_y))
		
		
	def main_loop(self):
		pygame.init()
		pygame.display.set_caption("Simulation of Bobs")
		self.screen.fill((135,206,250))
		clock = pygame.time.Clock()
		font = pygame.font.Font(None, 20)

		running = True
		self.draw_better_world()
		# self.hide_behind_terrain(self.assets["full_bob"], (0,0), self.world.terrain.get_terrain())

		
		while running:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.VIDEORESIZE:
					self.screen_height = event.size[1]
					self.screen_width = event.size[0]
				
				self.zoom(event)
				self.start_drag(event)
				
			self.camera()

			self.render()
			

			pygame.display.set_caption(f"Simulation of Bobs\tFPS: {int(clock.get_fps())}")


			pygame.display.flip()


			
			clock.tick()
