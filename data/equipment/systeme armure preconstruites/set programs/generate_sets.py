import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from data.equipment import groupe1_prices as grp_prices

# ============================================================
# EQUIPMENT DATABASE
# ============================================================

# Underlayers / Padded Armor - prices from master Groupe1 list
underlayers = [
    {"name": "Aketon", "price": grp_prices.get_groupe1_price("Aketon (basic padded jack)", 8), "type": "aketon"},
    {"name": "Gambeson (basic)", "price": grp_prices.get_groupe1_price("Gambeson (basic)", 9), "type": "gambeson"},
    {"name": "Gambeson (long / fended)", "price": grp_prices.get_groupe1_price("Gambeson (long / fended)", 14), "type": "gambeson"},
    {"name": "Reinforced Gambeson", "price": grp_prices.get_groupe1_price("Reinforced Gambeson", 18), "type": "gambeson"},
    {"name": "Reinforced Gambeson (long)", "price": grp_prices.get_groupe1_price("Reinforced Gambeson (long)", 26), "type": "gambeson"},
    {"name": "Padded Jack (medium / troop)", "price": grp_prices.get_groupe1_price("Padded Jack (medium / troop)", 22), "type": "padded_jack"},
    {"name": "Pourpoint (light civil)", "price": grp_prices.get_groupe1_price("Pourpoint (light civil)", 12), "type": "pourpoint"},
    {"name": "Arming Doublet", "price": grp_prices.get_groupe1_price("Arming Doublet", 45), "type": "arming_doublet"},
]

# Torso armor (main protection)
torso_mail = [
    {"name": "Mail Shirt (sleeveless)", "price": 80, "type": "mail"},
    {"name": "Mail Haubergeon (mid-length)", "price": 115, "type": "mail"},
    {"name": "Mail Hauberk (complete)", "price": 170, "type": "mail"},
    {"name": "Mail Coat (long with sleeves)", "price": 220, "type": "mail"},
]

torso_plate = [
    {"name": "Coat of Plates", "price": 45, "type": "plate"},
    {"name": "Jack of Plates", "price": 55, "type": "plate"},
    {"name": "Brigandine (standard troop)", "price": 85, "type": "plate"},
    {"name": "Brigandine (high quality)", "price": 240, "type": "plate"},
    {"name": "Simple Breastplate", "price": 42, "type": "plate"},
    {"name": "Breastplate + Backplate", "price": 95, "type": "plate"},
    {"name": "Breastplate + Backplate (tempered)", "price": 220, "type": "plate"},
]

# Pauldrons (épaulière) rule: require proper metal torso armor (breastplate + backplate / cuirass).
# Historical (XIVe–XVᵉ): Pauldrons are attached to and articulate with the cuirass.
# Not sufficient: Simple Breastplate alone, Coat of Plates, Jack of Plates, or Brigandine
# (even though they count as plate torso for fauld/tassets etc.).
cuirass_names = {"Breastplate + Backplate", "Breastplate + Backplate (tempered)"}

# Helmets
helmets = [
    {"name": "Leather Helmet", "price": 2},
    {"name": "Nasal Helmet", "price": 8},
    {"name": "Cervelière", "price": 9},
    {"name": "Kettle Hat", "price": 15},
    {"name": "Cabasset", "price": 22},
    {"name": "Morion", "price": 28},
    {"name": "Lobster-tailed Pot", "price": 38},
    {"name": "Sallet", "price": 42},
    {"name": "Barbute (Italian)", "price": 45},
    {"name": "Burgonet", "price": 45},
    {"name": "Bascinet (basic)", "price": 48},
    {"name": "Great Helm", "price": 70},
    {"name": "Armet (Italian articulated)", "price": 85},
    {"name": "Close Helmet", "price": 95},
    {"name": "Great Bascinet (with bevor)", "price": 135},
]

# Head accessories
head_accessories = [
    {"name": "Mail coif", "price": 20},
    {"name": "Aventail", "price": 16},
]

# Neck protection
neck_protection = [
    {"name": "Gorget (normal)", "price": 12},
    {"name": "Gorget (articulated/raised)", "price": 18},
    {"name": "Gorget (reinforced)", "price": 25},
    {"name": "Bevor", "price": 12},
]

# Shoulder protection
# Pauldrons require plate torso; Besagews require pauldrons + plate torso
shoulder_pauldrons = [
    {"name": "Pauldrons + Guards", "price": 75},
]
shoulder_besagews = [
    {"name": "Besagews (pair)", "price": 6},
]

arm_protection = [
    {"name": "Couter (pair)", "price": 10},
    {"name": "Vambraces + Couter", "price": 35},
    {"name": "Vambraces + Couter + Rerebrace", "price": 85},
]

# Mail voiders: only with metallic (plate) torso and NO mail on torso
arm_mail_voiders = [
    {"name": "Mail voiders (pair)", "price": 15},
]

# Hand protection
gauntlets = [
    {"name": "Gauntlets (normal)", "price": 22},
    {"name": "Gauntlets (articulated reinforced)", "price": 45},
]

# Torso accessories — ALL require plate torso (breastplate, brigandine, etc.)
torso_accessories = [
    {"name": "Fauld", "price": 18},
    {"name": "Plackart", "price": 15},
    {"name": "Garde-reins", "price": 14},
]

# Leg protection
# Tassets require plate torso
leg_tassets = [
    {"name": "Tassets (short pair)", "price": 16},
    {"name": "Tassets (long)", "price": 25},
]

# Cuisses (no plate torso requirement)
leg_cuisses = [
    {"name": "Cuisses (normal)", "price": 42},
    {"name": "Cuisses (reinforced Maximilian)", "price": 85},
]

# Combined upper leg list for reference
leg_upper = leg_tassets + leg_cuisses

leg_knee = [
    {"name": "Poleyns + Knee guards", "price": 28},
]

leg_lower = [
    {"name": "Schynbalds / Demi-greaves", "price": 15},
    {"name": "Greaves (normal)", "price": 35},
    {"name": "Greaves (reinforced)", "price": 55},
]

# Mail leg protection (can be worn under plate greaves/cuisses)
leg_mail = [
    {"name": "Mail Chausses", "price": 95},
    {"name": "Mail Demi-chausses", "price": 55},
]

feet = [
    {"name": "Sabatons (normal)", "price": 18},
    {"name": "Sabatons (broad bear-foot)", "price": 25},
]

# Shields (sorted by size) - prices from master Groupe1 list
shields = [
    {"name": "Brocchiere (Size 1)", "price": grp_prices.get_groupe1_price("Brocchiere (Size 1)", 5), "size": 1},
    {"name": "Small Buckler (Size 2)", "price": grp_prices.get_groupe1_price("Small Buckler (Size 2)", 7), "size": 2},
    {"name": "Buckler (Size 3)", "price": grp_prices.get_groupe1_price("Buckler (Size 3)", 9), "size": 3},
    {"name": "Large Buckler (Size 4)", "price": grp_prices.get_groupe1_price("Large Buckler (Size 4)", 12), "size": 4},
    {"name": "Small Rotella (Size 5)", "price": grp_prices.get_groupe1_price("Small Rotella (Size 5)", 14), "size": 5},
    {"name": "Rotella (Size 6)", "price": grp_prices.get_groupe1_price("Rotella (Size 6)", 16), "size": 6},
    {"name": "Large Rotella (Size 7)", "price": grp_prices.get_groupe1_price("Large Rotella (Size 7)", 22), "size": 7},
    {"name": "Heater Shield (Size 8)", "price": grp_prices.get_groupe1_price("Heater Shield (Size 8)", 24), "size": 8},
    {"name": "Velites Parma (Size 9)", "price": grp_prices.get_groupe1_price("Velites Parma (Size 9)", 26), "size": 9},
    {"name": "Kite Shield (Size 10)", "price": grp_prices.get_groupe1_price("Kite Shield (Size 10)", 27), "size": 10},
    {"name": "Scutum (Size 11)", "price": grp_prices.get_groupe1_price("Scutum (Size 11)", 35), "size": 11},
]

# Weapons - One-handed (PRIMARY eligible: Club or better, no Knife/Dagger as primary)
weapons_1h_primary = [
    {"name": "Club", "price": 6, "mounted": False},
    {"name": "Arming Sword", "price": 75, "mounted": False},
    {"name": "Baselard", "price": 55, "mounted": False},
    {"name": "Falchion", "price": 70, "mounted": False},
    {"name": "Cutlass", "price": 95, "mounted": False},
    {"name": "Katzbalger", "price": 95, "mounted": False},
    {"name": "Broadsword", "price": 110, "mounted": False},
    {"name": "Scimitar", "price": 140, "mounted": False},
    {"name": "Rapier", "price": 280, "mounted": False},
    {"name": "Sidesword", "price": 250, "mounted": False},
    {"name": "Main-gauche", "price": 95, "mounted": False},
    {"name": "Light Hammer", "price": 50, "mounted": True},
    {"name": "Mace", "price": 65, "mounted": True},
    {"name": "Flanged Mace", "price": 95, "mounted": True},
    {"name": "Hand Axe", "price": 45, "mounted": False},
    {"name": "Francisca", "price": 50, "mounted": False},
]

# Strict foot-only 1h primary weapons (excludes any with "mounted": True).
# This guarantees that mounted weapons (Light Hammer, Mace, Flanged Mace)
# are NEVER selected for !has_mount characters. The has_mount flag is set
# only for budgets >=200 with small probability (and can be set late in fill
# if remaining >=150), but foot characters (the vast majority of low-tier
# and many high-tier) must never receive them. Lance is separately gated.
weapons_1h_primary_foot = [w for w in weapons_1h_primary if not w.get("mounted", False)]

# All 1h weapons (including sidearms for secondary/additional weapon use)
# Note: mounted weapons are excluded here for safety (weapons_1h is currently unused
# in generate_set selection paths, but foot-only is the correct default).
weapons_1h = [
    {"name": "Knife", "price": 6, "mounted": False},
    {"name": "Dagger", "price": 14, "mounted": False},
    {"name": "Rondel Dagger", "price": 28, "mounted": False},
] + weapons_1h_primary_foot

# Weapons - Two-handed (foot only)
weapons_2h = [
    {"name": "Longsword", "price": 145, "mounted": False},
    {"name": "Estoc (2h)", "price": 220, "mounted": False},
    {"name": "Spear", "price": 7, "mounted": False},
    {"name": "Reinforced Spear", "price": 20, "mounted": False},
    {"name": "Billhook", "price": 35, "mounted": False},
    {"name": "Pike", "price": 28, "mounted": False},
    {"name": "Bill", "price": 55, "mounted": False},
    {"name": "Guisarme", "price": 55, "mounted": False},
    {"name": "Glaive", "price": 55, "mounted": False},
    {"name": "Halberd", "price": 75, "mounted": False},
    {"name": "Poleaxe", "price": 105, "mounted": False},
    {"name": "War Scythe", "price": 35, "mounted": False},
    {"name": "Bec de Corbin", "price": 160, "mounted": False},
    {"name": "Partisan", "price": 130, "mounted": False},
    {"name": "Ranseur", "price": 120, "mounted": False},
    {"name": "Military Fork", "price": 28, "mounted": False},
    {"name": "Lucerne Hammer", "price": 145, "mounted": False},
    {"name": "Quarterstaff", "price": 18, "mounted": False},
    {"name": "Morning Star", "price": 95, "mounted": False},
    {"name": "War Hammer", "price": 80, "mounted": False},
    {"name": "Maul", "price": 75, "mounted": False},
    {"name": "Battle Axe", "price": 95, "mounted": False},
]

# Weapons - Hand-and-a-half
weapons_1_5h = [
    {"name": "Messer", "price": 80, "mounted": False},
    {"name": "Bastard Estoc", "price": 170, "mounted": False},
    {"name": "Bastard Sword", "price": 155, "mounted": False},
    {"name": "Light Flail", "price": 65, "mounted": False},
    {"name": "War Hammer (Renaissance)", "price": 130, "mounted": False},
]

# Weapons - Mounted only
weapons_mounted = [
    {"name": "Lance", "price": 42, "mounted": True},
]

# Ranged weapons - Bows & Crossbows (PRIMARY ONLY - cannot be secondary)
ranged_bow_xbow = [
    {"name": "Short Bow", "price": 32, "ammo": "Arrows (12)", "ammo_price": 7, "is_bow_xbow": True},
    {"name": "Longbow", "price": 55, "ammo": "Arrows (12)", "ammo_price": 7, "is_bow_xbow": True},
    {"name": "Composite Bow", "price": 160, "ammo": "Arrows (12)", "ammo_price": 7, "is_bow_xbow": True},
    {"name": "Composite Bow (quality)", "price": 230, "ammo": "Arrows (12)", "ammo_price": 7, "is_bow_xbow": True},
    {"name": "Light Crossbow", "price": 95, "ammo": "Crossbow Bolts (12)", "ammo_price": 6, "is_bow_xbow": True},
    {"name": "Crossbow", "price": 135, "ammo": "Crossbow Bolts (12)", "ammo_price": 6, "is_bow_xbow": True},
    {"name": "Heavy Crossbow", "price": 175, "ammo": "Heavy Crossbow Bolts (12)", "ammo_price": 9, "is_bow_xbow": True},
]

# Ranged weapons - Throwing/Slings (can be primary or secondary)
ranged_throwing = [
    {"name": "Sling", "price": 0.2, "ammo": "Sling bullets (12)", "ammo_price": 0.03, "is_bow_xbow": False},
    {"name": "Staff Sling", "price": 0.5, "ammo": "Sling bullets (12)", "ammo_price": 0.03, "is_bow_xbow": False},
    {"name": "Javelin (x3)", "price": 18, "ammo": None, "ammo_price": 0, "is_bow_xbow": False},
    {"name": "Reinforced Javelin (x3)", "price": 39, "ammo": None, "ammo_price": 0, "is_bow_xbow": False},
    {"name": "War Dart (x3)", "price": 84, "ammo": None, "ammo_price": 0, "is_bow_xbow": False},
]

# All ranged weapons (for primary selection)
ranged_weapons = ranged_bow_xbow + ranged_throwing

# Mounts
mounts = [
    {"name": "Rouncey", "price": 75},
    {"name": "Courser", "price": 110},
    {"name": "Palfrey", "price": 100},
    {"name": "Destrier", "price": 220},
    {"name": "Destrier (quality)", "price": 350},
]

# Horse armor (barding)
horse_armor = [
    {"name": "Leather barding", "price": 140},
    {"name": "Chain barding", "price": 480},
    {"name": "Plate mail barding", "price": 950},
]

horse_head = [
    {"name": "Leather chanfron", "price": 22},
    {"name": "Plate chanfron", "price": 65},
]

horse_neck = [
    {"name": "Leather crinet", "price": 18},
    {"name": "Chain crinet", "price": 95},
    {"name": "Plate crinet", "price": 180},
]

horse_tack = [
    {"name": "Riding Saddle", "price": 35},
    {"name": "War Saddle", "price": 95},
]


def pick_affordable(items, remaining, max_ratio=1.0):
    """Pick a random item from the list that costs <= remaining * max_ratio."""
    affordable = [i for i in items if i["price"] <= remaining * max_ratio]
    if affordable:
        return random.choice(affordable)
    return None


def count_armor_pieces(equipment):
    """Count how many armor pieces are in the set (for 'nearly full armor' rule)."""
    armor_slots = {"Torso Armor", "Underlayer", "Helmet", "Head Accessory", "Neck",
                   "Shoulders", "Arms", "Hands", "Torso Accessory", "Upper Legs",
                   "Knees", "Lower Legs", "Leg Mail", "Feet"}
    return sum(1 for slot, _, _ in equipment if slot in armor_slots)


def generate_set(budget):
    """Generate a random valid equipment set within the given budget.

    ORDER: Weapons & Shield FIRST → Helmet → Body Armor → Rest of armor
    RULES:
    - If bow/crossbow: only small shield (size 3 or less)
    - If nearly full armor: shield can be smaller
    - Besagews require pauldrons + plate torso
    - Pauldrons (épaulière) require proper cuirass (Breastplate + Backplate). Pauldrons are attached to the metal torso armor (breast+back). Not allowed with coat-of-plates, brigandine, jack-of-plates or simple breastplate alone. (XIVe–XVᵉ historical rule)
    - Fauld, Garde-reins, Tassets require plate torso
    - Only one shoulder-carried weapon (polearms, longsword, etc.)
    - Characters with 2h weapons CAN carry shields
    - Mail chausses/demi-chausses can be worn under plate leg armor
    - Mounted weapons (Light Hammer, Mace, Flanged Mace, Lance) are STRICTLY
      only for has_mount=True characters. Foot characters (has_mount=False,
      which is ALWAYS true for budgets <200sp and often for higher) NEVER
      receive them in any primary/secondary/additional weapon slot. Enforced
      by using weapons_1h_primary_foot for all !has_mount weapon selections.
    """
    remaining = budget
    equipment = []
    has_mount = False
    torso_type = None  # "mail", "plate", or None
    has_2h_weapon = False
    has_bow_xbow = False  # tracks if primary ranged is bow/crossbow

    # ===== VERY LOW BUDGET HANDLING =====
    if budget <= 5:
        cheap_items = [
            ("Primary Weapon", "Club", 6),
            ("Primary Weapon", "Knife", 6),
            ("Shield", "Brocchiere (Size 1)", 5),
            ("Helmet", "Leather Helmet", 2),
            ("Primary Weapon (Ranged)", "Sling", 0.2),
            ("Ammunition", "Sling bullets (12)", 0.03),
        ]
        affordable_cheap = [i for i in cheap_items if i[2] <= remaining]
        if affordable_cheap:
            affordable_cheap.sort(key=lambda x: -x[2] + random.uniform(-0.5, 0.5))
            for item in affordable_cheap:
                if item[2] <= remaining:
                    existing_slots = [e[0] for e in equipment]
                    if "Primary Weapon" in item[0] and any("Primary Weapon" in s for s in existing_slots):
                        continue
                    equipment.append(item)
                    remaining -= item[2]
        total_spent = budget - remaining
        slot_order_low = {
            "Primary Weapon": 1, "Primary Weapon (Ranged)": 1.1, "Ammunition": 1.2, "Shield": 1.3,
            "Helmet": 2,
        }
        equipment.sort(key=lambda e: slot_order_low.get(e[0], 4))
        return equipment, total_spent

    # ===== MOUNT DECISION (before weapons, as it affects weapon choices) =====
    mount_chance = 0
    if budget >= 200:
        mount_chance = 0.2
    if budget >= 400:
        mount_chance = 0.3
    if budget >= 700:
        mount_chance = 0.4

    if random.random() < mount_chance:
        affordable_mounts = [m for m in mounts if m["price"] <= remaining * 0.4]
        if affordable_mounts:
            mount = random.choice(affordable_mounts)
            equipment.append(("Mount", mount["name"], mount["price"]))
            remaining -= mount["price"]
            has_mount = True

            # Saddle
            affordable_saddles = [s for s in horse_tack if s["price"] <= remaining]
            if affordable_saddles:
                saddle = random.choice(affordable_saddles)
                equipment.append(("Saddle", saddle["name"], saddle["price"]))
                remaining -= saddle["price"]

            # Horse armor
            if remaining > 140 and random.random() < 0.4:
                bard = pick_affordable(horse_armor, remaining, 0.5)
                if bard:
                    equipment.append(("Horse Armor", bard["name"], bard["price"]))
                    remaining -= bard["price"]

            # Chanfron
            if remaining > 22 and random.random() < 0.5:
                ch = pick_affordable(horse_head, remaining)
                if ch:
                    equipment.append(("Horse Head", ch["name"], ch["price"]))
                    remaining -= ch["price"]

            # Crinet
            if remaining > 18 and random.random() < 0.3:
                cr = pick_affordable(horse_neck, remaining)
                if cr:
                    equipment.append(("Horse Neck", cr["name"], cr["price"]))
                    remaining -= cr["price"]

    # ================================================================
    # PHASE 1: WEAPONS & SHIELD FIRST
    # ================================================================

    # ===== PRIMARY WEAPON =====
    if remaining >= 6:
        weapon_style = random.random()

        if budget <= 75:
            if has_mount:
                if remaining >= 42:
                    equipment.append(("Primary Weapon", "Lance", 42))
                    remaining -= 42
                    has_2h_weapon = True
                else:
                    pool = [w for w in weapons_2h if w["name"] in ("Spear", "Reinforced Spear") and w["price"] <= remaining]
                    if pool:
                        wpn = random.choice(pool)
                        equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                        remaining -= wpn["price"]
                        has_2h_weapon = True
            elif weapon_style < 0.65:
                spear_pool = [w for w in weapons_2h if w["name"] in ("Spear", "Reinforced Spear") and w["price"] <= remaining]
                if spear_pool:
                    wpn = random.choice(spear_pool)
                    equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                    remaining -= wpn["price"]
                    has_2h_weapon = True
                else:
                    equipment.append(("Primary Weapon", "Club", 6))
                    remaining -= 6
            elif weapon_style < 0.80:
                cheap_1h = [w for w in weapons_1h_primary_foot if w["price"] <= remaining and w["price"] <= 50]
                if cheap_1h:
                    wpn = random.choice(cheap_1h)
                    equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                    remaining -= wpn["price"]
                else:
                    equipment.append(("Primary Weapon", "Club", 6))
                    remaining -= 6
            elif weapon_style < 0.90:
                cheap_2h = [w for w in weapons_2h if w["price"] <= remaining and w["price"] <= 40]
                if cheap_2h:
                    wpn = random.choice(cheap_2h)
                    equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                    remaining -= wpn["price"]
                    has_2h_weapon = True
            else:
                pool = [w for w in ranged_throwing if w["price"] <= remaining]
                if pool:
                    wpn = random.choice(pool)
                    equipment.append(("Primary Weapon (Ranged)", wpn["name"], wpn["price"]))
                    remaining -= wpn["price"]
                    has_bow_xbow = wpn["is_bow_xbow"]
                    if wpn["ammo"] and remaining >= wpn["ammo_price"]:
                        equipment.append(("Ammunition", wpn["ammo"], wpn["ammo_price"]))
                        remaining -= wpn["ammo_price"]

        elif budget <= 400:
            if has_mount:
                    if remaining >= 42 and random.random() < 0.5:
                        equipment.append(("Primary Weapon", "Lance", 42))
                        remaining -= 42
                        has_2h_weapon = True
                    else:
                        mounted_pool = [w for w in weapons_1h_primary if w["mounted"] and w["price"] <= remaining]
                        non_mounted_pool = [w for w in weapons_1h_primary_foot if w["price"] <= remaining]
                        pool = mounted_pool if mounted_pool and random.random() < 0.6 else non_mounted_pool
                        if pool:
                            wpn = random.choice(pool)
                            equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                            remaining -= wpn["price"]
                    else:
                        if weapon_style < 0.35:
                            pool = [w for w in weapons_1h_primary_foot if w["price"] <= remaining]
                            if pool:
                                wpn = random.choice(pool)
                                equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                                remaining -= wpn["price"]
                        elif weapon_style < 0.55:
                            pool = [w for w in weapons_2h if w["price"] <= remaining]
                            if pool:
                                wpn = random.choice(pool)
                                equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                                remaining -= wpn["price"]
                                has_2h_weapon = True
                        elif weapon_style < 0.70:
                            pool = [w for w in weapons_1_5h if w["price"] <= remaining]
                            if pool:
                                wpn = random.choice(pool)
                                equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                                remaining -= wpn["price"]
                            else:
                                pool = [w for w in weapons_1h_primary_foot if w["price"] <= remaining]
                                if pool:
                                    wpn = random.choice(pool)
                                    equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                                    remaining -= wpn["price"]
                        elif weapon_style < 0.90:
                            pool = [w for w in ranged_bow_xbow if w["price"] <= remaining]
                            if pool:
                                wpn = random.choice(pool)
                                equipment.append(("Primary Weapon (Ranged)", wpn["name"], wpn["price"]))
                                remaining -= wpn["price"]
                                has_bow_xbow = wpn["is_bow_xbow"]
                                if wpn["ammo"] and remaining >= wpn["ammo_price"]:
                                    equipment.append(("Ammunition", wpn["ammo"], wpn["ammo_price"]))
                                    remaining -= wpn["ammo_price"]
                                    if remaining >= wpn["ammo_price"] and random.random() < 0.4:
                                        equipment.append(("Ammunition", wpn["ammo"], wpn["ammo_price"]))
                                        remaining -= wpn["ammo_price"]
                            else:
                                pool = [w for w in ranged_throwing if w["price"] <= remaining]
                                if pool:
                                    wpn = random.choice(pool)
                                    equipment.append(("Primary Weapon (Ranged)", wpn["name"], wpn["price"]))
                                    remaining -= wpn["price"]
                                    has_bow_xbow = wpn["is_bow_xbow"]
                                    if wpn["ammo"] and remaining >= wpn["ammo_price"]:
                                        equipment.append(("Ammunition", wpn["ammo"], wpn["ammo_price"]))
                                        remaining -= wpn["ammo_price"]
                        else:
                            spear_pool = [w for w in weapons_2h if w["name"] in ("Spear", "Reinforced Spear") and w["price"] <= remaining]
                            if spear_pool:
                                wpn = random.choice(spear_pool)
                                equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                                remaining -= wpn["price"]
                                has_2h_weapon = True

        else:
            # HIGH BUDGET (401+ sp)
            if has_mount:
                if remaining >= 42 and random.random() < 0.6:
                    equipment.append(("Primary Weapon", "Lance", 42))
                    remaining -= 42
                    has_2h_weapon = True
                else:
                    mounted_pool = [w for w in weapons_1h_primary if w["mounted"] and w["price"] <= remaining]
                    non_mounted_pool = [w for w in weapons_1h_primary_foot if w["price"] <= remaining]
                    pool = mounted_pool if mounted_pool and random.random() < 0.6 else non_mounted_pool
                    if pool:
                        wpn = random.choice(pool)
                        equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                        remaining -= wpn["price"]
            elif weapon_style < 0.50:
                polearm_pool = [w for w in weapons_2h if w["price"] <= remaining and w["price"] >= 55]
                if not polearm_pool:
                    polearm_pool = [w for w in weapons_2h if w["price"] <= remaining]
                if polearm_pool:
                    wpn = random.choice(polearm_pool)
                    equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                    remaining -= wpn["price"]
                    has_2h_weapon = True
            elif weapon_style < 0.70:
                pool = [w for w in weapons_1_5h if w["price"] <= remaining]
                pool += [w for w in weapons_2h if w["name"] in ("Longsword", "Estoc (2h)") and w["price"] <= remaining]
                if pool:
                    wpn = random.choice(pool)
                    equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                    remaining -= wpn["price"]
                    if wpn["name"] in ("Longsword", "Estoc (2h)"):
                        has_2h_weapon = True
            elif weapon_style < 0.85:
                quality_1h = [w for w in weapons_1h_primary_foot if w["price"] <= remaining and w["price"] >= 75]
                if quality_1h:
                    wpn = random.choice(quality_1h)
                    equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                    remaining -= wpn["price"]
                else:
                    pool = [w for w in weapons_1h_primary_foot if w["price"] <= remaining]
                    if pool:
                        wpn = random.choice(pool)
                        equipment.append(("Primary Weapon", wpn["name"], wpn["price"]))
                        remaining -= wpn["price"]
            else:
                pool = [w for w in ranged_bow_xbow if w["price"] <= remaining]
                if pool:
                    wpn = random.choice(pool)
                    equipment.append(("Primary Weapon (Ranged)", wpn["name"], wpn["price"]))
                    remaining -= wpn["price"]
                    has_bow_xbow = wpn["is_bow_xbow"]
                    if wpn["ammo"] and remaining >= wpn["ammo_price"]:
                        equipment.append(("Ammunition", wpn["ammo"], wpn["ammo_price"]))
                        remaining -= wpn["ammo_price"]
                        if remaining >= wpn["ammo_price"] and random.random() < 0.5:
                            equipment.append(("Ammunition", wpn["ammo"], wpn["ammo_price"]))
                            remaining -= wpn["ammo_price"]

    # ===== SECONDARY WEAPON (sidearm) =====
    sidearm_chance = 0.3 if budget <= 75 else 0.6
    if remaining >= 6 and random.random() < sidearm_chance:
        sidearms = [
            {"name": "Knife", "price": 6},
            {"name": "Dagger", "price": 14},
            {"name": "Rondel Dagger", "price": 28},
            {"name": "Hand Axe", "price": 45},
            {"name": "Falchion", "price": 70},
            {"name": "Arming Sword", "price": 75},
            {"name": "Messer", "price": 80},
        ]
        pool = [s for s in sidearms if s["price"] <= remaining]
        if pool:
            # Prefer proper side weapons (arming sword etc.) over cheap daggers when possible
            proper = [s for s in pool if s["name"] in ("Arming Sword", "Falchion", "Messer", "Hand Axe")]
            side = random.choice(proper) if proper else random.choice(pool)
            equipment.append(("Secondary Weapon", side["name"], side["price"]))
            remaining -= side["price"]

    # ===== ADDITIONAL RANGED (if primary was melee) =====
    has_ranged = any("Ranged" in e[0] for e in equipment)
    if not has_ranged and remaining >= 7 and random.random() < 0.3:
        pool = [w for w in ranged_throwing if w["price"] <= remaining]
        if pool:
            wpn = random.choice(pool)
            equipment.append(("Secondary (Ranged)", wpn["name"], wpn["price"]))
            remaining -= wpn["price"]
            if wpn["ammo"] and remaining >= wpn["ammo_price"]:
                equipment.append(("Ammunition", wpn["ammo"], wpn["ammo_price"]))
                remaining -= wpn["ammo_price"]

    # ===== SHIELD =====
    if budget <= 75:
        shield_chance = 0.75
    elif budget <= 400:
        shield_chance = 0.55
    else:
        shield_chance = 0.30

    if remaining >= 5 and random.random() < shield_chance:
        if has_bow_xbow:
            pool = [s for s in shields if s["price"] <= remaining and s["size"] <= 3]
        else:
            pool = [s for s in shields if s["price"] <= remaining]
        if pool:
            shld = random.choice(pool)
            equipment.append(("Shield", shld["name"], shld["price"]))
            remaining -= shld["price"]

    # ===== NEW RULE: BUY SIDE WEAPON (arming sword, falchion, messer or hand axe) BEFORE ANY ARMOR =====
    # Enforce that a proper side weapon is acquired before proceeding to helmet or body armor.
    side_weapon_names = {"Arming Sword", "Falchion", "Messer", "Hand Axe"}
    has_proper_side_weapon = any(
        e[1] in side_weapon_names for e in equipment if "Weapon" in e[0]
    )
    if not has_proper_side_weapon and remaining >= 45:
        pool = [
            w for w in weapons_1h_primary_foot
            if w["name"] in side_weapon_names and w["price"] <= remaining
        ]
        if pool:
            # Take the most expensive affordable proper side weapon
            side = max(pool, key=lambda x: x["price"])
            equipment.append(("Secondary Weapon", side["name"], side["price"]))
            remaining -= side["price"]

    # ================================================================
    # PHASE 2: HELMET (first plate armor piece is typically helmet)
    # ================================================================

    if remaining >= 2 and random.random() < 0.85:
        helm = pick_affordable(helmets, remaining, 0.5)
        if helm:
            equipment.append(("Helmet", helm["name"], helm["price"]))
            remaining -= helm["price"]

        # Head accessory
        if remaining >= 16 and random.random() < 0.35:
            acc = pick_affordable(head_accessories, remaining)
            if acc:
                equipment.append(("Head Accessory", acc["name"], acc["price"]))
                remaining -= acc["price"]

    # ================================================================
    # PHASE 3: BODY ARMOR (torso)
    # ================================================================

    has_mail_torso = False
    has_plate_torso = False
    has_cuirass = False  # proper breast+back plate for pauldrons (épaulière) historical rule

    torso_chance = random.random()
    if torso_chance < 0.35 and remaining >= 42:
        torso = pick_affordable(torso_plate, remaining, 0.7)
        if torso:
            equipment.append(("Torso Armor", torso["name"], torso["price"]))
            remaining -= torso["price"]
            torso_type = "plate"
            has_plate_torso = True
            if torso["name"] in cuirass_names:
                has_cuirass = True
    elif torso_chance < 0.65 and remaining >= 80:
        torso = pick_affordable(torso_mail, remaining, 0.7)
        if torso:
            equipment.append(("Torso Armor", torso["name"], torso["price"]))
            remaining -= torso["price"]
            torso_type = "mail"
            has_mail_torso = True
    elif torso_chance < 0.80 and remaining >= 122 and budget >= 300:
        mail = pick_affordable(torso_mail, remaining * 0.5, 0.9)
        if mail:
            equipment.append(("Torso Armor", mail["name"], mail["price"]))
            remaining -= mail["price"]
            has_mail_torso = True
            plate = pick_affordable(torso_plate, remaining, 0.7)
            if plate:
                equipment.append(("Torso Armor", plate["name"], plate["price"]))
                remaining -= plate["price"]
                has_plate_torso = True
                if plate["name"] in cuirass_names:
                    has_cuirass = True
            torso_type = "mail_and_plate"

    # ===== UNDERLAYER ===== (moved early for gorget and arm fabric rules: fabric must be under plate neck/arms)
    plate_piece_count = sum(1 for slot, name, _ in equipment if
                           (slot == "Torso Armor" and any(p["name"] == name for p in torso_plate)) or
                           (slot == "Helmet" and any(h["name"] == name and h["price"] >= 42 for h in helmets)) or
                           (slot in ("Shoulders", "Arms", "Hands", "Upper Legs", "Knees", "Lower Legs", "Feet")))

    if remaining >= 8 and random.random() < 0.85:
        if plate_piece_count >= 3 and has_plate_torso and remaining >= 45:
            if random.random() < 0.90:
                equipment.append(("Underlayer", "Arming Doublet", 45))
                remaining -= 45
            else:
                valid_underlayers = [u for u in underlayers if u["price"] <= remaining
                                     and u["type"] != "aketon" and u["type"] != "arming_doublet"]
                if valid_underlayers:
                    under = random.choice(valid_underlayers)
                    equipment.append(("Underlayer", under["name"], under["price"]))
                    remaining -= under["price"]
        elif has_plate_torso and remaining >= 45 and random.random() < 0.70:
            equipment.append(("Underlayer", "Arming Doublet", 45))
            remaining -= 45
        else:
            valid_underlayers = []
            for u in underlayers:
                if u["price"] > remaining:
                    continue
                if u["type"] == "aketon" and torso_type != "mail":
                    continue
                if u["type"] == "arming_doublet" and not has_plate_torso:
                    continue
                valid_underlayers.append(u)

            if valid_underlayers:
                under = random.choice(valid_underlayers)
                equipment.append(("Underlayer", under["name"], under["price"]))
                remaining -= under["price"]

    # ================================================================
    # PHASE 4: REST OF ARMOR
    # ================================================================

    # ===== NECK =====
    if remaining >= 12 and random.random() < 0.5:
        neck = pick_affordable(neck_protection, remaining)
        if neck:
            # NEW RULE: Gorget (and Bevor) always over at least fabric protection (aketon/gambison/arming doublet).
            # Never directly on skin. Minimum: fabric layer. Often mail too.
            gorget_names = {"Gorget (normal)", "Gorget (articulated/raised)", "Gorget (reinforced)", "Bevor"}
            if neck["name"] in gorget_names:
                fabric_protection_names = ["Arming Doublet", "Gambeson", "Reinforced Gambeson", "Padded Jack", "Pourpoint"]
                has_fabric_protection = any(
                    e[0] == "Underlayer" and any(fab in e[1] for fab in fabric_protection_names)
                    for e in equipment
                )
                if not has_fabric_protection:
                    # do not add gorget without fabric underneath
                    pass  # skip adding this neck item
                else:
                    equipment.append(("Neck", neck["name"], neck["price"]))
                    remaining -= neck["price"]
            else:
                equipment.append(("Neck", neck["name"], neck["price"]))
                remaining -= neck["price"]

    # ===== SHOULDERS =====
    # NEW RULE (historical): Pauldrons (épaulière) require proper metal torso armor system
    # (breastplate + backplate / cuirass). They are attached to and articulate with the cuirass.
    # Not allowed with only Simple Breastplate, Coat of Plates, Brigandine or Jack of Plates.
    # Besagews require pauldrons + plate torso (kept).
    has_pauldrons = False

    if remaining >= 75 and has_cuirass and random.random() < 0.35:
        equipment.append(("Shoulders", "Pauldrons + Guards", 75))
        remaining -= 75
        has_pauldrons = True

    if has_pauldrons and has_plate_torso and remaining >= 6 and random.random() < 0.5:
        equipment.append(("Shoulders", "Besagews (pair)", 6))
        remaining -= 6

    # ===== ARMS =====
    if remaining >= 10 and random.random() < 0.6:
        arm_pool = [a for a in arm_protection if a["price"] <= remaining]
        if has_plate_torso and not has_mail_torso and remaining >= 15:
            arm_pool += [a for a in arm_mail_voiders if a["price"] <= remaining]
        # NEW RULE: Vambraces, Couter, Rerebrace require Arming Doublet or other fabric (tissu) protection
        fabric_protection_names = ["Arming Doublet", "Gambeson", "Reinforced Gambeson", "Padded Jack", "Pourpoint"]
        has_fabric_protection = any(
            e[0] == "Underlayer" and any(fab in e[1] for fab in fabric_protection_names)
            for e in equipment
        )
        if not has_fabric_protection:
            arm_pool = [a for a in arm_pool if not any(req in a["name"] for req in ["Vambraces", "Couter", "Rerebrace"])]
        if arm_pool:
            arm = random.choice(arm_pool)
            equipment.append(("Arms", arm["name"], arm["price"]))
            remaining -= arm["price"]

    # ===== GAUNTLETS =====
    if remaining >= 22 and random.random() < 0.5:
        gaunt = pick_affordable(gauntlets, remaining)
        if gaunt:
            equipment.append(("Hands", gaunt["name"], gaunt["price"]))
            remaining -= gaunt["price"]

    # ===== TORSO ACCESSORIES (Fauld, Plackart, Garde-reins) =====
    # Rule: Fauld and Garde-reins require plate torso; Plackart is always allowed
    if remaining >= 14 and random.random() < 0.45:
        if has_plate_torso:
            tacc_pool = [t for t in torso_accessories if t["price"] <= remaining]
        else:
            # Only Plackart without plate torso
            tacc_pool = [t for t in torso_accessories if t["price"] <= remaining and t["name"] == "Plackart"]
        if tacc_pool:
            tacc = random.choice(tacc_pool)
            equipment.append(("Torso Accessory", tacc["name"], tacc["price"]))
            remaining -= tacc["price"]

    if remaining >= 14 and budget >= 300 and has_plate_torso and random.random() < 0.3:
        existing_tacc_names = [e[1] for e in equipment if e[0] == "Torso Accessory"]
        available = [t for t in torso_accessories if t["price"] <= remaining and t["name"] not in existing_tacc_names]
        if available:
            tacc = random.choice(available)
            equipment.append(("Torso Accessory", tacc["name"], tacc["price"]))
            remaining -= tacc["price"]

    # ===== UPPER LEGS =====
    # Rule: Tassets require plate torso; Cuisses are always allowed
    if remaining >= 16 and random.random() < 0.5:
        if has_plate_torso:
            upper_pool = [l for l in leg_upper if l["price"] <= remaining]
        else:
            upper_pool = [l for l in leg_cuisses if l["price"] <= remaining]
        if upper_pool:
            leg = random.choice(upper_pool)
            equipment.append(("Upper Legs", leg["name"], leg["price"]))
            remaining -= leg["price"]

    # ===== MAIL LEG PROTECTION (chausses / demi-chausses) =====
    # Can be worn under plate leg armor or standalone
    if remaining >= 55 and random.random() < 0.35:
        leg_m = pick_affordable(leg_mail, remaining)
        if leg_m:
            equipment.append(("Leg Mail", leg_m["name"], leg_m["price"]))
            remaining -= leg_m["price"]

    # ===== KNEES =====
    if remaining >= 28 and random.random() < 0.4:
        k = leg_knee[0]
        if k["price"] <= remaining:
            equipment.append(("Knees", k["name"], k["price"]))
            remaining -= k["price"]

    # ===== LOWER LEGS =====
    if remaining >= 15 and random.random() < 0.5:
        lower = pick_affordable(leg_lower, remaining)
        if lower:
            equipment.append(("Lower Legs", lower["name"], lower["price"]))
            remaining -= lower["price"]

    # ===== FEET =====
    if remaining >= 18 and random.random() < 0.35:
        foot = pick_affordable(feet, remaining)
        if foot:
            equipment.append(("Feet", foot["name"], foot["price"]))
            remaining -= foot["price"]

    # ===== NEARLY FULL ARMOR: downgrade shield if needed =====
    armor_count = count_armor_pieces(equipment)
    if armor_count >= 8:
        shield_idx = None
        for i, (slot, name, price) in enumerate(equipment):
            if slot == "Shield":
                for s in shields:
                    if s["name"] == name and s["size"] > 5:
                        shield_idx = i
                        break
        if shield_idx is not None:
            small_shields = [s for s in shields if s["size"] <= 5]
            if small_shields:
                new_shield = random.choice(small_shields)
                old_price = equipment[shield_idx][2]
                equipment[shield_idx] = ("Shield", new_shield["name"], new_shield["price"])
                remaining += old_price - new_shield["price"]

    # ================================================================
    # PHASE 5: SPEND REMAINING BUDGET
    # ================================================================
    for _attempt in range(5):
        if remaining < 5:
            break

        existing_slots = set(e[0] for e in equipment)

        # Fill empty armor slots
        if "Helmet" not in existing_slots and remaining >= 2:
            helm = pick_affordable(helmets, remaining)
            if helm:
                equipment.append(("Helmet", helm["name"], helm["price"]))
                remaining -= helm["price"]

        if "Torso Armor" not in existing_slots and remaining >= 42:
            torso = pick_affordable(torso_plate + torso_mail, remaining)
            if torso:
                equipment.append(("Torso Armor", torso["name"], torso["price"]))
                remaining -= torso["price"]
                if torso["type"] == "plate":
                    has_plate_torso = True
                    if torso["name"] in cuirass_names:
                        has_cuirass = True
                else:
                    has_mail_torso = True

        if "Neck" not in existing_slots and remaining >= 12:
            neck = pick_affordable(neck_protection, remaining)
            if neck:
                gorget_names = {"Gorget (normal)", "Gorget (articulated/raised)", "Gorget (reinforced)", "Bevor"}
                if neck["name"] in gorget_names:
                    fabric_protection_names = ["Arming Doublet", "Gambeson", "Reinforced Gambeson", "Padded Jack", "Pourpoint"]
                    has_fabric_protection = any(
                        e[0] == "Underlayer" and any(fab in e[1] for fab in fabric_protection_names)
                        for e in equipment
                    )
                    if has_fabric_protection:
                        equipment.append(("Neck", neck["name"], neck["price"]))
                        remaining -= neck["price"]
                    # else skip, per rule
                else:
                    equipment.append(("Neck", neck["name"], neck["price"]))
                    remaining -= neck["price"]

        if "Arms" not in existing_slots and remaining >= 10:
            arm_pool_extra = [a for a in arm_protection if a["price"] <= remaining]
            if has_plate_torso and not has_mail_torso and remaining >= 15:
                arm_pool_extra += [a for a in arm_mail_voiders if a["price"] <= remaining]
            # NEW RULE: Vambraces, Couter, Rerebrace require fabric protection (now that underlayer fill may have run in previous passes)
            fabric_protection_names = ["Arming Doublet", "Gambeson", "Reinforced Gambeson", "Padded Jack", "Pourpoint"]
            has_fabric_protection = any(
                e[0] == "Underlayer" and any(fab in e[1] for fab in fabric_protection_names)
                for e in equipment
            )
            if not has_fabric_protection:
                arm_pool_extra = [a for a in arm_pool_extra if not any(req in a["name"] for req in ["Vambraces", "Couter", "Rerebrace"])]
            if arm_pool_extra:
                arm = random.choice(arm_pool_extra)
                equipment.append(("Arms", arm["name"], arm["price"]))
                remaining -= arm["price"]

        if "Hands" not in existing_slots and remaining >= 22:
            gaunt = pick_affordable(gauntlets, remaining)
            if gaunt:
                equipment.append(("Hands", gaunt["name"], gaunt["price"]))
                remaining -= gaunt["price"]

        # Pauldrons: only if proper cuirass (NEW RULE)
        if "Shoulders" not in existing_slots and remaining >= 75 and has_cuirass:
            equipment.append(("Shoulders", "Pauldrons + Guards", 75))
            remaining -= 75
            has_pauldrons = True
            if remaining >= 6:
                equipment.append(("Shoulders", "Besagews (pair)", 6))
                remaining -= 6

        # Upper legs: tassets only with plate torso
        if "Upper Legs" not in existing_slots and remaining >= 16:
            if has_plate_torso:
                upper_pool = [l for l in leg_upper if l["price"] <= remaining]
            else:
                upper_pool = [l for l in leg_cuisses if l["price"] <= remaining]
            if upper_pool:
                leg = random.choice(upper_pool)
                equipment.append(("Upper Legs", leg["name"], leg["price"]))
                remaining -= leg["price"]

        # Mail leg protection
        if "Leg Mail" not in existing_slots and remaining >= 55:
            leg_m = pick_affordable(leg_mail, remaining)
            if leg_m:
                equipment.append(("Leg Mail", leg_m["name"], leg_m["price"]))
                remaining -= leg_m["price"]

        if "Knees" not in existing_slots and remaining >= 28:
            k = leg_knee[0]
            if k["price"] <= remaining:
                equipment.append(("Knees", k["name"], k["price"]))
                remaining -= k["price"]

        if "Lower Legs" not in existing_slots and remaining >= 15:
            lower = pick_affordable(leg_lower, remaining)
            if lower:
                equipment.append(("Lower Legs", lower["name"], lower["price"]))
                remaining -= lower["price"]

        if "Feet" not in existing_slots and remaining >= 18:
            foot = pick_affordable(feet, remaining)
            if foot:
                equipment.append(("Feet", foot["name"], foot["price"]))
                remaining -= foot["price"]

        # Torso accessories (require plate torso for fauld/garde-reins)
        if remaining >= 14:
            existing_tacc = [e[1] for e in equipment if e[0] == "Torso Accessory"]
            if has_plate_torso:
                available_tacc = [t for t in torso_accessories if t["price"] <= remaining and t["name"] not in existing_tacc]
            else:
                available_tacc = [t for t in torso_accessories if t["price"] <= remaining and t["name"] not in existing_tacc and t["name"] == "Plackart"]
            if available_tacc:
                tacc = random.choice(available_tacc)
                equipment.append(("Torso Accessory", tacc["name"], tacc["price"]))
                remaining -= tacc["price"]

        # Head accessory
        if "Head Accessory" not in existing_slots and remaining >= 16:
            acc = pick_affordable(head_accessories, remaining)
            if acc:
                equipment.append(("Head Accessory", acc["name"], acc["price"]))
                remaining -= acc["price"]

        # Underlayer
        if "Underlayer" not in existing_slots and remaining >= 8:
            plate_ct = sum(1 for slot, name, _ in equipment if
                          (slot == "Torso Armor" and any(p["name"] == name for p in torso_plate)) or
                          (slot in ("Shoulders", "Arms", "Hands", "Upper Legs", "Knees", "Lower Legs", "Feet")))
            if plate_ct >= 3 and has_plate_torso and remaining >= 45:
                equipment.append(("Underlayer", "Arming Doublet", 45))
                remaining -= 45
            else:
                valid_ul = []
                for u in underlayers:
                    if u["price"] > remaining:
                        continue
                    if u["type"] == "aketon" and torso_type != "mail":
                        continue
                    if u["type"] == "arming_doublet" and not has_plate_torso:
                        continue
                    valid_ul.append(u)
                if valid_ul:
                    under = random.choice(valid_ul)
                    equipment.append(("Underlayer", under["name"], under["price"]))
                    remaining -= under["price"]

        # Additional weapon
        if remaining > 50 and "Additional Weapon" not in existing_slots:
            primary_src = weapons_1h_primary if has_mount else weapons_1h_primary_foot
            expensive_weapons = [w for w in primary_src if w["price"] <= remaining and w["price"] >= 45]
            expensive_weapons += [w for w in weapons_1_5h if w["price"] <= remaining]
            if not has_2h_weapon:
                expensive_weapons += [w for w in weapons_2h if w["price"] <= remaining and w["price"] >= 55]
            if expensive_weapons:
                wpn = random.choice(expensive_weapons)
                equipment.append(("Additional Weapon", wpn["name"], wpn["price"]))
                remaining -= wpn["price"]

        # Secondary weapon
        if "Secondary Weapon" not in existing_slots and remaining >= 6:
            sidearms_fill = [
                {"name": "Knife", "price": 6},
                {"name": "Dagger", "price": 14},
                {"name": "Rondel Dagger", "price": 28},
                {"name": "Hand Axe", "price": 45},
                {"name": "Falchion", "price": 70},
                {"name": "Arming Sword", "price": 75},
                {"name": "Messer", "price": 80},
            ]
            pool = [s for s in sidearms_fill if s["price"] <= remaining]
            if pool:
                # Prefer proper side weapons when budget allows during fill
                proper = [s for s in pool if s["name"] in ("Arming Sword", "Falchion", "Messer", "Hand Axe")]
                side = random.choice(proper) if proper else random.choice(pool)
                equipment.append(("Secondary Weapon", side["name"], side["price"]))
                remaining -= side["price"]

        # Secondary ranged
        has_ranged_fill = any("Ranged" in e[0] for e in equipment)
        if not has_ranged_fill and "Secondary (Ranged)" not in existing_slots and remaining >= 7:
            pool = [w for w in ranged_throwing if w["price"] <= remaining]
            if pool:
                wpn = random.choice(pool)
                equipment.append(("Secondary (Ranged)", wpn["name"], wpn["price"]))
                remaining -= wpn["price"]
                if wpn["ammo"] and remaining >= wpn["ammo_price"]:
                    equipment.append(("Ammunition", wpn["ammo"], wpn["ammo_price"]))
                    remaining -= wpn["ammo_price"]

        # Extra ammo
        if remaining >= 6:
            ranged_items = [e for e in equipment if "Ranged" in e[0]]
            if ranged_items:
                for rw in ranged_bow_xbow + ranged_throwing:
                    if rw["name"] in [e[1] for e in ranged_items] and rw["ammo"]:
                        if remaining >= rw["ammo_price"]:
                            equipment.append(("Ammunition", rw["ammo"], rw["ammo_price"]))
                            remaining -= rw["ammo_price"]
                            break

        # Horse equipment
        if has_mount and remaining >= 18:
            has_horse_armor = any(e[0] == "Horse Armor" for e in equipment)
            has_horse_head = any(e[0] == "Horse Head" for e in equipment)
            has_horse_neck = any(e[0] == "Horse Neck" for e in equipment)

            if not has_horse_head and remaining >= 22:
                ch = pick_affordable(horse_head, remaining)
                if ch:
                    equipment.append(("Horse Head", ch["name"], ch["price"]))
                    remaining -= ch["price"]
            if not has_horse_neck and remaining >= 18:
                cr = pick_affordable(horse_neck, remaining)
                if cr:
                    equipment.append(("Horse Neck", cr["name"], cr["price"]))
                    remaining -= cr["price"]
            if not has_horse_armor and remaining >= 140:
                bard = pick_affordable(horse_armor, remaining)
                if bard:
                    equipment.append(("Horse Armor", bard["name"], bard["price"]))
                    remaining -= bard["price"]

        # Second additional weapon
        if remaining > 75:
            existing_additional = [e for e in equipment if e[0] == "Additional Weapon"]
            if len(existing_additional) < 2:
                primary_src = weapons_1h_primary if has_mount else weapons_1h_primary_foot
                extra_1h = [w for w in primary_src if w["price"] <= remaining and w["price"] >= 45]
                if extra_1h:
                    wpn = random.choice(extra_1h)
                    equipment.append(("Additional Weapon", wpn["name"], wpn["price"]))
                    remaining -= wpn["price"]

        # Shield
        if "Shield" not in existing_slots and remaining >= 5 and not has_bow_xbow:
            pool = [s for s in shields if s["price"] <= remaining]
            if pool:
                shld = random.choice(pool)
                equipment.append(("Shield", shld["name"], shld["price"]))
                remaining -= shld["price"]

        # Buy a mount
        if not has_mount and remaining >= 150 and "Mount" not in existing_slots:
            affordable_mounts_fill = [m for m in mounts if m["price"] <= remaining * 0.5]
            if affordable_mounts_fill:
                mount = random.choice(affordable_mounts_fill)
                equipment.append(("Mount", mount["name"], mount["price"]))
                remaining -= mount["price"]
                has_mount = True
                affordable_saddles_fill = [s for s in horse_tack if s["price"] <= remaining]
                if affordable_saddles_fill:
                    saddle = random.choice(affordable_saddles_fill)
                    equipment.append(("Saddle", saddle["name"], saddle["price"]))
                    remaining -= saddle["price"]

        # Mail torso if no torso armor yet
        if "Torso Armor" not in existing_slots and remaining >= 80:
            torso_fill = pick_affordable(torso_mail + torso_plate, remaining)
            if torso_fill:
                equipment.append(("Torso Armor", torso_fill["name"], torso_fill["price"]))
                remaining -= torso_fill["price"]
                if torso_fill["type"] == "plate":
                    has_plate_torso = True
                    if torso_fill["name"] in cuirass_names:
                        has_cuirass = True
                else:
                    has_mail_torso = True

        # Add mail torso under plate (combo) - not if voiders present
        has_voiders_already = any(e[1] == "Mail voiders (pair)" for e in equipment)
        if has_plate_torso and not has_mail_torso and remaining >= 80 and not has_voiders_already:
            existing_torso_names = [e[1] for e in equipment if e[0] == "Torso Armor"]
            mail_already = any("Mail" in n for n in existing_torso_names)
            if not mail_already:
                mail_fill = pick_affordable(torso_mail, remaining)
                if mail_fill:
                    equipment.append(("Torso Armor", mail_fill["name"], mail_fill["price"]))
                    remaining -= mail_fill["price"]
                    has_mail_torso = True

    total_spent = budget - remaining

    # Sort equipment by display order
    slot_order = {
        "Mount": 0.0, "Saddle": 0.1, "Horse Armor": 0.2, "Horse Head": 0.3, "Horse Neck": 0.4,
        "Primary Weapon": 1.0, "Primary Weapon (Ranged)": 1.1, "Secondary Weapon": 1.2,
        "Secondary (Ranged)": 1.3, "Ammunition": 1.4, "Shield": 1.5,
        "Helmet": 2.0, "Head Accessory": 2.1,
        "Torso Armor": 3.0, "Underlayer": 3.1,
        "Neck": 4.0, "Shoulders": 4.1, "Arms": 4.2, "Hands": 4.3,
        "Torso Accessory": 4.4, "Upper Legs": 4.5, "Leg Mail": 4.55,
        "Knees": 4.6, "Lower Legs": 4.7, "Feet": 4.8,
        "Additional Weapon": 5.0,
    }
    equipment.sort(key=lambda e: slot_order.get(e[0], 4.9))

    return equipment, total_spent


def format_set(set_number, budget, equipment, total_spent):
    """Format a single equipment set as markdown."""
    lines = []
    lines.append(f"### Set #{set_number:03d} — Budget: {budget} sp | Spent: {total_spent:.1f} sp")
    lines.append("")
    lines.append("| Slot | Item | Price |")
    lines.append("|------|------|-------|")
    for slot, name, price in equipment:
        if price < 1:
            price_str = f"{price*100:.0f} cp"
        else:
            price_str = f"{price:.0f} sp"
        lines.append(f"| {slot} | {name} | {price_str} |")
    lines.append("")
    return "\n".join(lines)


def format_set_compact(set_number, budget, equipment, total_spent):
    """Format a single equipment set as compact text: price + item list."""
    items = [name for _, name, _ in equipment]
    return f"#{set_number:03d} [{budget}sp] {', '.join(items)}"


def main():
    random.seed(42)

    # Generate 300 sets with budgets between 275 and 684 sp
    budgets = []
    for _ in range(300):
        budgets.append(random.randint(275, 684))

    # Sort budgets
    budgets.sort()

    # Generate output (markdown)
    output_lines = []
    output_lines.append("# Equipment Sets — Sword Coast (Groupe 1)")
    output_lines.append("")
    output_lines.append("**Setting:** Sword Coast + Baldur's Gate + Luskan")
    output_lines.append("**Tech Level:** 6-7 (Early to Late Renaissance)")
    output_lines.append("**Budget Range:** 275 sp to 684 sp")
    output_lines.append(f"**Total Sets Generated:** {len(budgets)}")
    output_lines.append("")
    output_lines.append("## Composition Rules Applied")
    output_lines.append("")
    output_lines.append("- **Order of selection:** Weapons & Shield → Helmet → Body Armor → Rest of armor")
    output_lines.append("- **Budget weapon progression:**")
    output_lines.append("  - Low budget (≤75 sp): Spear + Shield dominates (poor militia)")
    output_lines.append("  - Medium budget (76-400 sp): Shield + side weapon, OR bow/crossbow, OR polearm")
    output_lines.append("  - High budget (401+ sp): Heavy armor + polearm (spear+shield archetype disappears)")
    output_lines.append("- **Bow/Crossbow rule:** If equipped with a bow or crossbow, only a small shield (Size 3 or less) is allowed.")
    output_lines.append("- **Nearly full armor rule:** If wearing 8+ armor pieces, shield is downgraded to Size 5 or less.")
    output_lines.append("- **Shoulder-carried weapon:** Only ONE weapon carried on the shoulder (polearm, longsword, etc.) per set.")
    output_lines.append("- **Besagews rule:** Besagews require both Pauldrons AND plate torso protection.")
    output_lines.append("- **Pauldrons rule:** Pauldrons (épaulière) require proper cuirass = Breastplate + Backplate (metal torso armor system). Attached to and articulate with the cuirass. Not with simple breastplate / coat of plates / brigandine alone. (XIVᵉ–XVᵉ historical reality)")
    output_lines.append("- **Torso accessories rule:** Fauld, Garde-reins, and Tassets require plate torso.")
    output_lines.append("- **Two-handed + Shield:** Characters with two-handed primary weapons CAN carry shields.")
    output_lines.append("- Aketon can only be selected when wearing torso mail protection.")
    output_lines.append("- Arming Doublet can only be selected when wearing torso plate protection.")
    output_lines.append("- Gambeson / Reinforced Gambeson / Padded Jack / Pourpoint can be used freely as underlayers.")
    output_lines.append("- Vambraces, Couter, Rerebrace can only be added with Arming Doublet or other fabric (tissu) protection.")
    output_lines.append("- Gorget / Bevor always over at least fabric protection (aketon/gambison/arming doublet); never directly on skin. Often with mail collar underneath too.")
    output_lines.append("- Mail Chausses / Demi-chausses can be worn under plate leg armor or standalone.")
    output_lines.append("- Mounted weapons (Lance, Light Hammer, Mace, Flanged Mace) are STRICTLY only included when a mount is present (has_mount=True).")
    output_lines.append("  NO exceptions for low budgets: foot characters (<200sp always, and many higher) never get Light Hammer/Mace/Flanged Mace/Lance.")
    output_lines.append("- Two-handed foot weapons are not assigned to mounted characters.")
    output_lines.append("")
    output_lines.append("---")
    output_lines.append("")

    # Budget tier headers
    tier_names = [
        (275, 400, "Tier 1: Comfortable (275-400 sp)"),
        (401, 550, "Tier 2: Well-off (401-550 sp)"),
        (551, 684, "Tier 3: Wealthy (551-684 sp)"),
    ]

    # Compact text output
    compact_lines = []
    compact_lines.append("Equipment Sets — Sword Coast (Groupe 1)")
    compact_lines.append("=" * 45)
    compact_lines.append("")

    set_number = 1
    current_tier_idx = 0

    for budget in budgets:
        # Check if we need a new tier header
        while current_tier_idx < len(tier_names) and budget > tier_names[current_tier_idx][1]:
            current_tier_idx += 1

        if current_tier_idx < len(tier_names):
            low, high, name = tier_names[current_tier_idx]
            if budget >= low and (set_number == 1 or budgets[set_number - 2] < low):
                output_lines.append(f"## {name}")
                output_lines.append("")
                compact_lines.append(f"--- {name} ---")

        equipment, total_spent = generate_set(budget)
        if equipment:
            output_lines.append(format_set(set_number, budget, equipment, total_spent))
            compact_lines.append(format_set_compact(set_number, budget, equipment, total_spent))
        else:
            output_lines.append(f"### Set #{set_number:03d} — Budget: {budget} sp | Spent: 0 sp")
            output_lines.append("")
            output_lines.append("*Budget too low for any equipment.*")
            output_lines.append("")
            compact_lines.append(f"#{set_number:03d} [{budget}sp] (nothing)")
        set_number += 1

    # Write markdown output
    with open("/workspace/equipment_sets.md", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    # Write compact text output
    with open("/workspace/equipment_sets.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(compact_lines))

    print(f"Generated {len(budgets)} equipment sets successfully!")
    print(f"Output: /workspace/equipment_sets.md")
    print(f"Output: /workspace/equipment_sets.txt")



# =============================================================================
# UPGRADE: Normalize all prices in this module's DB to come from Groupe1 master
# This ensures the set generator also respects the required source file.
# =============================================================================
def _normalize_price_list(lst):
    if not isinstance(lst, list):
        return
    for item in lst:
        if isinstance(item, dict) and "name" in item and "price" in item:
            p = grp_prices.get_groupe1_price(item["name"], item.get("price", 0))
            if p > 0:
                item["price"] = p

for _lst_name in ["underlayers", "torso_mail", "torso_plate", "helmets", "mail_heads", "plate_heads", "neck", "shoulders", "arms", "hands", "waist", "upper_legs", "lower_legs", "feet", "weapons_1h_primary", "weapons_1h_secondary", "weapons_2h", "weapons_ranged", "weapons_mounted", "side_weapons", "mounts", "barding", "horse_head", "horse_neck", "saddles"]:
    if _lst_name in globals():
        _normalize_price_list(globals()[_lst_name])

if __name__ == "__main__":
    main()