"""
data/equipment/armor_sets.py

Nouveau système d'armures préconstruites (sets historiques réalistes).

Source de vérité :
premier-tests-grokvsc/data/equipment/systeme armure preconstruites/Sets_Armures.txt

Règle actuelle (demande utilisateur) :
- Un personnage peut consacrer jusqu'à 70% de son capital de départ à l'armure.
- Il prend **le set le plus cher** qu'il peut s'offrir avec ce budget.
- Le kit de base reste gratuit.
"""

from pathlib import Path
from typing import List, Dict, Optional
import re

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(__file__).parent
ARMOR_SETS_FILE = BASE_DIR / "systeme armure preconstruites" / "Sets_Armures.txt"


# =============================================================================
# PARSING
# =============================================================================

def _parse_armor_sets_file() -> List[Dict]:
    """
    Parse le fichier Sets_Armures.txt et retourne une liste de sets triés
    par prix décroissant (du plus cher au moins cher).
    """
    if not ARMOR_SETS_FILE.exists():
        raise FileNotFoundError(f"Fichier introuvable : {ARMOR_SETS_FILE}")

    sets = []
    text = ARMOR_SETS_FILE.read_text(encoding="utf-8")

    # Pattern : "123 sp - Nom du set"
    pattern = re.compile(r'^\s*(\d+(?:\.\d+)?)\s*sp\s*-\s*(.+?)\s*$', re.IGNORECASE)

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        match = pattern.match(line)
        if match:
            price_sp = float(match.group(1))
            name = match.group(2).strip()

            sets.append({
                "name": name,
                "price_sp": price_sp,
                "price_bp": round(price_sp * 10, 1)   # Conversion en bp (unité interne)
            })

    # Trier par prix décroissant (le plus cher en premier)
    sets.sort(key=lambda x: x["price_sp"], reverse=True)
    return sets


# Cache simple (le fichier ne change pas souvent)
_ARMOR_SETS_CACHE: Optional[List[Dict]] = None


def get_all_armor_sets() -> List[Dict]:
    """Retourne tous les sets d'armure, triés du plus cher au moins cher."""
    global _ARMOR_SETS_CACHE
    if _ARMOR_SETS_CACHE is None:
        _ARMOR_SETS_CACHE = _parse_armor_sets_file()
    return _ARMOR_SETS_CACHE


def get_most_expensive_affordable_set(budget_sp: float) -> Optional[Dict]:
    """
    Retourne le set d'armure le plus cher que le personnage peut s'offrir
    avec le budget donné (en sp).

    Règle utilisateur : on prend **le plus cher possible**.
    """
    if budget_sp <= 0:
        return None

    all_sets = get_all_armor_sets()

    for armor_set in all_sets:
        if armor_set["price_sp"] <= budget_sp:
            return armor_set.copy()

    # Si même le set le moins cher est trop cher
    return None


def get_armor_sets_within_budget(budget_sp: float) -> List[Dict]:
    """Retourne tous les sets que le personnage peut s'offrir (pour debug ou choix futur)."""
    if budget_sp <= 0:
        return []

    all_sets = get_all_armor_sets()
    return [s.copy() for s in all_sets if s["price_sp"] <= budget_sp]


# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def calculate_armor_budget(starting_capital_bp: float, percentage: float = 0.70) -> float:
    """
    Calcule le budget maximum allouable à l'armure.
    Par défaut : 70% du capital de départ (règle utilisateur actuelle).
    """
    if starting_capital_bp <= 0:
        return 0.0
    return starting_capital_bp * percentage / 10.0   # Retourne en sp


def format_armor_set(armor_set: Dict) -> str:
    """Joli affichage d'un set."""
    if not armor_set:
        return "Aucune armure"
    return f"{armor_set['name']} ({armor_set['price_sp']:.0f} sp)"


# =============================================================================
# TEST / DEBUG
# =============================================================================

if __name__ == "__main__":
    print("=== Test du nouveau système d'armures préconstruites ===\n")

    all_sets = get_all_armor_sets()
    print(f"Nombre total de sets chargés : {len(all_sets)}")
    print(f"Set le moins cher : {all_sets[-1]['name']} ({all_sets[-1]['price_sp']} sp)")
    print(f"Set le plus cher  : {all_sets[0]['name']} ({all_sets[0]['price_sp']} sp)\n")

    # Exemples de budget
    test_budgets = [50, 120, 180, 250, 400, 700]

    for budget in test_budgets:
        chosen = get_most_expensive_affordable_set(budget)
        print(f"Budget {budget:>4} sp -> {format_armor_set(chosen)}")
