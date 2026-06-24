import math
import os
import random
from functools import lru_cache
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
        (vigilance * 0.3) +
        (stealth * 0.3) +
        (speed * 0.25) +
        (dodge * 0.1) +
        (climbing * 0.1) +
        (endurance * 0.10) +
        (regeneration * 0.05)
    )
    
    total = combat_malus - secondary_malus
    return math.floor(total)


# ====================== COMBAT FORMULAS ======================

def cp(x: float) -> float:
    """Combat Points non-linéaire (y) selon valeur brute (x):
    Si x > 1 → y = x^1.4
    Si x < 0 → y = - ( (-x)^0.7 )
    Si x = 0 ou x = 1 → y = x
    """
    if x > 1:
        return round(x ** 1.4, 2)
    elif x < 0:
        return round(-((-x) ** 0.7), 2)
    else:
        return round(float(x), 2)


def calculate_grappling(weight_score: float, build_score: float, balance: float, quickness: float) -> float:
    """Grappling - Simulation réaliste (poids très impactant)"""
    return math.floor(
        weight_score  +      
        build_score * 0.1 +          
        balance /3 +              
        quickness /4               
    )


def calculate_melee(weight_score: float, size_score: int, coordination: float, 
                   balance: float, quickness: float) -> float:
    """Melee - Variance augmentée pour se rapprocher de Grappling"""
    return math.floor(
        weight_score / 2.0 +           
        quickness / 3 +              
        coordination / 4 +           
        balance / 5.0 +                
        size_score /2              
    )


def calculate_fencing(quickness: float, coordination: float, balance: float, size_score: int) -> float:
    """Fencing = floor( quickness/4 + Coordination/2 + Balance/3 )"""
    return math.floor(
        quickness / 5 + coordination / 3 + balance / 4 +  size_score * 1
    )


def calculate_projectiles(precision: float, coordination: float, quickness: float) -> int:
    return math.floor(precision + coordination / 3 + quickness / 5)


def calculate_reach(size_score: float | int) -> float:
    """Reach = size score (raw)"""
    return float(size_score)


def calculate_combat_points(
    grappling: float,
    melee: float,
    projectiles: float,
    fencing: float,
    racial_cp: float = 0.0
) -> float:
    """Total Combat Points = cp(Grappling) + cp(Melee) + cp(Projectiles) + cp(Fencing) + cp(Reach) + CP_racial"""
    total = (
        cp(grappling) +
        cp(melee) +
        cp(projectiles) +
        cp(fencing) +
        racial_cp
    )
    return round(total, 2)


# ====================== MAGIC SYSTEM ======================
# Seuil calibré pour ~50% de personnages magiquement actifs
# (basé sur la distribution des Combat Points générés par generate_character)
MAGIC_THRESHOLD = -6    # ~50% des personnages sont magiques (combat_points < ce seuil)
ARCANIST_THRESHOLD = -9.0  # ~20% les plus faibles (les plus "négatifs") sont Arcanistes


def determine_magic_type(combat_points: float, settlement_type: str = "Village") -> dict:
    """Détermine le type et sous-type de magie avec couleurs pour la magie sauvage"""
    
    if combat_points >= MAGIC_THRESHOLD:
        return {
            "magic": False,
            "type": "None",
            "subtype": None,
            "description": "Non-magique"
        }

    roll = random.random()

    if roll < 0.47:           # 47% Théurgique
        magic_type = "Théurgique"
        st_lower = settlement_type.lower()

        if any(x in st_lower for x in ["temple", "monastère", "sanctuaire", "capitale", "métropole", "ville"]):
            subtype = "Magie Blanche"
            desc = "Magie Blanche (guérison, protection, lumière divine)"
        elif any(x in st_lower for x in ["forest", "forêt", "wilderness", "druid", "jungle"]):
            subtype = "Magie Verte"
            desc = "Magie Verte (nature, croissance, esprits de la forêt)"
        else:
            # Cas neutre → légère préférence Blanche
            subtype = "Magie Blanche" if random.random() < 0.60 else "Magie Verte"
            desc = "Magie Blanche (guérison, protection)" if subtype == "Magie Blanche" else "Magie Verte (nature, croissance)"

    elif roll < 0.87:         # 40% Arcanique
        magic_type = "Arcanique"
        subtype = "Magicien"
        desc = "Magicien arcanique (étude, formules et savoir ancien)"

    else:                     # 13% Sauvage → Couleurs
        magic_type = "Sauvage"
        
        wild_roll = random.random()
        if wild_roll < 0.25:
            subtype = "Magie Blanche"
            desc = "Magie Sauvage - Blanche (chaos pur, imprévisible, énergie brute)"
        elif wild_roll < 0.50:
            subtype = "Magie Rouge"
            desc = "Magie Sauvage - Rouge (feu, destruction, passion, colère)"
        elif wild_roll < 0.70:
            subtype = "Magie Verte"
            desc = "Magie Sauvage - Verte (nature sauvage, vie primitive, croissance incontrôlée)"
        elif wild_roll < 0.85:
            subtype = "Magie Bleue"
            desc = "Magie Sauvage - Bleue (eau, illusions, connaissance cachée, froid)"
        else:
            subtype = "Magie Noire"
            desc = "Magie Sauvage - Noire (nécromancie, ombre, corruption, pouvoir obscur)"

    return {
        "magic": True,
        "type": magic_type,
        "subtype": subtype,
        "description": desc
    }


# ====================== WIZARD SPELLS (Niveau 1) ======================
# Data source: data/magic/sorts_mage_niveau_1_frequence.txt
# Each Arcanique/Magicien starts with 6 known random level-1 spells, weighted by frequency.

@lru_cache(maxsize=1)
def load_wizard_level1_spells() -> list[tuple[str, int]]:
    """Returns list of (spell_name, popularity_weight 1-5) for level 1 wizard spells."""
    here = os.path.dirname(__file__)
    path = os.path.join(here, "data", "magic", "sorts_mage_niveau_1_frequence.txt")
    if not os.path.exists(path):
        print("WARNING: sorts_mage_niveau_1_frequence.txt not found")
        return []

    spells: dict[str, int] = {}
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("=") or line.startswith("-") or "Sort" in line[:12]:
                    continue

                # Parse table rows: "Spell Name | 5 | Category" or "Spell Name | 5 | ..."
                if "|" in line:
                    parts = [p.strip() for p in line.split("|") if p.strip()]
                    if len(parts) >= 2:
                        name = parts[0]
                        try:
                            pop = int(parts[1])
                            if 1 <= pop <= 5:
                                # keep the highest weight seen for duplicates
                                if name not in spells or pop > spells[name]:
                                    spells[name] = pop
                        except ValueError:
                            continue
    except Exception as e:
        print(f"ERROR loading spells file: {e}")
        return []

    return [(name, weight) for name, weight in spells.items()]


def choose_starting_spells(magic_type: str, magic_subtype: str | None = None, count: int = 6) -> list[str]:
    """
    For Arcanique/Magicien characters: return 'count' distinct level-1 spells
    chosen randomly with weighting from the frequency file.
    Returns empty list for everyone else.
    """
    mtype = (magic_type or "").lower()
    msub = (magic_subtype or "").lower()

    if mtype != "arcanique":
        return []
    if "magicien" not in msub and "mage" not in msub:
        return []

    spell_weights = load_wizard_level1_spells()
    if not spell_weights:
        return []

    # Weighted sampling without replacement
    items = [s for s, w in spell_weights]
    weights = [w for s, w in spell_weights]

    selected: list[str] = []
    items = list(items)
    weights = list(weights)

    for _ in range(count):
        if not items:
            break
        total = sum(weights)
        if total <= 0:
            break
        r = random.uniform(0, total)
        upto = 0.0
        for i in range(len(weights)):
            if upto + weights[i] >= r:
                selected.append(items[i])
                del items[i]
                del weights[i]
                break
            upto += weights[i]

    return selected


# ====================== GOD / DIVINITY SYSTEM (Devotion Hierarchies) ======================
# Primary data source: the two formatted devotion files
#   - gods_by_region.tsv
#   - gods_by_ethnie.tsv
# These give ranked lists by "quantité de devotions" (worship popularity).

import os
import csv
from functools import lru_cache
from collections import defaultdict
import random


@lru_cache(maxsize=1)
def load_gods_by_region() -> dict[str, list[str]]:
    """{region_key: [god_rank1 (most devoted), god_rank2, ...]}"""
    here = os.path.dirname(__file__)
    path = os.path.join(here, "data", "magic", "gods_by_region.tsv")
    data = defaultdict(list)
    if not os.path.exists(path):
        print("WARNING: gods_by_region.tsv not found")
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                data[row["region"].strip()].append(row["god"].strip())
    except Exception as e:
        print(f"ERROR loading gods_by_region.tsv: {e}")
    return dict(data)


@lru_cache(maxsize=1)
def load_gods_by_ethnie() -> dict[str, list[str]]:
    """{ethnicity_key: [god_rank1 (most devoted), ...]}"""
    here = os.path.dirname(__file__)
    path = os.path.join(here, "data", "magic", "gods_by_ethnie.tsv")
    data = defaultdict(list)
    if not os.path.exists(path):
        print("WARNING: gods_by_ethnie.tsv not found")
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                data[row["ethnicity"].strip()].append(row["god"].strip())
    except Exception as e:
        print(f"ERROR loading gods_by_ethnie.tsv: {e}")
    return dict(data)


def _find_best_key(query: str, keys: list[str]) -> str | None:
    """Fuzzy match for region/ethnicity keys (case-insensitive contains)."""
    if not query:
        return None
    q = query.lower().strip()
    for k in keys:
        if q in k.lower() or k.lower() in q:
            return k
    # word overlap fallback
    qwords = set(q.split())
    for k in keys:
        if qwords & set(k.lower().split()):
            return k
    return None


def choose_god(
    ethnicity: str,
    region_name: str,
    settlement_type: str,
    magic_type: str = "",
    magic_subtype: str = "",
    max_candidates: int = 8
) -> str:
    """
    Choose a god using the devotion hierarchy (ethnie first or region lists from gods_by_*.tsv).
    Selection: pool gods from ethnie OR region, rank-weighted random (rank 1 far more common),
    settlement thematic bias, and magic-type bias.
    Special rule: Théurgique + "Magie Verte" (green/nature magic) → very strongly prefers nature gods
    (Chauntea, Silvanus, Mielikki, Eldath, Rillifane, Shiallia...).
    Théurgique characters are always guaranteed a non-None god.
    """
    by_reg = load_gods_by_region()
    by_eth = load_gods_by_ethnie()

    eth_key = _find_best_key(ethnicity, list(by_eth.keys()))
    reg_key = _find_best_key(region_name, list(by_reg.keys()))

    eth_list = by_eth.get(eth_key, []) if eth_key else []
    reg_list = by_reg.get(reg_key, []) if reg_key else []

    # Compute magic context early for guarantees and special rules
    mtype = (magic_type or "").lower()
    msub = (magic_subtype or "").lower()

    # Core nature gods (for early guarantees + Magie Verte rule)
    # Include common variants/spellings as they appear in the devotion TSVs
    nature_gods = {
        "Chauntea", "Silvanus", "Mielikki", "Eldath",
        "Rillifane Rallathil", "Rillifane",
        "Shiallia", "Lurue", "Gwaeron Windstrom", "Sheela Peryroyl",
        "Baervan"  # sometimes appears in forest/halfling/gnome nature contexts
    }

    # Early cultural match failed
    if not eth_list and not reg_list:
        if mtype == "théurgique":
            # Hard guarantee: Théurgique always gets a god, even with no eth/region match
            if "verte" in msub or "green" in msub or "nature" in msub:
                return "Silvanus"
            return "Chauntea"
        return "None"

    # Pool gods from ethnie OR region (first check cultural lists as requested)
    all_gods = set(eth_list) | set(reg_list)

    weights = defaultdict(float)

    for god in all_gods:
        eth_rank = eth_list.index(god) + 1 if god in eth_list else None
        reg_rank = reg_list.index(god) + 1 if god in reg_list else None

        ranks = [r for r in [eth_rank, reg_rank] if r is not None]
        best_rank = min(ranks) if ranks else 20
        w = 21 - best_rank   # rank1 -> weight 20, rank20 -> weight 1

        # Intersection bonus (god strong in both ethnie+region = culturally central)
        if eth_rank is not None and reg_rank is not None:
            w *= 1.7

        weights[god] = w

    # Settlement type thematic influence (user asked if settlement can influence - yes)
    sett = (settlement_type or "").lower()
    if any(x in sett for x in ["metropolis", "major port", "major trade", "large town"]):
        for g in ["Waukeen", "Gond", "Oghma", "Deneir", "Milil", "Sune", "Helm", "Tyr", "Torm"]:
            if g in weights:
                weights[g] *= 1.5
    if any(x in sett for x in ["rural village", "farming hamlet", "forest village"]):
        for g in ["Chauntea", "Silvanus", "Mielikki", "Eldath", "Rillifane Rallathil"]:
            if g in weights:
                weights[g] *= 1.5
    if any(x in sett for x in ["coastal", "fishing village", "major port city", "smuggler's port"]):
        for g in ["Umberlee", "Valkur", "Deep Sashelas", "Selûne", "Shaundakul"]:
            if g in weights:
                weights[g] *= 1.5
    if "mountain" in sett or "dwarven" in sett or "mining" in sett:
        for g in ["Moradin", "Berronar Purargent", "Clangeddin Barbeargent", "Dumathoïn"]:
            if g in weights:
                weights[g] *= 1.5

    # Magic type bias (Arcanique gets strong boost to arcanist gods; Théurgique mild + guarantee)
    arcanist_gods = {"Mystra", "Azuth", "Savras", "Velsharoon", "Leira", "Oghma", "Deneir", "Milil", "Corellon Larethian", "Labelas Enoreth", "Sehanine Archelune"}

    if mtype == "arcanique":
        for g in list(weights):
            if g in arcanist_gods:
                weights[g] *= 4.0
            else:
                weights[g] *= 0.18
    elif mtype == "théurgique":
        for g in list(weights):
            weights[g] *= 1.2

        # === Specific rule requested: Théurgique + Magie Verte = dieux de la nature ===
        # Strongly boost nature gods; heavily suppress others so green theurgs almost always get nature deities
        # when they exist in the character's ethnie/region devotion lists.
        if "verte" in msub or "green" in msub or "nature" in msub:
            for g in list(weights):
                if g in nature_gods:
                    weights[g] *= 7.0   # dominant preference
                else:
                    weights[g] *= 0.10  # strong suppression of non-nature gods for green theurgy

        # Enforce the rule more strictly: if the character's cultural lists contain at least one nature god,
        # only choose among the nature gods (respecting their relative devotion ranks + boosts).
        if "verte" in msub or "green" in msub or "nature" in msub:
            nature_available = {g: w for g, w in weights.items() if g in nature_gods}
            if nature_available:
                weights = nature_available

    elif mtype == "sauvage":
        wild = {"Malar", "Talos", "Auril", "Silvanus", "Mielikki", "Rillifane Rallathil", "Umberlee"}
        for g in list(weights):
            if g in wild:
                weights[g] *= 2.8
            else:
                weights[g] *= 0.5

    weights = {g: w for g, w in weights.items() if w >= 0.5}

    if not weights:
        if mtype == "théurgique":
            # Un Théurgique a TOUJOURS un dieu (per explicit requirement)
            c = eth_list or reg_list
            if c:
                if "verte" in msub or "green" in msub:
                    # Prefer a nature god from the available cultural list first
                    for g in c:
                        if g in nature_gods:
                            return g
                return c[0]
            # Last resort fallback
            return "Chauntea" if ("verte" in msub or "green" in msub) else "Mystra"
        return "None"

    # Weighted random selection: rank-1 gods dominate over rank-20
    total = sum(weights.values())
    r = random.uniform(0, total)
    upto = 0.0
    for god, w in sorted(weights.items(), key=lambda x: -x[1]):
        upto += w
        if r <= upto:
            return god

    result = max(weights, key=weights.get)

    # Ultimate safety net for Théurgique (should rarely be reached)
    if mtype == "théurgique" and (not result or result == "None"):
        c = eth_list or reg_list
        if c:
            if "verte" in msub or "green" in msub or "nature" in msub:
                for g in c:
                    if g in nature_gods:
                        return g
            return c[0]
        return "Silvanus" if ("verte" in msub or "green" in msub or "nature" in msub) else "Chauntea"

    return result


# ====================== SECONDARY ATTRIBUTES ======================
def sec_func(x: float) -> float:
    """Points de capacités secondaires (exponentiel)"""
    return round(6 * (math.exp(0.085 * x) - 1), 2)


# ====================== COMMENTAIRES ======================
"""
RÈGLES ACTUELLES (calibrées)

- MAGIC_THRESHOLD     = -1.5   → ~50% de personnages magiquement actifs
  (seuil sur Combat_Points : si >= seuil → non-magique)
- ARCANIST_THRESHOLD  = -7.0   → ~20% des personnages les plus faibles (les plus négatifs en CP) sont Arcanistes
- Skill Modifier      = combat_malus + secondary_malus (tous positifs = malus)

Pour ajuster le % de magiques, modifier MAGIC_THRESHOLD et relancer des simulations
via generate_character pour vérifier la distribution des Combat_Points.
"""