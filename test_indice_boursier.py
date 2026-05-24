"""
Christophe Tremblay
Projet final
test_indice_boursier.py
"""
 
import unittest
import matplotlib.pyplot as plt
from indice_boursier import IndiceBoursier
 
 
# Tests pour la methode __init__
class TestConstructeur(unittest.TestCase) :
 
    # Construction normale
    def test_construction_normale(objet) :
        indice = IndiceBoursier("AAPL")
        objet.assertEqual(indice.symbole, "AAPL", "Le symbole n'est pas correct")
        objet.assertEqual(indice.periode, "6mo", "La periode par defaut n'est pas correcte")
        objet.assertEqual(indice.dates, [], "La liste de dates doit etre vide")
        objet.assertEqual(indice.prix, [], "La liste de prix doit etre vide")
        objet.assertEqual(indice.est_valide, True, "L'indice devrait etre valide")
 
    # Le symbole doit etre mis en majuscules
    def test_symbole_en_majuscules(objet) :
        indice = IndiceBoursier("aapl")
        objet.assertEqual(indice.symbole, "AAPL", "Le symbole doit etre en majuscules")
 
    # Periode personnalisee
    def test_periode_personnalisee(objet) :
        indice = IndiceBoursier("TSLA", "1y")
        objet.assertEqual(indice.periode, "1y", "La periode n'a pas ete prise en compte")
 
    # Symbole vide -> indice non valide
    def test_symbole_vide(objet) :
        indice = IndiceBoursier("")
        objet.assertEqual(indice.est_valide, False, "L'indice devrait etre invalide")
 
    # Symbole None -> indice non valide
    def test_symbole_invalide(objet) :
        indice = IndiceBoursier(None)
        objet.assertEqual(indice.est_valide, False, "L'indice devrait etre invalide")
 
    # Periode invalide -> indice non valide
    def test_periode_invalide(objet) :
        indice = IndiceBoursier("AAPL", "100ans")
        objet.assertEqual(indice.est_valide, False, "L'indice devrait etre invalide")
 
 
# Tests pour la methode obtenir_prix_actuel
class TestObtenirPrixActuel(unittest.TestCase) :
 
    # Preparer un indice avec des donnees de test
    def setUp(objet) :
        objet.indice = IndiceBoursier("AAPL")
        objet.indice.dates = ["2025-01-01", "2025-01-02", "2025-01-03"]
        objet.indice.prix = [100.0, 105.0, 110.0]
 
    # Retourne le dernier prix de la liste
    def test_dernier_prix(objet) :
        objet.assertEqual(objet.indice.obtenir_prix_actuel(), 110.0, "Le prix actuel devrait etre le dernier de la liste")
 
    # Retourne None si aucune donnee
    def test_aucune_donnee_retourne_none(objet) :
        indice_vide = IndiceBoursier("AAPL")
        resultat = indice_vide.obtenir_prix_actuel()
        objet.assertEqual(resultat is None, True, "Devrait retourner None quand aucune donnee")
 
 
# Tests pour la methode obtenir_variation
class TestObtenirVariation(unittest.TestCase) :
 
    # Preparer un indice sans remplir les prix
    def setUp(objet) :
        objet.indice = IndiceBoursier("AAPL")
        objet.indice.dates = ["2025-01-01", "2025-01-02", "2025-01-03"]
 
    # Variation positive (100 -> 110 = +10%)
    def test_variation_positive(objet) :
        objet.indice.prix = [100.0, 105.0, 110.0]
        objet.assertEqual(objet.indice.obtenir_variation(), 10.0, "La variation devrait etre 10%")
 
    # Variation negative (100 -> 80 = -20%)
    def test_variation_negative(objet) :
        objet.indice.prix = [100.0, 90.0, 80.0]
        objet.assertEqual(objet.indice.obtenir_variation(), -20.0, "La variation devrait etre -20%")
 
    # Variation nulle (100 -> 100 = 0%)
    def test_variation_nulle(objet) :
        objet.indice.prix = [100.0, 100.0, 100.0]
        objet.assertEqual(objet.indice.obtenir_variation(), 0.0, "La variation devrait etre 0%")
 
    # Prix de depart egal a zero -> retourne 0.0 (division par zero evitee)
    def test_prix_debut_zero(objet) :
        objet.indice.prix = [0.0, 50.0, 100.0]
        objet.assertEqual(objet.indice.obtenir_variation(), 0.0, "La variation devrait etre 0.0 pour eviter division par zero")
 
    # Retourne None si aucune donnee
    def test_aucune_donnee_retourne_none(objet) :
        indice_vide = IndiceBoursier("AAPL")
        resultat = indice_vide.obtenir_variation()
        objet.assertEqual(resultat is None, True, "Devrait retourner None quand aucune donnee")
 
 
# Tests pour la methode obtenir_statistiques
class TestObtenirStatistiques(unittest.TestCase) :
 
    # Preparer un indice avec des donnees connues
    def setUp(objet) :
        objet.indice = IndiceBoursier("AAPL")
        objet.indice.dates = ["2025-01-01", "2025-01-02", "2025-01-03",
                              "2025-01-04", "2025-01-05"]
        objet.indice.prix = [100.0, 102.0, 101.0, 103.0, 110.0]
 
    # Le dictionnaire doit contenir toutes les bonnes cles
    def test_cles_dictionnaire(objet) :
        stats = objet.indice.obtenir_statistiques()
        objet.assertEqual("min" in stats, True, "La cle 'min' devrait etre presente")
        objet.assertEqual("max" in stats, True, "La cle 'max' devrait etre presente")
        objet.assertEqual("moyenne" in stats, True, "La cle 'moyenne' devrait etre presente")
        objet.assertEqual("volatilite" in stats, True, "La cle 'volatilite' devrait etre presente")
        objet.assertEqual("variation" in stats, True, "La cle 'variation' devrait etre presente")
 
    # Min et Max
    def test_minimum_et_maximum(objet) :
        stats = objet.indice.obtenir_statistiques()
        objet.assertEqual(stats["min"], 100.0, "Le minimum devrait etre 100.0")
        objet.assertEqual(stats["max"], 110.0, "Le maximum devrait etre 110.0")
 
    # Moyenne : (100 + 102 + 101 + 103 + 110) / 5 = 103.2
    def test_moyenne(objet) :
        stats = objet.indice.obtenir_statistiques()
        objet.assertEqual(stats["moyenne"], 103.2, "La moyenne devrait etre 103.2")
 
    # Variation : 100 -> 110 = +10%
    def test_variation_dans_stats(objet) :
        stats = objet.indice.obtenir_statistiques()
        objet.assertEqual(stats["variation"], 10.0, "La variation devrait etre 10.0")
 
    # Retourne None si aucune donnee
    def test_aucune_donnee_retourne_none(objet) :
        indice_vide = IndiceBoursier("AAPL")
        resultat = indice_vide.obtenir_statistiques()
        objet.assertEqual(resultat is None, True, "Devrait retourner None quand aucune donnee")
 
 
# Tests pour la methode tracer_courbe
class TestTracerCourbe(unittest.TestCase) :
 
    # Preparer un indice avec des donnees de test
    def setUp(objet) :
        objet.indice = IndiceBoursier("AAPL")
        objet.indice.dates = ["2025-01-01", "2025-01-02", "2025-01-03"]
        objet.indice.prix = [100.0, 105.0, 110.0]
 
    # Une ligne doit etre tracee sur l'axe
    def test_ligne_tracee(objet) :
        figure, axe = plt.subplots()
        objet.indice.tracer_courbe(axe)
        objet.assertEqual(len(axe.lines), 1, "Une seule ligne devrait etre tracee")
        plt.close(figure)
 
    # Le titre doit contenir le symbole
    def test_titre_contient_symbole(objet) :
        figure, axe = plt.subplots()
        objet.indice.tracer_courbe(axe)
        objet.assertEqual("AAPL" in axe.get_title(), True, "Le titre devrait contenir le symbole AAPL")
        plt.close(figure)
 
    # Les etiquettes des axes doivent etre definies
    def test_etiquettes_axes(objet) :
        figure, axe = plt.subplots()
        objet.indice.tracer_courbe(axe)
        objet.assertEqual(axe.get_xlabel(), "Date")
        objet.assertEqual(axe.get_ylabel(), "Prix de cloture")
        plt.close(figure)
 
    # Aucune donnee : aucune ligne tracee
    def test_aucune_donnee(objet) :
        indice_vide = IndiceBoursier("AAPL")
        figure, axe = plt.subplots()
        indice_vide.tracer_courbe(axe)
        objet.assertEqual(len(axe.lines), 0, "Aucune ligne ne devrait etre tracee si aucune donnee")
        plt.close(figure)
 
 
# Tests pour la methode __str__
class TestStr(unittest.TestCase) :
 
    # L'affichage contient le symbole et la periode
    def test_contenu_str(objet) :
        indice = IndiceBoursier("AAPL", "1y")
        texte = str(indice)
        objet.assertEqual("AAPL" in texte, True, "Le texte devrait contenir AAPL")
        objet.assertEqual("1y" in texte, True, "Le texte devrait contenir 1y")
 
 
if __name__ == "__main__" :
    unittest.main(verbosity = 2)
 