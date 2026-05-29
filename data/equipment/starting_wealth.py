"""
data/equipment/starting_wealth.py

Système de calcul du capital de départ d'un personnage.

Le capital est calculé en fonction de trois facteurs principaux :
- Le type de settlement (Metropolis >> Isolated Hamlet)
- La région d'origine (richesse économique de la région)
- L'ethnicité (culture et réputation économique)

Objectif : refléter un personnage "aisé mais pas riche".
"""

from typing import Dict

# =============================================================================
# 1. RICHESSE DE BASE PAR TYPE DE SETTLEMENT
# =============================================================================
# Valeurs en pièces d'or (gp). Ces valeurs représentent le capital de départ
# typique pour un personnage "aisé mais pas riche" dans ce type d'implantation.

SETTLEMENT_BASE_WEALTH: Dict[str, int] = {
    # Grandes villes et centres économiques
    "Metropolis": 160,
    "Major Port City": 145,
    "Major Trade City": 150,
    "Fortified City": 120,
    "Large Town": 95,

    # Petites villes et gros villages
    "Small Town": 70,
    "Rural Village": 45,
    "Fishing Village": 40,
    "Forest Village": 42,
    "Mountain Village": 48,
    "Farming Hamlet": 35,
    "Isolated Hamlet": 30,

    # Implantations spéciales
    "Caravan Oasis": 55,
    "Military Outpost": 50,
    "Mining Camp": 55,
    "Logging Camp": 40,
    "Remote Trading Post": 60,
    "Frontier Colony": 55,
    "Smuggler's Port": 65,
    "Inhabited Ruins": 45,
    "Permanent Encampment": 35,
    "Isolated Tower": 55,
    "Lake Village": 42,
    "Remote Monastery": 50,

    # Implantations raciales spécifiques
    "Dwarven Fortress": 110,
    "Elven Enclave": 90,
    "Underdark City": 85,

    # Fallback
    "Default": 60,
}


# =============================================================================
# 2. MODIFICATEURS PAR RÉGION
# =============================================================================
# Certaines régions de Faerûn sont structurellement plus riches que d'autres
# en raison du commerce, des ressources, de la stabilité politique, etc.

# Catégories de richesse régionale
REGIONAL_WEALTH_MODIFIERS: Dict[str, float] = {
    # === RÉGIONS TRÈS RICHES (commerce international, ports majeurs) ===
    "Waterdeep": 1.45,
    "Baldur's Gate": 1.35,
    "Sembia": 1.40,
    "Calimshan": 1.30,
    "Halruaa": 1.25,
    "Lantan": 1.20,

    # === RÉGIONS RICHES ===
    "Amn": 1.15,
    "Tethyr": 1.10,
    "Cormyr": 1.12,
    "Impiltur": 1.08,
    "Thesk": 1.05,
    "Turmish": 1.08,
    "Vilhon Reach": 1.10,

    # === RÉGIONS MOYENNES (la majorité) ===
    "Chondath": 1.00,
    "Chessenta": 1.00,
    "The Dalelands": 0.95,
    "Moonsea": 1.00,
    "Aglarond": 0.95,
    "Damara": 0.90,
    "The Shaar": 0.95,
    "Lake of Steam": 1.00,
    "Border Kingdoms": 0.95,
    "Luiren": 1.00,

    # === RÉGIONS PAUVRES / FRONTIÈRES ===
    "Icewind Dale": 0.70,
    "The North": 0.80,
    "Spine of the World": 0.75,
    "Vaasa": 0.75,
    "The Hordelands": 0.70,
    "Great Glacier": 0.60,
    "Sossal": 0.65,
    "Chult": 0.85,
    "Jungle de Mhair": 0.80,
    "Anauroch": 0.75,

    # === RÉGIONS SPÉCIALES / INSTABLES ===
    "Thay": 1.05,           # Riche mais très inégalitaire
    "Rashemen": 0.85,
    "Unther": 0.90,
    "Mulhorand": 0.95,
    "Old Empires": 0.90,

    # === RÉGIONS EXOTIQUES / LOINTAINES ===
    "Kara-Tur": 1.10,
    "Zakharans": 1.05,
    "Tymanther": 0.95,
    "Evermeet": 1.15,       # Riche mais isolé

    # Fallback
    "Default": 0.95,
}


# =============================================================================
# 3. MODIFICATEURS PAR ETHNIE
# =============================================================================
# Certaines ethnies ont une réputation économique, des traditions marchandes,
# ou au contraire une culture plus frugale/nomade.

ETHNICITY_WEALTH_MODIFIERS: Dict[str, float] = {
    # === ETHNIES MARCHANDES / URBAINES FORTES ===
    "Lantanna": 1.25,
    "Durpari": 1.20,
    "Calishite": 1.15,
    "Sembian": 1.18,
    "Turami": 1.10,
    "Chondathan": 1.05,

    # === ETHNIES "AISEES" MOYENNES ===
    "Tethyrian": 1.00,
    "Illuskan": 0.95,
    "Mulan": 1.08,
    "Damaran": 0.92,
    "Raumviran": 0.95,
    "Impilturan": 1.00,

    # === ETHNIES NOMADES / TRIBALES ===
    "Shaaran": 0.90,
    "Bedine": 0.80,
    "Tuigan": 0.82,
    "Uthgardt": 0.78,
    "Reghedman": 0.75,

    # === ETHNIES "EXOTIQUES" / MARCHANDES SPÉCIALISÉES ===
    "Shou": 1.12,
    "Maztican": 0.95,
    "Tashalan": 0.92,
    "Halruaan": 1.15,

    # === NAINS (généralement aisés grâce au commerce et à l'artisanat) ===
    "Gold Dwarf": 1.12,
    "Shield Dwarf": 1.05,
    "Gray Dwarf": 0.95,
    "Arctic Dwarf": 0.80,
    "Urdunnir": 1.10,
    "Wild Dwarf": 0.85,

    # === GNOMES ===
    "Rock Gnome": 1.00,
    "Forest Gnome": 0.88,

    # === HALFELINS ===
    "Lightfoot Halfling": 0.92,
    "Strongheart Halfling": 0.95,
    "Ghostwise Halfling": 0.80,

    # === ELFES (richesse variable selon le type) ===
    "Sun Elf": 1.10,
    "Moon Elf": 1.00,
    "Wood Elf": 0.88,
    "Wild Elf": 0.78,
    "Sea Elf": 0.90,
    "Star Elf": 1.05,
    "Avariel": 1.08,
    "Lythari": 0.95,

    # === DEMI-ELFES ===
    "Moon Half-elf": 0.98,
    "Sun Half-elf": 1.05,
    "Wood Half-elf": 0.90,
    "Drow Half-elf": 0.95,
    "Sea Half-elf": 0.92,
    "Wild Half-elf": 0.82,

    # === RACES "MARGINALES" OU PAUVRES EN MOYENNE ===
    "Half-Orc": 0.85,
    "Orc": 0.70,
    "Goblin": 0.60,
    "Hobgoblin": 0.75,

    # === RACES "EXOTIQUES" ===
    "Tiefling": 0.95,
    "Aasimar": 1.05,
    "Dragonborn": 1.00,
    "Goliath": 0.82,
    "Firbolg": 0.88,
    "Kenku": 0.85,
    "Lizardfolk": 0.75,
    "Triton": 0.95,
    "Aarakocra": 0.80,
    "Centaur": 0.85,

    # === GENASI (variables selon l'élément et l'intégration) ===
    "Air Genasi": 0.95,
    "Earth Genasi": 1.00,
    "Fire Genasi": 0.92,
    "Water Genasi": 0.95,

    # === DROW (richesse très inégalitaire) ===
    "Drow": 1.05,  # La moyenne est tirée vers le haut par les maisons nobles

    # Fallback
    "Default": 0.95,
}


# =============================================================================
# FONCTION PRINCIPALE
# =============================================================================

def calculate_starting_gold(
    ethnicity: str,
    region_name: str,
    settlement_type: str
) -> int:
    """
    Calcule le capital de départ d'un personnage en pièces d'or.

    Args:
        ethnicity: Nom de l'ethnie (ex: "Shaaran", "Calishite")
        region_name: Nom de la région d'origine (ex: "The Shaar", "Calimshan")
        settlement_type: Type d'implantation (ex: "Large Town", "Metropolis")

    Returns:
        Capital de départ en pièces d'or (arrondi).
    """
    # 1. Richesse de base selon le settlement
    base = SETTLEMENT_BASE_WEALTH.get(settlement_type, SETTLEMENT_BASE_WEALTH["Default"])

    # 2. Modificateur régional
    region_mod = REGIONAL_WEALTH_MODIFIERS.get(region_name, REGIONAL_WEALTH_MODIFIERS["Default"])

    # 3. Modificateur ethnique
    eth_mod = ETHNICITY_WEALTH_MODIFIERS.get(ethnicity, ETHNICITY_WEALTH_MODIFIERS["Default"])

    # Calcul final
    final_wealth = base * region_mod * eth_mod

    # Ajout d'une petite variance aléatoire (±15%)
    import random
    variance = random.uniform(0.85, 1.15)
    final_wealth *= variance

    # On arrondit et on s'assure d'un minimum décent
    final_gold = max(40, int(round(final_wealth)))

    return final_gold


# =============================================================================
# FONCTION UTILITAIRE (pour debug / affichage)
# =============================================================================

def get_wealth_breakdown(ethnicity: str, region_name: str, settlement_type: str) -> dict:
    """Retourne le détail du calcul pour debug."""
    base = SETTLEMENT_BASE_WEALTH.get(settlement_type, SETTLEMENT_BASE_WEALTH["Default"])
    region_mod = REGIONAL_WEALTH_MODIFIERS.get(region_name, REGIONAL_WEALTH_MODIFIERS["Default"])
    eth_mod = ETHNICITY_WEALTH_MODIFIERS.get(ethnicity, ETHNICITY_WEALTH_MODIFIERS["Default"])

    return {
        "base_from_settlement": base,
        "region_modifier": region_mod,
        "ethnicity_modifier": eth_mod,
        "combined_multiplier": round(region_mod * eth_mod, 3),
        "estimated_average": int(base * region_mod * eth_mod),
    }


if __name__ == "__main__":
    # Tests rapides
    print("Test de calcul de capital de départ :\n")

    tests = [
        ("Calishite", "Calimshan", "Metropolis"),
        ("Shaaran", "The Shaar", "Caravan Oasis"),
        ("Shield Dwarf", "Citadel Adbar", "Dwarven Fortress"),
        ("Uthgardt", "Spine of the World", "Nomad Camp"),
        ("Lantanna", "Lantan", "Major Port City"),
    ]

    for eth, region, settlement in tests:
        gold = calculate_starting_gold(eth, region, settlement)
        breakdown = get_wealth_breakdown(eth, region, settlement)
        print(f"{eth} | {region} | {settlement}")
        print(f"  → {gold} gp")
        print(f"  Détail : base={breakdown['base_from_settlement']}, "
              f"région×{breakdown['region_modifier']}, "
              f"ethnie×{breakdown['ethnicity_modifier']}\n")
