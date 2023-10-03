from world import World
from display import Display


if __name__ == "__main__":

	world = World({
		"size" : 100,
		"nbFood" : 200,
		"dayTick" : 100,
		"custom_terrain" : True,
		"generate_river" : True,
	})

	Display(world).main_loop()
