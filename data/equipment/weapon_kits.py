"""
data/equipment/weapon_kits.py

Gestion des "Kits d'armes et boucliers" (nouvelle Phase 1 du protocole d'équipement).

Fichier source : kits_armes_et_boucliers.txt
Logique : Toujours prendre le kit le plus cher que le personnage peut s'offrir.
"""

import re
import random
from pathlib import Path
from typing import List, Dict, Optional

BASE_DIR = Path(__file__).parent
KITS_FILE = BASE_DIR / "systeme armure preconstruites" / "kits_armes_et_boucliers.txt"


def _parse_weapon_kits() -> List[Dict]:
    """
    Parse le fichier kits_armes_et_boucliers.txt
    Retourne une liste de dicts triée par prix décroissant.
    """
    if not KITS_FILE.exists():
        raise FileNotFoundError(f"Fichier introuvable : {KITS_FILE}")

    kits = []
    text = KITS_FILE.read_text(encoding="utf-8")

    # Pattern pour capturer les kits : "123. 12.5 sp : Description [Enc: X]"
    # Le numéro au début est optionnel dans certaines extensions
    pattern = re.compile(
        r'^\s*\d*\.?\s*(?P<price>\d+\.\d+)\s*sp\s*:\s*(?P<description>.+?)\s*\[Enc:\s*(?P<enc>\d+)\s*\]',
        re.IGNORECASE
    )

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("=") or line.startswith("TRANCHE") or line.startswith("CATALOGUE") or line.startswith("RÈGLES"):
            continue

        match = pattern.search(line)
        if match:
            price_sp = float(match.group("price"))
            description = match.group("description").strip()
            enc = int(match.group("enc"))

            # Parse individual items in the kit
            components = [c.strip() for c in description.split('+')]

            # Detect shoulder weapons (based on user's rules)
            shoulder_keywords = [
                'longsword', 'espadon', 'zweihander', 'poleaxe', 'halberd', 
                'glaive', 'bill', 'pike', 'lucerne', 'guisarme', 'billhook',
                'heavy crossbow', 'longbow', 'composite bow', 'staff sling',
                'war scythe'
            ]
            shoulder_items = []
            for comp in components:
                comp_lower = comp.lower()
                if any(kw in comp_lower for kw in shoulder_keywords):
                    shoulder_items.append(comp)

            category = _categorize_kit(description)

            kits.append({
                "name": description,
                "price_sp": price_sp,
                "price_bp": round(price_sp * 10, 1),
                "encumbrance": enc,
                "components": components,
                "shoulder_weapons": shoulder_items,
                "has_too_many_shoulder": len(shoulder_items) > 1,
                "category": category,
                "raw_line": line
            })

    # Trier par prix décroissant (le plus cher en premier)
    kits.sort(key=lambda x: x["price_sp"], reverse=True)
    return kits


_KITS_CACHE: Optional[List[Dict]] = None


def get_all_weapon_kits() -> List[Dict]:
    """Retourne tous les kits d'armes+boucliers, triés du plus cher au moins cher."""
    global _KITS_CACHE
    if _KITS_CACHE is None:
        _KITS_CACHE = _parse_weapon_kits()
    return _KITS_CACHE


def get_most_expensive_affordable_weapon_kit(budget_sp: float) -> Optional[Dict]:
    """
    Retourne le kit d'armes + bouclier le plus cher que le personnage peut s'offrir.
    (Ancienne logique - conservée pour compatibilité)
    """
    if budget_sp <= 0:
        return None

    all_kits = get_all_weapon_kits()

    for kit in all_kits:
        if kit["price_sp"] <= budget_sp:
            return kit.copy()

    return None


def get_weighted_category_weapon_kit(budget_sp: float) -> Optional[Dict]:
    """
    Nouvelle logique demandée par l'utilisateur :

    1. Tire au hasard une catégorie avec les probabilités :
       - large_shield : 50%
       - polearm      : 25%
       - bow          : 12.5%
       - crossbow     : 12.5%

    2. Parmi les kits de cette catégorie que le personnage peut s'offrir,
       prend le plus cher possible.

    Si aucun kit de la catégorie tirée n'est abordable → fallback sur le kit
    le plus cher globalement abordable.
    """
    if budget_sp <= 0:
        return None

    all_kits = get_all_weapon_kits()
    if not all_kits:
        return None

    # Définir les catégories et leurs poids
    categories = ["large_shield", "polearm", "bow", "crossbow"]
    weights = [50, 25, 12.5, 12.5]   # 50% + 25% + 12.5% + 12.5% = 100%

    # On tire une catégorie
    chosen_category = random.choices(categories, weights=weights, k=1)[0]

    # Filtrer les kits de cette catégorie
    category_kits = [k for k in all_kits if k.get("category") == chosen_category]

    # Parmi ceux abordables dans cette catégorie, prendre le plus cher
    affordable_in_category = [k for k in category_kits if k["price_sp"] <= budget_sp]

    if affordable_in_category:
        # Trier par prix décroissant et prendre le premier
        affordable_in_category.sort(key=lambda x: x["price_sp"], reverse=True)
        return affordable_in_category[0].copy()

    # Fallback : aucun kit de cette catégorie n'est abordable
    # → on prend le kit le plus cher possible globalement
    return get_most_expensive_affordable_weapon_kit(budget_sp)


def get_weapon_kits_within_budget(budget_sp: float) -> List[Dict]:
    """Retourne tous les kits que le personnage peut s'offrir (pour debug)."""
    if budget_sp <= 0:
        return []
    return [k.copy() for k in get_all_weapon_kits() if k["price_sp"] <= budget_sp]


def get_violating_kits() -> List[Dict]:
    """Retourne les kits qui violent la règle 'max 1 arme à l'épaule'."""
    return [k for k in get_all_weapon_kits() if k.get("has_too_many_shoulder", False)]


def _categorize_kit(description: str) -> str:
    """
    Catégorise un kit selon les priorités demandées par l'utilisateur :
    - crossbow (arbalette)
    - bow (arc)
    - polearm
    - large_shield
    """
    desc = description.lower()

    # Priorité 1 : Crossbow / Arbalette
    if any(x in desc for x in ['heavy crossbow', 'crossbow']):
        return "crossbow"

    # Priorité 2 : Bow / Arc
    if any(x in desc for x in ['longbow', 'composite bow', 'short bow']):
        return "bow"

    # Priorité 3 : Polearms (hast lourdes)
    polearm_keywords = [
        'halberd', 'poleaxe', 'glaive', 'bill', 'billhook',
        'pike', 'lucerne', 'guisarme', 'war scythe'
    ]
    if any(kw in desc for kw in polearm_keywords):
        return "polearm"

    # Priorité 4 : Large Shields
    large_shield_keywords = [
        'infantry pavise', 'pavise', 'kite shield', 'heater shield',
        'large buckler', 'grand bouclier rond', 'large shield'
    ]
    if any(kw in desc for kw in large_shield_keywords):
        return "large_shield"

    # Fallback pour les kits avec boucliers moyens mais sans les catégories ci-dessus
    if 'target shield' in desc or 'heater shield' in desc:
        return "large_shield"

    return "other"


if __name__ == "__main__":
    print("=== Test du nouveau module Weapon Kits ===\n")
    kits = get_all_weapon_kits()
    print(f"Nombre total de kits chargés : {len(kits)}")

    violating = get_violating_kits()
    print(f"Kits violant la règle 'max 1 arme à l\\'épaule' : {len(violating)}\n")

    if violating:
        print("Exemples de kits à corriger :")
        for v in violating[:5]:
            print(f"  {v['price_sp']:>5} sp : {v['name'][:60]}  → {len(v['shoulder_weapons'])} shoulder weapons")

    print("\n--- Test sélection 'plus cher possible' (ancienne logique) ---")
    test_budgets = [5, 12, 25, 45]
    for budget in test_budgets:
        kit = get_most_expensive_affordable_weapon_kit(budget)
        if kit:
            print(f"Budget {budget:>5} sp -> {kit['name'][:55]} ({kit['price_sp']} sp)")
        else:
            print(f"Budget {budget:>5} sp → Aucun kit")

    print("\n--- Test nouvelle logique pondérée par catégorie ---")
    for budget in [8, 15, 30, 50]:
        kit = get_weighted_category_weapon_kit(budget)
        if kit:
            print(f"Budget {budget:>5} sp -> [{kit.get('category', '?')}] {kit['name'][:50]} ({kit['price_sp']} sp)")
        else:
            print(f"Budget {budget:>5} sp → Aucun kit")
