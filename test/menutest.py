import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 800, 600

# Création de la fenêtre Pygame
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("PROJET_PYTHON_2024_G5")

# Constantes de couleur
BLEU = (0, 0, 250)
NOIR = (0, 0, 0)
ROUGE = (250, 0, 0)
VERT = (0, 250, 0)
ROSE = (255, 192, 203)

# Initialisation de la police
policeChoisie = "GamepauseddemoRegular-RpmY6.otf"
police = pygame.font.Font(policeChoisie, 36)

# Fonction pour afficher du texte sur la fenêtre
def afficher_texte(texte, x, y, taille=36):
    fonte_texte = pygame.font.Font(policeChoisie, taille)
    surface_texte = fonte_texte.render(texte, True, NOIR)
    rect_texte = surface_texte.get_rect(center=(x, y))
    fenetre.blit(surface_texte, rect_texte)

# Fonction du menu principal
def menu_principal():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_souris, y_souris = pygame.mouse.get_pos()
                gestion_clic_menu(x_souris, y_souris)

        afficher_image_de_fond("fond.jpeg")

        afficher_texte("Game Of Life", LARGEUR // 2, 100, 56)
        dessiner_bouton(ROSE, 300, 200, 200, 70, "Start")
        dessiner_bouton(ROSE, 300, 300, 200, 70, "Options")
        dessiner_bouton(ROSE, 300, 400, 200, 70, "Quitter")

        pygame.display.update()

# Classe pour une tuile
class Tuile():
    def __init__(self, x, y):
        self.image = pygame.image.load("fond.jpeg")
        self.rect = self.image.get_rect(topleft=(x, y))

# Fonction pour convertir des coordonnées isométriques
def coordonnees_iso(x, y):
    return x - y, (x + y) / 2

# Fonction pour mettre à jour la fenêtre
def mettre_a_jour_fenetre():
    afficher_image_de_fond("fond.jpeg")

# Fonction pour afficher des tuiles
def afficher_tuiles(valeur):
    largeur_ecran, hauteur_ecran = fenetre.get_size()
    for y in range(-valeur // 2, valeur // 2):
        for x in range(-valeur // 2, valeur // 2):
            nouvelle_tuile = Tuile(largeur_ecran // 4 + hauteur_ecran // 2 + x * TAILLE_TUILE,
                                   hauteur_ecran // 2 - largeur_ecran // 4 + y * TAILLE_TUILE)
            fenetre.blit(nouvelle_tuile.image, coordonnees_iso(nouvelle_tuile.rect.x, nouvelle_tuile.rect.y))

# Fonction pour l'interface de jeu
def interface_jeu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        fait = False
        mettre_a_jour_fenetre()
        afficher_tuiles(20)
        pygame.display.update()

# Champs de texte
champs_texte = [pygame.Rect(200, 50 + i * 70, 300, 50) for i in range(8)]

# Couleurs des champs
couleur_active = pygame.Color('dodgerblue2')
couleur_inactive = pygame.Color('lightskyblue3')
couleur = couleur_inactive
textes_champs = [''] * 8
champ_actif = policeChoisie


# Fonction pour afficher un formulaire
def afficher_formulaire(variables):
    pygame.init()
    global couleur
    global champ_actif

    afficher_image_de_fond("fond.jpeg")

    for i, (variable, champ) in enumerate(zip(variables, champs_texte)):
        # Affichage de la variable
        surface_variable = police.render(variable, True, NOIR)
        fenetre.blit(surface_variable, (50, 50 + i * 70))

        # Champ de saisie
        pygame.draw.rect(fenetre, couleur, champ, 2)
        surface_texte = police.render(textes_champs[i], True, NOIR)
        largeur_texte = max(200, surface_texte.get_width() + 10)
        champ.w = largeur_texte
        fenetre.blit(surface_texte, (champ.x + 5, champ.y + 5))
        # Bouton de retour
        
        pygame.draw.rect(fenetre, ROSE, (600, 500, 120, 50))
        afficher_texte("Retour", 660, 525)

    pygame.display.flip()

    # Liste de variables
    variables = ['G.S.Larg', 'G.S.long', 'Energy', 'Velocity', 'Min energy', 'The mass', 'score Bp', 'memory']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, champ in enumerate(champs_texte):
                    if champ.collidepoint(event.pos):
                        champ_actif = i
                        couleur = couleur_active
                    else:
                        couleur = couleur_inactive
            if event.type == pygame.KEYDOWN:
                if champ_actif is not None:
                    if event.key == pygame.K_RETURN:
                        print("Variable {}: {}".format(champ_actif + 1, textes_champs[champ_actif]))
                        textes_champs[champ_actif] = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textes_champs[champ_actif] = textes_champs[champ_actif][:-1]
                    else:
                        textes_champs[champ_actif] += event.unicode

            afficher_formulaire(variables)

# Fonction pour gérer les clics dans le menu
def gestion_clic_menu(x, y):
    if 300 <= x <= 500:
        if 200 <= y <= 250:
            print("Démarrer")
            interface_jeu()
        elif 300 <= y <= 350:
            print("Options")
            variables = ['Energy', 'Velocity', 'Min energy', 'The mass', 'score Bp', 'memory',]
            afficher_formulaire(variables)
        elif 400 <= y <= 450:
            pygame.quit()
            sys.exit()

# Fonction pour dessiner un bouton sur la fenêtre
def dessiner_bouton(couleur, x, y, largeur, hauteur, texte):
    pygame.draw.ellipse(fenetre, couleur, (x, y, largeur, hauteur))
    afficher_texte(texte, x + largeur // 2, y + hauteur // 2)

# Fonction pour afficher une image de fond sur la fenêtre
def afficher_image_de_fond(chemin_image):
    arriere_plan = pygame.image.load(chemin_image)
    arriere_plan = pygame.transform.scale(arriere_plan, (LARGEUR, HAUTEUR))
    fenetre.blit(arriere_plan, (0, 0))

# Variables globales
TAILLE_TUILE = 16
fenetre_active = False
champ_texte_actif = policeChoisie


# Boucle principale
if __name__ == "__main__":
    menu_principal()
