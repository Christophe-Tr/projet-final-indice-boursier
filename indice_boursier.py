"""
Christophe Tremblay
Projet final
indice_boursier.py
"""
 
import yfinance as yf
 
 
# Liste des periodes acceptees par yfinance
PERIODES_VALIDES = ["1d", "5d", "1mo", "3mo", "6mo",
                    "1y", "2y", "5y", "10y", "ytd", "max"]
 
 
# Classe pour les differents indices boursiers
class IndiceBoursier :
 
    # Initialisation des attributs
    def __init__(objet, symbole, periode = "6mo") :
 
        # Initialiser les attributs avec des valeurs par defaut
        objet.symbole = ""
        objet.periode = "6mo"
        objet.nom_complet = ""
        objet.dates = []
        objet.prix = []
        objet.est_valide = True
 
        # Valider le symbole
        if symbole == "" or type(symbole) != str :
            print("Erreur : Le symbole doit etre un indice non vide.")
            objet.est_valide = False
            return
 
        # Valider la periode
        if periode not in PERIODES_VALIDES :
            print("Erreur : Periode invalide : " + str(periode))
            objet.est_valide = False
            return
 
        # Si tout est valide on assigne les vraies valeurs
        objet.symbole = symbole.upper().strip()
        objet.periode = periode
        objet.nom_complet = objet.symbole
 
    # Affichage de l'indice
    def __str__(objet) :
        return f"{objet.nom_complet} ({objet.symbole}) - {objet.periode}"
 
    # Telechargement des donnees depuis yfinance
    def telecharger_donnees(objet) :
 
        # Si l'indice n'est pas valide, on arrete
        if not objet.est_valide :
            print("Erreur : indice invalide, impossible de telecharger.")
            return None
 
        # Recuperer les donnees via yfinance
        # Ticker = code abrégé qui identifie une action en bourse
        ticker = yf.Ticker(objet.symbole)
        historique = ticker.history(period = objet.periode)
 
        # Si aucune donnee le symbole est probablement inexistant
        if historique.empty :
            print("Erreur : Aucune donnee pour le symbole : " + objet.symbole)
            objet.est_valide = False
            return None
 
        # Vider les listes avant de les remplir
        objet.dates = []
        objet.prix = []
 
        # Extraire les dates (index du tableau yfinance)
        for date in historique.index :
            objet.dates.append(date)
 
        # Extraire les prix de cloture
        for prix in historique["Close"] :
            objet.prix.append(round(float(prix), 2))
 
        # Essayer de recuperer le nom complet de l'entreprise
        try :
            info = ticker.info
 
            if "longName" in info :
                objet.nom_complet = info["longName"]
 
            elif "shortName" in info :
                objet.nom_complet = info["shortName"]
 
        # Si le nom n'est pas disponible, on garde juste le symbole
        except BaseException :
            objet.nom_complet = objet.symbole
 
    # Retourne le dernier prix de cloture (ou None si aucune donnee)
    def obtenir_prix_actuel(objet) :
 
        if len(objet.prix) == 0 :
            print("Erreur : Aucune donnee.")
            return None
 
        return objet.prix[-1]
 
    # Retourne la variation en pourcentage sur la periode (ou None)
    def obtenir_variation(objet) :
 
        if len(objet.prix) == 0 :
            print("Erreur : Aucune donnee.")
            return None
 
        prix_debut = objet.prix[0]
        prix_fin = objet.prix[-1]
 
        # Eviter la division par zero
        if prix_debut == 0 :
            return 0.0
 
        variation = ((prix_fin - prix_debut) / prix_debut) * 100
 
        return round(variation, 2)
 
    # Retourne un dictionnaire avec les statistiques (ou None si aucune donnee)
    def obtenir_statistiques(objet) :
 
        if len(objet.prix) == 0 :
            print("Erreur : Aucune donnee.")
            return None
 
        # Minimum et maximum
        minimum = min(objet.prix)
        maximum = max(objet.prix)
 
        # Moyenne
        somme = 0
 
        for prix in objet.prix :
            somme += prix
 
        moyenne = somme / len(objet.prix)
 
        # Volatilite (ecart type)
        somme_ecarts = 0
 
        for prix in objet.prix :
            somme_ecarts += (prix - moyenne) ** 2
 
        volatilite = (somme_ecarts / len(objet.prix)) ** 0.5
 
        # Construire le dictionnaire de statistiques
        stats = {
            "min" : round(minimum, 2),
            "max" : round(maximum, 2),
            "moyenne" : round(moyenne, 2),
            "volatilite" : round(volatilite, 2),
            "variation" : objet.obtenir_variation()
        }
 
        return stats
 
    # Trace la courbe des prix sur un axe matplotlib
    def tracer_courbe(objet, axe) :
 
        if len(objet.prix) == 0 :
            print("Erreur : Aucune donnee. Appelle telecharger_donnees() d'abord.")
            return None
 
        # Effacer le graphique precedent
        axe.clear()
 
        # Tracer la courbe des prix
        axe.plot(objet.dates, objet.prix, color = "blue", linewidth = 2, label = objet.symbole)
 
        # Titre et etiquettes
        titre = objet.nom_complet + " (" + objet.symbole + ") - " + objet.periode
        axe.set_title(titre)
        axe.set_xlabel("Date")
        axe.set_ylabel("Prix de cloture")
        axe.grid(True)
        axe.legend()