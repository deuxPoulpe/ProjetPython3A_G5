import random
from food import Food
from Utility.time_function_utility import execute_function_after_it

class Bob:
	"""
	Classe représentant un personnage 'Bob' dans un monde simulé.

	Attributs:
		energy (int): Énergie actuelle de Bob.
		velocity (int): Vitesse de déplacement de Bob.
		mass (int): Masse de Bob.
		perception (int): Capacité de perception de Bob.
		memory_space (list): Espace mémoire de Bob.
		max_energy (int): Énergie maximale que Bob peut accumuler.
		position (tuple): Position actuelle de Bob dans le monde (x, y).
		en_fuite (bool): État indiquant si Bob est en fuite.
		world (World): Référence au monde dans lequel Bob évolue.
	"""


	def __init__(self, x, y, world, energy=100, velocity=1, mass=1, perception=0, memory_points = 0, max_energy=200 ,):
		"""
		Initialise une nouvelle instance de Bob.

		Paramètres:
			x (int): Position initiale en x de Bob.
			y (int): Position initiale en y de Bob.
			world (World): Référence au monde dans lequel Bob évolue.
			energy (int, optionnel): Énergie initiale de Bob. Par défaut à 100.
			velocity (int, optionnel): Vitesse initiale de Bob. Par défaut à 1.
			mass (int, optionnel): Masse initiale de Bob. Par défaut à 1.
			perception (int, optionnel): Perception initiale de Bob. Par défaut à 0.
			max_energy (int, optionnel): Énergie maximale de Bob. Par défaut à 200.

		"""

		self.energy = energy
		self.velocity = velocity
		self.mass = mass
		self.perception = perception
		self.memory_points = memory_points
		self.memory_space = []
		self.perception_list = []
		self.max_energy = max_energy
		self.position = (x, y)
		self.old_position = (x, y)
		self.en_fuite = False
		self.world = world
		self.case_to_move = 0
		self.velocity_buffer = 0
		self.tiles_visited = []
		self.dead = False

		self.name = self.random_name()
		
	def __str__(self):
		return f"Bob {self.position} {self.velocity} {self.mass} {self.energy} {self.perception} {self.memory_space} {self.en_fuite} {self.world} {self.max_energy}"

	def get_pos(self):
		return self.position
	def get_energy(self):
		return self.energy
	def get_mass(self):
		return self.mass
	def get_velocity(self):
		return self.velocity
	def get_perception(self):
		return self.perception
	def get_name (self) : 
		return self.name
	def get_old_pos(self):
		return self.old_position
	def get_memory_points(self):
		return self.memory_points
	def get_world(self):
		return self.world
	def is_dead(self):
		return self.dead
	
	def set_max_energy(self, max_energy):
		self.max_energy = max_energy


	
	def eat_food(self):
		"""
        Allows Bob to eat. Increases Bob's energy if food is available at his position.

        Returns:
            bool: True if Bob ate, False otherwise.
        """
		if self.get_pos() in self.world.get_foods().keys() and self.energy != self.max_energy:
			food = self.world.get_foods()[self.get_pos()]
			self.energy += food.be_eaten(min(food.get_value(), self.max_energy - self.energy))
			return True
		else:
			return False

	def loose_energy(self, mode,*arg):
		if mode == "move":
			self.energy -= self.mass * self.velocity**2
		elif mode == "stand":
			self.energy -= 0.5
		elif mode == "self_reproduce":
			self.energy -= 3*self.max_energy/4
			self.energy -= 0.5
		elif mode == "move_height":
			self.energy -= self.mass * self.velocity**2 + arg[0] * self.mass
	
	def random_name(self):
		
		
		vowels = 'aeiou'
		consones = 'bcdfghjklmnpqrstvwxyz'
		taille_name = random.randint(3, 8)
		name= ''
		
		for i in range (taille_name):
			if i%2 == 0 : 
				name += random.choice(consones)
			else : 
				name += random.choice(vowels)
			name = name.capitalize()
		return name
			
		


	def move(self):
		"""
        Moves Bob to a new random position.

        Returns:
            bool: True after Bob's movement.
        """
		old_x, old_y = self.position
		dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
		new_x, new_y = old_x + dx, old_y + dy

		if self.world.get_terrain() is not None:
			terrain = self.world.get_terrain().get_terrain()
			height_diff = terrain[new_x][new_y] - terrain[old_x][old_y]
		else:
			height_diff = 0

		if self.energy < self.mass * self.velocity**2 + height_diff * self.mass:
			self.loose_energy("stand")
		else:
			self.position = (max(0, min(new_x, self.world.get_size() - 1)),
							max(0, min(new_y, self.world.get_size() - 1)))
			self.world.move_bob(self, old_x, old_y)

			self.loose_energy("move_height", height_diff)

		return True

	def die(self):
		"""
        Handles Bob's death. Bob dies if his energy is less than or equal to 0.

        Returns:
            bool: True if Bob dies, False otherwise.
        """
		if self.energy <= 0:
			self.make_it_dead = 3
			self.dead = True
			return True
		else:
			return False

	def reproduce(self):
		"""
        Handles Bob's reproduction. Reproduction occurs if Bob's energy is sufficient.

        Returns:
            bool: True if reproduction occurs, False otherwise.
        """
		if self.energy >= self.max_energy:
			self.world.spawn_reproduce(self)
			self.loose_energy("self_reproduce")
			return True
		else:
			return False

	def update_tick(self):
		"""
        Updates Bob's state at each 'tick' or time interval. Manages various actions like dying, eating, reproducing, and moving.

        Returns:
            None
        """
		if self.dead:
			self.make_it_dead -= 1
			if self.make_it_dead <= 0:
				self.world.kill_bob(self)
			return None

		if self.die():
			return None
		#self.mutate_memory_points()
		self.velocity_manager()
		self.old_position = self.position
  
		while self.case_to_move > 0:

			if self.world.enable_function["reproduce"]:
				if (self.reproduce()):
					self.loose_energy("stand")
			elif self.world.enable_function["sexual_reproduction"]:
				if(self.sexual_reproduction()):
					self.loose_energy("stand")

			if self.world.enable_function["perception"]:
				self.bob_perception_v2()
			if self.world.enable_function["memory"]:
				self.memory_store()

			if self.world.enable_function["move_smart"]:
				if (self.move_smart()):
					self.case_to_move -= 1

			else:
				self.move()
				self.case_to_move -= 1
				
			self.world.enable_function["eat_bob"]: (self.eat_bob())
			self.eat_food()

			if self.die():
				return None

	
	
	def velocity_manager(self):

		self.case_to_move += abs(self.velocity)
		self.velocity_buffer += self.velocity-abs(self.velocity)
		if self.velocity_buffer > 0:
			self.velocity_buffer -= 1
			self.case_to_move += 1
	
	def eat_bob(self):
		"""
		Permet à Bob de manger un autre Bob. Retourne True si Bob a mangé un autre Bob, False sinon.
		"""
		mass_bob_list = []
		copy_bobs = self.world.get_bobs()[self.get_pos()].copy()
		if len(copy_bobs) > 1:
			copy_bobs.remove(self)
			mass_bob_list = [x.get_mass() for x in copy_bobs]
			bob=copy_bobs[mass_bob_list.index(min(mass_bob_list))]

			if (bob.get_mass()/self.get_mass())<(2/3):
				if (self.energy + bob.get_energy()/2*(1-bob.get_mass()/self.get_mass())) >= self.max_energy:
					self.energy = self.max_energy
				else:
					self.energy += bob.get_energy()/2*(1-bob.get_mass()/self.get_mass())
				self.world.kill_bob(bob)
				return True
		return False
	

	def bob_perception(self):
		"""
		Permet à Bob de percevoir son environnement. Retourne une liste d'objets autour de lui.
		"""
		
		#Génération d'une matrice carré de taille perception-1
		perception_list = []
		for x in range(self.get_pos()[0]-(self.perception-1),self.get_pos()[0]+self.perception):
			for y in range(self.get_pos()[1]-(self.perception-1),self.get_pos()[1]+self.perception):
				if (x,y) in self.world.get_foods():
					perception_list.append(self.world.get_foods()[(x,y)])
				if (x,y) in self.world.get_bobs():
					perception_list.append(self.world.get_bobs()[(x,y)])
		
		#Ajout des bords manquants
		y=self.get_pos()[1]
		for x in range(self.get_pos()[0]-(self.perception),self.get_pos()[0]+self.perception+1,2*self.perception):
			if (x,self.y) in self.world.get_foods():
					perception_list.append(self.world.get_foods()[(x,y)])
			if (x,self.y) in self.world.get_bobs():
					perception_list.append(self.world.get_bobs()[(x,y)])
		
		x=self.get_pos()[0]
		for y in range(self.get_pos()[1]-(self.perception),self.get_pos()[1]+self.perception+1,2*self.perception):
			if (x,self.y) in self.world.get_foods():
					perception_list.append(self.world.get_foods()[(x,y)])
			if (x,self.y) in self.world.get_bobs():
					perception_list.append(self.world.get_bobs()[(x,y)])

		return perception_list

	def bob_get_things_by_distance(self,distance):
			"""
			Permet à Bob de percevoir uniquement les objets à une distance précise de lui.
			"""
			deplacement=0
			x=self.get_pos()[0]-distance
			y=self.get_pos()[1]
			self.perception_list.append([])

			while x <= self.get_pos()[0]:

				if (x,y+deplacement) in self.world.get_foods():
					self.perception_list[distance].append(self.world.get_foods()[(x,y+deplacement)])
				if (x,y-deplacement) in self.world.get_bobs():
					for bob in self.world.get_bobs()[(x,y-deplacement)]:
						self.perception_list[distance].append(bob)

				x+=1
				deplacement+=1

			deplacement=0
			x=self.get_pos()[0]+distance

			while x > self.get_pos()[0]:
				if (x,y+deplacement) in self.world.get_foods():
					self.perception_list[distance].append(self.world.get_foods()[(x,y+deplacement)])
				if (x,y-deplacement) in self.world.get_bobs():
					for bob in self.world.get_bobs()[(x,y-deplacement)]:
						self.perception_list[distance].append(bob)

				x-=1
				deplacement+=1


	def bob_perception_v2(self):
		"""
		Permet à Bob de percevoir son environnement. Mets à jour l'attribut perception_list de bob étant une liste d'objets autour de lui trié par distance décroissante.
		"""
		self.perception_list = []
		distance = round(self.perception)

		for i in range(0, distance+1):
			self.bob_get_things_by_distance(i)

		tampon=[]
		for k in range(0, len(self.perception_list)): #Gestion des foods de même distance mais différentes values
			for j in self.perception_list[k].copy():
				if isinstance(j, Food):
					tampon.append(j)
					self.perception_list[k].remove(j)
				tampon = sorted(tampon, key=lambda food: food.value, reverse=True)
				self.perception_list[k].append(tampon)
				tampon=[]

		self.perception_list.sort(key=lambda x: isinstance(x, Food), reverse=True)

		#self.perception_list.sort(key=lambda x: x.mass isinstance(x,Bob))

		return True


	#deux bobs doivent etre dans la meme case pour se reproduire 
	def sexual_reproduction(self):
		for partener in self.world.get_bobs()[self.position]:
			if (self.position == partener.position and self.energy> 150 and partener.energy > 150 ):
				self.world.spawn_sexuelreproduction(self,partener)
				self.energy -=100
				partener.energy -=100
				return True
		return False 


	def memory_store(self):

		"""
		Fonction qui va stocker dans une file de 5 éléments les 5 dernières cases traversées par le bob
		"""
		def distance(self,food):
			return abs(food.get_pos()[0]-self.get_pos()[0])+abs(food.get_pos()[1]-self.get_pos()[1])
		
		for k in self.perception_list:
			for j in k:
				if isinstance(j, Food):
					if len(self.memory_space) > self.memory_points*2:
						self.memory_space.pop(0)
					self.memory_space.append(j)
					
		for e in self.memory_space:
			if distance(self,e) < self.perception:
				self.memory_space.remove(e)
				self.memory_points -= 1

		self.memory_space.sort(key=lambda food: food.value, reverse=True)
		return True
	

	def move_smart(self): #fonction qui permet à bob de se déplacer de façon intelligente d'une seule case !
		for j in self.perception_list:
			for k in j:
				if isinstance(k,Bob):
					if (self.get_mass()/k.get_mass())<(2/3):
						self.move_dest(self.case_ou_aller(k,"fuir"))
						return True
					
					if (self.get_mass()/k.get_mass())>=(3/2):
						self.move_dest(self.case_ou_aller(k,"aller"))
						return True

				elif isinstance(k,Food):
					self.move_dest(self.case_ou_aller(k,"aller"))
					return True
				
		for i in self.memory_space:
			if isinstance(i,Food):
				self.move_dest(self.case_ou_aller(i,"aller"))
				self.memory_points -= 1
				return True
		



		self.move()
		return True
			
	
					
	def move_dest(self,dest):
		"""
        Teleport Bob to a destination

        Returns:
            bool: True after Bob's movement.
        """
		old_x, old_y = self.position
		new_x, new_y = dest
		if self.world.get_terrain() is not None:
			terrain = self.world.get_terrain().get_terrain()
			height_diff = terrain[new_x][new_y] - terrain[old_x][old_y]
		else:
			height_diff = 0

		if self.energy < self.mass * self.velocity**2 + height_diff * self.mass:
			self.loose_energy("stand")

		else:
			self.position = (max(0, min(new_x, self.world.get_size() - 1)),
							max(0, min(new_y, self.world.get_size() - 1)))
			self.world.move_bob(self, old_x, old_y)
			self.loose_energy("move_height", height_diff)
			return True


	def case_ou_aller(self, bob , mode):
		"""
		Fonction qui renvoie la case où le bob doit fuir pour éviter de se faire manger par un autre bob.
		"""

		if mode == "fuir":
			d = 1
		elif mode == "aller":
			d = -1

		x1 = self.get_pos()[0] #position en abcisse du bob qui doit fuir
		y1 = self.get_pos()[1] #position en ordonnée du bob qui doit fuir

		x = bob.get_pos()[0]
		y = bob.get_pos()[1]
		dx = self.get_pos()[0] - x
		dy = self.get_pos()[1] - y


		if dx > 0 and dy>0:
			randint = random.randint(0,1)
			if randint == 0:
				x1 += d
			else:
				y1 += d
		elif dx > 0 and dy<0:
			randint = random.randint(0,1)
			if randint == 0:
				x1 += d
			else:
				y1 -= d
		elif dx < 0 and dy>0:
			randint = random.randint(0,1)
			if randint == 0:
				x1 -= d
			else:
				y1 += d
		elif dx < 0 and dy<0:
			randint = random.randint(0,1)
			if randint == 0:
				x1 -= d
			else:
				y1 -= d
		
		elif dx == 0 and dy>0 and mode=="fuir":
			randint = random.randint(0,2)
			if randint == 0:
				x1 += d
			elif randint == 1:
				x1 -= d
			else:
				y1 += d
		elif dx == 0 and dy<0 and mode=="fuir":
			randint = random.randint(0,2)
			if randint == 0:
				x1 += d
			elif randint == 1:
				x1 -= d
			else:
				y1 -= d
		elif dx > 0 and dy==0 and mode=="fuir":
			randint = random.randint(0,2)
			if randint == 0:
				y1 += d
			elif randint == 1:
				y1 -= d
			else:
				x1 += d
		elif dx < 0 and dy==0 and mode=="fuir":
			randint = random.randint(0,2)
			if randint == 0:
				y1 += d
			elif randint == 1:
				y1 -= d
			else:
				x1 -= d
		elif dx == 0 and dy==0:
			pass

		elif dx == 0 and dy>0 and mode=="aller":
			y1+=d
		elif dx == 0 and dy<0 and mode=="aller":
			y1 -= d
		elif dx > 0 and dy==0 and mode=="aller":
				x1 += d
		elif dx < 0 and dy==0 and mode=="aller":
				x1 -= d

		return (x1,y1)
	
