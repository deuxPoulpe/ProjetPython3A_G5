import time
import multiprocessing as mp

class Api:
	
	def __init__(self, world, tick_interval_ms):

		self.data_lock = mp.Lock()
		self.world_sim = world
		self.tick_interval = mp.Manager().Value('i', tick_interval_ms)
		self.process = None
		self.shared_data = mp.Manager().dict()
		self.quit = False
		self.update_shared_data()
		self.shared_data['real_tick_time'] = 0
		self.shared_data['world'] = None
		self.shared_data['event'] = None
		self.shared_data['real_tick_time_data'] = []
		self.running = mp.Manager().Value('i', False)
		self.paused = mp.Manager().Value('i', True)
		self.option_shared_data = mp.Manager().list()
		self.option_shared_data.append(None)
		self.option_shared_data.append(None)
		self.option_shared_data.append(False)

		self.get_world = mp.Manager().Value('i', False)
		self.need_spawn_bob = mp.Manager().Value('i', False)
		self.ask_number_of_bob = mp.Manager().Value('i', 0)
		
	def change_options(self, argDict, terrain_config_dict):
		with self.data_lock:
			self.option_shared_data[0] = argDict
			self.option_shared_data[1] = terrain_config_dict
			self.option_shared_data[2] = True
   
	def is_changed_option(self):
		return self.option_shared_data[2]


	def get_tick_interval(self):
		return self.tick_interval.value
	def set_tick_interval(self, tick_interval_ms):
		self.tick_interval.value = tick_interval_ms

	def get_shared_data(self):
		return self.shared_data
	def set_event(self, event):
		with self.data_lock:
			self.shared_data['event'] = event
	def get_data_lock(self):
		return self.data_lock
	
	def spawn_bob(self, ask_number_of_bob):
		self.need_spawn_bob.value = True
		self.ask_number_of_bob.value = ask_number_of_bob
		while self.need_spawn_bob.value:
			pass

		

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

		with self.data_lock:
			self.shared_data['bobs'] = self.world_sim.get_bobs()
			self.shared_data['foods'] = self.world_sim.get_foods()
			self.shared_data['terrain'] = self.world_sim.get_terrain()
			self.shared_data['world_size'] = self.world_sim.get_size()
			self.shared_data['tick'] = self.world_sim.get_tick()
			self.shared_data['nb_bob'] = self.world_sim.get_nb_bob()
			self.shared_data['nb_food'] = self.world_sim.get_nb_food()
			self.shared_data['argDict'] = self.world_sim.get_argDict()
			self.shared_data['water_level'] = self.world_sim.get_water_level()
			self.shared_data['bob_population'] = self.world_sim.get_population_Bob()
			self.shared_data['food_population'] = self.world_sim.get_population_Food()

	def get_world_sim(self):
		self.get_world.value = True
		while self.get_world.value:
			pass
		return self.shared_data['world']
	
  
  
	def run(self):
	
		self.running.value = True
		while self.running.value:
			start = time.time()
			if self.get_world.value:
				self.shared_data['world'] = self.world_sim
				self.get_world.value = False
			if self.need_spawn_bob.value:
				self.world_sim.spawn_bob(self.ask_number_of_bob.value)
				self.need_spawn_bob.value = False

			if not self.paused.value:
				
				event = self.world_sim.update_tick()
				with self.data_lock:
					if 	event is not None:
						self.shared_data['event'] = event


				self.update_shared_data()
			elif self.option_shared_data[2]:
				self.world_sim.change_options(self.option_shared_data[0], self.option_shared_data[1])
				self.update_shared_data()
				self.option_shared_data[2] = False
				
			time.sleep(self.tick_interval.value/1000)
			with self.data_lock:
				self.shared_data['real_tick_time'] = time.time() - start
				self.shared_data['real_tick_time_data'].append(self.shared_data['real_tick_time'])
  
			
   
	def stop(self):
		if self.process is not None:
			self.running.value = False
			self.process.join()
   
   

   
   
	#faire un booléan . crée une variable qui va stocké l'objet et sera accesible des 2 côtés.	
   