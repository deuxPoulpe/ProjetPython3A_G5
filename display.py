import pygame
import pygame_menu


class Display:
	def __init__(self,world):
		self.screen_width = 800
		self.screen_height = 600
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height),pygame.RESIZABLE)
		self.world = world
		self.camera_x = 0
		self.camera_y = 0
		self.zoom_factor = 100
		self.zoom_speed = 10
		self.dragging = False
		self.drag_pos = None

	

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



	def main_loop(self):
		pygame.init()
		pygame.display.set_caption("Simulation of Bobs")
		clock = pygame.time.Clock()

		running = True
		while running:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				
				self.zoom(event)
				self.start_drag(event)

			self.camera()
			self.screen.fill((135,206,250))
			self.draw_world()
			pygame.display.flip()


			
			clock.tick()

