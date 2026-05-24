# utils.py - Character Generation Logic (Version Finale - 24 Mai 2026)

import random
import math
from typing import Tuple

from race_data import ethnicity_data
from ethnicity_weights import category_weights, ethnicity_weights
from origin_data import get_random_origin, region_names      # ← region_names ajouté
from settlement_data import get_random_settlement
from skill_data import generate_active_skills
from rules import (
    calculate_weight,
    calculate_height,
    calculate_size_score,
    calculate_grappling,
    calculate_melee,
    calculate_fencing,
    calculate_projectiles,
    calculate_combat_points,
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
def choose_race_and_ethnicity() -> Tuple[str, str]:
    """Choix pondéré d'une grande catégorie puis d'une ethnie spécifique"""
    
    category = random.choices(
        list(category_weights.keys()),
        weights=list(category_weights.values()),
        k=1
    )[0]

    r_mapping = {
        "Human": "Humain",
        "Dwarf": "Nain",
        "Elf": "Elfe",
        "Half-elf": "Demi-elfe",
        "Halfling": "Halfelin",
        "Gnome": "Gnome",
        "Half-orc": "Demi-orc",
        "Other": "Autre"
    }

    possible_ethnicities = [
        eth for eth, data in ethnicity_data.items()
        if data.get("r") in (category, r_mapping.get(category, category))
    ]

    if not possible_ethnicities:
        print(f"⚠️ Warning: No ethnicity found for category '{category}', using fallback")
        return "Human", "Chondathan"

    weights = [ethnicity_weights.get(eth, 1.0) for eth in possible_ethnicities]
    ethnicity = random.choices(possible_ethnicities, weights=weights, k=1)[0]

    return category, ethnicity


# ====================== MAIN CHARACTER GENERATOR ======================
def generate_character(char_id: str):
    """Génère un personnage complet"""
    
    race, ethnicity = choose_race_and_ethnicity()
    data = ethnicity_data[ethnicity]

    # ====================== ORIGIN & SETTLEMENT ======================
    origin_region = get_random_origin(ethnicity)

    # Recherche de l'ID de région
    region_id = None
    for rid, name in region_names.items():
        if name == origin_region or name in origin_region:
            region_id = rid
            break
    if region_id is None:
        region_id = 0

    # Récupération du type d'implantation
    region_name, settlement_type = get_random_settlement(region_id)

            # ====================== SKILLS ======================
    skills_data = generate_active_skills(
        region_id=region_id,
        ethnicity=ethnicity
    )
    skills = skills_data["skills"]
    bonus_languages = skills_data.get("bonus_languages", [])

    # ====================== ATTRIBUTES (Jet de dés) ======================
    weight_score = math.floor(roll_12d6() / 2) - 21 + data.get("w", 0)
    build_score  = roll_6d6() - 21 + data.get("b", 0)

    balance      = roll_6d6() - 21 + data.get("bal", 0)
    quickness    = roll_6d6() - 21 + data.get("quickness", 0)
    coordination = roll_6d6() - 21 + data.get("coo", 0)
    
    precision_base = (roll_12d6() / 2) - 21
    precision      = math.floor(precision_base + data.get("pre", 0))
    
    endurance    = roll_6d6() - 21 + data.get("end", 0)
    regeneration = roll_6d6() - 21 + data.get("reg", 0)
    vigilance    = roll_6d6() - 21 + data.get("vig", 0)
    beauty       = roll_6d6() - 21 + data.get("bea", 0)

    # ====================== DERIVED ATTRIBUTES ======================
    weight_kg = calculate_weight(weight_score)
    height_cm = calculate_height(weight_kg, build_score)
    size_score = calculate_size_score(height_cm)

    speed = math.floor(quickness + coordination / 3.0)

    climbing = math.floor(
        coordination / 3.0 + balance / 3.0 + 
        build_score / 10.0 + endurance / 6.0 - (weight_score / 9.0)
    )

    dodge = math.floor(
        (vigilance + quickness + coordination + balance - 
         weight_score - (build_score * 0.25)) / 4.0
    )

    stealth = math.floor(- (weight_score / 2) + (balance * 0.8) + (coordination * 0.6))

    # ====================== COMBAT ======================
    grappling   = calculate_grappling(weight_score, build_score, balance, quickness)
    melee       = calculate_melee(weight_score, size_score, quickness, coordination, balance)
    projectiles = calculate_projectiles(precision, coordination, quickness)
    fencing     = calculate_fencing(size_score, weight_score, quickness, coordination, balance)

    base_tcb = calculate_combat_points(grappling, melee, projectiles, fencing)
    racial_cp = data.get("cp", 0.0)
    combat_points = round(base_tcb + racial_cp, 2)

    # ====================== MAGIC ======================
    magic_info = determine_magic_type(combat_points)

    skill_modifier = calculate_skill_modifier(
        tcb=combat_points,
        vigilance=vigilance,
        endurance=endurance,
        regeneration=regeneration,
        stealth=stealth,
        speed=speed,
        dodge=dodge,
        climbing=climbing
    )

    if magic_info.get("magic") is True:
        skill_modifier -= 10

    # ====================== RETURN FINAL ======================
    return {
        "ID": char_id,
        "Indice": data["idx"],
        "Race": race,
        "Ethnicity": ethnicity,
        "Origin_Region": region_name,           # Région propre
        "Settlement_Type": settlement_type,     # ← Type d'implantation

        "Weight_Score": round(weight_score, 1),
        "Build_Score": round(build_score, 1),
        "Height_cm": height_cm,
        "Weight_kg": weight_kg,
        "Size_Score": round(size_score, 2),

        "Balance": round(balance, 1),
        "Quickness": round(quickness, 1),
        "Coordination": round(coordination, 1),
        "Precision": precision,
        "Endurance": round(endurance, 1),
        "Regeneration": round(regeneration, 1),
        "Vigilance": round(vigilance, 1),
        "Beauty": round(beauty, 1),
        "Stealth": stealth,
        "Speed": speed,
        "Dodge": dodge,
        "Climbing": climbing,

        "Grappling": grappling,
        "Melee": melee,
        "Projectiles": projectiles,
        "Fencing": fencing,

        "Combat_Points": combat_points,
        "Magic": "YES" if magic_info.get("magic") else "NO",
        "Magic_Type": magic_info.get("type", "None"),
        "Magic_Subtype": magic_info.get("subtype"),
        "Magic_Description": magic_info.get("description", ""),

        "Skill_Modifier": skill_modifier,
        "Special": data.get("spec", "Aucun"),
        "Skills": skills,
        "Bonus_Languages": bonus_languages,
    }