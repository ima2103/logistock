import json
import os
import pandas as pd
from datetime import datetime


class Configuration:
    """
    Gère la persistance des données dans un format JSON structuré.
    Stocke l'inventaire, les intensités de demande, les paramètres système
    et l'état de l'arbre MCTS (mémoire à long terme).
    """

    def __init__(self, fichier_memoire="memoire_logistique.json"):
        self.fichier_memoire = fichier_memoire
        # Paramètres par défaut
        self.hauteur_max = 20
        self.intensites = {}

    def _lire_json(self):
        """Lit le fichier JSON et gère les erreurs de lecture."""
        if os.path.exists(self.fichier_memoire):
            try:
                with open(self.fichier_memoire, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, ValueError):
                return {}
        return {}

    def _ecrire_json(self, donnees):
        """Écrit les données dans le JSON avec une indentation pour la lisibilité humaine."""
        donnees["derniere_mise_a_jour"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.fichier_memoire, 'w', encoding='utf-8') as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)

    def sauvegarder_inventaire(self, df):
        """Sauvegarde l'inventaire (DataFrame) et les intensités extraites."""
        donnees = self._lire_json()

        # Mise à jour des paramètres et de l'inventaire
        donnees["parametres"] = {"hauteur_max": self.hauteur_max}
        donnees["inventaire"] = df.to_dict(orient="records")

        # Extraction et stockage propre des intensités pour la machine
        intensites = {}
        for _, row in df.iterrows():
            intensites[row["Produit"]] = row["Intensité (λ)"]
        donnees["intensites"] = intensites

        self._ecrire_json(donnees)


    def charger_inventaire(self):
        donnees = self._lire_json()
        liste_inv = donnees.get("inventaire", [])

        colonnes = ["Produit", "Quantité", "Intensité (λ)", "Probabilité (%)"]

        if liste_inv:
            df = pd.DataFrame(liste_inv)
            # FORCE LE TYPE NUMÉRIQUE ICI
            if "Quantité" in df.columns:
                df["Quantité"] = pd.to_numeric(df["Quantité"], errors='coerce').fillna(0).astype(int)
            if "Intensité (λ)" in df.columns:
                df["Intensité (λ)"] = pd.to_numeric(df["Intensité (λ)"], errors='coerce').fillna(0.1)
            if "Probabilité (%)" in df.columns:
                df["Probabilité (%)"] = pd.to_numeric(df["Probabilité (%)"], errors='coerce').fillna(0.0)
            return df
        else:
            return pd.DataFrame(columns=colonnes)
    def sauvegarder_donnees_specifiques(self, cle, valeur):
        """
        Permet de sauvegarder des blocs spécifiques comme
        'rangement_optimal_actuel' ou 'intelligence_arbre' (MCTS).
        """
        donnees = self._lire_json()
        donnees[cle] = valeur
        self._ecrire_json(donnees)

    def charger_donnees_specifiques(self, cle):
        """Récupère une donnée spécifique (ex: l'arbre MCTS pour continuer le calcul)."""
        donnees = self._lire_json()
        return donnees.get(cle, None)

    def rafraichir_parametres(self):
        """Charge les paramètres globaux depuis le fichier vers l'instance."""
        donnees = self._lire_json()
        params = donnees.get("parametres", {})
        self.hauteur_max = params.get("hauteur_max", 20)
        self.intensites = donnees.get("intensites", {})