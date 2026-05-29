"""
data/equipment/faerun_regional_kits.py

Système de kits d'aventurier de base par région pour les Royaumes Oubliés.

Règle stricte :
- On utilise UNIQUEMENT les objets et les prix des fichiers fournis dans data/equipment/
- On conserve la monnaie Rolemaster (tp, cp, bp, sp, gp, pp) telle quelle.
- Pas de conversion en pièces d'or D&D.

Niveaux technologiques supportés (basés sur les fichiers disponibles) :
- Stone Age
- Copper Age
- Bronze Age
- Iron Age
- Middle Ages
- Renaissance

Pour les régions "entre deux niveaux", on crée des kits hybrides spécifiques.
"""

from typing import Dict, List, Tuple

# =============================================================================
# KITS PAR NIVEAU TECHNOLOGIQUE (basés sur les fichiers fournis)
# =============================================================================

# Chaque kit contient une liste d'objets avec leur prix exact du fichier source.

# =============================================================================
# STONE AGE BASIC ADVENTURER KIT (Great Glacier & régions équivalentes)
# =============================================================================
# Construit exclusivement à partir de Stone_Age_Equipment_List.txt
# Monnaie : Rolemaster (tp, cp, bp, sp, gp)
# Adapté pour un personnage Ulutiun / peuple du Grand Glacier

STONE_AGE_BASIC_KIT: List[Tuple[str, str]] = [
    # === SURVIE & TRANSPORT (Outdoor Survival) ===
    ("Backpack, large leather", "7 bp"),
    ("Fire-starting bow", "5 bp"),
    ("Sleeping furs, heavy", "75 cp+"),
    ("Waterskin (full, 1 gal)", "3 bp"),
    ("Torch x6", "6 tp"),
    ("Fishhook & line", "2 tp"),
    ("Fish Trap", "3 bp"),

    # === VÊTEMENTS & PROTECTION CONTRE LE FROID (très important) ===
    ("Cloak, fur", "25 bp"),
    ("Hat, fur", "3 bp"),
    ("Gloves, fur lined", "4 bp"),
    ("Coat, leather", "18 bp"),
    ("Pants, leather", "13 bp"),
    ("Soft boots, leather", "3-5 sp"),
    ("Heavy furs (Mammoth/Bear)", "12 sp"),   # Isolation extrême

    # === ARMES (chasseur/guerrier Stone Age) ===
    ("Spear", "23 bp"),
    ("Axe", "2 sp"),
    ("Short bow", "6 sp"),
    ("Arrows (20)", "4 bp"),
    ("Harpoon", "25 bp"),                     # Très pertinent pour le Grand Glacier
    ("Dagger, obsidian", "3 sp"),

    # === ARMURE (uniquement cuir / peaux) ===
    ("Leather jerkin", "1 sp"),
    ("Target shield", "35 bp"),               # Optionnel mais présent
]

# Exemple de kit hybride "Early Iron Age" (pour régions entre Stone Age et Iron Age)
# On mélange des objets Stone Age + premiers objets en métal de l'Iron Age
EARLY_IRON_AGE_KIT: List[Tuple[str, str]] = [
    # Base Stone Age (survie + vêtements)
    ("Backpack, large leather", "7 bp"),
    ("Sleeping furs, heavy", "75 cp+"),
    ("Waterskin (full, 1 gal)", "3 bp"),
    ("Cloak, fur", "25 bp"),
    ("Coat, leather", "18 bp"),
    ("Pants, leather", "13 bp"),
    ("Soft boots, leather", "3-5 sp"),

    # Améliorations Early Iron
    ("Fire-starting bow", "5 bp"),           # encore Stone Age
    ("Axe (Iron Age version)", "2 sp"),      # du Iron Age list
    ("Spear (Iron Age)", "23 bp"),
    ("Leather jerkin", "1 sp"),
    ("Target shield", "35 bp"),

    # Ajouts typiques Early Iron (à extraire du Iron Age list plus tard)
    # Pour l'instant on reste conservateur
]

# =============================================================================
# MAPPING RÉGION → KIT
# =============================================================================

# Pour l'instant on commence avec les régions clairement Stone Age ou très proches.

REGION_KIT_MAPPING: Dict[str, str] = {
    # === PURE STONE AGE ===
    "Great Glacier": "stone_age",
    "Glacière éternelle": "stone_age",

    # === EARLY IRON / HYBRID (à affiner plus tard) ===
    "Icewind Dale": "early_iron",
    "Spine of the World": "early_iron",

    # Fallback pour le moment
    "Default": "middle_ages",   # temporaire, on affinera
}

# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def get_kit_for_region(region_name: str) -> List[Tuple[str, str]]:
    """Retourne le kit d'équipement pour une région donnée."""
    kit_type = REGION_KIT_MAPPING.get(region_name, REGION_KIT_MAPPING["Default"])

    if kit_type == "stone_age":
        return STONE_AGE_KIT
    elif kit_type == "early_iron":
        return EARLY_IRON_AGE_KIT
    else:
        # Pour l'instant on renvoie un kit vide en attendant les autres niveaux
        return []


def calculate_kit_cost_in_source_currency(region_name: str) -> str:
    """
    Calcule le coût total du kit dans la monnaie du fichier source.
    Retourne une estimation textuelle (car les prix contiennent parfois des '+').
    """
    kit = get_kit_for_region(region_name)
    if not kit:
        return "Aucun kit défini"

    # Pour l'instant on affiche juste les items + prix bruts
    # Un vrai calcul de somme sera fait plus tard quand on aura nettoyé les prix
    total_items = len(kit)
    return f"{total_items} items (calcul précis à venir après normalisation des prix)"


if __name__ == "__main__":
    print("=== Test du nouveau système de kits (source pure) ===\n")

    test_regions = [
        "Great Glacier",
        "Icewind Dale",
        "Spine of the World",
    ]

    for region in test_regions:
        kit = get_kit_for_region(region)
        cost = calculate_kit_cost_in_source_currency(region)

        print(f"Région : {region}")
        print(f"  Type de kit : {REGION_KIT_MAPPING.get(region, 'Default')}")
        print(f"  Nombre d'items : {len(kit)}")
        print(f"  Coût (monnaie source) : {cost}")
        print("  Contenu :")
        for name, price in kit[:8]:   # on affiche les 8 premiers pour la lisibilité
            print(f"    - {name}: {price}")
        if len(kit) > 8:
            print(f"    ... (+ {len(kit)-8} autres items)")
        print()
