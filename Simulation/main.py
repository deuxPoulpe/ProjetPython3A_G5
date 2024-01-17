from world import World
from display import Display
from api import Api


if __name__ == "__main__":


	terrain_config = {
		"generate_river" : True,
		"number_of_river" : 1,
		"generate_lake" : True,
		"number_of_lake" : 2,
		"size_of_lake" : 20,
		"max_height" : 10,
		"seed" : 543,
		}

	world = World({
		"size" : 50,
		"nbFood" : 500,
		"dayTick" : 100,
		"Food_energy" : 100,
		"custom_terrain" : True,
		}, terrain_config)
	


	world.spawn_bob(500)
	api = Api(world, 1)
	display = Display(api)
	display.main_loop()
 
