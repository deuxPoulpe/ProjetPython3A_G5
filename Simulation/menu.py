import pygame
import sys
from display import Display
from api import Api
from world import World
import os
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox


class Menu:
    def __init__(self):
        pygame.init()
        
        self.in_game_menu = Ig_menu()
        
        # Dimensions de la fenêtre
        self.LARGEUR, self.HAUTEUR = 800, 600

        # Création de la fenêtre Pygame
        self.fenetre = pygame.display.set_mode((self.LARGEUR, self.HAUTEUR))
        pygame.display.set_caption("PROJET_PYTHON_2024_G5")

        # Constantes de couleur
        self.NOIR = (0, 0, 0)
        self.ROSE = (255, 192, 203)

       # Initialisation de la police
        self.policeChoisie = os.path.join("assets", "GamepauseddemoRegular-RpmY6.otf")
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
        arriere_plan = pygame.image.load(os.path.join("assets", chemin_image))

        arriere_plan = pygame.transform.scale(arriere_plan, (self.LARGEUR, self.HAUTEUR))
        self.fenetre.blit(arriere_plan, (0, 0))

    def dessiner_bouton(self, couleur, x, y, largeur, hauteur, texte):
        pygame.draw.ellipse(self.fenetre, couleur, (x, y, largeur, hauteur))
        self.afficher_texte(texte, x + largeur // 2, y + hauteur // 2)

    def afficher_formulaire(self, variables):
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

            ###################################################
            #    modifier les varibles pour les options ici   #
            ###################################################

            terrain_config = {
            	"generate_river" : True,
            	"number_of_river" : 1,
            	"generate_lake" : False,
            	"number_of_lake" : 1,
            	"size_of_lake" : 20,
            	"max_height" : 10,
            	"seed" : 6432,
                "water_level" : 0,
            	}

            world = World({
            	"size" : 50,
            	"nbFood" : 50,
            	"dayTick" : 100,
            	"Food_energy" : 100,
            	"custom_terrain" : True,
            	}, terrain_config)
            
            world.spawn_bob(50)
            api = Api(world, 1)
            display = Display(api, self.in_game_menu)
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


class Ig_menu: 
    def __init__(self):           
        self.option_value_terrain = {
            "generate_river" : True,
            "number_of_river" : 1,
            "generate_lake" : True,
            "number_of_lake" : 1,
            "size_of_lake" : 20,
            "water_level" : 0,
            "max_height" : 10,
            "seed" : -1,
		}
        
        self.option_values_sim = {
            "size": 100,
            "nbFood": 200,
            "Food_energy": 100,
            "bob_max_energy": 200,
            "bob_energy": 100,
            "bob_velocity": 1,
            "bob_mass": 1,
            "bob_perception": 0,
            "dayTick": 100,
            "bob_mutation": 0,
            "bob_memory_point": 0,
            "custom_terrain" : False,
        }
        self.option_changed = False

        
                
    def set_up_options_menu(self):
        
        self.world_size = tk.IntVar(value=self.option_values_sim["size"])
        self.food_number = tk.IntVar(value=self.option_values_sim["nbFood"])
        self.food_energy = tk.IntVar(value=self.option_values_sim["Food_energy"])
        self.bob_max_energy = tk.IntVar(value=self.option_values_sim["bob_max_energy"])
        self.bob_initial_energy = tk.IntVar(value=self.option_values_sim["bob_energy"])
        self.bob_initial_velocity = tk.DoubleVar(value=self.option_values_sim["bob_velocity"])
        self.bob_initial_mass = tk.IntVar(value=self.option_values_sim["bob_mass"])
        self.bob_initial_perception = tk.IntVar(value=self.option_values_sim["bob_perception"])
        self.day_tick = tk.IntVar(value=self.option_values_sim["dayTick"])
        self.mutation_rate = tk.DoubleVar(value=self.option_values_sim["bob_mutation"])
        self.bob_initial_memory_point = tk.IntVar(value=self.option_values_sim["bob_memory_point"])
        self.custom_terrain = tk.BooleanVar(value=self.option_values_sim["custom_terrain"])
        
        labels = ["World size", "Food number", "Food energy", "Bob max energy", "Bob initial energy", "Bob initial velocity",
                "Bob initial mass", "Bob initial perception", "Day tick", "Mutation rate", "Bob initial memory point", "Custom terrain"
                ]

        widget = [
                ttk.Entry(self.options_menu_frame, textvariable=self.world_size),
                ttk.Entry(self.options_menu_frame, textvariable=self.food_number),
                ttk.Entry(self.options_menu_frame, textvariable=self.food_energy),
                ttk.Entry(self.options_menu_frame, textvariable=self.bob_max_energy),
                ttk.Entry(self.options_menu_frame, textvariable=self.bob_initial_energy),
                ttk.Scale(self.options_menu_frame, from_=1, to=10, orient="horizontal", variable=self.bob_initial_velocity),
                ttk.Scale(self.options_menu_frame, from_=1, to=100, orient="horizontal", variable=self.bob_initial_mass),
                ttk.Scale(self.options_menu_frame, from_=0, to=200, orient="horizontal", variable=self.bob_initial_perception),
                ttk.Entry(self.options_menu_frame, textvariable=self.day_tick),
                ttk.Scale(self.options_menu_frame, from_=0, to=1, orient="horizontal", variable=self.mutation_rate),
                ttk.Scale(self.options_menu_frame, from_=0, to=100, orient="horizontal", variable=self.bob_initial_memory_point),
                ttk.Checkbutton(self.options_menu_frame, text="Custom\n terrain", variable=self.custom_terrain),
                ]

        for i, label_text in enumerate(labels):
            label = ttk.Label(self.options_menu_frame, text=label_text, font=("Pixel", 12))
            pady_value = 20 if i == 0 else 2
            label.grid(row=i + 1, column=0, pady=(pady_value, 0), padx=(10, 20), sticky="e")

            scale_var = widget[i]
            scale_var.grid(row=i + 1, column=1, pady=(pady_value, 5), padx=(0, 0), sticky="w")

            
            if isinstance(scale_var, ttk.Scale):
                label_var = ttk.Label(self.options_menu_frame, text="")
                label_var.grid(row=i + 1, column=2, pady=(pady_value, 5), padx=(2, 10), sticky="w")
                if label_text in {'Mutation rate', 'Bob initial velocity'}:
                    scale_var.bind("<Motion>", lambda event, scale_var=scale_var, label_var=label_var: self.slider_changed(event, scale_var, label_var, 1))
                    self.slider_changed(None, scale_var, label_var, 1)
                else:
                    scale_var.bind("<Motion>", lambda event, scale_var=scale_var, label_var=label_var: self.slider_changed(event, scale_var, label_var))
                    self.slider_changed(None, scale_var, label_var)
            elif isinstance(scale_var, ttk.Entry):
                scale_var.config(width=13)

            

        self.options_menu_frame.columnconfigure(0, weight=1)
        self.options_menu_frame.columnconfigure(1, weight=1)
        self.options_menu_frame.columnconfigure(2, weight=1)
        self.options_menu_frame.rowconfigure(len(labels) + 1, weight=1)
        
        terrain_option_button = ttk.Button(self.options_menu_frame, text="Terrain Option", command=self.show_option_terrain)
        terrain_option_button.grid(row=len(labels) + 1, column=0, columnspan=3, pady=15, sticky="n")
        terrain_option_button.grid_remove()
        
        load_button = ttk.Button(self.options_menu_frame, text="Charger une sauvegarde de paramètre", command=self.validation_option)
        load_button.grid(row=len(labels) + 2, column=0, columnspan=3, pady=15, sticky="s")
        
        validate_button = ttk.Button(self.options_menu_frame, text="Valider Option", command=self.validation_option)
        validate_button.grid(row=len(labels) + 3, column=0, columnspan=3, pady=15, sticky="s")

        
        return_button = ttk.Button(self.options_menu_frame, text="Retour", command=self.show_main_menu)
        return_button.grid(row=len(labels) + 4, column=0, columnspan=3, pady=15, sticky="s")
        
        def toggle_terrain_button_visibility(*args):
            if self.custom_terrain.get():
                terrain_option_button.grid()
            else:
                terrain_option_button.grid_remove()
        self.custom_terrain.trace_add('write', toggle_terrain_button_visibility)
                


    def set_up_options_terrain_menu(self):
        
        
        self.generate_river = tk.BooleanVar(value=self.option_value_terrain["generate_river"])
        self.number_of_river = tk.IntVar(value=self.option_value_terrain["number_of_river"])
        self.generate_lake = tk.BooleanVar(value=self.option_value_terrain["generate_lake"])
        self.number_of_lake = tk.IntVar(value=self.option_value_terrain["number_of_lake"])
        self.size_of_lake = tk.IntVar(value=self.option_value_terrain["size_of_lake"])
        self.max_height = tk.IntVar(value=self.option_value_terrain["max_height"])
        self.seed = tk.IntVar(value=self.option_value_terrain["seed"])
        self.water_level = tk.IntVar(value=self.option_value_terrain["water_level"])
        

        
        
        labels = [ "Génération de rivière", "Nombre de rivière", "Génération de lac", "Nombre de lac", "Taille des lac", "Hauteur max", "Niveau de l'eau", "seed"]

        widget = [ ttk.Checkbutton(self.option_terrain_frame, text="generate_river", variable=self.generate_river),
                ttk.Scale(self.option_terrain_frame, from_=0, to=5, orient="horizontal", variable=self.number_of_river),
                ttk.Checkbutton(self.option_terrain_frame, text="generate_lake", variable=self.generate_lake),
                ttk.Scale(self.option_terrain_frame, from_=0, to=5, orient="horizontal", variable=self.number_of_lake),
                ttk.Scale(self.option_terrain_frame, from_=0, to=100, orient="horizontal", variable=self.size_of_lake),
                ttk.Scale(self.option_terrain_frame, from_=0, to=15, orient="horizontal", variable=self.max_height),
                ttk.Scale(self.option_terrain_frame, from_=0, to=15, orient="horizontal", variable=self.water_level),
                ttk.Entry(self.option_terrain_frame, textvariable=self.seed),
                ]

        for i, label_text in enumerate(labels):
            label = ttk.Label(self.option_terrain_frame, text=label_text, font=("Pixel", 12))
            pady_value = 20 if i == 0 else 2
            label.grid(row=i + 1, column=0, pady=(pady_value, 0), padx=(10, 20), sticky="e")

            scale_var = widget[i]
            scale_var.grid(row=i + 1, column=1, pady=(pady_value, 5), padx=(0, 0), sticky="w")

            
            if isinstance(scale_var, ttk.Scale):
                label_var = ttk.Label(self.option_terrain_frame, text="")
                label_var.grid(row=i + 1, column=2, pady=(pady_value, 5), padx=(2, 10), sticky="w")
                if label_text in {'Mutation rate', 'Bob initial velocity'}:
                    scale_var.bind("<Motion>", lambda event, scale_var=scale_var, label_var=label_var: self.slider_changed(event, scale_var, label_var, 1))
                    self.slider_changed(None, scale_var, label_var, 1)
                else:
                    scale_var.bind("<Motion>", lambda event, scale_var=scale_var, label_var=label_var: self.slider_changed(event, scale_var, label_var))
                    self.slider_changed(None, scale_var, label_var)
            elif isinstance(scale_var, ttk.Entry):
                scale_var.config(width=13)
                
            

        self.option_terrain_frame.columnconfigure(0, weight=1)
        self.option_terrain_frame.columnconfigure(1, weight=1)
        self.option_terrain_frame.columnconfigure(2, weight=1)
        self.option_terrain_frame.rowconfigure(len([]) + 1, weight=1)
        
              
        return_button = ttk.Button(self.option_terrain_frame, text="Retour", command=self.show_options_menu)
        return_button.grid(row=len(labels) + 2, column=0, columnspan=3, pady=15, sticky="s")

        
        
    def update_geometry(self):
        width = 400
        height = 400
        self.root.update_idletasks()
        if self.options_menu_frame.winfo_ismapped():
            height = self.options_menu_frame.winfo_reqheight() + 100
        elif self.main_menu_frame.winfo_ismapped():
            height = self.main_menu_frame.winfo_reqheight() + 50
        elif self.option_terrain_frame.winfo_ismapped():
            height = self.option_terrain_frame.winfo_reqheight() + 50
        self.root.geometry(f"{width}x{height}")
        
    def slider_changed(self, event, scale_var, label_var, nb_decimals=0):
            label_var.configure(text=self.get_current_value(scale_var, nb_decimals))        

    def get_current_value(self, scale_var, nb_decimals):
        format_string = '{:.' + str(nb_decimals) + 'f}'
        return format_string.format(scale_var.get())

    def show_options_menu(self):
        self.options_menu_frame.pack(expand=True, fill=tk.BOTH)
        self.option_terrain_frame.pack_forget()
        self.main_menu_frame.pack_forget()
        self.update_geometry()

    def show_main_menu(self):
        self.options_menu_frame.pack_forget()
        self.main_menu_frame.pack(expand=True, fill=tk.BOTH)  
        self.update_geometry()
        
    def show_option_terrain(self):
        self.option_terrain_frame.pack(expand=True, fill=tk.BOTH)  
        self.options_menu_frame.pack_forget()
        self.main_menu_frame.pack_forget()
        self.update_geometry()
        
    def main_loop(self):
        
        self.option_value_terrain = self.option_value_terrain_validate if self.option_changed else self.option_value_terrain
        self.option_values_sim = self.option_values_sim_validate if self.option_changed else self.option_values_sim
        self.option_changed = False
        self.validated = False

        self.root = ThemedTk(theme="breeze")
        font_size = 12
        style = ttk.Style()
        style.configure("TButton", font=("Pixel", font_size))
        style.configure("TLabel", font=("Pixel", font_size))
        style.configure("TCheckbutton", font=("Pixel", font_size))
        style.configure("TEntry", font=("Pixel", font_size))
        self.root.resizable(True, True)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_position = (screen_width - 300) // 2
        y_position = (screen_height - 300) // 4
        
        self.root.geometry(f'280x300+{x_position}+{y_position}')
        self.root.title('Menu de Paramétrage')

        self.options_menu_frame = ttk.Frame(self.root)
        self.main_menu_frame = ttk.Frame(self.root)
        self.option_terrain_frame = ttk.Frame(self.root)
        
        self.main_menu_frame.pack(expand=True, fill=tk.BOTH)  
        
        start_sim_button = ttk.Button(self.main_menu_frame, text="Lancer une simulation", command=lambda: print("Simulation lancée"))
        start_sim_button.pack(pady=15)
        
        change_sim_button = ttk.Button(self.main_menu_frame, text="Changer les options de la simulation", command=self.change_the_option)
        change_sim_button.pack(pady=15)
        
        options_button = ttk.Button(self.main_menu_frame, text="Simulation Options", command=self.show_options_menu)
        options_button.pack(pady=15)

        save_button = ttk.Button(self.main_menu_frame, text="Sauvegarder", command=lambda: print("Sauvegardé"))
        save_button.pack(pady=15)
        
        load_save_button = ttk.Button(self.main_menu_frame, text="Charger une sauvegarde", command=lambda: print("Chargé"))
        load_save_button.pack(pady=15)
       
        close_button = ttk.Button(self.main_menu_frame, text="Retour", command=self.root.destroy)
        close_button.pack(pady=15, side=tk.BOTTOM)

        self.set_up_options_menu()
        self.set_up_options_terrain_menu()
                
        self.update_geometry()
        self.root.mainloop()
        
    def error_invalid_input(self):
        messagebox.showerror("Error", "Invalid input only int or float")

    def validation_option(self):
                
        try :
            self.world_size.get()
            self.food_number.get()
            self.food_energy.get()
            self.bob_max_energy.get()
            self.bob_initial_energy.get()
            self.bob_initial_velocity.get()
            self.bob_initial_mass.get()
            self.bob_initial_perception.get()
            self.day_tick.get()
            self.mutation_rate.get()
            self.bob_initial_memory_point.get()
        except:
            self.error_invalid_input()
            return -1
        
        self.option_values_sim_validate = {
            "size": self.world_size.get(),
            "nbFood": self.food_number.get(),
            "Food_energy": self.food_energy.get(),
            "bob_max_energy": self.bob_max_energy.get(),
            "bob_energy": self.bob_initial_energy.get(),
            "bob_velocity": self.bob_initial_velocity.get(),
            "bob_mass": self.bob_initial_mass.get(),
            "bob_perception": self.bob_initial_perception.get(),
            "dayTick": self.day_tick.get(),
            "bob_mutation": self.mutation_rate.get(),
            "bob_memory_point": self.bob_initial_memory_point.get(),
            "custom_terrain" : self.custom_terrain.get(),
        }
        
        self.option_value_terrain_validate = {
            "generate_river" : self.generate_river.get(),
            "number_of_river" : self.number_of_river.get(),
            "generate_lake" : self.generate_lake.get(),
            "number_of_lake" : self.number_of_lake.get(),
            "size_of_lake" : self.size_of_lake.get(),
            "max_height" : self.max_height.get(),
            "seed" : None if self.seed.get() == -1 else self.seed.get(),
            "water_level" : self.water_level.get(),
        }
        
        self.validated = True      
        
    def get_options(self):
        return self.option_values_sim_validate, self.option_value_terrain_validate
    def is_option_changed(self):
        return self.option_changed
    
    
    def change_the_option(self):
        if self.validated:
            self.option_changed = True
        self.root.destroy()
        
       
        
if __name__ == "__main__":
    menu = Menu()
    menu.menu_principal()
    # ig_menu = ig_menu()
    # ig_menu.main_loop()


