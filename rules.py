import math
import random
from typing import Dict

# ====================== PHYSICAL FORMULAS ======================

def calculate_weight(ws: float) -> float:
    """Poids en kg"""
    return round(71 * math.exp(0.0527 * ws), 1)


def calculate_height(weight_kg: float, build_score: float) -> float:
    """Taille en cm"""
    base_height = 40.9 * (weight_kg ** (1/3))
    build_factor = math.exp(-0.009 * build_score)
    height = base_height * build_factor
    return round(height, 1)


def calculate_size_score(height_cm: float) -> int:
    """Size Score logarithmique : +1 tous les +5% par rapport à 170 cm"""
    if height_cm <= 0:
        return 0
    return round(math.log(height_cm / 170) / math.log(1.05))


# ====================== SKILL SYSTEM ======================
def calculate_skill_modifier(
    tcb: float,
    vigilance: float,
    endurance: float,
    regeneration: float,
    stealth: float,
    speed: float,
    dodge: float,
    climbing: float
) -> int:
    """
    Skill Modifier final :
    - Combat Points forts → gros malus
    - Attributs secondaires positifs → malus supplémentaire (trade-off)
    Ordre d'influence : Vigilance ≈ Stealth > Speed > Dodge ≈ Climbing > Endurance > Regeneration
    """
    # Malus principal lié au combat
    combat_malus = 10-tcb / 4.0
    
    # Malus secondaire (attributs positifs = pénalité aux skills)
    secondary_malus = (
        (vigilance * 0.35) +
        (stealth * 0.35) +
        (speed * 0.25) +
        (dodge * 0.15) +
        (climbing * 0.15) +
        (endurance * 0.10) +
        (regeneration * 0.05)
    )
    
    total = combat_malus - secondary_malus
    return math.floor(total)


# ====================== COMBAT FORMULAS ======================

def cp(x: float) -> float:
    """Combat Points non linéaire"""
    if x > 1:
        return round(x ** 1.4, 2)
    elif x < 0:
        return round(-((-x) ** 0.7), 2)
    else:
        return round(float(x), 2)


def calculate_grappling(weight_score: float, build_score: float, balance: float, quickness: float) -> float:
    """Grappling - Simulation réaliste (poids très impactant)"""
    return math.floor(
        weight_score  +      # Poids = facteur dominant (comme demandé)
        build_score * 0.1 +          # Être trapu = gros avantage
        balance /3 +              # Équilibre et contrôle postural
        quickness /4               # Explosivité et réactivité
    )



def calculate_melee(weight_score: float, size_score: int, coordination: float, 
                   balance: float, quickness: float) -> float:
    """Melee - Variance augmentée pour se rapprocher de Grappling"""
    return math.floor(
        weight_score / 2.0 +           # Force brute (base solide)
        quickness / 3 +              # Vitesse d'exécution
        coordination / 4 +           # Technique et précision
        balance / 5.0 +                # Stabilité et puissance des coups
        size_score * 0              # Allonge (bonus notable)
    )


def calculate_fencing(size_score: int, weight_score: float, coordination: float, 
                     quickness: float, balance: float) -> float:
    """Fencing - Taille plus importante + bonne variance"""
    return math.floor(
        size_score * 1 +           # ← Augmenté (allonge = très gros avantage)
        coordination / 3 +          # Technique innée
        quickness / 5 +             # Vitesse
        balance / 4 +               # Footwork
        weight_score *0            # Puissance brute (faible)
    )


def calculate_projectiles(precision: float, coordination: float, quickness: float) -> int:
    return math.floor(precision + coordination / 3 + quickness / 5)


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
MAGIC_THRESHOLD = -0      # 50% des personnages sont magiques
ARCANIST_THRESHOLD = -7  # 20% des personnages les plus faibles sont Arcanistes


def determine_magic_type(combat_points: float) -> dict:
    """Système de magie calibré :
    - 20% Arcanistes (les plus faibles)
    - 30% Théurgistes
    - 50% Non-magiques"""
    
    if combat_points > MAGIC_THRESHOLD:
        return {
            "magic": False,
            "type": "None",
            "subtype": None,
            "description": "Non-magique"
        }
    
    if combat_points <= ARCANIST_THRESHOLD:
        return {
            "magic": True,
            "type": "Arcanique",
            "subtype": "Magicien",
            "description": "Arcaniste (magie savante)"
        }
    else:
        return {
            "magic": True,
            "type": "Théurgique",
            "subtype": "Théurgiste",
            "description": "Théurgiste (magie divine instinctive)"
        }


# ====================== SECONDARY ATTRIBUTES ======================
def sec_func(x: float) -> float:
    """Points de capacités secondaires (exponentiel)"""
    return round(6 * (math.exp(0.085 * x) - 1), 2)


# ====================== COMMENTAIRES ======================
"""
RÈGLES ACTUELLES

- MAGIC_THRESHOLD     = -0.6   → 50% magiques
- ARCANIST_THRESHOLD  = -7.17  → 20% Arcanistes
- Skill Modifier      = combat_malus + secondary_malus (tous positifs = malus)
"""