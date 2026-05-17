import math
import random
from typing import Dict

# ====================== PHYSICAL FORMULAS ======================

def calculate_weight(ws: float) -> float:
    """Poids en kg"""
    return round(68 * math.exp(0.0527 * ws), 1)


def calculate_height(weight_kg: float, build_score: float) -> float:
    """Taille en cm"""
    base_height = 41.65 * (weight_kg ** (1/3))
    build_factor = 1 - 0.0042 * build_score
    return round(base_height * build_factor, 1)


def calculate_size_score(height: float) -> int:
    """Size Score basé sur la taille"""
    return math.floor((height - 170) / 8)


# ====================== COMBAT FORMULAS ======================

def cp(x: float) -> float:
    """Combat Points non linéaire"""
    if x > 1:
        return round(x ** 1.4, 2)
    elif x < 0:
        return round(-((-x) ** 0.7), 2)
    else:
        return round(float(x), 2)


def calculate_grappling(weight_score: float, balance: float, quickness: float) -> float:
    return weight_score + math.floor(balance / 3 + quickness / 5)


def calculate_melee(weight_score: float, size_score: int, quickness: float, 
                   coordination: float, balance: float) -> float:
    return math.floor(weight_score / 2 + size_score / 2 + quickness / 4 + 
                     coordination / 5 + balance / 4)


def calculate_fencing(size_score: int, weight_score: float, quickness: float, 
                     coordination: float, balance: float) -> float:
    return math.floor(size_score + weight_score / 4 + quickness / 3 + 
                     coordination / 3 + balance / 5)


def calculate_projectiles(precision: float) -> float:
    return precision


# ====================== MAGIC SYSTEM ======================

def determine_magic_type(combat_points: float) -> Dict:
    """Détermine le type de magie selon le Total Combat Points"""
    if combat_points >= 0:
        return {
            "magic": False,
            "type": "None",
            "subtype": None,
            "description": "Aucun talent magique"
        }
    elif combat_points >= -5:
        return {
            "magic": True,
            "type": "Theurgist",
            "subtype": "Théurgiste",
            "description": "Théurgiste (magie divine instinctive)"
        }
    elif combat_points >= -12:
        return {
            "magic": True,
            "type": "Mage",
            "subtype": "Magicien",
            "description": "Magicien classique (étude et formules)"
        }
    else:  # -13 et moins
        if random.random() < 0.5:
            return {
                "magic": True,
                "type": "Double",
                "subtype": "Magicien & Théurgiste",
                "description": "Double talent : Magicien + Théurgiste"
            }
        else:
            wild_type = random.choice(["Sorcier", "Warlock", "Psionique", "Oracle", "Magie du Sang"])
            return {
                "magic": True,
                "type": "Wild",
                "subtype": wild_type,
                "description": f"Magie sauvage - {wild_type}"
            }


# ====================== SECONDARY ATTRIBUTES ======================

def sec_func(x: float) -> float:
    """Points de capacités secondaires (exponentiel)"""
    return round(6 * (math.exp(0.085 * x) - 1), 2)


# ====================== COMBAT POINTS TOTAL ======================

def calculate_combat_points(
    grappling: float,
    melee: float,
    projectiles: float,
    fencing: float,
    racial_cp: float = 0.0
) -> float:
    """Total Combat Points"""
    total = (
        cp(grappling) +
        cp(melee) +
        cp(projectiles) +
        cp(fencing) +
        racial_cp
    )
    return round(total, 2)


# ====================== CONSTANTS ======================

MAGIC_THRESHOLD = -1