# utils.py - Character Generation Logic (Version Finale - 26 Mai 2026)

import random
import math
from typing import Tuple

from language_data import generate_languages
from race_data import ethnicity_data
from ethnicity_weights import category_weights, ethnicity_weights
from origin_data import get_random_origin, region_names
from settlement_data import get_random_settlement
from data.equipment.regional_economy import calculate_starting_capital
from data.equipment import regional_adventurer_kits as regional_kits
from data.equipment import post_kit_purchases as post_kit
from data.equipment import armor_sets as armor  # Nouveau système de sets d'armure préconstruits
from data.equipment import remaining_equipment as remaining  # Achats avec capital restant (boucliers + armes + monture)
from skill_data import generate_skills
from knowledge_data import generate_secondary_skills
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


# ====================== BEAUTY CALCULATION ======================
def calculate_beauty(attributes: dict, racial_bea: float = 0) -> int:
    """Beauty calculé à partir des attributs (sans Build_Score ni Weight_Score)"""
    
    base = (
        attributes["coordination"] * 0.28 +
        attributes["balance"] * 0.22 +
        attributes["quickness"] * 0.16 +
        attributes["precision"] * 0.13 +
        attributes["endurance"] * 0.10 +
        attributes["regeneration"] * 0.06 +
        attributes["vigilance"] * 0.05
    )
    
    random_factor = roll_6d6() - 21
    beauty = round(base + random_factor + racial_bea)
    return max(-15, min(38, beauty))


# ====================== RACE & ETHNICITY ======================
def choose_race_and_ethnicity() -> Tuple[str, str]:
    """Choix pondéré d'une grande catégorie puis d'une ethnie spécifique"""
    
    category = random.choices(
        list(category_weights.keys()),
        weights=list(category_weights.values()),
        k=1
    )[0]

    r_mapping = {
        "Human": "Humain", "Dwarf": "Nain", "Elf": "Elfe", "Half-elf": "Demi-elfe",
        "Halfling": "Halfelin", "Gnome": "Gnome", "Half-orc": "Demi-orc", "Other": "Autre"
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
def generate_character(char_id: str = "TEMP"):
    """Génère un personnage complet"""
    
    race, ethnicity = choose_race_and_ethnicity()
    data = ethnicity_data[ethnicity]

    # ====================== ORIGIN & SETTLEMENT ======================
    origin_region = get_random_origin(ethnicity)

    region_id = None
    for rid, name in region_names.items():
        if name == origin_region or name in origin_region:
            region_id = rid
            break
    if region_id is None:
        region_id = 0

    region_name, settlement_type = get_random_settlement(region_id)

    # ====================== STARTING CAPITAL + KIT ÉQUIPEMENT ======================
    # Capital = 1 an de salaire médian local (en bp Rolemaster)
    # NOUVELLE STRATÉGIE :
    # Kit de départ universel identique pour tous les personnages.
    # Le capital de départ (1 an) sert uniquement à compléter l'équipement
    # selon le groupe d'accès au matériel de la région du personnage.
    starting_capital = calculate_starting_capital(
        region_name=region_name,
        settlement_type=settlement_type,
        ethnicity=ethnicity
    )

    # NOUVELLE STRATÉGIE :
    # Tous les personnages reçoivent le même kit de base universel.
    # Le capital de départ sert à compléter le matériel selon le groupe d'équipement.
    kit_items = regional_kits.get_universal_starting_kit()
    kit_cost_bp = sum(item["price_bp"] for item in kit_items)

    # ====================== NOUVEAU : ARMURE PRÉCONSTRUITE (70% du capital) ======================
    # Règle utilisateur (phase actuelle) :
    # - Le kit de base est gratuit.
    # - Jusqu'à 70% du capital de départ peut être dépensé dans l'armure.
    # - On prend **le set le plus cher possible** dans ce budget.
    armor_budget_sp = armor.calculate_armor_budget(starting_capital, percentage=0.70)
    chosen_armor_set = armor.get_most_expensive_affordable_set(armor_budget_sp)

    armor_cost_bp = 0.0
    if chosen_armor_set:
        armor_cost_bp = chosen_armor_set["price_bp"]

    # Capital restant après kit (gratuit) + armure
    remaining_capital_after_armor = starting_capital - armor_cost_bp

    # ====================== SKILLS ======================
    skills_data = generate_skills(
        settlement_type=settlement_type,
        region_id=region_id,
        ethnicity=ethnicity
    )

    secondary = generate_secondary_skills(
        ethnicity=ethnicity,
        region_id=region_id,
        settlement_type=settlement_type,
        active_count=skills_data["total"]
    )

    # Sécurité pour éviter les erreurs si les clés sont mal formées
    if not isinstance(secondary.get("literacy"), list):
        secondary["literacy"] = []
    if not isinstance(secondary.get("spoken_languages"), list):
        secondary["spoken_languages"] = []

    # ====================== ATTRIBUTES ======================
    weight_score = math.floor(roll_12d6() / 2) - 21 + data.get("w", 0)
    build_score  = roll_6d6() - 21 + data.get("b", 0)

    balance      = roll_6d6() - 21 + data.get("bal", 0)
    quickness    = roll_6d6() - 21 + data.get("quickness", 0)
    coordination = roll_6d6() - 21 + data.get("coo", 0)
    precision    = math.floor((roll_12d6() / 2) - 21 + data.get("pre", 0))
    endurance    = roll_6d6() - 21 + data.get("end", 0)
    regeneration = roll_6d6() - 21 + data.get("reg", 0)
    vigilance    = roll_6d6() - 21 + data.get("vig", 0)

    beauty = calculate_beauty({
        "coordination": coordination,
        "balance": balance,
        "quickness": quickness,
        "precision": precision,
        "endurance": endurance,
        "regeneration": regeneration,
        "vigilance": vigilance
    }, data.get("bea", 0))

    # ====================== DERIVED ATTRIBUTES ======================
    weight_kg = calculate_weight(weight_score)
    height_cm = calculate_height(weight_kg, build_score)
    size_score = calculate_size_score(height_cm)

    speed = math.floor(quickness + coordination / 3.0)
    climbing = math.floor(coordination / 3.0 + balance / 3.0 + build_score / 10.0 + endurance / 6.0 - (weight_score / 9.0))
    dodge = math.floor((vigilance + quickness + coordination + balance - weight_score - (build_score * 0.25)) / 4.0)
    stealth = math.floor(- (weight_score / 2) + (balance * 0.8) + (coordination * 0.6))

    # ====================== COMBAT ======================
    grappling   = calculate_grappling(weight_score, build_score, balance, quickness)
    melee       = calculate_melee(weight_score, size_score, quickness, coordination, balance)
    projectiles = calculate_projectiles(precision, coordination, quickness)
    fencing     = calculate_fencing(size_score, weight_score, quickness, coordination, balance)

    base_tcb = calculate_combat_points(grappling, melee, projectiles, fencing)
    combat_points = round(base_tcb + data.get("cp", 0.0), 2)

    # ====================== MAGIC & SKILL MODIFIER ======================
    magic_info = determine_magic_type(combat_points=combat_points, settlement_type=settlement_type)
    
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

    # ====================== CAPITAL (1 an) + ACHATS SUPPLÉMENTAIRES ======================
    # NOUVELLE STRATÉGIE :
    # Le kit de base est universel.
    # Les achats post-kit se font avec le capital, en respectant la liste disponible
    # du groupe d'équipement du personnage (+ surcoûts pour items Rare / Très rare).
    equipment_group = post_kit.get_equipment_group_for_region(region_name)

    # === NOUVELLE PHASE : Achats avec le capital restant (après armure) ===
    # Bouclier + armes (aléatoire, limite encombrement) + monture si possible
    remaining_result = remaining.buy_remaining_equipment(
        remaining_bp=remaining_capital_after_armor
    )

    # Pour compatibilité temporaire, on garde une structure similaire à l'ancien post-kit
    post_purchases = {
        "tier": 1 if remaining_result["purchases"] else 0,
        "tier_name": "Modest" if remaining_result["purchases"] else "None",
        "purchases": remaining_result["purchases"],
        "total_spent_bp": remaining_result["total_spent_bp"],
        "final_remaining_bp": remaining_result["final_remaining_bp"],
    }

    # ====================== RETURN ======================
    return {
        "ID": char_id,
        "Indice": data["idx"],
        "Race": race,
        "Ethnicity": ethnicity,
        "Origin_Region": region_name,
        "Settlement_Type": settlement_type,
        "Equipment_Group": equipment_group,   # Nouveau : groupe d'équipement (14 groupes)

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
        "Beauty": beauty,

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

        "Total_Skills": skills_data["total"],
        "Outdoor_Skills": skills_data["outdoor_skills"],
        "Urban_Skills": skills_data["urban_skills"],
        "Outdoor_Count": skills_data["outdoor_count"],
        "Urban_Count": skills_data["urban_count"],

        "Knowledge": secondary["knowledge"],
        "Craft": secondary["craft"],
        "Literacy": secondary["literacy"],
        "Spoken_Languages": secondary["spoken_languages"],

        "Starting_Capital": starting_capital,
        "Starting_Equipment_Kit": [item["name"] for item in kit_items],
        "Starting_Equipment_Cost_BP": round(kit_cost_bp, 1),
        "Starting_Equipment_Kit_Type": "universal_standard",

        # ====================== NOUVEAU : ARMURE (phase actuelle) ======================
        "Starting_Armor_Set": chosen_armor_set["name"] if chosen_armor_set else "Aucune",
        "Starting_Armor_Cost_BP": round(armor_cost_bp, 1),
        "Starting_Armor_Budget_Percent": 70,   # Règle en vigueur
        "Starting_Capital_After_Armor_BP": round(remaining_capital_after_armor, 1),

        # Note : le kit de base est GRATUIT (fourni par l'origine)
        # Le capital ci-dessous est le capital liquide (1 an de salaire)

        # Achats supplémentaires effectués avec le capital (montures, charettes, armure, etc.)
        # === NOUVEAU : Achats avec capital restant (phase bouclier/armes/monture) ===
        "Remaining_Equipment_Purchases": [p["name"] for p in post_purchases.get("purchases", [])],
        "Remaining_Equipment_Spent_BP": post_purchases.get("total_spent_bp", 0),
        "Final_Pocket_Money_BP": post_purchases.get("final_remaining_bp", remaining_capital_after_armor),
        "Has_Mount_After_Armor": any("rouncey" in p["name"].lower() or "mule" in p["name"].lower() or "pony" in p["name"].lower() or "courser" in p["name"].lower() for p in post_purchases.get("purchases", [])),

        "Special": data.get("spec", "Aucun"),
    }