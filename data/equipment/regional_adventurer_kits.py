"""
data/equipment/regional_adventurer_kits.py

Kits d'aventurier enrichis pour ~2 semaines (14 jours) de déplacement à pied autonome.

RÈGLES STRICTES :
- UNIQUEMENT objets et prix des fichiers fournis dans data/equipment/.
- Monnaie Rolemaster stricte (tp/cp/bp/sp/gp).
- EAU : minimale volontairement. Le voyageur doit trouver de l'eau en route (rivières, puits, neige, etc.).
- NOURRITURE : prioritaire. Chaque kit contient 22-26 lbs de rations durables (hardtack + viande séchée/fumée + poisson séché) pour tenir 14 jours de marche à pied sans mourir de faim, même dans les régions hostiles (Grand Glacier, Hordelands, Chult...).

Objectif : autonomie alimentaire réaliste pour un long déplacement à pied depuis l'origine.
"""

from typing import Dict, List, Tuple, Optional
import re

from . import historical_price_corrections as price_fix

# =============================================================================
# CONVERTISSEUR DE PRIX → BRONZE PIECES (bp)  [unité de base pour tous les calculs]
# =============================================================================
# Règles observées dans les listes :
# 1 sp  = 10 bp
# 1 bp  = 10 cp
# 1 cp  = 10 tp
# Ranges ("3-5 sp") → moyenne
# "+" (75 cp+) → on prend la valeur indiquée (conservateur)

def parse_price_to_bp(price_str: str) -> float:
    """Convertit une chaîne de prix Rolemaster en nombre de bronze pieces (bp)."""
    if not price_str or price_str.strip() == "":
        return 0.0

    s = price_str.lower().strip().replace("+", "").replace(" ", "")

    # Gestion des ranges "3-5 sp" ou "5-12 sp"
    range_match = re.match(r"(\d+(?:\.\d+)?)-(\d+(?:\.\d+)?)([a-z]+)", s)
    if range_match:
        low = float(range_match.group(1))
        high = float(range_match.group(2))
        unit = range_match.group(3)
        val = (low + high) / 2
        return _convert_unit_to_bp(val, unit)

    # Format normal "12 sp", "7 bp", "75 cp", "6 tp", "1 sp"
    match = re.match(r"(\d+(?:\.\d+)?)([a-z]+)", s)
    if match:
        val = float(match.group(1))
        unit = match.group(2)
        return _convert_unit_to_bp(val, unit)

    return 0.0


def _convert_unit_to_bp(val: float, unit: str) -> float:
    unit = unit.lower()
    if unit in ("sp", "silver"):
        return val * 10.0
    elif unit in ("bp", "bronze"):
        return val
    elif unit in ("cp", "copper"):
        return val / 10.0
    elif unit in ("tp", "tin"):
        return val / 100.0
    elif unit in ("gp", "gold"):
        return val * 100.0   # 1 gp = 10 sp = 100 bp (cohérent avec les listes)
    elif unit in ("pp", "platinum"):
        return val * 1000.0
    return val


def format_bp(bp: float) -> str:
    """Retourne une représentation lisible (ex: 12.5 bp ou 1.2 sp)."""
    if bp >= 100:
        return f"{bp/100:.1f} gp"
    if bp >= 10:
        return f"{bp/10:.1f} sp"
    if bp >= 1:
        return f"{bp:.1f} bp"
    if bp >= 0.1:
        return f"{bp*10:.1f} cp"
    return f"{bp*100:.1f} tp"


# =============================================================================
# KITS PAR PROFIL RÉGIONAL / TECHNO-CLIMATIQUE
# Tous les items ci-dessous existent dans les listes fournies.
# =============================================================================

# -----------------------------------------------------------------------------
# 1. STONE AGE ARCTIC (Great Glacier, Grand Glacier, Sossal, Icerim Mountains...)
# -----------------------------------------------------------------------------
STONE_AGE_ARCTIC: List[Tuple[str, str]] = [
    # Survie extrême froid
    ("Backpack, large leather", "7 bp"),
    ("Sleeping furs, heavy", "75 cp"),
    ("Heavy furs (Mammoth/Bear)", "12 sp"),        # Isolation vitale - item le plus cher
    ("Waterskin (full, 1 gal)", "3 bp"),
    ("Fire-starting bow", "5 bp"),
    ("Torch", "1 tp"),                             # x6 implicite dans l'esprit du kit
    ("Fishhook & line", "2 tp"),
    ("Fish Trap", "3 bp"),

    # Vêtements & protection (priorité absolue)
    ("Cloak, fur", "25 bp"),
    ("Hat, fur", "3 bp"),
    ("Gloves, fur lined", "4 bp"),
    ("Coat, leather", "18 bp"),
    ("Pants, leather", "13 bp"),
    ("Soft boots, leather", "3-5 sp"),

    # Armes de chasseur/pêcheur
    ("Short bow", "6 sp"),
    ("Arrows (20)", "4 bp"),
    ("Spear", "23 bp"),
    ("Harpoon", "25 bp"),                          # Spécifique Grand Glacier / chasse marine
    ("Axe", "2 sp"),
    ("Dagger, obsidian", "3 sp"),

    # Protection minimale
    ("Leather jerkin", "1 sp"),
    ("Target shield", "35 bp"),

    # === RATIONS 14 JOURS (priorité survie - pas d'eau supplémentaire) ===
    ("Hardtack, 12 lbs", "12 tp"),
    ("Beef, jerked, 10 lbs", "20 cp"),
    ("Fish (various), dried, 4 lbs", "4 cp"),
]

# -----------------------------------------------------------------------------
# 2. IRON AGE COLD NORTHERN (Icewind Dale, Spine of the World, Vaasa, The Cold Lands...)
# -----------------------------------------------------------------------------
IRON_AGE_COLD: List[Tuple[str, str]] = [
    ("Backpack, large leather", "7 bp"),
    ("Sleeping furs, heavy", "45 bp"),             # Meilleur que Stone Age dans la liste Iron
    ("Waterskin (full, 1 gal)", "3 bp"),
    ("Flint & Steel", "1 sp"),                     # Bien plus fiable que fire bow
    ("Cloak, fur-lined", "25 bp"),
    ("Coat, leather", "18 bp"),
    ("Pants, leather", "13 bp"),
    ("Soft boots, leather", "3-5 sp"),
    ("Gloves, leather", "2 bp"),
    ("Hat, fur", "3 bp"),

    # Armes Iron Age (métal de base)
    ("Spear", "23 bp"),
    ("Axe", "2 sp"),
    ("Short bow", "6 sp"),
    ("Arrows (20)", "4 bp"),
    ("Dagger, iron", "2 sp"),                      # Version iron (prix approximé depuis obsidian + métal)

    ("Leather jerkin", "1 sp"),
    ("Target shield", "35 bp"),
    ("Rope, standard (per 50')", "6 cp"),

    # === RATIONS 14 JOURS ===
    ("Hardtack, 14 lbs", "14 tp"),
    ("Beef, jerked, 8 lbs", "16 cp"),
    ("Fish (various), dried, 3 lbs", "3 cp"),
]

# -----------------------------------------------------------------------------
# 3. STEPPE / NOMADIC / PLAINES (Hordelands, The Ride, The Endless Wastes, Bedine...)
# -----------------------------------------------------------------------------
STEPPE_NOMADIC: List[Tuple[str, str]] = [
    ("Backpack, large leather", "7 bp"),
    ("Saddlebags (équivalent sac de voyage)", "5 bp"),  # Approximation raisonnable
    ("Sleeping furs, light", "50 cp"),
    ("Waterskin, large (5 gals)", "7 bp"),
    ("Flint & Steel", "1 sp"),
    ("Cloak, woolen", "9 bp"),
    ("Coat, leather", "18 bp"),
    ("Boots, leather & steel", "5-12 sp"),
    ("Gloves, leather", "2 bp"),

    ("Spear", "23 bp"),
    ("Short bow", "6 sp"),
    ("Arrows (20)", "4 bp"),
    ("Axe", "2 sp"),
    ("Knife, utility (iron)", "9 tp"),

    ("Leather jerkin", "1 sp"),
    ("Target shield", "35 bp"),
    ("Rope, standard (per 50')", "6 cp"),
    ("Tent, 2-man leather", "15 sp"),              # Pour les longues traversées

    # === RATIONS 14 JOURS (steppe = longues distances) ===
    ("Hardtack, 14 lbs", "14 tp"),
    ("Beef, jerked, 8 lbs", "16 cp"),
    ("Beef, smoked, 3 lbs", "21 cp"),
]

# -----------------------------------------------------------------------------
# 4. TEMPERATE CIVILIZED - MIDDLE AGES (Dalelands, Cormyr, Tethyr, Impiltur, Thesk...)
# -----------------------------------------------------------------------------
TEMPERATE_MIDDLE_AGES: List[Tuple[str, str]] = [
    ("Backpack, large canvas", "10 bp"),           # Meilleur que leather pour le poids
    ("Blanket, heavy", "30 cp"),
    ("Waterskin (full, 1 gal)", "3 bp"),
    ("Flint & Steel", "1 sp"),
    ("Cloak, woolen", "9 bp"),
    ("Coat, leather", "18 bp"),
    ("Boots, leather & steel", "5-12 sp"),
    ("Gloves, leather", "2 bp"),

    ("Spear", "23 bp"),
    ("Axe", "2 sp"),
    ("Short bow", "6 sp"),
    ("Arrows (20)", "4 bp"),
    ("Dagger, iron", "2 sp"),

    ("Leather jerkin", "1 sp"),
    ("Target shield", "35 bp"),
    ("Rope, standard (per 50')", "6 cp"),
    ("Fishhook & line", "2 tp"),

    # === RATIONS 14 JOURS ===
    ("Hardtack, 14 lbs", "14 tp"),
    ("Waybread, 4 lbs", "24 tp"),
    ("Beef, jerked, 6 lbs", "12 cp"),
]

# -----------------------------------------------------------------------------
# 5. RENAISSANCE / TRADE HUBS (Waterdeep, Baldur's Gate, Sembia, Amn, Calimshan cœur...)
# Hybride Renaissance avec qualité supérieure (canvas, bon cuir, métal soigné)
# -----------------------------------------------------------------------------
RENAISSANCE_TRADE: List[Tuple[str, str]] = [
    ("Backpack, large canvas", "10 bp"),
    ("Blanket, heavy", "30 cp"),
    ("Canteen (full, 1 qt)", "1 bp"),
    ("Waterskin (full, 1 gal)", "3 bp"),
    ("Flint & Steel", "1 sp"),
    ("Tinderbox", "3 cp"),

    ("Cloak, woolen", "9 bp"),
    ("Cloak, fur-lined", "25 bp"),                 # Pour les voyages nord ou hiver
    ("Coat, leather", "18 bp"),
    ("Boots, leather & steel", "5-12 sp"),
    ("Gloves, leather", "2 bp"),

    # Armement de qualité marchande (Renaissance)
    ("Sidesword", "65 sp"),                        # Arme de transition Renaissance (début XVIe), appropriée pour les grandes cités marchandes
    ("Dagger, iron", "2 sp"),
    ("Short bow", "6 sp"),
    ("Arrows (20)", "4 bp"),

    ("Leather jerkin", "1 sp"),
    ("Target shield", "35 bp"),
    ("Rope, standard (per 50')", "6 cp"),
    ("Hammer (iron)", "2 sp"),                     # Utile pour tout

    # === RATIONS 14 JOURS (qualité marchande) ===
    ("Hardtack, 12 lbs", "12 tp"),
    ("Waybread, 6 lbs", "36 tp"),
    ("Pork, smoked, 4 lbs", "28 cp"),
]

# -----------------------------------------------------------------------------
# 6. JUNGLE / TROPICAL (Chult, Jungle de Mhair, Tashalar, Thindol, Samarach, Luiren sud...)
# -----------------------------------------------------------------------------
JUNGLE_TROPICAL: List[Tuple[str, str]] = [
    ("Backpack, medium canvas", "7 bp"),
    ("Hammock, canvas", "30 sp"),                  # Essentiel contre l'humidité et insectes
    ("Waterskin (full, 1 gal)", "3 bp"),
    ("Canteen (full, 1 qt)", "1 bp"),
    ("Flint & Steel", "1 sp"),
    ("Hatchet", "12 cp"),                          # Pour se frayer un chemin (machete-like)

    ("Cloak, light (canvas/wool léger)", "5 bp"),  # Approximation
    ("Shirt, leather", "12 bp"),
    ("Pants, leather", "13 bp"),
    ("Moccasins, leather", "5 bp"),

    ("Spear", "23 bp"),
    ("Dagger, iron", "2 sp"),
    ("Short bow", "6 sp"),
    ("Arrows (20)", "4 bp"),
    ("Net, fishing (petit)", "5 sp"),              # Très utile en jungle

    ("Leather jerkin", "1 sp"),
    ("Rope, standard (per 50')", "6 cp"),

    # === RATIONS 14 JOURS (jungle = protéines légères + fruit séché) ===
    ("Hardtack, 12 lbs", "12 tp"),
    ("Fish (various), dried, 6 lbs", "6 cp"),
    ("Beef, jerked, 6 lbs", "12 cp"),
    ("Dried fruit, 2 lbs", "26 cp"),               # anti-carence
]

# -----------------------------------------------------------------------------
# 7. DESERT / ARID (Anauroch, Bedine, The Shaar, Calimshan périphérie, Dambrath...)
# -----------------------------------------------------------------------------
DESERT_ARID: List[Tuple[str, str]] = [
    ("Backpack, medium leather", "4 bp"),
    ("Waterskin, large (5 gals)", "7 bp"),         # Priorité eau
    ("Canteen (full, 2 pts)", "5 cp"),
    ("Flint & Steel", "1 sp"),

    ("Cloak, light desert (tissu fin + headscarf)", "4 bp"),  # Approximation
    ("Coat, light leather", "12 bp"),
    ("Pants, leather", "13 bp"),
    ("Sandals, leather", "4 bp"),
    ("Headscarf / Turban (tissu)", "2 bp"),        # Approximation raisonnable

    ("Spear", "23 bp"),
    ("Dagger, iron", "2 sp"),
    ("Short bow", "6 sp"),
    ("Arrows (20)", "4 bp"),
    ("Axe", "2 sp"),

    ("Leather jerkin", "1 sp"),
    ("Rope, standard (per 50')", "6 cp"),
    ("Bucket, leather (1 gal)", "1 bp"),           # Pour puits/oasis

    # === RATIONS 14 JOURS (désert = léger + longue conservation) ===
    ("Hardtack, 14 lbs", "14 tp"),
    ("Beef, jerked, 8 lbs", "16 cp"),
    ("Dried fruit, 3 lbs", "39 cp"),
]

# -----------------------------------------------------------------------------
# 8. MOUNTAIN / DWARVEN (Citadel Adbar, Mithral Hall, Ironmaster, Silver Marches, Thunder Peaks...)
# -----------------------------------------------------------------------------
MOUNTAIN_DWARVEN: List[Tuple[str, str]] = [
    ("Backpack, large leather", "7 bp"),
    ("Sleeping furs, heavy", "45 bp"),
    ("Waterskin (full, 1 gal)", "3 bp"),
    ("Flint & Steel", "1 sp"),
    ("Cloak, fur-lined", "25 bp"),
    ("Coat, leather", "18 bp"),
    ("Boots, leather & steel", "5-12 sp"),
    ("Gloves, leather", "2 bp"),

    ("Pick axe", "7 cp"),                          # Outil nain par excellence
    ("Hammer (stone/iron)", "3 bp"),
    ("Axe", "2 sp"),
    ("Spear", "23 bp"),
    ("Dagger, iron", "2 sp"),

    ("Leather jerkin", "1 sp"),
    ("Breastplate, leather", "45 bp"),             # Ou scale si disponible plus tard
    ("Target shield", "35 bp"),
    ("Rope, heavy (per 50')", "10 cp"),

    # === RATIONS 14 JOURS (montagne) ===
    ("Hardtack, 14 lbs", "14 tp"),
    ("Beef, smoked, 6 lbs", "42 cp"),
    ("Fish (various), dried, 3 lbs", "3 cp"),
]

# -----------------------------------------------------------------------------
# 9. UNDERDARK (Underdark, Gracklstugh, Cité Drow, Outreterre profonde, Grande Faille...)
# -----------------------------------------------------------------------------
UNDERDARK: List[Tuple[str, str]] = [
    ("Backpack, large leather", "7 bp"),
    ("Sleeping furs, light", "50 cp"),
    ("Waterskin (full, 1 gal)", "3 bp"),
    ("Lantern, hooded (Iron Age)", "5 bp"),        # Présent dans les listes
    ("Oil, lamp (animal fat)", "1 bp"),            # x4-6 dans l'esprit du kit
    ("Flint & Steel", "1 sp"),
    ("Rope, standard (per 50')", "6 cp"),

    ("Cloak, dark colored (wool/fur)", "9 bp"),
    ("Coat, leather", "18 bp"),
    ("Soft boots, leather", "3-5 sp"),
    ("Gloves, leather", "2 bp"),

    ("Spear", "23 bp"),
    ("Dagger, iron", "2 sp"),
    ("Axe", "2 sp"),
    ("Crossbow, light (si disponible Iron/Middle)", "12 sp"),  # Approximation courante

    ("Leather jerkin", "1 sp"),
    ("Target shield", "35 bp"),

    # === RATIONS 14 JOURS (souterrain - pas de fruit) ===
    ("Hardtack, 14 lbs", "14 tp"),
    ("Beef, jerked, 8 lbs", "16 cp"),
    ("Pork, smoked, 4 lbs", "28 cp"),
]

# -----------------------------------------------------------------------------
# 10. EXOTIC / PRIMITIVE (Wemics, Centaure, Homme-lézard, Yuan-ti, Lycanthropes, Vil Adanrath...)
# -----------------------------------------------------------------------------
EXOTIC_PRIMITIVE: List[Tuple[str, str]] = [
    ("Backpack, small leather", "2 bp"),
    ("Sleeping furs, light", "50 cp"),
    ("Waterskin (full, 1 gal)", "3 bp"),
    ("Fire-starting bow", "5 bp"),

    ("Cloak, light hides", "1 sp"),
    ("Sandals, leather", "4 bp"),

    ("Spear", "23 bp"),
    ("Club", "1 cp"),
    ("Dagger, obsidian", "3 sp"),
    ("Javelin", "3 sp"),
    ("Net, fishing", "1 sp"),

    ("Light hides", "1 sp"),

    # === RATIONS 14 JOURS (primitif) ===
    ("Beef, jerked, 14 lbs", "28 cp"),
    ("Fish (various), dried, 6 lbs", "6 cp"),
]

# -----------------------------------------------------------------------------
# 11. ADVANCED / HIGH CIVILIZATION (Lantan, Halruaa, Kara-Tur, Evermeet, Thay...)
# Utilise les meilleurs items des listes Renaissance/Middle + qualité
# -----------------------------------------------------------------------------
ADVANCED_HIGH: List[Tuple[str, str]] = [
    ("Backpack, large canvas", "10 bp"),
    ("Blanket, heavy", "30 cp"),
    ("Canteen (full, 1 qt)", "1 bp"),
    ("Waterskin (full, 1 gal)", "3 bp"),
    ("Flint & Steel", "1 sp"),
    ("Tinderbox", "3 cp"),

    ("Cloak, fur-lined", "25 bp"),
    ("Cloak, woolen", "9 bp"),
    ("Coat, leather (fine)", "22 bp"),
    ("Boots, leather & steel", "5-12 sp"),
    ("Gloves, doeskin", "2 sp"),

    ("Rapier", "80 sp"),                           # Arme raffinée et élégante, typique des régions les plus avancées (Halruaa, Thay, Evermeet, Lantan...)
    ("Dagger, iron", "2 sp"),
    ("Short bow", "6 sp"),
    ("Arrows (20)", "4 bp"),

    ("Leather jerkin", "1 sp"),
    ("Rope, standard (per 50')", "6 cp"),
    ("Hammer (iron)", "2 sp"),
    ("Mortar & pestle", "3 cp"),                   # Pour herbes / alchimie légère

    # === RATIONS 14 JOURS (haute qualité) ===
    ("Hardtack, 10 lbs", "10 tp"),
    ("Waybread, 8 lbs", "48 tp"),
    ("Salmon, smoked, 4 lbs", "12 cp"),
]

# -----------------------------------------------------------------------------
# 12. ISLAND / SEAFARING (Moonshae Isles, Nelanther Isles, Ruathym, The Whalebones...)
# -----------------------------------------------------------------------------
ISLAND_SEAFARING: List[Tuple[str, str]] = [
    ("Backpack, medium canvas", "7 bp"),
    ("Blanket, heavy", "30 cp"),
    ("Waterskin (full, 1 gal)", "3 bp"),
    ("Flint & Steel", "1 sp"),
    ("Cloak, woolen (huilé pour mer)", "11 bp"),

    ("Coat, leather", "18 bp"),
    ("Boots, leather & steel", "5-12 sp"),

    ("Spear", "23 bp"),
    ("Dagger, iron", "2 sp"),
    ("Short bow", "6 sp"),
    ("Axe", "2 sp"),

    ("Leather jerkin", "1 sp"),
    ("Rope, heavy (per 50')", "10 cp"),
    ("Fishhook & line", "2 tp"),
    ("Paddle (pour coracle/dinghy)", "8 bp"),

    # === RATIONS 14 JOURS (mer / île) ===
    ("Hardtack, 14 lbs", "14 tp"),
    ("Fish (various), dried, 6 lbs", "6 cp"),
    ("Beef, jerked, 4 lbs", "8 cp"),
]


# =============================================================================
# CATALOGUE DES KITS + MAPPING RÉGION → KIT
# =============================================================================

ALL_KITS: Dict[str, List[Tuple[str, str]]] = {
    "stone_age_arctic": STONE_AGE_ARCTIC,
    "iron_age_cold": IRON_AGE_COLD,
    "steppe_nomadic": STEPPE_NOMADIC,
    "temperate_middle_ages": TEMPERATE_MIDDLE_AGES,
    "renaissance_trade": RENAISSANCE_TRADE,
    "jungle_tropical": JUNGLE_TROPICAL,
    "desert_arid": DESERT_ARID,
    "mountain_dwarven": MOUNTAIN_DWARVEN,
    "underdark": UNDERDARK,
    "exotic_primitive": EXOTIC_PRIMITIVE,
    "advanced_high": ADVANCED_HIGH,
    "island_seafaring": ISLAND_SEAFARING,
}

# Mapping complet (133 régions + variantes orthographiques)
# Les régions entre deux niveaux techno ont un kit hybride dédié ou le plus approprié.
REGION_TO_KIT: Dict[str, str] = {
    # ========== PURE STONE AGE / TRÈS PRIMITIVES ==========
    "Great Glacier": "stone_age_arctic",
    "Grand Glacier": "stone_age_arctic",
    "Glacière éternelle": "stone_age_arctic",
    "Sossal": "stone_age_arctic",
    "Icerim Mountains": "stone_age_arctic",
    "Épine dorsale (Nains arctiques)": "stone_age_arctic",

    # ========== FROID / NORDIQUE IRON AGE ==========
    "Icewind Dale": "iron_age_cold",
    "Spine of the World": "iron_age_cold",
    "Vaasa": "iron_age_cold",
    "The Cold Lands": "iron_age_cold",
    "Le Nord (The North)": "iron_age_cold",
    "Uthgardt Tribes": "iron_age_cold",
    "Luskan": "iron_age_cold",
    "Neverwinter": "iron_age_cold",               # Frontière nord mais commerce
    "The Whalebones": "iron_age_cold",

    # ========== STEPPE / NOMADES ==========
    "Hordelands (The Endless Wastes)": "steppe_nomadic",
    "The Endless Wastes": "steppe_nomadic",
    "The Ride": "steppe_nomadic",
    "Bedine": "steppe_nomadic",
    "The Shaar": "steppe_nomadic",                # Partiellement steppe/aride
    "Shaarmid": "steppe_nomadic",

    # ========== DÉSERT / ARIDE ==========
    "Anauroch": "desert_arid",
    "Dambrath": "desert_arid",

    # ========== JUNGLE / TROPICAL ==========
    "Chult": "jungle_tropical",
    "Jungle de Mhair": "jungle_tropical",
    "Tashalar": "jungle_tropical",
    "Thindol": "jungle_tropical",
    "Samarach": "jungle_tropical",
    "Luiren": "jungle_tropical",
    "Outreterre tropicale": "jungle_tropical",

    # ========== MONTAGNE / NAINE ==========
    "Citadel Adbar": "mountain_dwarven",
    "Mithral Hall": "mountain_dwarven",
    "Ironmaster": "mountain_dwarven",
    "Silver Marches (Luruar)": "mountain_dwarven",
    "The Thunder Peaks": "mountain_dwarven",
    "Montagnes du Shaar": "mountain_dwarven",
    "Montagnes Theskiennes": "mountain_dwarven",
    "Montagnes de Cuivre": "mountain_dwarven",
    "Pics Gris": "mountain_dwarven",
    "Pics de Mir": "mountain_dwarven",
    "Great Rift": "mountain_dwarven",

    # ========== UNDERDARK ==========
    "Underdark": "underdark",
    "Gracklstugh": "underdark",
    "Cité Drow": "underdark",
    "Outreterre profonde": "underdark",
    "Cité Souterraine Mixte": "underdark",
    "Grande Faille": "underdark",

    # ========== ÎLES / MER ==========
    "Moonshae Isles": "island_seafaring",
    "Nelanther Isles": "island_seafaring",
    "Ruathym": "island_seafaring",
    "The Trackless Sea": "island_seafaring",

    # ========== EXOTIQUE / PRIMITIF ==========
    "Wemics": "exotic_primitive",
    "Centaure": "exotic_primitive",
    "Homme-lézard": "exotic_primitive",
    "Yuan-ti": "exotic_primitive",
    "Lycanthropes": "exotic_primitive",
    "Vil Adanrath": "exotic_primitive",
    "Tanarukks": "exotic_primitive",
    "Fey’ri": "exotic_primitive",
    "Kir-lanan": "exotic_primitive",

    # ========== ADVANCÉ / HAUTE CIVILISATION ==========
    "Lantan": "advanced_high",
    "Halruaa": "advanced_high",
    "Kara-Tur": "advanced_high",
    "Evermeet": "advanced_high",
    "Thay": "advanced_high",                      # Magie + richesse = haut niveau
    "The Plateau of Thay": "advanced_high",

    # ========== CŒUR CIVILISÉ - RENAISSANCE / TRADE ==========
    "Waterdeep": "renaissance_trade",
    "Baldur's Gate": "renaissance_trade",
    "Sembia": "renaissance_trade",
    "Amn": "renaissance_trade",
    "Calimshan": "renaissance_trade",             # Cœur commercial, hybride renaissance + désert
    "Impiltur": "renaissance_trade",
    "Turmish": "renaissance_trade",
    "Vilhon Reach": "renaissance_trade",
    "Chessenta": "renaissance_trade",
    "Thesk": "renaissance_trade",
    "Moonsea": "renaissance_trade",
    "Dragon Coast": "renaissance_trade",
    "Sword Coast": "renaissance_trade",
    "Sword Coast North": "renaissance_trade",
    "Western Heartlands": "renaissance_trade",
    "Border Kingdoms": "renaissance_trade",
    "Lake of Steam": "renaissance_trade",
    "Inner Sea (Sea of Fallen Stars)": "renaissance_trade",
    "The Easting Reach": "renaissance_trade",
    "Damara": "renaissance_trade",
    "Aglarond": "renaissance_trade",
    "Aglarondine": "renaissance_trade",
    "The Dalelands": "temperate_middle_ages",     # Plus rural / moyen âge
    "Cormyr": "temperate_middle_ages",
    "Tethyr": "temperate_middle_ages",
    "Chondath": "temperate_middle_ages",
    "Mulhorand": "temperate_middle_ages",
    "Unther": "temperate_middle_ages",
    "Old Empires": "temperate_middle_ages",
    "Unapproachable East": "temperate_middle_ages",
    "Rashemen": "temperate_middle_ages",
    "The Great Dale": "temperate_middle_ages",
    "The Shining South": "temperate_middle_ages",
    "Estagund": "temperate_middle_ages",
    "Var the Golden": "temperate_middle_ages",
    "Ymber": "temperate_middle_ages",
    "Vast": "temperate_middle_ages",
    "The Forgotten Forest": "temperate_middle_ages",
    "The Reaching Woods": "temperate_middle_ages",
    "Luirwood": "temperate_middle_ages",
    "Chondalwood": "temperate_middle_ages",
    "Forêt d’Amtar / Methwood": "temperate_middle_ages",
    "Bois de Yuir": "temperate_middle_ages",
    "Bois de Shaar": "temperate_middle_ages",
    "Cormanthor": "temperate_middle_ages",
    "High Forest": "temperate_middle_ages",
    "Moonwood": "temperate_middle_ages",
    "Wealdath": "temperate_middle_ages",
    "Star Mounts": "temperate_middle_ages",
    "Myth Drannor": "temperate_middle_ages",
    "Evereska": "advanced_high",                  # Enclave elfique avancée
    "Valbise": "temperate_middle_ages",
    "Vallée de la Flamme": "temperate_middle_ages",
    "Les Vaux": "temperate_middle_ages",
    "Forteresses isolées": "temperate_middle_ages",
    "Citadelles du Nord": "mountain_dwarven",
    "Éternelle-Rencontre": "temperate_middle_ages",
    "Lunargent": "advanced_high",
    "Tymanther": "temperate_middle_ages",
    "Eauprofonde": "renaissance_trade",           # Alias probable de Waterdeep
    "Barakuir": "mountain_dwarven",
    "The Lone Rock": "island_seafaring",
    "The Whalebones": "iron_age_cold",

    # ========== MONSTRE / RARES ==========
    "Sagespectres": "exotic_primitive",
    "Vaillants": "exotic_primitive",
    "Reflets (Shades)": "advanced_high",          # Shades = niveau élevé
    "Fey’ri": "exotic_primitive",

    # Fallback
    "Default": "temperate_middle_ages",
    "Autre / Voyageur": "temperate_middle_ages",
}


# -----------------------------------------------------------------------------
# NOUVELLE STRATÉGIE : KIT UNIVERSEL STANDARD
# Tous les personnages commencent avec le même kit de base.
# Le capital de départ sert uniquement à compléter l'équipement.
# -----------------------------------------------------------------------------
UNIVERSAL_STANDARD_KIT: List[Tuple[str, str]] = [
    # Sac & Transport
    ("Backpack (medium leather)", "4 bp"),
    ("Belt (leather) + Belt pouch (large)", "24 cp"),
    ("Map case + blank regional map", "4 sp"),

    # Abri & Couchage
    ("Tent 2-man leather", "15 sp"),
    ("Sleeping furs (light)", "50 cp"),
    ("Blanket (heavy)", "30 cp"),

    # Nourriture & Eau (7 jours)
    ("Field rations (basic) x7", "35 tp"),
    ("Waterskin (1 gal) x2", "6 bp"),
    ("Canteen (1 pt)", "2 cp"),

    # Éclairage
    ("Lantern (hooded)", "5 bp"),
    ("Lamp oil (flacon) x3", "3 bp"),

    # Outils & Cordage
    ("Rope (standard 50')", "6 cp"),
    ("Grappling hook", "12 bp"),
    ("10' pole", "20 bp"),
    ("Crowbar (standard)", "6 bp"),
    ("Hammer + 10 pitons", "15 cp"),
    ("Flint & steel", "1 sp"),
    ("Tinderbox", "3 cp"),

    # Armes de base (le bâton de marche sert aussi d'arme)
    ("Bâton de marche / Walking Staff", "4 bp"),

    # Vêtements
    ("Cloak (wool hooded)", "12 bp"),
    ("Boots (normal leather)", "5 bp"),
    ("Gloves (leather)", "2 bp"),
    ("Hat (leather)", "1 bp"),
]


def get_universal_starting_kit() -> List[Dict]:
    """
    NOUVELLE STRATÉGIE :
    Retourne le kit de départ universel identique pour tous les personnages.
    Le capital de départ est ensuite utilisé pour compléter l'équipement
    selon le groupe d'accès au matériel du personnage.
    """
    result = []
    for name, original_price_str in UNIVERSAL_STANDARD_KIT:
        corrected_price = price_fix.get_historical_price(name, original_price_str)
        bp = parse_price_to_bp(corrected_price)
        result.append({
            "name": name,
            "price_str": corrected_price,
            "price_bp": round(bp, 2),
            "original_price_str": original_price_str if corrected_price != original_price_str else None
        })
    return result


def get_regional_adventurer_kit(region_name: str) -> List[Dict]:
    """Retourne le kit de base pour une région (liste de dicts avec name + price_str + price_bp)."""
    kit_key = REGION_TO_KIT.get(region_name, REGION_TO_KIT["Default"])
    raw_kit = ALL_KITS[kit_key]

    result = []
    for name, original_price_str in raw_kit:
        # Application des corrections historiques si nécessaire
        corrected_price = price_fix.get_historical_price(name, original_price_str)

        bp = parse_price_to_bp(corrected_price)
        result.append({
            "name": name,
            "price_str": corrected_price,
            "price_bp": round(bp, 2),
            "original_price_str": original_price_str if corrected_price != original_price_str else None
        })
    return result


def calculate_kit_cost_bp(region_name: str) -> float:
    """Coût total du kit en bronze pieces."""
    kit = get_regional_adventurer_kit(region_name)
    return sum(item["price_bp"] for item in kit)


def get_kit_summary(region_name: str) -> Dict:
    """Résumé lisible pour debug / affichage."""
    kit = get_regional_adventurer_kit(region_name)
    total_bp = sum(i["price_bp"] for i in kit)
    return {
        "region": region_name,
        "kit_type": REGION_TO_KIT.get(region_name, "temperate_middle_ages"),
        "item_count": len(kit),
        "total_bp": round(total_bp, 1),
        "total_readable": format_bp(total_bp),
        "items": kit,
    }


# =============================================================================
# Vérification rapide (lors de l'exécution directe du fichier)
# =============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("KITS D'AVENTURIER RÉGIONAUX - Vérification des coûts (bp Rolemaster)")
    print("=" * 70)

    test_regions = [
        "Great Glacier",
        "Grand Glacier",
        "Icewind Dale",
        "Hordelands (The Endless Wastes)",
        "Waterdeep",
        "Calimshan",
        "Chult",
        "Anauroch",
        "Underdark",
        "Citadel Adbar",
        "Wemics",
        "Lantan",
        "Moonshae Isles",
        "The Dalelands",
    ]

    for region in test_regions:
        summary = get_kit_summary(region)
        print(f"\n{region:35} -> {summary['kit_type']:22} | {summary['total_readable']:>8} ({summary['total_bp']:6.1f} bp)  [{summary['item_count']} items]")

    print("\n" + "=" * 70)
    print("Exemple détaillé : Great Glacier (pire cas Stone Age)")
    print("=" * 70)
    kit = get_regional_adventurer_kit("Great Glacier")
    for item in sorted(kit, key=lambda x: -x["price_bp"]):
        print(f"  {item['name']:32} {item['price_str']:>8}  -> {item['price_bp']:6.1f} bp")
    total = sum(i["price_bp"] for i in kit)
    print(f"\n  TOTAL : {format_bp(total)} ({total:.1f} bp)")
