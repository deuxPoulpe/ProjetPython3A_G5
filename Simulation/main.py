from world import World
from display import Display


if __name__ == "__main__":


	terrain_config = {
		"generate_river" : False,
		"number_of_river" : 3,
		"generate_lake" : False,
		"number_of_lake" : 1,
		"size_of_lake" : 20,
		"max_height" : 10,
		}

	world = World({
		"size" : 100,
		"nbFood" : 500,
		"dayTick" : 100,
		"Food_energy" : 100,
		"custom_terrain" : False,
		}, terrain_config)
	


	world.spawn_bob(500)

	display = Display(world)
	display.main_loop(100)
	display.graph()




