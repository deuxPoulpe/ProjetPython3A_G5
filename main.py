
from world import World
from graphique import Affichage_graphique
from main_menu import Menu
import multiprocessing
import pygame

from tiles import Tile

def run_simulation(world_size, initial_bob_count, tick_interval):
	world = World(world_size)
	world.spawn("bob", initial_bob_count)
	graphique = Affichage_graphique(world)
	graphique.run(tick_interval)
	graphique.graph()
     

def choose_simulation():
	multi_simulation = Menu().main_menu()

	if multi_simulation:
		pygame.quit()
		num_simulations = 4

		# Créez une liste de paramètres pour chaque simulation
		simulation_params = [
			(50, 50, 1),  # world_size, initial_bob_count, tick_interval
			(50, 50, 1),
			(50, 50, 1),
			(50, 50, 1)
			
		]
		

		# Utilisez multiprocessing pour exécuter les simulations en parallèle
		with multiprocessing.Pool(num_simulations) as pool:
			pool.starmap(run_simulation, simulation_params)
	else:
		pygame.quit()
		run_simulation(50, 50, 1)



if __name__ == "__main__":


	# choose_simulation()

	run_simulation(50, 20, 100)


	
	


	
	

	
	
