"""
data/modifiers.py

Centralisation des dictionnaires de modifiers (craft, knowledge, literacy).

Ce fichier regroupe les 6+1 gros dictionnaires qui étaient auparavant
dans knowledge_data.py. L'objectif est de :
- Alléger le fichier de logique
- Faciliter l'enrichissement des données
- Réduire le nombre de fallbacks silencieux ({} / "Default")

Les données sont utilisées par generate_secondary_skills() via des .get()
avec fallback sur {} ou "Default" quand une ethnie/région/settlement
n'a pas encore d'entrées spécifiques.
"""

from typing import Dict


# =============================================================================
# ETHNICITY CRAFT MODIFIERS
# =============================================================================
# Bonus/malus selon l'ethnie (traditions culturelles et éducation typique)

ethnicity_craft_modifiers: Dict[str, Dict[str, float]] = {
    
    # ==================== HUMAINS ====================
    "Chondathan": {
        "Accounting & Estate Management": 4.0,
        "Navigation (Land & Sea)": 3.5,
        "Cartography": 3.2,
        "Architecture": 2.8,
        "Dyeing & Textile Coloring": 2.5,
    },
    "Tethyrian": {
        "Masonry": 3.5,
        "Carpentry & Woodworking": 3.5,
        "Animal Husbandry & Training": 3.0,
        "Accounting & Estate Management": 2.8,
        "Architecture": 2.5,
    },
    "Calishite": {
        "Jewelry & Goldsmithing": 4.8,
        "Alchemy (Theory & Practice)": 4.2,
        "Calligraphy & Illumination": 3.8,
        "Perfumery & Cosmetics": 3.5,
        "Navigation (Land & Sea)": 3.2,
    },
    "Illuskan": {
        "Shipbuilding": 4.5,
        "Navigation (Land & Sea)": 4.0,
        "Carpentry & Woodworking": 3.5,
        "Weapon Forging (Axes & Swords)": 3.2,
        "Animal Husbandry & Training": 2.8,
    },
    "Mulan": {
        "Masonry": 4.2,
        "Calligraphy & Illumination": 4.0,
        "Architecture": 3.8,
        "Jewelry & Goldsmithing": 3.5,
        "Alchemy (Theory & Practice)": 3.0,
    },
    "Damaran": {
        "Animal Husbandry & Training": 4.0,
        "Leatherworking & Tanning": 3.5,
        "Carpentry & Woodworking": 3.2,
        "Weapon Forging (Axes & Swords)": 3.0,
        "Masonry": 2.8,
    },
    "Turami": {
        "Navigation (Land & Sea)": 4.0,
        "Shipbuilding": 3.8,
        "Fishing & Aquaculture": 3.5,
        "Jewelry & Goldsmithing": 3.2,
        "Dyeing & Textile Coloring": 3.0,
    },
    "Chultan": {
        "Herbalism & Potion Brewing": 4.5,
        "Leatherworking & Tanning": 3.8,
        "Wood Carving": 3.5,
        "Poison Lore & Application": 3.2,
        "Animal Husbandry & Training": 3.0,
    },
    "Rashemi": {
        "Animal Husbandry & Training": 4.5,
        "Leatherworking & Tanning": 4.0,
        "Weapon Forging (Axes & Swords)": 3.8,
        "Carpentry & Woodworking": 3.5,
        "Masonry": 3.0,
    },
    "Shaaran": {
        "Navigation (Land & Sea)": 4.2,
        "Animal Husbandry & Training": 4.0,
        "Leatherworking & Tanning": 3.5,
        "Caravan Logistics": 3.2,
        "Weapon Forging (Axes & Swords)": 3.0,
    },
    "Bedine": {
        "Animal Husbandry & Training": 4.5,
        "Leatherworking & Tanning": 4.0,
        "Navigation (Land & Sea)": 3.8,
        "Weapon Forging (Axes & Swords)": 3.5,
        "Herbalism & Potion Brewing": 3.0,
    },
    "Ffolk": {
        "Fishing & Aquaculture": 4.0,
        "Carpentry & Woodworking": 3.8,
        "Animal Husbandry & Training": 3.5,
        "Leatherworking & Tanning": 3.2,
        "Wood Carving": 3.0,
    },
    "Uthgardt": {
        "Animal Husbandry & Training": 4.5,
        "Leatherworking & Tanning": 4.2,
        "Weapon Forging (Axes & Swords)": 4.0,
        "Carpentry & Woodworking": 3.5,
        "Herbalism & Potion Brewing": 3.0,
    },
    "Arkaiun": {
        "Navigation (Land & Sea)": 3.8,
        "Fishing & Aquaculture": 3.5,
        "Leatherworking & Tanning": 3.2,
        "Carpentry & Woodworking": 3.0,
        "Animal Husbandry & Training": 2.8,
    },
    "Durpari": {
        "Accounting & Estate Management": 4.5,
        "Jewelry & Goldsmithing": 4.0,
        "Navigation (Land & Sea)": 3.8,
        "Calligraphy & Illumination": 3.5,
        "Caravan Logistics": 3.2,
    },
    "Halruaan": {
        "Alchemy (Theory & Practice)": 5.0,
        "Calligraphy & Illumination": 4.2,
        "Architecture": 4.0,
        "Jewelry & Goldsmithing": 3.8,
        "Navigation (Land & Sea)": 3.5,
    },
    "Lantan": {
        "Locksmithing & Mechanisms": 4.8,
        "Shipbuilding": 4.5,
        "Navigation (Land & Sea)": 4.2,
        "Carpentry & Woodworking": 3.8,
        "Accounting & Estate Management": 3.5,
    },
    "Luiric (Luiren Halfling)": {
        "Fishing & Aquaculture": 4.0,
        "Animal Husbandry & Training": 3.8,
        "Carpentry & Woodworking": 3.5,
        "Leatherworking & Tanning": 3.2,
        "Cooking (Fine Cuisine)": 3.0,
    },
    "Nar": {
        "Animal Husbandry & Training": 4.2,
        "Leatherworking & Tanning": 3.8,
        "Weapon Forging (Axes & Swords)": 3.5,
        "Carpentry & Woodworking": 3.2,
        "Herbalism & Potion Brewing": 3.0,
    },
    "Imaskari": {
        "Architecture": 4.5,
        "Masonry": 4.2,
        "Calligraphy & Illumination": 4.0,
        "Alchemy (Theory & Practice)": 3.8,
        "Locksmithing & Mechanisms": 3.5,
    },
    "Lantanna": {
        "Navigation (Land & Sea)": 4.5,
        "Shipbuilding": 4.2,
        "Locksmithing & Mechanisms": 4.0,
        "Carpentry & Woodworking": 3.5,
        "Accounting & Estate Management": 3.2,
    },
    "Maztican": {
        "Herbalism & Potion Brewing": 4.5,
        "Leatherworking & Tanning": 4.0,
        "Wood Carving": 3.8,
        "Animal Husbandry & Training": 3.5,
        "Poison Lore & Application": 3.2,
    },
    "Gur": {
        "Animal Husbandry & Training": 4.0,
        "Leatherworking & Tanning": 3.8,
        "Carpentry & Woodworking": 3.5,
        "Navigation (Land & Sea)": 3.2,
        "Weapon Forging (Axes & Swords)": 3.0,
    },
    "Tuigan": {
        "Animal Husbandry & Training": 4.8,
        "Leatherworking & Tanning": 4.5,
        "Weapon Forging (Axes & Swords)": 4.2,
        "Carpentry & Woodworking": 3.5,
        "Navigation (Land & Sea)": 3.2,
    },
    "Ulutiun": {
        "Animal Husbandry & Training": 4.5,
        "Leatherworking & Tanning": 4.2,
        "Fishing & Aquaculture": 4.0,
        "Carpentry & Woodworking": 3.5,
        "Herbalism & Potion Brewing": 3.2,
    },

    # ==================== ELFES & DEMI-ELFES ====================
    "Moon Elf": {
        "Calligraphy & Illumination": 4.5,
        "Wood Carving": 4.2,
        "Jewelry & Goldsmithing": 3.8,
        "Alchemy (Theory & Practice)": 3.5,
        "Navigation (Land & Sea)": 3.2,
    },
    "Sun Elf": {
        "Calligraphy & Illumination": 5.0,
        "Architecture": 4.5,
        "Jewelry & Goldsmithing": 4.2,
        "Alchemy (Theory & Practice)": 4.0,
        "Masonry": 3.5,
    },
    "Wood Elf": {
        "Wood Carving": 4.8,
        "Carpentry & Woodworking": 4.5,
        "Herbalism & Potion Brewing": 4.2,
        "Leatherworking & Tanning": 3.8,
        "Animal Husbandry & Training": 3.5,
    },
    "Drow": {
        "Poison Lore & Application": 5.0,
        "Jewelry & Goldsmithing": 4.5,
        "Alchemy (Theory & Practice)": 4.2,
        "Weapon Forging (Axes & Swords)": 4.0,
        "Calligraphy & Illumination": 3.5,
    },
    "Sea Elf": {
        "Fishing & Aquaculture": 4.5,
        "Navigation (Land & Sea)": 4.2,
        "Leatherworking & Tanning": 3.5,
        "Wood Carving": 3.2,
        "Carpentry & Woodworking": 3.0,
    },
    "Wild Elf": {
        "Herbalism & Potion Brewing": 4.5,
        "Wood Carving": 4.2,
        "Leatherworking & Tanning": 3.8,
        "Animal Husbandry & Training": 3.5,
        "Poison Lore & Application": 3.2,
    },
    "Star Elf": {
        "Calligraphy & Illumination": 4.5,
        "Alchemy (Theory & Practice)": 4.0,
        "Jewelry & Goldsmithing": 3.8,
        "Navigation (Land & Sea)": 3.5,
        "Wood Carving": 3.2,
    },
    "Avariel": {
        "Jewelry & Goldsmithing": 4.2,
        "Calligraphy & Illumination": 4.0,
        "Wood Carving": 3.5,
        "Alchemy (Theory & Practice)": 3.2,
        "Navigation (Land & Sea)": 3.0,
    },
    "Lythari": {
        "Herbalism & Potion Brewing": 4.5,
        "Wood Carving": 4.0,
        "Animal Husbandry & Training": 3.8,
        "Leatherworking & Tanning": 3.5,
        "Poison Lore & Application": 3.0,
    },

    # ==================== DEMI-ELFES (spécifiques) ====================
    "Wood Half-elf": {
        "Wood Carving": 4.0,
        "Carpentry & Woodworking": 3.8,
        "Herbalism & Potion Brewing": 3.5,
        "Leatherworking & Tanning": 3.2,
        "Animal Husbandry & Training": 3.0,
    },
    "Moon Half-elf": {
        "Calligraphy & Illumination": 3.8,
        "Wood Carving": 3.5,
        "Jewelry & Goldsmithing": 3.2,
        "Navigation (Land & Sea)": 3.0,
        "Alchemy (Theory & Practice)": 2.8,
    },
    "Sun Half-elf": {
        "Calligraphy & Illumination": 4.2,
        "Architecture": 3.8,
        "Jewelry & Goldsmithing": 3.5,
        "Alchemy (Theory & Practice)": 3.2,
        "Masonry": 3.0,
    },
    "Drow Half-elf": {
        "Poison Lore & Application": 4.0,
        "Jewelry & Goldsmithing": 3.8,
        "Weapon Forging (Axes & Swords)": 3.5,
        "Alchemy (Theory & Practice)": 3.2,
        "Calligraphy & Illumination": 3.0,
    },
    "Sea Half-elf": {
        "Fishing & Aquaculture": 4.0,
        "Navigation (Land & Sea)": 3.8,
        "Leatherworking & Tanning": 3.5,
        "Carpentry & Woodworking": 3.2,
        "Wood Carving": 3.0,
    },
    "Wild Half-elf": {
        "Herbalism & Potion Brewing": 4.0,
        "Wood Carving": 3.8,
        "Leatherworking & Tanning": 3.5,
        "Animal Husbandry & Training": 3.2,
        "Poison Lore & Application": 3.0,
    },

    # ==================== NAINS ====================
    "Nain": {
        "Masonry": 5.0,
        "Weapon Forging (Axes & Swords)": 4.8,
        "Metalworking (General)": 4.5,
        "Jewelry & Goldsmithing": 4.2,
        "Architecture": 4.0,
    },
    "Shield Dwarf": {
        "Masonry": 4.8,
        "Weapon Forging (Axes & Swords)": 4.5,
        "Metalworking (General)": 4.2,
        "Jewelry & Goldsmithing": 3.8,
        "Architecture": 3.5,
    },
    "Gold Dwarf": {
        "Jewelry & Goldsmithing": 5.0,
        "Metalworking (General)": 4.8,
        "Masonry": 4.5,
        "Weapon Forging (Axes & Swords)": 4.2,
        "Accounting & Estate Management": 3.8,
    },
    "Gray Dwarf (Duergar)": {
        "Metalworking (General)": 4.5,
        "Weapon Forging (Axes & Swords)": 4.2,
        "Masonry": 4.0,
        "Poison Lore & Application": 3.8,
        "Locksmithing & Mechanisms": 3.5,
    },

    # ==================== GNOMES ====================
    "Gnome": {
        "Locksmithing & Mechanisms": 4.8,
        "Jewelry & Goldsmithing": 4.2,
        "Alchemy (Theory & Practice)": 4.0,
        "Carpentry & Woodworking": 3.5,
        "Calligraphy & Illumination": 3.2,
    },
    "Rock Gnome": {
        "Locksmithing & Mechanisms": 5.0,
        "Jewelry & Goldsmithing": 4.5,
        "Alchemy (Theory & Practice)": 4.2,
        "Carpentry & Woodworking": 3.8,
        "Metalworking (General)": 3.5,
    },
    "Forest Gnome": {
        "Wood Carving": 4.5,
        "Herbalism & Potion Brewing": 4.2,
        "Carpentry & Woodworking": 4.0,
        "Animal Husbandry & Training": 3.5,
        "Leatherworking & Tanning": 3.2,
    },

    # ==================== HALFELINS ====================
    "Halfelin": {
        "Cooking (Fine Cuisine)": 4.5,
        "Animal Husbandry & Training": 4.0,
        "Fishing & Aquaculture": 3.8,
        "Leatherworking & Tanning": 3.5,
        "Carpentry & Woodworking": 3.2,
    },
    "Lightfoot Halfling": {
        "Cooking (Fine Cuisine)": 4.2,
        "Animal Husbandry & Training": 3.8,
        "Fishing & Aquaculture": 3.5,
        "Leatherworking & Tanning": 3.2,
        "Carpentry & Woodworking": 3.0,
    },
    "Strongheart Halfling": {
        "Cooking (Fine Cuisine)": 4.5,
        "Animal Husbandry & Training": 4.2,
        "Fishing & Aquaculture": 3.8,
        "Masonry": 3.5,
        "Carpentry & Woodworking": 3.2,
    },

    # ==================== DEMI-ORCS & ORCS ====================
    "Half-Orc": {
        "Weapon Forging (Axes & Swords)": 4.0,
        "Leatherworking & Tanning": 3.8,
        "Animal Husbandry & Training": 3.5,
        "Carpentry & Woodworking": 3.2,
        "Metalworking (General)": 3.0,
    },
    "Orc": {
        "Weapon Forging (Axes & Swords)": 4.5,
        "Leatherworking & Tanning": 4.0,
        "Animal Husbandry & Training": 3.8,
        "Carpentry & Woodworking": 3.5,
        "Metalworking (General)": 3.2,
    },

    # ==================== AUTRES RACES ====================
    "Tiefling": {
        "Alchemy (Theory & Practice)": 4.2,
        "Poison Lore & Application": 4.0,
        "Jewelry & Goldsmithing": 3.8,
        "Calligraphy & Illumination": 3.5,
        "Weapon Forging (Axes & Swords)": 3.2,
    },
    "Aasimar": {
        "Calligraphy & Illumination": 4.0,
        "Jewelry & Goldsmithing": 3.8,
        "Alchemy (Theory & Practice)": 3.5,
        "Architecture": 3.2,
        "Masonry": 3.0,
    },
    "Dragonborn": {
        "Metalworking (General)": 4.2,
        "Weapon Forging (Axes & Swords)": 4.0,
        "Jewelry & Goldsmithing": 3.5,
        "Masonry": 3.2,
        "Alchemy (Theory & Practice)": 3.0,
    },
    "Genasi (Air)": {
        "Navigation (Land & Sea)": 4.0,
        "Shipbuilding": 3.5,
        "Jewelry & Goldsmithing": 3.2,
        "Alchemy (Theory & Practice)": 3.0,
        "Calligraphy & Illumination": 2.8,
    },
    "Genasi (Earth)": {
        "Masonry": 4.5,
        "Architecture": 4.0,
        "Metalworking (General)": 3.8,
        "Jewelry & Goldsmithing": 3.5,
        "Weapon Forging (Axes & Swords)": 3.2,
    },
    "Genasi (Fire)": {
        "Alchemy (Theory & Practice)": 4.5,
        "Metalworking (General)": 4.0,
        "Weapon Forging (Axes & Swords)": 3.8,
        "Jewelry & Goldsmithing": 3.5,
        "Glassblowing & Ceramics": 3.2,
    },
    "Genasi (Water)": {
        "Fishing & Aquaculture": 4.2,
        "Navigation (Land & Sea)": 4.0,
        "Alchemy (Theory & Practice)": 3.8,
        "Jewelry & Goldsmithing": 3.5,
        "Herbalism & Potion Brewing": 3.2,
    },
    "Triton": {
        "Fishing & Aquaculture": 4.5,
        "Navigation (Land & Sea)": 4.2,
        "Jewelry & Goldsmithing": 3.5,
        "Alchemy (Theory & Practice)": 3.2,
        "Weapon Forging (Axes & Swords)": 3.0,
    },
    "Yuan-ti Pureblood": {
        "Poison Lore & Application": 5.0,
        "Alchemy (Theory & Practice)": 4.5,
        "Herbalism & Potion Brewing": 4.2,
        "Calligraphy & Illumination": 3.8,
        "Jewelry & Goldsmithing": 3.5,
    },

    # ==================== FALLBACK ====================
    "Default": {
        "Carpentry & Woodworking": 2.0,
        "Cooking (Fine Cuisine)": 1.5,
    }
}


# =============================================================================
# REGION CRAFT MODIFIERS
# =============================================================================
# Bonus selon la région d'origine (traditions locales, ressources, culture)

region_craft_modifiers: Dict[str, Dict[str, float]] = {
    
    # ==================== NORTHWEST & SWORD COAST ====================
    "Sword Coast": {
        "Navigation (Land & Sea)": 4.2,
        "Shipbuilding": 4.0,
        "Accounting & Estate Management": 3.0,
    },
    "Waterdeep": {
        "Accounting & Estate Management": 4.8,
        "Jewelry & Goldsmithing": 4.2,
        "Calligraphy & Illumination": 3.8,
        "Architecture": 3.5,
        "Navigation (Land & Sea)": 3.2,
    },
    "Neverwinter": {
        "Masonry": 4.0,
        "Carpentry & Woodworking": 3.8,
        "Weapon Forging (Axes & Swords)": 3.5,
        "Navigation (Land & Sea)": 3.2,
    },
    "Baldur's Gate": {
        "Accounting & Estate Management": 4.5,
        "Navigation (Land & Sea)": 4.2,
        "Shipbuilding": 3.8,
        "Carpentry & Woodworking": 3.5,
    },
    "Luskan": {
        "Navigation (Land & Sea)": 4.5,
        "Shipbuilding": 4.2,
        "Weapon Forging (Axes & Swords)": 3.8,
        "Leatherworking & Tanning": 3.5,
    },
    "Silver Marches": {
        "Weapon Forging (Axes & Swords)": 4.5,
        "Metalworking (General)": 4.0,
        "Animal Husbandry & Training": 3.8,
        "Masonry": 3.5,
    },
    "Moonshae Isles": {
        "Fishing & Aquaculture": 4.2,
        "Shipbuilding": 4.0,
        "Carpentry & Woodworking": 3.8,
        "Animal Husbandry & Training": 3.5,
    },

    # ==================== NORTH & COLD LANDS ====================
    "Icewind Dale": {
        "Animal Husbandry & Training": 4.5,
        "Leatherworking & Tanning": 4.2,
        "Fishing & Aquaculture": 4.0,
        "Weapon Forging (Axes & Swords)": 3.8,
    },
    "The North": {
        "Animal Husbandry & Training": 4.0,
        "Leatherworking & Tanning": 3.8,
        "Weapon Forging (Axes & Swords)": 3.5,
        "Carpentry & Woodworking": 3.2,
    },

    # ==================== WESTERN HEARTLANDS ====================
    "Western Heartlands": {
        "Animal Husbandry & Training": 3.8,
        "Carpentry & Woodworking": 3.5,
        "Masonry": 3.2,
        "Accounting & Estate Management": 3.0,
    },
    "El-Turel": {
        "Masonry": 4.2,
        "Architecture": 3.8,
        "Jewelry & Goldsmithing": 3.5,
        "Calligraphy & Illumination": 3.2,
    },

    # ==================== CENTRAL & EASTERN ====================
    "Cormyr": {
        "Accounting & Estate Management": 4.5,
        "Masonry": 4.0,
        "Architecture": 3.8,
        "Weapon Forging (Axes & Swords)": 3.5,
    },
    "Sembia": {
        "Accounting & Estate Management": 4.8,
        "Navigation (Land & Sea)": 4.0,
        "Jewelry & Goldsmithing": 3.8,
        "Calligraphy & Illumination": 3.5,
    },
    "Dalelands": {
        "Animal Husbandry & Training": 4.0,
        "Carpentry & Woodworking": 3.8,
        "Fishing & Aquaculture": 3.5,
        "Leatherworking & Tanning": 3.2,
    },
    "The Vast": {
        "Mining & Smelting": 4.2,
        "Metalworking (General)": 4.0,
        "Weapon Forging (Axes & Swords)": 3.8,
        "Masonry": 3.5,
    },

    # ==================== SOUTH & CALIMSHAN ====================
    "Calimshan": {
        "Jewelry & Goldsmithing": 4.8,
        "Alchemy (Theory & Practice)": 4.5,
        "Calligraphy & Illumination": 4.2,
        "Perfumery & Cosmetics": 4.0,
        "Navigation (Land & Sea)": 3.8,
    },
    "Tethyr": {
        "Masonry": 4.2,
        "Carpentry & Woodworking": 4.0,
        "Animal Husbandry & Training": 3.8,
        "Accounting & Estate Management": 3.5,
    },

    # ==================== EAST & UNAPPROACHABLE EAST ====================
    "Thay": {
        "Alchemy (Theory & Practice)": 4.8,
        "Calligraphy & Illumination": 4.5,
        "Masonry": 4.0,
        "Architecture": 3.8,
    },
    "Aglarond": {
        "Wood Carving": 4.2,
        "Carpentry & Woodworking": 3.8,
        "Fishing & Aquaculture": 3.5,
        "Herbalism & Potion Brewing": 3.2,
    },
    "Rashemen": {
        "Animal Husbandry & Training": 4.5,
        "Leatherworking & Tanning": 4.2,
        "Herbalism & Potion Brewing": 4.0,
        "Weapon Forging (Axes & Swords)": 3.8,
    },

    # ==================== SOUTH & CHULT ====================
    "Chult": {
        "Herbalism & Potion Brewing": 4.8,
        "Poison Lore & Application": 4.5,
        "Wood Carving": 4.2,
        "Leatherworking & Tanning": 4.0,
    },
    "Mhair Jungles": {
        "Herbalism & Potion Brewing": 4.5,
        "Wood Carving": 4.2,
        "Leatherworking & Tanning": 3.8,
        "Poison Lore & Application": 3.5,
    },

    # ==================== OTHER REGIONS ====================
    "The Shaar": {
        "Animal Husbandry & Training": 4.5,
        "Navigation (Land & Sea)": 4.0,
        "Leatherworking & Tanning": 3.8,
        "Weapon Forging (Axes & Swords)": 3.5,
    },
    "The High Moor": {
        "Weapon Forging (Axes & Swords)": 3.8,
        "Leatherworking & Tanning": 3.5,
        "Animal Husbandry & Training": 3.2,
        "Herbalism & Potion Brewing": 3.0,
    },
    "The Underdark": {
        "Poison Lore & Application": 4.5,
        "Metalworking (General)": 4.2,
        "Weapon Forging (Axes & Swords)": 4.0,
        "Masonry": 3.8,
    },
    "Moonsea": {
        "Navigation (Land & Sea)": 4.0,
        "Shipbuilding": 3.8,
        "Fishing & Aquaculture": 3.5,
        "Accounting & Estate Management": 3.2,
    },
    "The Ride": {
        "Animal Husbandry & Training": 4.5,
        "Leatherworking & Tanning": 4.0,
        "Weapon Forging (Axes & Swords)": 3.8,
    },

    # ==================== FALLBACK ====================
    "Default": {
        "Carpentry & Woodworking": 1.5,
        "Animal Husbandry & Training": 1.5,
    }
}


# =============================================================================
# SETTLEMENT CRAFT MODIFIERS
# =============================================================================

settlement_craft_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== MAJOR URBAN CENTERS ====================
    "Metropolis": {
        "Accounting & Estate Management": 4.5,
        "Jewelry & Goldsmithing": 4.0,
        "Calligraphy & Illumination": 3.8,
        "Alchemy (Theory & Practice)": 3.5,
        "Architecture": 3.5,
    },
    "Large City": {
        "Accounting & Estate Management": 4.2,
        "Jewelry & Goldsmithing": 3.8,
        "Calligraphy & Illumination": 3.5,
        "Locksmithing & Mechanisms": 3.0,
        "Architecture": 3.0,
    },
    "Small City": {
        "Architecture": 3.5,
        "Masonry": 3.2,
        "Carpentry & Woodworking": 3.0,
        "Accounting & Estate Management": 2.8,
        "Jewelry & Goldsmithing": 2.5,
    },

    # ==================== TOWNS & PORTS ====================
    "Large Town": {
        "Carpentry & Woodworking": 3.2,
        "Animal Husbandry & Training": 2.8,
        "Masonry": 2.5,
        "Fishing & Aquaculture": 2.5,
    },
    "Small Town": {
        "Carpentry & Woodworking": 3.0,
        "Animal Husbandry & Training": 2.8,
        "Leatherworking & Tanning": 2.5,
    },
    "Major Port City": {
        "Navigation (Land & Sea)": 4.5,
        "Shipbuilding": 4.2,
        "Fishing & Aquaculture": 3.8,
        "Accounting & Estate Management": 3.5,
    },
    "Major Trade City": {
        "Accounting & Estate Management": 4.5,
        "Navigation (Land & Sea)": 4.0,
        "Jewelry & Goldsmithing": 3.8,
        "Caravan Logistics": 3.5,
    },

    # ==================== FORTRESSES & ENCLAVES ====================
    "Dwarven Fortress": {
        "Masonry": 5.0,
        "Weapon Forging (Axes & Swords)": 4.8,
        "Metalworking (General)": 4.5,
        "Jewelry & Goldsmithing": 4.2,
    },
    "Elven Enclave": {
        "Wood Carving": 4.8,
        "Calligraphy & Illumination": 4.5,
        "Jewelry & Goldsmithing": 4.0,
        "Herbalism & Potion Brewing": 3.8,
    },
    "Underdark City": {
        "Poison Lore & Application": 4.8,
        "Metalworking (General)": 4.5,
        "Weapon Forging (Axes & Swords)": 4.2,
        "Masonry": 4.0,
    },

    # ==================== RURAL & WILD ====================
    "Village": {
        "Animal Husbandry & Training": 3.5,
        "Carpentry & Woodworking": 3.2,
        "Leatherworking & Tanning": 2.8,
        "Fishing & Aquaculture": 2.5,
    },
    "Farming Village": {
        "Animal Husbandry & Training": 4.0,
        "Carpentry & Woodworking": 3.0,
        "Leatherworking & Tanning": 2.5,
    },
    "Fishing Village": {
        "Fishing & Aquaculture": 4.5,
        "Navigation (Land & Sea)": 3.5,
        "Carpentry & Woodworking": 3.0,
        "Leatherworking & Tanning": 2.8,
    },
    "Logging Camp": {
        "Carpentry & Woodworking": 4.5,
        "Wood Carving": 4.0,
        "Leatherworking & Tanning": 3.2,
    },
    "Mining Outpost": {
        "Mining & Smelting": 4.8,
        "Metalworking (General)": 4.0,
        "Weapon Forging (Axes & Swords)": 3.5,
        "Masonry": 3.2,
    },
    "Frontier Outpost": {
        "Animal Husbandry & Training": 3.8,
        "Weapon Forging (Axes & Swords)": 3.5,
        "Leatherworking & Tanning": 3.2,
        "Carpentry & Woodworking": 3.0,
    },

    # ==================== SPECIAL ====================
    "Caravan Oasis": {
        "Animal Husbandry & Training": 4.0,
        "Navigation (Land & Sea)": 3.8,
        "Leatherworking & Tanning": 3.5,
        "Carpentry & Woodworking": 3.0,
    },
    "Inhabited Ruins": {
        "Masonry": 3.5,
        "Architecture": 3.2,
        "Weapon Forging (Axes & Swords)": 3.0,
        "Herbalism & Potion Brewing": 2.8,
    },
    "Permanent Encampment": {
        "Animal Husbandry & Training": 3.8,
        "Leatherworking & Tanning": 3.5,
        "Carpentry & Woodworking": 3.2,
        "Weapon Forging (Axes & Swords)": 3.0,
    },

    # ==================== FALLBACK ====================
    "Default": {
        "Carpentry & Woodworking": 2.0,
        "Animal Husbandry & Training": 1.5,
    }
}


# =============================================================================
# ETHNICITY KNOWLEDGE MODIFIERS
# =============================================================================

ethnicity_knowledge_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== HUMANS ====================
    "Chondathan": {
        "Trade Routes & Commerce": 4.8,
        "Major Cities & Regions": 4.5,
        "Political Currents & Rivalries": 4.2,
        "Laws & Customs of Nations": 3.5,
        "Guilds & Organizations": 3.8,
    },
    "Tethyrian": {
        "History of the Realms": 4.2,
        "Political Currents & Rivalries": 4.0,
        "Major Cities & Regions": 3.8,
        "Nobility & Heraldry": 3.5,
        "Trade Routes & Commerce": 3.2,
    },
    "Calishite": {
        "Trade Routes & Commerce": 4.5,
        "Major Cities & Regions": 4.2,
        "History of Magic": 4.0,
        "Political Currents & Rivalries": 3.8,
        "Secret Organizations": 3.5,
    },
    "Illuskan": {
        "Major Cities & Regions": 4.0,
        "Political Currents & Rivalries": 3.8,
        "Trade Routes & Commerce": 3.5,
        "History of the Realms": 3.2,
        "Navigation Lore": 4.2,
    },
    "Mulan": {
        "History of Magic": 4.8,
        "Major Cities & Regions": 4.5,
        "Political Currents & Rivalries": 4.2,
        "Nobility & Heraldry": 4.0,
        "Laws & Customs of Nations": 3.8,
    },
    "Damaran": {
        "Major Cities & Regions": 4.0,
        "Political Currents & Rivalries": 3.8,
        "Trade Routes & Commerce": 3.5,
        "History of the Realms": 3.2,
        "Guilds & Organizations": 3.0,
    },
    "Turami": {
        "Trade Routes & Commerce": 4.2,
        "Major Cities & Regions": 4.0,
        "Political Currents & Rivalries": 3.5,
        "Navigation Lore": 3.8,
        "Secret Organizations": 3.2,
    },
    "Chultan": {
        "Herbalism & Potion Brewing": 4.5,
        "Local Folklore & Legends": 4.2,
        "Poison Lore & Application": 4.0,
        "History of the Realms": 3.5,
        "Fey & Feywild Knowledge": 3.2,
    },
    "Rashemi": {
        "Major Cities & Regions": 3.8,
        "Political Currents & Rivalries": 3.5,
        "History of the Realms": 3.2,
        "Local Folklore & Legends": 4.5,
        "Herbalism & Potion Brewing": 4.2,
    },
    "Shaaran": {
        "Trade Routes & Commerce": 4.5,
        "Major Cities & Regions": 4.2,
        "Political Currents & Rivalries": 3.8,
        "Navigation Lore": 4.0,
        "Caravan Logistics": 3.5,
    },
    "Bedine": {
        "Navigation Lore": 4.5,
        "Major Cities & Regions": 3.8,
        "Trade Routes & Commerce": 3.5,
        "Local Folklore & Legends": 4.0,
        "Herbalism & Potion Brewing": 3.8,
    },
    "Ffolk": {
        "Local Folklore & Legends": 4.5,
        "Major Cities & Regions": 3.5,
        "History of the Realms": 3.2,
        "Fey & Feywild Knowledge": 4.0,
        "Political Currents & Rivalries": 3.0,
    },
    "Uthgardt": {
        "Local Folklore & Legends": 4.8,
        "Major Cities & Regions": 3.5,
        "Political Currents & Rivalries": 3.2,
        "History of the Realms": 3.0,
        "Herbalism & Potion Brewing": 4.0,
    },
    "Arkaiun": {
        "Major Cities & Regions": 3.8,
        "Trade Routes & Commerce": 3.5,
        "Political Currents & Rivalries": 3.2,
        "Local Folklore & Legends": 4.0,
    },
    "Durpari": {
        "Trade Routes & Commerce": 4.8,
        "Major Cities & Regions": 4.5,
        "Political Currents & Rivalries": 4.0,
        "Guilds & Organizations": 3.8,
        "Accounting & Estate Management": 4.2,
    },
    "Halruaan": {
        "History of Magic": 5.0,
        "Major Cities & Regions": 4.2,
        "Political Currents & Rivalries": 4.0,
        "Secret Organizations": 3.8,
        "Fey & Feywild Knowledge": 3.5,
    },
    "Lantanna": {
        "Trade Routes & Commerce": 4.2,
        "Major Cities & Regions": 4.0,
        "Political Currents & Rivalries": 3.5,
        "Locksmithing & Mechanisms": 4.5,
        "Navigation Lore": 4.0,
    },
    "Luiric (Luiren Halfling)": {
        "Major Cities & Regions": 3.8,
        "Trade Routes & Commerce": 3.5,
        "Local Folklore & Legends": 4.2,
        "Political Currents & Rivalries": 3.2,
        "Fey & Feywild Knowledge": 3.8,
    },
    "Nar": {
        "Major Cities & Regions": 3.8,
        "Political Currents & Rivalries": 3.5,
        "Local Folklore & Legends": 4.2,
        "History of the Realms": 3.2,
        "Herbalism & Potion Brewing": 4.0,
    },
    "Imaskari": {
        "Major Cities & Regions": 4.5,
        "History of Magic": 4.8,
        "Political Currents & Rivalries": 4.2,
        "Architecture": 4.0,
        "Secret Organizations": 3.8,
    },
    "Lantanna": {
        "Trade Routes & Commerce": 4.0,
        "Major Cities & Regions": 3.8,
        "Political Currents & Rivalries": 3.5,
        "Navigation Lore": 4.2,
        "Locksmithing & Mechanisms": 4.5,
    },
    "Maztican": {
        "Local Folklore & Legends": 4.5,
        "Major Cities & Regions": 3.8,
        "Political Currents & Rivalries": 3.5,
        "Herbalism & Potion Brewing": 4.8,
        "Poison Lore & Application": 4.5,
    },
    "Gur": {
        "Major Cities & Regions": 4.0,
        "Trade Routes & Commerce": 3.8,
        "Political Currents & Rivalries": 3.5,
        "Local Folklore & Legends": 4.5,
        "Secret Organizations": 4.0,
    },
    "Tuigan": {
        "Major Cities & Regions": 3.5,
        "Political Currents & Rivalries": 3.8,
        "Trade Routes & Commerce": 4.5,
        "Local Folklore & Legends": 4.0,
        "Navigation Lore": 4.2,
    },
    "Ulutiun": {
        "Major Cities & Regions": 3.2,
        "Local Folklore & Legends": 4.5,
        "Political Currents & Rivalries": 3.0,
        "Herbalism & Potion Brewing": 4.2,
        "Fishing & Aquaculture": 4.0,
    },

    # ==================== ELFES & DEMI-ELFES ====================
    "Moon Elf": {
        "Major Cities & Regions": 4.0,
        "Fey & Feywild Knowledge": 4.8,
        "History of the Realms": 4.5,
        "Political Currents & Rivalries": 3.8,
        "Secret Organizations": 3.5,
    },
    "Sun Elf": {
        "History of Magic": 4.8,
        "Major Cities & Regions": 4.5,
        "Political Currents & Rivalries": 4.2,
        "Fey & Feywild Knowledge": 4.0,
        "Laws & Customs of Nations": 4.0,
    },
    "Wood Elf": {
        "Local Folklore & Legends": 4.8,
        "Fey & Feywild Knowledge": 4.5,
        "Herbalism & Potion Brewing": 4.2,
        "Major Cities & Regions": 3.5,
        "Political Currents & Rivalries": 3.2,
    },
    "Drow": {
        "Major Cities & Regions": 4.2,
        "Secret Organizations": 4.8,
        "Political Currents & Rivalries": 4.5,
        "Poison Lore & Application": 4.5,
        "History of Magic": 4.0,
    },
    "Sea Elf": {
        "Major Cities & Regions": 3.8,
        "Fey & Feywild Knowledge": 4.2,
        "Navigation Lore": 4.5,
        "Local Folklore & Legends": 4.0,
        "Fishing & Aquaculture": 4.2,
    },
    "Wild Elf": {
        "Local Folklore & Legends": 4.8,
        "Fey & Feywild Knowledge": 4.5,
        "Herbalism & Potion Brewing": 4.2,
        "Poison Lore & Application": 3.8,
    },
    "Star Elf": {
        "Major Cities & Regions": 4.2,
        "Fey & Feywild Knowledge": 4.8,
        "History of Magic": 4.0,
        "Political Currents & Rivalries": 3.8,
        "Astronomy & Star Navigation": 4.5,
    },
    "Avariel": {
        "Major Cities & Regions": 3.8,
        "Fey & Feywild Knowledge": 4.5,
        "History of the Realms": 4.0,
        "Political Currents & Rivalries": 3.5,
    },
    "Lythari": {
        "Local Folklore & Legends": 4.8,
        "Fey & Feywild Knowledge": 4.5,
        "Herbalism & Potion Brewing": 4.2,
        "Political Currents & Rivalries": 3.5,
    },

    # ==================== DEMI-ELFES ====================
    "Wood Half-elf": {
        "Local Folklore & Legends": 4.2,
        "Fey & Feywild Knowledge": 4.0,
        "Herbalism & Potion Brewing": 3.8,
        "Major Cities & Regions": 3.5,
    },
    "Moon Half-elf": {
        "Major Cities & Regions": 4.0,
        "Fey & Feywild Knowledge": 4.2,
        "History of the Realms": 3.8,
        "Political Currents & Rivalries": 3.5,
    },
    "Sun Half-elf": {
        "History of Magic": 4.0,
        "Major Cities & Regions": 4.2,
        "Political Currents & Rivalries": 3.8,
        "Fey & Feywild Knowledge": 3.5,
    },
    "Drow Half-elf": {
        "Secret Organizations": 4.2,
        "Political Currents & Rivalries": 4.0,
        "Major Cities & Regions": 3.8,
        "Poison Lore & Application": 4.0,
    },
    "Sea Half-elf": {
        "Navigation Lore": 4.2,
        "Fey & Feywild Knowledge": 3.8,
        "Major Cities & Regions": 3.5,
        "Fishing & Aquaculture": 4.0,
    },
    "Wild Half-elf": {
        "Local Folklore & Legends": 4.5,
        "Fey & Feywild Knowledge": 4.2,
        "Herbalism & Potion Brewing": 4.0,
        "Poison Lore & Application": 3.5,
    },

    # ==================== NAINS ====================
    "Nain": {
        "Major Cities & Regions": 4.0,
        "History of the Realms": 4.2,
        "Political Currents & Rivalries": 3.5,
        "Trade Routes & Commerce": 3.2,
        "Guilds & Organizations": 4.5,
    },
    "Shield Dwarf": {
        "Major Cities & Regions": 3.8,
        "History of the Realms": 4.0,
        "Political Currents & Rivalries": 3.5,
        "Guilds & Organizations": 4.2,
    },
    "Gold Dwarf": {
        "Trade Routes & Commerce": 4.2,
        "Major Cities & Regions": 4.0,
        "Political Currents & Rivalries": 3.8,
        "Accounting & Estate Management": 4.5,
        "Guilds & Organizations": 4.2,
    },
    "Gray Dwarf (Duergar)": {
        "Major Cities & Regions": 4.2,
        "Secret Organizations": 4.5,
        "Political Currents & Rivalries": 4.0,
        "Poison Lore & Application": 3.8,
    },

    # ==================== GNOMES ====================
    "Gnome": {
        "Major Cities & Regions": 4.0,
        "Political Currents & Rivalries": 3.8,
        "History of Magic": 3.5,
        "Trade Routes & Commerce": 3.2,
        "Guilds & Organizations": 4.2,
    },
    "Rock Gnome": {
        "Major Cities & Regions": 4.2,
        "Political Currents & Rivalries": 3.8,
        "Locksmithing & Mechanisms": 4.5,
        "Trade Routes & Commerce": 3.5,
    },
    "Forest Gnome": {
        "Local Folklore & Legends": 4.5,
        "Fey & Feywild Knowledge": 4.2,
        "Herbalism & Potion Brewing": 4.0,
        "Major Cities & Regions": 3.5,
    },

    # ==================== HALFELINS ====================
    "Halfelin": {
        "Major Cities & Regions": 3.8,
        "Trade Routes & Commerce": 3.5,
        "Local Folklore & Legends": 4.2,
        "Political Currents & Rivalries": 3.2,
        "Fey & Feywild Knowledge": 3.8,
    },
    "Lightfoot Halfling": {
        "Major Cities & Regions": 4.0,
        "Trade Routes & Commerce": 3.8,
        "Local Folklore & Legends": 4.2,
        "Political Currents & Rivalries": 3.5,
    },
    "Strongheart Halfling": {
        "Major Cities & Regions": 3.8,
        "Trade Routes & Commerce": 4.0,
        "Local Folklore & Legends": 4.2,
        "Political Currents & Rivalries": 3.5,
        "Guilds & Organizations": 3.8,
    },

    # ==================== DEMI-ORCS & ORCS ====================
    "Half-Orc": {
        "Major Cities & Regions": 3.5,
        "Political Currents & Rivalries": 3.8,
        "Local Folklore & Legends": 4.0,
        "Trade Routes & Commerce": 3.2,
    },
    "Orc": {
        "Major Cities & Regions": 3.2,
        "Political Currents & Rivalries": 3.5,
        "Local Folklore & Legends": 4.2,
        "Poison Lore & Application": 3.8,
    },

    # ==================== AUTRES RACES ====================
    "Tiefling": {
        "Major Cities & Regions": 4.0,
        "Secret Organizations": 4.5,
        "Political Currents & Rivalries": 4.2,
        "History of Magic": 3.8,
        "Poison Lore & Application": 4.0,
    },
    "Aasimar": {
        "Major Cities & Regions": 3.8,
        "Political Currents & Rivalries": 4.0,
        "History of Magic": 3.5,
        "Nobility & Heraldry": 4.2,
        "Laws & Customs of Nations": 3.8,
    },
    "Dragonborn": {
        "Major Cities & Regions": 3.8,
        "Political Currents & Rivalries": 4.0,
        "History of the Realms": 4.2,
        "Trade Routes & Commerce": 3.5,
    },
    "Genasi (Air)": {
        "Major Cities & Regions": 3.5,
        "Navigation Lore": 4.2,
        "Political Currents & Rivalries": 3.8,
        "Fey & Feywild Knowledge": 3.5,
    },
    "Genasi (Earth)": {
        "Major Cities & Regions": 3.8,
        "Political Currents & Rivalries": 3.5,
        "Trade Routes & Commerce": 3.2,
        "Masonry & Architecture": 4.0,
    },
    "Genasi (Fire)": {
        "Major Cities & Regions": 3.5,
        "Political Currents & Rivalries": 4.0,
        "History of Magic": 3.8,
        "Alchemy (Theory & Practice)": 4.2,
    },
    "Genasi (Water)": {
        "Major Cities & Regions": 3.8,
        "Navigation Lore": 4.2,
        "Fishing & Aquaculture": 4.0,
        "Political Currents & Rivalries": 3.5,
    },
    "Triton": {
        "Major Cities & Regions": 3.5,
        "Navigation Lore": 4.5,
        "Fishing & Aquaculture": 4.2,
        "Political Currents & Rivalries": 3.8,
    },
    "Yuan-ti Pureblood": {
        "Major Cities & Regions": 4.0,
        "Secret Organizations": 4.8,
        "Political Currents & Rivalries": 4.5,
        "Poison Lore & Application": 4.8,
        "History of Magic": 4.2,
    },

    # ==================== FALLBACK ====================
    "Default": {
        "Major Cities & Regions": 3.0,
        "Political Currents & Rivalries": 2.5,
    }
}


# =============================================================================
# REGION KNOWLEDGE MODIFIERS
# =============================================================================

region_knowledge_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== NORTHWEST & SWORD COAST ====================
    "Sword Coast": {
        "Trade Routes & Commerce": 4.8,
        "Major Cities & Regions": 4.5,
        "Geography of Faerûn": 4.2,
        "Political Currents & Rivalries": 4.0,
    },
    "Waterdeep": {
        "Major Cities & Regions": 5.0,
        "Political Currents & Rivalries": 4.8,
        "Guilds & Organizations": 4.5,
        "Trade Routes & Commerce": 4.2,
    },
    "Neverwinter": {
        "Major Cities & Regions": 4.2,
        "Political Currents & Rivalries": 3.8,
        "History of the Realms": 3.5,
        "Trade Routes & Commerce": 3.2,
    },
    "Baldur's Gate": {
        "Trade Routes & Commerce": 4.5,
        "Major Cities & Regions": 4.2,
        "Political Currents & Rivalries": 4.0,
        "Guilds & Organizations": 3.8,
    },
    "Luskan": {
        "Major Cities & Regions": 3.8,
        "Political Currents & Rivalries": 4.2,
        "Secret Organizations": 4.0,
        "Trade Routes & Commerce": 3.5,
    },
    "Silver Marches": {
        "Major Cities & Regions": 4.0,
        "Political Currents & Rivalries": 3.5,
        "Trade Routes & Commerce": 3.2,
        "Local Folklore & Legends": 4.2,
    },
    "Moonshae Isles": {
        "Major Cities & Regions": 3.5,
        "Local Folklore & Legends": 4.5,
        "Fey & Feywild Knowledge": 4.2,
        "Political Currents & Rivalries": 3.2,
    },

    # ==================== NORTH & COLD ====================
    "Icewind Dale": {
        "Major Cities & Regions": 3.5,
        "Local Folklore & Legends": 4.8,
        "Political Currents & Rivalries": 3.2,
        "Herbalism & Potion Brewing": 4.0,
    },
    "The North": {
        "Major Cities & Regions": 3.8,
        "Political Currents & Rivalries": 3.5,
        "Local Folklore & Legends": 4.2,
        "Trade Routes & Commerce": 3.2,
    },

    # ==================== HEARTLANDS ====================
    "Cormyr": {
        "Major Cities & Regions": 4.5,
        "Political Currents & Rivalries": 4.8,
        "Nobility & Heraldry": 4.5,
        "Laws & Customs of Nations": 4.2,
    },
    "Sembia": {
        "Trade Routes & Commerce": 4.8,
        "Major Cities & Regions": 4.5,
        "Political Currents & Rivalries": 4.2,
        "Accounting & Estate Management": 4.5,
    },
    "Dalelands": {
        "Major Cities & Regions": 4.0,
        "Political Currents & Rivalries": 3.8,
        "Local Folklore & Legends": 4.2,
        "Trade Routes & Commerce": 3.5,
    },
    "The Vast": {
        "Major Cities & Regions": 3.8,
        "Political Currents & Rivalries": 4.0,
        "Trade Routes & Commerce": 3.5,
        "Mining & Smelting": 4.2,
    },

    # ==================== SOUTH ====================
    "Calimshan": {
        "Major Cities & Regions": 4.5,
        "Political Currents & Rivalries": 4.2,
        "History of Magic": 4.0,
        "Trade Routes & Commerce": 4.8,
    },
    "Tethyr": {
        "Major Cities & Regions": 4.2,
        "Political Currents & Rivalries": 4.0,
        "Nobility & Heraldry": 4.5,
        "Trade Routes & Commerce": 3.8,
    },

    # ==================== EAST ====================
    "Thay": {
        "Major Cities & Regions": 4.5,
        "Political Currents & Rivalries": 4.8,
        "History of Magic": 5.0,
        "Secret Organizations": 4.5,
    },
    "Aglarond": {
        "Major Cities & Regions": 3.8,
        "Political Currents & Rivalries": 3.5,
        "Fey & Feywild Knowledge": 4.5,
        "Local Folklore & Legends": 4.2,
    },
    "Rashemen": {
        "Major Cities & Regions": 3.5,
        "Local Folklore & Legends": 4.8,
        "Political Currents & Rivalries": 3.8,
        "Herbalism & Potion Brewing": 4.5,
    },

    # ==================== OTHER ====================
    "Chult": {
        "Major Cities & Regions": 3.5,
        "Local Folklore & Legends": 4.8,
        "Herbalism & Potion Brewing": 4.5,
        "Poison Lore & Application": 4.2,
    },
    "The Shaar": {
        "Major Cities & Regions": 3.8,
        "Trade Routes & Commerce": 4.5,
        "Political Currents & Rivalries": 3.5,
        "Navigation Lore": 4.0,
    },
    "The Underdark": {
        "Major Cities & Regions": 4.2,
        "Secret Organizations": 4.8,
        "Political Currents & Rivalries": 4.5,
        "Poison Lore & Application": 4.5,
    },
    "Moonsea": {
        "Major Cities & Regions": 4.0,
        "Political Currents & Rivalries": 4.2,
        "Trade Routes & Commerce": 3.8,
        "Navigation Lore": 3.5,
    },

    # ==================== FALLBACK ====================
    "Default": {
        "Major Cities & Regions": 3.0,
        "Political Currents & Rivalries": 2.5,
    }
}


# =============================================================================
# SETTLEMENT KNOWLEDGE MODIFIERS
# =============================================================================

settlement_knowledge_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== MAJOR URBAN CENTERS ====================
    "Metropolis": {
        "Major Cities & Regions": 5.0,
        "Political Currents & Rivalries": 4.8,
        "Guilds & Organizations": 4.5,
        "Court Etiquette & Protocol": 4.5,
        "Nobility & Heraldry": 4.2,
        "Trade Routes & Commerce": 4.0,
    },
    "Large City": {
        "Major Cities & Regions": 4.8,
        "Political Currents & Rivalries": 4.5,
        "Guilds & Organizations": 4.2,
        "Trade Routes & Commerce": 3.8,
    },
    "Small City": {
        "Major Cities & Regions": 4.2,
        "Political Currents & Rivalries": 3.8,
        "Trade Routes & Commerce": 3.5,
        "Guilds & Organizations": 3.2,
    },

    # ==================== TOWNS & PORTS ====================
    "Large Town": {
        "Major Cities & Regions": 3.5,
        "Political Currents & Rivalries": 3.2,
        "Trade Routes & Commerce": 3.0,
        "Local Folklore & Legends": 3.0,
    },
    "Small Town": {
        "Major Cities & Regions": 3.0,
        "Political Currents & Rivalries": 2.8,
        "Local Folklore & Legends": 3.2,
    },
    "Major Port City": {
        "Major Cities & Regions": 4.5,
        "Trade Routes & Commerce": 4.8,
        "Political Currents & Rivalries": 4.0,
        "Navigation Lore": 4.2,
    },
    "Major Trade City": {
        "Trade Routes & Commerce": 5.0,
        "Major Cities & Regions": 4.5,
        "Political Currents & Rivalries": 4.2,
        "Guilds & Organizations": 4.0,
    },

    # ==================== FORTRESSES & ENCLAVES ====================
    "Dwarven Fortress": {
        "Major Cities & Regions": 4.0,
        "Political Currents & Rivalries": 3.5,
        "History of the Realms": 4.2,
        "Guilds & Organizations": 4.5,
    },
    "Elven Enclave": {
        "Major Cities & Regions": 3.8,
        "Fey & Feywild Knowledge": 4.8,
        "Local Folklore & Legends": 4.5,
        "History of the Realms": 4.2,
    },
    "Underdark City": {
        "Major Cities & Regions": 4.2,
        "Secret Organizations": 4.8,
        "Political Currents & Rivalries": 4.5,
        "Poison Lore & Application": 4.5,
    },

    # ==================== RURAL & WILD ====================
    "Village": {
        "Major Cities & Regions": 2.5,
        "Local Folklore & Legends": 3.5,
        "Political Currents & Rivalries": 2.2,
        "Trade Routes & Commerce": 2.0,
    },
    "Farming Village": {
        "Major Cities & Regions": 2.2,
        "Local Folklore & Legends": 3.2,
        "Animal Husbandry & Training": 3.5,
    },
    "Fishing Village": {
        "Major Cities & Regions": 2.8,
        "Local Folklore & Legends": 3.5,
        "Navigation Lore": 3.8,
        "Fishing & Aquaculture": 4.0,
    },
    "Logging Camp": {
        "Major Cities & Regions": 2.5,
        "Local Folklore & Legends": 3.0,
        "Political Currents & Rivalries": 2.2,
    },
    "Mining Outpost": {
        "Major Cities & Regions": 3.0,
        "Political Currents & Rivalries": 2.8,
        "Trade Routes & Commerce": 3.2,
        "Mining & Smelting": 4.5,
    },
    "Frontier Outpost": {
        "Major Cities & Regions": 3.2,
        "Political Currents & Rivalries": 3.0,
        "Local Folklore & Legends": 3.8,
        "Trade Routes & Commerce": 2.5,
    },

    # ==================== SPECIAL ====================
    "Caravan Oasis": {
        "Major Cities & Regions": 3.5,
        "Trade Routes & Commerce": 4.2,
        "Political Currents & Rivalries": 3.0,
        "Navigation Lore": 3.8,
    },
    "Inhabited Ruins": {
        "Major Cities & Regions": 3.8,
        "History of the Realms": 4.5,
        "Political Currents & Rivalries": 3.5,
        "Local Folklore & Legends": 4.2,
    },
    "Permanent Encampment": {
        "Major Cities & Regions": 2.8,
        "Local Folklore & Legends": 4.0,
        "Political Currents & Rivalries": 2.5,
        "Herbalism & Potion Brewing": 3.5,
    },

    # ==================== FALLBACK ====================
    "Default": {}
}


# =============================================================================
# ETHNICITY LITERACY MODIFIERS (probabilités de langues écrites)
# =============================================================================

ethnicity_literacy_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== HUMAINS (enrichi pour réduire les fallbacks) ====================
    "Chondathan":      {"Thorass": 18.0, "Chondathan": 32.0, "Cormyrian": 8.0, "Sembian": 7.0},
    "Tethyrian":       {"Thorass": 28.0, "Chondathan": 15.0, "Illuskan": 10.0, "Druidic": 6.0},
    "Damaran":         {"Thorass": 30.0, "Chondathan": 10.0, "Draconique": 7.0},
    "Calishite":       {"Mulhorandi": 28.0, "Thorass": 16.0, "Maztican": 7.0, "Chultan": 5.0},
    "Illuskan":        {"Thorass": 22.0, "Illuskan": 14.0, "Maztican": 6.0, "Céleste": 5.0},
    "Mulan":           {"Mulhorandi": 30.0, "Thorass": 14.0, "Céleste": 6.0, "Shou": 5.0},
    "Turami":          {"Thorass": 25.0, "Turmish": 22.0, "Chondathan": 18.0, "Mulhorandi": 8.0, "Chessentan": 6.0},
    "Ffolk":           {"Thorass": 12.0, "Illuskan": 20.0, "Chondathan": 15.0, "Druidic": 18.0, "Moonshae": 10.0},
    "Rashemi":         {"Thorass": 15.0, "Rashemi": 28.0, "Chondathan": 12.0, "Aglarondan": 8.0, "Druidic": 6.0},
    "Uthgardt":        {"Thorass": 8.0, "Illuskan": 18.0, "Chondathan": 10.0, "Druidic": 22.0, "Uthgardt": 15.0},
    "Shaaran":         {"Thorass": 18.0, "Shaaran": 25.0, "Chondathan": 14.0, "Turmish": 10.0, "Mulhorandi": 7.0},
    "Nar":             {"Thorass": 14.0, "Damaran": 22.0, "Chondathan": 12.0, "Rashemi": 10.0, "Druidic": 8.0},
    "Arkaiun":         {"Thorass": 16.0, "Chondathan": 20.0, "Damaran": 12.0, "Turmish": 9.0, "Shaaran": 8.0},
    "Bedine":          {"Thorass": 10.0, "Midani": 30.0, "Chondathan": 8.0, "Shaaran": 12.0, "Druidic": 6.0},
    "Chultan":         {"Thorass": 12.0, "Chultan": 28.0, "Mulhorandi": 10.0, "Maztican": 8.0, "Druidic": 7.0},
    "Durpari":         {"Thorass": 20.0, "Durpari": 26.0, "Chondathan": 15.0, "Turmish": 9.0, "Mulhorandi": 6.0},
    "Halruaan":        {"Thorass": 22.0, "Halruaan": 30.0, "Chondathan": 10.0, "Mulhorandi": 8.0, "Céleste": 6.0},
    "Imaskari":        {"Thorass": 15.0, "Imaskari": 28.0, "Chondathan": 12.0, "Mulhorandi": 10.0, "Draconique": 7.0},
    "Gur":             {"Thorass": 18.0, "Guran": 24.0, "Chondathan": 14.0, "Damaran": 10.0, "Druidic": 8.0},
    "Tuigan":          {"Thorass": 12.0, "Tuigan": 32.0, "Chondathan": 10.0, "Shou": 8.0, "Rashemi": 6.0},
    "Ulutiun":         {"Thorass": 8.0, "Uluik": 30.0, "Illuskan": 12.0, "Chondathan": 8.0, "Druidic": 10.0},

    # ==================== ELFES & DEMI-ELFES ====================
    "Moon Elf":        {"Espruar": 42.0, "Elven High Speech": 18.0, "Thorass": 8.0, "Céleste": 6.0},
    "Sun Elf":         {"Espruar": 35.0, "Elven High Speech": 32.0, "Céleste": 8.0, "Thorass": 6.0},
    "Wood Elf":        {"Espruar": 45.0, "Sylvestre": 12.0, "Elven High Speech": 10.0, "Thorass": 6.0},
    "Drow":            {"Glifo (Drow)": 40.0, "Undercommon": 10.0, "Sylvestre": 7.0, "Abyssal": 6.0},
    "Half-Elf":        {"Espruar": 28.0, "Thorass": 22.0, "Elven High Speech": 12.0, "Chondathan": 7.0},

    # ==================== NAINS ====================
    "Nain":            {"Nain": 38.0, "Thorass": 10.0, "Draconique": 7.0, "Géant": 6.0},
    "Shield Dwarf":    {"Nain": 40.0, "Thorass": 12.0, "Abyssal": 6.0},
    "Gold Dwarf":      {"Nain": 42.0, "Thorass": 8.0, "Glifo (Drow)": 5.0},

    # ==================== AUTRES RACES (enrichi) ====================
    "Halfelin":        {"Thorass": 30.0, "Tuigan": 8.0, "Chondathan": 7.0, "Illuskan": 6.0},
    "Lightfoot Halfling": {"Thorass": 22.0, "Chondathan": 18.0, "Illuskan": 10.0, "Druidic": 8.0, "Gnomish": 6.0},
    "Strongheart Halfling": {"Thorass": 18.0, "Chondathan": 15.0, "Damaran": 12.0, "Druidic": 10.0, "Gnomish": 8.0},
    "Gnome":           {"Thorass": 24.0, "Nain": 18.0, "Gnomish": 12.0, "Aquan": 6.0},
    "Half-Orc":        {"Orc": 32.0, "Thorass": 18.0, "Goblin": 7.0},
    "Orc":             {"Orc": 38.0, "Goblin": 10.0, "Thorass": 8.0},
    "Tiefling":        {"Infernal": 36.0, "Thorass": 12.0, "Abyssal": 10.0, "Chondathan": 6.0},
    "Dragonborn":      {"Draconique": 40.0, "Thorass": 10.0, "Druidic": 6.0, "Géant": 5.0},
    "Aasimar":         {"Thorass": 20.0, "Céleste": 28.0, "Chondathan": 12.0, "Elven High Speech": 8.0, "Draconique": 6.0},
    "Reghedman":       {"Thorass": 10.0, "Illuskan": 22.0, "Chondathan": 12.0, "Druidic": 18.0, "Uthgardt": 10.0},
    "Genasi (Air)":    {"Thorass": 14.0, "Auran": 25.0, "Chondathan": 15.0, "Céleste": 8.0, "Draconique": 6.0},
    "Genasi (Earth)":  {"Thorass": 16.0, "Terran": 24.0, "Chondathan": 14.0, "Dwarvish": 10.0, "Draconique": 7.0},
    "Genasi (Fire)":   {"Thorass": 15.0, "Ignan": 26.0, "Chondathan": 13.0, "Draconique": 9.0, "Céleste": 6.0},
    "Genasi (Water)":  {"Thorass": 14.0, "Aquan": 25.0, "Chondathan": 14.0, "Draconique": 8.0, "Elven High Speech": 7.0},
    "Triton":          {"Thorass": 12.0, "Aquan": 30.0, "Chondathan": 10.0, "Draconique": 8.0, "Céleste": 7.0},
    "Yuan-ti Pureblood": {"Thorass": 10.0, "Abyssal": 28.0, "Chultan": 18.0, "Draconique": 12.0, "Druidic": 8.0},

    # ==================== 8 DERNIÈRES ETHNICITÉS SANS LITERACY (remplies pour réduire les fallbacks) ====================
    "Lantanna":        {"Thorass": 18.0, "Lantanese": 30.0, "Chondathan": 14.0, "Calishite": 10.0, "Draconique": 6.0},
    "Maztican":        {"Thorass": 12.0, "Maztican": 28.0, "Nexalan": 18.0, "Chultan": 10.0, "Mulhorandi": 7.0},
    "Netherese":       {"Thorass": 22.0, "Netherese": 32.0, "High Netherese": 15.0, "Draconique": 8.0, "Céleste": 6.0},
    "Raumviran":       {"Thorass": 15.0, "Raumviran": 30.0, "Damaran": 12.0, "Shou": 8.0, "Chondathan": 7.0},
    "Sossrim":         {"Thorass": 10.0, "Sossrim": 28.0, "Illuskan": 15.0, "Uluik": 12.0, "Druidic": 8.0},
    "Shou":            {"Thorass": 12.0, "Shou": 35.0, "Tuigan": 10.0, "Chondathan": 8.0, "Céleste": 6.0},
    "Talfir":          {"Thorass": 18.0, "Talfir": 25.0, "Chondathan": 16.0, "Tethyrian": 12.0, "Druidic": 8.0},
    "Tashalan":        {"Thorass": 16.0, "Tashalan": 26.0, "Chultan": 14.0, "Calishite": 12.0, "Maztican": 8.0},

    # ==================== HALF-ELF VARIANTS + GRAY DWARF (demande utilisateur) ====================
    "Wood Half-elf":   {"Espruar": 35.0, "Sylvestre": 20.0, "Thorass": 12.0, "Chondathan": 10.0, "Druidic": 8.0},
    "Moon Half-elf":   {"Espruar": 30.0, "Elven High Speech": 18.0, "Thorass": 18.0, "Chondathan": 12.0, "Céleste": 6.0},
    "Sun Half-elf":    {"Espruar": 25.0, "Elven High Speech": 22.0, "Thorass": 15.0, "Mulhorandi": 10.0, "Céleste": 8.0},
    "Wild Half-elf":   {"Espruar": 28.0, "Sylvestre": 25.0, "Thorass": 10.0, "Uthgardt": 12.0, "Druidic": 10.0},
    "Drow Half-elf":   {"Glifo (Drow)": 32.0, "Undercommon": 18.0, "Thorass": 14.0, "Chondathan": 10.0, "Abyssal": 8.0},
    "Sea Half-elf":    {"Espruar": 28.0, "Aquan": 22.0, "Thorass": 15.0, "Chondathan": 12.0, "Turmish": 8.0},

    "Gray Dwarf (Duergar)": {"Nain": 35.0, "Undercommon": 22.0, "Thorass": 12.0, "Abyssal": 10.0, "Draconique": 8.0},

    # ==================== SOUS-RACES NAINES ET ELFES OBSCURES (pousser Literacy plus haut) ====================
    "Gray Dwarf":      {"Nain": 36.0, "Undercommon": 24.0, "Thorass": 10.0, "Abyssal": 12.0, "Draconique": 7.0},
    "Wild Dwarf":      {"Nain": 28.0, "Sylvestre": 18.0, "Druidic": 20.0, "Thorass": 8.0, "Chultan": 10.0},
    "Arctic Dwarf":    {"Nain": 32.0, "Uluik": 22.0, "Illuskan": 12.0, "Thorass": 8.0, "Druidic": 10.0},

    "Wild Elf":        {"Espruar": 25.0, "Sylvestre": 32.0, "Druidic": 18.0, "Thorass": 6.0, "Uthgardt": 8.0},
    "Sea Elf":         {"Espruar": 30.0, "Aquan": 28.0, "Sylvestre": 12.0, "Thorass": 10.0, "Chondathan": 8.0},
    "Star Elf":        {"Espruar": 28.0, "Elven High Speech": 25.0, "Céleste": 18.0, "Thorass": 8.0, "Draconique": 7.0},

    # ==================== DERNIÈRES SOUS-RACES OBSCURES (Urdunnir + Avariel/Lythari + gnomes/halflings) ====================
    "Urdunnir":        {"Nain": 38.0, "Undercommon": 15.0, "Thorass": 8.0, "Draconique": 10.0, "Terran": 12.0},

    "Avariel":         {"Espruar": 32.0, "Elven High Speech": 22.0, "Céleste": 18.0, "Auran": 12.0, "Thorass": 6.0},
    "Lythari":         {"Espruar": 28.0, "Sylvestre": 25.0, "Druidic": 18.0, "Thorass": 8.0, "Uthgardt": 6.0},

    "Rock Gnome":      {"Gnomish": 30.0, "Thorass": 18.0, "Nain": 15.0, "Draconique": 10.0, "Chondathan": 8.0},
    "Forest Gnome":    {"Gnomish": 28.0, "Sylvestre": 22.0, "Druidic": 18.0, "Espruar": 12.0, "Thorass": 8.0},

    "Ghostwise Halfling": {"Gnomish": 12.0, "Druidic": 25.0, "Sylvestre": 18.0, "Thorass": 8.0, "Chondathan": 10.0, "Uthgardt": 8.0},

    # ==================== TOUTES DERNIÈRES (Vaasan + Genasi + Goliath + Firbolg + Half-Orc Mountain) ====================
    "Vaasan":          {"Thorass": 18.0, "Damaran": 25.0, "Chondathan": 18.0, "Illuskan": 10.0, "Draconique": 7.0},

    "Air Genasi":      {"Auran": 28.0, "Thorass": 15.0, "Céleste": 18.0, "Chondathan": 12.0, "Draconique": 8.0},
    "Earth Genasi":    {"Terran": 26.0, "Nain": 18.0, "Thorass": 14.0, "Draconique": 12.0, "Chondathan": 10.0},
    "Fire Genasi":     {"Ignan": 28.0, "Thorass": 14.0, "Draconique": 16.0, "Calishite": 10.0, "Céleste": 8.0},
    "Water Genasi":    {"Aquan": 28.0, "Thorass": 14.0, "Chondathan": 12.0, "Turami": 10.0, "Draconique": 8.0},

    "Goliath":         {"Giant": 30.0, "Thorass": 12.0, "Uthgardt": 18.0, "Illuskan": 12.0, "Druidic": 10.0},
    "Firbolg":         {"Giant": 22.0, "Druidic": 25.0, "Sylvestre": 18.0, "Espruar": 12.0, "Thorass": 8.0},

    "Half-Orc Mountain": {"Orc": 25.0, "Thorass": 15.0, "Uthgardt": 18.0, "Illuskan": 12.0, "Giant": 10.0},

    # ==================== DEFAULT ====================
    "Default":         {"Thorass": 25.0, "Chondathan": 8.0, "Espruar": 6.0, "Nain": 5.0}
}
