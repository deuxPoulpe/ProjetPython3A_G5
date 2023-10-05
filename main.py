from world import World
from display import Display


if __name__ == "__main__":


	terrain_config = {
		"number_of_river" : 1,
		"generate_river" : True,
		"generate_lake" : True,
		"number_of_lake" : 2,
		"size_of_lake" : 20,
		"max_height" : 7,
		}

	world = World({
		"size" : 100,
		"nbFood" : 200,
		"dayTick" : 100,
		"custom_terrain" : True,
		}, terrain_config)

	Display(world).main_loop()
