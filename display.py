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
		self.floor_display = pygame.Surface((32 * world.get_size(), 20 * world.get_size()))
		self.world = world
		self.camera_x = 0
		self.camera_y = 0
		self.zoom_factor = 100
		self.zoom_speed = 50
		self.dragging = False
		self.drag_pos = None
		self.floor = pygame.sprite.Group()


		self.grass = pygame.image.load(os.path.join("assets/tiles", "tile_028.png")).convert()
		self.dirt = pygame.image.load(os.path.join("assets/tiles", "tile_000.png")).convert()
		self.water = pygame.image.load(os.path.join("assets/tiles", "tile_094.png")).convert()
		self.grass.set_colorkey((0, 0, 0))
		self.dirt.set_colorkey((0, 0, 0))
		self.water.set_colorkey((0, 0, 0))


	

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

	def generate_terrain(self,size, scale=0.05, octaves=10, persistence=0.5, lacunarity=2.0, z_min=0, z_max=5):

		terrain = np.zeros((size, size))
		random_seed = random.randint(0, 1024)
		
		for x in range(size):
			for y in range(size):
				terrain[x][y] = snoise2(x*scale + random_seed, 
										y*scale + random_seed,
										octaves=octaves, 
										persistence=persistence, 
										lacunarity=lacunarity
				)

		# Normalisation du terrain pour le ramener entre z_min et z_max
		terrain = np.interp(terrain, (terrain.min(), terrain.max()), (z_min, z_max))
		terrain = np.round(terrain).astype(int)

		return terrain


	def draw_isometric_grid(self):
		size = self.world.get_size()
		self.floor.empty()

		grid = self.generate_terrain(self.world.get_size())

		start_x = self.floor_display.get_size()[0] // 2
		start_y = self.floor_display.get_size()[1] // 20

		
		for i in range(size):
			for j in range(size):
				if grid[i][j] == 5 or grid[i][j] == 4:
					water = Tile(0,0, self.water)
					water.set_pos(start_x + (i - j) * 32 / 2, start_y + (i + j) * 32 / 4 + 27)
					self.floor.add(water)
				else:
					tile = Tile(0,0, self.grass)
					dirt = Tile(0,0, self.dirt)
					dirt.set_pos(start_x + (i - j) * 32 / 2, start_y + (i + j) * 32 / 4 + 9 * (grid[i][j]+1))
					tile.set_pos(start_x + (i - j) * 32 / 2, start_y + (i + j) * 32 / 4 + 9 * grid[i][j])
					self.floor.add(dirt)
					self.floor.add(tile)
					
				

					
		
		
		self.floor.draw(self.floor_display)		
		self.floor_display.set_colorkey((0, 0, 0))


	def render(self):
		self.screen.fill((135,206,250))
		# self.draw_world()


		floor_display_temp = pygame.transform.scale(self.floor_display, (6*self.zoom_factor, 3*self.zoom_factor))

		grid_x = -self.camera_x + self.screen_width // 2 - floor_display_temp.get_size()[0] // 2
		grid_y = -self.camera_y + self.screen_height // 2 - floor_display_temp.get_size()[1] // 2
		
		self.screen.blit(floor_display_temp, ( grid_x , grid_y))
		
	def main_loop(self):
		pygame.init()
		pygame.display.set_caption("Simulation of Bobs")
		clock = pygame.time.Clock()
		font = pygame.font.Font(None, 20)

		running = True
		self.draw_isometric_grid()
		
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
