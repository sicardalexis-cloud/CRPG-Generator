# rules.py - Constantes et formules centrales
import math
import random
from typing import Dict


# ====================== FORMULES DE COMBAT ======================
def cp(x: float) -> float:
    """Combat Points non linéaire"""
    if x > 1:
        return round(x ** 1.4, 2)
    elif x < 0:
        return round(-((-x) ** 0.7), 2)
    else:
        return round(float(x), 2)


def sec_func(x: float) -> float:
    """Points de capacités secondaires (exponentiel)"""
    return round(6 * (math.exp(0.085 * x) - 1), 2)


# ====================== PHYSICAL FORMULAS ======================
def calculate_weight(ws: float) -> float:
    """Poids en kg"""
    return round(68 * math.exp(0.047 * ws), 1)


def calculate_height(ws: float, bs: float) -> float:
    """Taille en cm"""
    size_factor = (ws * 0.72) - (bs / 3 * 0.38)
    return round(170 * (1.0307 ** (size_factor * 0.85)), 1)


def calculate_size_score(height: float) -> int:
    """Size Score basé sur la taille"""
    return math.floor((height - 170) / 8)


# ====================== COMBAT FORMULAS ======================
def calculate_grappling(weight_score: float, balance: float) -> int:
    return round(weight_score + (balance / 3))


def calculate_melee(
    weight_score: float,
    size_score: int,
    coordination: float,
    balance: float
) -> int:
    return math.floor(
        (weight_score / 2) +
        (size_score / 2) +
        (coordination / 6) +
        (balance / 6)
    )


def calculate_fencing(
    size_score: int,
    weight_score: float,
    coordination: float
) -> int:
    return size_score + math.floor(weight_score / 4) + math.floor(coordination / 3)


def calculate_projectiles(precision: float) -> int:
    return round(precision)


# ====================== COMBAT POINTS ======================
def calculate_combat_points(
    grappling: float,
    melee: float,
    projectiles: float,
    fencing: float
) -> float:
    """Total Combat Points (TCB) avec Fencing inclus"""
    return (
        cp(grappling) +
        cp(melee) +
        cp(projectiles) +
        cp(fencing)
    )


# ====================== SYSTÈME DE MAGIE ======================
def determine_magic_type(combat_points: float) -> Dict:
    """
    NOUVEAU SYSTÈME : Plus de Théurgistes
    """
    tcb = round(combat_points, 2)

    if tcb > 0:
        return {
            "magic": False,
            "type": "Non-magique",
            "subtype": None,
            "description": "Aucun talent magique détecté"
        }

    elif tcb >= -7:           # 0 à -7
        return {
            "magic": True,
            "type": "Théurgiste",
            "subtype": "Théurgie",
            "description": "Théurgiste (magie divine / invocation)"
        }

    elif tcb >= -15:          # -8 à -15
        return {
            "magic": True,
            "type": "Magicien",
            "subtype": "Magie savante",
            "description": "Magicien classique (étude et formules)"
        }

    else:                     # -16 et moins
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
                "type": "Sauvage",
                "subtype": wild_type,
                "description": f"Magie sauvage - {wild_type}"
            }


# ====================== CONSTANTS ======================
MAGIC_THRESHOLD = -1   # Conservé pour compatibilité si besoin


# ====================== COMMENTAIRES ======================
"""
RÈGLES ACTUELLES - 13 Mai 2026

Combat Capacities:
- Grappling   = Weight Score + floor(Balance / 3)
- Melee       = floor(WS/2 + Size/2 + Coord/6 + Bal/6)
- Projectiles = Precision
- Fencing     = Size Score + floor(WS/4) + floor(Coord/3)

=== SYSTÈME DE MAGIE ===
Total Combat Points (TCB) = cp(Grap) + cp(Melee) + cp(Proj) + cp(Fencing)

→  0 à -7     : Théurgiste
→ -8 à -15    : Magicien
→ -16 et moins: 50% Double / 50% Magie Sauvage
"""