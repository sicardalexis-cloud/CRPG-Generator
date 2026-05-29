# settlement_data.py
import random
from typing import Tuple, Dict

# =============================================
# TYPES D'IMPLANTATION
# =============================================
settlement_types = {
    1: "Metropolis",
    2: "Major Port City",
    3: "Major Trade City",
    4: "Fortified City",
    5: "Large Town",
    6: "Small Town",
    7: "Rural Village",
    8: "Fishing Village",
    9: "Forest Village",
    10: "Mountain Village",
    11: "Farming Hamlet",
    12: "Isolated Hamlet",
    13: "Isolated Farmstead",
    14: "Caravan Oasis",
    15: "Military Outpost",
    16: "Mining Camp",
    17: "Remote Monastery",
    18: "Logging Camp",
    19: "Nomad Camp",
    20: "Frontier Colony",
    21: "Smuggler's Port",
    22: "Inhabited Ruins",
    23: "Underdark City",
    24: "Isolated Tower",
    25: "Lake Village",
    26: "Dwarven Fortress",
    27: "Elven Enclave",
    28: "Holy Site",
    29: "Permanent Encampment",
    30: "Remote Trading Post"
}

# =============================================
# PROBABILITÉS DE TYPES D'IMPLANTATION PAR RÉGION
# =============================================
origin_settlement_weights: Dict[int, Dict[int, int]] = {
    # === Régions Urbaines / Marchandes ===
    1: {1: 25, 2: 30, 3: 20, 5: 15, 14: 5, 21: 5},           # Calimshan
    2: {3: 30, 5: 25, 6: 15, 7: 10, 13: 10, 14: 5, 21: 5},    # Amn
    3: {4: 20, 5: 25, 6: 20, 7: 15, 10: 10, 13: 5, 17: 5},    # Tethyr
    4: {2: 35, 5: 25, 6: 15, 8: 15, 21: 10},                  # Baldur's Gate
    5: {1: 40, 2: 25, 5: 20, 6: 10, 15: 5},                   # Waterdeep
    6: {3: 35, 5: 25, 6: 20, 21: 15, 13: 5},                  # Sembia
    7: {4: 30, 5: 25, 6: 20, 7: 10, 13: 10, 17: 5},           # Cormyr
    8: {5: 25, 6: 25, 7: 20, 8: 15, 9: 10, 18: 5},            # Chondath

    # === Régions Côtières / Maritimes ===
    9: {2: 30, 5: 20, 8: 20, 21: 15, 25: 10, 30: 5},          # Vilhon Reach
    10: {5: 25, 6: 20, 7: 20, 8: 15, 13: 10, 18: 10},         # Turmish
    11: {5: 25, 6: 25, 7: 20, 8: 15, 21: 10, 25: 5},          # Chessenta
    12: {1: 20, 3: 25, 5: 20, 14: 15, 7: 10, 19: 10},         # Mulhorand
    13: {4: 20, 5: 25, 6: 20, 15: 15, 20: 10, 27: 10},        # Unther
    14: {7: 25, 9: 20, 10: 15, 17: 15, 18: 15, 19: 10},       # Rashemen
    15: {4: 25, 6: 20, 7: 20, 10: 15, 13: 10, 15: 10},        # Damara
    16: {5: 25, 6: 20, 8: 20, 2: 15, 21: 10, 25: 10},         # Impiltur
    17: {5: 20, 6: 25, 7: 20, 9: 15, 18: 10, 27: 10},         # Thesk
    18: {4: 25, 5: 20, 6: 20, 15: 15, 20: 10, 27: 10},        # Moonsea
    19: {2: 35, 5: 25, 8: 20, 21: 15, 22: 5},                 # Luskan
    20: {2: 30, 5: 25, 6: 20, 8: 15, 9: 5, 18: 5},            # Neverwinter
    21: {10: 30, 11: 25, 12: 20, 18: 15, 30: 10},             # Icewind Dale
    22: {8: 40, 2: 20, 11: 15, 12: 15, 25: 10},               # Moonshae Isles
    23: {10: 35, 11: 25, 12: 20, 19: 15, 30: 5},              # Sossal

    # === Régions Sauvages / Nord ===
    41: {10: 25, 11: 25, 12: 20, 18: 15, 13: 10, 30: 5},      # Le Nord
    42: {19: 55, 11: 20, 12: 15, 30: 10},                     # Uthgardt Tribes

    # === Régions Elfiques / Forestières ===
    25: {27: 35, 9: 25, 17: 15, 24: 15, 1: 10},               # Evermeet
    26: {27: 45, 9: 25, 11: 15, 17: 10, 30: 5},               # Cormanthor
    27: {9: 40, 11: 25, 18: 20, 12: 10, 30: 5},               # High Forest
    28: {9: 40, 11: 30, 12: 20, 18: 5, 30: 5},                # Moonwood
    29: {9: 35, 7: 25, 8: 20, 11: 15, 18: 5},                 # Wealdath
    98: {9: 40, 11: 25, 12: 20, 18: 10, 30: 5},               # Luirwood

    # === Régions Naines ===
    31: {26: 35, 4: 25, 10: 20, 16: 15, 23: 5},               # Citadel Adbar
    32: {26: 35, 4: 25, 10: 20, 16: 15, 23: 5},               # Mithral Hall
    33: {26: 40, 10: 25, 12: 20, 16: 10, 23: 5},              # Great Rift
    34: {26: 35, 10: 25, 12: 20, 16: 15, 23: 5},              # Ironmaster
    86: {26: 40, 10: 25, 12: 20, 16: 10, 23: 5},              # Citadelles du Nord

    # === Régions Souterraines ===
    39: {23: 50, 18: 20, 12: 15, 30: 10, 16: 5},              # Underdark
    87: {23: 65, 18: 20, 30: 10, 12: 5},                      # Cité Drow
    88: {23: 45, 18: 25, 30: 20, 12: 10},                     # Cité Souterraine Mixte
    93: {23: 40, 16: 25, 12: 20, 18: 15},                     # Gracklstugh

    # === Régions Désertiques / Arides ===
    83: {14: 40, 11: 25, 12: 20, 7: 10, 30: 5},               # Bedine

    # === Régions Exotiques / Autres ===
    24: {9: 35, 8: 25, 18: 20, 20: 10, 30: 10},               # Chult
    42: {19: 60, 11: 20, 12: 15, 30: 5},                      # Uthgardt
    106: {14: 30, 2: 25, 5: 20, 3: 15, 7: 10},                # Zakharans
    119: {1: 25, 5: 25, 6: 20, 7: 15, 9: 15},                 # Kara-Tur

    # === Régions récentes (82+) ===
    30: {5: 25, 6: 25, 7: 20, 13: 15, 18: 10, 30: 5},         # Lantan
    35: {7: 30, 9: 25, 11: 20, 18: 15, 30: 10},               # Luiren
    36: {4: 25, 5: 25, 6: 20, 10: 15, 13: 10, 30: 5},         # Vaasa
    37: {10: 30, 11: 25, 12: 20, 18: 15, 30: 10},             # Spine of the World
    38: {9: 40, 11: 25, 17: 15, 24: 15, 30: 5},               # Star Mounts
    40: {14: 35, 11: 25, 12: 20, 7: 15, 30: 5},               # Anauroch
    43: {1: 25, 4: 25, 5: 20, 15: 15, 17: 15},                # Thay
    44: {9: 35, 11: 25, 18: 20, 27: 15, 30: 5},               # Aglarond
    45: {9: 40, 11: 25, 12: 20, 18: 10, 30: 5},               # Silver Marches
    46: {7: 30, 9: 25, 11: 20, 18: 15, 30: 10},               # The Dalelands
    47: {15: 30, 16: 25, 8: 20, 9: 15, 30: 10},               # The Shaar
    48: {2: 30, 8: 25, 21: 20, 25: 15, 30: 10},               # Lake of Steam
    49: {5: 25, 6: 25, 7: 20, 13: 15, 30: 10},                # Border Kingdoms
    50: {19: 40, 15: 25, 11: 20, 30: 15},                     # Hordelands
    51: {4: 25, 5: 25, 6: 20, 15: 15, 20: 15},                # Old Empires
    52: {9: 30, 11: 25, 18: 20, 30: 15, 19: 10},              # Unapproachable East
    53: {5: 25, 6: 25, 7: 20, 13: 15, 30: 10},                # Western Heartlands
    54: {2: 35, 8: 25, 21: 20, 25: 15, 30: 5},                # Sword Coast
    55: {10: 30, 11: 25, 12: 20, 18: 15, 30: 10},             # Sword Coast North
    56: {2: 30, 8: 25, 21: 20, 25: 15, 30: 10},               # Dragon Coast
    57: {10: 35, 12: 25, 18: 20, 30: 15, 11: 5},              # Great Glacier
    58: {25: 35, 26: 25, 2: 20, 21: 15, 30: 5},               # Inner Sea
    59: {1: 30, 5: 25, 6: 20, 15: 15, 30: 10},                # Halruaa
    60: {9: 35, 8: 25, 18: 20, 20: 15, 30: 5},                # Dambrath
    61: {7: 30, 9: 25, 11: 20, 18: 15, 30: 10},               # Estagund
    62: {3: 30, 5: 25, 6: 20, 13: 15, 30: 10},                # Var the Golden
    63: {3: 25, 5: 25, 6: 20, 7: 15, 13: 10, 30: 5},          # Shaarmid
    64: {9: 35, 8: 25, 18: 20, 20: 15, 30: 5},                # Thindol
    65: {9: 35, 8: 25, 18: 20, 20: 15, 30: 5},                # Samarach
    66: {9: 35, 8: 25, 18: 20, 20: 10, 30: 10},               # Tashalar
    67: {9: 30, 8: 25, 18: 20, 20: 15, 30: 10},               # The Shining South
    68: {5: 25, 6: 25, 7: 20, 13: 15, 30: 10},                # Ymber
    69: {8: 35, 2: 25, 21: 20, 25: 15, 30: 5},                # Nelanther Isles
    70: {25: 35, 26: 25, 8: 20, 21: 15, 30: 5},               # The Whalebones
    71: {25: 40, 26: 30, 21: 20, 30: 10},                     # The Trackless Sea
    72: {10: 35, 12: 25, 18: 20, 30: 15, 11: 5},              # The Cold Lands
    73: {14: 35, 11: 25, 12: 20, 19: 15, 30: 5},              # The Endless Wastes
    74: {9: 40, 11: 25, 18: 20, 30: 10, 12: 5},               # The Great Dale
    75: {1: 25, 4: 25, 5: 20, 15: 15, 17: 15},                # The Plateau of Thay
    76: {5: 25, 6: 25, 7: 20, 13: 15, 30: 10},                # The Easting Reach
    77: {9: 40, 11: 25, 18: 20, 30: 10, 12: 5},               # The Forgotten Forest
    78: {10: 30, 11: 25, 12: 20, 18: 15, 30: 10},             # The Lone Rock
    79: {10: 30, 11: 25, 12: 20, 18: 15, 30: 10},             # The Reaching Woods
    80: {10: 35, 12: 25, 18: 20, 26: 15, 30: 5},              # The Thunder Peaks
    81: {15: 30, 16: 25, 8: 20, 9: 15, 30: 10},               # The Ride
    82: {9: 35, 11: 25, 18: 20, 27: 15, 30: 5},               # Aglarondine

    # === Régions manquantes complétées ===
    84: {26: 40, 4: 25, 16: 20, 12: 10, 23: 5},               # Barakuir
    85: {9: 40, 11: 25, 30: 15, 19: 10, 12: 10},              # Chondalwood
    89: {2: 30, 8: 25, 21: 20, 25: 15, 30: 10},               # Eauprofonde / Côte des Épées
    90: {10: 35, 12: 25, 18: 20, 26: 15, 30: 5},              # Épine dorsale du monde
    91: {9: 45, 11: 25, 12: 15, 30: 10, 19: 5},               # Forêt d’Amtar / Methwood
    92: {26: 40, 10: 25, 12: 20, 16: 10, 23: 5},              # Forteresses isolées
    94: {26: 45, 10: 25, 12: 20, 16: 10},                     # Grande Faille
    95: {10: 30, 12: 25, 18: 20, 30: 15, 11: 10},             # Grand Glacier
    96: {10: 35, 12: 25, 18: 20, 30: 15, 11: 5},              # Glacière éternelle
    97: {2: 35, 8: 30, 21: 20, 25: 10, 30: 5},                # Ruathym
    99: {27: 40, 9: 30, 17: 15, 24: 10, 1: 5},                # Myth Drannor
    100: {27: 45, 9: 25, 17: 15, 24: 10, 1: 5},               # Evereska
    101: {10: 30, 11: 25, 12: 20, 18: 15, 30: 10},            # Valbise
    102: {26: 35, 16: 25, 10: 20, 12: 15, 4: 5},              # Vallée de la Flamme
    103: {7: 30, 6: 25, 11: 20, 13: 15, 30: 10},              # Les Vaux
    104: {5: 25, 6: 25, 7: 20, 13: 15, 30: 10},               # Vast
    105: {9: 35, 8: 25, 18: 20, 20: 10, 30: 10},              # Jungle de Mhair
    107: {10: 30, 19: 25, 12: 20, 18: 15, 30: 10},            # Pics Gris
    108: {23: 40, 18: 25, 9: 15, 30: 10, 12: 10},             # Outreterre tropicale
    109: {9: 35, 11: 25, 18: 20, 12: 15, 30: 5},              # Forêts du Nord (Gnomes)
    110: {27: 40, 9: 30, 1: 15, 17: 10, 24: 5},               # Éternelle-Rencontre
    111: {5: 25, 6: 25, 4: 20, 10: 15, 13: 10, 30: 5},        # Lunargent
    112: {9: 40, 11: 25, 18: 20, 30: 10, 12: 5},              # Bois de Yuir
    113: {10: 30, 19: 25, 12: 20, 18: 15, 30: 10},            # Montagnes du Shaar
    114: {9: 45, 11: 25, 19: 15, 30: 10, 12: 5},              # Vil Adanrath
    115: {4: 30, 5: 25, 26: 20, 15: 15, 20: 10},              # Tymanther
    116: {10: 35, 12: 25, 15: 20, 26: 15, 30: 5},             # Icerim Mountains
    117: {10: 35, 12: 25, 15: 20, 26: 15, 30: 5},             # Montagnes Theskiennes
    118: {10: 35, 12: 25, 15: 20, 26: 15, 30: 5},             # Montagnes de Cuivre
    120: {23: 50, 18: 25, 12: 15, 30: 10},                    # Pics de Mir
    121: {9: 40, 11: 25, 18: 20, 30: 10, 12: 5},              # Bois de Shaar
    122: {23: 45, 18: 25, 12: 15, 30: 10, 16: 5},             # Outreterre profonde

    # === Régions restantes (123 à 133) ===
    123: {19: 40, 9: 25, 11: 15, 30: 15, 18: 5},              # Lycanthropes
    124: {15: 35, 16: 25, 8: 20, 9: 15, 30: 5},               # Wemics
    125: {28: 40, 29: 25, 6: 15, 30: 15, 18: 5},              # Yuan-ti
    126: {15: 40, 16: 25, 8: 20, 9: 10, 30: 5},               # Centaure
    127: {18: 35, 8: 25, 9: 20, 30: 15, 2: 5},                # Homme-lézard
    128: {23: 35, 10: 25, 19: 20, 6: 15, 30: 5},              # Tanarukks
    129: {27: 40, 9: 25, 4: 15, 30: 15, 6: 5},                # Fey’ri
    130: {23: 45, 24: 25, 30: 20, 18: 10},                    # Sagespectres
    131: {4: 30, 5: 25, 26: 20, 15: 15, 30: 10},              # Vaillants
    132: {23: 40, 22: 25, 24: 20, 30: 15},                    # Kir-lanan
    133: {23: 45, 24: 25, 30: 20, 18: 10},                    # Reflets (Shades)

    # === Valeur par défaut ===
    0: {5: 25, 6: 25, 7: 20, 11: 15, 12: 15}                  # Autre / Voyageur
}


# =============================================
# FONCTION PRINCIPALE
# =============================================
def get_random_settlement(region_id: int) -> Tuple[str, str]:
    """Retourne (nom_de_la_région, type_d_implantation)"""
    from origin_data import region_names
    
    region_name = region_names.get(region_id, "Région inconnue")
    
    weights = origin_settlement_weights.get(region_id, origin_settlement_weights[0])
    
    settlement_idx = random.choices(
        list(weights.keys()),
        weights=list(weights.values()),
        k=1
    )[0]
    
    # Robust fallback: if invalid ID, pick a random valid one
    if settlement_idx not in settlement_types:
        valid_ids = list(settlement_types.keys())
        settlement_idx = random.choice(valid_ids)
    
    settlement_name = settlement_types[settlement_idx]
    
    return region_name, settlement_name