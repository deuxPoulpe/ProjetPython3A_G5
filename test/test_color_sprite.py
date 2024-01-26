import pygame
import os
from time import sleep

# Initialisation de pygame
pygame.init()

# Réglages de base
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

# Chargement et mise à l'échelle de l'image de Bob
bob = pygame.image.load(os.path.join("assets", "Sprites/bob.png")).convert_alpha()
bob = pygame.transform.scale(bob, (500, 500))


def update_bob_color(x):
    # Assurez-vous que x est dans une plage raisonnable
    x = max(0, min(x, 100))

    # Calculer les composantes de couleur pour une transition plus douce
    red_amount = int((x - 40) * 2.55) if x > 40 else 10
    green_amount = int(x * 2.55) if x <= 50 else max(0, 127 - int(((x - 50) / 40) * 255))
    sub_green_amount = int((x - 80)/20 * 70) if x > 80 else 0
    blue_amount = int(x * 2.55)

    # Création des surfaces pour les opérations de couleur
    add_color_surface = pygame.Surface((500, 500))
    sub_color_surface = pygame.Surface((500, 500))

    # Ajuster les surfaces pour ADD et SUB
    add_color_surface.fill((red_amount, green_amount, 0))
    sub_color_surface.fill((0, sub_green_amount, blue_amount))
    print(f"red_amount: {red_amount}, green_amount: {green_amount}, sub_green_amount: {sub_green_amount}, blue_amount: {blue_amount}")

    # Appliquer les modifications de couleur
    bob_color_modified = bob.copy()
    bob_color_modified.blit(add_color_surface, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    bob_color_modified.blit(sub_color_surface, (0, 0), special_flags=pygame.BLEND_RGB_SUB)

    return bob_color_modified.convert_alpha()

# Boucle principale
x = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    x += 1
    sleep(0.1)
    # Mettre à jour la couleur de Bob en fonction de x
    bob_updated = update_bob_color(x)

    # Affichage
    screen.fill((0, 0, 0))
    screen.blit(bob_updated, (0, 0))
    pygame.display.update()
    clock.tick(60)
