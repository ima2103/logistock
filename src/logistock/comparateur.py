"""
comparateur.py – Calcul et comparaison des scores de rangement
"""


def calculer_score_arrangement(arrangement, intensites):
    """
    Calcule le score d'évidage théorique d'un arrangement donné.

    Paramètres
    ----------
    arrangement : list[str]
        Ordre des sacs Sommet → Bas.
    intensites : dict
        Intensité λ par produit.

    Retourne
    --------
    (score_evidage: float, nb_manipulations: int)
    """
    # pile[0] = bas, pile[-1] = sommet
    pile = list(reversed(arrangement))
    cout_total = 0.0
    manipulations = 0

    while pile:
        # Localiser l'instance la plus haute (dernier index) de chaque TYPE
        top_items = {}
        for idx, prod in enumerate(pile):
            top_items[prod] = idx  # on garde le dernier = le plus haut

        somme_lambda = sum(intensites.get(p, 1.0) for p in top_items)
        if somme_lambda == 0:
            somme_lambda = 1.0

        for prod, idx_sommet in top_items.items():
            pi = intensites.get(prod, 1.0) / somme_lambda
            k = len(pile) - 1 - idx_sommet   # sacs au-dessus
            ci = 1 + 2 * k
            cout_total += pi * ci

        # Retire le sac au sommet pour avancer
        pile.pop()
        manipulations += 1

    return cout_total, manipulations


def calculer_cout_retrait(pile, sac_id):
    """
    Coût de retrait d'un sac précis dans la pile.
    pile = [bas, ..., sommet]  (convention GestionnairePile)
    Retourne 1 + 2*k  (k = nombre de sacs au-dessus du sac cible)
    """
    if sac_id not in pile:
        return None
    idx = pile.index(sac_id)      # pile.index renvoie la 1re occurrence
    k = len(pile) - 1 - idx
    return 1 + 2 * k


def comparer_rangements(resultats: dict):
    """
    Classe les rangements du meilleur au moins bon (score évidage croissant).

    Paramètres
    ----------
    resultats : dict
        {nom_methode: {"score": float, "manips": int, "arrangement": list}}

    Retourne
    --------
    list of (nom, dict) trié par score croissant.
    """
    return sorted(resultats.items(), key=lambda x: x[1]["score"])
