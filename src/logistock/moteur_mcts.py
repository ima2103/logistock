import math
import random
import copy
import time


class Noeud:
    def __init__(self, etat_pile, sacs_restants, parent=None, action=None):
        self.etat_pile = etat_pile  # Liste des sacs (ex: ["Sable", "Ciment"])
        self.sacs_restants = sacs_restants  # Sacs qu'il reste à poser
        self.parent = parent
        self.action = action
        self.enfants = []
        self.n = 0
        self.somme_couts_evidage = 0

    def est_developpe(self, nb_piles):
        return len(self.enfants) == nb_piles

    def calculer_ucb(self, N_parent):
        """ Formule UCB1 adaptée pour la MINIMISATION des coûts. """
        if self.n == 0:
            return float('inf')  # Priorité absolue à l'exploration

        # On cherche à minimiser le coût moyen
        moyenne = self.somme_couts_evidage / self.n
        # Le terme d'exploration est soustrait car on minimise
        exploration = 2 * math.sqrt(math.log(N_parent) / self.n)
        return moyenne - exploration


class MCTS_Optimiseur:
    def __init__(self, config):
        self.config = config
        self.racine = None

    def rechercher_meilleur_rangement(self, tous_les_sacs, n_simulations=1000):
        self.racine = Noeud([], tous_les_sacs)

        for _ in range(n_simulations):
            # 1. Sélection & Développement
            noeud = self._selection_et_developpement(self.racine)

            # 2. Simulation (Rollout) améliorée
            cout_estime = self._simulation_evidage_total(noeud.etat_pile, noeud.sacs_restants)

            # 3. Rétropropagation
            self._retropropagation(noeud, cout_estime)

        return self._extraire_meilleure_pile()

    def _selection_et_developpement(self, noeud):
        while noeud.sacs_restants:
            # On identifie les TYPES uniques de sacs restants (ex: 'A', 'B')
            types_possibles = list(set(noeud.sacs_restants))

            if len(noeud.enfants) < len(types_possibles):
                # On développe un nouveau nœud pour un type non testé
                deja_testes = [e.action for e in noeud.enfants]
                candidats = [t for t in types_possibles if t not in deja_testes]

                if not candidats:
                    # Cas rare de repli
                    break

                choix = random.choice(candidats)
                nouvelle_pile = noeud.etat_pile + [choix]
                nouveaux_restants = list(noeud.sacs_restants)
                nouveaux_restants.remove(choix)

                nouvel_enfant = Noeud(nouvelle_pile, nouveaux_restants, parent=noeud, action=choix)
                noeud.enfants.append(nouvel_enfant)
                return nouvel_enfant
            else:
                # Tous les types sont développés, on descend vers le meilleur UCB (Minimisation)
                noeud = min(noeud.enfants, key=lambda c: c.calculer_ucb(noeud.n))
        return noeud

    def _simulation_evidage_total(self, pile_partielle, sacs_restants):
        """
        Simule le coût total d'évidage en considérant les probabilités par TYPE.
        """
        # Génération d'une pile complète aléatoire pour l'évaluation
        pile_complete = pile_partielle + random.sample(sacs_restants, len(sacs_restants))
        temp_pile = list(pile_complete)
        cout_total_simule = 0

        while temp_pile:
            # 1. Identifier pour chaque TYPE l'emplacement de son instance la plus haute
            # (Celle qui coûte le moins cher à sortir)
            top_items = {}  # Map: Type -> Index dans la pile
            for idx, prod in enumerate(temp_pile):
                top_items[prod] = idx  # On écrase pour garder le dernier index (le sommet)

            # 2. Calculer la somme des intensités des types PRÉSENTS
            somme_lambda = 0
            poids_demande = {}
            for prod in top_items.keys():
                # On utilise 1.0 par défaut si l'intensité n'est pas trouvée
                w = self.config.intensites.get(prod, 1.0)
                poids_demande[prod] = w
                somme_lambda += w

            if somme_lambda == 0: somme_lambda = 1  # Sécurité

            # 3. Calculer l'espérance pour cette étape
            esperance_etape = 0
            indices_candidats = []
            probs_candidats = []

            for prod, idx_sommet in top_items.items():
                # Probabilité que le client veuille ce TYPE de produit
                pi = poids_demande[prod] / somme_lambda

                # Coût : 1 (retrait) + 2 * k (obstacles au-dessus)
                # Sommet pile = index (len-1). Donc k = (len-1) - index.
                k = len(temp_pile) - 1 - idx_sommet
                ci = 1 + 2 * k

                esperance_etape += pi * ci

                # Préparation pour le tirage aléatoire de la transition
                indices_candidats.append(idx_sommet)
                probs_candidats.append(pi)

            cout_total_simule += esperance_etape

            # 4. Transition : On retire réellement un objet pour avancer dans la simulation
            # On tire au sort selon les probabilités de demande
            idx_a_retirer = random.choices(indices_candidats, weights=probs_candidats, k=1)[0]
            temp_pile.pop(idx_a_retirer)

        return cout_total_simule

    def _retropropagation(self, noeud, cout):
        while noeud:
            noeud.n += 1
            noeud.somme_couts_evidage += cout
            noeud = noeud.parent

    def _extraire_meilleure_pile(self):
        # On redescend l'arbre en prenant les nœuds les plus visités (robustesse)
        chemin = []
        courant = self.racine
        while courant.enfants:
            courant = max(courant.enfants, key=lambda c: c.n)
            chemin.append(courant.action)

        score_final = courant.somme_couts_evidage / courant.n if courant.n > 0 else 0
        # L'arbre est construit du bas vers le haut (action 1 = sol)
        # On retourne [Sommet, ..., Sol] pour l'affichage standard
        return chemin[::-1], score_final

    def sauvegarder_arbre_dans_json(self):
        if self.racine is None: return

        def noeud_vers_dict(noeud):
            return {
                "etat": noeud.etat_pile,
                "n": noeud.n,
                "somme_couts": noeud.somme_couts_evidage,
                "sacs_restants": noeud.sacs_restants,
                "action": noeud.action,
                "enfants": [noeud_vers_dict(e) for e in noeud.enfants]
            }

        arbre_dict = noeud_vers_dict(self.racine)
        self.config.sauvegarder_donnees_specifiques("arbre_mcts", arbre_dict)

    def charger_arbre_depuis_json(self):
        donnees = self.config.charger_donnees_specifiques("arbre_mcts")
        if not donnees: return

        def dict_vers_noeud(d, parent=None):
            n = Noeud(d["etat"], d["sacs_restants"], parent=parent, action=d["action"])
            n.n = d["n"]
            n.somme_couts_evidage = d["somme_couts"]
            n.enfants = [dict_vers_noeud(e, parent=n) for e in d["enfants"]]
            return n

        self.racine = dict_vers_noeud(donnees)