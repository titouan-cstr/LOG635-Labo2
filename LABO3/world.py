"""Module du monde virtuel (plateau Cluedo abstrait) pour la Personne 1.

Gère les pièces ordonnées du manoir, le déplacement du détective IA
(commandé par les touches fléchées) et l'état dynamique des entités
découvertes pendant l'enquête.
"""

from constants import ROOMS


class ManorBoard:
    """Représente le plateau virtuel du manoir et la position de l'agent IA.

    Les pièces sont stockées dans un ordre fixe pour permettre la navigation
    via les touches fléchées (suivante, précédente, première, dernière).
    Aucune association entre pièce, arme et suspect n'est codée en dur.
    """

    def __init__(self, rooms=None, wrap_around=True):
        """Initialise le plateau avec une liste ordonnée de pièces.

        Args:
            rooms: Liste optionnelle de noms de pièces. Utilise `ROOMS` par défaut.
            wrap_around: Si True, `next_room()` depuis la dernière pièce revient à
                la première et `prev_room()` depuis la première va à la dernière.
        """
        room_list = list(rooms) if rooms is not None else list(ROOMS)
        if not room_list:
            raise ValueError("Le plateau doit contenir au moins une pièce.")

        self.rooms = room_list
        self.wrap_around = wrap_around
        self.current_index = 0

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
        if room not in self.rooms:
            raise ValueError(f"Pièce inconnue : {room!r}. Pièces valides : {self.rooms}")
        self.current_index = self.rooms.index(room)
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
