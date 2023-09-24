import pygame
import pygame_menu
from world import World
from graphique import Affichage_graphique

class Menu:

	def __init__(self):
		self.world_size_input = None
		self.initial_bob_count_input = None
		self.food_per_day_input = None
		self.food_value_input = None
		self.max_energy_input = None
		self.tick_interval_input = None


	def run_simulation(self):
		pygame.quit()

		world_size = int(self.world_size_input.get_value())
		initial_bob_count = int(self.initial_bob_count_input.get_value())
		food_per_day = int(self.food_per_day_input.get_value())
		food_value = int(self.food_value_input.get_value())
		maxEnergy = int(self.max_energy_input.get_value())
		tick_interval = int(self.tick_interval_input.get_value())

		world = World(world_size, food_per_day, food_value, maxEnergy)
		world.spawn("bob", initial_bob_count)
		graphique = Affichage_graphique(world)
		graphique.run(tick_interval)
		graphique.graph()


	def main_menu(self):

		
		pygame.init()

		mytheme = pygame_menu.themes.THEME_DARK.copy()
		mytheme.widget_font = pygame_menu.font.FONT_FRANCHISE
		mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE


		screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
		pygame.display.set_caption("Simulation of Bobs")

		menu = pygame_menu.Menu(
			height=720,
			theme=mytheme,
			title='Simulation of Bobs',
			width=1280
		)


		def on_resize():
			menu.resize(screen.get_size()[0], screen.get_size()[1])


	
		self.world_size_input = menu.add.text_input('World Size: ', default="50", maxchar=4, input_type=pygame_menu.locals.INPUT_INT)
		self.initial_bob_count_input = menu.add.text_input('Initial Bob Count: ', default="50", maxchar=4, input_type=pygame_menu.locals.INPUT_INT)
		self.food_per_day_input = menu.add.text_input('Food Per Day: ', default="50", maxchar=4, input_type=pygame_menu.locals.INPUT_INT)
		self.food_value_input = menu.add.text_input('Food Value: ', default="200", maxchar=4, input_type=pygame_menu.locals.INPUT_INT)
		self.max_energy_input = menu.add.text_input('Max Energy: ', default="200", maxchar=4, input_type=pygame_menu.locals.INPUT_INT)
		self.tick_interval_input = menu.add.text_input('Tick Interval (ms): ', default="1", maxchar=4, input_type=pygame_menu.locals.INPUT_INT)

		
		menu.add.button('Start Single Simulation', self.run_simulation)

		menu.add.button('Exit', pygame_menu.events.EXIT)
		menu.enable()
		on_resize()

		while True:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					break
				if event.type == pygame.VIDEORESIZE:
					screen = pygame.display.set_mode((event.size[0], event.size[1]), pygame.RESIZABLE)
					on_resize()

			# Draw the menu
			screen.fill((25, 0, 50))

			menu.update(events)
			menu.draw(screen)
			

			pygame.display.flip()


