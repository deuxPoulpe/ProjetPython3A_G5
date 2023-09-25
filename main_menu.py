import pygame
import pygame_menu
from world import World
from graphique import Affichage_graphique

class Menu:

	
	def main_menu(self):

		def on_resize():
			menu.resize(screen.get_size()[0]*0.4, screen.get_size()[1]*0.7)	

			
		def run_simulation():
			global running
			pygame_menu.events.CLOSE
			pygame.quit()
			running = False
			

			world_size = int(world_size_input.get_value())
			initial_bob_count = int(initial_bob_count_input.get_value())
			food_per_day = int(food_per_day_input.get_value())
			food_value = int(food_value_input.get_value())
			maxEnergy = int(max_energy_input.get_value())
			tick_interval = int(tick_interval_input.get_value())
			tickDays = int(tick_days_input.get_value())

			world = World(world_size, food_per_day, food_value, maxEnergy, tickDays)
			world.spawn("bob", initial_bob_count)
			graphique = Affichage_graphique(world)
			graphique.run(tick_interval)
			graphique.graph()

		pygame.init()
	
		mytheme = pygame_menu.themes.THEME_BLUE.copy()
		mytheme.widget_font = pygame_menu.font.FONT_MUNRO
		mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE
		mytheme.title_font = pygame_menu.font.FONT_MUNRO
		mytheme.title_font_color = (0, 0, 0)
		mytheme.title_font_background_color = (255, 255, 255)
		mytheme.title_font_shadow = False
		mytheme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
		mytheme.cursor_selection_color = (0, 0, 0, 120)
		mytheme.selection_color = (0, 0, 0)

		screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
		pygame.display.set_caption("Simulation of Bobs")

		menu = pygame_menu.Menu(
			height=720,
			theme=mytheme,
			title='Simulation of Bobs',
			width=1280
		)

	
		world_size_input = menu.add.text_input('World Size: ', default="100", maxchar=4, input_type=pygame_menu.locals.INPUT_INT)
		initial_bob_count_input = menu.add.text_input('Initial Bob Count: ', default="100", maxchar=4, input_type=pygame_menu.locals.INPUT_INT)
		food_per_day_input = menu.add.text_input('Food Per Day: ', default="200", maxchar=4, input_type=pygame_menu.locals.INPUT_INT)
		food_value_input = menu.add.text_input('Food Value: ', default="100", maxchar=4, input_type=pygame_menu.locals.INPUT_INT)
		max_energy_input = menu.add.text_input('Max Energy: ', default="200", maxchar=4, input_type=pygame_menu.locals.INPUT_INT)
		tick_interval_input = menu.add.text_input('Tick Interval (iteration): ', default="1", maxchar=4, input_type=pygame_menu.locals.INPUT_INT)
		tick_days_input = menu.add.text_input('Tick Days: ', default="100", maxchar=4, input_type=pygame_menu.locals.INPUT_INT)
		
		start_simu = menu.add.button("Start Single Simulation", run_simulation)
		start_simu.set_padding([40,0,0,0])
		menu.add.button("Exit", pygame_menu.events.EXIT)

		menu.enable()

		on_resize()
		running = True

		while running:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					break
				if event.type == pygame.VIDEORESIZE:
					screen = pygame.display.set_mode((event.size[0], event.size[1]), pygame.RESIZABLE)
					on_resize()

			screen.fill((135,206,250))

			menu.update(events)

			if not running:
				break
			menu.draw(screen)
			

			pygame.display.flip()


