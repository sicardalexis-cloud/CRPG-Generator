"""
data/equipment/equipment_groups.py

NOUVELLE STRATÉGIE D'ÉQUIPEMENT - Groupes d'Accès au Matériel (14 Groupes)

Ce module implémente le système de groupes proposé par l'utilisateur.
Au lieu de gérer ~30 régions individuellement via des niveaux technologiques,
les régions sont regroupées par similarité d'accès au matériel (technologie + commerce + culture).

Chaque groupe partage une grande partie de son pool d'équipement,
avec seulement 5-15% d'items spécifiques ou culturels par groupe.

NOTE : Depuis fin mai 2026, **tous les 14 groupes** disposent d'une définition
détaillée complète dans un fichier `*_Equipement_Complet.txt`.
"""

from typing import Dict, List, Set

# =============================================================================
# DÉFINITION DES 14 GROUPES D'ÉQUIPEMENT
# =============================================================================

EQUIPMENT_GROUPS: Dict[str, dict] = {
    "Groupe1_Cote_des_Epees": {
        "name": "Bloc Côte des Épées",
        "regions": ["Sword Coast", "Baldur's Gate", "Luskan", "Waterdeep", "Neverwinter"],
        "tech_range": (6, 7),
        "base_tech": 7,
        "has_detailed_list": True,
        "detailed_file": "Groupe1_Cote_des_Epees_Equipement_Complet.txt",
        "high_tech_availability": "Tech 6-7 facilement disponible",
        "firearms_rule": "x3 price + Rare",
        "description": "Hub commercial principal. Meilleur accès global aux armures avancées et armes à poudre.",
        "specialty": "cosmopolite",
    },
    "Groupe2_Sud_Marchand": {
        "name": "Bloc Sud Marchand",
        "regions": ["Amn", "Tethyr", "Turmish", "Sembia", "Calimshan", "Chessenta"],
        "tech_range": (5, 6),
        "base_tech": 5,
        "has_detailed_list": True,
        "detailed_file": "Groupe2_Sud_Marchand_Equipement_Complet.txt",
        "high_tech_availability": "Tech 6 accessible, Tech 7 plus rare",
        "firearms_rule": "x3 price + Rare",
        "description": "Royaumes marchands du sud + empire calishite + Chessenta. Bon accès aux produits du sud (cimeterres, shamshirs, soieries, épices, chameaux).",
        "specialty": "commerce_sud",
    },
    "Groupe3_Coeur_Continental": {
        "name": "Bloc Cœur Continental",
        "regions": ["The Dalelands", "Western Heartlands", "Impiltur"],
        "tech_range": (4, 5),
        "base_tech": 5,
        "has_detailed_list": True,
        "detailed_file": "Groupe3_Coeur_Continental_Equipement_Complet.txt",
        "high_tech_availability": "Tech 6 = Rare, Tech 7 = Très rare",
        "firearms_rule": "x3 price + Très rare",
        "description": "Régions rurales et féodales. Équipement pratique et robuste. Groupe de référence 'standard'.",
        "specialty": "pratique_rural",
    },
    "Groupe4_Vilhon_Est": {
        "name": "Bloc Vilhon / Est Côtier",
        "regions": ["Chondath", "Vilhon Reach", "Moonsea", "Aglarond"],
        "tech_range": (5, 6),
        "base_tech": 5,
        "has_detailed_list": True,
        "detailed_file": "Groupe4_Vilhon_Est_Equipement_Complet.txt",
        "high_tech_availability": "Tech 6 accessible",
        "firearms_rule": "x3 price + Rare",
        "description": "Zone côtière est avec influence maritime et forêt magique.",
        "specialty": "maritime_est",
    },
    "Groupe5_Nord_Sauvage": {
        "name": "Bloc Nord Sauvage",
        "regions": ["Le Nord (The North)", "Vaasa", "Icewind Dale", "Damara"],
        "tech_range": (4, 5),
        "base_tech": 5,
        "has_detailed_list": True,
        "detailed_file": "Groupe5_Nord_Sauvage_Equipement_Complet.txt",
        "high_tech_availability": "Tech 6 = Rare, Tech 7 = Très rare",
        "firearms_rule": "x3 price + Très rare",
        "description": "Frontière sauvage et climat froid + Damara (royaume du nord). Équipement rustique (fourrures, haches, armures légères).",
        "specialty": "rustique_froid",
    },
    "Groupe6_Bloc_Nain": {
        "name": "Bloc Nain",
        "regions": ["Citadel Adbar", "Mithral Hall", "Great Rift"],
        "tech_range": (5, 7),
        "base_tech": 6,
        "has_detailed_list": True,
        "detailed_file": "Groupe6_Bloc_Nain_Equipement_Complet.txt",
        "high_tech_availability": "Excellente qualité même sur tech élevé",
        "firearms_rule": "x3 price + Rare",
        "description": "Citadelles naines. Excellente qualité d'armures lourdes et d'armes.",
        "specialty": "nain_qualite",
    },
    "Groupe7_Marches_Argent": {
        "name": "Bloc Marches d'Argent",
        "regions": ["Silver Marches (Luruar)"],
        "tech_range": (5, 6),
        "base_tech": 5,
        "has_detailed_list": True,
        "detailed_file": "Groupe7_Marches_Argent_Equipement_Complet.txt",
        "high_tech_availability": "Tech 6 accessible",
        "firearms_rule": "x3 price + Rare",
        "description": "Alliance nordique (nains + humains + elfes). Mélange unique.",
        "specialty": "alliance_nordique",
    },
    "Groupe8_Mulhorand": {
        "name": "Bloc Mulhorand",
        "regions": ["Mulhorand"],
        "tech_range": (5, 6),
        "base_tech": 5,
        "has_detailed_list": True,
        "detailed_file": "Groupe8_Mulhorand_Equipement_Complet.txt",
        "high_tech_availability": "Tech 6 accessible",
        "firearms_rule": "x3 price + Rare",
        "description": "Empire à forte influence égyptienne antique. Équipement très culturel.",
        "specialty": "egyptien_antique",
    },
    "Groupe9_Thay": {
        "name": "Bloc Thay",
        "regions": ["Thay"],
        "tech_range": (6, 7),
        "base_tech": 7,
        "has_detailed_list": True,
        "detailed_file": "Groupe9_Thay_Equipement_Complet.txt",
        "high_tech_availability": "Tech 6-7 facilement disponible",
        "firearms_rule": "x3 price + Rare",
        "description": "Empire des Red Wizards. Magie très présente, culture orientale décorative.",
        "specialty": "magie_orientale",
    },
    "Groupe10_Rashemen": {
        "name": "Bloc Rashemen",
        "regions": ["Rashemen"],
        "tech_range": (4, 6),
        "base_tech": 5,
        "has_detailed_list": True,
        "detailed_file": "Groupe10_Rashemen_Equipement_Complet.txt",
        "high_tech_availability": "Tech 6 accessible",
        "firearms_rule": "x3 price + Rare",
        "description": "Culture chamanique et sorcières (Wychlaran). Équipement rustique + magique.",
        "specialty": "chamanique",
    },
    "Groupe11_Moonshae": {
        "name": "Bloc Moonshae Isles",
        "regions": ["Moonshae Isles"],
        "tech_range": (5, 5),
        "base_tech": 5,
        "has_detailed_list": True,
        "detailed_file": "Groupe11_Moonshae_Isles_Equipement_Complet.txt",
        "high_tech_availability": "Tech 6 = Rare",
        "firearms_rule": "x3 price + Rare",
        "description": "Îles celtiques avec fort druidisme. Culture insulaire différente.",
        "specialty": "druidique_celtique",
    },
    "Groupe12_Old_Empires": {
        "name": "Bloc Old Empires",
        "regions": ["Unther", "Old Empires"],
        "tech_range": (5, 6),
        "base_tech": 5,
        "has_detailed_list": True,
        "detailed_file": "Groupe12_Old_Empires_Equipement_Complet.txt",
        "high_tech_availability": "Tech 6 accessible",
        "firearms_rule": "x3 price + Rare",
        "description": "Anciens empires. Culture très ancienne, chars, magie religieuse.",
        "specialty": "ancien_empire",
    },
    "Groupe13_Evermeet": {
        "name": "Bloc Evermeet",
        "regions": ["Evermeet"],
        "tech_range": (6, 8),
        "base_tech": 7,
        "has_detailed_list": True,
        "detailed_file": "Groupe13_Evermeet_Equipement_Complet.txt",
        "high_tech_availability": "Tech 6-8 disponible (haute qualité elfe)",
        "firearms_rule": "x3 price + Rare",
        "description": "Île elfe mythique. Équipement elfe de très haute qualité + forte magie.",
        "specialty": "elfique_pur",
    },
    "Groupe14_Underdark": {
        "name": "Bloc Underdark",
        "regions": ["Underdark"],
        "tech_range": (4, 7),
        "base_tech": 5,
        "has_detailed_list": True,
        "detailed_file": "Groupe14_Underdark_Equipement_Complet.txt",
        "high_tech_availability": "Tech 4-7 variable selon race (drow/duergar/svirfneblin)",
        "firearms_rule": "x3 price + Rare",
        "description": "Réseau souterrain. Cultures drow, duergar, svirfneblin. Matériaux spéciaux.",
        "specialty": "souterrain_exotique",
    },
}


# =============================================================================
# MAPPING RÉGION → GROUPE D'ÉQUIPEMENT
# =============================================================================

REGION_TO_EQUIPMENT_GROUP: Dict[str, str] = {}

for group_id, group_data in EQUIPMENT_GROUPS.items():
    for region in group_data["regions"]:
        REGION_TO_EQUIPMENT_GROUP[region] = group_id


# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def get_equipment_group(region: str) -> str:
    """Retourne l'ID du groupe d'équipement pour une région donnée."""
    return REGION_TO_EQUIPMENT_GROUP.get(region, "Groupe3_Coeur_Continental")  # fallback


def get_group_data(region: str) -> dict:
    """Retourne les données complètes du groupe pour une région."""
    group_id = get_equipment_group(region)
    return EQUIPMENT_GROUPS.get(group_id, EQUIPMENT_GROUPS["Groupe3_Coeur_Continental"])


def get_group_tech_range(region: str) -> tuple:
    """Retourne la fourchette de tech (min, max) pour le groupe de la région."""
    group_data = get_group_data(region)
    return group_data.get("tech_range", (4, 5))


def get_all_groups() -> List[str]:
    """Retourne la liste de tous les IDs de groupes."""
    return list(EQUIPMENT_GROUPS.keys())


def get_regions_in_group(group_id: str) -> List[str]:
    """Retourne la liste des régions appartenant à un groupe."""
    return EQUIPMENT_GROUPS.get(group_id, {}).get("regions", [])


# =============================================================================
# SPÉCIALITÉS CULTURELLES (pour enrichir les listes plus tard)
# =============================================================================

GROUP_SPECIAL_ITEMS: Dict[str, List[str]] = {
    "Groupe8_Mulhorand": [
        "Chariot de guerre mulhorandi",
        "Armure à écailles décorée",
        "Lance de pharaon",
        "Khopesh",
    ],
    "Groupe9_Thay": [
        "Cloak (soie riche)",
        "Turban riche",
        "Vêtements brodés",
        "Baguette de composant (Red Wizard style)",
    ],
    "Groupe13_Evermeet": [
        "Elven Longbow",
        "Elven Steed",
        "Cloak (soie elfe)",
        "Cape elfe brodée",
        "Vêtements de soie elfe",
    ],
    "Groupe14_Underdark": [
        "Armure en adamantine",
        "Arme en adamantine",
        "Pierreries drow",
        "Équipement résistant aux poisons",
    ],
    "Groupe10_Rashemen": [
        "Armure en fourrure renforcée",
        "Hache de sorcière",
        "Amulette chamanique",
    ],
}

# (print silenced; still provides Equipment_Group via get_equipment_group_for_region)