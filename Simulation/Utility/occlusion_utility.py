import pygame


def tile_to_array(tile_image):
    """
    Convertit une image de tuile Pygame en un tableau utilisé pour le calcul de l'occlusion.

    :param tile_image: Image de tuile Pygame.
    :return: Tableau 2D où chaque valeur représente la transparence ou l'opacité de la tuile.
    """
    
    tile_array = pygame.surfarray.array_alpha(tile_image)

    final_array = [[0 for _ in range(48)] for _ in range(32)]

    for i in range(len(tile_array)):
        for j in range(len(tile_array)):
            if tile_array[i][j] != 0:
                for k in range(len(final_array[i])-j):
                    final_array[i][k+j] = 255
                break

    return final_array



def hide_behind_terrain_image(bob_sprite, tile_array, close_tile_height):
    """
    Modifie un sprite pour qu'il apparaisse derrière un terrain, en fonction d'un tableau de tuiles.

    :param bob_sprite: Sprite Pygame à modifier.
    :param tile_array: Tableau de tuiles indiquant l'occlusion.
    :param close_tile_height: Hauteurs des tuiles proches pour ajuster l'occlusion.
    :return: Sprite Pygame modifié avec les parties occluses rendues transparentes.
    """
    bob_array = pygame.surfarray.array3d(bob_sprite.get_image())
    width, height, _ = bob_array.shape

    base_offset_x = int(8 *(1 - bob_sprite.get_size()))
    base_offset_y = int(16 *(1 - bob_sprite.get_size())) - 7

    offsets = [
        (24 + base_offset_x, base_offset_y + 9 * close_tile_height[1]),  # Left
        (- 8 + base_offset_x, base_offset_y + 9 * close_tile_height[0]),  # Right
        (8 + base_offset_x, base_offset_y - 10 + 9 * close_tile_height[2])  # Bottom
    ]

    for i in range(width):
        for j in range(height):
            for offset_x, offset_y in offsets:
                x, y = i + offset_x, j + offset_y
                if 0 <= x < len(tile_array) and 0 <= y < len(tile_array[x]) and tile_array[x][y] != 0:
                    bob_array[i,j] = 0

    return pygame.surfarray.make_surface(bob_array)

