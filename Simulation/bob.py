import random


class Bob:
	def __init__(self, x, y, world ,energy = 100, velocity = 1, mass = 1, perception = 0, max_energy = 200,):
		self.energy = energy
		self.velocity = velocity
		self.mass = mass
		self.perception = perception
		self.memory_space = []
		self.max_energy = max_energy
		self.position = (x,y)
		self.en_fuite = False
		self.world = world

	#getters

	def get_pos(self):
		return self.position
	def get_energy(self):
		return self.energy
	def get_mass(self):
		return self.mass


	def __str__(self):
		return f"Bob {self.position} {self.velocity} {self.mass} {self.energy} {self.perception} {self.memory_space} {self.en_fuite} {self.world} {self.max_energy}"
	

	

	#fonction qui permet aux bobs de manger
	def eat(self): #food est un objet de la classe food
		if self.get_pos() in self.world.get_foods() and self.energy != self.max_energy:
			food = max(self.world.get_foods()[self.get_pos()], key = lambda x : x.get_value())
			self.energy += food.be_eaten(min(food.get_value(), self.max_energy - self.energy))
			return True
		else:
			return False
		




	def move(self): #fonction de déplacement du bob dorra
		
		old_x = self.position[0] #l'ancienne valeur de x
		old_y = self.position[1] #l'ancienne valeur de y 
		dx = random.randint(-1,1) 
		dy = random.randint(-1,1) 
		 #update position 
		new_x = self.position[0] + dx
		new_y = self.position[1] + dy
		#garantir que bob reste dans la fenêtre du jeu 
		self.position = (max(0, min(new_x,self.world.get_size()-1)),
				   		max(0, min(new_y,self.world.get_size()-1)))
		self.world.move_bob(self,old_x,old_y)

		self.energy -= 1

		return True
	
		
	def die(self):
		if self.energy <= 0:
			self.world.kill_bob(self)
			return True
		else:
			return False
		

	def reproduce(self):
		if self.energy >= self.max_energy:
			self.energy = 3*self.energy/4
			self.world.spawn_reproduce(self)
			return True
		else:
			return False
		

	
	def update_tick(self):

		actions = [self.die,self.eat,self.reproduce,self.move]

		#parcours des actions
		for action in actions:
			#si l'action est effectuée, on sort de la boucle
			if action():
				break