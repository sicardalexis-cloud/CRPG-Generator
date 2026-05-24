# origin_data.py
# Régions de Faerûn + Origine régionale par ethnie
# Version finale - 24 Mai 2026

import random   # ← AJOUTÉ EN HAUT DU FICHIER

region_names = {
    1: "Calimshan", 2: "Amn", 3: "Tethyr", 4: "Baldur's Gate", 5: "Waterdeep",
    6: "Sembia", 7: "Cormyr", 8: "Chondath", 9: "Vilhon Reach", 10: "Turmish",
    11: "Chessenta", 12: "Mulhorand", 13: "Unther", 14: "Rashemen", 15: "Damara",
    16: "Impiltur", 17: "Thesk", 18: "Moonsea", 19: "Luskan", 20: "Neverwinter",
    21: "Icewind Dale", 22: "Moonshae Isles", 23: "Sossal", 24: "Chult",
    25: "Evermeet", 26: "Cormanthor", 27: "High Forest", 28: "Moonwood",
    29: "Wealdath", 30: "Lantan", 31: "Citadel Adbar", 32: "Mithral Hall",
    33: "Great Rift", 34: "Ironmaster", 35: "Luiren", 36: "Vaasa",
    37: "Spine of the World", 38: "Star Mounts", 39: "Underdark", 40: "Anauroch",
    41: "Le Nord (The North)", 42: "Uthgardt Tribes", 43: "Thay", 44: "Aglarond",
    45: "Silver Marches (Luruar)", 46: "The Dalelands", 47: "The Shaar",
    48: "Lake of Steam", 49: "Border Kingdoms", 50: "Hordelands (The Endless Wastes)",
    51: "Old Empires", 52: "Unapproachable East", 53: "Western Heartlands",
    54: "Sword Coast", 55: "Sword Coast North", 56: "Dragon Coast",
    57: "Great Glacier", 58: "Inner Sea (Sea of Fallen Stars)", 59: "Halruaa",
    60: "Dambrath", 61: "Estagund", 62: "Var the Golden", 63: "Shaarmid",
    64: "Thindol", 65: "Samarach", 66: "Tashalar", 67: "The Shining South",
    68: "Ymber", 69: "Nelanther Isles", 70: "The Whalebones",
    71: "The Trackless Sea", 72: "The Cold Lands", 73: "The Endless Wastes",
    74: "The Great Dale", 75: "The Plateau of Thay", 76: "The Easting Reach",
    77: "The Forgotten Forest", 78: "The Lone Rock", 79: "The Reaching Woods",
    80: "The Thunder Peaks", 81: "The Ride", 82: "Aglarondine",
    0: "Autre / Voyageur"
}

# ==================== ORIGINE RÉGIONALE PAR ETHNIE ====================
origin_by_ethnicity = {
    # ==================== HUMAINS ====================
    "Calishite":      {1: 65, 2: 15, 3: 8, 30: 5, 48: 4, 0: 3},
    "Chondathan":     {8: 25, 9: 20, 46: 15, 53: 12, 6: 8, 54: 5, 0: 15},
    "Damaran":        {15: 30, 16: 20, 18: 15, 36: 10, 45: 8, 72: 5, 0: 12},
    "Illuskan":       {19: 25, 20: 20, 21: 15, 37: 12, 41: 10, 55: 8, 0: 10},
    "Mulan":          {12: 40, 43: 25, 13: 15, 51: 10, 58: 5, 0: 5},
    "Rashemi":        {14: 55, 44: 20, 17: 10, 42: 5, 50: 5, 0: 5},
    "Tethyrian":      {3: 25, 2: 20, 4: 18, 53: 12, 54: 10, 46: 8, 0: 7},
    "Chultan":        {24: 70, 66: 15, 47: 8, 60: 3, 0: 4},
    "Turami":         {10: 45, 11: 20, 8: 15, 56: 10, 0: 10},
    "Ffolk":          {22: 65, 69: 15, 70: 10, 0: 10},
    "Sossrim":        {23: 50, 72: 25, 36: 10, 0: 15},
    "Arkaiun":        {6: 40, 7: 25, 46: 15, 0: 20},
    "Bedine":         {40: 70, 47: 15, 0: 15},
    "Durpari":        {12: 35, 13: 25, 51: 20, 0: 20},
    "Gur":            {47: 45, 60: 20, 61: 15, 0: 20},
    "Halruaan":       {59: 75, 0: 25},
    "Maztican":       {66: 60, 24: 20, 0: 20},
    "Netherese":      {40: 30, 41: 25, 45: 20, 0: 25},
    "Shou":           {50: 40, 52: 30, 0: 30},
    "Tuigan":         {50: 65, 73: 20, 0: 15},
    "Uthgardt":       {41: 60, 37: 25, 55: 10, 0: 5},
    "Vaasan":         {36: 55, 72: 25, 0: 20},

    # ==================== DEMI-ELFES & ELFES ====================
    "Wood Half-elf":  {27: 30, 45: 20, 26: 15, 5: 10, 7: 8, 0: 17},
    "Moon Half-elf":  {5: 28, 4: 22, 6: 15, 45: 12, 25: 8, 0: 15},
    "Drow Half-elf":  {39: 40, 5: 18, 4: 15, 43: 10, 0: 17},
    "Sun Half-elf":   {5: 28, 6: 22, 25: 18, 4: 12, 45: 10, 0: 10},
    "Wild Half-elf":  {27: 35, 45: 20, 26: 15, 37: 10, 0: 20},
    "Sea Half-elf":   {22: 35, 69: 25, 70: 20, 0: 20},

    "Wood Elf":       {27: 45, 26: 25, 28: 15, 45: 8, 0: 7},
    "Moon Elf":       {25: 40, 26: 30, 45: 15, 5: 8, 0: 7},
    "Drow":           {39: 65, 26: 15, 24: 10, 0: 10},
    "Sun Elf":        {25: 55, 26: 25, 45: 10, 0: 10},
    "Wild Elf":       {27: 50, 28: 25, 37: 15, 0: 10},
    "Sea Elf":        {22: 40, 25: 25, 69: 20, 70: 10, 0: 5},
    "Star Elf":       {25: 45, 26: 30, 38: 15, 0: 10},
    "Avariel":        {38: 60, 27: 25, 26: 10, 0: 5},
    "Lythari":        {27: 65, 28: 25, 0: 10},

    # ==================== NAINS, GNOMES, HALFELINS ====================
    "Shield Dwarf":   {31: 35, 32: 25, 34: 15, 45: 12, 0: 13},
    "Gold Dwarf":     {33: 60, 32: 20, 31: 10, 0: 10},
    "Gray Dwarf":     {39: 45, 37: 25, 27: 15, 0: 15},
    "Halfelin":       {35: 40, 46: 25, 45: 15, 6: 10, 0: 10},

    # ==================== AUTRES ====================
    "Half-Orc":       {39: 35, 37: 25, 50: 15, 41: 10, 0: 15},
    "Goliath":        {37: 45, 33: 25, 45: 15, 0: 15},
    "Aarakocra":      {38: 40, 27: 30, 26: 15, 0: 15},
    "Tiefling":       {1: 15, 5: 15, 43: 15, 59: 10, 0: 45},
    "Aasimar":        {5: 20, 7: 15, 14: 10, 25: 10, 59: 10, 0: 35},
}


def get_random_origin(ethnicity: str) -> str:
    """Retourne une région d'origine pondérée.
       La région 0 ('Autre / Voyageur') est systématiquement remplacée."""
    
    origins = origin_by_ethnicity.get(ethnicity)
    if not origins:
        # Fallback sécurisé
        return random.choice(list(region_names.values())[:-1])  # exclut "Autre / Voyageur"

    regions = list(origins.keys())
    weights = list(origins.values())
    
    chosen_idx = random.choices(regions, weights=weights, k=1)[0]

    # === REMPLACEMENT FORT DE LA RÉGION 0 ===
    if chosen_idx == 0:
        # On choisit une région valide parmi celles possibles pour cette ethnie
        valid_regions = [rid for rid in regions if rid != 0]
        
        if valid_regions:
            chosen_idx = random.choice(valid_regions)
        else:
            # Si vraiment aucune autre région, on prend une région aléatoire générale
            all_valid = [rid for rid in region_names.keys() if rid != 0]
            chosen_idx = random.choice(all_valid)

    return region_names.get(chosen_idx, "Région inconnue")