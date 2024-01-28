import pickle
import pygame
from display import Display
from api import Api
from world import World
import os
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import filedialog, messagebox, ttk, simpledialog
from Utility.save_utility import save, load


class Menu:
    def __init__(self):
        
        self.world = None
        self.api = None
        self.display = None
        
        self.toggle_fonction = {
            "move_smart" : False,
            "sexual_reproduction" : False,
            "custom_event" : False,
        }
             
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
            "event_days_rate" : 100,
            "toggle_fonction" : self.toggle_fonction,
        }
        self.option_changed = False
        self.is_running = False
        
            
        pygame.init()
        
        self.in_game_menu = Ig_menu()
        
        # Dimensions de la fenêtre
        self.LARGEUR, self.HAUTEUR = 800, 600

        # Initialisation de la bibliothèque Pygame pour le son
        pygame.mixer.init()
        # Charger la chanson (remplacez "votre_chanson.mp3" par le chemin de votre fichier audio)
        self.chanson = pygame.mixer.Sound("music2.mp3")
         # Jouer la chanson en boucle (-1 indique une lecture en boucle)
        pygame.mixer.Sound.play(self.chanson, loops=-1)

        # Création de la fenêtre Pygame
        self.fenetre = pygame.display.set_mode((self.LARGEUR, self.HAUTEUR))
        pygame.display.set_caption("PROJET_PYTHON_2024_G5")

        # Constantes de couleur
        self.NOIR = (0, 0, 0)
        self.ROSE = (255, 192, 203)

       # Initialisation de la police
        self.policeChoisie = os.path.join("assets", "GamepauseddemoRegular-RpmY6.otf")
        self.arial = os.path.join("assets", "arial.ttf")

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

        
    def jouer_chanson(self):
        # Jouer la chanson en boucle (-1 indique une lecture en boucle)
        self.music = pygame.mixer.Sound.play(self.chanson, loops=-1)      

    def dessiner_rectangle(self, couleur, x, y, largeur, hauteur, texte, taille_texte=36):
        pygame.draw.rect(self.fenetre, couleur, (x, y, largeur, hauteur))
        self.afficher_texte(texte, x + largeur // 2, y + hauteur // 2, taille_texte)
    def save_game(fic_name,jeu):
        with open(fic_name,'rb') as fichier:
            dictionnaire = pickle.load(fichier)
        dictionnaire[fic_name] = jeu

        with open(fic_name,'wb') as fichier:
            pickle.dump(dictionnaire,fichier)
    def save_load_menu(self):
        # Afficher le formulaire pour le nom de fichier
        file_name = self.ask_for_file_name()
        
        # Sauvegarder les données actuelles dans le fichier
        if file_name:
            save(file_name, World)
            print(f"Le jeu a été sauvegardé dans le fichier {file_name}")

        else:
            # Mettez à jour les variables du jeu avec les données chargées
            load(file_name)
            print(f"Le jeu a été chargé depuis le fichier {file_name}")

    def ask_for_file_name(self):
        # Utilisez la boîte de dialogue pour demander le nom de fichier
        root = tk.Tk()
        root.withdraw()
        file_name = filedialog.askopenfilename()

        if not file_name:
            create_new_file = tk.messagebox.askyesno("Fichier non trouve","le fichier n'existe pas.Voulez-vous creer un nouveau fichier ?")
            if create_new_file:
                file_name = self.create_new_file_dialog()

        return file_name
    
    def create_new_file_dialog(self):
        root=tk.Tk()
        root.withdraw()
        file_name =  filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    
        return file_name

    def load_game(self, file_name):
        # Charger les données depuis le fichier
        loaded_data = {}
        try:
            with open(file_name, 'rb') as file:
                loaded_data = pickle.load(file)
        except FileNotFoundError:
            print(f"Le fichier {file_name} n'existe pas.")
        except Exception as e:
            print(f"Une erreur s'est produite lors du chargement du jeu : {e}")

        return loaded_data




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
        self.afficher_image_de_fond("fond2.jpg")
       
        #for i, (variable, champ) in enumerate(zip(variables, self.champs_texte)):
            
            # # Affichage de la variable
            #surface_variable = self.police.render(variable, True, self.NOIR)
            # self.fenetre.blit(surface_variable, (50, 50 + i * 50))

            # # Champ de saisie
            # pygame.draw.rect(self.fenetre, self.couleur, champ, 2)
            # surface_texte = self.policeme.render(self.textes_champs[i], True, self.NOIR)
            # largeur_texte = max(200, surface_texte.get_width() + 10)
            # champ.w = largeur_texte
            # self.fenetre.blit(surface_texte, (champ.x + 5, champ.y + 5))

            # Bouton de retour
        self.dessiner_bouton(self.ROSE, 600, 505, 140, 50, "Retour")

        pygame.display.flip()


        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # for i, champ in enumerate(self.champs_texte):
                    #     if champ.collidepoint(event.pos):
                    #         self.champ_actif = i
                    #         self.couleur = self.couleur_active
                    #     else:
                    #         self.couleur = self.couleur_inactive
                    # if 600 <= event.pos[0] <= 700 and 500 <= event.pos[1] <= 530:
                    return True
                        # Attribuer les valeurs saisies aux variables
                        # for i, variable in enumerate(variables):
                        #     self.valeurs_variables[variable] = int(self.textes_champs[i])


                

    def gestion_clic_menu(self, x, y):
        bouton_demarrer = pygame.Rect(300, 200, 200, 50)
        bouton_resume = pygame.Rect(300, 300, 200, 50)
        bouton_quitter = pygame.Rect(300, 500, 200, 50)
        bouton_load_save = pygame.Rect(300, 400, 200, 50 ) 
        boutton_Retour = pygame.Rect(600, 500, 100, 30)  # Ajuster la taille du bouton
        if bouton_demarrer.collidepoint(x, y):
            pygame.quit()

            self.in_game_menu.main_loop()


        elif bouton_resume.collidepoint(x, y):
            variables = ['number_of_river', 'number_of_lake', 'size_of_lake', 'max_height', 'nbFood', 'dayTick', 'Food_energy', 'generate_river', 'generate_lake', 'custo_terrain']
            self.afficher_formulaire(variables)
        
        elif bouton_quitter.collidepoint(x, y):
            pygame.quit()
        
        elif boutton_Retour.collidepoint(x,y):
            return True
        
        elif bouton_load_save.collidepoint(x, y):
              #self.save_load_menu()
              self.save_world()
    


            

    def menu_principal(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_souris, y_souris = pygame.mouse.get_pos()
                    self.gestion_clic_menu(x_souris, y_souris)

            self.afficher_image_de_fond("fond.jpeg")

            text = "This game is centered around a visual and interactive simulation of natural selection.\n The game world is a grid, initially set at 100x100, with creatures named Bob living in it. \n There are 100 Bobs with individual attributes like speed, size, and memory, represented by customizable sprites.\n The graphical representation can be adjusted based on user preferences, such as making faster creatures\n appear bluer and larger ones redder. Each Bob starts in a random cell, and the simulation progresses in\n time increments, with Bobs performing various actions depending on the simulated characteristics.\n The parameters of the simulation are modifiable for experimentation.\n"

            self.afficher_texte("Game Of Life", self.LARGEUR // 2, 100, 56)
            self.dessiner_bouton(self.ROSE, 300, 200, 200, 50, "Start")
            self.dessiner_bouton(self.ROSE, 300, 300, 200, 50, "History")
            self.dessiner_bouton(self.ROSE, 300, 400, 200, 50, "Load_Save")
            self.dessiner_bouton(self.ROSE , 300, 500, 200, 50, "Quitter")
            

            pygame.display.update()

    def interface_jeu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.mettre_a_jour_fenetre()
            # Mettez votre interface de jeu ici
            pygame.display.update()

    def mettre_a_jour_fenetre(self):
        self.afficher_image_de_fond("fond.jpeg")
        
    def set_up_options_menu(self):
        
        def toggle_terrain_button_visibility(*args):
            if self.custom_terrain.get():
                terrain_option_button.grid()
            else:
                terrain_option_button.grid_remove()
        
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
        self.event_days_rate = tk.IntVar(value=self.option_values_sim["event_days_rate"])
        
        labels = ["World size", "Food number", "Food energy", "Bob max energy", "Bob initial energy", "Bob initial velocity",
                "Bob initial mass", "Bob initial perception", "Day tick", "Mutation rate", "Bob initial memory point", "Event Days rate", "Custom terrain"
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
                ttk.Entry(self.options_menu_frame, textvariable=self.event_days_rate),
                ttk.Checkbutton(self.options_menu_frame, text="", variable=self.custom_terrain),
                ]

        for i, label_text in enumerate(labels):
            label = ttk.Label(self.options_menu_frame, text=label_text, font=("Pixel", 12))
            pady_value = 20 if i == 0 else 2

            label.grid(row=i + 1, column=0, pady=(pady_value, 5), padx=(10, 20), sticky="e")

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
        
        terrain_option_button = ttk.Button(self.options_menu_frame, text="Terrain Option", command=self.show_option_terrain, width=15)
        terrain_option_button.grid(row=len(labels) + 1, column=0, columnspan=3, pady=15, sticky="n")
        toggle_terrain_button_visibility()
        
        toggle_function_button = ttk.Button(self.options_menu_frame, text="Toggle Function", command=self.show_toggle_foncion, width=15)
        toggle_function_button.grid(row=len(labels) + 2, column=0, columnspan=3, pady=15, sticky="n")

        save_button = ttk.Button(self.options_menu_frame, text="Save Options", command=self.save_options, width=15)
        save_button.grid(row=len(labels) + 3, column=0, columnspan=3, pady=15, sticky="s")
        
        load_button = ttk.Button(self.options_menu_frame, text="Load Option", command=self.load_options, width=15)
        load_button.grid(row=len(labels) + 4, column=0, columnspan=3, pady=15, sticky="s")
        
        validate_button = ttk.Button(self.options_menu_frame, text="Validate Options", command=self.validation_option, width=15)
        validate_button.grid(row=len(labels) + 5, column=0, columnspan=3, pady=15, sticky="s")

        
        return_button = ttk.Button(self.options_menu_frame, text="Return", command=self.show_main_menu, width=15)
        return_button.grid(row=len(labels) + 6, column=0, columnspan=3, pady=15, sticky="s")
        
        
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
        

        
        
        labels = ["River generation", "Number of rivers", "Lake generation", "Number of lakes", "Lake size", "Max height", "Water level", "Seed"]

        widget = [ ttk.Checkbutton(self.option_terrain_frame, text="", variable=self.generate_river),
                ttk.Scale(self.option_terrain_frame, from_=0, to=5, orient="horizontal", variable=self.number_of_river),
                ttk.Checkbutton(self.option_terrain_frame, text="", variable=self.generate_lake),
                ttk.Scale(self.option_terrain_frame, from_=0, to=5, orient="horizontal", variable=self.number_of_lake),
                ttk.Scale(self.option_terrain_frame, from_=0, to=100, orient="horizontal", variable=self.size_of_lake),
                ttk.Scale(self.option_terrain_frame, from_=0, to=15, orient="horizontal", variable=self.max_height),
                ttk.Scale(self.option_terrain_frame, from_=0, to=15, orient="horizontal", variable=self.water_level),
                ttk.Entry(self.option_terrain_frame, textvariable=self.seed),
                ]

        for i, label_text in enumerate(labels):
            label = ttk.Label(self.option_terrain_frame, text=label_text, font=("Pixel", 12))
            pady_value = 20 if i == 0 else 2
            label.grid(row=i + 1, column=0, pady=(pady_value, 5), padx=(10, 20), sticky="e")
            
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
        self.option_terrain_frame.rowconfigure(len(labels) + 1, weight=1)
        
              
        return_button = ttk.Button(self.option_terrain_frame, text="Return", command=self.show_options_menu, width=15)
        return_button.grid(row=len(labels) + 2, column=0, columnspan=3, pady=15, sticky="s")
        
        
    def set_up_toggle_fonction_menu(self):
        
        self.toggle_move_smart = tk.BooleanVar(value=self.toggle_fonction["move_smart"])
        self.toggle_sexual_reproduce = tk.BooleanVar(value=self.toggle_fonction["sexual_reproduction"])
        self.toggle_custom_event = tk.BooleanVar(value=self.toggle_fonction["custom_event"])

        labels = ["Move Smart", "Sexual Reproduce", "Custom event"]

        widget = [ 
                ttk.Checkbutton(self.toggle_fonction_menu, text="", variable=self.toggle_move_smart),
                ttk.Checkbutton(self.toggle_fonction_menu, text="", variable=self.toggle_sexual_reproduce),
                ttk.Checkbutton(self.toggle_fonction_menu, text="", variable=self.toggle_custom_event),
                ]

        for i, label_text in enumerate(labels):
            label = ttk.Label(self.toggle_fonction_menu, text=label_text, font=("Pixel", 12))
            pady_value = 20 if i == 0 else 2
            label.grid(row=i + 1, column=0, pady=(pady_value, 5), padx=(10, 20), sticky="e")
            
            scale_var = widget[i]
            scale_var.grid(row=i + 1, column=1, pady=(pady_value, 5), padx=(0, 0), sticky="w")
            
        self.toggle_fonction_menu.columnconfigure(0, weight=1)
        self.toggle_fonction_menu.columnconfigure(1, weight=1)
        self.toggle_fonction_menu.columnconfigure(2, weight=1)
        self.toggle_fonction_menu.rowconfigure(len(labels) + 1, weight=1)
                  
        return_button = ttk.Button(self.toggle_fonction_menu, text="Return", command=self.show_options_menu, width=15)
        return_button.grid(row=len(labels) + 1, column=0, columnspan=3, pady=15, sticky="s")       
        
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
        elif self.toggle_fonction_menu.winfo_ismapped():
            height = self.toggle_fonction_menu.winfo_reqheight() + 50
        self.root.geometry(f"{width}x{height}")
        
    def slider_changed(self, event, scale_var, label_var, nb_decimals=0):
            label_var.configure(text=self.get_current_value(scale_var, nb_decimals))        

    def get_current_value(self, scale_var, nb_decimals):
        format_string = '{:.' + str(nb_decimals) + 'f}'
        return format_string.format(scale_var.get())

    def show_options_menu(self):
        self.options_menu_frame.pack(expand=True, fill=tk.BOTH)
        self.option_terrain_frame.pack_forget()
        self.toggle_fonction_menu.pack_forget()
        self.main_menu_frame.pack_forget()
        self.bind_escape_key(self.options_menu_frame)
        self.root.bind("<Return>", lambda event: self.validation_option())
        self.update_geometry()

    def show_main_menu(self):
        self.options_menu_frame.pack_forget()
        self.main_menu_frame.pack(expand=True, fill=tk.BOTH)  
        self.bind_escape_key(self.main_menu_frame)
        self.update_geometry()
        
    def show_option_terrain(self):
        self.option_terrain_frame.pack(expand=True, fill=tk.BOTH)  
        self.options_menu_frame.pack_forget()
        self.main_menu_frame.pack_forget()
        self.bind_escape_key(self.option_terrain_frame)
        self.update_geometry()
        
    def show_toggle_foncion(self):
        self.toggle_fonction_menu.pack(expand=True, fill=tk.BOTH)  
        self.options_menu_frame.pack_forget()
        self.main_menu_frame.pack_forget()
        self.bind_escape_key(self.toggle_fonction_menu)
        self.update_geometry()

    def bind_escape_key(self, frame):
        self.root.bind("<Escape>", lambda event, frame=frame: self.handle_escape_key(frame))

    def handle_escape_key(self, frame):
        if frame == self.options_menu_frame:
            self.show_main_menu()
        elif frame == self.option_terrain_frame or frame == self.toggle_fonction_menu:
            self.show_options_menu()
        else:
            self.root.destroy()

        
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
            self.seed.get()
        except:
            self.error_invalid_input()
            return -1
        
        self.toggle_fonction_validate = {
            "move_smart" : self.toggle_move_smart.get(),
            "sexual_reproduction" : self.toggle_sexual_reproduce.get(),
            "custom_event" : self.toggle_custom_event.get(),
        }

        
        
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
            "event_days_rate" : self.event_days_rate.get(),
            "toggle_fonction" : self.toggle_fonction_validate,
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
        
        messagebox.showinfo("Info", "Options validated")
        
    def get_options(self):
        return self.option_values_sim_validate, self.option_value_terrain_validate
    def is_option_changed(self):
        return self.option_changed
    
    
    def change_the_option(self):
        if not self.is_running:
            messagebox.showerror("Error", "You need to start a new simulation before changing the option")
        elif self.validated:
            self.option_changed = True
            self.validated = False
            self.root.destroy()
        else:
            messagebox.showerror("Error", "You need to validate the option before changing it")
    
    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Sélectionnez un fichier", filetypes=[("Fichiers textes", "*.pkl"), ("Tous les fichiers", "*.*")])

        if file_path:
            return file_path
        else:
            return None
        
    def load_save_workd(self):
        file_path = self.open_file_dialog()
        if file_path is None:
            return -1
        
        if file_path:
            objs_gen = load(file_path)
            obj = next(objs_gen)
            if isinstance(obj, World):
                messagebox.showinfo("Info", "Save loaded")
                self.world = obj
                self.option_values_sim = self.world.get_argDict()
                self.option_value_terrain = self.world.get_terrain_config()
                self.toggle_fonction = self.world.get_argDict()["toggle_fonction"]
                self.option_values_sim_validate = self.option_values_sim
                self.option_value_terrain_validate = self.option_value_terrain
                self.toggle_fonction_validate = self.toggle_fonction
                self.option_changed = True
                self.validated = True
                self.set_up_options_menu()
                self.set_up_options_terrain_menu()
                self.set_up_toggle_fonction_menu()

            else:
                messagebox.showerror("Error", "Invalid save file")
        else:
            messagebox.showerror("Error", "Path not found")

    def save_world(self):
        if not self.is_running and self.world is None:
            messagebox.showerror("Error", "You need to start a new simulation before saving it")
            return -1

        file_path = filedialog.asksaveasfilename(title="Sélectionnez un fichier", filetypes=[("Fichiers textes", "*.pkl"), ("Tous les fichiers", "*.*")])
        if file_path is None:
            return -1

        if file_path:
            if not file_path.endswith(".pkl"):
                file_path += ".pkl"
            print("Fichier sélectionné:", file_path)
            world_to_save = self.api.get_world_sim() if self.api else None
            if world_to_save is None:
                messagebox.showerror("Error", "You need to start a new simulation before saving it")
                return -1
            save(file_path, world_to_save)
            messagebox.showinfo("Info", "Save successful")
        else:
            messagebox.showerror("Error", "Path not found")
            return -1
        
        
    def save_options(self):
        if self.validated:
            file_path = filedialog.asksaveasfilename(title="Sélectionnez un fichier", filetypes=[("Fichiers textes", "*.pkl"), ("Tous les fichiers", "*.*")])
            if file_path is None:
                return -1
        
            if file_path:
                if not file_path.endswith(".pkl"):
                    file_path += ".pkl"
                save(file_path, "valide_option", (self.option_value_terrain_validate, self.option_values_sim_validate))
                messagebox.showinfo("Info", "Save successful")
            else:
                messagebox.showerror("Error", "Path not found")
                return -1
        else:
            messagebox.showerror("Error", "You need to validate the option before saving it")
            return -1
        
    def load_options(self):
        file_path = self.open_file_dialog()
        if file_path is None:
            return -1
        
        if file_path:
            objs_gen = load(file_path)
            obj = next(objs_gen)
            if obj == "valide_option":
                obj = next(objs_gen)
                messagebox.showinfo("Info", "Save loaded")
                self.option_values_sim = obj[1]
                self.option_value_terrain = obj[0]
                self.toggle_fonction = self.option_values_sim["toggle_fonction"]
                self.option_values_sim_validate = self.option_values_sim
                self.option_value_terrain_validate = self.option_value_terrain
                self.toggle_fonction_validate = self.toggle_fonction 
                self.option_changed = True
                self.validated = True
                self.set_up_options_menu()
                self.set_up_options_terrain_menu()
                self.set_up_toggle_fonction_menu()
            else:
                messagebox.showerror("Error", "Invalid save file")
        else:
            messagebox.showerror("Error", "Path not found")
            return -1


        
        
    def start_new_simulation(self):
        if self.is_running:
            messagebox.showerror("Error", "You need to stop the current simulation before starting a new one")
            return -1
        elif self.validated:

            self.option_changed = True

            if self.world is None:
                self.world = World(self.option_values_sim_validate, self.option_value_terrain_validate)
        
                ask_number_of_bob = simpledialog.askinteger("Number of bob", "Enter the number of bob you want to spawn", parent=self.root, minvalue=1, maxvalue=self.world.get_size()**2)
                if ask_number_of_bob is None:
                    return -1
                
                self.world.spawn_bob(ask_number_of_bob)

            self.api = Api(self.world, 100)
            self.display = Display(self.api, self)
            self.is_running = True
                
            self.root.destroy()
            self.display.main_loop()
            
        else:
            messagebox.showerror("Error", "You need to validate the option before starting a new simulation")
            return -1
        
    def stop_simulation(self):
        if not self.is_running:
            messagebox.showerror("Error", "You need to start a new simulation before changing the option")
            return -1
        else:
            self.is_running = False
            self.display.close_display()
            self.world = None
            self.api = None
            self.display = None
            return 0
        
    def exit(self):
        self.root.destroy()
        if self.is_running:
            self.stop_simulation()
        exit()


    
    
class Ig_menu: 

    def __init__(self):

       
        self.world = None
        self.api = None
        self.display = None
        
        self.toggle_fonction = {
            "move_smart" : False,
            "sexual_reproduction" : False,
            "custom_event" : False,
        }

             
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
            "event_days_rate" : 100,
            "toggle_fonction" : self.toggle_fonction,
        }
        self.option_changed = False
        self.is_running = False
        
                
    def set_up_options_menu(self):
        
        def toggle_terrain_button_visibility(*args):
            if self.custom_terrain.get():
                terrain_option_button.grid()
            else:
                terrain_option_button.grid_remove()
        
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
        self.event_days_rate = tk.IntVar(value=self.option_values_sim["event_days_rate"])
        
        labels = ["World size", "Food number", "Food energy", "Bob max energy", "Bob initial energy", "Bob initial velocity",
                "Bob initial mass", "Bob initial perception", "Day tick", "Mutation rate", "Bob initial memory point", "Event Days rate", "Custom terrain"
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
                ttk.Entry(self.options_menu_frame, textvariable=self.event_days_rate),
                ttk.Checkbutton(self.options_menu_frame, text="", variable=self.custom_terrain),
                ]

        for i, label_text in enumerate(labels):
            label = ttk.Label(self.options_menu_frame, text=label_text, font=("Pixel", 12))
            pady_value = 20 if i == 0 else 2

            label.grid(row=i + 1, column=0, pady=(pady_value, 5), padx=(10, 20), sticky="e")

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
        
        terrain_option_button = ttk.Button(self.options_menu_frame, text="Terrain Option", command=self.show_option_terrain, width=15)
        terrain_option_button.grid(row=len(labels) + 1, column=0, columnspan=3, pady=15, sticky="n")
        toggle_terrain_button_visibility()
        
        toggle_function_button = ttk.Button(self.options_menu_frame, text="Toggle Function", command=self.show_toggle_foncion, width=15)
        toggle_function_button.grid(row=len(labels) + 2, column=0, columnspan=3, pady=15, sticky="n")

        save_button = ttk.Button(self.options_menu_frame, text="Save Options", command=self.save_options, width=15)
        save_button.grid(row=len(labels) + 3, column=0, columnspan=3, pady=15, sticky="s")
        
        load_button = ttk.Button(self.options_menu_frame, text="Load Option", command=self.load_options, width=15)
        load_button.grid(row=len(labels) + 4, column=0, columnspan=3, pady=15, sticky="s")
        
        validate_button = ttk.Button(self.options_menu_frame, text="Validate Options", command=self.validation_option, width=15)
        validate_button.grid(row=len(labels) + 5, column=0, columnspan=3, pady=15, sticky="s")

        
        return_button = ttk.Button(self.options_menu_frame, text="Return", command=self.show_main_menu, width=15)
        return_button.grid(row=len(labels) + 6, column=0, columnspan=3, pady=15, sticky="s")
        
        
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
        

        
        
        labels = ["River generation", "Number of rivers", "Lake generation", "Number of lakes", "Lake size", "Max height", "Water level", "Seed"]

        widget = [ ttk.Checkbutton(self.option_terrain_frame, text="", variable=self.generate_river),
                ttk.Scale(self.option_terrain_frame, from_=0, to=5, orient="horizontal", variable=self.number_of_river),
                ttk.Checkbutton(self.option_terrain_frame, text="", variable=self.generate_lake),
                ttk.Scale(self.option_terrain_frame, from_=0, to=5, orient="horizontal", variable=self.number_of_lake),
                ttk.Scale(self.option_terrain_frame, from_=0, to=100, orient="horizontal", variable=self.size_of_lake),
                ttk.Scale(self.option_terrain_frame, from_=0, to=15, orient="horizontal", variable=self.max_height),
                ttk.Scale(self.option_terrain_frame, from_=0, to=15, orient="horizontal", variable=self.water_level),
                ttk.Entry(self.option_terrain_frame, textvariable=self.seed),
                ]

        for i, label_text in enumerate(labels):
            label = ttk.Label(self.option_terrain_frame, text=label_text, font=("Pixel", 12))
            pady_value = 20 if i == 0 else 2
            label.grid(row=i + 1, column=0, pady=(pady_value, 5), padx=(10, 20), sticky="e")
            
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
        self.option_terrain_frame.rowconfigure(len(labels) + 1, weight=1)
        
              
        return_button = ttk.Button(self.option_terrain_frame, text="Return", command=self.show_options_menu, width=15)
        return_button.grid(row=len(labels) + 2, column=0, columnspan=3, pady=15, sticky="s")
        
        
    def set_up_toggle_fonction_menu(self):
        
        self.toggle_move_smart = tk.BooleanVar(value=self.toggle_fonction["move_smart"])
        self.toggle_sexual_reproduce = tk.BooleanVar(value=self.toggle_fonction["sexual_reproduction"])
        self.toggle_custom_event = tk.BooleanVar(value=self.toggle_fonction["custom_event"])

        labels = ["Move Smart", "Sexual Reproduce", "Custom event"]

        widget = [ 
                ttk.Checkbutton(self.toggle_fonction_menu, text="", variable=self.toggle_move_smart),
                ttk.Checkbutton(self.toggle_fonction_menu, text="", variable=self.toggle_sexual_reproduce),
                ttk.Checkbutton(self.toggle_fonction_menu, text="", variable=self.toggle_custom_event),
                ]

        for i, label_text in enumerate(labels):
            label = ttk.Label(self.toggle_fonction_menu, text=label_text, font=("Pixel", 12))
            pady_value = 20 if i == 0 else 2
            label.grid(row=i + 1, column=0, pady=(pady_value, 5), padx=(10, 20), sticky="e")
            
            scale_var = widget[i]
            scale_var.grid(row=i + 1, column=1, pady=(pady_value, 5), padx=(0, 0), sticky="w")
            
        self.toggle_fonction_menu.columnconfigure(0, weight=1)
        self.toggle_fonction_menu.columnconfigure(1, weight=1)
        self.toggle_fonction_menu.columnconfigure(2, weight=1)
        self.toggle_fonction_menu.rowconfigure(len(labels) + 1, weight=1)
                  
        return_button = ttk.Button(self.toggle_fonction_menu, text="Return", command=self.show_options_menu, width=15)
        return_button.grid(row=len(labels) + 1, column=0, columnspan=3, pady=15, sticky="s")       
        
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
        elif self.toggle_fonction_menu.winfo_ismapped():
            height = self.toggle_fonction_menu.winfo_reqheight() + 50
        self.root.geometry(f"{width}x{height}")
        
    def slider_changed(self, event, scale_var, label_var, nb_decimals=0):
            label_var.configure(text=self.get_current_value(scale_var, nb_decimals))        

    def get_current_value(self, scale_var, nb_decimals):
        format_string = '{:.' + str(nb_decimals) + 'f}'
        return format_string.format(scale_var.get())

    def show_options_menu(self):
        self.options_menu_frame.pack(expand=True, fill=tk.BOTH)
        self.option_terrain_frame.pack_forget()
        self.toggle_fonction_menu.pack_forget()
        self.main_menu_frame.pack_forget()
        self.bind_escape_key(self.options_menu_frame)
        self.root.bind("<Return>", lambda event: self.validation_option())
        self.update_geometry()

    def show_main_menu(self):
        self.options_menu_frame.pack_forget()
        self.main_menu_frame.pack(expand=True, fill=tk.BOTH)  
        self.bind_escape_key(self.main_menu_frame)
        self.update_geometry()
        
    def show_option_terrain(self):
        self.option_terrain_frame.pack(expand=True, fill=tk.BOTH)  
        self.options_menu_frame.pack_forget()
        self.main_menu_frame.pack_forget()
        self.bind_escape_key(self.option_terrain_frame)
        self.update_geometry()
        
    def show_toggle_foncion(self):
        self.toggle_fonction_menu.pack(expand=True, fill=tk.BOTH)  
        self.options_menu_frame.pack_forget()
        self.main_menu_frame.pack_forget()
        self.bind_escape_key(self.toggle_fonction_menu)
        self.update_geometry()

    def bind_escape_key(self, frame):
        self.root.bind("<Escape>", lambda event, frame=frame: self.handle_escape_key(frame))

    def handle_escape_key(self, frame):
        if frame == self.options_menu_frame:
            self.show_main_menu()
        elif frame == self.option_terrain_frame or frame == self.toggle_fonction_menu:
            self.show_options_menu()
        else:
            self.root.destroy()
            
    def main_loop(self):
        
        pygame.mixer.init()
        # Charger la chanson (remplacez "votre_chanson.mp3" par le chemin de votre fichier audio)
        self.chanson = pygame.mixer.Sound("music2.mp3")
         # Jouer la chanson en boucle (-1 indique une lecture en boucle)
        pygame.mixer.Sound.play(self.chanson, loops=-1)

        self.option_value_terrain = self.option_value_terrain_validate if self.option_changed else self.option_value_terrain
        self.option_values_sim = self.option_values_sim_validate if self.option_changed else self.option_values_sim
        self.toggle_custom_event = self.toggle_fonction_validate if self.option_changed else self.toggle_fonction
        self.option_changed = False
        self.validated = False

        self.root = ThemedTk(theme="breeze")
        font_size = 12
        style = ttk.Style()
        style.configure("TButton", font=("Pixel", font_size))
        style.configure("TLabel", font=("Pixel", font_size))
        style.configure("TCheckbutton", font=("Pixel", font_size))
        style.configure("TEntry", font=("Pixel", font_size))
        self.root.resizable(False, False)
        
        screen_width = min(1920, self.root.winfo_screenwidth())
        screen_height = min(1080, self.root.winfo_screenheight())
        
        x_position = (screen_width - 300) // 2
        y_position = (screen_height - 300) // 6
        
        self.root.geometry(f'280x300+{x_position}+{y_position}')
        self.root.title('Game Of Life')
        self.root.iconbitmap(os.path.join("assets/UI", "bob.ico")) if os.name == 'nt' else None

        self.root.bind("<Escape>", lambda event: self.root.destroy())

        self.options_menu_frame = ttk.Frame(self.root)
        self.main_menu_frame = ttk.Frame(self.root)
        self.option_terrain_frame = ttk.Frame(self.root)
        self.toggle_fonction_menu = ttk.Frame(self.root)
                
        start_sim_button = ttk.Button(self.main_menu_frame, text="Start New\nSimulation", command=self.start_new_simulation, width=15)
        start_sim_button.pack(pady=15)
        
        exit_sim_button = ttk.Button(self.main_menu_frame, text="     Stop\nSimulation", command=self.stop_simulation, width=15)
        exit_sim_button.pack(pady=15)
        
        change_sim_button = ttk.Button(self.main_menu_frame, text="Change Simulation\n        Options", command=self.change_the_option, width=15)
        change_sim_button.pack(pady=15)
        
        options_button = ttk.Button(self.main_menu_frame, text="Simulation Options", command=self.show_options_menu, width=15)
        options_button.pack(pady=15)

        save_button = ttk.Button(self.main_menu_frame, text="Save", command=self.save_world, width=15)
        save_button.pack(pady=15)
        
        load_save_button = ttk.Button(self.main_menu_frame, text="Load Save", command=self.load_save_world, width=15)
        load_save_button.pack(pady=15)
        
        exit_button = ttk.Button(self.main_menu_frame, text="Exit", command=self.exit, width=15)
        exit_button.pack(pady=15, side=tk.BOTTOM)
       
        close_button = ttk.Button(self.main_menu_frame, text="Return", command=self.root.destroy, width=15)
        close_button.pack(pady=15, side=tk.BOTTOM)

        self.set_up_options_menu()
        self.set_up_options_terrain_menu()
        self.set_up_toggle_fonction_menu()
                
        self.update_geometry()
        self.show_main_menu()

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
            self.seed.get()
        except:
            self.error_invalid_input()
            return -1
        
        self.toggle_fonction_validate = {
            "move_smart" : self.toggle_move_smart.get(),
            "sexual_reproduction" : self.toggle_sexual_reproduce.get(),
            "custom_event" : self.toggle_custom_event.get(),
        }
        
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
            "event_days_rate" : self.event_days_rate.get(),
            "toggle_fonction" : self.toggle_fonction_validate,
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
        
        messagebox.showinfo("Info", "Options validated")
        
    def get_options(self):
        return self.option_values_sim_validate, self.option_value_terrain_validate
    def is_option_changed(self):
        return self.option_changed
    
    
    def change_the_option(self):
        if not self.is_running:
            messagebox.showerror("Error", "You need to start a new simulation before changing the option")
        elif self.validated:
            self.option_changed = True
            self.validated = False
            self.root.destroy()
        else:
            messagebox.showerror("Error", "You need to validate the option before changing it")
    
    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Sélectionnez un fichier", filetypes=[("Fichiers textes", "*.pkl"), ("Tous les fichiers", "*.*")])

        if file_path:
            return file_path
        else:
            return None
        
    def load_save_world(self):
        file_path = self.open_file_dialog()
        if file_path is None:
            return -1
        
        if file_path:
            objs_gen = load(file_path)
            obj = next(objs_gen)
            if isinstance(obj, World):
                messagebox.showinfo("Info", "Save loaded")
                self.world = obj
                self.option_values_sim = self.world.get_argDict()
                self.option_value_terrain = self.world.get_terrain_config()
                self.toggle_fonction = self.world.get_argDict()["toggle_fonction"]
                self.option_values_sim_validate = self.option_values_sim
                self.option_value_terrain_validate = self.option_value_terrain
                self.toggle_fonction_validate = self.toggle_fonction
                self.option_changed = True
                self.validated = True
                self.set_up_options_menu()
                self.set_up_options_terrain_menu()
                self.set_up_toggle_fonction_menu()

            else:
                messagebox.showerror("Error", "Invalid save file")
        else:
            messagebox.showerror("Error", "Path not found")

    def save_world(self):
        if not self.is_running and self.world is None:
            messagebox.showerror("Error", "You need to start a new simulation before saving it")
            return -1

        file_path = filedialog.asksaveasfilename(title="Sélectionnez un fichier", filetypes=[("Fichiers textes", "*.pkl"), ("Tous les fichiers", "*.*")])
        if file_path is None:
            return -1

        if file_path:
            if not file_path.endswith(".pkl"):
                file_path += ".pkl"
            print("Fichier sélectionné:", file_path)
            world_to_save = self.api.get_world_sim() if self.api else None
            if world_to_save is None:
                messagebox.showerror("Error", "You need to start a new simulation before saving it")
                return -1
            save(file_path, world_to_save)
            messagebox.showinfo("Info", "Save successful")
        else:
            messagebox.showerror("Error", "Path not found")
            return -1
        
        
    def save_options(self):
        if self.validated:
            file_path = filedialog.asksaveasfilename(title="Sélectionnez un fichier", filetypes=[("Fichiers textes", "*.pkl"), ("Tous les fichiers", "*.*")])
            if file_path is None:
                return -1
        
            if file_path:
                if not file_path.endswith(".pkl"):
                    file_path += ".pkl"
                save(file_path, "valide_option", (self.option_value_terrain_validate, self.option_values_sim_validate))
                messagebox.showinfo("Info", "Save successful")
            else:
                messagebox.showerror("Error", "Path not found")
                return -1
        else:
            messagebox.showerror("Error", "You need to validate the option before saving it")
            return -1
        
    def load_options(self):
        file_path = self.open_file_dialog()
        if file_path is None:
            return -1
        
        if file_path:
            objs_gen = load(file_path)
            obj = next(objs_gen)
            if obj == "valide_option":
                obj = next(objs_gen)
                messagebox.showinfo("Info", "Save loaded")
                self.option_values_sim = obj[1]
                self.option_value_terrain = obj[0]
                self.toggle_fonction = self.option_values_sim["toggle_fonction"]
                self.option_values_sim_validate = self.option_values_sim
                self.option_value_terrain_validate = self.option_value_terrain
                self.toggle_fonction_validate = self.toggle_fonction 
                self.option_changed = True
                self.validated = True
                self.set_up_options_menu()
                self.set_up_options_terrain_menu()
                self.set_up_toggle_fonction_menu()
            else:
                messagebox.showerror("Error", "Invalid save file")
        else:
            messagebox.showerror("Error", "Path not found")
            return -1


        
        
    def start_new_simulation(self):
        if self.is_running:
            messagebox.showerror("Error", "You need to stop the current simulation before starting a new one")
            return -1
        elif self.validated:

            self.option_changed = True

            if self.world is None:
                self.world = World(self.option_values_sim_validate, self.option_value_terrain_validate)
        
                ask_number_of_bob = simpledialog.askinteger("Number of bob", "Enter the number of bob you want to spawn", parent=self.root, minvalue=1, maxvalue=self.world.get_size()**2)
                if ask_number_of_bob is None:
                    return -1
                
                self.world.spawn_bob(ask_number_of_bob)

            self.api = Api(self.world, 100)
            self.display = Display(self.api, self)
            self.is_running = True
                
            self.root.destroy()
            self.display.main_loop()
            
        else:
            messagebox.showerror("Error", "You need to validate the option before starting a new simulation")
            return -1
        
    def stop_simulation(self):
        if not self.is_running:
            messagebox.showerror("Error", "You need to start a new simulation before changing the option")
            return -1
        else:
            self.is_running = False
            self.display.close_display()
            self.world = None
            self.api = None
            self.display = None
            return 0
        
    def exit(self):
        self.root.destroy()
        if self.is_running:
            self.stop_simulation()
        exit()


          
        
if __name__ == "__main__":

    menu = Menu()
    menu.menu_principal()
    # ig_menu = Ig_menu()
    # ig_menu.main_loop()

