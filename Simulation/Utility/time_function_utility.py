


def execute_function_during_it(function, *arg, nb_iter = 0):
	"""
	Executes a function during a given nb_iter.
	Args:
		function (function): The function to execute.
		nb_iter (int): The number of iteration to execute the function.
	"""
	def generator():
		for _ in range(nb_iter):
			yield function(*arg)
	
	return generator()

def execute_function_after_it(function, *arg, nb_iter = 0):
	"""
	Executes a function after a given nb_iter.
	Args:
		function (function): The function to execute.
		nb_iter (int): The number of iteration to execute the function.
	"""
	def generator():
		for _ in range(nb_iter):
			yield None
		yield function(*arg)
	
	return generator()
