import pygame
import pygame_menu
from tiles import Tile
import os
import matplotlib.pyplot as plt
import numpy as np
from noise import snoise2
import random


class Display:
	def __init__(self,world):
		self.screen_width = 800
		self.screen_height = 600
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),pygame.RESIZABLE)
		self.floor_display = pygame.Surface((32 * world.get_size(), 22 * world.get_size()))
		self.world = world
		self.camera_x = 0
		self.camera_y = 0
		self.zoom_factor = 100
		self.zoom_speed = 50
		self.dragging = False
		self.drag_pos = None
		self.floor = pygame.sprite.Group()


		self.assets = {
			"grass": pygame.image.load(os.path.join("assets/tiles", "tile_028.png")).convert(),
			"dirt": pygame.image.load(os.path.join("assets/tiles", "tile_003.png")).convert(),
			"close_water": pygame.image.load(os.path.join("assets/tiles", "tile_020.png")).convert(),
			"water": pygame.image.load(os.path.join("assets/tiles", "tile_094.png")).convert(),
			"plants": []			
		}


		for k in range(0, 12):
			self.assets["plants"].append(pygame.image.load(os.path.join("assets/tiles", f"tile_0{k+41}.png")).convert())
			self.assets["plants"][k].set_colorkey((0, 0, 0))
		
		for key in self.assets:
			if key != "plants":
				self.assets[key].set_colorkey((0, 0, 0))


		self.previous_zoom_factor = self.zoom_factor  # Store the zoom level of the last frame
		self.needs_rescaling = True
		


	

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

	def generate_terrain(self ,size, scale=0.02, octaves=6, persistence=0.3, lacunarity=2.0, z_min=0, z_max=20):

		terrain = np.zeros((size, size))
		plant_to_add = np.zeros((size, size))
		random_seed = random.randint(0, 1024)
		
		for x in range(size):
			for y in range(size):
				terrain[x][y] = snoise2(x*scale + random_seed, 
										y*scale + random_seed,
										octaves=octaves, 
										persistence=persistence, 
										lacunarity=lacunarity
				)

		terrain = np.interp(terrain, (terrain.min(), terrain.max()), (z_min, z_max))
		terrain = np.round(terrain).astype(int)


		for i in range(random.randint(size , size*2)):
			x = random.randint(0,size-1)
			y = random.randint(0,size-1)
			plant_to_add[x][y] = 1

		return terrain, plant_to_add


	def draw_sprite_world(self):
		size = self.world.get_size()
		self.floor.empty()

		grid = self.generate_terrain(self.world.get_size())[0]
		plant_to_add = self.generate_terrain(self.world.get_size())[1]

		start_x = self.floor_display.get_size()[0] // 2
		start_y = self.floor_display.get_size()[1] // 5

		if self.world.get_argDict()["custom_terrain"]:
		
			for i in range(size):
				for j in range(size):
					for k in range(grid[i][j]):
						dirt = Tile(0,0, self.assets["dirt"])
						dirt.set_pos(start_x + (i - j) * 32 / 2, start_y + (i + j) * 32 / 4 - 9 * k)
						self.floor.add(dirt)
							
					if grid[i][j] <= 1:
						water = Tile(0,0, self.assets["water"])
						water.set_pos(start_x + (i - j) * 32 / 2, start_y + (i + j) * 32 / 4 - 15)
						self.floor.add(water)
					elif grid[i][j] == 2:
						tile = Tile(0,0, self.assets["close_water"])
						tile.set_pos(start_x + (i - j) * 32 / 2, start_y + (i + j) * 32 / 4 - 18)
						self.floor.add(tile)
					else:
						tile = Tile(0,0, self.assets["grass"])
						tile.set_pos(start_x + (i - j) * 32 / 2, start_y + (i + j) * 32 / 4 - 9 * grid[i][j])
						self.floor.add(tile)

					if plant_to_add[i][j]== 1 and grid[i][j] > 2:
						tile = Tile(0,0, self.assets["plants"][random.randint(0,11)])
						tile.set_pos(start_x + (i - j) * 32 / 2, start_y + (i + j) * 32 / 4 - 9 * (grid[i][j]+1))
						self.floor.add(tile)


		else:
			for i in range(size):
				for j in range(size):
					tile = Tile(0,0, self.grass)
					tile.set_pos(start_x + (i - j) * 32 / 2, start_y + (i + j) * 32 / 4)
					self.floor.add(tile)

		self.floor.draw(self.floor_display)		


	def render(self):
		self.screen.fill((135,206,250))
		# self.draw_world()

		if self.needs_rescaling:
				
			self.floor_display_temp = pygame.Surface((6*self.zoom_factor, 3*self.zoom_factor))
			self.floor_display_temp.set_colorkey((0, 0, 0))
			pygame.transform.scale(self.floor_display, (6*self.zoom_factor, 3*self.zoom_factor), self.floor_display_temp)

			self.needs_rescaling = False

		grid_x = -self.camera_x + self.screen_width // 2 - self.floor_display_temp.get_size()[0] // 2
		grid_y = -self.camera_y + self.screen_height // 2 - self.floor_display_temp.get_size()[1] // 2
		
		self.screen.blit(self.floor_display_temp, ( grid_x , grid_y))
		
	def main_loop(self):
		pygame.init()
		pygame.display.set_caption("Simulation of Bobs")
		clock = pygame.time.Clock()
		font = pygame.font.Font(None, 20)

		running = True
		self.draw_sprite_world()
		
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
