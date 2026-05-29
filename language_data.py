# language_data.py
import random
from typing import List, Dict

# =============================================
# LISTE COMPLÈTE DES LANGUES
# =============================================
all_languages = [
    "Chondathan", "Elfique", "Nain", "Illuskan", "Orc", "Goblin", "Draconique",
    "Undercommon", "Céleste", "Infernal", "Abyssal", "Sylvestre", "Géant",
    "Auran", "Aquan", "Ignan", "Shaaran", "Tuigan", "Rashemi", "Mulhorandi",
    "Untheric", "Chessentan", "Dambrathan", "Halruaan", "Shou", "Thindol",
    "Samarach", "Tashalan", "Bedine", "Ulutiun", "Sossrim", "Aglarondan",
    "Cormyrian", "Sembian", "Turmish", "Impilturan", "Theskian", "Vaasan",
    "Nar", "Reghed", "Yuan-ti", "Centaur", "Wemic", "Maztican", "Kara-Turan",
    "Netherese", "Thorass", "Chultan", "Luiren", "Moonshae", "Northlander",
    "Arkaiun", "Durpari", "Talfir", "Imaskari", "Raumviran", "Lantanna",
    "Gur", "Ffolk", "Elven High Speech", "Drow Sign Language", "Thieves' Cant",
    "Druidic"
]

# =============================================
# LANGUES DE BASE PAR ETHNIE
# =============================================
ethnicity_base_languages: Dict[str, List[str]] = {
    # ==================== HUMAINS ====================
    "Chondathan": ["Chondathan"],
    "Tethyrian": ["Tethyrian", "Chondathan"],
    "Calishite": ["Calishite", "Mulhorandi"],
    "Damaran": ["Damaran", "Chondathan"],
    "Illuskan": ["Illuskan"],
    "Mulan": ["Mulhorandi"],
    "Rashemi": ["Rashemi"],
    "Turami": ["Turami", "Chondathan"],
    "Uthgardt": ["Uthgardt", "Illuskan"],
    "Chultan": ["Chultan"],
    "Shaaran": ["Shaaran"],
    "Ffolk": ["Ffolk", "Chondathan"],
    "Sossrim": ["Sossrim", "Illuskan"],
    "Vaasan": ["Vaasan", "Illuskan"],
    "Arkaiun": ["Arkaiun"],
    "Durpari": ["Durpari"],
    "Imaskari": ["Imaskari", "Mulhorandi"],
    "Lantanna": ["Lantanna"],
    "Raumviran": ["Raumviran"],
    "Tashalan": ["Tashalan"],
    "Tuigan": ["Tuigan"],
    "Shou": ["Shou"],
    "Maztican": ["Maztican"],
    "Netherese": ["Netherese"],
    "Talfir": ["Talfir", "Chondathan"],
    "Ulutiun": ["Ulutiun"],
    "Reghedman": ["Reghed", "Illuskan"],

    # ==================== ELFES & DEMI-ELFES ====================
    "Elf Moon": ["Elfique"],
    "Elf Sun": ["Elfique"],
    "Elf Wood": ["Elfique"],
    "Elf Wild": ["Elfique"],
    "Elf Drow": ["Glifo (Drow)"],
    "Elf Sea": ["Elfique"],
    "Elf Star": ["Elfique"],
    "Elf Avariel": ["Elfique"],
    "Elf Lythari": ["Elfique"],
    "Half-Elf": ["Elfique", "Chondathan"],

    # Demi-Elfes spécifiques (standardisés)
    "Wood Half-elf": ["Elfique", "Chondathan"],
    "Moon Half-elf": ["Elfique", "Chondathan"],
    "Sun Half-elf": ["Elfique", "Chondathan"],
    "Wild Half-elf": ["Elfique", "Chondathan"],
    "Sea Half-elf": ["Elfique", "Chondathan"],
    "Drow Half-elf": ["Glifo (Drow)", "Chondathan"],

    # ==================== NAINS ====================
    "Nain": ["Nain"],
    "Shield Dwarf": ["Nain"],
    "Gold Dwarf": ["Nain"],
    "Gray Dwarf": ["Nain"],
    "Wild Dwarf": ["Nain"],
    "Arctic Dwarf": ["Nain"],
    "Urdunnir": ["Nain"],

    # ==================== AUTRES RACES ====================
    "Half-Orc": ["Orc"],
    "Orc": ["Orc"],
    "Gray Orc": ["Orc"],
    "Goblin": ["Goblin"],
    "Hobgoblin": ["Goblin"],
    "Yuan-ti Pureblood": ["Yuan-ti"],
    "Dragonborn": ["Draconique"],
    "Firbolg": ["Sylvestre"],
    "Kenku": ["Chondathan"],
    "Triton": ["Aquan"],
    "Lizardfolk": ["Draconique"],
    "Aarakocra": ["Auran"],
    "Goliath": ["Géant"],
    "Centaur": ["Sylvestre"],

    # ==================== DERNIÈRES BASE LANGUAGES (complétion) ====================
    "Aasimar":         ["Céleste"],
    "Air Genasi":      ["Auran"],
    "Earth Genasi":    ["Terran"],
    "Fire Genasi":     ["Ignan"],
    "Water Genasi":    ["Aquan"],

    "Avariel":         ["Elfique"],
    "Lythari":         ["Elfique"],

    "Drow":            ["Glifo (Drow)"],

    "Moon Elf":        ["Elfique"],
    "Sun Elf":         ["Elfique"],
    "Wood Elf":        ["Elfique"],
    "Wild Elf":        ["Elfique"],
    "Sea Elf":         ["Elfique"],
    "Star Elf":        ["Elfique"],

    "Bedine":          ["Midani"],
    "Nar":             ["Damaran"],
    "Gur":             ["Rashemi"],
    "Halruaan":        ["Halruaan"],

    "Lightfoot Halfling":  ["Chondathan"],
    "Strongheart Halfling": ["Chondathan"],
    "Ghostwise Halfling":  ["Chondathan"],

    "Forest Gnome":    ["Gnomish"],
    "Rock Gnome":      ["Gnomish"],

    "Half-Orc Mountain": ["Orc"],
    "Tiefling":        ["Infernal"],

    # ==================== DEFAULT ====================
    "Default": ["Chondathan"]
}

# =============================================
# LANGUES RÉGIONALES (1 à 133) - Version Complète
# =============================================
region_languages: Dict[int, List[str]] = {
    # 1-90 déjà présentes dans ta version précédente
    1: ["Chondathan"], 2: ["Chondathan"], 3: ["Chondathan"], 4: ["Chondathan"],
    5: ["Chondathan"], 6: ["Chondathan"], 7: ["Chondathan"], 8: ["Chondathan"],
    9: ["Chondathan"], 10: ["Chondathan"], 11: ["Chessentan"], 12: ["Mulhorandi"],
    13: ["Untheric"], 14: ["Rashemi"], 15: ["Chondathan"], 16: ["Chondathan"],
    17: ["Chondathan"], 18: ["Chondathan"], 19: ["Illuskan"], 20: ["Illuskan"],
    21: ["Illuskan"], 22: ["Illuskan"], 23: ["Illuskan"], 24: ["Chultan"],
    25: ["Elfique"], 26: ["Elfique"], 27: ["Elfique"], 28: ["Elfique"],
    29: ["Elfique"], 30: ["Chondathan"], 31: ["Nain"], 32: ["Nain"],
    33: ["Nain"], 34: ["Nain"], 35: ["Chondathan"], 36: ["Chondathan"],
    37: ["Illuskan"], 38: ["Elfique"], 39: ["Undercommon"], 40: ["Chondathan"],
    41: ["Illuskan"], 42: ["Illuskan"], 43: ["Thayan"], 44: ["Aglarondan"],
    45: ["Illuskan"], 46: ["Chondathan"], 47: ["Shaaran"], 48: ["Chondathan"],
    49: ["Chondathan"], 50: ["Tuigan"], 51: ["Mulhorandi"], 52: ["Chondathan"],
    53: ["Chondathan"], 54: ["Chondathan"], 55: ["Illuskan"], 56: ["Chondathan"],
    57: ["Illuskan"], 58: ["Chondathan"], 59: ["Halruaan"], 60: ["Dambrathan"],
    61: ["Dambrathan"], 62: ["Dambrathan"], 63: ["Shaaran"], 64: ["Thindol"],
    65: ["Samarach"], 66: ["Tashalan"], 67: ["Chondathan"], 68: ["Chondathan"],
    69: ["Chondathan"], 70: ["Illuskan"], 71: ["Illuskan"], 72: ["Illuskan"],
    73: ["Tuigan"], 74: ["Chondathan"], 75: ["Thayan"], 76: ["Chondathan"],
    77: ["Elfique"], 78: ["Illuskan"], 79: ["Chondathan"], 80: ["Illuskan"],
    81: ["Illuskan"], 82: ["Aglarondan"], 83: ["Bedine"], 84: ["Chondathan"],
    85: ["Chondathan"], 86: ["Nain"], 87: ["Glifo (Drow)"], 88: ["Undercommon"],
    89: ["Chondathan"], 90: ["Illuskan"],

    # === 91 à 133 ===
    91: ["Chondathan"],      # Forêt d’Amtar / Methwood
    92: ["Nain"],            # Forteresses isolées (Nains gris)
    93: ["Nain"],            # Gracklstugh
    94: ["Nain"],            # Grande Faille
    95: ["Illuskan"],        # Grand Glacier
    96: ["Illuskan"],        # Glacière éternelle
    97: ["Illuskan"],        # Îles de la mer inviolée / Ruathym
    98: ["Elfique"],         # Luirwood (Elfes sauvages)
    99: ["Elfique"],         # Myth Drannor / Cormanthyr
    100: ["Elfique"],        # Evereska
    101: ["Illuskan"],       # Valbise
    102: ["Nain"],           # Vallée de la Flamme
    103: ["Chondathan"],     # Vaux / Les Vaux
    104: ["Chondathan"],     # Vast
    105: ["Chultan"],        # Jungle de Mhair / Péninsule Lapalienne
    106: ["Maztican"],       # Zakharans
    107: ["Orc"],            # Pics Gris (Orcs)
    108: ["Undercommon"],    # Outreterre tropicale
    109: ["Chondathan"],     # Forêts du Nord / Hautes Terres (Gnomes)
    110: ["Elfique"],        # Éternelle-Rencontre (Evermeet)
    111: ["Illuskan"],       # Lunargent / Contrées du Nord
    112: ["Elfique"],        # Bois de Yuir
    113: ["Shaaran"],        # Montagnes du Shaar / Lapaliiya
    114: ["Elfique"],        # Vil Adanrath (Lythari)
    115: ["Draconique"],     # Tymanther (Drakeides)
    116: ["Géant"],          # Icerim Mountains (Goliath)
    117: ["Géant"],          # Montagnes Theskiennes (Goliath)
    118: ["Géant"],          # Montagnes de Cuivre (Goliath)
    119: ["Shou"],           # Kara-Tur
    120: ["Glifo (Drow)"],   # Pics de Mir (Drows)
    121: ["Elfique"],        # Bois de Shaar (Elfes sauvages)
    122: ["Undercommon"],    # Outreterre profonde (Orogs)
    123: ["Sylvestre"],      # Lycanthropes
    124: ["Sylvestre"],      # Wemics
    125: ["Yuan-ti"],        # Yuan-ti
    126: ["Sylvestre"],      # Centaure
    127: ["Draconique"],     # Homme-lézard
    128: ["Abyssal"],        # Tanarukks
    129: ["Elfique"],        # Fey’ri
    130: ["Undercommon"],    # Sagespectres
    131: ["Chondathan"],     # Vaillants
    132: ["Undercommon"],    # Kir-lanan
    133: ["Shadow Weave"],   # Reflets (Shades)

    # Fallback
    0: ["Chondathan"]
}

# =============================================
# POOL DE LANGUES BONUS PAR ETHNIE (cultures spécifiques)
# =============================================
ethnicity_bonus_languages: Dict[str, List[str]] = {
    # === Humains ===
    "Chondathan": ["Illuskan", "Thorass", "Chessentan", "Turmish", "Cormyrian"],
    "Tethyrian": ["Elfique", "Illuskan", "Thorass", "Cormyrian", "Sembian"],
    "Calishite": ["Tashalan", "Infernal", "Thorass", "Halruaan", "Lantanna"],
    "Damaran": ["Chondathan", "Illuskan", "Vaasan", "Nar", "Reghed"],
    "Illuskan": ["Chondathan", "Reghed", "Northlander", "Vaasan", "Sossrim"],
    "Mulan": ["Mulhorandi", "Untheric", "Chessentan", "Thayan", "Rashemi"],
    "Rashemi": ["Rashemi", "Thayan", "Mulhorandi", "Infernal", "Chondathan"],
    "Turami": ["Chondathan", "Turmish", "Chessentan", "Halruaan", "Lantanna"],
    "Uthgardt": ["Illuskan", "Reghed", "Géant", "Northlander", "Vaasan"],
    "Chultan": ["Chultan", "Shaaran", "Yuan-ti", "Tashalan", "Chondathan"],
    "Shaaran": ["Shaaran", "Chultan", "Dambrathan", "Yuan-ti", "Tashalan"],
    "Ffolk": ["Chondathan", "Illuskan", "Moonshae", "Northlander", "Sossrim"],
    "Sossrim": ["Illuskan", "Sossrim", "Northlander", "Reghed", "Vaasan"],
    "Vaasan": ["Illuskan", "Vaasan", "Nar", "Reghed", "Northlander"],
    "Arkaiun": ["Chondathan", "Arkaiun", "Dambrathan", "Shaaran", "Thindol"],
    "Durpari": ["Chondathan", "Durpari", "Halruaan", "Lantanna", "Tashalan"],

    # === Elfes & Demi-elfes ===
    "Elf Moon": ["Elfique", "Sylvestre", "Elven High Speech", "Thorass", "Druidic"],
    "Elf Sun": ["Elfique", "Sylvestre", "Elven High Speech", "Thorass", "Céleste"],
    "Elf Wood": ["Elfique", "Sylvestre", "Druidic", "Elven High Speech", "Auran"],
    "Elf Wild": ["Elfique", "Sylvestre", "Druidic", "Elven High Speech", "Géant"],
    "Elf Drow": ["Glifo (Drow)", "Undercommon", "Draconique", "Abyssal", "Infernal"],
    "Elf Sea": ["Elfique", "Aquan", "Sylvestre", "Chondathan", "Auran"],
    "Elf Star": ["Elfique", "Elven High Speech", "Sylvestre", "Céleste", "Thorass"],
    "Elf Avariel": ["Elfique", "Auran", "Sylvestre", "Elven High Speech", "Céleste"],
    "Elf Lythari": ["Elfique", "Sylvestre", "Druidic", "Elven High Speech", "Géant"],

    # Demi-Elfes spécifiques (standardisés)
    "Wood Half-elf": ["Elfique", "Sylvestre", "Druidic", "Elven High Speech", "Chondathan"],
    "Moon Half-elf": ["Elfique", "Sylvestre", "Elven High Speech", "Thorass", "Chondathan"],
    "Sun Half-elf": ["Elfique", "Sylvestre", "Elven High Speech", "Céleste", "Chondathan"],
    "Wild Half-elf": ["Elfique", "Sylvestre", "Druidic", "Géant", "Chondathan"],
    "Sea Half-elf": ["Elfique", "Aquan", "Sylvestre", "Chondathan", "Auran"],
    "Drow Half-elf": ["Glifo (Drow)", "Undercommon", "Abyssal", "Infernal", "Chondathan"],

    # "Demi-elfe" supprimé (nom obsolète après standardisation)

    # === Nains ===
    "Nain": ["Nain", "Géant", "Undercommon", "Thorass", "Chondathan"],
    "Shield Dwarf": ["Nain", "Géant", "Undercommon", "Thorass", "Illuskan"],
    "Gold Dwarf": ["Nain", "Géant", "Thorass", "Chondathan", "Undercommon"],
    "Gray Dwarf": ["Nain", "Undercommon", "Infernal", "Géant", "Orc"],
    "Wild Dwarf": ["Nain", "Sylvestre", "Druidic", "Géant", "Elfique"],
    "Arctic Dwarf": ["Nain", "Illuskan", "Géant", "Undercommon", "Reghed"],
    "Urdunnir": ["Nain", "Undercommon", "Géant", "Thorass", "Infernal"],

    # === Autres races ===
    "Half-Orc": ["Orc", "Goblin", "Undercommon", "Chondathan", "Illuskan"],
    "Orc": ["Orc", "Goblin", "Undercommon", "Infernal", "Géant"],
    "Gray Orc": ["Orc", "Undercommon", "Goblin", "Infernal", "Géant"],
    "Goblin": ["Goblin", "Orc", "Undercommon", "Infernal", "Chondathan"],
    "Hobgoblin": ["Goblin", "Infernal", "Orc", "Undercommon", "Draconique"],
    "Yuan-ti Pureblood": ["Yuan-ti", "Draconique", "Abyssal", "Infernal", "Chondathan"],
    "Dragonborn": ["Draconique", "Infernal", "Céleste", "Géant", "Auran"],
    "Firbolg": ["Sylvestre", "Druidic", "Géant", "Elfique", "Elven High Speech"],
    "Kenku": ["Chondathan", "Thieves' Cant", "Illuskan", "Elfique", "Undercommon"],
    "Triton": ["Aquan", "Céleste", "Elfique", "Chondathan", "Draconique"],
    "Lizardfolk": ["Draconique", "Yuan-ti", "Undercommon", "Abyssal", "Chondathan"],
    "Aarakocra": ["Auran", "Sylvestre", "Elfique", "Céleste", "Druidic"],
    "Goliath": ["Géant", "Chondathan", "Illuskan", "Nain", "Undercommon"],
    "Centaur": ["Sylvestre", "Elven High Speech", "Druidic", "Elfique", "Géant"],

    # === Nouvelles entrées pour réduire les fallbacks vers le Default générique ===
    "Air Genasi":      ["Auran", "Chondathan", "Thorass", "Illuskan", "Céleste"],
    "Earth Genasi":    ["Terran", "Chondathan", "Nain", "Thorass", "Draconique"],
    "Fire Genasi":     ["Ignan", "Calishite", "Thorass", "Draconique", "Chondathan"],
    "Water Genasi":    ["Aquan", "Chondathan", "Turami", "Thorass", "Draconique"],

    "Lightfoot Halfling":  ["Chondathan", "Illuskan", "Thorass", "Gnomish", "Druidic"],
    "Strongheart Halfling": ["Chondathan", "Damaran", "Thorass", "Gnomish", "Druidic"],

    # Humains obscurs / régionaux encore manquants
    "Bedine":      ["Midani", "Shaaran", "Chondathan", "Thorass", "Druidic"],
    "Nar":         ["Damaran", "Chondathan", "Rashemi", "Thorass", "Vaasan"],
    "Halruaan":    ["Halruaan", "Chondathan", "Thorass", "Lantanna", "Mulhorandi"],
    "Imaskari":    ["Imaskari", "Chondathan", "Mulhorandi", "Thorass", "Draconique"],
    "Lantanna":    ["Lantanna", "Chondathan", "Thorass", "Calishite", "Illuskan"],
    "Maztican":    ["Maztican", "Nexalan", "Chultan", "Thorass", "Tashalan"],
    "Shou":        ["Shou", "Tuigan", "Chondathan", "Thorass", "Draconique"],
    "Talfir":      ["Talfir", "Chondathan", "Tethyrian", "Thorass", "Druidic"],
    "Tashalan":    ["Tashalan", "Chultan", "Calishite", "Thorass", "Maztican"],
    "Drow":        ["Glifo (Drow)", "Undercommon", "Abyssal", "Infernal", "Draconique"],

    # Elfes principaux (qui manquaient en bonus)
    "Moon Elf":    ["Elfique", "Sylvestre", "Elven High Speech", "Thorass", "Druidic"],
    "Sun Elf":     ["Elfique", "Elven High Speech", "Sylvestre", "Céleste", "Thorass"],
    "Wood Elf":    ["Elfique", "Sylvestre", "Druidic", "Elven High Speech", "Thorass"],
    "Wild Elf":    ["Elfique", "Sylvestre", "Druidic", "Géant", "Thorass"],
    "Sea Elf":     ["Elfique", "Aquan", "Sylvestre", "Chondathan", "Thorass"],
    "Star Elf":    ["Elfique", "Elven High Speech", "Sylvestre", "Céleste", "Thorass"],

    # === Dernières 14 (fin de la passe bonus languages) ===
    "Aasimar":         ["Céleste", "Thorass", "Chondathan", "Elven High Speech", "Draconique"],
    "Avariel":         ["Elfique", "Auran", "Elven High Speech", "Céleste", "Sylvestre"],
    "Lythari":         ["Elfique", "Sylvestre", "Druidic", "Géant", "Elven High Speech"],
    "Forest Gnome":    ["Gnomish", "Sylvestre", "Druidic", "Elfique", "Thorass"],
    "Rock Gnome":      ["Gnomish", "Nain", "Thorass", "Draconique", "Chondathan"],
    "Ghostwise Halfling": ["Druidic", "Sylvestre", "Gnomish", "Uthgardt", "Thorass"],
    "Gur":             ["Rashemi", "Damaran", "Chondathan", "Thorass", "Shaaran"],
    "Half-Orc Mountain": ["Orc", "Géant", "Illuskan", "Uthgardt", "Thorass"],
    "Netherese":       ["Netherese", "Thorass", "Draconique", "High Netherese", "Céleste"],
    "Raumviran":       ["Raumviran", "Damaran", "Shou", "Thorass", "Chondathan"],
    "Reghedman":       ["Reghed", "Illuskan", "Géant", "Uthgardt", "Thorass"],
    "Tiefling":        ["Infernal", "Abyssal", "Thorass", "Chondathan", "Draconique"],
    "Tuigan":          ["Tuigan", "Shou", "Géant", "Thorass", "Chondathan"],
    "Ulutiun":         ["Uluik", "Illuskan", "Géant", "Thorass", "Sossrim"],

    # === Default ===
    "Default": ["Chondathan", "Illuskan", "Elfique", "Thorass", "Sylvestre"]
}

# =============================================
# POOL DE LANGUES BONUS PAR RÉGION (5 langues par région)
# =============================================
region_bonus_languages: Dict[int, List[str]] = {
    # === 1-20 : Cœur des Royaumes & Ouest ===
    1: ["Chondathan", "Tashalan", "Infernal", "Thorass", "Halruaan"],      # Calimshan
    2: ["Chondathan", "Thorass", "Illuskan", "Sembian", "Chessentan"],     # Amn
    3: ["Chondathan", "Thorass", "Elfique", "Halruaan", "Lantanna"],       # Tethyr
    4: ["Chondathan", "Illuskan", "Thorass", "Druidic", "Elven High Speech"], # Baldur's Gate
    5: ["Thorass", "Illuskan", "Elfique", "Druidic", "Chondathan"],        # Waterdeep
    6: ["Chondathan", "Sembian", "Thorass", "Cormyrian", "Chessentan"],    # Sembia
    7: ["Cormyrian", "Thorass", "Chessentan", "Elven High Speech", "Sembian"], # Cormyr
    8: ["Chondathan", "Chessentan", "Turmish", "Thorass", "Infernal"],     # Chondath
    9: ["Chondathan", "Chessentan", "Turmish", "Halruaan", "Thorass"],     # Vilhon Reach
    10: ["Chondathan", "Turmish", "Chessentan", "Halruaan", "Thorass"],    # Turmish
    11: ["Chessentan", "Mulhorandi", "Untheric", "Infernal", "Thayan"],    # Chessenta
    12: ["Mulhorandi", "Untheric", "Chessentan", "Thayan", "Infernal"],    # Mulhorand
    13: ["Untheric", "Mulhorandi", "Chessentan", "Infernal", "Thayan"],    # Unther
    14: ["Rashemi", "Thayan", "Mulhorandi", "Infernal", "Chondathan"],     # Rashemen
    15: ["Chondathan", "Illuskan", "Vaasan", "Nar", "Reghed"],             # Damara
    16: ["Chondathan", "Impilturan", "Theskian", "Chessentan", "Thorass"], # Impiltur
    17: ["Chondathan", "Theskian", "Rashemi", "Thayan", "Illuskan"],       # Thesk
    18: ["Chondathan", "Illuskan", "Thorass", "Sembian", "Druidic"],       # Moonsea
    19: ["Illuskan", "Reghed", "Northlander", "Vaasan", "Géant"],          # Luskan
    20: ["Illuskan", "Northlander", "Reghed", "Chondathan", "Thorass"],    # Neverwinter

    # === 21-40 ===
    21: ["Illuskan", "Reghed", "Northlander", "Géant", "Sossrim"],         # Icewind Dale
    22: ["Illuskan", "Moonshae", "Northlander", "Chondathan", "Elfique"],  # Moonshae Isles
    23: ["Illuskan", "Sossrim", "Northlander", "Géant", "Reghed"],         # Sossal
    24: ["Chultan", "Shaaran", "Yuan-ti", "Tashalan", "Chondathan"],       # Chult
    25: ["Elfique", "Sylvestre", "Elven High Speech", "Auran", "Céleste"], # Evermeet
    26: ["Elfique", "Sylvestre", "Elven High Speech", "Druidic", "Thorass"],# Cormanthor
    27: ["Elfique", "Sylvestre", "Druidic", "Elven High Speech", "Géant"], # High Forest
    28: ["Elfique", "Sylvestre", "Druidic", "Elven High Speech", "Auran"], # Moonwood
    29: ["Elfique", "Sylvestre", "Druidic", "Géant", "Elven High Speech"], # Wealdath
    30: ["Chondathan", "Lantanna", "Halruaan", "Thorass", "Infernal"],     # Lantan
    31: ["Nain", "Géant", "Undercommon", "Thorass", "Illuskan"],           # Citadel Adbar
    32: ["Nain", "Géant", "Undercommon", "Thorass", "Chondathan"],         # Mithral Hall
    33: ["Nain", "Géant", "Undercommon", "Thorass", "Infernal"],           # Great Rift
    34: ["Nain", "Géant", "Undercommon", "Illuskan", "Thorass"],           # Ironmaster
    35: ["Chondathan", "Luiren", "Halfling", "Thorass", "Elfique"],        # Luiren
    36: ["Chondathan", "Vaasan", "Illuskan", "Nar", "Reghed"],             # Vaasa
    37: ["Illuskan", "Géant", "Nain", "Reghed", "Northlander"],            # Spine of the World
    38: ["Elfique", "Sylvestre", "Auran", "Elven High Speech", "Géant"],   # Star Mounts
    39: ["Undercommon", "Draconique", "Glifo (Drow)", "Abyssal", "Infernal"], # Underdark
    40: ["Chondathan", "Bedine", "Thorass", "Infernal", "Shaaran"],        # Anauroch

    # === 41-70 ===
    41: ["Illuskan", "Reghed", "Northlander", "Vaasan", "Géant"],          # Le Nord
    42: ["Illuskan", "Uthgardt", "Géant", "Reghed", "Northlander"],        # Uthgardt
    43: ["Thayan", "Infernal", "Mulhorandi", "Chessentan", "Untheric"],    # Thay
    44: ["Aglarondan", "Elfique", "Chondathan", "Thorass", "Sylvestre"],   # Aglarond
    45: ["Illuskan", "Nain", "Géant", "Thorass", "Reghed"],                # Silver Marches
    46: ["Chondathan", "Elfique", "Thorass", "Druidic", "Sembian"],        # The Dalelands
    47: ["Shaaran", "Chultan", "Dambrathan", "Yuan-ti", "Tashalan"],       # The Shaar
    48: ["Chondathan", "Tashalan", "Infernal", "Halruaan", "Thorass"],     # Lake of Steam
    49: ["Chondathan", "Chessentan", "Turmish", "Infernal", "Thayan"],     # Border Kingdoms
    50: ["Tuigan", "Shou", "Géant", "Kara-Turan", "Chondathan"],           # Hordelands
    55: ["Illuskan", "Northlander", "Reghed", "Vaasan", "Géant"],          # Sword Coast North
    59: ["Halruaan", "Draconique", "Céleste", "Infernal", "Elfique"],      # Halruaa
    66: ["Tashalan", "Chultan", "Shaaran", "Yuan-ti", "Infernal"],         # Tashalar

    # === 71-100 ===
    86: ["Nain", "Géant", "Undercommon", "Chondathan", "Illuskan"],        # Citadelles du Nord
    87: ["Glifo (Drow)", "Undercommon", "Abyssal", "Infernal", "Draconique"], # Cité Drow
    100: ["Elfique", "Sylvestre", "Elven High Speech", "Auran", "Céleste"],# Evereska
    105: ["Chultan", "Shaaran", "Yuan-ti", "Tashalan", "Dambrathan"],      # Jungle Mhair
    107: ["Orc", "Goblin", "Undercommon", "Infernal", "Géant"],            # Pics Gris
    119: ["Shou", "Kara-Turan", "Tuigan", "Géant", "Chondathan"],          # Kara-Tur

    # === 120-133 ===
    120: ["Glifo (Drow)", "Undercommon", "Abyssal", "Infernal", "Draconique"], # Pics de Mir
    121: ["Shaaran", "Chultan", "Elfique", "Druidic", "Yuan-ti"],          # Bois de Shaar
    122: ["Undercommon", "Orc", "Goblin", "Infernal", "Draconique"],       # Outreterre profonde
    123: ["Sylvestre", "Druidic", "Elfique", "Géant", "Auran"],            # Lycanthropes
    124: ["Sylvestre", "Elven High Speech", "Druidic", "Géant", "Chondathan"], # Wemics
    125: ["Yuan-ti", "Draconique", "Abyssal", "Infernal", "Chondathan"],   # Yuan-ti
    126: ["Sylvestre", "Elven High Speech", "Druidic", "Elfique", "Géant"],# Centaure
    127: ["Draconique", "Yuan-ti", "Undercommon", "Abyssal", "Chondathan"],# Homme-lézard
    128: ["Abyssal", "Infernal", "Draconique", "Undercommon", "Orc"],      # Tanarukks
    129: ["Elfique", "Infernal", "Abyssal", "Draconique", "Sylvestre"],    # Fey’ri
    130: ["Undercommon", "Glifo (Drow)", "Infernal", "Abyssal", "Draconique"], # Sagespectres
    131: ["Chondathan", "Illuskan", "Thorass", "Sembian", "Cormyrian"],    # Vaillants
    132: ["Undercommon", "Glifo (Drow)", "Infernal", "Abyssal", "Draconique"], # Kir-lanan
    133: ["Shadow Weave", "Infernal", "Céleste", "Abyssal", "Thayan"],     # Reflets (Shades)

    # === RÉGIONS OBSCURES / MANQUANTES - Bonus languages plus intéressants ===
    # Sud et Royaumes du Sud
    51: ["Mulhorandi", "Untheric", "Chessentan", "Thayan", "Infernal"],     # Old Empires
    52: ["Aglarondan", "Rashemi", "Thayan", "Chondathan", "Elfique"],       # Unapproachable East
    53: ["Chondathan", "Tethyrian", "Illuskan", "Elfique", "Thorass"],      # Western Heartlands
    54: ["Chondathan", "Illuskan", "Thorass", "Tethyrian", "Elfique"],      # Sword Coast
    56: ["Chondathan", "Tethyrian", "Chessentan", "Thorass", "Infernal"],   # Dragon Coast
    57: ["Illuskan", "Reghed", "Géant", "Uluik", "Sossrim"],                # Great Glacier
    58: ["Chondathan", "Sembian", "Impilturan", "Theskian", "Thorass"],     # Inner Sea
    60: ["Dambrathan", "Chultan", "Shaaran", "Yuan-ti", "Infernal"],        # Dambrath
    61: ["Durpari", "Halruaan", "Chondathan", "Tashalan", "Thorass"],       # Estagund
    62: ["Durpari", "Chondathan", "Halruaan", "Thorass", "Lantanna"],       # Var the Golden
    63: ["Shaaran", "Chultan", "Dambrathan", "Tashalan", "Yuan-ti"],        # Shaarmid
    64: ["Thindol", "Chultan", "Tashalan", "Shaaran", "Dambrathan"],        # Thindol
    65: ["Samarach", "Chultan", "Tashalan", "Shaaran", "Infernal"],         # Samarach

    # Nord et Terres Froides
    67: ["Illuskan", "Northlander", "Reghed", "Géant", "Sossrim"],          # The Shining South (Nord)
    68: ["Illuskan", "Uluik", "Géant", "Sossrim", "Reghed"],                # Ymber
    69: ["Illuskan", "Northlander", "Chondathan", "Thorass", "Elfique"],    # Nelanther Isles
    70: ["Illuskan", "Northlander", "Géant", "Reghed", "Sossrim"],          # The Whalebones

    # Mers et zones isolées
    71: ["Illuskan", "Northlander", "Chondathan", "Elfique", "Thorass"],    # The Trackless Sea
    72: ["Illuskan", "Reghed", "Uluik", "Géant", "Sossrim"],                # The Cold Lands
    73: ["Tuigan", "Shou", "Géant", "Chondathan", "Thorass"],               # The Endless Wastes (bis)
    74: ["Chondathan", "Impilturan", "Theskian", "Rashemi", "Thorass"],     # The Great Dale
    75: ["Thayan", "Mulhorandi", "Infernal", "Chessentan", "Untheric"],     # The Plateau of Thay
    76: ["Chondathan", "Impilturan", "Theskian", "Aglarondan", "Thorass"],  # The Easting Reach
    77: ["Elfique", "Sylvestre", "Druidic", "Thorass", "Chondathan"],       # The Forgotten Forest
    78: ["Chondathan", "Illuskan", "Thorass", "Elfique", "Northlander"],    # The Lone Rock
    79: ["Chondathan", "Tethyrian", "Elfique", "Druidic", "Thorass"],       # The Reaching Woods
    80: ["Chondathan", "Sembian", "Cormyrian", "Thorass", "Géant"],         # The Thunder Peaks
    81: ["Chondathan", "Damaran", "Vaasan", "Illuskan", "Thorass"],         # The Ride
    82: ["Aglarondan", "Elfique", "Chondathan", "Sylvestre", "Thorass"],    # Aglarondine
    83: ["Bedine", "Midani", "Shaaran", "Chondathan", "Thorass"],           # Bedine
    84: ["Nain", "Géant", "Undercommon", "Thorass", "Illuskan"],            # Barakuir
    85: ["Chondathan", "Tethyrian", "Elfique", "Druidic", "Thorass"],       # Chondalwood

    # Zones souterraines et spéciales
    88: ["Nain", "Undercommon", "Géant", "Glifo (Drow)", "Draconique"],      # Cité Souterraine Mixte
    89: ["Chondathan", "Illuskan", "Thorass", "Elfique", "Nain"],            # Eauprofonde (eau profonde)
    90: ["Nain", "Géant", "Uluik", "Illuskan", "Reghed"],                    # Épine dorsale (Nains arctiques)

    # Forêts et régions sauvages
    91: ["Chultan", "Shaaran", "Elfique", "Druidic", "Yuan-ti"],             # Forêt d’Amtar / Methwood
    92: ["Nain", "Géant", "Undercommon", "Thorass", "Illuskan"],            # Forteresses isolées
    93: ["Nain", "Undercommon", "Glifo (Drow)", "Draconique", "Infernal"],   # Gracklstugh
    94: ["Nain", "Géant", "Undercommon", "Thorass", "Chondathan"],           # Grande Faille
    95: ["Illuskan", "Uluik", "Géant", "Reghed", "Sossrim"],                # Grand Glacier
    96: ["Illuskan", "Uluik", "Géant", "Reghed", "Sossrim"],                # Glacière éternelle
    97: ["Illuskan", "Northlander", "Chondathan", "Elfique", "Thorass"],    # Ruathym
    98: ["Chondathan", "Tethyrian", "Elfique", "Druidic", "Thorass"],       # Luirwood
    99: ["Elfique", "Sylvestre", "Elven High Speech", "Druidic", "Thorass"],# Myth Drannor

    # Zones exotiques et lointaines
    101: ["Chondathan", "Damaran", "Vaasan", "Illuskan", "Thorass"],        # Valbise
    102: ["Chondathan", "Tethyrian", "Infernal", "Elfique", "Thorass"],    # Vallée de la Flamme
    103: ["Chondathan", "Tethyrian", "Illuskan", "Druidic", "Thorass"],    # Les Vaux
    104: ["Chondathan", "Sembian", "Impilturan", "Theskian", "Thorass"],   # Vast
    106: ["Chultan", "Shaaran", "Yuan-ti", "Tashalan", "Dambrathan"],      # Zakharans (approximatif)
    108: ["Chultan", "Yuan-ti", "Draconique", "Abyssal", "Undercommon"],   # Outreterre tropicale
    109: ["Gnomish", "Elfique", "Sylvestre", "Druidic", "Thorass"],         # Forêts du Nord (Gnomes)
    110: ["Elfique", "Sylvestre", "Elven High Speech", "Druidic", "Céleste"], # Éternelle-Rencontre
    111: ["Elfique", "Sylvestre", "Auran", "Elven High Speech", "Céleste"], # Lunargent
    112: ["Aglarondan", "Elfique", "Chondathan", "Sylvestre", "Thorass"],  # Bois de Yuir
    113: ["Shaaran", "Chultan", "Dambrathan", "Yuan-ti", "Géant"],         # Montagnes du Shaar
    114: ["Tuigan", "Shou", "Géant", "Chondathan", "Thorass"],             # Vil Adanrath
    115: ["Draconique", "Infernal", "Chondathan", "Thorass", "Géant"],     # Tymanther
    116: ["Illuskan", "Uluik", "Géant", "Reghed", "Sossrim"],              # Icerim Mountains
    117: ["Chondathan", "Theskian", "Rashemi", "Thayan", "Thorass"],       # Montagnes Theskiennes
    118: ["Nain", "Géant", "Undercommon", "Chondathan", "Thorass"],        # Montagnes de Cuivre

    # === Fallback ===
    0: ["Chondathan", "Illuskan", "Elfique", "Thorass", "Sylvestre"]
}


def get_regional_language(region_id: int) -> str:
    """Retourne une langue régionale principale"""
    langs = region_languages.get(region_id, ["Chondathan"])
    return random.choice(langs)


def generate_languages(
    ethnicity: str,
    region_id: int = 0,
    skill_modifier: int = 0
) -> List[str]:
    """Génère les langues parlées"""

    # Normalisation des anciens noms (après standardisation)
    alias_map = {
        "Demi-elfe": "Half-Elf",
        "Elf Wood": "Wood Elf",
        "Elf Moon": "Moon Elf",
        "Elf Sun": "Sun Elf",
        "Elf Drow": "Drow",
        "Elf Sea": "Sea Elf",
        "Elf Star": "Star Elf",
        "Elf Wild": "Wild Elf",
        "Elf Avariel": "Avariel",
        "Elf Lythari": "Lythari",
        "Half-Elf Wood": "Wood Half-elf",
        "Half-Elf Moon": "Moon Half-elf",
        "Half-Elf Sun": "Sun Half-elf",
        "Half-Elf Drow": "Drow Half-elf",
        "Half-Elf Sea": "Sea Half-elf",
        "Half-Elf Wild": "Wild Half-elf",
    }
    ethnicity = alias_map.get(ethnicity, ethnicity)

    languages = set()

    # 1. Langue ethnique de base
    base_eth = ethnicity_base_languages.get(ethnicity, ["Chondathan"])
    languages.add(random.choice(base_eth))

    # 2. Langue régionale
    regional_lang = get_regional_language(region_id)
    if regional_lang not in languages and random.random() < 0.75:
        languages.add(regional_lang)

    # 3. Langues bonus
    bonus_count = max(1, skill_modifier // 5)   # plus généreux

    eth_bonus = ethnicity_bonus_languages.get(ethnicity, ethnicity_bonus_languages["Default"])
    reg_bonus = region_bonus_languages.get(region_id, region_bonus_languages[0])

    bonus_pool = list(set(eth_bonus + reg_bonus))

    for _ in range(bonus_count):
        if bonus_pool and random.random() < 0.85:
            new_lang = random.choice(bonus_pool)
            if new_lang not in languages:
                languages.add(new_lang)

    return sorted(list(languages))