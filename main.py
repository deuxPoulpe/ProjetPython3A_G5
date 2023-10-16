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
		"custom_terrain" : True,
		}, terrain_config)
	

	nb_bob = 100

	for j in range(nb_bob):
		bob = Bob(random.randint(0,world.get_size()-1),random.randint(0,world.get_size()-1),world)
		if bob.get_pos() not in world.get_bobs():
			world.get_bobs()[bob.get_pos()] = []
		world.get_bobs()[bob.get_pos()].append(bob)
		

	Display(world).main_loop()


