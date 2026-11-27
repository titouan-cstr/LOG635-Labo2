# Partie 1 — Monde virtuel et scénario (`README_P1.md`)

Ce document décrit le travail de la **Personne 1** pour le Laboratoire 3 de LOG635 : représentation du manoir virtuel, entités officielles, navigation entre les pièces, associations dynamiques, chargement des faits initiaux et scénario d'enquête.

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

---

## 3. Associations dynamiques et suivi de l'état du monde ([world.py](world.py))

Au démarrage, le plateau ne contient **aucune relation codée en dur** entre les pièces, les armes et les personnes (Critère #5). Toutes les informations sont enregistrées dynamiquement à l'exécution selon les faits fournis par l'utilisateur ou le fichier de départ.

### Méthodes d'enregistrement (utilisées quand P3/P4 interprètent une réponse)

| Méthode | Rôle |
| --- | --- |
| `board.mark_room_visited(room=None, name_confirmed=True)` | Marque une pièce (courante par défaut) comme visitée |
| `board.place_weapon(weapon, room=None)` | Associe une arme à une pièce (déplace l'arme si elle était ailleurs) |
| `board.place_person(person, room=None, hour=None)` | Sans `hour` : position actuelle ; avec `hour` (`0..24`) : passage horodaté |
| `board.record_clue(clue, room=None)` | Enregistre un indice observé dans la pièce |
| `board.set_person_status(person, status, hour=None)` | Enregistre `"mort"` (définit la victime et l'heure du crime) ou `"vivant"` |
| `board.reset_associations()` | Remet le plateau à zéro pour lancer une nouvelle enquête |

### Méthodes d'inspection (utilisées par P3 pour générer des questions et P4 pour afficher l'état)

| Méthode | Retour |
| --- | --- |
| `board.get_room_state(room=None)` | État complet de la pièce (`visited`, `weapons`, `persons`, `sightings`, `clues`) |
| `board.get_weapons_in_room(room=None)` | Armes trouvées dans la pièce |
| `board.get_persons_in_room(room=None)` | Personnes actuellement dans la pièce |
| `board.get_person_timeline(person)` | Historique trié `[{"room": ..., "hour": ...}]` d'une personne |
| `board.get_unvisited_rooms()` | Pièces pas encore visitées |
| `board.get_unlocated_weapons()` | Armes dont la pièce est encore inconnue |
| `board.get_unlocated_persons()` | Personnes sans position ni passage connu |
| `board.get_summary()` | Snapshot global de l'enquête |

Exemple d'utilisation intégrée :

```python
from world import ManorBoard

board = ManorBoard()
board.move_to("Bureau")
board.mark_room_visited()
board.set_person_status("Black", "mort", hour=21)
board.place_person("Black", room="Bureau")
board.place_weapon("Corde", room="Cuisine")
board.place_person("Moutarde", room="Cuisine", hour=21)

print(board.get_unlocated_weapons())  # ['Poignard', 'Revolver', 'Chandelier', 'Cle', 'Matraque']
print(board.get_person_timeline("Moutarde"))  # [{'room': 'Cuisine', 'hour': 21}]
```

---

## 4. Vérification et tests unitaires

Lancer les tests de la partie 1 depuis le dossier `LABO3/` :

```bash
python3 -m unittest discover -s tests -v
```

---

*Prochaines étapes : fichier `faits_initiaux.txt` et chargeur au démarrage (Étape 3), puis conception complète du scénario d'enquête (Étape 4).*
