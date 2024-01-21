from world import World
from display import Display
from api import Api


if __name__ == "__main__":


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
		"size" : 50,
		"nbFood" : 50,
		"dayTick" : 100,
		"Food_energy" : 100,
		"custom_terrain" : True,
		}, terrain_config)
	


	world.spawn_bob(50)
	api = Api(world, 500)
	display = Display(api)
	display.main_loop()
 
