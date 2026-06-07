# utils.py - Character Generation Logic (Version Finale - 26 Mai 2026)

import random
import math
from typing import Tuple, Optional, List, Dict
import re
from pathlib import Path

from language_data import generate_languages
from race_data import ethnicity_data
from ethnicity_weights import category_weights, ethnicity_weights
from origin_data import get_random_origin, region_names
from settlement_data import get_random_settlement
from data.equipment.regional_economy import calculate_starting_capital
from data.equipment import regional_adventurer_kits as regional_kits
from data.equipment import post_kit_purchases as post_kit
# Note: old armor builder / prebuilts / protocol removed per upgrade.
# Equipment now: free universal survival kit (0 cost to capital) + one max-affordable from 100_kits_XV_siecle_Cote_des_Epees_EN (1).txt
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


# =============================================================================
# LOADER FOR 80 KITS XVe SIECLE (new simple equipment system)
# =============================================================================

def load_100_kits_file() -> list:
    """Parse the 100 kits file (XV siecle Cote des Epees EN). Returns list of dicts with price_sp, kit_id, description, items (list of names)."""
    here = Path(__file__).parent
    file_path = here / "data" / "equipment" / "systeme armure preconstruites" / "100_kits_XV_siecle_Cote_des_Epees_EN (1).txt"
    kits = []
    if not file_path.exists():
        print(f"WARNING: 100 kits file not found at {file_path}")
        return kits
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("=") or " sp - Kit " not in line:
                    continue
                m = re.match(r'^(\d+(?:\.\d+)?)\s*sp\s*-\s*Kit\s*(\d+)\s*-\s*(.*?)\s*:\s*(.*)$', line, re.IGNORECASE)
                if not m:
                    continue
                price = float(m.group(1))
                kit_num = m.group(2)
                desc = m.group(3).strip()
                items_part = m.group(4).strip()
                items = []
                if items_part:
                    for seg in items_part.split(','):
                        seg = seg.strip()
                        # strip ONLY the trailing (price) at the very end (e.g. 'Item (45)' or 'Bolts (12) (9)')
                        # but preserve internal quantity modifiers like 'Bolts (12)' that the user added
                        seg_clean = re.sub(r'\s*\(\d+(?:\.\d+)?\)$', '', seg).strip()
                        if seg_clean:
                            items.append(seg_clean)
                kits.append({
                    "price_sp": price,
                    "kit_id": f"Kit {kit_num}",
                    "description": desc,
                    "items": items
                })
    except Exception as e:
        print(f"ERROR loading 100 kits: {e}")
    return kits


def select_most_expensive_affordable_kit(capital_sp: float, kits: list) -> Optional[dict]:
    """Return the most expensive kit (by price_sp) that fits <= capital_sp, or None."""
    if not kits:
        return None
    affordable = [k for k in kits if k["price_sp"] <= capital_sp + 0.0001]
    if not affordable:
        return None
    return max(affordable, key=lambda k: k["price_sp"])


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

    equipment_group = post_kit.get_equipment_group_for_region(region_name)

    # ====================== ATTRIBUTES (moved up for new equipment protocol using Melee/Projectiles) ======================
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
        climbing=climbing,
    )

    # ====================== STARTING CAPITAL + FREE KIT + 80 XVe KITS (per upgrade) ======================
    # - Free kit (survival stuff + food) from regional_adventurer_kits: UNIVERSAL, always given, cost=0 to capital.
    # - Then select from "100_kits_XV_siecle_Cote_des_Epees_EN (1).txt" the MOST EXPENSIVE kit affordable
    #   with the FULL starting_capital (in sp, 3-year model).
    # - All remaining capital is kept exactly (no 5% bonus, no other spends, no specialty rules, no builder).
    # - Prebuilt_Kit_Cost_Sp + Prebuilt_Kit_Items + Armes_et_Bouclier populated from the chosen kit.
    # - Free kit goes to Starting_Equipment_Kit (value recorded but not deducted from capital).
    # - Columns removed from CSV per request: Starting_Equipment_Cost_BP, Starting_Equipment_Kit_Type,
    #   Armure, Monture_et_Reste, Equipment_Source (info consolidated into Armes_et_Bouclier + Prebuilt_* + Phase*).
    starting_capital = calculate_starting_capital(
        region_name=region_name,
        settlement_type=settlement_type,
        ethnicity=ethnicity
    )

    # Free survival kit (always; does not reduce the starting capital)
    kit_items = regional_kits.get_universal_starting_kit()
    kit_cost_bp = sum(item["price_bp"] for item in kit_items)

    # Load and select most expensive 100kit <= full capital
    kits = load_100_kits_file()
    chosen_kit = select_most_expensive_affordable_kit(starting_capital, kits)

    kit_spent_sp = chosen_kit["price_sp"] if chosen_kit else 0.0
    capital_left = max(0.0, float(starting_capital) - kit_spent_sp)

    # Safe defaults + new 80kit values (used by return dict and formatters)
    prebuilt_kit_info = chosen_kit
    used_prebuilt = bool(chosen_kit)

    chosen_weapon_kit = None
    chosen_armor_set = None
    chosen_mount = None
    weapon_kit_cost_bp = 0.0
    armor_cost_bp = 0.0
    mount_cost_bp = 0.0
    remaining_after_phases = capital_left

    if chosen_kit:
        items = chosen_kit.get("items", [])
        kit_id = chosen_kit.get("kit_id", "Kit")
        desc = chosen_kit.get("description", "")
        kit_label = f"{kit_id} - {desc}"
        full_items_str = ", ".join(items) if items else kit_label

        # Mount detection (saddles etc are bundled in kit price; we surface the animal name for Phase3_Mount / Has_Mount)
        mount_kw = ["Rouncey", "Courser", "Destrier", "Palfrey", "Mule", "Pony"]
        mounts = [it for it in items if any(kw.lower() in it.lower() for kw in mount_kw)]
        monture_name = mounts[0] if mounts else None

        # Armor-ish pieces (for Phase2_Armor_Set summary)
        armor_kw = [
            "aketon", "gambeson", "pourpoint", "padded", "jack", "doublet", "brigandine",
            "coat of plates", "mail", "haubergeon", "haubert", "voiders", "aventail",
            "breastplate", "backplate", "plackart", "cuirass", "plate", "tassets", "fauld",
            "cuisses", "poleyns", "greaves", "sabatons", "gauntlets", "vambraces", "couter",
            "rerebrace", "pauldrons", "gardes", "gorget", "bevor",
            "helmet", "helm", "sallet", "bascinet", "armet", "cerveliere", "nasal", "kettle",
            "great helm", "close helmet", "tournament helmet"
        ]
        armure_parts = [it for it in items if any(kw in it.lower() for kw in armor_kw)]
        armure_str = ", ".join(armure_parts) if armure_parts else "Aucune (kit mixte)"

        # Full kit content for visibility (weapons + armor + any included)
        armes_str = full_items_str

        chosen_weapon_kit = {"name": armes_str}
        chosen_armor_set = {"name": armure_str, "price_sp": kit_spent_sp, "price_bp": round(kit_spent_sp * 10, 1)}
        chosen_mount = {"name": monture_name} if monture_name else None

        weapon_kit_cost_bp = round(kit_spent_sp * 10, 1)
        armor_cost_bp = round(kit_spent_sp * 10, 1)
        mount_cost_bp = 0.0  # cost already inside the single kit price
    else:
        # Capital below cheapest kit (28sp) - very rare with 7yr model
        chosen_weapon_kit = {"name": "Aucun (capital < kit le moins cher)"}
        chosen_armor_set = {"name": "Aucune"}
        chosen_mount = None
        weapon_kit_cost_bp = 0.0
        armor_cost_bp = 0.0
        mount_cost_bp = 0.0

    # No additional phase3 purchases (the 80kit is the complete equipment purchase)
    phase3_purchases = []
    post_purchases = {
        "tier": 0,
        "tier_name": "None",
        "purchases": phase3_purchases,
        "total_spent_bp": 0,
        "final_remaining_bp": int(round(capital_left * 10)),
    }

    remaining_after_phases = capital_left

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

    # (ATTRIBUTES, COMBAT, MAGIC & SKILL MODIFIER moved up early for the new melee/projectile-based equipment protocol)
    # The early block defines melee, projectiles, combat_points, magic_info, skill_modifier etc.

    if magic_info.get("magic") is True:
        skill_modifier -= 10

    # (old equipment protocol + 5% pocket removed; now free kit + single max 80kit selection with exact leftover kept)

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

        # ====================== PHASE MAPPINGS (for compat) ======================
        "Phase1_Weapon_Kit": chosen_weapon_kit["name"] if chosen_weapon_kit else "Aucun",
        "Phase1_Weapon_Kit_Cost_BP": round(weapon_kit_cost_bp, 1),

        "Phase2_Armor_Set": chosen_armor_set["name"] if chosen_armor_set else "Aucune",
        "Phase2_Armor_Cost_BP": round(armor_cost_bp, 1),

        "Phase3_Mount": chosen_mount["name"] if chosen_mount else "Aucune",
        "Phase3_Mount_Cost_BP": round(mount_cost_bp, 1),

        "Remaining_Equipment_Purchases": (chosen_kit["items"] if chosen_kit else []) or [p["name"] for p in post_purchases.get("purchases", [])],
        "Remaining_Equipment_Spent_BP": round(kit_spent_sp * 10, 1) if chosen_kit else post_purchases.get("total_spent_bp", 0),
        "Final_Pocket_Money_BP": post_purchases.get("final_remaining_bp", max(0, int(round(remaining_after_phases * 10)))),
        "Has_Mount": bool(chosen_mount),

        # === 100 kits XV siecle Cote des Epees EN + free survival kit only ===
        "Prebuilt_Kit_Tier": chosen_kit["kit_id"] if chosen_kit else None,
        "Prebuilt_Kit_Cost_Sp": round(kit_spent_sp, 1),
        "Prebuilt_Kit_Items": chosen_kit["items"] if chosen_kit else [],

        # === Main equipment display column ===
        "Armes_et_Bouclier": chosen_weapon_kit["name"] if chosen_weapon_kit else "Aucun",

        # For main.py splitting (free survival + 80kit gear as the "purchased" equipment)
        "Post_Kit_Purchases": chosen_kit["items"] if chosen_kit else [],

        "Special": data.get("spec", "Aucun"),
    }