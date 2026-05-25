# Importation de VOTRE package comme une librairie standard
from logistock import optimalSorting, GestionnairePile, Configuration

# --- 1. DÉFINITION DU PROBLÈME (Données du client) ---
print("--- 1. CALCUL DE L'OPTIMISATION ---")
produits = ["Ciment", "Sable", "Gravier"]
quantites = {
    "Ciment": 5,
    "Sable": 10,
    "Gravier": 3
}
# Fréquence de sortie (λ)
frequences = {
    "Ciment": 0.2,  # Sort peu souvent
    "Sable": 0.8,   # Sort très souvent
    "Gravier": 0.1  # Sort rarement
}

# --- 2. APPEL A L'INTELLIGENCE (API) ---
# L'utilisateur n'a pas besoin de savoir ce qu'est un MCTS ou un noeud.
# Il appelle juste "optimalSorting".
pile_optimale, cout_prevu = optimalSorting(
    produits=produits,
    effectifs=quantites,
    intensites=frequences,
    hauteur_max=20,
    iterations=2000, # Il décide du temps de réflexion de l'IA
)

print(f"✅ Coût théorique minimal : {cout_prevu:.2f} mouvements")
print(f"✅ Ordre recommandé (Haut -> Bas) : {pile_optimale}")

# --- 3. MISE EN PRATIQUE (Gestionnaire) ---
print("\n--- 2. SIMULATION EN ENTREPÔT ---")

# Initialisation du Jumeau Numérique
config = Configuration()
entrepot = GestionnairePile(config)

# Le logisticien range les sacs selon le plan de l'IA
# Note : L'IA donne l'ordre du Sommet vers le Bas.
# Pour remplir une pile vide, on empile du Sol vers le Sommet (donc on inverse).
entrepot.afficher_pile()

# Visualisation
entrepot.afficher_pile()

# Simulation d'un client qui arrive
print("Clients à l'approche...")
entrepot.retirer_sac_specifique("Sable") # Devrait être facile car le sable est fréquent
entrepot.retirer_sac_specifique("Gravier") # Devrait être coûteux car le gravier est rare