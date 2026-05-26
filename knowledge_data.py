# knowledge_data.py
import random
from typing import Dict
from typing import Dict, List
from language_data import generate_languages
from skill_data import generate_skills   # ← Changé


# ====================== CRAFT WEIGHTS (52 métiers) ======================
# =============================================
# CRAFT SKILLS (Pondérées) - Royaumes Oubliés
# =============================================

craft_weights: Dict[str, int] = {
    # === Compétences courantes / artisanales ===
    "Masonry": 22,
    "Smithing & Metallurgy": 20,
    "Leatherworking & Tanning": 18,
    "Carpentry & Woodworking": 17,
    "Cooking (Fine Cuisine)": 15,
    "Accounting & Estate Management": 14,
    "Weaving & Spinning": 12,
    "Herbalism & Potion Brewing": 11,
    "Dyeing & Textile Coloring": 10,

    # === Compétences intermédiaires ===
    "Architecture": 10,
    "Navigation (Land & Sea)": 10,
    "Cabinetmaking & Marquetry": 9,
    "Locksmithing & Mechanisms": 9,
    "Cartography": 8,
    "Glassworking": 8,
    "Ceramics & Pottery": 7,
    "Weapons & Armor Smithing": 7,
    "Stoneworking": 7,

    # === Compétences spécialisées ===
    "Animal Husbandry & Training": 6,
    "Beekeeping": 6,
    "Shipbuilding": 6,
    "Sail & Rope Making": 6,
    "Viticulture & Winemaking": 6,
    "Brewing & Distilling": 6,
    "Candle & Soap Making": 5,
    "Preservation & Salting": 5,

    # === Compétences rares / haut niveau ===
    "Jewelry & Goldsmithing": 5,
    "Alchemy (Theory & Practice)": 5,
    "Embroidery & Fine Sewing": 4,
    "Calligraphy & Illumination": 4,
    "Bookbinding": 4,
    "Musical Instrument Making": 4,
    "Stone & Wood Carving": 4,
    "Heraldry & Lineage": 4,

    # === Très rares / hautement spécialisées ===
    "Poison Lore & Application": 3,
    "Clockmaking & Complex Mechanisms": 3,
    "Lens Making & Optics": 3,
    "Perfumery & Cosmetics": 3,
    "Taxidermy": 3,
    "Engraving on Metal & Gems": 3,
    "Fireworks Making": 3,
    "Bone & Ivory Carving": 3,
    "Papermaking & Ink Making": 3,
    "Rare Dye Making": 3,

    # === Exceptionnelles ===
    "Magical Goldsmithing (Theoretical)": 2,
    "Exotic Herbalism": 2,
    "Ritual Object Crafting": 2,
    "Mosaic & Fresco Art": 2,
    "High Court Intrigue & Politics": 2,
    "Forgery of Official Documents": 2,
}

# ====================== ETHNICITY CRAFT MODIFIERS ======================
# Bonus/malus selon l'ethnie (représente les traditions culturelles et l'éducation typique)

ethnicity_craft_modifiers: Dict[str, Dict[str, float]] = {
    
    # ==================== HUMAINS ====================
    "Chondathan": {
        "Accounting & Estate Management": 4.0,
        "Navigation (Land & Sea)": 3.5,
        "Cartography": 3.2,
        "Architecture": 2.8,
        "Dyeing & Textile Coloring": 2.5,
        "Merchant Trade Routes & Economics": 2.5,
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
        "Perfumery & Cosmetics": 4.0,
        "Calligraphy & Illumination": 3.5,
        "Rare Dye Making": 3.0,
        "Merchant Trade Routes & Economics": 3.0,
    },
    "Damaran": {
        "Smithing & Metallurgy": 4.7,
        "Masonry": 4.2,
        "Leatherworking & Tanning": 3.8,
        "Weapons & Armor Smithing": 3.5,
        "Stoneworking": 3.0,
    },
    "Illuskan": {
        "Navigation (Land & Sea)": 4.8,
        "Shipbuilding": 4.5,
        "Sail & Rope Making": 4.0,
        "Deep-Sea Fishing": 3.8,
        "Leatherworking & Tanning": 2.8,
    },
    "Mulan": {
        "Accounting & Estate Management": 4.5,
        "Architecture": 4.0,
        "Calligraphy & Illumination": 3.8,
        "Bookbinding": 3.0,
    },
    "Rashemi": {
        "Herbalism & Potion Brewing": 4.8,
        "Animal Husbandry & Training": 3.5,
        "Beekeeping": 3.2,
        "Ritual Object Crafting": 3.0,
    },
    "Turami": {
        "Cooking (Fine Cuisine)": 4.2,
        "Viticulture & Winemaking": 4.0,
        "Brewing & Distilling": 4.0,
        "Preservation & Salting": 3.0,
    },
    "Uthgardt": {
        "Leatherworking & Tanning": 4.0,
        "Weapons & Armor Smithing": 3.8,
        "Animal Husbandry & Training": 3.5,
        "Trapping and Snaring": 3.5,
        "Wild Plant Foraging": 3.0,
    },
    "Chultan": {
        "Herbalism & Potion Brewing": 4.5,
        "Alchemy (Theory & Practice)": 4.0,
        "Exotic Herbalism": 4.0,
        "Trapping and Snaring": 3.2,
    },
    "Shaaran": {
        "Animal Husbandry & Training": 4.5,
        "Trapping and Snaring": 4.0,
        "Wild Plant Foraging": 3.8,
        "Plains Tracking": 3.5,
    },
    "Bedine": {
        "Desert Water Mastery": 4.5,
        "Desert Thermal Endurance": 4.0,
        "Wild Plant Foraging": 3.5,
        "Trapping and Snaring": 3.0,
    },

    # ==================== ELFES & DEMI-ELFES ====================
    "Elf Wood": {
        "Wild Plant Foraging": 4.5,
        "Herbalism & Potion Brewing": 4.0,
        "Carpentry & Woodworking": 3.8,
        "Bowmaking": 3.5,
    },
    "Elf Wild": {
        "Wild Plant Foraging": 4.8,
        "Trapping and Snaring": 4.2,
        "Herbalism & Potion Brewing": 4.0,
        "Forest Stealth": 3.5,  # même si c'est outdoor, on peut l'inclure ici
    },
    "Elf Moon": {
        "Calligraphy & Illumination": 4.0,
        "Herbalism & Potion Brewing": 3.8,
        "Architecture": 3.5,
    },
    "Elf Sun": {
        "Architecture": 4.2,
        "Jewelry & Goldsmithing": 3.8,
        "Calligraphy & Illumination": 3.5,
    },
    "Elf Drow": {
        "Underground Navigation": 4.5,
        "Alchemy (Theory & Practice)": 4.0,
        "Poison Lore & Application": 4.0,
        "Weapons & Armor Smithing": 3.5,
    },
    "Half-Elf": {
        "Wild Plant Foraging": 3.5,
        "Herbalism & Potion Brewing": 3.2,
        "Navigation (Land & Sea)": 3.0,
    },

    # ==================== NAINS ====================
    "Shield Dwarf": {
        "Smithing & Metallurgy": 5.0,
        "Masonry": 4.5,
        "Weapons & Armor Smithing": 4.2,
        "Stoneworking": 4.0,
    },
    "Gold Dwarf": {
        "Smithing & Metallurgy": 4.8,
        "Masonry": 4.5,
        "Jewelry & Goldsmithing": 4.0,
        "Architecture": 3.8,
    },
    "Gray Dwarf": {
        "Underground Navigation": 4.5,
        "Smithing & Metallurgy": 4.2,
        "Weapons & Armor Smithing": 4.0,
    },

    # ==================== AUTRES RACES ====================
    "Half-Orc": {
        "Weapons & Armor Smithing": 4.0,
        "Smithing & Metallurgy": 3.8,
        "Leatherworking & Tanning": 3.5,
    },
    "Goliath": {
        "Mountain Endurance": 4.0,  # même si outdoor, pertinent
        "Stoneworking": 4.0,
        "Masonry": 3.5,
    },
    "Firbolg": {
        "Wild Plant Foraging": 4.5,
        "Herbalism & Potion Brewing": 4.2,
        "Animal Husbandry & Training": 3.8,
    },
    "Lizardfolk": {
        "Marsh Movement": 4.0,
        "Trapping and Snaring": 3.8,
        "Herbalism & Potion Brewing": 3.5,
    },

    # ==================== FALLBACK ====================
    "Default": {
        "Carpentry & Woodworking": 2.0,
        "Wild Plant Foraging": 2.0,
        "Cooking (Fine Cuisine)": 1.5,
    }
}

# ====================== REGION CRAFT MODIFIERS ======================
# Bonus selon la région d'origine (traditions locales, ressources disponibles, culture)

region_craft_modifiers: Dict[str, Dict[str, float]] = {
    
    # ==================== NORTHWEST & SWORD COAST ====================
    "Sword Coast": {
        "Navigation (Land & Sea)": 4.2,
        "Shipbuilding": 4.0,
        "Deep-Sea Fishing": 3.8,
        "Accounting & Estate Management": 3.0,
    },
    "Waterdeep": {
        "Accounting & Estate Management": 4.8,
        "Calligraphy & Illumination": 3.8,
        "Jewelry & Goldsmithing": 3.5,
        "Architecture": 3.2,
        "Merchant Trade Routes & Economics": 3.0,
    },
    "Neverwinter": {
        "Architecture": 4.2,
        "Smithing & Metallurgy": 3.8,
        "Shipbuilding": 3.5,
        "Alchemy (Theory & Practice)": 3.2,
    },
    "Luskan": {
        "Navigation (Land & Sea)": 4.5,
        "Shipbuilding": 4.2,
        "Deep-Sea Fishing": 4.0,
        "Weapons & Armor Smithing": 3.5,
    },
    "Baldur's Gate": {
        "Accounting & Estate Management": 4.2,
        "Navigation (Land & Sea)": 3.8,
        "Alchemy (Theory & Practice)": 3.5,
    },
    "Candlekeep": {
        "Calligraphy & Illumination": 5.0,
        "Bookbinding": 4.8,
        "Astronomy & Star Navigation": 3.5,
    },

    # ==================== NORTH & SAVAGE FRONTIER ====================
    "Silver Marches": {
        "Smithing & Metallurgy": 4.2,
        "Masonry": 3.8,
        "Stoneworking": 3.5,
        "Animal Husbandry & Training": 3.0,
    },
    "Icewind Dale": {
        "Trapping and Snaring": 4.5,
        "Wild Plant Foraging": 4.2,
        "Leatherworking & Tanning": 3.8,
        "Animal Husbandry & Training": 3.5,
    },
    "High Forest": {
        "Herbalism & Potion Brewing": 4.8,
        "Musical Instrument Making": 4.0,
        "Weaving & Spinning": 3.5,
    },
    "Savage Frontier": {
        "Trapping and Snaring": 4.2,
        "Wild Plant Foraging": 4.0,
        "Leatherworking & Tanning": 3.8,
    },
    "Uthgardt Lands": {
        "Trapping and Snaring": 4.5,
        "Leatherworking & Tanning": 4.0,
        "Weapons & Armor Smithing": 3.8,
    },
    "Spine of the World": {
        "Trapping and Snaring": 4.5,
        "Leatherworking & Tanning": 4.0,
        "Smithing & Metallurgy": 3.8,
    },

    # ==================== HEARTLANDS & DALELANDS ====================
    "Dalelands": {
        "Herbalism & Potion Brewing": 4.5,
        "Animal Husbandry & Training": 4.0,
        "Beekeeping": 3.8,
        "Weaving & Spinning": 3.2,
    },
    "Cormyr": {
        "Masonry": 4.0,
        "Architecture": 4.2,
        "Accounting & Estate Management": 3.8,
        "Calligraphy & Illumination": 3.5,
    },
    "Sembia": {
        "Accounting & Estate Management": 5.0,
        "Dyeing & Textile Coloring": 3.8,
        "Jewelry & Goldsmithing": 3.5,
    },
    "Impiltur": {
        "Smithing & Metallurgy": 4.0,
        "Weapons & Armor Smithing": 3.8,
        "Masonry": 3.5,
    },

    # ==================== SOUTH & SHINING SOUTH ====================
    "Calimshan": {
        "Jewelry & Goldsmithing": 5.0,
        "Alchemy (Theory & Practice)": 4.5,
        "Perfumery & Cosmetics": 4.2,
        "Rare Dye Making": 4.0,
        "Calligraphy & Illumination": 3.5,
    },
    "Tethyr": {
        "Viticulture & Winemaking": 4.5,
        "Brewing & Distilling": 4.0,
        "Cooking (Fine Cuisine)": 3.8,
        "Animal Husbandry & Training": 3.5,
    },
    "Amn": {
        "Accounting & Estate Management": 5.0,
        "Jewelry & Goldsmithing": 3.8,
        "Dyeing & Textile Coloring": 3.5,
    },
    "Chult": {
        "Exotic Herbalism": 5.0,
        "Herbalism & Potion Brewing": 4.5,
        "Trapping and Snaring": 4.0,
        "Wild Plant Foraging": 4.2,
    },
    "Shaar": {
        "Animal Husbandry & Training": 4.8,
        "Trapping and Snaring": 4.2,
        "Wild Plant Foraging": 4.0,
    },
    "Halruaa": {
        "Alchemy (Theory & Practice)": 4.8,
        "Ritual Object Crafting": 4.5,
        "Calligraphy & Illumination": 4.0,
    },

    # ==================== EAST & UNAPPROACHABLE EAST ====================
    "Rashemen": {
        "Herbalism & Potion Brewing": 5.0,
        "Ritual Object Crafting": 4.2,
        "Beekeeping": 3.5,
    },
    "Thay": {
        "Alchemy (Theory & Practice)": 5.0,
        "Ritual Object Crafting": 4.5,
        "Calligraphy & Illumination": 4.0,
    },
    "Aglarond": {
        "Herbalism & Potion Brewing": 4.5,
        "Musical Instrument Making": 3.8,
        "Weaving & Spinning": 3.5,
    },
    "Moonsea": {
        "Smithing & Metallurgy": 4.5,
        "Weapons & Armor Smithing": 4.2,
        "Masonry": 3.8,
    },

   
    #    # ==================== EAST & UNAPPROACHABLE EAST ====================
    "Moonsea": {
        "Smithing & Metallurgy": 4.5,
        "Weapons & Armor Smithing": 4.2,
        "Masonry": 3.8,
    },
    "Rashemen": {
        "Herbalism & Potion Brewing": 5.0,
        "Ritual Object Crafting": 4.2,
        "Beekeeping": 3.5,
    },
    "Thay": {
        "Alchemy (Theory & Practice)": 5.0,
        "Ritual Object Crafting": 4.5,
        "Calligraphy & Illumination": 4.0,
    },
    "Aglarond": {
        "Herbalism & Potion Brewing": 4.5,
        "Musical Instrument Making": 3.8,
        "Weaving & Spinning": 3.5,
    },
    "The Vast": {
        "Masonry": 4.0,
        "Carpentry & Woodworking": 3.8,
        "Architecture": 3.5,
    },
    "Mulhorand": {
        "Calligraphy & Illumination": 4.5,
        "Architecture": 4.0,
        "Bookbinding": 3.8,
    },
    "Unther": {
        "Masonry": 4.0,
        "Smithing & Metallurgy": 3.8,
    },
    "Chessenta": {
        "Weapons & Armor Smithing": 4.2,
        "Architecture": 3.8,
    },

    # ==================== INTERIOR & COLD LANDS ====================
    "Anauroch": {
        "Wild Plant Foraging": 4.5,
        "Trapping and Snaring": 4.0,
    },
    "Damara": {
        "Masonry": 4.2,
        "Smithing & Metallurgy": 4.0,
        "Animal Husbandry & Training": 3.8,
    },
    "Vaasa": {
        "Masonry": 4.0,
        "Smithing & Metallurgy": 4.0,
        "Stoneworking": 3.8,
    },
    "Narfell": {
        "Animal Husbandry & Training": 4.5,
        "Trapping and Snaring": 4.0,
        "Leatherworking & Tanning": 3.8,
    },
    "Great Dale": {
        "Herbalism & Potion Brewing": 4.2,
        "Weaving & Spinning": 3.8,
    },

    # ==================== FORESTS, MOORS & WILD AREAS ====================
    "Cormanthor": {
        "Herbalism & Potion Brewing": 4.5,
        "Calligraphy & Illumination": 4.0,
        "Musical Instrument Making": 3.8,
    },
    "Misty Forest": {
        "Herbalism & Potion Brewing": 4.5,
        "Trapping and Snaring": 4.0,
    },
    "Ardeep Forest": {
        "Herbalism & Potion Brewing": 4.2,
        "Musical Instrument Making": 3.5,
    },
    "Luirwood": {
        "Herbalism & Potion Brewing": 4.3,
        "Ritual Object Crafting": 3.5,
    },
    "High Moor": {
        "Wild Plant Foraging": 4.0,
        "Trapping and Snaring": 3.8,
    },
    "Trollclaws": {
        "Trapping and Snaring": 4.2,
        "Leatherworking & Tanning": 3.8,
    },
    "Evermoors": {
        "Animal Husbandry & Training": 4.0,
        "Trapping and Snaring": 3.8,
    },

        # ==================== CITIES & SPECIAL ZONES ====================
    "Silverymoon": {
        "Calligraphy & Illumination": 4.2,
        "Herbalism & Potion Brewing": 4.0,
        "Architecture": 3.8,
    },
    "Zhentil Keep": {
        "Smithing & Metallurgy": 4.0,
        "Weapons & Armor Smithing": 4.2,
        "Alchemy (Theory & Practice)": 3.5,
    },
    "Elturel": {
        "Masonry": 3.8,
        "Architecture": 3.5,
        "Accounting & Estate Management": 3.2,
    },
    "Turmish": {
        "Masonry": 4.0,
        "Architecture": 3.8,
        "Viticulture & Winemaking": 3.5,
    },
    "Lake of Steam": {
        "Deep-Sea Fishing": 4.0,
        "Shipbuilding": 3.5,
        "Cooking (Fine Cuisine)": 3.2,
    },

    # ==================== ISLANDS & REMOTE AREAS ====================
    "Moonshae Isles": {
        "Deep-Sea Fishing": 4.2,
        "Shipbuilding": 4.0,
        "Sail & Rope Making": 3.5,
    },
    "Nelanther Isles": {
        "Navigation (Land & Sea)": 4.5,
        "Deep-Sea Fishing": 4.0,
        "Shipbuilding": 3.8,
    },
    "Evermeet": {
        "Herbalism & Potion Brewing": 4.5,
        "Musical Instrument Making": 4.2,
        "Calligraphy & Illumination": 4.0,
    },
    "Lantan": {
        "Clockmaking & Complex Mechanisms": 4.8,
        "Locksmithing & Mechanisms": 4.2,
        "Lens Making & Optics": 3.8,
    },
    "Mintarn": {
        "Shipbuilding": 4.5,
        "Deep-Sea Fishing": 4.0,
    },
    "Orlumbor": {
        "Shipbuilding": 4.8,
        "Sail & Rope Making": 4.0,
    },

    # ==================== AUTRES RÉGIONS ====================
    "The North": {
        "Trapping and Snaring": 4.2,
        "Leatherworking & Tanning": 3.8,
        "Smithing & Metallurgy": 3.5,
    },
    "The High Moor": {
        "Wild Plant Foraging": 4.0,
        "Trapping and Snaring": 3.8,
    },
    "The Trollclaws": {
        "Trapping and Snaring": 4.2,
        "Leatherworking & Tanning": 3.8,
    },
    "The Evermoors": {
        "Animal Husbandry & Training": 4.0,
        "Trapping and Snaring": 3.8,
    },
    "The Great Dale": {
        "Herbalism & Potion Brewing": 4.2,
        "Weaving & Spinning": 3.8,
    },
    "The Shaar": {
        "Animal Husbandry & Training": 4.8,
        "Trapping and Snaring": 4.2,
        "Wild Plant Foraging": 4.0,
    },
    "The Vilhon Reach": {
        "Navigation (Land & Sea)": 4.0,
        "Shipbuilding": 3.8,
    },
    "The Dragon Coast": {
        "Navigation (Land & Sea)": 4.5,
        "Deep-Sea Fishing": 4.0,
    },
    "The Unapproachable East": {
        "Alchemy (Theory & Practice)": 4.0,
        "Herbalism & Potion Brewing": 3.8,
    },
    "The Cold Lands": {
        "Trapping and Snaring": 4.5,
        "Leatherworking & Tanning": 4.0,
    },
    "The Shining South": {
        "Jewelry & Goldsmithing": 4.0,
        "Alchemy (Theory & Practice)": 3.8,
    },
    "The Heartlands": {
        "Accounting & Estate Management": 4.0,
        "Animal Husbandry & Training": 3.5,
    },
    "The Sword Coast North": {
        "Navigation (Land & Sea)": 4.2,
        "Shipbuilding": 3.8,
    },
    "The Western Heartlands": {
        "Animal Husbandry & Training": 4.0,
        "Accounting & Estate Management": 3.5,
    },
    "The Moonsea North": {
        "Smithing & Metallurgy": 4.2,
        "Weapons & Armor Smithing": 4.0,
    },
    "The Moonsea South": {
        "Masonry": 4.0,
        "Architecture": 3.8,
    },
    "The Dalelands East": {
        "Herbalism & Potion Brewing": 4.5,
        "Animal Husbandry & Training": 4.0,
    },
    "The Dalelands West": {
        "Herbalism & Potion Brewing": 4.3,
        "Beekeeping": 3.8,
    },
    "The Forgotten Forest": {
        "Herbalism & Potion Brewing": 4.5,
        "Musical Instrument Making": 3.8,
    },
    "The Chondalwood": {
        "Herbalism & Potion Brewing": 4.5,
        "Weaving & Spinning": 3.5,
    },
    "The Wealdath": {
        "Herbalism & Potion Brewing": 4.8,
        "Trapping and Snaring": 4.0,
    },
    "The Forest of Amtar": {
        "Herbalism & Potion Brewing": 4.5,
        "Wild Plant Foraging": 4.0,
    },
    "The Thunder Peaks": {
        "Masonry": 4.0,
        "Stoneworking": 3.8,
    },
    "The Desert of Anauroch": {
        "Wild Plant Foraging": 4.5,
        "Trapping and Snaring": 4.0,
    },
    "The Endless Wastes": {
        "Wild Plant Foraging": 4.5,
        "Trapping and Snaring": 4.2,
    },
    "The Plateau of Thay": {
        "Alchemy (Theory & Practice)": 4.8,
        "Ritual Object Crafting": 4.5,
    },
    "The Lake of Dragons": {
        "Navigation (Land & Sea)": 4.0,
        "Deep-Sea Fishing": 3.8,
    },
    "The Alamber Sea": {
        "Navigation (Land & Sea)": 4.5,
        "Deep-Sea Fishing": 4.0,
    },
    "The Inner Sea": {
        "Navigation (Land & Sea)": 4.2,
        "Deep-Sea Fishing": 3.8,
    },
    "The Trackless Sea": {
        "Navigation (Land & Sea)": 4.5,
        "Shipbuilding": 4.0,
        "Deep-Sea Fishing": 4.0,
    },

    # ==================== FALLBACK ====================
    "Default": {}
}


# =============================================
# SETTLEMENT CRAFT MODIFIERS
# =============================================
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
        "Accounting & Estate Management": 3.5,
        "Locksmithing & Mechanisms": 3.2,
        "Jewelry & Goldsmithing": 3.0,
    },

    # ==================== TOWNS & BOROUGHS ====================
    "Large Town": {
        "Masonry": 3.5,
        "Carpentry & Woodworking": 3.5,
        "Architecture": 3.2,
        "Accounting & Estate Management": 3.0,
    },
    "Small Town": {
        "Masonry": 3.2,
        "Carpentry & Woodworking": 3.2,
        "Herbalism & Potion Brewing": 2.8,
        "Cooking (Fine Cuisine)": 2.5,
    },
    "Town": {
        "Masonry": 3.0,
        "Carpentry & Woodworking": 3.0,
        "Accounting & Estate Management": 2.8,
    },

    # ==================== VILLAGES & SMALL SETTLEMENTS ====================
    "Village": {
        "Masonry": 3.5,
        "Carpentry & Woodworking": 3.5,
        "Herbalism & Potion Brewing": 3.0,
        "Animal Husbandry & Training": 2.8,
    },
    "Hamlet": {
        "Carpentry & Woodworking": 3.2,
        "Herbalism & Potion Brewing": 3.2,
        "Animal Husbandry & Training": 3.0,
    },
    "Thorp": {
        "Carpentry & Woodworking": 3.5,
        "Herbalism & Potion Brewing": 3.0,
        "Animal Husbandry & Training": 3.2,
    },

    # ==================== RURAL & SPECIALIZED ====================
    "Rural": {
        "Animal Husbandry & Training": 4.0,
        "Beekeeping": 3.8,
        "Herbalism & Potion Brewing": 3.5,
        "Weaving & Spinning": 3.0,
    },
    "Farming Village": {
        "Animal Husbandry & Training": 4.2,
        "Herbalism & Potion Brewing": 3.5,
        "Cooking (Fine Cuisine)": 3.0,
    },
    "Fishing Village": {
        "Deep-Sea Fishing": 4.5,
        "Shipbuilding": 3.8,
        "Sail & Rope Making": 3.5,
        "Cooking (Fine Cuisine)": 3.0,
    },
    "Mining Town": {
        "Masonry": 4.0,
        "Stoneworking": 4.2,
        "Smithing & Metallurgy": 4.0,
        "Weapons & Armor Smithing": 3.5,
    },

    # ==================== MILITARY & FORTIFIED ====================
    "Fortress": {
        "Weapons & Armor Smithing": 4.5,
        "Smithing & Metallurgy": 4.5,
        "Masonry": 4.0,
        "Locksmithing & Mechanisms": 3.5,
    },
    "Citadel": {
        "Masonry": 4.5,
        "Smithing & Metallurgy": 4.2,
        "Weapons & Armor Smithing": 4.0,
    },
    "Military Outpost": {
        "Weapons & Armor Smithing": 4.2,
        "Smithing & Metallurgy": 4.0,
        "Leatherworking & Tanning": 3.5,
    },

    # ==================== COMMERCIAL & TRADE ====================
    "Port City": {
        "Navigation (Land & Sea)": 4.5,
        "Shipbuilding": 4.2,
        "Deep-Sea Fishing": 3.8,
        "Accounting & Estate Management": 3.5,
    },
    "Trading Post": {
        "Accounting & Estate Management": 4.5,
        "Dyeing & Textile Coloring": 3.5,
        "Jewelry & Goldsmithing": 3.2,
    },
    "Market Town": {
        "Accounting & Estate Management": 4.2,
        "Dyeing & Textile Coloring": 3.8,
        "Cooking (Fine Cuisine)": 3.0,
    },

    # ==================== RELIGIOUS & CULTURAL ====================
    "Monastery": {
        "Calligraphy & Illumination": 4.5,
        "Bookbinding": 4.2,
        "Herbalism & Potion Brewing": 3.8,
        "Ritual Object Crafting": 4.0,
    },
    "Temple Complex": {
        "Calligraphy & Illumination": 4.2,
        "Ritual Object Crafting": 4.5,
        "Bookbinding": 3.8,
    },

    # ==================== WILD & FRONTIER ====================
    "Wilderness": {
        "Herbalism & Potion Brewing": 4.5,
        "Wild Plant Foraging": 4.2,
        "Trapping and Snaring": 4.0,
        "Leatherworking & Tanning": 3.5,
    },
    "Frontier Outpost": {
        "Trapping and Snaring": 4.0,
        "Leatherworking & Tanning": 3.8,
        "Weapons & Armor Smithing": 3.5,
        "Wild Plant Foraging": 3.5,
    },
    "Nomad Camp": {
        "Animal Husbandry & Training": 4.2,
        "Leatherworking & Tanning": 4.0,
        "Wild Plant Foraging": 3.8,
    },

    # ==================== FALLBACK ====================
    "Default": {}
}


# ====================== KNOWLEDGE WEIGHTS (Base weights - 45 knowledges) ======================
knowledge_weights: Dict[str, int] = {
    # === General & Common Knowledge ===
    "History of the Realms": 18,
    "Geography of Faerûn": 20,
    "Major Cities & Regions": 17,
    "Trade Routes & Commerce": 15,
    "Laws & Customs of Nations": 14,
    "Nobility & Heraldry": 13,
    "Local Folklore & Legends": 12,
    "Festivals, Calendars & Traditions": 11,
    "Court Etiquette & Protocol": 10,
    "Guilds & Organizations": 12,
    "Cultural Interactions": 10,

    # === Cultural Knowledge ===
    "Elven Culture": 9,
    "Dwarven Culture": 9,
    "Gnomish Culture": 7,
    "Halfling Culture": 7,
    "Orc & Goblinoid Culture": 6,
    "Genasi & Elemental Peoples": 5,

    # === Ancient & Historical ===
    "Ancient Realms (Netheril, Imaskar...)": 8,
    "History of Netheril": 7,
    "History of Imaskar": 6,
    "Fall of Myth Drannor": 8,
    "Spellplague & Its Aftermath": 8,
    "Lost Kingdoms & Cities": 7,
    "Ruins & Major Archaeological Sites": 9,

    # === Religion & Cosmology ===
    "Major Religions & Deities": 16,
    "Divine Myths & Legends": 13,
    "Religious Cults & Orders": 11,
    "Cosmology (Weave, Shadow Weave)": 9,

    # === Magic & Esoteric ===
    "Weave Theory": 8,
    "History of Magic": 10,
    "Magical Schools & Traditions": 9,
    "Legendary Artifacts & Relics": 7,

    # === Creature & Organization Lore ===
    "Dragon Lore": 8,
    "Aberration Lore": 5,
    "Fey & Feywild Knowledge": 6,
    "Secret Organizations": 7,

    # === Political & Practical ===
    "Political Currents & Rivalries": 12,
    "Astronomy & Star Navigation": 8,
}

# ====================== ETHNICITY KNOWLEDGE MODIFIERS ======================
ethnicity_knowledge_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== HUMANS ====================
    "Chondathan": {
        "Trade Routes & Commerce": 4.8,
        "Major Cities & Regions": 4.5,
        "Political Currents & Rivalries": 4.2,
        "Accounting & Estate Management": 4.0,
        "Laws & Customs of Nations": 3.5,
        "Guilds & Organizations": 3.8,
    },
    "Tethyrian": {
        "History of the Realms": 4.2,
        "Geography of Faerûn": 4.0,
        "Laws & Customs of Nations": 3.8,
        "Local Folklore & Legends": 3.5,
        "Nobility & Heraldry": 3.2,
    },
    "Calishite": {
        "Nobility & Heraldry": 4.8,
        "Court Etiquette & Protocol": 4.5,
        "Trade Routes & Commerce": 4.2,
        "Major Cities & Regions": 4.0,
        "Political Currents & Rivalries": 3.8,
    },
    "Damaran": {
        "History of the Realms": 4.5,
        "Laws & Customs of Nations": 4.2,
        "Nobility & Heraldry": 3.8,
        "Local Folklore & Legends": 3.5,
    },
    "Illuskan": {
        "Geography of Faerûn": 4.5,
        "Trade Routes & Commerce": 4.0,
        "Local Folklore & Legends": 3.8,
        "History of the Realms": 3.5,
    },
    "Mulan": {
        "Laws & Customs of Nations": 4.5,
        "Political Currents & Rivalries": 4.2,
        "Major Cities & Regions": 4.0,
        "Court Etiquette & Protocol": 3.8,
        "History of Magic": 3.5,
    },
    "Rashemi": {
        "Divine Myths & Legends": 4.5,
        "Local Folklore & Legends": 4.2,
        "Major Religions & Deities": 4.0,
        "Cosmology (Weave, Shadow Weave)": 3.8,
    },
    "Turami": {
        "Festivals, Calendars & Traditions": 4.2,
        "Local Folklore & Legends": 4.0,
        "Cooking (Fine Cuisine)": 3.5,
        "Trade Routes & Commerce": 3.2,
    },
    "Uthgardt": {
        "Local Folklore & Legends": 4.5,
        "Orc & Goblinoid Culture": 4.0,
        "Trapping and Snaring": 3.8,
        "Wild Plant Foraging": 3.5,
    },
    "Chultan": {
        "Herbalism & Potion Brewing": 4.5,
        "Major Cities & Regions": 3.8,
        "Ruins & Major Archaeological Sites": 4.0,
        "Local Folklore & Legends": 3.5,
    },
    "Shaaran": {
        "Animal Husbandry & Training": 4.2,
        "Local Folklore & Legends": 3.8,
        "Wild Plant Foraging": 4.0,
    },
    "Ffolk": {
        "Local Folklore & Legends": 4.2,
        "Festivals, Calendars & Traditions": 4.0,
        "Deep-Sea Fishing": 3.5,
    },
    "Sossrim": {
        "Local Folklore & Legends": 4.0,
        "Trapping and Snaring": 4.2,
        "Wild Plant Foraging": 3.8,
    },
    "Vaasan": {
        "Masonry": 3.5,
        "History of the Realms": 3.8,
        "Ruins & Major Archaeological Sites": 3.5,
    },
    "Bedine": {
        "Wild Plant Foraging": 4.5,
        "Local Folklore & Legends": 4.0,
        "Trade Routes & Commerce": 3.5,
    },

    # ==================== HALF-ELVES ====================
    "Half-Elf": {
        "Cultural Interactions": 4.5,
        "Elven Culture": 4.0,
        "History of the Realms": 3.8,
        "Major Cities & Regions": 3.5,
    },
    "Half-Elf Moon": {
        "Elven Culture": 4.5,
        "Divine Myths & Legends": 4.0,
        "Fey & Feywild Knowledge": 4.2,
    },
    "Half-Elf Wood": {
        "Elven Culture": 4.5,
        "Fey & Feywild Knowledge": 4.8,
        "Herbalism & Potion Brewing": 3.8,
    },
    "Half-Elf Sun": {
        "Elven Culture": 4.2,
        "Court Etiquette & Protocol": 4.0,
        "Nobility & Heraldry": 3.8,
    },

    # ==================== ELVES ====================
    "Elf Moon": {
        "Elven Culture": 5.0,
        "Fey & Feywild Knowledge": 4.8,
        "Divine Myths & Legends": 4.5,
        "History of Magic": 4.0,
    },
    "Elf Sun": {
        "Elven Culture": 4.8,
        "Nobility & Heraldry": 4.5,
        "Court Etiquette & Protocol": 4.2,
        "Legendary Artifacts & Relics": 3.8,
    },
    "Elf Wood": {
        "Elven Culture": 5.0,
        "Fey & Feywild Knowledge": 5.0,
        "Herbalism & Potion Brewing": 4.5,
    },
    "Elf Wild": {
        "Fey & Feywild Knowledge": 5.0,
        "Wild Plant Foraging": 4.5,
        "Local Folklore & Legends": 4.2,
    },
    "Elf Drow": {
        "Secret Organizations": 4.8,
        "Cosmology (Weave, Shadow Weave)": 4.5,
        "Legendary Artifacts & Relics": 4.0,
    },
    "Elf Sea": {
        "Trade Routes & Commerce": 4.2,
        "Geography of Faerûn": 4.0,
        "Navigation (Land & Sea)": 3.8,
    },

    # ==================== DWARVES ====================
    "Shield Dwarf": {
        "Dwarven Culture": 5.0,
        "History of the Realms": 4.2,
        "Ruins & Major Archaeological Sites": 4.0,
    },
    "Gold Dwarf": {
        "Dwarven Culture": 5.0,
        "Nobility & Heraldry": 4.2,
        "Legendary Artifacts & Relics": 4.0,
    },
    "Gray Dwarf": {
        "Secret Organizations": 4.5,
        "Ruins & Major Archaeological Sites": 4.2,
    },

    # ==================== OTHER RACES ====================
    "Half-Orc": {
        "Orc & Goblinoid Culture": 5.0,
        "History of the Realms": 3.5,
    },
    "Firbolg": {
        "Fey & Feywild Knowledge": 4.5,
        "Herbalism & Potion Brewing": 4.2,
    },
    "Lizardfolk": {
        "Wild Plant Foraging": 4.0,
        "Herbalism & Potion Brewing": 3.8,
    },

    # ==================== FALLBACK ====================
    "Default": {}
}

# ====================== REGION KNOWLEDGE MODIFIERS ======================
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
        "Court Etiquette & Protocol": 4.5,
        "Guilds & Organizations": 4.5,
        "Nobility & Heraldry": 4.0,
    },
    "Neverwinter": {
        "Architecture": 4.2,
        "History of the Realms": 4.0,
        "Major Cities & Regions": 3.8,
    },
    "Luskan": {
        "Trade Routes & Commerce": 4.5,
        "Geography of Faerûn": 4.0,
        "Major Cities & Regions": 3.8,
    },
    "Baldur's Gate": {
        "Trade Routes & Commerce": 4.5,
        "Major Cities & Regions": 4.2,
        "Political Currents & Rivalries": 4.0,
    },
    "Candlekeep": {
        "History of Magic": 5.0,
        "Legendary Artifacts & Relics": 4.8,
        "Weave Theory": 4.5,
        "History of the Realms": 4.2,
        "Bookbinding": 4.0,
    },

    # ==================== NORTH & SAVAGE FRONTIER ====================
    "Silver Marches": {
        "Ruins & Major Archaeological Sites": 4.2,
        "History of the Realms": 4.0,
        "Dwarven Culture": 3.8,
    },
    "Icewind Dale": {
        "Local Folklore & Legends": 4.5,
        "Trapping and Snaring": 4.0,
        "Wild Plant Foraging": 4.0,
        "Geography of Faerûn": 3.8,
    },
    "High Forest": {
        "Fey & Feywild Knowledge": 5.0,
        "Herbalism & Potion Brewing": 4.5,
        "Local Folklore & Legends": 4.2,
    },
    "Savage Frontier": {
        "Wild Plant Foraging": 4.5,
        "Local Folklore & Legends": 4.2,
        "Geography of Faerûn": 4.0,
    },
    "Uthgardt Lands": {
        "Local Folklore & Legends": 4.8,
        "Orc & Goblinoid Culture": 4.5,
        "Trapping and Snaring": 4.0,
    },
    "Spine of the World": {
        "Ruins & Major Archaeological Sites": 4.5,
        "Geography of Faerûn": 4.2,
        "Wild Plant Foraging": 4.0,
    },

    # ==================== HEARTLANDS & DALELANDS ====================
    "Dalelands": {
        "Local Folklore & Legends": 4.8,
        "Festivals, Calendars & Traditions": 4.5,
        "History of the Realms": 4.2,
        "Herbalism & Potion Brewing": 3.8,
    },
    "Cormyr": {
        "Nobility & Heraldry": 4.8,
        "Court Etiquette & Protocol": 4.5,
        "Laws & Customs of Nations": 4.2,
        "History of the Realms": 4.0,
    },
    "Sembia": {
        "Trade Routes & Commerce": 5.0,
        "Accounting & Estate Management": 4.5,
        "Guilds & Organizations": 4.2,
    },
    "Thesk": {
        "Trade Routes & Commerce": 4.5,
        "Guilds & Organizations": 4.0,
    },
    "Impiltur": {
        "History of the Realms": 4.0,
        "Nobility & Heraldry": 3.8,
    },
    "Western Heartlands": {
        "Animal Husbandry & Training": 4.0,
        "Local Folklore & Legends": 3.8,
        "Trade Routes & Commerce": 3.5,
    },

    # ==================== SOUTH & SHINING SOUTH ====================
    "Calimshan": {
        "Trade Routes & Commerce": 5.0,
        "Nobility & Heraldry": 4.5,
        "Court Etiquette & Protocol": 4.2,
        "Major Cities & Regions": 4.0,
    },
    "Tethyr": {
        "Festivals, Calendars & Traditions": 4.5,
        "Local Folklore & Legends": 4.2,
        "Viticulture & Winemaking": 4.0,
    },
    "Amn": {
        "Trade Routes & Commerce": 5.0,
        "Accounting & Estate Management": 4.8,
        "Guilds & Organizations": 4.5,
    },
    "Chult": {
        "Ruins & Major Archaeological Sites": 4.8,
        "Exotic Herbalism": 4.5,
        "Major Cities & Regions": 4.0,
    },
    "Shaar": {
        "Animal Husbandry & Training": 4.5,
        "Local Folklore & Legends": 4.0,
        "Wild Plant Foraging": 4.0,
    },
    "Halruaa": {
        "History of Magic": 5.0,
        "Weave Theory": 4.8,
        "Legendary Artifacts & Relics": 4.5,
        "Cosmology (Weave, Shadow Weave)": 4.2,
    },
    "Vilhon Reach": {
        "Trade Routes & Commerce": 4.2,
        "Major Cities & Regions": 4.0,
    },
    "Dragon Coast": {
        "Trade Routes & Commerce": 4.5,
        "Major Cities & Regions": 4.0,
        "Geography of Faerûn": 3.8,
    },

    # ==================== EAST & UNAPPROACHABLE EAST ====================
    "Moonsea": {
        "Political Currents & Rivalries": 4.8,
        "History of the Realms": 4.5,
        "Major Cities & Regions": 4.2,
    },
    "Rashemen": {
        "Divine Myths & Legends": 5.0,
        "Local Folklore & Legends": 4.8,
        "Major Religions & Deities": 4.5,
        "Cosmology (Weave, Shadow Weave)": 4.0,
    },
    "Thay": {
        "History of Magic": 5.0,
        "Weave Theory": 4.8,
        "Legendary Artifacts & Relics": 4.5,
        "Secret Organizations": 4.2,
    },
    "Aglarond": {
        "Herbalism & Potion Brewing": 4.5,
        "Fey & Feywild Knowledge": 4.2,
        "Local Folklore & Legends": 4.0,
    },
    "The Vast": {
        "History of the Realms": 4.0,
        "Major Cities & Regions": 3.8,
    },
    "Mulhorand": {
        "History of the Realms": 4.5,
        "Nobility & Heraldry": 4.2,
        "Major Religions & Deities": 4.0,
    },
    "Unther": {
        "History of the Realms": 4.2,
        "Ruins & Major Archaeological Sites": 4.0,
    },
    "Chessenta": {
        "History of the Realms": 4.0,
        "Nobility & Heraldry": 3.8,
    },

    # ==================== INTERIOR & COLD LANDS ====================
    "Anauroch": {
        "Wild Plant Foraging": 4.5,
        "Ruins & Major Archaeological Sites": 4.2,
        "Geography of Faerûn": 4.0,
    },
    "Damara": {
        "History of the Realms": 4.2,
        "Nobility & Heraldry": 3.8,
    },
    "Vaasa": {
        "Ruins & Major Archaeological Sites": 4.0,
        "History of the Realms": 3.8,
    },
    "Narfell": {
        "Animal Husbandry & Training": 4.2,
        "Local Folklore & Legends": 4.0,
    },
    "Great Dale": {
        "Herbalism & Potion Brewing": 4.5,
        "Local Folklore & Legends": 4.2,
    },

    # ==================== FORESTS, MOORS & WILD AREAS ====================
    "Cormanthor": {
        "Fey & Feywild Knowledge": 5.0,
        "Elven Culture": 4.8,
        "Herbalism & Potion Brewing": 4.5,
    },
    "Misty Forest": {
        "Fey & Feywild Knowledge": 4.8,
        "Herbalism & Potion Brewing": 4.5,
    },
    "Ardeep Forest": {
        "Fey & Feywild Knowledge": 4.5,
        "Local Folklore & Legends": 4.0,
    },
    "Luirwood": {
        "Herbalism & Potion Brewing": 4.5,
        "Divine Myths & Legends": 4.0,
    },
    "High Moor": {
        "Wild Plant Foraging": 4.5,
        "Ruins & Major Archaeological Sites": 4.2,
    },
    "Trollclaws": {
        "Wild Plant Foraging": 4.2,
        "Trapping and Snaring": 4.0,
    },
    "Evermoors": {
        "Animal Husbandry & Training": 4.0,
        "Local Folklore & Legends": 3.8,
    },

    # ==================== CITIES & SPECIAL ZONES ====================
    "Silverymoon": {
        "History of Magic": 4.2,
        "Major Cities & Regions": 4.0,
        "Court Etiquette & Protocol": 3.8,
    },
    "Zhentil Keep": {
        "Political Currents & Rivalries": 4.8,
        "Secret Organizations": 4.5,
    },
    "Elturel": {
        "Laws & Customs of Nations": 4.0,
        "Major Religions & Deities": 3.8,
    },
    "Turmish": {
        "Trade Routes & Commerce": 4.0,
        "Major Cities & Regions": 3.8,
    },
    "Lake of Steam": {
        "Trade Routes & Commerce": 4.2,
        "Geography of Faerûn": 4.0,
    },

    # ==================== ISLANDS & REMOTE AREAS ====================
    "Moonshae Isles": {
        "Local Folklore & Legends": 4.5,
        "Festivals, Calendars & Traditions": 4.2,
        "Deep-Sea Fishing": 4.0,
    },
    "Nelanther Isles": {
        "Trade Routes & Commerce": 4.5,
        "Geography of Faerûn": 4.2,
    },
    "Evermeet": {
        "Elven Culture": 5.0,
        "Fey & Feywild Knowledge": 5.0,
        "History of the Realms": 4.2,
    },
    "Lantan": {
        "History of Magic": 4.5,
        "Legendary Artifacts & Relics": 4.2,
        "Weave Theory": 4.0,
    },

    # ==================== FALLBACK ====================
    "Default": {}
}

# ====================== SETTLEMENT KNOWLEDGE MODIFIERS ======================
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
        "Court Etiquette & Protocol": 4.0,
        "Nobility & Heraldry": 3.8,
    },
    "Small City": {
        "Major Cities & Regions": 4.5,
        "Laws & Customs of Nations": 4.0,
        "Guilds & Organizations": 3.8,
        "Political Currents & Rivalries": 3.5,
    },

    # ==================== TOWNS & BOROUGHS ====================
    "Large Town": {
        "Major Cities & Regions": 4.0,
        "Local Folklore & Legends": 3.8,
        "Festivals, Calendars & Traditions": 3.5,
        "Laws & Customs of Nations": 3.2,
    },
    "Small Town": {
        "Local Folklore & Legends": 4.2,
        "Festivals, Calendars & Traditions": 4.0,
        "Guilds & Organizations": 3.5,
    },
    "Town": {
        "Local Folklore & Legends": 4.0,
        "Festivals, Calendars & Traditions": 3.8,
        "Laws & Customs of Nations": 3.5,
    },

    # ==================== VILLAGES & SMALL SETTLEMENTS ====================
    "Village": {
        "Local Folklore & Legends": 4.5,
        "Festivals, Calendars & Traditions": 4.2,
        "Herbalism & Potion Brewing": 3.5,
    },
    "Hamlet": {
        "Local Folklore & Legends": 4.8,
        "Festivals, Calendars & Traditions": 4.5,
        "Herbalism & Potion Brewing": 3.8,
    },
    "Thorp": {
        "Local Folklore & Legends": 4.5,
        "Festivals, Calendars & Traditions": 4.0,
    },

    # ==================== RURAL & SPECIALIZED AREAS ====================
    "Rural": {
        "Local Folklore & Legends": 4.2,
        "Festivals, Calendars & Traditions": 4.0,
        "Animal Husbandry & Training": 3.5,
    },
    "Farming Village": {
        "Local Folklore & Legends": 4.0,
        "Festivals, Calendars & Traditions": 3.8,
        "Herbalism & Potion Brewing": 3.5,
    },
    "Fishing Village": {
        "Local Folklore & Legends": 4.0,
        "Geography of Faerûn": 3.8,
        "Trade Routes & Commerce": 3.5,
    },
    "Mining Town": {
        "Ruins & Major Archaeological Sites": 4.5,
        "History of the Realms": 4.0,
        "Stoneworking": 3.5,
    },

    # ==================== MILITARY & FORTIFIED ====================
    "Fortress": {
        "Laws & Customs of Nations": 4.2,
        "Political Currents & Rivalries": 4.0,
        "History of the Realms": 3.8,
        "Nobility & Heraldry": 3.5,
    },
    "Citadel": {
        "Nobility & Heraldry": 4.5,
        "History of the Realms": 4.2,
        "Laws & Customs of Nations": 4.0,
    },
    "Military Outpost": {
        "Laws & Customs of Nations": 4.0,
        "Political Currents & Rivalries": 3.8,
        "History of the Realms": 3.5,
    },

    # ==================== COMMERCIAL & TRADE ====================
    "Port City": {
        "Trade Routes & Commerce": 4.8,
        "Major Cities & Regions": 4.5,
        "Geography of Faerûn": 4.2,
    },
    "Trading Post": {
        "Trade Routes & Commerce": 5.0,
        "Guilds & Organizations": 4.5,
        "Major Cities & Regions": 4.0,
    },
    "Market Town": {
        "Trade Routes & Commerce": 4.5,
        "Guilds & Organizations": 4.2,
        "Major Cities & Regions": 4.0,
    },

    # ==================== RELIGIOUS & CULTURAL ====================
    "Monastery": {
        "Major Religions & Deities": 5.0,
        "Divine Myths & Legends": 4.8,
        "Cosmology (Weave, Shadow Weave)": 4.5,
        "History of Magic": 4.0,
        "Bookbinding": 3.8,
    },
    "Temple Complex": {
        "Major Religions & Deities": 5.0,
        "Divine Myths & Legends": 4.8,
        "Religious Cults & Orders": 4.5,
        "Cosmology (Weave, Shadow Weave)": 4.2,
    },

    # ==================== WILD & FRONTIER AREAS ====================
    "Wilderness": {
        "Ruins & Major Archaeological Sites": 4.8,
        "Fey & Feywild Knowledge": 4.5,
        "Wild Plant Foraging": 4.2,
        "Local Folklore & Legends": 4.0,
    },
    "Frontier Outpost": {
        "Ruins & Major Archaeological Sites": 4.5,
        "Local Folklore & Legends": 4.0,
        "Political Currents & Rivalries": 3.8,
    },
    "Nomad Camp": {
        "Local Folklore & Legends": 4.5,
        "Animal Husbandry & Training": 4.0,
        "Wild Plant Foraging": 3.8,
    },

    # ==================== FALLBACK ====================
    "Default": {}
}

ethnicity_literacy_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== HUMAINS ====================
    "Chondathan":      {"Thorass": 18.0, "Chondathan": 32.0, "Cormyrian": 8.0, "Sembian": 7.0},
    "Tethyrian":       {"Thorass": 28.0, "Chondathan": 15.0, "Illuskan": 10.0, "Druidic": 6.0},
    "Damaran":         {"Thorass": 30.0, "Chondathan": 10.0, "Draconique": 7.0},
    "Calishite":       {"Mulhorandi": 28.0, "Thorass": 16.0, "Maztican": 7.0, "Chultan": 5.0},
    "Illuskan":        {"Thorass": 22.0, "Illuskan": 14.0, "Maztican": 6.0, "Céleste": 5.0},
    "Mulan":           {"Mulhorandi": 30.0, "Thorass": 14.0, "Céleste": 6.0, "Shou": 5.0},

    # ==================== ELFES & DEMI-ELFES ====================
    "Elf Moon":        {"Espruar": 42.0, "Elven High Speech": 18.0, "Thorass": 8.0, "Céleste": 6.0},
    "Elf Sun":         {"Espruar": 35.0, "Elven High Speech": 32.0, "Céleste": 8.0, "Thorass": 6.0},
    "Elf Wood":        {"Espruar": 45.0, "Sylvestre": 12.0, "Elven High Speech": 10.0, "Thorass": 6.0},
    "Elf Drow":        {"Glifo (Drow)": 40.0, "Undercommon": 10.0, "Sylvestre": 7.0, "Abyssal": 6.0},
    "Half-Elf":        {"Espruar": 28.0, "Thorass": 22.0, "Elven High Speech": 12.0, "Chondathan": 7.0},

    # ==================== NAINS ====================
    "Nain":            {"Nain": 38.0, "Thorass": 10.0, "Draconique": 7.0, "Géant": 6.0},
    "Shield Dwarf":    {"Nain": 40.0, "Thorass": 12.0, "Abyssal": 6.0},
    "Gold Dwarf":      {"Nain": 42.0, "Thorass": 8.0, "Glifo (Drow)": 5.0},

    # ==================== AUTRES RACES ====================
    "Halfelin":        {"Thorass": 30.0, "Tuigan": 8.0, "Chondathan": 7.0, "Illuskan": 6.0},
    "Gnome":           {"Thorass": 24.0, "Nain": 18.0, "Gnomish": 12.0, "Aquan": 6.0},
    "Half-Orc":        {"Orc": 32.0, "Thorass": 18.0, "Goblin": 7.0},
    "Orc":             {"Orc": 38.0, "Goblin": 10.0, "Thorass": 8.0},
    "Tiefling":        {"Infernal": 36.0, "Thorass": 12.0, "Abyssal": 10.0, "Chondathan": 6.0},
    "Dragonborn":      {"Draconique": 40.0, "Thorass": 10.0, "Druidic": 6.0, "Géant": 5.0},

    # ==================== DEFAULT ====================
    "Default":         {"Thorass": 25.0, "Chondathan": 8.0, "Espruar": 6.0, "Nain": 5.0}
}


# ====================== HELPERS ======================
def _calculate_craft_count() -> int:
    """Nombre de compétences d'artisanat : toujours entre 1 et 3"""
    return random.randint(1, 3)


def _calculate_know_count(outdoor_count: int, urban_count: int) -> int:
    """Nombre de connaissances = 10 - (outdoor + urban)"""
    total_skills = outdoor_count + urban_count
    know_count = 10 - total_skills
    return max(0, know_count)   # Évite les valeurs négatives


def _calculate_literacy_count(
    know_count: int, 
    settlement_type: str, 
    ethnicity: str
) -> int:
    """Version drastiquement réduite : beaucoup de personnages ne savent pas lire/écrire"""
    
    if know_count >= 8:
        base = random.randint(1, 3)
    elif know_count >= 5:
        base = random.randint(0, 2)
    else:
        base = random.randint(0, 1)

    # Bonus selon settlement
    if any(x in settlement_type.lower() for x in ["metropolis", "large city", "capitale", "grande"]):
        base += random.randint(0, 2)
    elif any(x in settlement_type.lower() for x in ["large town", "ville moyenne"]):
        base += random.randint(0, 1)

    # Bonus selon ethnie lettrée
    if ethnicity in ["Elf Moon", "Elf Sun", "Elf Star", "Gnome", "Rock Gnome", "Half-Elf", "Aasimar"]:
        base += random.randint(0, 1)

    return max(0, min(4, base))

def _get_region_name(region_id: int) -> str:
    region_map = {1: "Sword Coast", 2: "Waterdeep", 3: "Calimshan", 4: "Dalelands", 5: "Moonsea"}
    return region_map.get(region_id, "Default")


def weighted_sample_without_replacement(population, weights, k):
    """Tirage pondéré sans remplacement (version pure Python)"""
    if k <= 0:
        return []
    
    # Création d'une copie pour ne pas modifier l'original
    population = list(population)
    weights = list(weights)
    
    result = []
    for _ in range(k):
        if not population:
            break
        # Normalisation des poids
        total = sum(weights)
        if total == 0:
            break
        cum_weights = [sum(weights[:i+1]) for i in range(len(weights))]
        
        # Tirage
        r = random.uniform(0, total)
        for i, cum in enumerate(cum_weights):
            if r <= cum:
                result.append(population[i])
                # Suppression de l'élément tiré
                del population[i]
                del weights[i]
                break
    
    return result

def generate_secondary_skills(
    ethnicity: str,
    region_id: int,
    settlement_type: str,
    active_count: int = None   # gardé pour compatibilité
) -> Dict:
    """Génère les compétences secondaires"""
    
    # === NOUVELLE LOGIQUE ===
    skills_data = generate_skills(settlement_type, region_id, ethnicity)
    
    outdoor_count = skills_data["outdoor_count"]
    urban_count = skills_data["urban_count"]
    
    craft_count = _calculate_craft_count()
    know_count = _calculate_know_count(outdoor_count, urban_count)
    literacy_count = _calculate_literacy_count(know_count, settlement_type, ethnicity)

    region_name = _get_region_name(region_id)

    # ====================== 1. CRAFTS ======================
    eth_mod = ethnicity_craft_modifiers.get(ethnicity, {})
    reg_mod = region_craft_modifiers.get(region_name, {})
    sett_mod = settlement_craft_modifiers.get(settlement_type, {})

    craft_names = list(craft_weights.keys())
    final_craft_weights = []
    
    for craft in craft_names:
        base = craft_weights[craft]
        bias = (eth_mod.get(craft, 0) + reg_mod.get(craft, 0) + sett_mod.get(craft, 0))
        final_weight = max(base + bias * 1.65, 0.5)
        final_craft_weights.append(final_weight)

    if craft_count >= len(craft_names):
        craft = craft_names[:]
    else:
        craft = weighted_sample_without_replacement(craft_names, final_craft_weights, craft_count)

    # ====================== 2. CONNAISSANCES ======================
    eth_know_mod = ethnicity_knowledge_modifiers.get(ethnicity, {})
    reg_know_mod = region_knowledge_modifiers.get(region_name, {})
    sett_know_mod = settlement_knowledge_modifiers.get(settlement_type, {})

    know_names = list(knowledge_weights.keys())
    final_know_weights = []
    
    for know in know_names:
        base = knowledge_weights[know]
        bias = (eth_know_mod.get(know, 0) + reg_know_mod.get(know, 0) + sett_know_mod.get(know, 0))
        final_weight = max(base + bias * 2.4, 0.8)
        final_know_weights.append(final_weight)

    if know_count >= len(know_names):
        knowledge = know_names[:]
    else:
        knowledge = weighted_sample_without_replacement(
            know_names, final_know_weights, know_count
        )

    # ====================== 3. LANGUES ÉCRITES ======================
    eth_lit_mod = ethnicity_literacy_modifiers.get(ethnicity, ethnicity_literacy_modifiers["Default"])
    lang_names = list(eth_lit_mod.keys()) if eth_lit_mod else ["Thorass"]

    literacy: List[str] = []

    if literacy_count > 0:
        # Première langue écrite = première langue parlée (80% de chance)
        spoken_languages_temp = generate_languages(ethnicity, region_id, (active_count or 0) * 2)
        first_spoken = spoken_languages_temp[0] if spoken_languages_temp else None

        if first_spoken and random.random() < 0.80 and first_spoken in eth_lit_mod:
            first_lang = first_spoken
        else:
            favored = list(eth_lit_mod.keys())
            if not favored:
                favored = ["Thorass"]
            native_weights = [eth_lit_mod.get(lang, 5.0) * 3.8 for lang in favored]
            first_lang = random.choices(favored, weights=native_weights, k=1)[0]

        literacy.append(first_lang)

        # Langues écrites supplémentaires
        remaining = literacy_count - 1
        if remaining > 0:
            final_weights = [0.3 if lang == first_lang else eth_lit_mod.get(lang, 1.0) * 4.0 
                           for lang in lang_names]
            additional = random.choices(lang_names, weights=final_weights, k=remaining)
            
            for lang in additional:
                if lang not in literacy:
                    literacy.append(lang)

    # ====================== 4. LANGUES PARLÉES ======================
    spoken_languages = generate_languages(
        ethnicity=ethnicity,
        region_id=region_id,
        skill_modifier=(active_count or 0) * 2
    )

    # ====================== RETURN ======================
    return {
        "knowledge": knowledge,
        "craft": craft,
        "literacy": literacy,
        "spoken_languages": spoken_languages,
        "total_knowledge": len(knowledge),
        "total_craft": len(craft),
        "total_literacy": len(literacy),
        "total_spoken": len(spoken_languages)
    }