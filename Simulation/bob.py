import random
import food

from queue import *

class Bob:
	"""
    Class representing a character 'Bob' in a simulated world.

    Attributes:
        energy (int): Bob's current energy.
        velocity (int): Bob's movement speed.
        mass (int): Bob's mass.
        perception (int): Bob's perception ability.
        memory_space (list): Bob's memory space.
        max_energy (int): The maximum energy Bob can accumulate.
        position (tuple): Bob's current position in the world (x, y).
        en_fuite (bool): Indicates whether Bob is fleeing.
        world (World): Reference to the world in which Bob exists.
    """


	def __init__(self, x, y, world, energy=100, velocity=1, mass=1, perception=0, memory_points = 0, memory_space = Queue(5), max_energy=200):
		"""
        Initializes a new instance of Bob.

        Parameters:
            x (int): Initial position of Bob in the x-axis.
            y (int): Initial position of Bob in the y-axis.
            world (World): Reference to the world in which Bob exists.
            energy (int, optional): Initial energy of Bob. Default is 100.
            velocity (int, optional): Initial velocity of Bob. Default is 1.
            mass (int, optional): Initial mass of Bob. Default is 1.
            perception (int, optional): Initial perception of Bob. Default is 0.
            max_energy (int, optional): Maximum energy of Bob. Default is 200.
        """

		self.energy = energy
		self.velocity = velocity
		self.mass = mass
		self.perception = perception
		self.memory_points = memory_points
		self.memory_space = memory_space
		self.max_energy = max_energy
		self.position = (x, y)
		self.en_fuite = False
		self.world = world
		self.color = random.choice("red", "green", "blue")

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

	def loose_energy(self, mode):
		if mode == "move":
			self.energy -= self.mass * self.velocity**2
		elif mode == "stand":
			self.energy -= 0.5
		elif mode == "sexual_reproduction":
			self.energy -= 100
			
	

	def move(self):
		"""
        Moves Bob to a new random position.

        Returns:
            bool: True after Bob's movement.
        """
		old_x, old_y = self.position
		dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
		new_x, new_y = old_x + dx, old_y + dy
		self.position = (max(0, min(new_x, self.world.get_size() - 1)),
						max(0, min(new_y, self.world.get_size() - 1)))
		self.world.move_bob(self, old_x, old_y)
		self.loose_energy("move")

	

		return True

	def die(self):
		"""
        Handles Bob's death. Bob dies if his energy is less than or equal to 0.

        Returns:
            bool: True if Bob dies, False otherwise.
        """
		if self.energy <= 0:
			self.world.kill_bob(self)
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
			self.energy = 3 * self.energy // 4
			self.world.spawn_reproduce(self)
			return True
		else:
			return False

	def update_tick(self):
		"""
        Updates Bob's state at each 'tick' or time interval. Manages various actions like dying, eating, reproducing, and moving.

        Returns:
            None
   
		Incluant les évènements :
			bob_perception_v2(self)
			move_smart(self)
			memory_store(self)
			mutate_memory_points(self)
			eat_bob()
			Implémenter le choix en entre sexual_reproduction(self) et reproduce(self) 


        """
	

		if self.die():
			return None
		
		self.mutate_memory_points()

		if self.world.enable_function["perception"] : self.bob_perception_v2()

		if self.world.enable_function["memory"] : self.memory_store()

		if self.world.enable_function["reproduce"]:
			if (self.reproduce()) :
				self.loose_energy("stand")
				return None

		if self.word.enable_function["sexual_reproduction"]:
			if (self.sexual_reproduction()):
				self.loose_energy("stand")
				return None
			
		if self.world.enable_function["eat_bob"] and (self.eat_bob()):
			self.loose_energy("stand")
			return None

		if(self.eat_food()) :
			self.loose_energy("stand")
			return None

		if self.world.enable_function["move_smart"] and (self.move_smart()):
			self.loose_energy("move")
			return None

		






			



def velocity_manager(self):

		self.case_to_move += abs(self.velocity)
		self.velocity_buffer += self.velocity-abs(self.velocity)
		if self.velocity_buffer > 0:
			self.velocity_buffer -= 1
			case_to_move += 1
	
def eat_bob(self):
		copy_bobs = self.world.get_bobs()[self.get_pos()].remove(self).copy()
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

def bob_perception_v2(self):
		"""
		Permet à Bob de percevoir son environnement. Retourne une liste d'objets autour de lui trié par distance décroissante.
		"""
		perception_list = []
		
		def bob_get_things_by_distance(self,distance):
			"""
			Permet à Bob de percevoir uniquement les objets à une distance précise de lui.
			"""
			deplacement=0
			x=self.get_pos()[0]-distance
			y=self.get_pos()[1]

			while x <= self.get_pos()[0]:

				if (x,y+deplacement) in self.world.get_foods():
						perception_list.append(self.world.get_foods()[(x,y+deplacement)])
				if (x,y-deplacement) in self.world.get_bobs():
						perception_list.append(self.world.get_bobs()[(x,y-deplacement)])

				x-=1
				deplacement+=1

			deplacement=0
			x=self.get_pos()[0]+distance

			while x > self.get_pos()[0]:

				if (x,y+deplacement) in self.world.get_foods():
						perception_list.append(self.world.get_foods()[(x,y+deplacement)])
				if (x,y-deplacement) in self.world.get_bobs():
						perception_list.append(self.world.get_bobs()[(x,y-deplacement)])

				x-=1
				deplacement+=1

		
		distance = self.perception
		while distance > 0:
			self.bob_get_things_by_distance(distance)
			distance-=1

		return perception_list



	#deux bobs doivent etre dans la meme case pour se reproduire 
def sexual_reproduction(self):
		for partener in self.world.get_bobs[self.position]:
			if (self.position == partener.position and self.energy> 150 and partener.energy > 150 ):
				
				self.loose_energy("sexual_reproduction")

				self.world.spawn_reproduce(partener, self) # Modifier fonction spawn_reproduce dans World
				return True
			
		return False 



def memory_store(self):

		"""
		Fonction qui va stocké dans une file de 5 éléments les 5 dernières cases traversées par le bob
		"""
		
		for k in self.perception_list:
			for j in k:
				if isinstance(j, food.Food):
					self.memory_space[0].append(j)
				elif isinstance(j, Bob) and (self.get_mass()/j.get_mass())<(2/3):
					self.memory



def mutate_memory_points(self):
		
		"""
		Fonction qui modifie de façon aléatoire les points de mémoire du bob. Ce qui lui permet de sauvegarder plus ou moins d'objet dans sa liste de perception.

		"""

		if (random.randint(0, 1) > self.word.mutation) :
			
			values = [-1, 0 , 1]

			mutation = random.choice(values)

			self.memory_points += mutation

		return self.memory_points

def move_smart(self): #fonction qui permet à bob de se déplacer de façon intelligente d'une seule case !
		for i in self.memory_space:
			for j in i:
				for k in j:

					if isinstance(k,Bob):
						if (self.get_mass()/k.get_mass())<(2/3):
							self.move_dest(self.case_ou_aller(k,"fuir"))
							return True
						
						if (self.get_mass()/k.get_mass())>=(3/2):
							self.move_dest(self.case_ou_aller(k,"aller"))
							return True

					elif isinstance(k,food.Food):
						self.move(self.case_ou_aller(k,"aller"))
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
		self.position = (max(0, min(new_x, self.world.get_size() - 1)),
						max(0, min(new_y, self.world.get_size() - 1)))
		self.world.move_bob(self, old_x, old_y)
		self.loose_energy("move")


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



		