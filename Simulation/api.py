import time
import multiprocessing as mp

class Api:
	
	def __init__(self, world, tick_interval_ms):
		self.world_sim = world
		self.tick_interval = mp.Manager().Value('i', tick_interval_ms)
		self.process = None
		self.shared_data = mp.Manager().dict()
		self.quit = False
		self.update_shared_data()
		self.shared_data['real_tick_time'] = 0
		self.running = mp.Manager().Value('i', False)
		self.paused = mp.Manager().Value('i', False)


	def get_tick_interval(self):
		return self.tick_interval.value
	def set_tick_interval(self, tick_interval_ms):
		self.tick_interval.value = tick_interval_ms
	def get_shared_data(self):
		return self.shared_data
     

	def pause(self):
		if self.process is not None:
			self.paused.value = True
  
	def resume(self):
		if self.process is not None:
			self.paused.value = False

	def start(self):
		self.process = mp.Process(target=self.run)
		self.process.start()
  
	def update_shared_data(self):
		self.shared_data['bobs'] = self.world_sim.get_bobs()
		self.shared_data['foods'] = self.world_sim.get_foods()
		self.shared_data['terrain'] = self.world_sim.get_terrain()
		self.shared_data['world_size'] = self.world_sim.get_size()
		self.shared_data['tick'] = self.world_sim.get_tick()
		self.shared_data['nb_bob'] = self.world_sim.get_nb_bob()
		self.shared_data['nb_food'] = self.world_sim.get_nb_food()
		self.shared_data['argDict'] = self.world_sim.get_argDict()
		self.shared_data['water_level'] = self.world_sim.get_water_level()
  
  
	def run(self):
		self.running.value = True
		while self.running.value:
			start = time.time()
			if not self.paused.value:
				
				self.world_sim.update_tick()
				self.update_shared_data()

			time.sleep(self.tick_interval.value/1000)
			self.shared_data['real_tick_time'] = time.time() - start
   


   
			
   
	def stop(self):
		if self.process is not None:
			self.running.value = False
			self.process.join()
   
   
			
   