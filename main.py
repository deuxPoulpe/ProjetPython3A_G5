from world import World
from display import Display
from bob import Bob


if __name__ == "__main__":


	terrain_config = {
		"generate_river" : True,
		"number_of_river" : 2,
		"generate_lake" : True,
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
	

	Display(world).main_loop()


