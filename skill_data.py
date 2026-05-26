# =============================================
# skill_data.py
# =============================================
import random
from typing import Dict, List, Set

# =============================================
# LISTES DES SKILLS
# =============================================

OUTDOOR_SKILLS: List[str] = [
    "Swimming", "Foraging and Herbalism", "Tracking and Hunting", "Forest Stealth",
    "Mountaineering and Portage", "Rock Climbing", "Mountain Navigation", 
    "Desert Survival", "Open Field Orientation", "Swamp Survival",
    "Extreme Cold Resistance", "Snow Shelter Construction", "Arctic Hunting",
    "Underground Navigation", "Underground Stealth", "Maritime Navigation",
    "Deep Sea Fishing", "Coastal Survival", "Plains Tracking",
    "Dense Forest Orientation", "Tropical Disease Resistance",
]

URBAN_SKILLS: List[str] = [
    "Lockpicking and Trap Disarming", "Urban Stealth", "Building Climbing / Parkour",
    "Building Infiltration", "Forgery", "Sleight of Hand", 
    "Urban Observation and Tailing", "Streetwise (Urban Underworld)", 
    "Disguise", "Guild Knowledge", "Criminal Organizations", 
    "Black Market Operations", "City Secrets and Hidden Routes",
    "Noble Houses and Politics", "Fences and Buyers Network",
]

# =============================================
# BIAIS OUTDOOR PAR RÉGION
# =============================================
region_outdoor_bias: Dict[int, List[str]] = {
    # NORD / FROID
    21: ["Arctic Hunting", "Snow Shelter Construction", "Extreme Cold Resistance", "Mountain Navigation", "Rock Climbing", "Underground Navigation"],
    23: ["Arctic Hunting", "Snow Shelter Construction", "Extreme Cold Resistance", "Plains Tracking", "Forest Stealth", "Underground Navigation"],
    37: ["Mountain Navigation", "Rock Climbing", "Extreme Cold Resistance", "Snow Shelter Construction", "Underground Navigation", "Plains Tracking"],
    57: ["Arctic Hunting", "Extreme Cold Resistance", "Snow Shelter Construction", "Mountain Navigation", "Underground Navigation", "Plains Tracking"],
    72: ["Extreme Cold Resistance", "Snow Shelter Construction", "Arctic Hunting", "Mountain Navigation", "Underground Navigation", "Forest Stealth"],
    95: ["Extreme Cold Resistance", "Snow Shelter Construction", "Arctic Hunting", "Mountain Navigation", "Rock Climbing", "Underground Navigation"],
    96: ["Extreme Cold Resistance", "Snow Shelter Construction", "Arctic Hunting", "Mountain Navigation", "Underground Navigation", "Plains Tracking"],

    # FORESTIÈRES
    26: ["Forest Stealth", "Dense Forest Orientation", "Foraging and Herbalism", "Tracking and Hunting", "Underground Navigation", "Mountaineering and Portage"],
    27: ["Forest Stealth", "Dense Forest Orientation", "Foraging and Herbalism", "Tracking and Hunting", "Swamp Survival", "Underground Stealth"],
    28: ["Forest Stealth", "Dense Forest Orientation", "Foraging and Herbalism", "Tracking and Hunting", "Swamp Survival", "Underground Navigation"],
    29: ["Forest Stealth", "Dense Forest Orientation", "Foraging and Herbalism", "Tracking and Hunting", "Swamp Survival", "Plains Tracking"],
    77: ["Forest Stealth", "Dense Forest Orientation", "Foraging and Herbalism", "Tracking and Hunting", "Swamp Survival", "Underground Stealth"],
    85: ["Forest Stealth", "Dense Forest Orientation", "Foraging and Herbalism", "Tracking and Hunting", "Swamp Survival", "Underground Navigation"],
    91: ["Forest Stealth", "Dense Forest Orientation", "Foraging and Herbalism", "Tracking and Hunting", "Swamp Survival", "Plains Tracking"],
    112: ["Forest Stealth", "Dense Forest Orientation", "Foraging and Herbalism", "Tracking and Hunting", "Swamp Survival", "Underground Navigation"],
    121: ["Forest Stealth", "Dense Forest Orientation", "Foraging and Herbalism", "Tracking and Hunting", "Swamp Survival", "Plains Tracking"],

    # MONTAGNEUSES
    10: ["Rock Climbing", "Mountain Navigation", "Mountaineering and Portage", "Underground Navigation", "Underground Stealth", "Extreme Cold Resistance"],
    31: ["Rock Climbing", "Mountain Navigation", "Underground Navigation", "Underground Stealth", "Mountaineering and Portage", "Snow Shelter Construction"],
    32: ["Rock Climbing", "Mountain Navigation", "Underground Navigation", "Underground Stealth", "Mountaineering and Portage", "Snow Shelter Construction"],
    80: ["Rock Climbing", "Mountain Navigation", "Underground Navigation", "Mountaineering and Portage", "Extreme Cold Resistance", "Snow Shelter Construction"],
    90: ["Rock Climbing", "Mountain Navigation", "Underground Navigation", "Mountaineering and Portage", "Extreme Cold Resistance", "Snow Shelter Construction"],
    107: ["Rock Climbing", "Mountain Navigation", "Underground Navigation", "Mountaineering and Portage", "Extreme Cold Resistance", "Snow Shelter Construction"],
    113: ["Rock Climbing", "Mountain Navigation", "Underground Navigation", "Mountaineering and Portage", "Plains Tracking", "Tracking and Hunting"],
    116: ["Rock Climbing", "Mountain Navigation", "Extreme Cold Resistance", "Snow Shelter Construction", "Underground Navigation", "Mountaineering and Portage"],

    # DÉSERTIQUES
    1: ["Desert Survival", "Open Field Orientation", "Plains Tracking", "Foraging and Herbalism", "Coastal Survival", "Swimming"],
    40: ["Desert Survival", "Open Field Orientation", "Plains Tracking", "Foraging and Herbalism", "Underground Navigation", "Underground Stealth"],
    73: ["Desert Survival", "Open Field Orientation", "Plains Tracking", "Foraging and Herbalism", "Underground Navigation", "Tracking and Hunting"],
    83: ["Desert Survival", "Open Field Orientation", "Plains Tracking", "Foraging and Herbalism", "Coastal Survival", "Swimming"],

    # CÔTIÈRES
    4: ["Coastal Survival", "Maritime Navigation", "Deep Sea Fishing", "Swimming", "Swamp Survival", "Urban Stealth"],
    8: ["Coastal Survival", "Maritime Navigation", "Deep Sea Fishing", "Swimming", "Foraging and Herbalism", "Swamp Survival"],
    22: ["Coastal Survival", "Maritime Navigation", "Deep Sea Fishing", "Swimming", "Swamp Survival", "Forest Stealth"],
    54: ["Coastal Survival", "Maritime Navigation", "Deep Sea Fishing", "Swimming", "Urban Stealth", "Building Infiltration"],

    # SOUTERRAINES
    39: ["Underground Navigation", "Underground Stealth", "Rock Climbing", "Swamp Survival", "Extreme Cold Resistance", "Mountain Navigation"],
    87: ["Underground Navigation", "Underground Stealth", "Rock Climbing", "Mountain Navigation", "Swamp Survival", "Tracking and Hunting"],
    93: ["Underground Navigation", "Underground Stealth", "Rock Climbing", "Mountain Navigation", "Extreme Cold Resistance", "Swamp Survival"],
    122: ["Underground Navigation", "Underground Stealth", "Rock Climbing", "Mountain Navigation", "Swamp Survival", "Extreme Cold Resistance"],

    # AUTRES RÉGIONS IMPORTANTES
    5: ["Coastal Survival", "Maritime Navigation", "Urban Stealth", "Building Infiltration", "Swimming", "Streetwise (Urban Underworld)"],
    14: ["Foraging and Herbalism", "Forest Stealth", "Swamp Survival", "Tracking and Hunting", "Dense Forest Orientation", "Underground Navigation"],
    15: ["Mountain Navigation", "Rock Climbing", "Extreme Cold Resistance", "Snow Shelter Construction", "Underground Navigation", "Plains Tracking"],
    16: ["Coastal Survival", "Maritime Navigation", "Swimming", "Urban Stealth", "Building Infiltration", "Deep Sea Fishing"],
    24: ["Foraging and Herbalism", "Swamp Survival", "Tropical Disease Resistance", "Forest Stealth", "Tracking and Hunting", "Coastal Survival"],
    44: ["Forest Stealth", "Foraging and Herbalism", "Coastal Survival", "Swamp Survival", "Tracking and Hunting", "Dense Forest Orientation"],
    46: ["Forest Stealth", "Foraging and Herbalism", "Dense Forest Orientation", "Tracking and Hunting", "Swamp Survival", "Plains Tracking"],
    105: ["Foraging and Herbalism", "Swamp Survival", "Tropical Disease Resistance", "Forest Stealth", "Tracking and Hunting", "Dense Forest Orientation"],

    # Fallback
    0: ["Tracking and Hunting", "Foraging and Herbalism", "Forest Stealth", "Mountain Navigation", "Swimming", "Plains Tracking"]
}

# =============================================
# FONCTION FALLBACK
# =============================================
def get_region_outdoor_bias(region_id: int) -> List[str]:
    """Retourne le biais Outdoor pour une région"""
    return region_outdoor_bias.get(region_id, [
        "Tracking and Hunting", "Foraging and Herbalism", "Forest Stealth",
        "Mountain Navigation", "Swimming", "Plains Tracking"
    ])


# =============================================
# BIAIS ETHNIE (3 compétences Outdoor favorites)
# =============================================
ethnicity_outdoor_bias: Dict[str, List[str]] = {
    # === HUMAINS ===
    "Chondathan": ["Plains Tracking", "Open Field Orientation", "Coastal Survival"],
    "Tethyrian": ["Forest Stealth", "Plains Tracking", "Foraging and Herbalism"],
    "Calishite": ["Desert Survival", "Open Field Orientation", "Plains Tracking"],
    "Damaran": ["Mountain Navigation", "Rock Climbing", "Plains Tracking"],
    "Illuskan": ["Maritime Navigation", "Deep Sea Fishing", "Coastal Survival"],
    "Mulan": ["Swamp Survival", "Foraging and Herbalism", "Underground Navigation"],
    "Rashemi": ["Forest Stealth", "Foraging and Herbalism", "Swamp Survival"],
    "Turami": ["Coastal Survival", "Swimming", "Foraging and Herbalism"],
    "Uthgardt": ["Tracking and Hunting", "Forest Stealth", "Plains Tracking"],
    "Bedine": ["Desert Survival", "Open Field Orientation", "Plains Tracking"],
    "Chultan": ["Foraging and Herbalism", "Swamp Survival", "Tropical Disease Resistance"],
    "Shaaran": ["Plains Tracking", "Tracking and Hunting", "Open Field Orientation"],
    "Sossrim": ["Arctic Hunting", "Extreme Cold Resistance", "Snow Shelter Construction"],
    "Vaasan": ["Mountain Navigation", "Rock Climbing", "Extreme Cold Resistance"],

    # === ELFES & DEMI-ELFES ===
    "Elf Wood": ["Forest Stealth", "Dense Forest Orientation", "Foraging and Herbalism"],
    "Elf Wild": ["Forest Stealth", "Tracking and Hunting", "Dense Forest Orientation"],
    "Elf Moon": ["Forest Stealth", "Dense Forest Orientation", "Foraging and Herbalism"],
    "Elf Sun": ["Forest Stealth", "Dense Forest Orientation", "Mountain Navigation"],
    "Elf Drow": ["Underground Navigation", "Underground Stealth", "Rock Climbing"],
    "Elf Sea": ["Coastal Survival", "Maritime Navigation", "Swimming"],
    "Half-Elf": ["Forest Stealth", "Foraging and Herbalism", "Coastal Survival"],
    "Half-Elf Wood": ["Forest Stealth", "Dense Forest Orientation", "Foraging and Herbalism"],
    "Half-Elf Moon": ["Forest Stealth", "Dense Forest Orientation", "Foraging and Herbalism"],

    # === NAINS ===
    "Shield Dwarf": ["Mountain Navigation", "Rock Climbing", "Underground Navigation"],
    "Gold Dwarf": ["Mountain Navigation", "Rock Climbing", "Underground Navigation"],
    "Gray Dwarf": ["Underground Navigation", "Underground Stealth", "Rock Climbing"],
    "Urdunnir": ["Underground Navigation", "Underground Stealth", "Rock Climbing"],

    # === HALFELINS & GNOMES ===
    "Lightfoot Halfling": ["Plains Tracking", "Foraging and Herbalism", "Forest Stealth"],
    "Strongheart Halfling": ["Plains Tracking", "Foraging and Herbalism", "Tracking and Hunting"],
    "Ghostwise Halfling": ["Forest Stealth", "Foraging and Herbalism", "Dense Forest Orientation"],
    "Rock Gnome": ["Underground Navigation", "Rock Climbing", "Mountain Navigation"],
    "Forest Gnome": ["Forest Stealth", "Foraging and Herbalism", "Dense Forest Orientation"],

    # === AUTRES RACES ===
    "Half-Orc": ["Tracking and Hunting", "Mountain Navigation", "Underground Stealth"],
    "Orc": ["Tracking and Hunting", "Mountain Navigation", "Underground Stealth"],
    "Goliath": ["Mountain Navigation", "Rock Climbing", "Mountaineering and Portage"],
    "Tiefling": ["Underground Navigation", "Urban Stealth", "Forest Stealth"],
    "Dragonborn": ["Mountain Navigation", "Rock Climbing", "Underground Navigation"],
    "Firbolg": ["Forest Stealth", "Foraging and Herbalism", "Dense Forest Orientation"],
    "Kenku": ["Urban Stealth", "Urban Observation and Tailing", "Forest Stealth"],
    "Lizardfolk": ["Swamp Survival", "Swimming", "Tracking and Hunting"],
    "Aasimar": ["Forest Stealth", "Foraging and Herbalism", "Mountain Navigation"],
    "Aarakocra": ["Mountain Navigation", "Dense Forest Orientation", "Forest Stealth"],

    "Shou": ["Dense Forest Orientation", "Mountain Navigation", "Foraging and Herbalism"],
    "Tuigan": ["Plains Tracking", "Tracking and Hunting", "Open Field Orientation"],
    "Maztican": ["Forest Stealth", "Swamp Survival", "Foraging and Herbalism"],
    "Netherese": ["Mountain Navigation", "Underground Navigation", "Rock Climbing"],
    "Arkaiun": ["Forest Stealth", "Plains Tracking", "Tracking and Hunting"],
    "Durpari": ["Coastal Survival", "Swimming", "Maritime Navigation"],
    "Lantanna": ["Coastal Survival", "Swimming", "Deep Sea Fishing"],
    "Raumviran": ["Extreme Cold Resistance", "Mountain Navigation", "Snow Shelter Construction"],
    "Tashalan": ["Swamp Survival", "Tropical Disease Resistance", "Forest Stealth"],
    "Imaskari": ["Desert Survival", "Underground Navigation", "Rock Climbing"],

    # === AUTRES RACES ===
    "Aarakocra": ["Mountain Navigation", "Dense Forest Orientation", "Forest Stealth"],
    "Centaur": ["Plains Tracking", "Tracking and Hunting", "Open Field Orientation"],
    "Yuan-ti": ["Swamp Survival", "Tropical Disease Resistance", "Forest Stealth"],
    "Lizardfolk": ["Swamp Survival", "Swimming", "Tracking and Hunting"],           # déjà présent mais renforcé
    "Firbolg": ["Forest Stealth", "Foraging and Herbalism", "Dense Forest Orientation"], # déjà présent

    # === DEMI-ELFES & VARIANTS ===
    "Half-Elf Sun": ["Forest Stealth", "Dense Forest Orientation", "Mountain Navigation"],
    "Half-Elf Drow": ["Underground Navigation", "Underground Stealth", "Rock Climbing"],
    "Half-Elf Sea": ["Coastal Survival", "Maritime Navigation", "Swimming"],




    # === Fallback ===
    "Default": ["Tracking and Hunting", "Foraging and Herbalism", "Forest Stealth"]
}





# =============================================
# FONCTIONS DE COMPTAGE
# =============================================
def get_outdoor_skill_count(settlement_type: str) -> int:
    st = settlement_type.lower()
    if any(x in st for x in ["métropole", "capitale", "grande ville"]):
        return random.choices([0, 1, 2, 3], weights=[35, 35, 20, 10])[0]
    elif any(x in st for x in ["ville moyenne", "bourg"]):
        return random.choices([1, 2, 3, 4], weights=[25, 35, 25, 15])[0]
    else:
        return random.choices([3, 4, 5, 6], weights=[15, 25, 35, 25])[0]


def get_urban_skill_count(settlement_type: str) -> int:
    st = settlement_type.lower()
    if any(x in st for x in ["métropole", "capitale", "grande ville"]):
        return random.choices([3, 4, 5, 6], weights=[15, 25, 35, 25])[0]
    elif any(x in st for x in ["ville moyenne", "bourg"]):
        return random.choices([2, 3, 4], weights=[25, 40, 35])[0]
    else:
        return random.choices([0, 1, 2], weights=[40, 35, 25])[0]


# =============================================
# GÉNÉRATION PRINCIPALE
# =============================================
def generate_skills(settlement_type: str, region_id: int = 0, ethnicity: str = None) -> Dict:
    outdoor_count = get_outdoor_skill_count(settlement_type)
    urban_count = get_urban_skill_count(settlement_type)
    
    # Outdoor avec biais
    outdoor_pool: Set[str] = set(random.sample(OUTDOOR_SKILLS, min(8, len(OUTDOOR_SKILLS))))
    
    if region_id in region_outdoor_bias:
        outdoor_pool.update(region_outdoor_bias[region_id])
    
    if ethnicity and ethnicity in ethnicity_outdoor_bias:
        outdoor_pool.update(ethnicity_outdoor_bias[ethnicity])
    
    outdoor_list = list(outdoor_pool)
    selected_outdoor = random.sample(outdoor_list, min(outdoor_count, len(outdoor_list)))
    
    # Urban simple
    selected_urban = random.sample(URBAN_SKILLS, min(urban_count, len(URBAN_SKILLS)))
    
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