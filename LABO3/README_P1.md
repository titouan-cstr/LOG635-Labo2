# Partie 1 — Monde virtuel et scénario (`README_P1.md`)

Ce document décrit le travail de la **Personne 1** pour le Laboratoire 3 de LOG635 : représentation du manoir virtuel, entités officielles, navigation entre les pièces, chargement des faits initiaux et scénario d'enquête.

---

## 1. Entités officielles du monde ([constants.py](constants.py))

Afin d'éviter toute erreur de correspondance entre la base de connaissances FOL (**P2**), les grammaires NLTK (**P3**) et les entrées utilisateur (**P4**), tous les identifiants logiques sont **sans accents ni espaces** :

| Catégorie | Identifiants FOL (`constants.py`) | Nombre |
| --- | --- | --- |
| **Victime (`VICTIM`)** | `Black` | 1 |
| **Suspects (`PERSONS`)** | `Moutarde`, `Rose`, `Violet`, `Pervenche`, `Olive`, `Leblanc` | 6 |
| **Armes (`WEAPONS`)** | `Corde`, `Poignard`, `Revolver`, `Chandelier`, `Cle`, `Matraque` | 6 |
| **Pièces (`ROOMS`, ordonnées)** | `Cuisine`, `Salon`, `Bureau`, `Chambre`, `Cave`, `Veranda` | 6 |

> **Pour P2 et P3 :** `ALL_PERSONS` regroupe `PERSONS + [VICTIM]`, et `DISPLAY_NAMES` fournit les libellés lisibles en français (ex. `"Moutarde"` → `"Colonel Moutarde"`, `"Cle"` → `"clé anglaise"`).

---

## 2. Plateau virtuel et navigation ([world.py](world.py))

La classe `ManorBoard` modélise le manoir virtuel sous forme d'une liste ordonnée de 6 pièces :

```text
[0] Cuisine  <-->  [1] Salon  <-->  [2] Bureau  <-->  [3] Chambre  <-->  [4] Cave  <-->  [5] Veranda
```

### API de navigation pour P4 (touches fléchées)

| Touche clavier | Méthode `ManorBoard` | Comportement |
| --- | --- | --- |
| `→` (droite) | `board.next_room()` | Passe à la pièce suivante (boucle sur `Cuisine` par défaut) |
| `←` (gauche) | `board.prev_room()` | Passe à la pièce précédente (boucle sur `Veranda` par défaut) |
| `↑` (haut) | `board.first_room()` | Revient à la première pièce (`Cuisine`) |
| `↓` (bas) | `board.last_room()` | Va à la dernière pièce (`Veranda`) |
| Position actuelle | `board.current_room()` | Retourne le nom de la pièce courante |
| Infos d'affichage | `board.get_navigation_info()` | Retourne `{current_room, index, total, prev_room, next_room}` |

Exemple d'utilisation :

```python
from world import ManorBoard

board = ManorBoard()          # Démarre dans "Cuisine"
print(board.current_room())   # "Cuisine"
print(board.next_room())      # "Salon"
print(board.last_room())      # "Veranda"
```

---

## 3. Vérification et tests unitaires

Lancer les tests de la partie 1 depuis le dossier `LABO3/` :

```bash
python3 -m unittest discover -s tests -v
```

---

*Prochaines étapes : associations dynamiques entité/pièce/heure (Étape 2), chargement de `faits_initiaux.txt` (Étape 3) et scénario complet d'enquête (Étape 4).*
