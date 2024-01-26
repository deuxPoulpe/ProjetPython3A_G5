import pickle
import os

class GestionnaireSauvegarde:
    def __init__(self, extension_fichier, dossier_sauvegarde):
        # Constructeur de la classe GestionnaireSauvegarde
        self.extension_fichier = extension_fichier  # Extension du fichier pour les données sauvegardées
        self.dossier_sauvegarde = dossier_sauvegarde  # Dossier où les fichiers de sauvegarde seront stockés

    def sauvegarder_donnees(self, donnees, nom):
        # Sauvegarder des données dans un fichier
        fichier_sauvegarde = open(self.dossier_sauvegarde+"/"+nom+self.extension_fichier, "wb")
        pickle.dump(donnees, fichier_sauvegarde)
        fichier_sauvegarde.close()

    def charger_donnees(self, nom):
        # Charger des données à partir d'un fichier
        fichier_sauvegarde = open(self.dossier_sauvegarde+"/"+nom+self.extension_fichier, "rb")
        donnees = pickle.load(fichier_sauvegarde)
        fichier_sauvegarde.close()
        return donnees

    def verifier_existence_fichier(self, nom):
        # Vérifier si un fichier avec un nom donné existe dans le dossier de sauvegarde
        return os.path.exists(self.dossier_sauvegarde+"/"+nom+self.extension_fichier)

    def charger_donnees_jeu(self, fichiers_a_charger, donnees_par_defaut):
        # Charger les données du jeu depuis des fichiers ou utiliser des données par défaut si les fichiers n'existent pas
        variables = []
        for index, fichier in enumerate(fichiers_a_charger):
            if self.verifier_existence_fichier(fichier):
                variables.append(self.charger_donnees(fichier))
            else:
                variables.append(donnees_par_defaut[index])

        if len(variables) > 1:
            return tuple(variables)
        else:
            return variables[0]

    def sauvegarder_donnees_jeu(self, donnees_a_sauvegarder, noms_fichiers):
        # Sauvegarder les données du jeu dans des fichiers
        for index, fichier in enumerate(donnees_a_sauvegarder):
            self.sauvegarder_donnees(fichier, noms_fichiers[index])
