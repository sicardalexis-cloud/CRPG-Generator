# skill_data.py
import random
from typing import Dict, List

# =============================================
# LISTE DES COMPÉTENCES ACTIVES (36 compétences)
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

    # Elfes & Demi-elfes
    "Wood Half-elf": [9, 7, 8, 4, 12],
    "Moon Half-elf": [9, 4, 30, 7, 15],
    "Sun Half-elf": [4, 30, 15, 1, 11],
    "Wild Half-elf": [8, 9, 31, 7, 19],
    "Drow Half-elf": [22, 23, 24, 6, 9],
    "Sea Half-elf": [25, 26, 34, 2, 27],
    "Elf Wood": [9, 7, 8, 12, 31],
    "Elf Moon": [9, 7, 4, 30, 15],
    "Elf Sun": [4, 30, 15, 11, 1],
    "Elf Wild": [8, 9, 31, 7, 19],
    "Elf Drow": [22, 23, 24, 6, 9],
    "Elf Sea": [25, 26, 34, 2, 27],

    # Nains, Gnomes, Halfelins
    "Shield Dwarf": [10, 11, 12, 19, 20],
    "Gold Dwarf": [10, 11, 6, 30, 5],
    "Gray Dwarf": [22, 23, 24, 6, 11],
    "Rock Gnome": [6, 11, 20, 5, 30],
    "Forest Gnome": [9, 7, 8, 4, 24],
    "Lightfoot Halfling": [29, 4, 28, 1, 30],
    "Strongheart Halfling": [6, 1, 4, 28, 19],

    # Autres
    "Half-Orc": [10, 11, 31, 19, 28],
    "Aasimar": [4, 30, 5, 1, 8],
    "Tiefling": [28, 29, 6, 4, 30],
    "Dragonborn": [10, 11, 19, 1, 4],
    "Goliath": [10, 11, 19, 20, 12],
    "Autre": [1, 4, 6, 28, 30]
}

# =============================================
# POOLS DE COMPÉTENCES ACTIVES - RÉGIONS (indices 1-36)
# =============================================
region_active_pool: Dict[int, List[int]] = {
    1: [30, 28, 4, 6, 29, 13, 14, 25, 26],      # Calimshan
    2: [30, 28, 29, 4, 6, 25, 26, 34, 1],       # Amn
    3: [6, 1, 8, 30, 4, 7, 9, 31, 28],          # Tethyr
    4: [28, 30, 6, 29, 4, 1, 25, 26, 34],       # Baldur's Gate
    5: [30, 28, 4, 6, 29, 1, 25, 26, 34],       # Waterdeep
    6: [30, 28, 29, 4, 6, 1, 25, 34, 26],       # Sembia
    7: [6, 1, 8, 30, 4, 7, 9, 31, 28],          # Cormyr
    8: [30, 28, 4, 6, 1, 25, 26, 34, 29],       # Chondath
    9: [25, 26, 34, 2, 35, 4, 30, 1, 28],       # Vilhon Reach
    10: [1, 4, 30, 6, 28, 25, 26, 34, 27],      # Turmish

    11: [1, 4, 30, 6, 11, 15, 28, 31, 5],       # Chessenta
    12: [13, 14, 15, 4, 30, 6, 28, 1, 25],      # Mulhorand
    13: [13, 14, 15, 4, 30, 6, 28, 1, 25],      # Unther
    14: [7, 8, 9, 19, 4, 31, 1, 28, 30],        # Rashemen
    15: [10, 11, 12, 19, 20, 1, 6, 31, 28],     # Damara
    16: [1, 4, 30, 6, 28, 10, 11, 25, 26],      # Impiltur
    17: [30, 28, 4, 6, 29, 31, 1, 25, 34],      # Thesk
    18: [28, 30, 6, 4, 29, 10, 11, 1, 25],      # Moonsea
    19: [25, 26, 27, 28, 29, 6, 4, 1, 30],      # Luskan
    20: [30, 28, 4, 6, 29, 1, 25, 26, 34],      # Neverwinter

    21: [19, 20, 21, 10, 11, 12, 31, 1, 6],     # Icewind Dale
    22: [25, 26, 27, 34, 35, 2, 4, 30, 1],      # Moonshae Isles
    23: [19, 20, 21, 10, 11, 1, 31, 4, 6],      # Sossal
    24: [7, 8, 9, 18, 17, 2, 34, 35, 5],        # Chult
    25: [9, 7, 8, 4, 2, 25, 34, 1, 30],         # Evermeet
    26: [9, 7, 8, 4, 31, 1, 30, 5, 12],         # Cormanthor
    27: [9, 7, 8, 31, 4, 1, 30, 10, 11],        # High Forest
    28: [9, 7, 8, 4, 31, 19, 20, 1, 30],        # Moonwood
    29: [9, 7, 8, 31, 4, 18, 17, 2, 34],        # Wealdath
    30: [6, 11, 24, 4, 30, 28, 29, 1, 34],      # Lantan

    # ==================== 31 à 133 ====================
    31: [10, 11, 12, 19, 20, 6, 24, 1, 31],     # Citadel Adbar
    32: [10, 11, 12, 19, 20, 6, 24, 1, 31],     # Mithral Hall
    33: [10, 11, 12, 19, 20, 6, 24, 1, 31],     # Great Rift
    34: [10, 11, 12, 19, 20, 6, 24, 1, 31],     # Ironmaster
    35: [6, 29, 4, 28, 9, 7, 8, 1, 30],         # Luiren
    36: [10, 11, 19, 20, 21, 1, 6, 31, 12],     # Vaasa
    37: [10, 11, 12, 19, 20, 21, 31, 1, 6],     # Spine of the World
    38: [9, 7, 8, 4, 11, 3, 1, 30, 34],         # Star Mounts
    39: [22, 23, 24, 6, 11, 29, 28, 4, 30],     # Underdark
    40: [13, 14, 15, 31, 1, 4, 30, 28, 6],      # Anauroch

    41: [10, 11, 19, 20, 21, 31, 1, 6, 28],     # Le Nord
    42: [31, 32, 8, 9, 19, 20, 1, 10, 11],      # Uthgardt Tribes
    43: [30, 28, 4, 6, 29, 5, 1, 30, 28],       # Thay
    44: [25, 26, 34, 9, 7, 4, 30, 2, 1],        # Aglarond
    45: [10, 11, 12, 19, 20, 1, 6, 30, 28],     # Silver Marches
    46: [7, 8, 9, 31, 1, 4, 30, 5, 32],         # The Dalelands
    47: [31, 32, 33, 1, 8, 18, 13, 14, 4],      # The Shaar
    48: [25, 26, 27, 34, 13, 14, 30, 28, 6],    # Lake of Steam
    49: [28, 29, 6, 4, 30, 31, 1, 8, 18],       # Border Kingdoms
    50: [31, 32, 33, 1, 8, 14, 19, 10, 4],      # Hordelands

    51: [30, 28, 4, 1, 13, 14, 6, 28, 5],       # Old Empires
    52: [9, 7, 8, 19, 20, 4, 30, 5, 31],        # Unapproachable East
    53: [1, 4, 30, 28, 6, 31, 7, 8, 28],        # Western Heartlands
    54: [25, 26, 27, 34, 28, 29, 6, 4, 30],     # Sword Coast
    55: [10, 11, 19, 20, 28, 29, 1, 6, 31],     # Sword Coast North
    56: [25, 26, 27, 34, 28, 4, 30, 6, 1],      # Dragon Coast
    57: [19, 20, 21, 10, 11, 12, 31, 1, 6],     # Great Glacier
    58: [25, 26, 27, 34, 2, 35, 4, 30, 28],     # Inner Sea
    59: [4, 30, 28, 5, 6, 1, 29, 34, 25],       # Halruaa
    60: [1, 31, 4, 8, 9, 28, 6, 30, 19],        # Dambrath

    61: [31, 32, 33, 1, 4, 30, 28, 8, 18],      # Estagund
    62: [30, 28, 29, 4, 6, 1, 34, 25, 26],      # Var the Golden
    63: [31, 32, 33, 13, 14, 1, 4, 30, 28],     # Shaarmid
    64: [25, 26, 34, 2, 35, 4, 30, 28, 6],      # Thindol
    65: [7, 8, 9, 18, 17, 2, 34, 4, 28],        # Samarach
    66: [25, 26, 34, 35, 2, 4, 30, 28, 1],      # Tashalar
    67: [31, 32, 33, 13, 14, 4, 30, 1, 28],     # The Shining South
    68: [7, 8, 9, 31, 4, 30, 28, 5, 1],         # Ymber
    69: [25, 26, 27, 34, 35, 28, 29, 6, 4],     # Nelanther Isles
    70: [19, 20, 21, 25, 26, 2, 1, 31, 4],      # The Whalebones

    71: [25, 26, 27, 34, 2, 35, 4, 30, 1],      # The Trackless Sea
    72: [19, 20, 21, 10, 11, 12, 31, 1, 6],     # The Cold Lands
    73: [13, 14, 15, 31, 32, 1, 4, 30, 28],     # The Endless Wastes
    74: [7, 8, 9, 31, 32, 4, 1, 19, 20],        # The Great Dale
    75: [4, 30, 28, 6, 29, 5, 1, 34, 25],       # The Plateau of Thay
    76: [25, 26, 27, 34, 2, 30, 28, 4, 1],      # The Easting Reach
    77: [9, 7, 8, 31, 4, 19, 20, 1, 30],        # The Forgotten Forest
    78: [10, 11, 12, 19, 20, 6, 1, 31, 4],      # The Lone Rock
    79: [9, 7, 8, 31, 4, 18, 17, 1, 30],        # The Reaching Woods
    80: [10, 11, 12, 19, 20, 6, 1, 31, 4],      # The Thunder Peaks

    81: [31, 32, 1, 8, 4, 30, 28, 10, 11],      # The Ride
    82: [9, 7, 8, 4, 25, 34, 30, 1, 5],         # Aglarondine
    83: [13, 14, 15, 31, 1, 4, 30, 28, 6],      # Bedine
    84: [10, 11, 12, 6, 24, 19, 20, 1, 30],     # Barakuir
    85: [9, 7, 8, 4, 31, 6, 28, 1, 30],         # Chondalwood
    86: [10, 11, 12, 19, 20, 6, 24, 1, 30],     # Citadelles du Nord
    87: [22, 23, 24, 6, 29, 28, 4, 11, 30],     # Cité Drow
    88: [22, 23, 24, 6, 11, 29, 28, 4, 30],     # Cité Souterraine Mixte
    89: [25, 26, 27, 34, 28, 29, 6, 4, 30],     # Eauprofonde
    90: [19, 20, 21, 10, 11, 12, 6, 1, 31],     # Épine dorsale

    91: [9, 7, 8, 31, 4, 6, 28, 1, 30],         # Forêt d’Amtar / Methwood
    92: [10, 11, 12, 19, 20, 6, 24, 1, 30],     # Forteresses isolées
    93: [22, 23, 24, 6, 11, 19, 20, 1, 30],     # Gracklstugh
    94: [10, 11, 12, 6, 24, 19, 20, 1, 30],     # Grande Faille
    95: [19, 20, 21, 10, 11, 12, 31, 1, 6],     # Grand Glacier
    96: [19, 20, 21, 10, 11, 31, 1, 6, 4],      # Glacière éternelle
    97: [25, 26, 27, 19, 20, 1, 4, 30, 28],     # Ruathym
    98: [9, 7, 8, 4, 31, 1, 30, 5, 28],         # Luirwood
    99: [9, 7, 8, 4, 30, 5, 1, 31, 11],         # Myth Drannor
    100: [9, 7, 8, 4, 11, 1, 30, 5, 31],        # Evereska

    101: [19, 20, 21, 10, 11, 31, 1, 6, 4],     # Valbise
    102: [10, 11, 12, 6, 24, 19, 20, 1, 30],    # Vallée de la Flamme
    103: [7, 8, 31, 1, 4, 30, 5, 32, 28],       # Les Vaux
    104: [31, 32, 1, 4, 30, 28, 10, 11, 6],     # Vast
    105: [7, 8, 9, 18, 17, 2, 34, 4, 28],       # Jungle de Mhair
    106: [13, 14, 15, 25, 26, 4, 30, 28, 1],    # Zakharans
    107: [10, 11, 19, 20, 31, 8, 6, 4, 28],     # Pics Gris
    108: [22, 23, 24, 6, 11, 18, 17, 4, 31],    # Outreterre tropicale
    109: [9, 7, 8, 6, 24, 4, 11, 1, 30],        # Forêts du Nord (Gnomes)
    110: [9, 7, 8, 4, 25, 34, 30, 1, 5],        # Éternelle-Rencontre

    111: [10, 11, 19, 20, 31, 1, 30, 4, 28],    # Lunargent
    112: [9, 7, 8, 31, 4, 18, 17, 1, 30],       # Bois de Yuir
    113: [10, 11, 31, 8, 19, 6, 4, 28, 1],      # Montagnes du Shaar
    114: [9, 7, 8, 31, 4, 19, 20, 1, 30],       # Vil Adanrath
    115: [10, 11, 1, 4, 31, 6, 28, 19, 20],     # Tymanther
    116: [10, 11, 12, 19, 20, 21, 1, 31, 6],    # Icerim Mountains
    117: [10, 11, 12, 19, 20, 31, 1, 6, 4],     # Montagnes Theskiennes
    118: [10, 11, 12, 19, 20, 6, 31, 1, 4],     # Montagnes de Cuivre
    119: [1, 4, 30, 31, 32, 7, 8, 28, 5],       # Kara-Tur
    120: [22, 23, 24, 6, 11, 29, 28, 4, 30],    # Pics de Mir

    121: [9, 7, 8, 31, 4, 18, 17, 1, 30],       # Bois de Shaar
    122: [22, 23, 24, 6, 11, 19, 20, 10, 31],   # Outreterre profonde
    123: [9, 8, 31, 19, 20, 4, 7, 1, 28],       # Lycanthropes
    124: [31, 32, 8, 9, 4, 1, 18, 7, 30],       # Wemics
    125: [28, 29, 6, 4, 30, 18, 17, 9, 31],     # Yuan-ti
    126: [1, 31, 32, 8, 4, 9, 30, 11, 28],      # Centaure
    127: [2, 18, 17, 34, 26, 9, 8, 4, 28],      # Homme-lézard
    128: [10, 11, 19, 6, 28, 4, 31, 23, 24],    # Tanarukks
    129: [4, 9, 7, 30, 28, 6, 11, 1, 29],       # Fey’ri
    130: [22, 23, 24, 4, 30, 28, 9, 7, 5],      # Sagespectres

    131: [1, 4, 10, 11, 31, 6, 30, 28, 19],     # Vaillants
    132: [3, 11, 4, 9, 22, 23, 24, 30, 28],     # Kir-lanan
    133: [22, 23, 24, 9, 29, 28, 4, 6, 30],     # Reflets (Shades)
}

# =============================================
# BIAIS SELON TYPE DE SETTLEMENT
# =============================================
settlement_skill_bias: Dict[int, List[int]] = {
    # === MILIEUX URBAINS (Équitation faible ou absente) ===
    1: [30, 28, 29, 4, 79, 84],      # Capitale / Grande Métropole          → Équitation supprimée
    2: [30, 28, 4, 79, 76, 84],      # Grande Ville portuaire
    3: [30, 28, 4, 79, 77, 84],      # Grande Ville marchande
    4: [28, 30, 6, 29, 4, 1],        # Ville fortifiée                     → un peu d'équitation
    5: [30, 28, 4, 6, 29, 79],       # Ville moyenne
    28: [4, 30, 28, 29, 6, 1],       # Quartier noble / Aristocratique

    # === MILIEUX RURAUX / NOMADE (Équitation forte) ===
    7: [1, 31, 7, 8, 10, 32],        # Village rural
    8: [1, 25, 26, 34, 2, 35],       # Village côtier
    9: [7, 8, 9, 1, 31, 4],          # Village forestier
    10: [10, 11, 12, 1, 19, 20],     # Village de montagne
    11: [1, 31, 32, 7, 8, 10],       # Hameau agricole
    19: [1, 31, 32, 8, 10, 19],      # Tribu nomade          → très forte équitation
    20: [1, 31, 10, 4, 8, 30],       # Colonie frontalière

    # === AUTRES ===
    14: [13, 14, 15, 1, 31, 8],      # Caravansérail / Oasis
    15: [1, 10, 11, 6, 4, 30],       # Avant-poste militaire
    16: [10, 11, 6, 20, 1, 12],      # Camp minier
    26: [10, 11, 12, 20, 6, 1],      # Forteresse naine
    30: [30, 28, 4, 1, 6, 79],       # Poste de commerce isolé

    # Fallback
    0: [1, 4, 6, 28, 30, 7]
}

# =============================================
# FONCTION DE GÉNÉRATION
# =============================================
def generate_active_skills(
    region_id: int,
    ethnicity: str,
    settlement_type: int = 0,
    num_skills: int = 5
) -> Dict[str, str]:
    """Génère 5 compétences actives en mélangeant ethnie + région + settlement"""
    
    skills = {}
    
    eth_pool = ethnicity_active_pool.get(ethnicity, [1, 4, 6, 28, 30])
    reg_pool = region_active_pool.get(region_id, list(range(1, 37)))
    bias_pool = settlement_skill_bias.get(settlement_type, [1, 4, 6, 28, 30])

    combined_pool = eth_pool * 2 + reg_pool * 3 + bias_pool * 2

    attempts = 0
    while len(skills) < num_skills and attempts < 100:
        idx = random.choice(combined_pool)
        if 1 <= idx <= len(active_skills_list):
            skill_name = active_skills_list[idx - 1]
            if skill_name not in skills:
                skills[skill_name] = "Connue"
        attempts += 1

    # Fallback si pas assez de compétences
    if len(skills) < num_skills:
        for skill_name in active_skills_list:
            if skill_name not in skills:
                skills[skill_name] = "Connue"
                if len(skills) >= num_skills:
                    break

    return skills