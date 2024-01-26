from world import World
from display import Display
from api import Api
from menu import *


if __name__ == "__main__":

	# menu = Menu()
	# menu.menu_principal()

	terrain_config = {
		"generate_river" : True,
		"number_of_river" : 1,
		"generate_lake" : False,
		"number_of_lake" : 1,
		"size_of_lake" : 20,
		"max_height" : 10,
		"seed" : 6432,
		}

	world = World({
		"size" : 10,
		"nbFood" : 1,
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
	
	#Test reproduction_sexual

	"""
	world.enable_function["reproduce"] = False
	world.enable_function["sexual_reproduction"] = True
	world.spawn_bob(1,velocity=1,mass=1)
	world.spawn_bob(1,velocity=1,mass=1)
	"""	
	#Test reproduction
	"""
	print("Test reproduction")
	world.enable_function["reproduce"] = True
	world.enable_function["sexual_reproduction"] = False
	world.spawn_bob(1,velocity=1,mass=1)
	for position, liste_objets in world.get_bobs().items():
		for objet in liste_objets:
			print(objet.get_energy())
	"""

	#Test perception
	
	print("Test perception")
	world.enable_function["move_smart"] = True
	world.enable_function["eat_bob"] = True
	world.enable_function["perception"] = True
	world.spawn_bob(1, velocity = 5, mass=4, perception = 30)
	world.spawn_bob(1, velocity = 1, mass=1, perception = 0)

	for j in world.population_bob:
		print(j.get_perception)
		

	api = Api(world, 500)
	display = Display(api)
	display.main_loop()
