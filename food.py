
class Food:
    def __init__(self, x, y, world, type="banane",value = 100):
        self.value = value
        self.pos = (x,y)
        self.world = world
        self.type = type
        pass




    #getters
    def get_value(self):
        return self.value
    def get_pos(self):
        return self.pos
    

    #methods

    def be_eaten(self):
        pass