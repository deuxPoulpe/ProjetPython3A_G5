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
		"custom_terrain" : True,
		}, terrain_config)
	

	for i in range(20):
		for j in range(20):
			bob = Bob(i,j,world)
			if bob.get_pos() not in world.get_bobs():
				world.get_bobs()[bob.get_pos()] = []
			world.get_bobs()[bob.get_pos()].append(bob)
		

	Display(world).main_loop()


