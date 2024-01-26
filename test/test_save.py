import pickle

class Bob:
    def __init__(self,poids):
        self.poids = poids
        self.taille = poids**(1/3)

    def getpoids(self):
        return self.poids

def save(filename,*args):
    with open(filename, 'wb') as output:
        for i in args:
            pickle.dump(i, output, pickle.HIGHEST_PROTOCOL)
            print("saved",i)
    output.close()


