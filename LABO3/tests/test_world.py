"""Tests unitaires pour le module du monde virtuel (`world.py`)."""

import unittest

from constants import PERSONS, ROOMS, VICTIM, WEAPONS
from world import ManorBoard


class TestManorBoardNavigation(unittest.TestCase):
    """Vérifie la structure du plateau et la navigation entre les pièces."""

    def test_entities_count_satisfies_rubric(self):
        """Le plateau doit disposer d'au moins 6 pièces, 6 armes et 6 suspects."""
        self.assertGreaterEqual(len(ROOMS), 6)
        self.assertGreaterEqual(len(WEAPONS), 6)
        self.assertGreaterEqual(len(PERSONS), 6)
        self.assertEqual(VICTIM, "Black")

    def test_initial_position_is_first_room(self):
        """L'agent démarre dans la première pièce de la liste ordonnée."""
        board = ManorBoard()
        self.assertEqual(board.current_room(), ROOMS[0])
        self.assertEqual(board.get_room_order(), ROOMS)

    def test_next_and_prev_with_wrap_around(self):
        """Les flèches → et ← parcourent toutes les pièces en boucle."""
        board = ManorBoard(wrap_around=True)

        # Avance d'une pièce à chaque appel jusqu'à revenir au point de départ
        visited = [board.current_room()]
        for _ in range(len(ROOMS) - 1):
            visited.append(board.next_room())
        self.assertEqual(visited, ROOMS)

        # Un pas de plus boucle sur la première pièce
        self.assertEqual(board.next_room(), ROOMS[0])
        # Un pas en arrière depuis la première boucle sur la dernière
        self.assertEqual(board.prev_room(), ROOMS[-1])

    def test_next_and_prev_without_wrap_around(self):
        """Sans bouclage, l'agent reste bloqué aux extrémités du plateau."""
        board = ManorBoard(wrap_around=False)
        self.assertEqual(board.prev_room(), ROOMS[0])

        board.last_room()
        self.assertEqual(board.next_room(), ROOMS[-1])

    def test_first_and_last_room_shortcuts(self):
        """Les raccourcis ↑ et ↓ placent l'agent au début ou à la fin."""
        board = ManorBoard()
        board.next_room()
        board.next_room()
        self.assertEqual(board.last_room(), ROOMS[-1])
        self.assertEqual(board.first_room(), ROOMS[0])

    def test_move_to_valid_and_invalid_room(self):
        """`move_to` accepte une pièce valide et lève ValueError sinon."""
        board = ManorBoard()
        self.assertEqual(board.move_to("Bureau"), "Bureau")
        self.assertEqual(board.current_room(), "Bureau")

        with self.assertRaises(ValueError):
            board.move_to("Garage")

    def test_empty_rooms_raises_error(self):
        """Un plateau sans aucune pièce est invalide."""
        with self.assertRaises(ValueError):
            ManorBoard(rooms=[])


if __name__ == "__main__":
    unittest.main()
