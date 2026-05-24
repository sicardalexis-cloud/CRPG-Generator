# skill_data.py
import random
from typing import Dict, List

# =============================================
# LISTE DES COMPÉTENCES ACTIVES (avec indices)
# =============================================
active_skills_list = [
    # 1-6 : Compétences générales
    "Équitation", "Natation", "Escalade", 
    "Performance (Acrobatie/ Danse / Musique / Prestidigitation)",
    "Médecine", "Manipulation de pièges et serrures",

    # 7-9 : Survie en forêt
    "Cueillette et connaissance des plantes forestières", 
    "Pistage et traque en milieu boisé",
    "Furtivité et déplacement silencieux en forêt",

    # 10-12 : Survie en montagne
    "Marche en montagne et portage en altitude", 
    "Escalade rocheuse et progression technique",
    "Navigation en relief montagneux",

    # 13-15 : Survie en désert
    "Conservation et recherche d’eau en milieu aride", 
    "Marche désertique et résistance thermique",
    "Orientation et navigation en milieu ouvert",

    # 16-18 : Survie en marais
    "Navigation et progression en terrain inondé", 
    "Résistance aux maladies et insectes des marais",
    "Pistage et chasse en milieu humide",

    # 19-21 : Survie en toundra / glacial
    "Résistance au froid extrême et hypothermie", 
    "Construction d’abris en neige et glace",
    "Chasse et pistage en milieu arctique",

    # 22-24 : Survie en milieu souterrain
    "Navigation et orientation en obscurité totale", 
    "Résistance aux toxines et gaz souterrains",
    "Furtivité et discrétion en milieu confiné",

    # 25-27 : Survie en mer
    "Navigation maritime et lecture des courants", 
    "Pêche en haute mer et survie aquatique",
    "Résistance au mal de mer et gestion des tempêtes",

    # 28-30 : Survie urbaine
    "Streetwise et connaissance des bas-fonds urbains", 
    "Furtivité et déplacement discret en ville",
    "Réseautage et recherche d’informations urbaines",

    # 31-33 : Survie en plaine / savane
    "Pistage et chasse en milieu ouvert", 
    "Orientation en grande plaine",
    "Cueillette et connaissance des plantes de savane",

    # 34-36 : Survie côtière / insulaire
    "Survie côtière et connaissance des marées", 
    "Pêche et récolte en zone littorale",
    "Navigation et orientation sur petite île"
]


# =============================================
# POOLS DE COMPÉTENCES PAR ETHNIE
# =============================================
ethnicity_active_pool: Dict[str, List[int]] = {
    # ==================== HUMAINS ====================
    "Chondathan": [1, 28, 4, 6, 30],
    "Tethyrian": [1, 4, 28, 6, 7],
    "Calishite": [13, 14, 4, 30, 6],
    "Damaran": [10, 19, 1, 12, 20],
    "Illuskan": [10, 12, 19, 26, 21],
    "Mulan": [4, 30, 6, 11, 15],
    "Rashemi": [7, 8, 9, 4, 17],
    "Turami": [1, 4, 28, 6, 30],
    "Uthgardt": [8, 31, 9, 19, 10],
    "Chultan": [7, 8, 17, 16, 9],
    "Shaaran": [31, 32, 33, 1, 14],
    "Ffolk": [26, 25, 34, 4, 9],
    "Sossrim": [19, 20, 21, 26, 12],
    "Vaasan": [10, 19, 12, 1, 20],
    "Nar": [10, 19, 21, 1, 8],
    "Gur": [1, 8, 28, 4, 30],
    "Halruaan": [4, 30, 6, 13, 15],
    "Bedine": [13, 14, 15, 8, 33],
    "Arkaiun": [1, 8, 9, 4, 28],
    "Durpari": [25, 26, 34, 1, 4],
    "Imaskari": [6, 15, 30, 4, 13],
    "Lantanna": [25, 26, 34, 6, 4],
    "Raumviran": [10, 19, 12, 1, 8],
    "Tashalan": [7, 8, 17, 16, 9],
    "Tuigan": [1, 31, 32, 21, 14],
    "Shou": [4, 30, 1, 7, 29],
    "Maztican": [7, 8, 9, 11, 9],
    "Netherese": [6, 30, 4, 15, 13],
    "Talfir": [1, 28, 4, 6, 29],
    "Ulutiun": [19, 20, 21, 26, 12],
    "Reghedman": [10, 19, 21, 1, 8],

    # ==================== ELFES & DEMI-ELFES ====================
    "Wood Half-elf": [9, 7, 8, 4, 12],
    "Moon Half-elf": [9, 4, 30, 7, 15],
    "Sun Half-elf": [4, 30, 15, 1, 11],
    "Wild Half-elf": [8, 9, 31, 7, 19],
    "Drow Half-elf": [24, 6, 23, 22, 9],
    "Sea Half-elf": [25, 26, 34, 2, 9],
    "Elf Wood": [9, 7, 8, 12, 31],
    "Elf Moon": [9, 7, 4, 30, 15],
    "Elf Sun": [4, 30, 15, 11, 1],
    "Elf Wild": [8, 9, 31, 7, 19],
    "Elf Drow": [24, 6, 23, 22, 9],
    "Elf Sea": [25, 26, 34, 2, 9],
    "Elf Star": [4, 15, 9, 30, 7],
    "Elf Avariel": [3, 11, 15, 9, 4],
    "Elf Lythari": [9, 7, 8, 31, 19],

    # ==================== NAINS, GNOMES, HALFELINS ====================
    "Nain": [10, 11, 19, 6, 12],
    "Shield Dwarf": [10, 11, 19, 6, 20],
    "Gold Dwarf": [10, 11, 6, 30, 5],
    "Gray Dwarf": [22, 23, 24, 6, 11],
    "Gnome": [6, 24, 4, 7, 11],
    "Rock Gnome": [6, 11, 20, 5, 30],
    "Forest Gnome": [9, 7, 8, 4, 24],
    "Deep Gnome": [22, 23, 24, 6, 11],
    "Halfelin": [6, 29, 4, 6, 28],
    "Lightfoot Halfling": [29, 4, 28, 1, 30],
    "Strongheart Halfling": [6, 1, 4, 28, 19],
    "Ghostwise Halfling": [9, 8, 4, 7, 24],

    # ==================== AUTRES RACES ====================
    "Half-Orc": [10, 11, 31, 19, 28],
    "Gray Orc": [24, 23, 22, 6, 31],
    "Mountain Orc": [10, 11, 19, 31, 20],
    "Air Genasi": [4, 29, 36, 30, 1],
    "Earth Genasi": [10, 11, 6, 23, 20],
    "Fire Genasi": [4, 19, 28, 31, 6],
    "Water Genasi": [2, 25, 26, 34, 27],
    "Aasimar": [4, 30, 5, 1, 8],
    "Tiefling": [28, 29, 6, 4, 30],
    "Goblin": [29, 6, 24, 6, 28],
    "Hobgoblin": [1, 6, 12, 30, 28],
    "Yuan-ti Pureblood": [30, 28, 4, 6, 29],
    "Dragonborn": [10, 11, 19, 1, 4],
    "Firbolg": [7, 8, 9, 5, 34],
    "Kenku": [4, 29, 6, 28, 6],
    "Lizardfolk": [2, 18, 34, 26, 17],
    "Triton": [2, 25, 26, 34, 27],
    "Aarakocra": [4, 36, 29, 11, 32],
    "Goliath": [10, 11, 19, 20, 12],
    "Centaur": [1, 31, 32, 33, 4]
}


def generate_active_skills(region_id: int = 0, ethnicity: str = "Chondathan") -> Dict:
    """Retourne EXACTEMENT 2 compétences choisies aléatoirement parmi les 5 de l'ethnie"""
    
    indices = ethnicity_active_pool.get(ethnicity, [1, 4, 6, 28, 29])  # fallback
    
    # Choix de 2 compétences différentes parmi les 5
    selected_indices = random.sample(indices, 2)
    
    # Conversion des indices en noms de compétences
    selected_skills = [active_skills_list[i-1] for i in selected_indices 
                       if 1 <= i <= len(active_skills_list)]
    
    # Conversion en dictionnaire
    skills_dict = {skill: "Maîtrisé" for skill in selected_skills}
    
    return {
        "skills": skills_dict,
        "bonus_languages": []
    }