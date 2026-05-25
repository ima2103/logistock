"""
groupe4.py – Adaptateur vers le moteur MCTS du Groupe 4 (F2.py)
================================================================
Fait le pont entre notre interface (produits / effectifs / intensites)
et l'interface du Groupe 4 (inventory / lambdas / min_iterations / epsilon).

Différences clés entre les deux moteurs :
  • G4 : stack = [sommet … bas], cases vides = 'X'
  • Nous : arrangement = list[str] Sommet → Bas (sans 'X')
  • G4 converge via epsilon ; nous via n_simulations fixes
  • G4 expose min_iterations + epsilon comme paramètres utilisateur
"""

from .groupe4_engine import run_mcts


def groupe4_rangement(produits, effectifs, intensites, hauteur_max,
                      min_iterations=300, epsilon=0.01):
    """
    Appelle le moteur MCTS du Groupe 4 et retourne le résultat
    dans le format attendu par notre application.

    Paramètres
    ----------
    produits       : list[str]   — liste des types de produits
    effectifs      : dict        — {produit: quantité}
    intensites     : dict        — {produit: lambda (intensité)}
    hauteur_max    : int         — hauteur maximale de la pile (non utilisé
                                   par G4 car la taille = somme des effectifs)
    min_iterations : int         — nombre minimum d'itérations avant test
                                   de convergence (paramètre G4)
    epsilon        : float       — seuil de convergence (paramètre G4)

    Retourne
    --------
    (arrangement: list[str], score: float)
        arrangement = ordre Sommet → Bas (sans cases vides)
        score       = espérance de coût d'évidage estimée par G4
    """
    # ── Conversion vers l'interface Groupe 4 ─────────────────────────────────
    inventory = {p: int(effectifs.get(p, 0)) for p in produits
                 if int(effectifs.get(p, 0)) > 0}
    lambdas   = {p: float(intensites.get(p, 1.0)) for p in inventory}

    if not inventory:
        return [], 0.0

    # ── Lancement du moteur G4 ────────────────────────────────────────────────
    root_node, final_iters = run_mcts(inventory, min_iterations, epsilon, lambdas)

    # ── Extraction du meilleur arrangement ───────────────────────────────────
    # On parcourt l'arbre pour trouver les nœuds « pile complète » :
    # c'est le premier nœud en mode SORTIE dont le parent est en mode REMPLISSAGE.
    full_piles = {}

    def _find_full(node):
        if (node.state.mode == "SORTIE"
                and node.parent is not None
                and node.parent.state.mode == "REMPLISSAGE"):
            key = node.state.stack
            if key not in full_piles:
                full_piles[key] = node
        for child in node.children.values():
            _find_full(child)

    _find_full(root_node)

    if not full_piles:
        # Aucun nœud complet trouvé (trop peu d'itérations) → fallback racine
        raw_stack = list(root_node.state.stack)
        arrangement = [s for s in raw_stack if s != 'X']
        score = root_node.expected_cost
        return arrangement, score

    # Trier par coût croissant et prendre le meilleur
    best_node = sorted(full_piles.values(), key=lambda n: n.expected_cost)[0]

    # Leur stack : index 0 = sommet, dernier index = bas, 'X' = vide
    # → on filtre les 'X' et on obtient directement Sommet → Bas
    arrangement = [s for s in best_node.state.stack if s != 'X']
    score       = best_node.expected_cost

    return arrangement, score
