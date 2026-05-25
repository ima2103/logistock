
---

# 🏗️ Logistock : Organisez votre stock sans effort

**Vous en avez assez de déplacer 10 sacs pour atteindre celui qui est tout en bas ?** Logistock est une intelligence artificielle simple qui calcule pour vous l'ordre de rangement idéal de vos produits stockés en pile (les uns sur les autres).

---

## ❓ C'est quoi "l'Évidage" ?

C'est le fait de vider votre pile au fur et à mesure des ventes.

* Si vous vendez souvent du **Ciment** et qu'il est au fond de la pile, vous allez vous épuiser à déplacer tout ce qui est au-dessus pour le sortir.
* **Le but de Logistock :** Placer les produits les plus demandés au sommet pour que vous n'ayez presque jamais à déplacer de sacs inutiles.

---

## 🚀 Installation rapide

Ouvrez votre terminal et tapez :

```bash
pip install logistock==0.1.3

```

---

## 🛠️ Comment l'utiliser ? 

C'est très simple. Imaginez que vous avez 3 types de sacs à ranger. Voici comment demander à l'IA de vous aider :

```python
from logistock.api import optimalSorting

# 1. Listez vos produits
mes_produits = ["Ciment", "Sable", "Gravier"]

# 2. Indiquez les quantités que vous avez en stock
mes_quantites = {"Ciment": 10, "Sable": 5, "Gravier": 5}

# 3. Donnez une note d'importance (Intensité)
# Plus le chiffre est gros, plus vous vendez ce produit souvent !
mes_ventes = {"Ciment": 5.0, "Sable": 1.0, "Gravier": 0.5}

# 4. L'IA calcule le meilleur rangement
# On lui demande de tester 5000 combinaisons pour être sûr
plan, score = optimalSorting(
    produits=mes_produits,
    effectifs=mes_quantites,
    intensites=mes_ventes,
    hauteur_max=20,
    iterations=5000
)

print("Voici l'ordre de rangement du HAUT vers le BAS :")
print(plan)
print(f"Score de fatigue prévu : {score:.2f} (Plus c'est bas, mieux c'est !)")

```

---

## 🧠 Comment ça marche (Simplement) ?

L'algorithme utilise une méthode appelée **MCTS** (Recherche Arborescente de Monte Carlo). C'est la même technologie que les IA qui jouent aux échecs !

1. **Il imagine des milliers de piles** différentes.
2. **Il simule la vente** de chaque sac selon vos habitudes (vos scores d'importance).
3. **Il calcule votre fatigue** (le nombre de sacs que vous avez dû déplacer pour rien).
4. **Il vous donne la solution** qui vous fatigue le moins.

---

## 📂 Contenu du package

* **`optimalSorting`** : La fonction magique qui fait tout le travail.
* **Mémoire Intelligente** : Le package crée un petit fichier `memoire_logistique.json`. Il permet à l'IA de se souvenir de ses calculs précédents pour devenir plus rapide et plus précise à chaque fois.
* **Rapports PDF** : Compatible avec la création de fiches de rangement prêtes à imprimer.

---

## ⚙️ Configuration Technique (`pyproject.toml`)

Si vous développez avec ce package, voici la configuration recommandée :

```toml
[project]
name = "logistock"
version = "0.1.1"
dependencies = [
    "pandas",
    "fpdf2",
]

```

---

## 📄 Licence

Ce projet est libre d'utilisation sous licence **MIT**.

---


