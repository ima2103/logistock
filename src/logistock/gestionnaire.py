class GestionnairePile:
    def __init__(self, config):
        """
        Initialise l'entrepôt avec une pile unique.
        Config : instance de la classe Configuration pour connaître la hauteur max.
        """
        self.config = config
        # Une seule liste représentant l'unique pile de sacs
        self.pile = []

    def ajouter_sac(self, sac_id):
        """
        Ajoute un sac au sommet de la pile si l'espace le permet.
        """
        if not self.est_pleine():
            self.pile.append(sac_id)
            print(f"📦 Sac '{sac_id}' ajouté au sommet.")
            return True
        else:
            print(f"⚠️ Alerte : La pile est pleine ({self.config.hauteur_max} sacs) !")
            return False

    def retirer_sac_sommet(self):
        """
        Retire le sac qui se trouve tout en haut (LIFO - Last In First Out).
        """
        if not self.est_vide():
            sac_retire = self.pile.pop()
            print(f"📤 Sac '{sac_retire}' retiré du sommet.")
            return sac_retire
        else:
            print("⚠️ Erreur : La pile est déjà vide.")
            return None

    def retirer_sac_specifique(self, sac_id):
        """
        Simule le retrait d'un sac n'importe où dans la pile.
        Calcule la pénibilité réelle (nombre de sacs à déplacer).
        """
        if sac_id not in self.pile:
            print(f"❌ Le sac '{sac_id}' n'est pas dans la pile.")
            return None

        # k = nombre de sacs au-dessus du sac cible
        index_sac = self.pile.index(sac_id)
        k = len(self.pile) - 1 - index_sac

        # On retire le sac (en réalité, on déplace les k sacs au-dessus)
        self.pile.pop(index_sac)

        cout_reel = 1 + 2 * k
        print(f"✅ Sac '{sac_id}' extrait. Pénibilité réelle de l'opération : {cout_reel}")
        return cout_reel

    def est_pleine(self):
        """ Vérifie si la limite de hauteur est atteinte """
        return len(self.pile) >= self.config.hauteur_max

    def est_vide(self):
        """ Vérifie s'il n'y a plus de sacs """
        return len(self.pile) == 0

    def obtenir_etat(self):
        """ Retourne l'état actuel sous forme de liste de listes pour le MCTS """
        # Le MCTS attend une liste de piles, ici on en a une seule
        return [list(self.pile)]

    def afficher_pile(self):
        """ Affiche visuellement la pile (du haut vers le bas) """
        print("\n--- ÉTAT DE LA PILE ---")
        if self.est_vide():
            print("[ Vide ]")
        else:
            for i, sac in enumerate(reversed(self.pile)):
                print(f"| {sac} |" + (" (Sommet)" if i == 0 else ""))
        print("-----------------------\n")