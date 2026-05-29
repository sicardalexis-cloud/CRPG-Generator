"""
data/equipment/remaining_equipment.py

Logique d'achat avec le capital restant après l'armure (nouvelle phase).

Règles actuelles (utilisateur) :
- Tirage au hasard des boucliers + armes dans la limite d'encombrement.
- Pas d'armes en double (sauf javelots).
- Si argent reste → achat d'une monture au hasard parmi celles abordables.
- Ensuite, on peut continuer à acheter des armes grâce à la monture.
- Si très peu d'argent après armure (+ monture) → le perso se contente du gourdin gratuit du kit.
"""

import random
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# =============================================================================
# CONFIG
# =============================================================================

BASE_DIR = Path(__file__).parent
WEAPONS_FILE = BASE_DIR / "systeme armure preconstruites" / "liste_armes_communes_eau_profonde.txt"

# Puissance de la pondération par Fréquence.
# Plus cette valeur est élevée, plus les objets très fréquents (9-10) sont favorisés
# par rapport aux objets rares (1-4).
#   1.0 = linéaire (choix presque uniforme parmi les objets abordables)
#   2.0 = déjà nettement plus fort
#   3.0 = très fort (recommandé si tu veux que les objets courants dominent fortement)
#   4.0 = extrême (presque uniquement les objets les plus fréquents)
WEAPON_FREQUENCY_EXPONENT = 3.0

# =============================================================================
# PARSING DU FICHIER ARMES + BOUCLIERS
# =============================================================================

def _parse_weapons_file() -> List[Dict]:
    """
    Parse le fichier et retourne une liste de dicts avec :
    - name
    - price_sp / price_bp
    - frequence (1-10) → pour pondérer les tirages
    - encumbrance (si présent) → pour les règles de port
    """
    if not WEAPONS_FILE.exists():
        raise FileNotFoundError(f"Fichier introuvable : {WEAPONS_FILE}")

    items = []
    current_category = "Other"

    text = WEAPONS_FILE.read_text(encoding="utf-8")

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Catégories
        if line.startswith("BOUCLIERS"):
            current_category = "Shield"
            continue
        elif line.startswith("COUTEAUX") or line.startswith("ÉPÉES"):
            current_category = "Melee"
            continue
        elif "HAST" in line or "PIQUES" in line:
            current_category = "Polearm"
            continue
        elif "CONTONDANTES" in line or "CLUBS" in line:
            current_category = "Blunt"
            continue
        elif line.startswith("HACHES"):
            current_category = "Axe"
            continue
        elif "DISTANCE" in line:
            current_category = "Ranged"
            continue
        elif "PAYSANNES" in line:
            current_category = "Melee"
            continue
        elif line.startswith("=") or line.startswith("LISTE") or line.startswith("FIN"):
            continue

        # Nouveau format : "... 3 sp    Fréquence: 8   Encombrement: 1"
        match = re.search(
            r'^(?P<name>.+?)\s+(?P<price>\d+(?:\.\d+)?)\s*sp\s+.*Fréquence:\s*(?P<freq>\d+).*?Encombrement:\s*(?P<enc>\d+)',
            line,
            re.IGNORECASE
        )

        if not match:
            # Fallbacks
            match = re.search(
                r'^(?P<name>.+?)\s+(?P<price>\d+(?:\.\d+)?)\s*sp\s+.*Fréquence:\s*(?P<freq>\d+)',
                line,
                re.IGNORECASE
            )
            if not match:
                match = re.match(
                    r'^(?P<name>.+?)\s+(?P<price>\d+(?:\.\d+)?)\s*sp\s+(?P<enc>\d+)$',
                    line
                )

        if match:
            name = match.group("name").strip()
            price_sp = float(match.group("price"))
            freq = int(match.group("freq")) if match.lastgroup and match.group("freq") else 5
            enc = int(match.group("enc")) if match.lastgroup and match.group("enc") else 3

            # Parse new columns: Stockage and Monté (robust to encoding issues)
            stockage = "porte"
            low = line.lower()
            if "stockage:" in low:
                if "epaule" in low or "\u00e9paule" in low:
                    stockage = "epaule"   # normalized without accent
                elif "porte" in low:
                    stockage = "porte"

            monte = False
            if "monté:" in low or "monte:" in low:
                if "oui" in low or "cavalerie" in low:
                    monte = True

            items.append({
                "name": name,
                "price_sp": price_sp,
                "price_bp": round(price_sp * 10, 1),
                "frequence": freq,
                "encumbrance": enc,
                "stockage": stockage,      # "porté" ou "épaule"
                "monte": monte,            # True si "arme de cavalerie"
                "category": current_category
            })

    return items


_WEAPONS_CACHE: Optional[List[Dict]] = None


def get_all_weapons_and_shields() -> List[Dict]:
    global _WEAPONS_CACHE
    if _WEAPONS_CACHE is None:
        _WEAPONS_CACHE = _parse_weapons_file()
    return _WEAPONS_CACHE


def get_shields() -> List[Dict]:
    return [i for i in get_all_weapons_and_shields() if i["category"] == "Shield"]


def get_weapons() -> List[Dict]:
    return [i for i in get_all_weapons_and_shields() if i["category"] != "Shield"]


# =============================================================================
# RÈGLES D'ENCOMBREMENT (simplifiées pour cette phase)
# =============================================================================

def can_carry_item(current_enc: int, item_enc: int, has_mount: bool, heavy_count: int) -> bool:
    """
    Règles d'encombrement classiques :
    - Sans monture : max 7 points pour les items normaux.
    - Max 1 arme lourde (enc >= 4) sans monture.
    - Les armes lourdes ne comptent pas dans les 7 points.
    - Avec monture : beaucoup plus de liberté.
    """
    if has_mount:
        return True

    if item_enc >= 4:
        # Arme lourde
        return heavy_count < 1
    else:
        # Arme normale
        return (current_enc + item_enc) <= 7


def select_random_shield_and_weapons(
    budget_bp: float,
    has_mount: bool = False,
    shoulder_count: int = 0,
    max_attempts: int = 50
) -> Tuple[List[Dict], float, int]:
    """
    Sélectionne au hasard 1 bouclier + des armes en respectant :
    - le budget
    - l'encombrement
    - la règle "épaule" (max 1 sans monture)
    - les armes de cavalerie (uniquement si has_mount)
    - pondération par Fréquence (très forte)

    Retourne (liste_items, argent_dépensé_bp, nouveau_shoulder_count)
    """
    all_items = get_all_weapons_and_shields()
    shields = get_shields()
    weapons = get_weapons()

    if budget_bp <= 50:
        return [], 0.0, shoulder_count

    selected = []
    spent = 0.0
    current_enc = 0
    heavy_count = 0
    owned_names = set()
    current_shoulder = shoulder_count

    # 1. Bouclier
    affordable_shields = [
        s for s in shields
        if s["price_bp"] <= budget_bp
        and can_carry_item(current_enc, s["encumbrance"], has_mount, heavy_count)
    ]
    if affordable_shields:
        weights = [s.get("frequence", 5) ** WEAPON_FREQUENCY_EXPONENT for s in affordable_shields]
        shield = random.choices(affordable_shields, weights=weights, k=1)[0]
        selected.append(shield)
        spent += shield["price_bp"]
        current_enc += shield["encumbrance"]
        owned_names.add(shield["name"])

    # 2. Armes (avec toutes les nouvelles règles)
    attempts = 0
    while attempts < max_attempts:
        attempts += 1

        affordable = []
        for w in weapons:
            if w["name"] in owned_names:
                continue
            if w["price_bp"] > (budget_bp - spent):
                continue

            # Règle "arme de cavalerie"
            if w.get("monte", False) and not has_mount:
                continue

            # Règle "épaule" : max 1 sans monture
            if w.get("stockage") == "epaule" and not has_mount and current_shoulder >= 1:
                continue

            if not can_carry_item(current_enc, w["encumbrance"], has_mount, heavy_count):
                continue

            affordable.append(w)

        if not affordable:
            break

        weights = [item.get("frequence", 5) ** WEAPON_FREQUENCY_EXPONENT for item in affordable]
        candidate = random.choices(affordable, weights=weights, k=1)[0]

        enc = candidate["encumbrance"]
        is_heavy = enc >= 4
        is_shoulder = candidate.get("stockage") == "epaule"

        selected.append(candidate)
        spent += candidate["price_bp"]
        owned_names.add(candidate["name"])

        if is_heavy:
            heavy_count += 1
        else:
            current_enc += enc

        if is_shoulder:
            current_shoulder += 1

    return selected, round(spent, 1), current_shoulder


def select_random_mount(budget_bp: float) -> Optional[Dict]:
    """Choisit une monture au hasard parmi celles que le perso peut payer."""
    # Liste simple de montures (on peut l'enrichir plus tard)
    mounts = [
        {"name": "Rouncey", "price_bp": 450},
        {"name": "Mule", "price_bp": 400},
        {"name": "Pony", "price_bp": 400},
        {"name": "Courser", "price_bp": 620},
        {"name": "Palfrey", "price_bp": 570},
    ]

    affordable = [m for m in mounts if m["price_bp"] <= budget_bp]
    if not affordable:
        return None

    return random.choice(affordable)


# =============================================================================
# FONCTION PRINCIPALE DE LA PHASE
# =============================================================================

def buy_remaining_equipment(
    remaining_bp: float,
    seed: Optional[int] = None
) -> Dict:
    """
    Logique complète pour le capital restant après l'armure.
    Gère correctement :
    - Armes de cavalerie (seulement après monture)
    - Armes "épaule" (max 1 sans monture)
    - Pondération forte par Fréquence
    """
    if seed is not None:
        random.seed(seed)

    purchases = []
    total_spent = 0.0
    has_mount = False
    shoulder_count = 0

    # Phase 1 : Bouclier + armes (avant monture)
    weapons_and_shield, spent1, shoulder_count = select_random_shield_and_weapons(
        remaining_bp, has_mount=False, shoulder_count=shoulder_count
    )
    purchases.extend(weapons_and_shield)
    total_spent += spent1
    remaining_bp -= spent1

    # Phase 2 : Monture si argent reste
    if remaining_bp > 300:
        mount = select_random_mount(remaining_bp)
        if mount:
            purchases.append({
                "name": mount["name"],
                "price_bp": mount["price_bp"],
                "category": "Mount"
            })
            total_spent += mount["price_bp"]
            remaining_bp -= mount["price_bp"]
            has_mount = True

    # Phase 3 : Encore des armes après avoir une monture (peut prendre cavalerie + plusieurs épaule)
    if has_mount and remaining_bp > 100:
        extra, spent_extra, _ = select_random_shield_and_weapons(
            remaining_bp, has_mount=True, shoulder_count=shoulder_count
        )
        purchases.extend(extra)
        total_spent += spent_extra
        remaining_bp -= spent_extra

    return {
        "purchases": purchases,
        "total_spent_bp": round(total_spent, 1),
        "final_remaining_bp": round(max(0, remaining_bp), 1),
        "has_mount": has_mount
    }
