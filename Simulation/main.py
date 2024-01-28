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
		"max_height" : 3,
		"seed" : 6432,
		 "water_level" : 0,
		}
	
	toggle_fonction = {
            "move_smart" : False,
            "sexual_reproduction" : False,
            "custom_event" : False,
            "reproduce" : True,
            "perception" : False,
            "memory" : False,
            "eat_bob" : False,
        }

	world = World({
			"size": 5,
            "nbFood": 0,
            "Food_energy": 100,
            "bob_max_energy": 200,
            "bob_energy": 100,
            "bob_velocity": 1,
            "bob_mass": 1,
            "bob_perception": 0,
            "dayTick": 100,
            "bob_mutation": 0,
            "bob_memory_point": 0,
            "custom_terrain" : True,
            "event_days_rate" : 100,
            "toggle_fonction" : toggle_fonction,

		}, terrain_config)
	
#------------------------BATTERIE DE TESTS------------------------#
	#Test prédation
	
	# world.enable_function["eat_bob"] = True
	# world.enable_function["move_smart"] = True

	# world.spawn_bob(1,velocity=1,mass=3)
	# world.spawn_bob(1,velocity=1,mass=1)
	

	
	# #Test reproduction_sexual
	# world.enable_function["reproduce"] = False
	# world.enable_function["sexual_reproduction"] = True
	# world.enable_function["move_smart"] = True
	# world.spawn_bob(1,velocity=1,mass=1)
	# world.spawn_bob(1,velocity=1,mass=1)
	

	# #Test reproduction
	# print("Test reproduction")
	# world.enable_function["reproduce"] = True
	# world.enable_function["sexual_reproduction"] = False
	# world.enable_function["move_smart"] = True
	# world.spawn_bob(1,velocity=1,mass=1)
	

	# #Test velocity
	# print("Test velocity")
	# world.enable_function["reproduce"] = False
	# world.enable_function["sexual_reproduction"] = False
	# world.enable_function["move_smart"] = True
	# world.spawn_bob(1,velocity=1,mass=1)
	# world.spawn_bob(1,velocity=2,mass=1)
	# world.spawn_bob(1,velocity=3,mass=1)
	# world.spawn_bob(1,velocity=4,mass=1)


	#Test memory
	
	# print("Test memory")
	# world.enable_function["memory"] = True
	# world.enable_function["move_smart"] = True
	# world.enable_function["eat_bob"] = False
	# world.enable_function["perception"] = True
	# # world.spawn_bob(1,velocity=1,mass=1, perception = 1)
	# # world.spawn_bob(1,velocity=2,mass=2, perception = 0)
	# bob = Bob(2,3,world,velocity=1,mass=1, perception = 1)
	# bob1 = Bob(3,3,world,velocity=1,mass=1, perception = 1)

	# world.bobs[(2,3)]=[bob]
	# world.bobs[(3,3)]=[bob1]

	# save("test_memory",world)

	# world.spawn_bob(1,velocity=1,mass=1)
	# world.spawn_bob(1,velocity=5,mass=1)
	# world.spawn_bob(1,velocity=10,mass=1)

	# save("Test height lost energy",world)

	world.spawn_bob(1,velocity=1,mass=1)
	# save("Test height lost energy.pkl",world)

	api = Api(world, 500)
	ig = Ig_menu()
	display = Display(api, ig)
	ig.api = api
	ig.world = world
	ig.display = display
	display.main_loop()
