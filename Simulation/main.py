from menu import Menu, Ig_menu
from world import World
from api import Api
from bob import Bob
from display import Display


if __name__ == "__main__":

	terrain_config = {
		"generate_river" : True,
		"number_of_river" : 1,
		"generate_lake" : False,
		"number_of_lake" : 1,
		"size_of_lake" : 20,
		"max_height" : 10,
		"seed" : 6432,
		 "water_level" : 0,
		}

	world = World({
		"size" : 20,
		"nbFood" : 50,
		"dayTick" : 100,
		"Food_energy" : 100,
		"custom_terrain" : False,
		}, terrain_config)
	

	world.spawn_bob(1)
	api = Api(world, 500)
	ig = Ig_menu()
	display = Display(api, ig)
	display.main_loop()

	# menu = Menu()
	# menu.menu_principal()
