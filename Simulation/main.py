from world import World
from display import Display


if __name__ == "__main__":


	terrain_config = {
		"generate_river" : True,
		"number_of_river" : 1,
		"generate_lake" : True,
		"number_of_lake" : 1,
		"size_of_lake" : 20,
		"max_height" : 10,
		}

	world = World({
		"size" : 100,
		"nbFood" : 200,
		"dayTick" : 100,
		"Food_energy" : 100,
		"custom_terrain" : True,
		}, terrain_config)
	


	world.spawn_bob(30)

	display = Display(world)
	display.main_loop(100)



