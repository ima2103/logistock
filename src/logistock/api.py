from .configuration import Configuration
from .moteur_mcts import MCTS_Optimiseur


def optimalSorting(produits, effectifs, intensites, hauteur_max, iterations=5000):
    """
    Fonction principale demandée :
    Prend les types de produits, leurs quantités et leurs intensités (λ).
    Retourne le rangement global (du sommet vers le bas) le plus efficace.
    """
    # 1. Configuration et chargement des intensités
    config = Configuration()
    config.hauteur_max = hauteur_max
    config.intensites = {p: max(float(v), 0.1) for p, v in intensites.items()}
    # 2. Préparation de la liste de tous les sacs à ranger
    sacs_a_ranger = []
    for p in produits:
        qty = int(effectifs.get(p, 0))
        sacs_a_ranger.extend([p] * qty)

    # 3. Initialisation du moteur MCTS
    ia = MCTS_Optimiseur(config)

    # On tente de charger l'intelligence précédente si elle existe
    ia.charger_arbre_depuis_json()

    # 4. Lancement de la recherche de la meilleure combinaison
    # L'IA va tester différentes combinaisons de rangement pour trouver
    # celle qui minimise l'espérance de coût total d'évidage.
    meilleure_combinaison, score_evidage = ia.rechercher_meilleur_rangement(sacs_a_ranger, n_simulations=iterations)

    # Sauvegarde dans le JSON via Configuration
    config.sauvegarder_donnees_specifiques("dernier_cout_evidage", score_evidage)
    config.sauvegarder_donnees_specifiques("rangement_optimal_actuel", meilleure_combinaison)
    # 5. Sauvegarde de l'arbre pour la prochaine fois (continuité)
    ia.sauvegarder_arbre_dans_json()

    return meilleure_combinaison, score_evidage # Retourne l'ordre Sommet -> Bas