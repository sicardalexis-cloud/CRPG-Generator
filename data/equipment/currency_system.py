"""
data/equipment/currency_system.py

Nouveau système monétaire unifié (proposé par l'utilisateur).

Règles :
- Toutes les pièces physiques pèsent exactement **1/4 once** (0.25 oz).
- Le système est décimal : chaque pièce vaut 10 fois la précédente.
- La valeur vient du métal, pas du poids.

Hiérarchie :
1 mithril piece (mp) = 10 pp
1 platinum piece (pp) = 10 gp
1 gold piece     (gp) = 10 sp
1 silver piece   (sp) = 10 bp
1 bronze piece   (bp) = 10 cp
1 copper piece   (cp) = 10 tp
1 tin piece      (tp) = 10 iron pieces (ip)

Pour les calculs historiques (basés sur le poids d'argent) :
- On utilise la **silver piece (sp)** comme référence.
- 1 sp = 1/4 once d'argent pur.
"""

from typing import Dict

# =============================================================================
# DÉFINITION DU SYSTÈME
# =============================================================================

COIN_HIERARCHY = [
    ("mp", "mithril piece", 1000000),   # 1 mp = 1 000 000 sp
    ("pp", "platinum piece", 100000),   # 1 pp = 100 000 sp
    ("gp", "gold piece",     10000),    # 1 gp = 10 000 sp
    ("sp", "silver piece",   1000),     # 1 sp = 1 000 sp (base de référence pour l'argent)
    ("bp", "bronze piece",   100),      # 1 bp = 100 sp
    ("cp", "copper piece",   10),       # 1 cp = 10 sp
    ("tp", "tin piece",      1),        # 1 tp = 1 sp
    ("ip", "iron piece",     0.1),      # 1 ip = 0.1 sp
]

# Poids d'une pièce (toutes les pièces font le même poids physique)
COIN_WEIGHT_OZ = 0.25   # 1/4 once

# =============================================================================
# CONVERSION HISTORIQUE (basée sur le poids d'argent)
# =============================================================================

# 1 once = 28.349523125 grammes
OZ_TO_GRAMS = 28.349523125

def kg_silver_to_sp(kg: float) -> float:
    """
    Convertit un poids en kg d'argent pur en nombre de Silver Pieces (sp).
    
    1 sp = 1/4 once d'argent = 0.25 oz
    1 kg = 1000 g
    1 oz = 28.349523125 g
    """
    ounces = kg * 1000 / OZ_TO_GRAMS
    sp = ounces / COIN_WEIGHT_OZ
    return sp

def sp_to_kg_silver(sp: float) -> float:
    """Convertit des Silver Pieces en kg d'argent pur."""
    ounces = sp * COIN_WEIGHT_OZ
    kg = ounces * OZ_TO_GRAMS / 1000
    return kg

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def format_currency(amount_sp: float) -> str:
    """
    Formate un montant en silver pieces dans le système décimal le plus lisible.
    Ex: 2450 sp → 2 gp 4 sp 5 bp
    """
    if amount_sp >= 10000:
        gp = int(amount_sp // 10000)
        rest = amount_sp % 10000
        if rest == 0:
            return f"{gp} gp"
        return f"{gp} gp + {format_currency(rest)}"

    if amount_sp >= 1000:
        sp = int(amount_sp // 1000)
        rest = amount_sp % 1000
        if rest == 0:
            return f"{sp} sp"
        return f"{sp} sp + {format_currency(rest)}"

    if amount_sp >= 100:
        bp = int(amount_sp // 100)
        rest = amount_sp % 100
        if rest == 0:
            return f"{bp} bp"
        return f"{bp} bp + {format_currency(rest)}"

    if amount_sp >= 10:
        cp = int(amount_sp // 10)
        rest = amount_sp % 10
        if rest == 0:
            return f"{cp} cp"
        return f"{cp} cp + {format_currency(rest)}"

    if amount_sp >= 1:
        tp = int(amount_sp // 1)
        rest = amount_sp % 1
        if rest < 0.1:
            return f"{tp} tp"
        ip = int(round(rest * 10))
        return f"{tp} tp + {ip} ip"

    # Moins d'1 tp
    ip = round(amount_sp * 10, 1)
    return f"{ip} ip"

# Exemple de test
if __name__ == "__main__":
    print("=== Test du système monétaire ===\n")
    
    # Exemple : une armure qui valait 2 kg d'argent
    kg = 2.0
    sp_value = kg_silver_to_sp(kg)
    print(f"{kg} kg d'argent pur = {sp_value:.1f} sp")
    print(f"Format : {format_currency(sp_value)}")
    print()
    
    # Test de formatage
    test_values = [2450, 175, 42.5, 3.8, 0.7]
    for v in test_values:
        print(f"{v:6.1f} sp → {format_currency(v)}")
