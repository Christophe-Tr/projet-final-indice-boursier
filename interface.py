"""
Christophe Tremblay
Projet final
interface.py
"""

import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import matplotlib
matplotlib.use("TkAgg") # Backend qui fonctionne avec tkinter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from indice_boursier import IndiceBoursier
from indice_boursier import PERIODES_VALIDES


# Nom du fichier CSV contenant les 10 actions favorites
NOM_FICHIER_CSV = "CSV indice boursier.csv"


# Chargement des actions depuis le fichier CSV
def charger_actions() :

    actions = []

    # Essayer d'abord le chemin direct, sinon avec le prefixe complet
    try :
        fichier_test = open(NOM_FICHIER_CSV)
        fichier_test.close()
        chemin = NOM_FICHIER_CSV

    except :
        chemin = "Projet/projet_final_indice_boursier/" + NOM_FICHIER_CSV

    # Essayer plusieurs encodages selon le systeme (Mac, Windows, etc.)
    encodage = "utf-8"

    try :
        fichier_test = open(chemin, encoding = "utf-8")
        fichier_test.read()
        fichier_test.close()

    except :
        encodage = "mac_roman"

    # Lire le fichier CSV ligne par ligne
    try :

        with open(chemin, encoding = encodage) as fichier :
            lecteur = csv.reader(fichier, delimiter = ";")
            numero_ligne = 0

            for ligne in lecteur :

                # Sauter l'entete (premiere ligne)
                if numero_ligne > 0 :

                    # Construire un dictionnaire pour chaque action
                    action = {
                        "nom" : ligne[0],
                        "description" : ligne[1],
                        "capitalisation" : ligne[2],
                        "date_entree" : ligne[3],
                        "pays" : ligne[4],
                        "secteur" : ligne[5],
                        "symbole" : ligne[6]
                    }

                    actions.append(action)

                numero_ligne += 1

    except BaseException as erreur :
        print("Erreur lors du chargement du fichier CSV : " + str(erreur))

    return actions


# Classe pour l'interface graphique de l'application
class InterfaceApplication :

    # Initialisation de l'interface
    def __init__(objet, fenetre) :

        # Configuration de la fenetre
        objet.fenetre = fenetre
        objet.fenetre.title("Recherche d'indices boursiers")
        objet.fenetre.geometry("900x750")

        # Indice presentement affiche (aucun au depart)
        objet.indice_courant = None

        # Action selectionnee dans le menu deroulant (aucune au depart)
        objet.details_action = None

        # Charger les 10 actions depuis le fichier CSV
        objet.actions = charger_actions()

        # Construction des differentes zones de l'interface
        objet.creer_titre()
        objet.creer_zone_recherche()
        objet.creer_zone_graphique()
        objet.creer_zone_statistiques()

    # Titre en haut de la fenetre
    def creer_titre(objet) :

        cadre = tk.Frame(objet.fenetre, bg = "#2c3e50", height = 50)
        cadre.pack(fill = tk.X)

        titre = tk.Label(cadre,
                         text = "Outil de recherche d'indices boursiers",
                         font = ("Arial", 16, "bold"),
                         bg = "#2c3e50", fg = "white")
        titre.pack(pady = 10)

    # Zone contenant le champ de recherche et le bouton
    def creer_zone_recherche(objet) :

        cadre = tk.Frame(objet.fenetre, pady = 10)
        cadre.pack(fill = tk.X, padx = 20)

        # Etiquette et champ pour le symbole
        tk.Label(cadre, text = "Symbole :",
                 font = ("Arial", 11)).grid(row = 0, column = 0, padx = 5)

        objet.champ_symbole = tk.Entry(cadre, width = 15, font = ("Arial", 11))
        objet.champ_symbole.grid(row = 0, column = 1, padx = 5)
        objet.champ_symbole.insert(0, "AAPL")

        # Etiquette et liste deroulante pour la periode
        tk.Label(cadre, text = "Periode :",
                 font = ("Arial", 11)).grid(row = 0, column = 2, padx = 5)

        objet.liste_periodes = ttk.Combobox(cadre,
                                            values = PERIODES_VALIDES,
                                            state = "readonly",
                                            width = 8,
                                            font = ("Arial", 11))
        objet.liste_periodes.set("6mo")
        objet.liste_periodes.grid(row = 0, column = 3, padx = 5)

        # Bouton rechercher
        bouton = tk.Button(cadre, text = "Rechercher",
                           command = objet.rechercher,
                           bg = "#2980b9", fg = "black",
                           font = ("Arial", 11, "bold"),
                           padx = 15, pady = 4)
        bouton.grid(row = 0, column = 4, padx = 10)

        # Etiquette et liste deroulante pour les actions favorites (CSV)
        tk.Label(cadre, text = "Exemple d'actions :",
                 font = ("Arial", 11)).grid(row = 1, column = 0,
                                            padx = 5, pady = (10, 0))

        # Construire la liste des noms d'actions a afficher dans le menu
        noms_actions = []

        for action in objet.actions :
            noms_actions.append(action["nom"])

        objet.liste_actions = ttk.Combobox(cadre,
                                           values = noms_actions,
                                           state = "readonly",
                                           width = 25,
                                           font = ("Arial", 11))
        objet.liste_actions.grid(row = 1, column = 1, columnspan = 3,
                                 padx = 5, pady = (10, 0), sticky = "w")

        # Appeler la methode selection_action quand l'utilisateur choisit une action
        objet.liste_actions.bind("<<ComboboxSelected>>", objet.selection_action)

    # Zone pour afficher le graphique matplotlib
    def creer_zone_graphique(objet) :

        cadre = tk.Frame(objet.fenetre)
        cadre.pack(fill = tk.BOTH, expand = True, padx = 20, pady = 10)

        # Creer la figure et l'axe matplotlib
        objet.figure = Figure(figsize = (8, 4), dpi = 100)
        objet.axe = objet.figure.add_subplot(111)
        objet.axe.set_title("Entre un symbole et clique sur Rechercher")
        objet.axe.grid(True)

        # Integrer la figure dans la fenetre Tkinter
        objet.canvas = FigureCanvasTkAgg(objet.figure, master = cadre)
        objet.canvas.draw()
        objet.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)

    # Zone pour afficher les statistiques
    def creer_zone_statistiques(objet) :

        cadre = tk.LabelFrame(objet.fenetre, text = "Statistiques",
                              font = ("Arial", 11, "bold"),
                              padx = 10, pady = 10)
        cadre.pack(fill = tk.X, padx = 20, pady = 10)

        objet.etiquette_stats = tk.Label(cadre,
                                         text = "Aucune donnee affichee.",
                                         font = ("Arial", 10),
                                         justify = tk.LEFT,
                                         wraplength = 820)
        objet.etiquette_stats.pack(anchor = tk.W)

    # Appelee quand l'utilisateur choisit une action dans le menu deroulant
    def selection_action(objet, evenement) :

        nom_choisi = objet.liste_actions.get()

        # Trouver l'action correspondante dans la liste chargee
        for action in objet.actions :

            if action["nom"] == nom_choisi :

                # Remplir automatiquement le champ symbole
                objet.champ_symbole.delete(0, tk.END)
                objet.champ_symbole.insert(0, action["symbole"])

                # Garder les details pour les afficher plus tard
                objet.details_action = action

                # Afficher les details dans la zone statistiques
                objet.afficher_details_action()
                return

    # Afficher uniquement les details d'une action selectionnee
    def afficher_details_action(objet) :

        if objet.details_action is None :
            return

        action = objet.details_action

        # Construire le texte ligne par ligne
        texte = ""
        texte += "Nom            : " + action["nom"] + "\n"
        texte += "Symbole        : " + action["symbole"] + "\n"
        texte += "Secteur        : " + action["secteur"] + "\n"
        texte += "Pays           : " + action["pays"] + "\n"
        texte += "Capitalisation : " + action["capitalisation"] + "\n"
        texte += "Date d'entree  : " + action["date_entree"] + "\n"
        texte += "\nDescription :\n" + action["description"]

        objet.etiquette_stats.config(text = texte)

    # Appelee quand l'utilisateur clique sur le bouton Rechercher
    def rechercher(objet) :

        symbole = objet.champ_symbole.get().strip()
        periode = objet.liste_periodes.get()

        # Verifier que le symbole n'est pas vide
        if symbole == "" :
            messagebox.showwarning("Attention", "Entre un symbole boursier.")
            return

        # Creer l'indice
        indice = IndiceBoursier(symbole, periode)

        # Verifier que l'indice est valide (symbole et periode corrects)
        if not indice.est_valide :
            messagebox.showerror("Erreur", "Symbole ou periode invalide.")
            return

        # Essayer de telecharger les donnees (peut echouer pour cause reseau)
        try :
            indice.telecharger_donnees()

        # Toute autre exception (probleme reseau, etc.)
        except BaseException as erreur :
            messagebox.showerror("Erreur inattendue", str(erreur))
            return

        # Si aucun prix n'a ete charge, le telechargement a echoue
        if len(indice.prix) == 0 :
            messagebox.showerror("Erreur",
                                 "Impossible de telecharger les donnees pour " + symbole)
            return

        # Afficher la courbe et les statistiques
        objet.indice_courant = indice
        indice.tracer_courbe(objet.axe)
        objet.canvas.draw()
        objet.afficher_statistiques(indice)

    # Afficher les statistiques de l'indice dans l'etiquette
    def afficher_statistiques(objet, indice) :

        stats = indice.obtenir_statistiques()
        prix_actuel = indice.obtenir_prix_actuel()

        # Construire le texte ligne par ligne
        texte = ""

        # Ajouter les details de l'action si une a ete selectionnee dans le menu
        if objet.details_action is not None :
            action = objet.details_action
            texte += "Nom            : " + action["nom"] + "\n"
            texte += "Secteur        : " + action["secteur"] + "\n"
            texte += "Pays           : " + action["pays"] + "\n"
            texte += "Capitalisation : " + action["capitalisation"] + "\n"
            texte += "Date d'entree  : " + action["date_entree"] + "\n"
            texte += "\n"

        # Ajouter les statistiques calculees
        texte += "Prix actuel : " + str(round(prix_actuel, 2)) + "\n"
        texte += "Minimum     : " + str(stats["min"]) + "\n"
        texte += "Maximum     : " + str(stats["max"]) + "\n"
        texte += "Moyenne     : " + str(stats["moyenne"]) + "\n"
        texte += "Volatilite  : " + str(stats["volatilite"]) + "\n"
        texte += "Variation   : " + str(stats["variation"]) + " %"

        objet.etiquette_stats.config(text = texte)


# Fonction pour demarrer l'application graphique
def lancer_application() :
    fenetre = tk.Tk()
    InterfaceApplication(fenetre)
    fenetre.mainloop()
