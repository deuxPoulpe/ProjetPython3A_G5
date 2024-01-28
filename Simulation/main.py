from menu import Menu, Ig_menu
from world import World
from api import Api
from menu import *
from bob import Bob
from display import Display
from Utility.save_utility import save


if __name__ == "__main__":

	# menu = Menu()
	# menu.menu_principal()
	# exit()

	terrain_config = {
		"generate_river" : False,
		"number_of_river" : 1,
		"generate_lake" : False,
		"number_of_lake" : 1,
		"size_of_lake" : 20,
		"max_height" : 10,
		"seed" : 6432,
		 "water_level" : 0,
		}

	world = World({
		"size" : 10,
		"nbFood" : 10,
		"dayTick" : 100,
		"Food_energy" : 100,
		"custom_terrain" : False,
		}, terrain_config)
	
#------------------------BATTERIE DE TESTS------------------------#
	#Test prédation
	""""
	world.enable_function["eat_bob"] = True
	world.enable_function["move_smart"] = True

	world.spawn_bob(1,velocity=5,mass=3)
	world.spawn_bob(1,velocity=1,mass=1)
	

	"""
	"""
	#Test reproduction_sexual
	world.enable_function["reproduce"] = False
	world.enable_function["sexual_reproduction"] = True
	world.enable_function["move_smart"] = True
	world.spawn_bob(1,velocity=1,mass=1)
	world.spawn_bob(1,velocity=1,mass=1)
	"""
	

	#Test reproduction
	"""
	print("Test reproduction")
	world.enable_function["reproduce"] = True
	world.enable_function["sexual_reproduction"] = False
	world.enable_function["move_smart"] = True
	world.spawn_bob(1,velocity=1,mass=1)
	"""

	#Test memory
	
	print("Test memory")
	world.enable_function["memory"] = True
	world.enable_function["move_smart"] = True
	world.enable_function["eat_bob"] = False
	world.enable_function["perception"] = True
	# world.spawn_bob(1,velocity=1,mass=1, perception = 1)
	# world.spawn_bob(1,velocity=2,mass=2, perception = 0)
	bob = Bob(2,3,world,velocity=1,mass=1, perception = 1)
	bob1 = Bob(3,3,world,velocity=1,mass=1, perception = 1)

	world.bobs[(2,3)]=[bob]
	world.bobs[(3,3)]=[bob1]

	#save("test_memory",world)
	

	

	


	api = Api(world, 500)
	ig = Ig_menu()
	display = Display(api, ig)
	ig.is_running = True
	ig.display = display
	ig.api = api
	ig.world = world
	display.main_loop()
