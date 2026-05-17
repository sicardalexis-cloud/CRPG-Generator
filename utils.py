# utils.py - Character Generation Logic
import random
import math
from typing import Dict

from race_data import ethnicity_data
from ethnicity_weights import category_weights, ethnicity_weights
from rules import (
    calculate_weight,
    calculate_height,
    calculate_size_score,
    calculate_grappling,
    calculate_melee,
    calculate_fencing,
    calculate_projectiles,
    calculate_combat_points,
    sec_func,
    determine_magic_type,
    calculate_skill_modifier
)


# ====================== DICE ROLLS ======================
def roll_4d6() -> int:
    return sum(random.randint(1, 6) for _ in range(4))


def roll_6d6() -> int:
    return sum(random.randint(1, 6) for _ in range(6))


def roll_12d6() -> int:
    return sum(random.randint(1, 6) for _ in range(12))


# ====================== RACE & ETHNICITY ======================
def choose_race_and_ethnicity():
    """Choix pondéré d'une catégorie puis d'une ethnie"""
    category = random.choices(
        list(category_weights.keys()),
        weights=list(category_weights.values()),
        k=1
    )[0]

    possible_ethnicities = [
        eth for eth, data in ethnicity_data.items() 
        if data.get("r") == category
    ]

    weights = [ethnicity_weights.get(eth, 1) for eth in possible_ethnicities]
    ethnicity = random.choices(possible_ethnicities, weights=weights, k=1)[0]

    return category, ethnicity


# ====================== MAIN GENERATOR ======================
def generate_character(char_id: str):
    # ====================== RACE ======================
    race, ethnicity = choose_race_and_ethnicity()
    data = ethnicity_data[ethnicity]

    # ====================== ATTRIBUTES ======================
    weight_score = math.floor(roll_12d6() / 2) - 21 + data.get("w", 0)
    build_score  = roll_6d6() - 21 + data.get("b", 0)

    weight_kg = calculate_weight(weight_score)
    height    = calculate_height(weight_kg, build_score)
    size_score = calculate_size_score(height)

    # Autres attributs
    balance      = roll_6d6() - 21 + data.get("bal", 0)
    quickness    = roll_6d6() - 21 + data.get("spd", 0)      # ← "spd" et non "qui"
    coordination = roll_6d6() - 21 + data.get("coo", 0)
    precision    = roll_6d6() - 21 + data.get("pre", 0)
    endurance    = roll_6d6() - 21 + data.get("end", 0)
    regeneration = roll_6d6() - 21 + data.get("reg", 0)
    vigilance    = roll_6d6() - 21 + data.get("vig", 0)
    beauty       = roll_6d6() - 21 + data.get("bea", 0)

    # Stealth
    stealth = math.floor(- (weight_score / 2) + (balance * 0.8) + (coordination * 0.6))

    # ====================== COMBAT CAPACITIES ======================
    grappling   = calculate_grappling(weight_score, balance, quickness)
    melee       = calculate_melee(weight_score, size_score, quickness, coordination, balance)
    projectiles = calculate_projectiles(precision)
    fencing     = calculate_fencing(size_score, weight_score, quickness, coordination, balance)

    # ====================== TOTAL COMBAT POINTS ======================
    base_tcb = calculate_combat_points(grappling, melee, projectiles, fencing)
    racial_bonus = data.get("cp", 0.0)
    combat_points = round(base_tcb + racial_bonus, 2)

    # ====================== MAGIC ======================
    magic_info = determine_magic_type(combat_points)

    # ====================== SECONDARY CAPACITIES ======================
    sec_total = (
        sec_func(stealth) +
        sec_func(quickness) +
        sec_func(endurance) +
        sec_func(regeneration) +
        sec_func(vigilance) +
        sec_func(beauty)
    )

    # ====================== SKILLS ======================
    base = 0 if magic_info["magic"] else 70
    skill_points = base - combat_points - sec_total
    
    skill_modifier = calculate_skill_modifier(combat_points)
    skill_bonus = round(skill_modifier + (math.log(max(skill_points / 6 + 1, 1)) / 0.085), 3)

    # ====================== RETURN ======================
    return {
        "ID": char_id,
        "Indice": data["idx"],
        "Race": race,
        "Ethnicity": ethnicity,

        "Weight_Score": round(weight_score, 1),
        "Build_Score": round(build_score, 1),
        "Height_cm": height,
        "Weight_kg": weight_kg,
        "Size_Score": size_score,

        "Balance": round(balance, 1),
        "Quickness": round(quickness, 1),
        "Coordination": round(coordination, 1),
        "Precision": round(precision, 1),
        "Endurance": round(endurance, 1),

        "Regeneration": round(regeneration, 1),
        "Vigilance": round(vigilance, 1),
        "Beauty": round(beauty, 1),
        "Stealth": stealth,

        "Grappling": grappling,
        "Melee": melee,
        "Projectiles": projectiles,
        "Fencing": fencing,

        "Combat_Points": combat_points,
        "Magic": "YES" if magic_info["magic"] else "NO",
        "Magic_Type": magic_info["type"],
        "Magic_Subtype": magic_info.get("subtype"),
        "Magic_Description": magic_info["description"],

        "Skill_Points": round(skill_points, 1),
        "Skill_Modifier": skill_modifier,
        "Skill_Bonus": skill_bonus,
        "Special": data.get("spec", "None")
    }