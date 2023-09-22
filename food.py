# Classe représentant la nourriture
class Food:
	def __init__(self, x, y, world ,food_value = 200):
		self.x = x
		self.y = y
		self.world = world
		self.food_value = food_value

	def kill(self):
		self.world.grid[self.x][self.y].remove(self)
		self.world.foods.remove(self)

	def beEaten(self,value):
		if value <= self.food_value:
			self.food_value -= value
			if self.food_value <= 0:
				self.world.kill_food(self)
			return value
		else:
			self.world.kill_food(self)
			return self.food_value
	
	def getFoodValue(self):
		return self.food_value
	def getPos(self):
		return (self.x,self.y)
