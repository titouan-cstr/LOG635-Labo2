"""Tests unitaires pour le module du monde virtuel (`world.py`)."""

from pathlib import Path
import tempfile
import unittest

from constants import INITIAL_FACTS_FILE, PERSONS, ROOMS, VICTIM, WEAPONS
from world import (
    ManorBoard,
    apply_fact_to_board,
    apply_initial_facts,
    load_initial_facts,
)


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

        visited = [board.current_room()]
        for _ in range(len(ROOMS) - 1):
            visited.append(board.next_room())
        self.assertEqual(visited, ROOMS)

        self.assertEqual(board.next_room(), ROOMS[0])
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


class TestManorBoardDynamicAssociations(unittest.TestCase):
    """Vérifie les associations dynamiques et le suivi d'état du manoir."""

    def test_board_starts_with_no_hardcoded_associations(self):
        """Au démarrage, aucune arme ni personne n'est associée à une pièce."""
        board = ManorBoard()
        self.assertEqual(board.get_unvisited_rooms(), ROOMS)
        self.assertEqual(board.get_unlocated_weapons(), WEAPONS)
        self.assertEqual(len(board.get_unlocated_persons()), len(PERSONS) + 1)

    def test_place_and_relocate_weapon(self):
        """Placer une arme l'associe à une pièce et évite les doublons si déplacée."""
        board = ManorBoard()
        board.place_weapon("Corde")  # pièce courante = Cuisine
        self.assertEqual(board.get_weapons_in_room("Cuisine"), ["Corde"])
        self.assertNotIn("Corde", board.get_unlocated_weapons())

        # Déplacement dynamique vers Bureau
        board.place_weapon("Corde", room="Bureau")
        self.assertEqual(board.get_weapons_in_room("Cuisine"), [])
        self.assertEqual(board.get_weapons_in_room("Bureau"), ["Corde"])

    def test_place_person_current_and_hourly_sightings(self):
        """Enregistre position actuelle et passages horodatés triés par heure."""
        board = ManorBoard()
        board.place_person("Moutarde", room="Salon")
        board.place_person("Moutarde", room="Bureau")
        self.assertEqual(board.get_persons_in_room("Salon"), [])
        self.assertEqual(board.get_persons_in_room("Bureau"), ["Moutarde"])

        board.place_person("Moutarde", room="Veranda", hour=22)
        board.place_person("Moutarde", room="Cuisine", hour=20)
        self.assertEqual(
            board.get_person_timeline("Moutarde"),
            [
                {"room": "Cuisine", "hour": 20},
                {"room": "Veranda", "hour": 22},
            ],
        )
        self.assertNotIn("Moutarde", board.get_unlocated_persons())

    def test_clues_visit_and_status_tracking(self):
        """Gère les indices, les visites de pièces et le statut mort/vivant."""
        board = ManorBoard()
        board.mark_room_visited("Cave")
        board.record_clue("MarqueCou", room="Cave")
        board.record_clue("MarqueCou", room="Cave")  # déduplication
        board.set_person_status("Black", "mort", hour=21)
        board.set_person_status("Rose", "vivant")

        cave = board.get_room_state("Cave")
        self.assertTrue(cave["visited"])
        self.assertTrue(cave["name_confirmed"])
        self.assertEqual(cave["clues"], ["MarqueCou"])
        self.assertNotIn("Cave", board.get_unvisited_rooms())

        summary = board.get_summary()
        self.assertEqual(summary["victim"], "Black")
        self.assertEqual(summary["crime_hour"], 21)
        self.assertEqual(summary["statuses"]["Rose"], "vivant")

    def test_different_configurations_and_reset(self):
        """Prouve l'absence de lien codé en dur en testant deux scénarios opposés."""
        board = ManorBoard()

        # Scénario A
        board.place_weapon("Poignard", room="Salon")
        board.place_person("Rose", room="Salon", hour=19)
        self.assertEqual(board.get_weapons_in_room("Salon"), ["Poignard"])

        # Réinitialisation puis Scénario B complètement différent
        board.reset_associations()
        self.assertEqual(board.get_weapons_in_room("Salon"), [])
        board.place_weapon("Chandelier", room="Cave")
        board.place_person("Olive", room="Cave", hour=23)
        self.assertEqual(board.get_weapons_in_room("Cave"), ["Chandelier"])
        self.assertEqual(board.get_person_timeline("Olive"), [{"room": "Cave", "hour": 23}])

    def test_validation_errors(self):
        """Lève ValueError si une entité ou une heure est invalide."""
        board = ManorBoard()
        with self.assertRaises(ValueError):
            board.place_weapon("Laser")
        with self.assertRaises(ValueError):
            board.place_person("Batman", room="Cuisine")
        with self.assertRaises(ValueError):
            board.place_person("Moutarde", room="Cuisine", hour=25)
        with self.assertRaises(ValueError):
            board.place_person("Moutarde", room="Cuisine", hour=True)
        with self.assertRaises(ValueError):
            board.set_person_status("Black", "disparu")
        with self.assertRaises(ValueError):
            board.record_clue("   ")


class TestInitialFactsLoader(unittest.TestCase):
    """Vérifie le chargement de `faits_initiaux.txt` et la synchronisation du plateau."""

    def test_load_default_initial_facts_file(self):
        """Le fichier `faits_initiaux.txt` est lisible et ignore commentaires/lignes vides."""
        facts = load_initial_facts(INITIAL_FACTS_FILE)
        self.assertGreaterEqual(len(facts), 9)
        self.assertIn("Black est mort", facts)
        self.assertIn("Black est mort à 21h", facts)
        self.assertIn("Black est dans le bureau", facts)
        self.assertTrue(all(not f.startswith("#") for f in facts))

    def test_apply_initial_facts_updates_board(self):
        """Appliquer les faits de départ renseigne victime, heure, lieu et statuts."""
        board = ManorBoard()
        facts = apply_initial_facts(board, INITIAL_FACTS_FILE)
        self.assertGreater(len(facts), 0)

        summary = board.get_summary()
        self.assertEqual(summary["victim"], "Black")
        self.assertEqual(summary["crime_hour"], 21)
        self.assertEqual(board.get_persons_in_room("Bureau"), ["Black"])
        for suspect in PERSONS:
            self.assertEqual(summary["statuses"][suspect], "vivant")

    def test_apply_fact_handles_accents_weapons_and_hourly_sightings(self):
        """Prend en charge les variantes avec accents, armes et passages horodatés."""
        board = ManorBoard()
        self.assertTrue(apply_fact_to_board(board, "La clé est dans la véranda"))
        self.assertTrue(apply_fact_to_board(board, "Moutarde était dans la cuisine à 22h"))
        self.assertTrue(apply_fact_to_board(board, "Black est dans le bureau"))
        self.assertTrue(apply_fact_to_board(board, "Black a des marques au cou"))
        self.assertFalse(apply_fact_to_board(board, "Phrase non reconnue sans entité"))

        self.assertEqual(board.get_weapons_in_room("Veranda"), ["Cle"])
        self.assertEqual(board.get_person_timeline("Moutarde"), [{"room": "Cuisine", "hour": 22}])
        self.assertEqual(board.get_room_state("Bureau")["clues"], ["MarqueCou"])

    def test_missing_initial_facts_file_raises_error(self):
        """Lève FileNotFoundError si le chemin fourni n'existe pas."""
        with self.assertRaises(FileNotFoundError):
            load_initial_facts("fichier_inexistant_123.txt")

    def test_custom_temp_file_loading(self):
        """Charge n'importe quel fichier externe sans rien coder en dur."""
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as tmp:
            tmp.write("# Commentaire\n\nRose est morte\nLe poignard est dans le salon\n")
            tmp_path = Path(tmp.name)

        try:
            board = ManorBoard()
            facts = apply_initial_facts(board, tmp_path)
            self.assertEqual(facts, ["Rose est morte", "Le poignard est dans le salon"])
            self.assertEqual(board.get_summary()["victim"], "Rose")
            self.assertEqual(board.get_weapons_in_room("Salon"), ["Poignard"])
        finally:
            tmp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
