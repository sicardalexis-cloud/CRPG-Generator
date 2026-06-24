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
# Equipment now: free universal survival kit (0 cost to capital) + one (smartly chosen) affordable 100-kit.
# Kit file selection:
#   - Default: 100_kits_XV_siecle_Cote_des_Epees_EN (1).txt   ← (you just updated this one)
#   - Théurgique + Magie Verte (druids): 100_Kits_Druide_Complete_100kits.txt
#   - Arcanique / Magicien: 100_Magician_Kits .txt
#
# Smart selection rules (applied after loading the appropriate kit list):
#   - If (Projectiles - Melee) > 3 → prioritize the most expensive affordable kit that contains a projectile weapon.
#   - If (Melee - Projectiles) > 3 → prioritize the most expensive affordable kit that is melee/close-combat oriented
#     (melee weapons + armor, no ranged weapons).
#   - Otherwise → most expensive affordable kit overall.
#
# The chosen kit file name is recorded in "Prebuilt_Kit_Source" (visible in CSV exports).
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
    calculate_reach,
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


def _kit_has_projectile_weapon(kit: dict) -> bool:
    """Check if a kit contains at least one projectile/ranged weapon (bow, crossbow, sling, etc.)."""
    if not kit or not kit.get("items"):
        return False
    items_lower = [it.lower() for it in kit["items"]]
    projectile_keywords = [
        "bow", "longbow", "short bow", "crossbow", "light crossbow",
        "sling", "sling bullet", "arrows", "crossbow bolts",
        "dart", "javelin", "sling staff",
    ]
    return any(
        any(kw in item for kw in projectile_keywords)
        for item in items_lower
    )


def _kit_is_melee_oriented(kit: dict) -> bool:
    """Return True if the kit is focused on close combat (melee weapons + armor, no projectile weapons)."""
    if not kit or not kit.get("items"):
        return False
    items_lower = [it.lower() for it in kit["items"]]
    melee_keywords = [
        "sword", "arming sword", "broadsword", "falchion", "messer",
        "axe", "hand axe", "francisca", "poleaxe", "halberd", "bill", "glaive", "military fork",
        "mace", "hammer", "war hammer", "lucerne hammer",
        "spear", "pike", "quarterstaff",
        "shield", "buckler", "targe", "great targe", "heater shield", "kite shield",
        "armor", "brigandine", "plate", "mail", "gambeson", "jack", "doublet", "aketon",
        "club", "staff",
    ]
    has_melee = any(any(kw in item for kw in melee_keywords) for item in items_lower)
    has_ranged = _kit_has_projectile_weapon(kit)
    return has_melee and not has_ranged


def _is_magic_light_projectile(name: str) -> bool:
    """True only for the individual per-piece magic light projectiles (Arrows +x etc.).
    The generic 'Ammunition +1 (10x)' packs are NOT filtered by this logic.
    """
    n = name.lower()
    return any(prefix in n for prefix in ("arrows +", "crossbow bolts +", "sling bullets +", "javelins +", "darts +"))


def _get_ranged_ammo_types(kit: dict) -> set[str]:
    """Return which specific ammo categories this kit supports.
    Used to decide 'the right magic ammunitions' when the character has ranged weapons.
    Avoids false positives like 'crossbow' containing 'bow'.
    """
    if not kit or not kit.get("items"):
        return set()
    text = " ".join(kit.get("items", [])).lower()
    types = set()

    # Crossbow first (more specific) to avoid "bow" substring match
    if any(kw in text for kw in ("crossbow", "crossbow bolts")):
        types.add("crossbow_bolts")

    # Bows: explicit long/short bow or "bow" that is not part of crossbow
    if any(kw in text for kw in ("longbow", "short bow", " shortbow", "arrows")) or \
       ("bow" in text and "crossbow" not in text):
        types.add("arrows")

    if "sling" in text:
        types.add("sling_bullets")
    if "javelin" in text:
        types.add("javelins")
    if "dart" in text:
        types.add("darts")
    return types


def _is_magic_item_allowed_for_kit(item: dict, kit: dict | None) -> bool:
    """Apply the rule:
    - If the character/kit has NO ranged weapons → only magic sling bullets, darts or javelins.
    - If the character HAS a ranged weapon → only the matching ("right") magic ammunition types.
    Non light-projectile magic items (potions, wands, generic packs, etc.) are always allowed.
    """
    name = item.get("name", "")
    if not _is_magic_light_projectile(name):
        return True

    if not kit:
        # Extreme low-capital case (no kit purchased): conservative, only standalone usable
        n = name.lower()
        return any(x in n for x in ("sling bullets", "darts", "javelins"))

    has_ranged_weapon = _kit_has_projectile_weapon(kit)
    n = name.lower()

    if not has_ranged_weapon:
        # No ranged weapon in the kit → restrict to sling bullets / darts / javelins
        return any(x in n for x in ("sling bullets", "darts", "javelins"))

    # Has at least one ranged weapon → only the right ammo for what is present.
    ranged_types = _get_ranged_ammo_types(kit)

    if "arrows +" in n:
        return "arrows" in ranged_types
    if "crossbow bolts +" in n:
        return "crossbow_bolts" in ranged_types
    if "sling bullets +" in n:
        return "sling_bullets" in ranged_types
    if "javelins +" in n:
        # Thrown javelins are flexible even for other ranged-focused characters
        return True
    if "darts +" in n:
        return True

    return True


# ====================== STARTING MAGIC ITEMS ======================

# Magic item budget for starting characters
# Formula: max(0, (MAGIC_BUDGET_PIVOT - starting_capital) // 2)
MAGIC_BUDGET_PIVOT = 1800
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


def _select_starting_magic_items(budget: int, kit: dict | None = None) -> list[dict]:
    """
    Selection of starting magic items by repeatedly picking from the 10 most expensive
    affordable items.

    Algorithm:
    1. Budget = max(0, (MAGIC_BUDGET_PIVOT - starting_capital) // 2)
       (MAGIC_BUDGET_PIVOT = 1800)
    2. Filter items affordable with current budget.
    3. If a kit is provided, apply kit-aware filtering for magic projectiles.
    4. While budget remains and items can still be afforded:
         - Identify all items that fit in the *current remaining* budget.
         - Sort them by price (most expensive first).
         - Take the top 10 (or fewer if less than 10 fit).
         - Randomly pick *one* from these top 10.
         - If it still fits (it should), add it and subtract its price.
         - Remove the chosen item from the pool.
    5. Stop when no more items can be purchased with remaining budget.

    This produces fewer but generally higher-value / more expensive magic items
    compared to the previous weighted-random approach.
    """
    if budget <= 0:
        return []
    all_items = _load_starting_magic_items()
    if not all_items:
        return []
    affordable = [it for it in all_items if it["price"] <= budget]
    if kit is not None:
        affordable = [it for it in affordable if _is_magic_item_allowed_for_kit(it, kit)]
    if not affordable:
        return []

    import random
    selected = []
    remaining = budget

    while True:
        # Items we can currently afford with remaining budget
        can_afford = [it for it in affordable if it["price"] <= remaining]
        if not can_afford:
            break

        # Sort by descending price and take the 10 most expensive
        can_afford_sorted = sorted(can_afford, key=lambda x: x["price"], reverse=True)
        top_10 = can_afford_sorted[:10]

        # Pick one at random from the top 10
        chosen = random.choice(top_10)

        if chosen["price"] <= remaining:
            selected.append(chosen)
            remaining -= chosen["price"]

        # Remove from pool so we don't consider it again
        affordable.remove(chosen)

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
    weight_score = roll_6d6() - 21 + data.get("w", 0)
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
    reach       = int(round(calculate_reach(size_score)))
    grappling   = calculate_grappling(weight_score, build_score, balance, quickness)
    melee       = calculate_melee(weight_score, size_score, coordination, balance, quickness)
    projectiles = calculate_projectiles(precision, coordination, quickness)
    fencing     = calculate_fencing(quickness, coordination, balance, size_score)

    base_tcb = calculate_combat_points(grappling, melee, projectiles, fencing)
    combat_points = round(base_tcb + data.get("cp", 0.0), 2)

    # ====================== MAGIC & SKILL MODIFIER ======================
    magic_info = determine_magic_type(combat_points=combat_points, settlement_type=settlement_type)

    # English display versions for pure-English character sheets (fiches)
    _magic_type_map = {
        "Théurgique": "Theurgic",
        "Arcanique": "Arcane",
        "Sauvage": "Wild",
        "None": "None",
    }
    _magic_subtype_map = {
        "Magicien": "Wizard",
        "Magie Blanche": "White Magic",
        "Magie Verte": "Green Magic",
        "Magie Rouge": "Red Magic",
        "Magie Bleue": "Blue Magic",
        "Magie Noire": "Black Magic",
    }
    _magic_desc_map = {
        ("Théurgique", "Magie Blanche"): "White Magic (healing, protection, divine light)",
        ("Théurgique", "Magie Verte"): "Green Magic (nature, growth, forest spirits) — Druidic",
        ("Arcanique", "Magicien"): "Arcane Wizard (study, formulas, ancient knowledge)",
        ("Sauvage", "Magie Blanche"): "Wild Magic - White (pure chaos, unpredictable raw energy)",
        ("Sauvage", "Magie Rouge"): "Wild Magic - Red (fire, destruction, passion, rage)",
        ("Sauvage", "Magie Verte"): "Wild Magic - Green (wild nature, primal life, uncontrolled growth)",
        ("Sauvage", "Magie Bleue"): "Wild Magic - Blue (water, illusions, hidden knowledge, cold)",
        ("Sauvage", "Magie Noire"): "Wild Magic - Black (necromancy, shadow, corruption, dark power)",
    }

    mtype_raw = magic_info.get("type", "None") or "None"
    msubtype_raw = magic_info.get("subtype") or ""

    magic_type_eng = _magic_type_map.get(mtype_raw, mtype_raw)
    magic_subtype_eng = _magic_subtype_map.get(msubtype_raw, msubtype_raw)

    # Special case for green theurgic (druid flavor)
    if mtype_raw == "Théurgique" and msubtype_raw == "Magie Verte":
        magic_subtype_eng = "Druid"

    magic_desc_eng = _magic_desc_map.get((mtype_raw, msubtype_raw), magic_info.get("description", ""))

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
    # - Base: ~250 sp par niveau (5 ans de salaire local, ajusté par région + settlement). [doublé]
    # - Free universal survival kit (always given, cost 0 to capital).
    # - Smart kit selection:
    #     * If Projectiles > Melee + 3 → prioritize kit with projectile weapon.
    #     * If Melee > Projectiles + 3 → prioritize melee/close-combat oriented kit (armor + melee weapons).
    #     * Otherwise → most expensive affordable kit.
    # - Remaining money after kit = Final_Pocket_Money (in BP for now).
    starting_capital = calculate_starting_capital(
        region_name=region_name,
        settlement_type=settlement_type,
        ethnicity=ethnicity,
        level=level
    )

    # ====================== STARTING MAGIC OBJECTS ======================
    # Budget for starting magic items = max(0, (MAGIC_BUDGET_PIVOT - starting_capital) // 2) sp
    # (Pivot à 1800 pour compenser le capital doublé à 5 ans de salaire)
    #
    # Selection protocol (see _select_starting_magic_items for the code):
    #   1. Compute budget from (MAGIC_BUDGET_PIVOT - capital) / 2
    #   2. Keep only items whose price <= budget ("affordable" pool)
    #   3. Repeatedly:
    #        - Among items that fit in the *current remaining* budget,
    #          take the 10 most expensive (or all if fewer than 10).
    #        - Randomly select one of them.
    #        - Buy it if possible and subtract its price.
    #        - Remove it from consideration.
    #   4. Stop when no more items can be afforded.
    #
    # This tends to produce fewer but more expensive / higher-impact
    # magic items rather than many cheap ones.
    #
    # The selected items are stored in:
    #   - character["Starting_Magic_Items"]   (list of formatted strings)
    #   - character["Magic_Item_Budget"]
    # They are appended to the "Armes_et_Bouclier" column in the CSV
    # (not in "Magic_And_Spells" anymore, per your earlier request).
    #
    # IMPORTANT: actual selection (with kit-aware filtering of magic projectiles)
    # is performed AFTER kit choice, so we know what ranged weapons (if any) the
    # character has. See the block after kit processing + _is_magic_item_allowed_for_kit.
    magic_budget = max(0, (MAGIC_BUDGET_PIVOT - starting_capital) // 2)
    starting_magic_items: list[dict] = []   # filled after kit selection below

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

    # New rule: if the character is significantly better with projectiles than melee,
    # prioritize kits that include a projectile weapon (bow, crossbow, sling...).
    affordable = [k for k in kits if k["price_sp"] <= starting_capital + 0.0001]
    if not affordable:
        chosen_kit = None
    else:
        ranged_biased = (projectiles - melee) > 3
        melee_biased = (melee - projectiles) > 3
        if ranged_biased:
            ranged_kits = [k for k in affordable if _kit_has_projectile_weapon(k)]
            if ranged_kits:
                chosen_kit = max(ranged_kits, key=lambda k: k["price_sp"])
            else:
                chosen_kit = max(affordable, key=lambda k: k["price_sp"])
        elif melee_biased:
            # Prefer close-combat / melee-oriented kits when the character is significantly better in melee
            melee_kits = [k for k in affordable if _kit_is_melee_oriented(k)]
            if melee_kits:
                chosen_kit = max(melee_kits, key=lambda k: k["price_sp"])
            else:
                chosen_kit = max(affordable, key=lambda k: k["price_sp"])
        else:
            chosen_kit = max(affordable, key=lambda k: k["price_sp"])

    # Record which kit list was actually used (useful when maintaining several kit files)
    if chosen_kit is not None:
        chosen_kit["source_file"] = kit_file_path.name if kit_file_path else "unknown"

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
        # Capital below cheapest kit (very low capital case)
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

    # ====================== STARTING MAGIC ITEMS (after kit: kit-aware ammo filtering) ======================
    # Now that we know the final chosen_kit (and thus whether it contains bows, crossbows,
    # slings, javelins, darts etc.), we can select magic items while respecting the rule:
    # - No ranged weapons in kit → only magic sling bullets / darts / javelins.
    # - Has ranged weapon → only the correct matching magic ammunition.
    starting_magic_items = []
    if magic_budget > 0:
        starting_magic_items = _select_starting_magic_items(magic_budget, kit=chosen_kit)

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
        "Reach": reach,
        "Combat_Points": combat_points,

        "Magic": "YES" if magic_info.get("magic") else "NO",
        "Magic_Type": magic_info.get("type", "None"),
        "Magic_Subtype": magic_info.get("subtype"),
        "God": god,
        "Magic_Description": magic_info.get("description", ""),

        # Pure English versions for the PDF character sheets
        "Magic_Type_Eng": magic_type_eng,
        "Magic_Subtype_Eng": magic_subtype_eng,
        "Magic_Description_Eng": magic_desc_eng,
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
        "Remaining_Capital_Sp": int(round( (post_purchases.get("final_remaining_bp", max(0, int(round(remaining_after_phases * 10)))) ) / 10 )),
        "Has_Mount": bool(chosen_mount),

        # === 100 kits XV siecle Cote des Epees EN + free survival kit only ===
        "Prebuilt_Kit_Tier": chosen_kit["kit_id"] if chosen_kit else None,
        "Prebuilt_Kit_Cost_Sp": round(kit_spent_sp, 1),
        "Prebuilt_Kit_Items": chosen_kit["items"] if chosen_kit else [],
        "Prebuilt_Kit_Source": chosen_kit.get("source_file") if chosen_kit else None,

        # === Main equipment display column ===
        "Armes_et_Bouclier": chosen_weapon_kit["name"] if chosen_weapon_kit else "Aucun",

        # For main.py splitting (free survival + 80kit gear as the "purchased" equipment)
        "Post_Kit_Purchases": chosen_kit["items"] if chosen_kit else [],

        "Special": data.get("spec", "Aucun"),
    }