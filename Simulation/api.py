import time
import multiprocessing as mp

class Api:
	
	def __init__(self, world, tick_interval_ms):
		self.world_sim = world
		self.tick_interval = tick_interval_ms
		self.process = None
		self.shared_data = mp.Manager().dict()
		self.quit = False
		self.update_shared_data()
  
	def get_data_bobs(self):
		return self.shared_data['bobs']
	def get_data_foods(self):
		return self.shared_data['foods']
	def get_data_terrain(self):
		return self.shared_data['terrain']
	def get_data_world_size(self):
		return self.shared_data['world_size']
	def get_data_tick(self):
		return self.shared_data['tick']
	def get_data_nb_bob(self):
		return self.shared_data['nb_bob']
	def get_data_nb_food(self):
		return self.shared_data['nb_food']
	def get_date_argDict(self):
		return self.shared_data['argDict']
     

	def pause(self):
		if self.process is not None:
			self.process.suspend()
  
	def resume(self):
		if self.process is not None:
			self.process.resume()

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
  
  
	def run(self):
		while True:
			start = time.time()
			self.world_sim.update_tick()
			self.update_shared_data()

			time.sleep(self.tick_interval/1000)
			print("tick time : " + str(time.time() - start))


   
			
   
	def stop(self):
		if self.process is not None:
			exit()
			
   