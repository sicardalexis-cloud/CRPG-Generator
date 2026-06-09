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
# Equipment now: free universal survival kit (0 cost to capital) + one max-affordable from the appropriate 100-kits file.
#   - Default: 100_kits_XV_siecle_Cote_des_Epees_EN (1).txt
#   - Théurgique + Magie Verte (druids): 100_Kits_Druide_Complete_100kits.txt
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
    calculate_skill_modifier,
    choose_god,
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
# LOADER FOR 100 KITS (equipment system)
# =============================================================================

def _get_kit_file_path(magic_type: str = "", magic_subtype: str = "") -> Path:
    """Return the appropriate 100-kits file path.
    - Théurgique + Magie Verte (druids) → 100_Kits_Druide_Complete_100kits.txt
    - Arcanique / Magicien (wizards) → 100_Magician_Kits .txt (user-provided)
    - Default → 100_kits_XV_siecle_Cote_des_Epees_EN (1).txt
    """
    here = Path(__file__).parent
    base = here / "data" / "equipment" / "systeme armure preconstruites"
    mtype = (magic_type or "").lower()
    msub = (magic_subtype or "").lower()

    if mtype == "théurgique" and "verte" in msub:
        druid_file = base / "100_Kits_Druide_Complete_100kits.txt"
        if druid_file.exists():
            return druid_file

    if mtype == "arcanique" or "magicien" in msub:
        magician_file = base / "100_Magician_Kits .txt"
        if magician_file.exists():
            return magician_file

    return base / "100_kits_XV_siecle_Cote_des_Epees_EN (1).txt"


def load_100_kits_file(kit_file: Optional[Path] = None) -> list:
    """Parse the 100 kits file. If kit_file is provided, use it (e.g. druid kits).
    Otherwise falls back to the default XVe kit list.
    Returns list of dicts with price_sp, kit_id, description, items (list of names).
    """
    if kit_file is None:
        here = Path(__file__).parent
        file_path = here / "data" / "equipment" / "systeme armure preconstruites" / "100_kits_XV_siecle_Cote_des_Epees_EN (1).txt"
    else:
        file_path = kit_file
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
                    # Support both "," and " + " as separators (different kit files use different styles)
                    segments = re.split(r'\s*,\s*|\s*\+\s*', items_part)
                    for seg in segments:
                        seg = seg.strip()
                        if not seg:
                            continue
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


# ====================== STARTING MAGIC ITEMS ======================
def _load_starting_magic_items() -> list[dict]:
    """Parse the starting magic items list. Returns [{'name': str, 'price': int}, ...]"""
    from pathlib import Path
    here = Path(__file__).parent
    path = here / "data" / "equipment" / "systeme armure preconstruites" / "magic item markets" / "starting magic items.txt"
    items = []
    if not path.exists():
        print(f"WARNING: starting magic items file not found at {path}")
        return items
    try:
        import re
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("---") or line.startswith("OBJETS"):
                    continue
                if ":" in line:
                    name_part, price_part = line.rsplit(":", 1)
                    name = name_part.strip()
                    m = re.search(r"(\d+)\s*sp", price_part, re.IGNORECASE)
                    if m:
                        price = int(m.group(1))
                        items.append({"name": name, "price": price})
    except Exception as e:
        print(f"ERROR loading starting magic items: {e}")
    return items


def _select_starting_magic_items(budget: int) -> list[dict]:
    """Randomly select items whose total price <= budget (greedy after shuffle)."""
    if budget <= 0:
        return []
    all_items = _load_starting_magic_items()
    if not all_items:
        return []
    affordable = [it for it in all_items if it["price"] <= budget]
    if not affordable:
        return []
    import random
    random.shuffle(affordable)
    selected = []
    remaining = budget
    for item in affordable:
        if item["price"] <= remaining:
            selected.append(item)
            remaining -= item["price"]
    return selected


def _format_magic_and_spells(spells_known: list[str], magic_items: list[dict] = None) -> str:
    """Build the content for the 'Magic_And_Spells' CSV column (only spells now; magic items go to Armes_et_Bouclier column)."""
    if spells_known:
        return " | ".join(spells_known)
    return ""


def _combine_armes_et_bouclier(char: dict) -> str:
    """Combine regular equipment with starting magic items for the CSV 'Armes_et_Bouclier' column."""
    armes = char.get("Armes_et_Bouclier", "Aucun") or "Aucun"
    magic_items = char.get("Starting_Magic_Items", []) or []
    if not magic_items:
        return armes if armes else "Aucun"
    magic_str = " | ".join(magic_items)
    if armes and armes != "Aucun":
        return f"{armes} | {magic_str}"
    return magic_str


# ====================== MAIN CHARACTER GENERATOR ======================
def generate_character(char_id: str = "TEMP", level: int = 1):
    """Génère un personnage complet (capital de départ = pièces d'argent par niveau)"""
    level = max(1, int(level))
    
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

    # God choice (contextual: ethnicity + region + settlement + magic type + subtype)
    # Special rule: Théurgique + Magie Verte → strongly nature gods (Chauntea, Silvanus, etc.)
    god = choose_god(
        ethnicity=ethnicity,
        region_name=region_name,
        settlement_type=settlement_type,
        magic_type=magic_info.get("type", ""),
        magic_subtype=magic_info.get("subtype", "") or ""
    )

    # Wizard (Arcanique/Magicien) starting spells: 6 random level-1 spells weighted by frequency
    from rules import choose_starting_spells
    spells_known: list[str] = choose_starting_spells(
        magic_info.get("type", ""),
        magic_info.get("subtype", "")
    )

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

    # ====================== STARTING CAPITAL (pièces d'argent par niveau de personnage) ======================
    # - Base: ~50 sp par niveau (ajusté par région + settlement via regional_economy).
    # - Free universal survival kit (always given, cost 0 to capital).
    # - Then pick the most expensive affordable 100-kit from the XVe kit list.
    # - Remaining money after kit = Final_Pocket_Money (in BP for now).
    starting_capital = calculate_starting_capital(
        region_name=region_name,
        settlement_type=settlement_type,
        ethnicity=ethnicity,
        level=level
    )

    # ====================== STARTING MAGIC OBJECTS ======================
    # Budget = (900 - starting_capital) / 2   (in sp)
    # Items chosen from the "starting magic items.txt" list, total price <= budget
    magic_budget = max(0, (900 - starting_capital) // 2)
    starting_magic_items = []
    if magic_budget > 0:
        starting_magic_items = _select_starting_magic_items(magic_budget)

    # Free survival kit (always; does not reduce the starting capital)
    kit_items = regional_kits.get_universal_starting_kit()
    kit_cost_bp = sum(item["price_bp"] for item in kit_items)

    # Load and select most expensive 100kit <= full capital
    # Special case: Théurgique + Magie Verte (green magic druids) use the dedicated druid kit list instead of the default one
    kit_file_path = _get_kit_file_path(
        magic_info.get("type", ""),
        magic_info.get("subtype", "")
    )
    kits = load_100_kits_file(kit_file_path)
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
        "God": god,
        "Magic_Description": magic_info.get("description", ""),
        "Spells_Known": spells_known,
        "Num_Spells_Known": len(spells_known),
        "Starting_Magic_Items": [f"{item['name']} ({item['price']} sp)" for item in starting_magic_items],
        "Magic_Item_Budget": magic_budget,
        "Magic_And_Spells": _format_magic_and_spells(spells_known, starting_magic_items),

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

        "Level": level,
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