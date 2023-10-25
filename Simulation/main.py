from world import World
from display import Display
from bob import Bob
import random


if __name__ == "__main__":


	terrain_config = {
		"generate_river" : True,
		"number_of_river" : 1,
		"generate_lake" : False,
		"number_of_lake" : 1,
		"size_of_lake" : 20,
		"max_height" : 10,
		}

	world = World({
		"size" : 100,
		"nbFood" : 200,
		"dayTick" : 100,
		"custom_terrain" : False,
		}, terrain_config)
	

	nb_bob = 100

	world.spawn_bob(30)
	world.spawn_food(30)	

	Display(world).main_loop()



