
class Food:
	def __init__(self, x, y, world, type="banane",value = 100):
		self.value = value
		self.pos = (x,y)
		self.world = world
		self.type = type


	#getters
	def get_value(self):
		return self.value
	def get_pos(self):
		return self.pos
	

	#methods

	def be_eaten(self,value):
		if self.value - value <= 0:
			self.world.kill_food(self)
			return self.value
		else:
			self.value -= value
			return value
		