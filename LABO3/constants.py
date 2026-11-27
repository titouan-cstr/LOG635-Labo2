# Entités du jeu (identifiants sans accents ni espaces pour la logique FOL et NLTK)
VICTIM = "Black"
PERSONS = ["Moutarde", "Rose", "Violet", "Pervenche", "Olive", "Leblanc"]
ALL_PERSONS = PERSONS + [VICTIM]
WEAPONS = ["Corde", "Poignard", "Revolver", "Chandelier", "Cle", "Matraque"]
ROOMS = ["Cuisine", "Salon", "Bureau", "Chambre", "Cave", "Veranda"]

# Noms complets pour l'affichage console et la synthèse vocale
DISPLAY_NAMES = {
    "Black": "Monsieur Black",
    "Moutarde": "Colonel Moutarde",
    "Rose": "Mademoiselle Rose",
    "Violet": "Professeur Violet",
    "Pervenche": "Madame Pervenche",
    "Olive": "Docteur Olive",
    "Leblanc": "Madame Leblanc",
    "Corde": "corde",
    "Poignard": "poignard",
    "Revolver": "revolver",
    "Chandelier": "chandelier",
    "Cle": "clé anglaise",
    "Matraque": "matraque",
    "Cuisine": "cuisine",
    "Salon": "salon",
    "Bureau": "bureau",
    "Chambre": "chambre",
    "Cave": "cave",
    "Veranda": "véranda",
}

# Chemins du projet
INITIAL_FACTS_FILE = "faits_initiaux.txt"
GRAMMARS_DIR = "grammars"
TTS_OUTPUT_FILE = "tts_output/voice.mp3"