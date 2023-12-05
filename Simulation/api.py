import time
import multiprocessing as mp

class Api:
	
	def __init__(self, world, tick_interval_ms):
		self.world_sim = world
		self.tick_interval = tick_interval_ms



	def get_world_bobs(self):
		return self.world_sim.get_bobs()
	def get_world_foods(self):
		return self.world_sim.get_foods()
	def get_world_terrain(self):
		return self.world_sim.get_terrain()
	def get_world_size(self):
		return self.world_sim.get_size()


	def main_loop(self):
		while True:
			time.sleep(self.tick_interval)
			self.world_sim.update_tick()