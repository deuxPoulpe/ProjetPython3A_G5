import pygame
import sys
from display import Display
from api import Api
from world import World

class Menu:
    def __init__(self):
        pygame.init()

        # Dimensions de la fenêtre
        self.LARGEUR, self.HAUTEUR = 800, 600

        # Création de la fenêtre Pygame
        self.fenetre = pygame.display.set_mode((self.LARGEUR, self.HAUTEUR))
        pygame.display.set_caption("PROJET_PYTHON_2024_G5")

        # Constantes de couleur
        self.NOIR = (0, 0, 0)
        self.ROSE = (255, 192, 203)

       # Initialisation de la police
        self.policeChoisie = "GamepauseddemoRegular-RpmY6.otf"
        self.police = pygame.font.Font(self.policeChoisie, 36)
        self.policeme = pygame.font.Font(None, 24)        

        # Champs de texte
        self.champs_texte = [pygame.Rect(350, 50 + i * 50, 300, 30) for i in range(10)]

        # Couleurs des champs
        self.couleur_active = pygame.Color('dodgerblue2')
        self.couleur_inactive = pygame.Color('lightskyblue3')
        self.couleur = self.couleur_inactive
        self.textes_champs = [''] * 10
        self.champ_actif = None

        # Dictionnaire pour stocker les valeurs des variables
        self.valeurs_variables = {}

    def afficher_texte(self, texte, x, y, taille=36):
        fonte_texte = pygame.font.Font(self.policeChoisie, taille)
        surface_texte = fonte_texte.render(texte, True, self.NOIR)
        rect_texte = surface_texte.get_rect(center=(x, y))
        self.fenetre.blit(surface_texte, rect_texte)

    def afficher_image_de_fond(self, chemin_image):
        arriere_plan = pygame.image.load(chemin_image)
        arriere_plan = pygame.transform.scale(arriere_plan, (self.LARGEUR, self.HAUTEUR))
        self.fenetre.blit(arriere_plan, (0, 0))

    def dessiner_bouton(self, couleur, x, y, largeur, hauteur, texte):
        pygame.draw.ellipse(self.fenetre, couleur, (x, y, largeur, hauteur))
        self.afficher_texte(texte, x + largeur // 2, y + hauteur // 2)

    def afficher_formulaire(self, variables):
        pygame.init()
        self.afficher_image_de_fond("fond.jpeg")

        for i, (variable, champ) in enumerate(zip(variables, self.champs_texte)):
            # Affichage de la variable
            surface_variable = self.police.render(variable, True, self.NOIR)
            self.fenetre.blit(surface_variable, (50, 50 + i * 50))

            # Champ de saisie
            pygame.draw.rect(self.fenetre, self.couleur, champ, 2)
            surface_texte = self.policeme.render(self.textes_champs[i], True, self.NOIR)
            largeur_texte = max(200, surface_texte.get_width() + 10)
            champ.w = largeur_texte
            self.fenetre.blit(surface_texte, (champ.x + 5, champ.y + 5))

            # Bouton de retour
            self.dessiner_bouton(self.ROSE, 600, 505, 150, 50, "Retour")

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, champ in enumerate(self.champs_texte):
                        if champ.collidepoint(event.pos):
                            self.champ_actif = i
                            self.couleur = self.couleur_active
                        else:
                            self.couleur = self.couleur_inactive
                    if 600 <= event.pos[0] <= 700 and 500 <= event.pos[1] <= 530:
                        return True
                        # Attribuer les valeurs saisies aux variables
                        for i, variable in enumerate(variables):
                            self.valeurs_variables[variable] = int(self.textes_champs[i])
                    

                if event.type == pygame.KEYDOWN:
                    if self.champ_actif is not None:
                        if event.key == pygame.K_RETURN:
                            try:
                                value = int(self.textes_champs[self.champ_actif])  # Convertir en entier
                                print("{}: {}".format(variables[self.champ_actif], value))
                            except ValueError:
                                print("Veuillez entrer une valeur numérique.")

                            self.textes_champs[self.champ_actif] = ''  # Réinitialiser le champ de texte
                        elif event.key == pygame.K_BACKSPACE:
                            self.textes_champs[self.champ_actif] = self.textes_champs[self.champ_actif][:-1]
                        else:
                            self.textes_champs[self.champ_actif] += event.unicode

                if self.afficher_formulaire(variables):
                    print("Retour au menu principal")
                    self.menu_principal()

    def gestion_clic_menu(self, x, y):
        bouton_demarrer = pygame.Rect(300, 200, 200, 50)
        bouton_options = pygame.Rect(300, 300, 200, 50)
        bouton_quitter = pygame.Rect(300, 400, 200, 50)
        boutton_Retour = pygame.Rect(600, 500, 100, 30)  # Ajuster la taille du bouton
        if bouton_demarrer.collidepoint(x, y):
            pygame.quit()
            terrain_config = {
            	"generate_river" : True,
            	"number_of_river" : 1,
            	"generate_lake" : False,
            	"number_of_lake" : 1,
            	"size_of_lake" : 20,
            	"max_height" : 10,
            	"seed" : 6432,
            	}

            world = World({
            	"size" : 50,
            	"nbFood" : 50,
            	"dayTick" : 100,
            	"Food_energy" : 100,
            	"custom_terrain" : True,
            	}, terrain_config)
            world.spawn_bob(50)
            api = Api(world, 500)
            display = Display(api)
            display.main_loop()
        elif bouton_options.collidepoint(x, y):
            print("Options")
            variables = ['number_of_river', 'number_of_lake', 'size_of_lake', 'max_height', 'nbFood', 'dayTick', 'Food_energy', 'generate_river', 'generate_lake', 'custo_terrain']
            self.afficher_formulaire(variables)
        elif bouton_quitter.collidepoint(x, y):
            pygame.quit()
            sys.exit()

    def menu_principal(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_souris, y_souris = pygame.mouse.get_pos()
                    self.gestion_clic_menu(x_souris, y_souris)

            self.afficher_image_de_fond("fond.jpeg")

            self.afficher_texte("Game Of Life", self.LARGEUR // 2, 100, 56)
            self.dessiner_bouton(self.ROSE, 300, 200, 200, 50, "Start")
            self.dessiner_bouton(self.ROSE, 300, 300, 200, 50, "Options")
            self.dessiner_bouton(self.ROSE, 300, 400, 200, 50, "Quitter")

            pygame.display.update()

    def interface_jeu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.mettre_a_jour_fenetre()
            # Mettez votre interface de jeu ici
            pygame.display.update()

    def mettre_a_jour_fenetre(self):
        self.afficher_image_de_fond("fond.jpeg")

if __name__ == "__main__":
    menu = Menu()
    menu.menu_principal()