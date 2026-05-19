import math
import random
from typing import Dict

# ====================== PHYSICAL FORMULAS ======================

def calculate_weight(ws: float) -> float:
    """Poids en kg"""
    return round(68 * math.exp(0.0527 * ws), 1)


def calculate_height(weight_kg: float, build_score: float) -> float:
 
    
    base_height = 41.65 * (weight_kg ** (1/3))
    
    if build_score > 0:
        # Trapu → plus petit
        build_factor = math.exp(-0.0092 * build_score)
    else:
        # Élancé → plus grand
        build_factor = math.exp(-0.0125 * build_score)
    
    # Sécurité : on évite les tailles absurdes
    build_factor = max(0.685, min(1.295, build_factor))
    
    height = base_height * build_factor
    return round(height, 1)


def calculate_size_score(height: float) -> int:
    """Size Score basé sur la taille"""
    return ((height - 170) / 8)


# ====================== SKILL SYSTEM ======================
def calculate_skill_modifier(tcb: float) -> float:
    """Skills Modifier =  -TCB / 4"""
    return math.floor(- tcb / 4)


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


def calculate_melee(weight_score: float, size_score: int, coordination: float, 
                   balance: float, quickness: float) -> float:
    return math.floor(weight_score / 2  + quickness / 4 + 
                     coordination / 5 + balance / 4)


def calculate_fencing(size_score: int, weight_score: float, coordination: float, 
                     quickness: float, balance: float) -> float:
    return math.floor(size_score + weight_score / 4 + quickness / 3 + 
                     coordination / 3 + balance / 5)


# ====================== PROJECTILES (Capacité unique de tir) ======================
def calculate_projectiles(precision: float, coordination: float, quickness: float) -> int:
    """Projectiles - Tir à courte distance
    Precision + Coordination + Quickness"""
    return math.floor(precision + coordination / 3 + quickness / 5)


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


# ====================== MAGIC SYSTEM ======================

def determine_magic_type(combat_points: float) -> dict:
    """Nouveau système de magie (mise à jour Mai 2026)
    Si Combat Points < -2 → le personnage est magiquement actif
    Puis répartition aléatoire : Théurgique 50% | Arcanique 40% | Sauvage 10%"""
    
    if combat_points >= -2:
        return {
            "magic": False,
            "type": "None",
            "subtype": None,
            "description": "Non-magique"
        }
    
    # Magiquement actif
    roll = random.random()
    
    if roll < 0.50:
        return {
            "magic": True,
            "type": "Théurgique",
            "subtype": "Théurgiste",
            "description": "Théurgiste (magie divine instinctive)"
        }
    elif roll < 0.90:        # 0.50 à 0.90 = 40%
        return {
            "magic": True,
            "type": "Arcanique",
            "subtype": "Magicien",
            "description": "Magicien arcanique (étude et formules)"
        }
    else:                    # 10%
        wild_type = random.choice(["Sorcier", "Warlock", "Psionique", "Oracle", "Magie du Sang", "Sorcellerie"])
        return {
            "magic": True,
            "type": "Sauvage",
            "subtype": wild_type,
            "description": f"Magie sauvage - {wild_type}"
        }


# ====================== SECONDARY ATTRIBUTES ======================

def sec_func(x: float) -> float:
    """Points de capacités secondaires (exponentiel)"""
    return round(6 * (math.exp(0.085 * x) - 1), 2)


# ====================== CONSTANTS ======================
MAGIC_THRESHOLD = -1


# ====================== COMMENTAIRES ======================
"""
RÈGLES ACTUELLES - 17 Mai 2026

- Weight Score = floor(12d6/2) - 21 + racial mod
- Build Score  = 6d6 - 21 + racial mod
- Projectiles = floor(Precision + Coordination/3 + Quickness/5)
- Skills Modifier = -TCB / 4
"""