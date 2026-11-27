"""Module du monde virtuel (plateau Cluedo abstrait) pour la Personne 1.

Gère les pièces ordonnées du manoir, le déplacement du détective IA
(commandé par les touches fléchées) et l'enregistrement dynamique des
associations personne / arme / pièce / heure découvertes pendant l'enquête.
"""

from constants import ALL_PERSONS, ROOMS, WEAPONS


class ManorBoard:
    """Représente le plateau virtuel du manoir et la position de l'agent IA.

    Les pièces sont stockées dans un ordre fixe pour permettre la navigation
    via les touches fléchées (suivante, précédente, première, dernière).
    Aucune association entre pièce, arme et suspect n'est codée en dur :
    toutes les relations sont enregistrées dynamiquement à l'exécution.
    """

    VALID_STATUSES = ("mort", "vivant")

    def __init__(self, rooms=None, weapons=None, persons=None, wrap_around=True):
        """Initialise le plateau avec des entités valides et un état vierge.

        Args:
            rooms: Liste optionnelle de noms de pièces. Utilise `ROOMS` par défaut.
            weapons: Liste optionnelle d'armes valides. Utilise `WEAPONS` par défaut.
            persons: Liste optionnelle de personnes valides. Utilise `ALL_PERSONS` par défaut.
            wrap_around: Si True, `next_room()` depuis la dernière pièce revient à
                la première et `prev_room()` depuis la première va à la dernière.
        """
        room_list = list(rooms) if rooms is not None else list(ROOMS)
        if not room_list:
            raise ValueError("Le plateau doit contenir au moins une pièce.")

        self.rooms = room_list
        self.weapons = list(weapons) if weapons is not None else list(WEAPONS)
        self.persons = list(persons) if persons is not None else list(ALL_PERSONS)
        self.wrap_around = wrap_around
        self.current_index = 0

        self.reset_associations()

    # ------------------------------------------------------------------
    # Réinitialisation et validation
    # ------------------------------------------------------------------

    def reset_associations(self):
        """Réinitialise toutes les associations dynamiques du plateau."""
        self._rooms_state = {
            room: {
                "visited": False,
                "name_confirmed": False,
                "weapons": [],
                "persons": [],
                "sightings": [],
                "clues": [],
            }
            for room in self.rooms
        }
        self._weapon_locations = {}
        self._person_current_room = {}
        self._person_timelines = {person: [] for person in self.persons}
        self._person_statuses = {}
        self._victim = None
        self._crime_hour = None

    def _resolve_room(self, room=None):
        """Retourne `room` si fourni, sinon la pièce courante, après validation."""
        target = self.current_room() if room is None else room
        if target not in self._rooms_state:
            raise ValueError(f"Pièce inconnue : {target!r}. Pièces valides : {self.rooms}")
        return target

    def _validate_weapon(self, weapon):
        """Vérifie que l'arme appartient bien au référentiel du monde."""
        if weapon not in self.weapons:
            raise ValueError(f"Arme inconnue : {weapon!r}. Armes valides : {self.weapons}")

    def _validate_person(self, person):
        """Vérifie que la personne appartient bien au référentiel du monde."""
        if person not in self.persons:
            raise ValueError(f"Personne inconnue : {person!r}. Personnes valides : {self.persons}")

    @staticmethod
    def _validate_hour(hour):
        """Vérifie qu'une heure est un entier valide (0 à 24 inclus)."""
        if isinstance(hour, bool) or not isinstance(hour, int) or not (0 <= hour <= 24):
            raise ValueError(f"Heure invalide : {hour!r}. Un entier entre 0 et 24 est attendu.")

    # ------------------------------------------------------------------
    # Navigation sur le plateau (touches fléchées pour P4)
    # ------------------------------------------------------------------

    def current_room(self):
        """Retourne le nom de la pièce où se trouve actuellement l'agent."""
        return self.rooms[self.current_index]

    def next_room(self):
        """Déplace l'agent vers la pièce suivante (touche flèche droite →)."""
        if self.current_index < len(self.rooms) - 1:
            self.current_index += 1
        elif self.wrap_around:
            self.current_index = 0
        return self.current_room()

    def prev_room(self):
        """Déplace l'agent vers la pièce précédente (touche flèche gauche ←)."""
        if self.current_index > 0:
            self.current_index -= 1
        elif self.wrap_around:
            self.current_index = len(self.rooms) - 1
        return self.current_room()

    def first_room(self):
        """Déplace l'agent vers la première pièce du plateau (touche flèche haut ↑)."""
        self.current_index = 0
        return self.current_room()

    def last_room(self):
        """Déplace l'agent vers la dernière pièce du plateau (touche flèche bas ↓)."""
        self.current_index = len(self.rooms) - 1
        return self.current_room()

    def move_to(self, room):
        """Déplace directement l'agent vers une pièce donnée par son nom."""
        target = self._resolve_room(room)
        self.current_index = self.rooms.index(target)
        return self.current_room()

    def get_room_order(self):
        """Retourne une copie de la liste ordonnée des pièces du plateau."""
        return list(self.rooms)

    def get_navigation_info(self):
        """Retourne un dictionnaire décrivant la position courante pour l'affichage."""
        total = len(self.rooms)
        next_idx = (self.current_index + 1) % total if self.wrap_around else min(self.current_index + 1, total - 1)
        prev_idx = (self.current_index - 1) % total if self.wrap_around else max(self.current_index - 1, 0)
        return {
            "current_room": self.current_room(),
            "index": self.current_index,
            "total": total,
            "prev_room": self.rooms[prev_idx],
            "next_room": self.rooms[next_idx],
        }

    # ------------------------------------------------------------------
    # Associations dynamiques (Critère #5)
    # ------------------------------------------------------------------

    def mark_room_visited(self, room=None, name_confirmed=True):
        """Marque une pièce (par défaut la pièce courante) comme visitée."""
        target = self._resolve_room(room)
        self._rooms_state[target]["visited"] = True
        if name_confirmed:
            self._rooms_state[target]["name_confirmed"] = True

    def place_weapon(self, weapon, room=None):
        """Associe dynamiquement une arme à une pièce (défaut : pièce courante).

        Si l'arme était déjà localisée dans une autre pièce, elle en est retirée
        pour éviter les doublons incohérents sur le plateau.
        """
        self._validate_weapon(weapon)
        target = self._resolve_room(room)

        previous_room = self._weapon_locations.get(weapon)
        if previous_room is not None and previous_room != target:
            self._rooms_state[previous_room]["weapons"].remove(weapon)

        if weapon not in self._rooms_state[target]["weapons"]:
            self._rooms_state[target]["weapons"].append(weapon)
        self._weapon_locations[weapon] = target

    def place_person(self, person, room=None, hour=None):
        """Associe dynamiquement une personne à une pièce, avec heure optionnelle.

        - Sans heure (`hour=None`) : met à jour la position actuelle de la personne.
        - Avec heure (`hour=int`) : enregistre un passage horodaté dans la pièce
          et dans l'historique temporel de la personne.
        """
        self._validate_person(person)
        target = self._resolve_room(room)

        if hour is None:
            previous_room = self._person_current_room.get(person)
            if previous_room is not None and previous_room != target:
                self._rooms_state[previous_room]["persons"].remove(person)
            if person not in self._rooms_state[target]["persons"]:
                self._rooms_state[target]["persons"].append(person)
            self._person_current_room[person] = target
            return

        self._validate_hour(hour)
        sighting = {"person": person, "hour": hour}
        if sighting not in self._rooms_state[target]["sightings"]:
            self._rooms_state[target]["sightings"].append(sighting)

        timeline_entry = {"room": target, "hour": hour}
        if timeline_entry not in self._person_timelines[person]:
            self._person_timelines[person].append(timeline_entry)
            self._person_timelines[person].sort(key=lambda entry: entry["hour"])

    def record_clue(self, clue, room=None):
        """Enregistre un indice textuel/logique découvert dans une pièce."""
        if not isinstance(clue, str) or not clue.strip():
            raise ValueError("L'indice doit être une chaîne de caractères non vide.")
        target = self._resolve_room(room)
        cleaned = clue.strip()
        if cleaned not in self._rooms_state[target]["clues"]:
            self._rooms_state[target]["clues"].append(cleaned)

    def set_person_status(self, person, status, hour=None):
        """Enregistre l'état d'une personne (`'mort'` ou `'vivant'`)."""
        self._validate_person(person)
        normalized = status.strip().lower()
        if normalized not in self.VALID_STATUSES:
            raise ValueError(f"Statut invalide : {status!r}. Attendu : {self.VALID_STATUSES}")

        self._person_statuses[person] = normalized
        if normalized == "mort":
            self._victim = person
            if hour is not None:
                self._validate_hour(hour)
                self._crime_hour = hour

    # ------------------------------------------------------------------
    # Inspection de l'état pour P3 (génération de questions) et P4
    # ------------------------------------------------------------------

    def get_room_state(self, room=None):
        """Retourne une copie complète de l'état connu d'une pièce."""
        target = self._resolve_room(room)
        state = self._rooms_state[target]
        return {
            "room": target,
            "visited": state["visited"],
            "name_confirmed": state["name_confirmed"],
            "weapons": list(state["weapons"]),
            "persons": list(state["persons"]),
            "sightings": [dict(s) for s in state["sightings"]],
            "clues": list(state["clues"]),
        }

    def get_weapons_in_room(self, room=None):
        """Retourne la liste des armes actuellement associées à la pièce."""
        target = self._resolve_room(room)
        return list(self._rooms_state[target]["weapons"])

    def get_persons_in_room(self, room=None):
        """Retourne la liste des personnes actuellement présentes dans la pièce."""
        target = self._resolve_room(room)
        return list(self._rooms_state[target]["persons"])

    def get_person_timeline(self, person):
        """Retourne les passages horodatés connus d'une personne (triés par heure)."""
        self._validate_person(person)
        return [dict(entry) for entry in self._person_timelines[person]]

    def get_unvisited_rooms(self):
        """Retourne la liste des pièces qui n'ont pas encore été visitées."""
        return [room for room in self.rooms if not self._rooms_state[room]["visited"]]

    def get_unlocated_weapons(self):
        """Retourne les armes qui n'ont pas encore été associées à une pièce."""
        return [weapon for weapon in self.weapons if weapon not in self._weapon_locations]

    def get_unlocated_persons(self):
        """Retourne les personnes sans position actuelle ni passage horodaté connu."""
        return [
            person
            for person in self.persons
            if person not in self._person_current_room and not self._person_timelines[person]
        ]

    def get_summary(self):
        """Retourne un résumé global de l'état du monde virtuel."""
        return {
            "current_room": self.current_room(),
            "victim": self._victim,
            "crime_hour": self._crime_hour,
            "statuses": dict(self._person_statuses),
            "weapon_locations": dict(self._weapon_locations),
            "unvisited_rooms": self.get_unvisited_rooms(),
            "unlocated_weapons": self.get_unlocated_weapons(),
            "unlocated_persons": self.get_unlocated_persons(),
            "rooms": {room: self.get_room_state(room) for room in self.rooms},
        }
