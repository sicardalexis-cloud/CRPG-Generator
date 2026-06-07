# =============================================
# skill_data.py
# =============================================
import random
from typing import Dict, List, Set

# =============================================
# LISTES DES SKILLS
# =============================================

outdoor_skills_list = [
    "Hermetic Medicine", "Battlefield Riding", "Dark Water Swimming", "Primitive Fire Mastery",
    "Wild Plant Foraging", "Advanced Tracking", "Forest Stealth", "Mountain Endurance",
    "Technical Rock Climbing", "Complex Terrain Navigation", "Desert Water Mastery",
    "Desert Thermal Endurance", "Open Land Navigation", "Marsh Movement", "Marsh Disease Resistance",
    "Wetland Tracking", "Extreme Cold Resistance", "Snow and Ice Shelter Building", "Arctic Hunting",
    "Total Darkness Navigation", "Subterranean Hazard Resistance", "Confined Space Stealth", "Underground Navigation",
    "Oceanic Navigation", "Deep-Sea Fishing", "Storm and Seasickness Mastery", "Plains Tracking",
    "Savanna Plant Knowledge", "Coastal Survival", "Littoral Foraging", "Island Navigation",
    "Trapping and Snaring", "Game Butchering and Preservation", "Weather Reading",
    "Rope Making and Knot Mastery", "Shelter Construction", "Forced March Endurance",
    "River Crossing", "Wild Animal Handling", "Field Weapon Maintenance", "Signaling and Rescue"
]



# =============================================
# COMPÉTENCES URBAINES PONDERÉES
# =============================================

URBAN_SKILLS_WITH_WEIGHTS = [
    ("Streetwise (Urban Underworld)", 25),
    ("Urban Stealth & Shadowing", 22),
    ("Urban Observation and Tailing", 20),
    ("Disguise & Impersonation", 17),
    ("Sleight of Hand & Cheating", 14),
    ("Guild Knowledge & Politics", 13),
    ("Black Market Operations", 12),
    ("Criminal Organizations & Syndicates", 11),
    ("City Secrets & Hidden Routes", 10),
    ("Fences and Buyers Network", 9),
    ("Lockpicking and Trap Disarming", 9),
    ("Noble Houses & Court Intrigue", 8),
    ("Forgery of Documents & Seals", 7),
    ("Information Brokerage", 7),
    ("Smuggling Networks", 6),
    ("Poison Lore & Subtle Application", 5),
    ("Heraldry & Lineage Recognition", 4),
    ("Temple Politics & Religious Intrigue", 4),
    ("High Society Manipulation", 3),
]

# Extraction pour compatibilité
URBAN_SKILLS = [skill for skill, weight in URBAN_SKILLS_WITH_WEIGHTS]
URBAN_WEIGHTS = [weight for skill, weight in URBAN_SKILLS_WITH_WEIGHTS]



# =============================================
# BIAIS OUTDOOR PAR RÉGION
# =============================================
region_outdoor_bias: Dict[int, List[str]] = {
    
    # ==================== RÉGIONS 1 À 70 ====================

    # Désert / Aride
    1: ["Desert Water Mastery", "Desert Thermal Endurance", "Open Land Navigation", "Wild Plant Foraging", "Plains Tracking"],
    2: ["Desert Water Mastery", "Desert Thermal Endurance", "Open Land Navigation", "Wild Plant Foraging", "Advanced Tracking"],
    3: ["Desert Water Mastery", "Open Land Navigation", "Plains Tracking", "Wild Plant Foraging", "Weather Reading"],
    12: ["Desert Water Mastery", "Desert Thermal Endurance", "Open Land Navigation", "Advanced Tracking", "Weather Reading"],

    # Côtières / Littorales
    4: ["Coastal Survival", "Littoral Foraging", "Oceanic Navigation", "Storm and Seasickness Mastery", "Dark Water Swimming"],
    5: ["Coastal Survival", "Littoral Foraging", "Oceanic Navigation", "Deep-Sea Fishing", "Storm and Seasickness Mastery"],
    8: ["Coastal Survival", "Littoral Foraging", "Dark Water Swimming", "Oceanic Navigation", "River Crossing"],
    16: ["Coastal Survival", "Littoral Foraging", "Deep-Sea Fishing", "Storm and Seasickness Mastery", "Oceanic Navigation"],
    22: ["Coastal Survival", "Oceanic Navigation", "Dark Water Swimming", "Storm and Seasickness Mastery", "River Crossing"],
    25: ["Coastal Survival", "Littoral Foraging", "Oceanic Navigation", "Deep-Sea Fishing", "Dark Water Swimming"],
    69: ["Coastal Survival", "Oceanic Navigation", "Deep-Sea Fishing", "Storm and Seasickness Mastery", "Dark Water Swimming"],

    # Forestières / Tempérées
    7: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Primitive Fire Mastery", "Shelter Construction"],
    14: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Complex Terrain Navigation", "Hermetic Medicine"],
    26: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Primitive Fire Mastery", "Shelter Construction"],
    27: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Marsh Movement", "Hermetic Medicine"],
    28: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Marsh Movement", "Primitive Fire Mastery"],
    29: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Plains Tracking", "Shelter Construction"],
    35: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Primitive Fire Mastery", "Complex Terrain Navigation"],
    44: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Marsh Movement", "Shelter Construction"],
    46: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Complex Terrain Navigation", "Plains Tracking"],
    52: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Marsh Movement", "Hermetic Medicine"],
    79: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Primitive Fire Mastery", "Shelter Construction"],

    # Montagneuses / Hautes Terres
    10: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Advanced Tracking", "Hermetic Medicine"],
    11: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Advanced Tracking", "Shelter Construction"],
    15: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Extreme Cold Resistance", "Hermetic Medicine"],
    18: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Advanced Tracking", "Primitive Fire Mastery"],
    31: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Extreme Cold Resistance", "Hermetic Medicine"],
    32: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Snow and Ice Shelter Building", "Advanced Tracking"],
    45: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Wild Plant Foraging", "Advanced Tracking"],
    49: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Advanced Tracking", "Hermetic Medicine"],
    51: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Plains Tracking", "Extreme Cold Resistance"],

    # Marécageuses / Humides
    17: ["Marsh Movement", "Marsh Disease Resistance", "Wetland Tracking", "Wild Plant Foraging", "Primitive Fire Mastery"],
    24: ["Marsh Movement", "Marsh Disease Resistance", "Wild Plant Foraging", "Forest Stealth", "Advanced Tracking"],
    60: ["Marsh Movement", "Marsh Disease Resistance", "Wild Plant Foraging", "Advanced Tracking", "Primitive Fire Mastery"],
    64: ["Marsh Movement", "Marsh Disease Resistance", "Wetland Tracking", "Coastal Survival", "Advanced Tracking"],
    65: ["Marsh Movement", "Marsh Disease Resistance", "Forest Stealth", "Advanced Tracking", "Wild Plant Foraging"],
    108: ["Marsh Movement", "Marsh Disease Resistance", "Wild Plant Foraging", "Advanced Tracking", "Hermetic Medicine"],

    # Plaines / Ouvertes
    6: ["Plains Tracking", "Open Land Navigation", "Wild Plant Foraging", "Forced March Endurance", "Weather Reading"],
    29: ["Plains Tracking", "Open Land Navigation", "Wild Plant Foraging", "Advanced Tracking", "Shelter Construction"],
    47: ["Plains Tracking", "Open Land Navigation", "Wild Plant Foraging", "Advanced Tracking", "Forced March Endurance"],
    61: ["Plains Tracking", "Open Land Navigation", "Wild Plant Foraging", "Advanced Tracking", "Weather Reading"],
    62: ["Plains Tracking", "Open Land Navigation", "Desert Water Mastery", "Advanced Tracking", "Forced March Endurance"],

    # Autres régions importantes (1-70)
    13: ["Technical Rock Climbing", "Complex Terrain Navigation", "Mountain Endurance", "Underground Navigation", "Hermetic Medicine"],
    33: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Wild Plant Foraging", "Advanced Tracking"],
    39: ["Underground Navigation", "Confined Space Stealth", "Technical Rock Climbing", "Mountain Endurance", "Hermetic Medicine"],
    48: ["Coastal Survival", "Littoral Foraging", "Oceanic Navigation", "Dark Water Swimming", "Storm and Seasickness Mastery"],
    50: ["Plains Tracking", "Open Land Navigation", "Advanced Tracking", "Forced March Endurance", "Weather Reading"],
    59: ["Wild Plant Foraging", "Marsh Movement", "Marsh Disease Resistance", "Forest Stealth", "Advanced Tracking"],
    66: ["Coastal Survival", "Marsh Movement", "Wild Plant Foraging", "Littoral Foraging", "Advanced Tracking"],
    67: ["Coastal Survival", "Wild Plant Foraging", "Plains Tracking", "Littoral Foraging", "Advanced Tracking"],
    68: ["Forest Stealth", "Wild Plant Foraging", "Complex Terrain Navigation", "Advanced Tracking", "Mountain Endurance"],

    
        # ==================== RÉGIONS 71 À 130 ====================

    # Régions Forestières / Tempérées (suite)
    71: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Primitive Fire Mastery", "Shelter Construction"],
    77: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Marsh Movement", "Hermetic Medicine"],
    78: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Extreme Cold Resistance", "Hermetic Medicine"],
    84: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Forest Stealth", "Advanced Tracking"],
    85: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Marsh Movement", "Hermetic Medicine"],
    91: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Plains Tracking", "Shelter Construction"],
    98: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Marsh Movement", "Primitive Fire Mastery"],
    99: ["Forest Stealth", "Wild Plant Foraging", "Complex Terrain Navigation", "Advanced Tracking", "Mountain Endurance"],
    110: ["Forest Stealth", "Wild Plant Foraging", "Complex Terrain Navigation", "Advanced Tracking", "Hermetic Medicine"],
    111: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Mountain Endurance", "Shelter Construction"],
    112: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Marsh Movement", "Hermetic Medicine"],
    114: ["Mountain Endurance", "Technical Rock Climbing", "Forest Stealth", "Advanced Tracking", "Hermetic Medicine"],
    117: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Forest Stealth", "Advanced Tracking"],
    118: ["Mountain Endurance", "Technical Rock Climbing", "Wild Plant Foraging", "Complex Terrain Navigation", "Advanced Tracking"],
    121: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Plains Tracking", "Shelter Construction"],

    # Régions Montagneuses / Froides
    72: ["Extreme Cold Resistance", "Snow and Ice Shelter Building", "Arctic Hunting", "Mountain Endurance", "Technical Rock Climbing"],
    80: ["Mountain Endurance", "Technical Rock Climbing", "Extreme Cold Resistance", "Snow and Ice Shelter Building", "Complex Terrain Navigation"],
    90: ["Mountain Endurance", "Technical Rock Climbing", "Extreme Cold Resistance", "Snow and Ice Shelter Building", "Advanced Tracking"],
    95: ["Extreme Cold Resistance", "Snow and Ice Shelter Building", "Arctic Hunting", "Mountain Endurance", "Technical Rock Climbing"],
    96: ["Extreme Cold Resistance", "Snow and Ice Shelter Building", "Arctic Hunting", "Plains Tracking", "Mountain Endurance"],
    100: ["Mountain Endurance", "Technical Rock Climbing", "Forest Stealth", "Complex Terrain Navigation", "Hermetic Medicine"],
    101: ["Extreme Cold Resistance", "Arctic Hunting", "Snow and Ice Shelter Building", "Mountain Endurance", "Advanced Tracking"],
    107: ["Mountain Endurance", "Technical Rock Climbing", "Extreme Cold Resistance", "Snow and Ice Shelter Building", "Hermetic Medicine"],
    113: ["Mountain Endurance", "Technical Rock Climbing", "Advanced Tracking", "Plains Tracking", "Forced March Endurance"],
    115: ["Mountain Endurance", "Technical Rock Climbing", "Plains Tracking", "Wild Plant Foraging", "Advanced Tracking"],
    116: ["Mountain Endurance", "Technical Rock Climbing", "Extreme Cold Resistance", "Snow and Ice Shelter Building", "Complex Terrain Navigation"],
    120: ["Mountain Endurance", "Technical Rock Climbing", "Extreme Cold Resistance", "Snow and Ice Shelter Building", "Advanced Tracking"],

    # Régions Côtières / Maritimes
    76: ["Coastal Survival", "Oceanic Navigation", "Deep-Sea Fishing", "Storm and Seasickness Mastery", "Littoral Foraging"],
    83: ["Coastal Survival", "Littoral Foraging", "Oceanic Navigation", "Deep-Sea Fishing", "Storm and Seasickness Mastery"],

    # Régions Marécageuses / Humides
    75: ["Marsh Movement", "Marsh Disease Resistance", "Wetland Tracking", "Wild Plant Foraging", "Advanced Tracking"],
    87: ["Underground Navigation", "Confined Space Stealth", "Technical Rock Climbing", "Advanced Tracking", "Hermetic Medicine"],
    93: ["Underground Navigation", "Confined Space Stealth", "Technical Rock Climbing", "Mountain Endurance", "Extreme Cold Resistance"],
    108: ["Marsh Movement", "Marsh Disease Resistance", "Wild Plant Foraging", "Advanced Tracking", "Hermetic Medicine"],

    # Régions Désertiques / Arides (suite)
    73: ["Desert Water Mastery", "Desert Thermal Endurance", "Open Land Navigation", "Advanced Tracking", "Weather Reading"],
    102: ["Desert Water Mastery", "Desert Thermal Endurance", "Open Land Navigation", "Plains Tracking", "Advanced Tracking"],
    104: ["Mountain Endurance", "Technical Rock Climbing", "Plains Tracking", "Wild Plant Foraging", "Advanced Tracking"],

    # Régions Mixtes / Diverses
    74: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Complex Terrain Navigation", "Shelter Construction"],
    81: ["Coastal Survival", "Oceanic Navigation", "Deep-Sea Fishing", "Storm and Seasickness Mastery", "Dark Water Swimming"],
    82: ["Plains Tracking", "Open Land Navigation", "Wild Plant Foraging", "Forced March Endurance", "Weather Reading"],
    86: ["Forest Stealth", "Advanced Tracking", "Primitive Fire Mastery", "Shelter Construction", "Hermetic Medicine"],
    88: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Advanced Tracking", "Forced March Endurance"],
    89: ["Coastal Survival", "Littoral Foraging", "Dark Water Swimming", "Weather Reading", "Storm and Seasickness Mastery"],
    92: ["Marsh Movement", "Wild Plant Foraging", "Advanced Tracking", "Primitive Fire Mastery", "Hermetic Medicine"],
    94: ["Underground Navigation", "Confined Space Stealth", "Technical Rock Climbing", "Extreme Cold Resistance", "Hermetic Medicine"],
    97: ["Plains Tracking", "Open Land Navigation", "Advanced Tracking", "Forced March Endurance", "Weather Reading"],
    103: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Mountain Endurance", "Complex Terrain Navigation"],
    105: ["Wild Plant Foraging", "Marsh Movement", "Marsh Disease Resistance", "Forest Stealth", "Advanced Tracking"],
    106: ["Coastal Survival", "Oceanic Navigation", "Deep-Sea Fishing", "Littoral Foraging", "Storm and Seasickness Mastery"],
    109: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Advanced Tracking", "Hermetic Medicine"],
    119: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Plains Tracking", "Shelter Construction"],
    122: ["Underground Navigation", "Confined Space Stealth", "Technical Rock Climbing", "Marsh Movement", "Advanced Tracking"],
    123: ["Extreme Cold Resistance", "Snow and Ice Shelter Building", "Arctic Hunting", "Mountain Endurance", "Hermetic Medicine"],
    124: ["Desert Water Mastery", "Desert Thermal Endurance", "Open Land Navigation", "Advanced Tracking", "Weather Reading"],
    125: ["Coastal Survival", "Oceanic Navigation", "Deep-Sea Fishing", "Storm and Seasickness Mastery", "Dark Water Swimming"],
    126: ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking", "Complex Terrain Navigation", "Forced March Endurance"],
    127: ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation", "Extreme Cold Resistance", "Advanced Tracking"],
    128: ["Marsh Movement", "Marsh Disease Resistance", "Wetland Tracking", "Wild Plant Foraging", "Primitive Fire Mastery"],
    129: ["Plains Tracking", "Open Land Navigation", "Wild Plant Foraging", "Weather Reading", "Forced March Endurance"],
    130: ["Technical Rock Climbing", "Mountain Endurance", "Complex Terrain Navigation", "Advanced Tracking", "Hermetic Medicine"],

    # ==================== FALLBACK ====================
    0: ["Wild Plant Foraging", "Advanced Tracking", "Primitive Fire Mastery", "Shelter Construction", 
        "Forest Stealth", "Forced March Endurance", "Weather Reading"]
}



# =============================================
# BIAIS ETHNIE (3 compétences Outdoor favorites)
# =============================================
ethnicity_outdoor_bias: Dict[str, List[str]] = {
    
    # === HUMAINS ===
    "Chondathan": ["Plains Tracking", "Open Land Navigation", "Advanced Tracking"],
    "Tethyrian": ["Forest Stealth", "Wild Plant Foraging", "Advanced Tracking"],
    "Calishite": ["Desert Water Mastery", "Desert Thermal Endurance", "Open Land Navigation"],
    "Damaran": ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation"],
    "Illuskan": ["Oceanic Navigation", "Deep-Sea Fishing", "Storm and Seasickness Mastery"],
    "Mulan": ["Marsh Movement", "Marsh Disease Resistance", "Wild Plant Foraging"],
    "Rashemi": ["Forest Stealth", "Wild Plant Foraging", "Marsh Movement"],
    "Turami": ["Coastal Survival", "Littoral Foraging", "Dark Water Swimming"],
    "Uthgardt": ["Advanced Tracking", "Forest Stealth", "Plains Tracking"],
    "Bedine": ["Desert Water Mastery", "Desert Thermal Endurance", "Open Land Navigation"],
    "Chultan": ["Wild Plant Foraging", "Marsh Movement", "Marsh Disease Resistance"],
    "Shaaran": ["Plains Tracking", "Advanced Tracking", "Open Land Navigation"],
    "Sossrim": ["Arctic Hunting", "Extreme Cold Resistance", "Snow and Ice Shelter Building"],
    "Vaasan": ["Mountain Endurance", "Technical Rock Climbing", "Extreme Cold Resistance"],

    # === ELFES & DEMI-ELFES ===
    "Wood Elf": ["Forest Stealth", "Wild Plant Foraging", "Complex Terrain Navigation"],
    "Wild Elf": ["Forest Stealth", "Advanced Tracking", "Wild Plant Foraging"],
    "Moon Elf": ["Forest Stealth", "Wild Plant Foraging", "Complex Terrain Navigation"],
    "Sun Elf": ["Forest Stealth", "Complex Terrain Navigation", "Mountain Endurance"],
    "Drow": ["Underground Navigation", "Confined Space Stealth", "Technical Rock Climbing"],
    "Sea Elf": ["Coastal Survival", "Oceanic Navigation", "Dark Water Swimming"],
    "Half-Elf": ["Forest Stealth", "Wild Plant Foraging", "Coastal Survival"],
    "Wood Half-elf": ["Forest Stealth", "Wild Plant Foraging", "Complex Terrain Navigation"],
    "Moon Half-elf": ["Forest Stealth", "Wild Plant Foraging", "Complex Terrain Navigation"],
    "Sun Half-elf": ["Forest Stealth", "Complex Terrain Navigation", "Mountain Endurance"],
    "Drow Half-elf": ["Underground Navigation", "Confined Space Stealth", "Technical Rock Climbing"],
    "Sea Half-elf": ["Coastal Survival", "Oceanic Navigation", "Dark Water Swimming"],

    # === NAINS ===
    "Shield Dwarf": ["Mountain Endurance", "Technical Rock Climbing", "Underground Navigation"],
    "Gold Dwarf": ["Mountain Endurance", "Technical Rock Climbing", "Underground Navigation"],
    "Gray Dwarf": ["Underground Navigation", "Confined Space Stealth", "Technical Rock Climbing"],
    "Urdunnir": ["Underground Navigation", "Confined Space Stealth", "Technical Rock Climbing"],

    # === HALFELINS & GNOMES ===
    "Lightfoot Halfling": ["Plains Tracking", "Wild Plant Foraging", "Forest Stealth"],
    "Strongheart Halfling": ["Plains Tracking", "Advanced Tracking", "Wild Plant Foraging"],
    "Ghostwise Halfling": ["Forest Stealth", "Wild Plant Foraging", "Complex Terrain Navigation"],
    "Rock Gnome": ["Underground Navigation", "Technical Rock Climbing", "Mountain Endurance"],
    "Forest Gnome": ["Forest Stealth", "Wild Plant Foraging", "Complex Terrain Navigation"],

    # === AUTRES RACES ===
    "Half-Orc": ["Advanced Tracking", "Mountain Endurance", "Hermetic Medicine"],
    "Orc": ["Advanced Tracking", "Mountain Endurance", "Hermetic Medicine"],
    "Goliath": ["Mountain Endurance", "Technical Rock Climbing", "Complex Terrain Navigation"],
    "Tiefling": ["Underground Navigation", "Confined Space Stealth", "Forest Stealth"],
    "Dragonborn": ["Mountain Endurance", "Technical Rock Climbing", "Underground Navigation"],
    "Firbolg": ["Forest Stealth", "Wild Plant Foraging", "Complex Terrain Navigation"],
    "Kenku": ["Forest Stealth", "Advanced Tracking", "Plains Tracking"],
    "Lizardfolk": ["Marsh Movement", "Marsh Disease Resistance", "Dark Water Swimming"],
    "Aasimar": ["Forest Stealth", "Wild Plant Foraging", "Mountain Endurance"],

    # ==================== GENASI ====================
    "Air Genasi": ["Open Land Navigation", "Complex Terrain Navigation", "Weather Reading"],
    "Earth Genasi": ["Mountain Endurance", "Technical Rock Climbing", "Forced March Endurance"],
    "Fire Genasi": ["Desert Water Mastery", "Desert Thermal Endurance", "Open Land Navigation"],
    "Water Genasi": ["Dark Water Swimming", "Coastal Survival", "Oceanic Navigation"],

    # ==================== HALFLINGS (already defined above, kept for clarity) ====================

    # ==================== AUTRES ETHNIES HUMAINES ====================
    "Nar": ["Forest Stealth", "Advanced Tracking", "Plains Tracking"],
    "Reghedman": ["Arctic Hunting", "Extreme Cold Resistance", "Snow and Ice Shelter Building"],

    # ==================== AUTRES RACES (suite) ====================
    "Triton": ["Dark Water Swimming", "Oceanic Navigation", "Coastal Survival"],
    "Yuan-ti Pureblood": ["Marsh Movement", "Marsh Disease Resistance", "Wild Plant Foraging"],
    "Aarakocra": ["Mountain Endurance", "Complex Terrain Navigation", "Forest Stealth"],
    "Centaur": ["Plains Tracking", "Advanced Tracking", "Open Land Navigation"],
    "Yuan-ti": ["Marsh Movement", "Marsh Disease Resistance", "Wild Plant Foraging"],

    # === ETHNIES SUPPLÉMENTAIRES ===
    "Shou": ["Complex Terrain Navigation", "Mountain Endurance", "Wild Plant Foraging"],
    "Tuigan": ["Plains Tracking", "Advanced Tracking", "Open Land Navigation"],
    "Maztican": ["Forest Stealth", "Wild Plant Foraging", "Marsh Movement"],
    "Netherese": ["Mountain Endurance", "Technical Rock Climbing", "Underground Navigation"],
    "Arkaiun": ["Forest Stealth", "Plains Tracking", "Advanced Tracking"],
    "Durpari": ["Coastal Survival", "Oceanic Navigation", "Dark Water Swimming"],
    "Lantanna": ["Coastal Survival", "Oceanic Navigation", "Deep-Sea Fishing"],
    "Raumviran": ["Extreme Cold Resistance", "Snow and Ice Shelter Building", "Mountain Endurance"],
    "Tashalan": ["Marsh Movement", "Marsh Disease Resistance", "Wild Plant Foraging"],
    "Imaskari": ["Desert Water Mastery", "Underground Navigation", "Technical Rock Climbing"],

    # === FALLBACK ===
    "Default": ["Wild Plant Foraging", "Advanced Tracking", "Forest Stealth"]
}


# =============================================
# FONCTIONS DE COMPTAGE
# =============================================
def get_outdoor_skill_count(settlement_type: str) -> int:
    st = settlement_type.lower()
    
    # Big urban / major settlements (low outdoor)
    big_urban = [
        "metropolis", "major port city", "major trade city",
        "capitale", "grande métropole", "grande ville",
        "underdark city", "dwarven fortress", "elven enclave"
    ]
    # Medium settlements
    medium = [
        "large town", "fortified city", "small town",
        "ville moyenne", "bourg"
    ]
    
    if any(x in st for x in big_urban):
        return random.choices([0, 1, 2, 3], weights=[35, 35, 20, 10])[0]
    elif any(x in st for x in medium):
        return random.choices([1, 2, 3, 4], weights=[25, 35, 25, 15])[0]
    else:
        # Rural, villages, camps, outposts, etc.
        return random.choices([3, 4, 5, 6], weights=[15, 25, 35, 25])[0]


def get_urban_skill_count(settlement_type: str) -> int:
    st = settlement_type.lower()
    
    big_urban = [
        "metropolis", "major port city", "major trade city",
        "capitale", "grande métropole", "grande ville",
        "underdark city", "dwarven fortress", "elven enclave"
    ]
    medium = [
        "large town", "fortified city", "small town",
        "ville moyenne", "bourg"
    ]
    
    if any(x in st for x in big_urban):
        return random.choices([3, 4, 5, 6], weights=[15, 25, 35, 25])[0]
    elif any(x in st for x in medium):
        return random.choices([2, 3, 4], weights=[25, 40, 35])[0]
    else:
        return random.choices([0, 1, 2], weights=[40, 35, 25])[0]


# =============================================
# HELPERS
# =============================================

def _weighted_sample_unique(items, weights, k):
    """Échantillonnage pondéré SANS REMISE (évite les doublons)."""
    items = list(items)
    weights = list(weights)
    selected = []
    for _ in range(min(k, len(items))):
        if not items:
            break
        total = sum(weights)
        if total <= 0:
            idx = random.randrange(len(items))
        else:
            r = random.uniform(0, total)
            cum = 0
            idx = 0
            for i, w in enumerate(weights):
                cum += w
                if r <= cum:
                    idx = i
                    break
        selected.append(items.pop(idx))
        weights.pop(idx)
    return selected


# =============================================
# GÉNÉRATION PRINCIPALE (Version améliorée)
# =============================================
def generate_skills(settlement_type: str, region_id: int = 0, ethnicity: str = None) -> Dict:
    outdoor_count = get_outdoor_skill_count(settlement_type)
    urban_count = get_urban_skill_count(settlement_type)
    
    outdoor_pool: Set[str] = set()
    
    # === PRIORITÉ 1 : Biais ethnique (le plus important) ===
    if ethnicity and ethnicity in ethnicity_outdoor_bias:
        outdoor_pool.update(ethnicity_outdoor_bias[ethnicity])
    
    # === PRIORITÉ 2 : Biais régional ===
    if region_id in region_outdoor_bias:
        outdoor_pool.update(region_outdoor_bias[region_id])
    
    # === PRIORITÉ 3 : Très peu d'aléatoire ===
    random_count = 1
    if len(outdoor_pool) < outdoor_count + random_count:
        needed = outdoor_count + random_count - len(outdoor_pool)
        random_add = random.sample(outdoor_skills_list, needed)
        outdoor_pool.update(random_add)

    outdoor_list = list(outdoor_pool)
    selected_outdoor = random.sample(outdoor_list, min(outdoor_count, len(outdoor_list)))
    
    # ====================== URBAN SKILLS PONDERÉES (SANS DOUBLONS) ======================
    if urban_count > 0:
        selected_urban = _weighted_sample_unique(URBAN_SKILLS, URBAN_WEIGHTS, urban_count)
    else:
        selected_urban = []
    
    # Ceinture + bretelles : dédoublonnage final (au cas où)
    selected_outdoor = list(dict.fromkeys(selected_outdoor))
    selected_urban = list(dict.fromkeys(selected_urban))
    
    all_skills = selected_outdoor + selected_urban
    random.shuffle(all_skills)
    
    return {
        "outdoor_skills": selected_outdoor,
        "urban_skills": selected_urban,
        "all_skills": all_skills,
        "total": len(all_skills),
        "outdoor_count": len(selected_outdoor),
        "urban_count": len(selected_urban)
    }