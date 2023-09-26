import os

class World:
	def __init__(self,argDict):
		self.argDict = argDict
		self.bobs = []
		self.foods = []
		self.spriteBob = ""
		self.spriteFood = ""
		self.tick = 0
		self.population_bob = []
		self.population_food = []

		assert all([type(argDict["size"]) == int ,
		type(argDict["nbFood"]) == int ,
		type(argDict["dayTick"]) == int
		])
	#exemple argDict:

	# argDict = {
	# 	"size" : size (100),
	# 	"nbFood" : nbFood (200),
	# 	"dayTick" : dayTick (100),
	# }


	#getters
	def getSize(self):
		return 
	def getPopulationBob(self):
		return self.population_bob
	def getPopulationFood(self):
		return self.population_food
	def getTick(self):
		return self.tick
	def getArgDict(self):
		return self.argDict

	#setter
	def setArgDict(self,newArgDict):
		self.argDict = newArgDict
	