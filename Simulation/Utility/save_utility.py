import pickle


def save(filename,*args):
    with open(filename, 'wb') as output:
        for i in args:
            pickle.dump(i, output, pickle.HIGHEST_PROTOCOL)
    output.close()

def load(file):
    with open(file, 'rb') as input:
        while True:
            try:
                yield pickle.load(input)
            except EOFError:
                break
    input.close()