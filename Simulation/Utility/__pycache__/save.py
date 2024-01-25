import pickle
def save(self,filename,*args):
		"""
        Saves the current state of the world to a file.

        Parameters:
            filename (str): Name of the file to save the state to.
            *args: Additional arguments or objects to save.
        """
		with open(filename, 'wb') as output:
			for i in args:
				pickle.dump(i, output, pickle.HIGHEST_PROTOCOL)
				print("saved",i)
		output.close()
		
def load_save(self, filename):
    """
    Load a save from a file.

    Parameters: name of the file to load the save from.
    """
    with open(filename, 'rb') as input_file:
        loaded_objects = []
        while True:
            try:
                loaded_objects.append(pickle.load(input_file))
            except EOFError:
                break
    return tuple(loaded_objects)