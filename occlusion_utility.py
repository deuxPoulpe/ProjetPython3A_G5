import pygame
import os
from terrain import Terrain
from sprite import Sprite_bob
import numpy as np
import time


terrain = Terrain(100, {
		"generate_river" : True,
		"number_of_river" : 2,
		"generate_lake" : True,
		"number_of_lake" : 1,
		"size_of_lake" : 20,
		"max_height" : 10,
		})


def afficher_matrice(matrice):
	try:
		if len(matrice.shape) == 3:
			matrice = matrice[:,:,0]
	except:
		pass
	for i in range(len(matrice)):
		for j in range(len(matrice[i])):
			if matrice[i][j] != 0:
				print("#",end=" ")
			else:
				print(".",end=" ")
		print()
	print()

def tile_to_array(tile_image):
	tile_array = pygame.surfarray.array_alpha(tile_image)

	final_array = [[0 for _ in range(48)] for _ in range(32)]

	for i in range(len(tile_array)):
		for j in range(len(tile_array)):
			if tile_array[i][j] != 0:
				for k in range(len(final_array[i])-j):
					final_array[i][k+j] = 255
				break

	return final_array


def hide_behind_terrain(bob_sprite, tile_array, close_tile_height):
	
	bob_array = pygame.surfarray.array3d(bob_sprite.get_image())
	
	width, height, _ = bob_array.shape

	base_offset_x = int(8 *(1 - bob_sprite.get_size()))
	base_offset_y = int(16 *(1 - bob_sprite.get_size())) - 7

	offset_x_left = 24 + base_offset_x
	offset_x_right = - 8 + base_offset_x
	offset_x_bot = 8 + base_offset_x

	offset_y_left = base_offset_y + 9 * close_tile_height[1]
	offset_y_right = base_offset_y + 9 * close_tile_height[0]
	offset_y_bot = base_offset_y - 10 + 9 * close_tile_height[2]

	for i in range(width):
		for j in range(height):
			x = i + offset_x_right
			y = j + offset_y_right
			if x >= 0 and y >= 0:
				try:
					if tile_array[x][y] != 0:
						bob_array[i,j] = 0
				except:
					pass
			x = i + offset_x_left
			y = j + offset_y_left
			if x >= 0 and y >= 0:
				try:
					if tile_array[x][y] != 0:
						bob_array[i,j] = 0
				except:
					pass

			x = i + offset_x_bot
			y = j + offset_y_bot
			if x >= 0 and y >= 0:
				try:
					if tile_array[x][y] != 0:
						bob_array[i,j] = 0
				except:
					pass


	bob_sprite.set_image(pygame.surfarray.make_surface(bob_array))


def show_time(f):
	start_time = time.time()
	f()
	end_time = time.time()
	print(f"Le temps d'exécution est de {end_time - start_time} secondes.")



def test_loop():

	pygame.init()
	screen = pygame.display.set_mode((800,600), pygame.RESIZABLE)

	bob_image = pygame.image.load(os.path.join("assets","bob.png")).convert()
	tile = pygame.image.load(os.path.join("assets/tiles","tile_028.png"))
	bob_sprite = Sprite_bob(0,0, bob_image, 1)
	tile_array = tile_to_array(tile)



	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		screen.fill((0,0,0))
		hide_behind_terrain(bob_sprite, tile_array, [2,2,2])
		screen.blit(pygame.transform.scale_by(bob_sprite.get_image(),10), (200,150))

		pygame.display.flip()


