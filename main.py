from world import World
from display import Display


if __name__ == "__main__":


	terrain_config = {
		"generate_river" : True,
		"number_of_river" : 2,
		"generate_lake" : False,
		"number_of_lake" : 1,
		"size_of_lake" : 50,
		"max_height" : 10,
		}

	world = World({
		"size" : 500,
		"nbFood" : 200,
		"dayTick" : 100,
		"custom_terrain" : True,
		}, terrain_config)

	Display(world).main_loop()
