import pickle
import math

class Bob:
    def __init__(self,poids):
        self.poids = poids
        self.taille = poids**(1/3)

        def getpoids(self):
            return self.poids

def save(self,filename,*args):
    with open(filename, 'wb') as output:
        for i in args:
            pickle.dump(i, output, pickle.HIGHEST_PROTOCOL)
            print("saved",i)
    output.close()


def load(file):
    with open(file, 'rb') as input:
        bob = pickle.load(input)
        print(bob.getpoids())
    input.close()

bob1= Bob(50)
save("lol","save.pkl",50,"lol",1,2,3,4)
# load("save.pkl")