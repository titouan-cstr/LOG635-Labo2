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

## 4. Faits initiaux et chargement au démarrage ([faits_initiaux.txt](faits_initiaux.txt))

Au lancement du programme, les faits de départ sont lus depuis `faits_initiaux.txt` (Critère #1.1) afin qu'aucune situation ne soit figée dans le code Python :

- Une phrase simple en français par ligne (format compatible avec les grammaires `.fcfg` de **P3**).
- Les lignes vides et les lignes commençant par `#` sont ignorées.
- Contenu de départ : uniquement la découverte de la victime (`Black est mort`, `Black est mort à 21h`, `Black est dans le bureau`) et le statut vivant des 6 suspects. Le reste (armes, déplacements, indices) est recueilli dynamiquement pendant l'enquête.

### Fonctions utilitaires pour P3 et P4 ([world.py](world.py))

| Fonction | Rôle |
| --- | --- |
| `load_initial_facts(filepath=INITIAL_FACTS_FILE)` | Lit le fichier texte UTF-8 et retourne `list[str]` des faits propres |
| `apply_fact_to_board(board, fact)` | Synchronise une phrase française simple avec l'état de `ManorBoard` |
| `apply_initial_facts(board, filepath=INITIAL_FACTS_FILE)` | Charge le fichier, met à jour `board` et retourne la liste des phrases pour **P3/P2** |

Exemple d'utilisation au démarrage dans `main.py` (**P4**) :

```python
from world import ManorBoard, apply_initial_facts

board = ManorBoard()
initial_facts = apply_initial_facts(board)  # Met à jour board et retourne les phrases françaises
# P3 peut ensuite convertir chaque phrase de `initial_facts` en clause FOL pour P2
```

---

## 5. Scénario complet d'enquête (Critère #7 & Rapport)

> **Important (Critère #5) :** Ce scénario n'est **pas codé en dur** dans `world.py`. Il sert de trame de référence pour la démo, les tests d'intégration avec **P2 / P3 / P4** et la section « Scénario et faits » du rapport PDF.

### 5.1 Résumé et solution attendue (QUI / COMMENT / OÙ / QUAND)

| Élément | Valeur | Justification logique |
| --- | --- | --- |
| **Victime** | `Black` | Fourni dans `faits_initiaux.txt` (`Black est mort`) |
| **QUI (Coupable)** | `Moutarde` | Présent dans le `Bureau` à `21h` et retrouvé à `22h` dans la `Cave` avec la `Corde` |
| **COMMENT (Arme)** | `Corde` | `Black` présente des marques au cou (`MarqueCou(Black)`), incompatibles avec le `Poignard` |
| **OÙ (Lieu)** | `Bureau` | Corps de `Black` retrouvé dans le `Bureau` |
| **QUAND (Heure)** | `21h` | Heure estimée du décès (`Black est mort à 21h`) |

**Phrase finale attendue (Critère #9) :**
> `Colonel Moutarde a tué Monsieur Black dans le bureau avec une corde à 21h`

---

### 5.2 Répartition des armes et fausses pistes dans les 6 pièces

| Pièce (ordre) | Arme découverte | Indice / rôle dans l'enquête |
| --- | --- | --- |
| `Cuisine` | `Chandelier` | Arme innocente (pas de trace de coup) |
| `Salon` | `Revolver` | Arme innocente (aucun coup de feu entendu) |
| `Bureau` | `Poignard` | **Fausse piste n°1 :** arme trouvée sur la scène du crime, mais aucune blessure par lame (`MarqueCou(Black)` oriente vers la `Corde`) |
| `Chambre` | `Matraque` | Arme innocente |
| `Cave` | `Corde` | **Arme du crime :** cachée au sous-sol après l'étranglement |
| `Veranda` | `Cle` | Arme innocente (clé anglaise de jardinage) |

---

### 5.3 Chronologie des suspects et alibis

| Suspect | Statut | À `21h` (heure du crime) | À `22h` (`UneHeureApresCrime`) | Conclusion |
| --- | --- | --- | --- | --- |
| `Moutarde` | Vivant | `Bureau` (avec `Black`, sans témoin) | `Cave` (pièce de la `Corde`) | **Coupable / Suspect** |
| `Pervenche` | Vivante | `Salon` (avec `Rose`, alibi mutuel) | `Bureau` (découvre le corps + `Poignard`) | **Fausse piste n°2** — Innocente |
| `Olive` | Vivant | `Veranda` (seul, dispute avec `Black` à `20h`) | `Veranda` (arme sur place : `Cle`) | **Fausse piste n°3** — Innocent |
| `Rose` | Vivante | `Salon` (avec `Pervenche`) | `Salon` (arme sur place : `Revolver`) | Innocente |
| `Violet` | Vivant | `Cuisine` | `Cuisine` (arme sur place : `Chandelier`) | Innocent |
| `Leblanc` | Vivante | `Chambre` | `Chambre` (arme sur place : `Matraque`) | Innocente |

---

### 5.4 Déroulement type des interactions (guide pour P3 et P4)

1. **Démarrage (Canal 1 — fichier texte)** : chargement de `faits_initiaux.txt` via `apply_initial_facts(board)`.
2. **Navigation par les flèches (`→ ← ↑ ↓`) et questions/réponses (Canaux 2, 3, 4)** :
   - **Dans `Cuisine`** : `Le chandelier est dans la cuisine`, `Violet était dans la cuisine à 22h`.
   - **Dans `Salon`** : `Le revolver est dans le salon`, `Rose était dans le salon à 22h`.
   - **Dans `Bureau`** (scène du crime) : `Black a des marques au cou` *(ex. réponse vocale, Critère #2.1)*, `Le poignard est dans le bureau`, `Pervenche était dans le bureau à 22h` *(fausse piste, mais innocente car `Poignard != Corde`)*.
   - **Dans `Chambre`** : `La matraque est dans la chambre`, `Leblanc était dans la chambre à 22h`.
   - **Dans `Cave`** : `La corde est dans la cave`, question oui/non avec touche **`1`** (`Oui`, Critère #3.2) pour confirmer `Moutarde était dans la cave à 22h`.
   - **Dans `Veranda`** : `La clé est dans la véranda`, `Olive était dans la véranda à 22h`.
3. **Déduction finale (P2 + annonce TTS P4, Critère #2.2 & #9)** :
   - `PieceCrime = Bureau`, `ArmeCrime = Corde`, `Victime = Black`, `HeureCrime = 21`, `Suspect = Moutarde`, `Innocents = [Black, Violet, Rose, Pervenche, Leblanc, Olive]`.

---

### 5.5 Notes d'interface importantes pour l'équipe (P2 / P3 / P4)

- **Attention pour P2 ([inference_engine.py](inference_engine.py)) :**
  1. La ligne 109 contient `Piece_Arme(y, x)` au lieu de `Arme_Piece(y, x)`.
  2. La règle `PieceCrime(x) & Arme(y) & Arme_Piece(y, x) ==> ArmeCrime(y)` désignerait à tort le `Poignard` (fausse piste présente dans le `Bureau`) si elle n'est pas conditionnée par l'indice médico-légal (`MarqueCou(x) ==> ArmeCrime(Corde)`).
  3. Pour innocenter `Pervenche` (présente à `22h` dans le `Bureau`, même pièce que le crime, où se trouve le `Poignard`), P2 peut utiliser son alibi à `21h` (`Salon`) ou le fait que l'arme du `Bureau` (`Poignard`) diffère de `Corde`.
- **Attention pour P3 (`grammars/*.fcfg`) :** mettre à jour les lexiques des `.fcfg` avec les noms exacts de [constants.py](constants.py) (`Moutarde`, `Rose`, `Violet`, `Pervenche`, `Olive`, `Leblanc`, `Black`, `Corde`, `Poignard`, `Revolver`, `Chandelier`, `Cle`, `Matraque`, `Cuisine`, `Salon`, `Bureau`, `Chambre`, `Cave`, `Veranda`).

---

## 6. Vérification et tests unitaires

Lancer les tests complets de la partie 1 depuis le dossier `LABO3/` :

```bash
python3 -m unittest discover -s tests -v
```
