"""
analyze_top_weapon_per_char.py

Analyse demandée :
Pour chaque personnage généré :
  - Regarde TOUT son inventaire d'armes (kit universel + achats post-kit)
  - Identifie l'arme la plus chère qu'il possède (prix réel payé : final_price_sp avec surcoût pour les post-kit)
  - Puis, sur un grand échantillon, donne les 10 armes "les plus chères du perso" les plus fréquentes (en %)

Règles :
- On ne compte que les armes offensives (pas les boucliers, pas les armures).
- Prix post-kit = prix avec surcharge Rare/Très rare du groupe.
- Le Bâton de marche du kit est très bon marché (~0.4 sp) et sera rarement l'arme la plus chère.
"""

import random
from collections import Counter
from datetime import datetime
from typing import Optional, Tuple

from utils import generate_character
from data.equipment import post_kit_purchases as post_kit
from data.equipment import group_equipment_pools
from data.equipment import regional_adventurer_kits as kits

# =============================================================================
# FILTRE "ARME OFFENSIVE"
# =============================================================================

ARMOR_KEYWORDS = [
    "breastplate", "hauberk", "brigandine", "gambeson", "plackart",
    "coat of plates", "jack of plates", "haubergeon", "chain hauberk",
    "lorica", "byrnie", "cuirasse", "armure",
    "helmet", "helm", "bascinet", "sallet", "armet", "burgonet", "great helm",
    "spangenhelm", "nasal", "cerveliere", "morion", "kettle hat", "close helmet",
    "gauntlet", "vambrace", "couter", "pauldrons", "greaves", "cuisses",
    "poleyns", "sabatons", "tassets", "fauld", "gorget", "bevor", "aventail",
    "mail coif", "coif", "voiders", "rerebrace", "brassards"
]

def is_offensive_weapon(name: str) -> bool:
    """
    Retourne True si l'item est une arme offensive (épée, hache, arc, arbalète,
    lance, javelot, masse, fléau, pique, arbalète, mousquet, etc.).
    Exclut explicitement :
    - les boucliers
    - les pièces d'armure (torse, tête, membres)
    """
    if not name:
        return False

    n = name.lower()

    # Exclusions claires
    if post_kit.is_shield(name):
        return False
    if any(kw in n for kw in ARMOR_KEYWORDS):
        return False

    # Utilise la fonction existante qui détecte bien les armes
    if not post_kit.is_weapon_or_armor(name):
        return False

    # Mots-clés positifs pour les armes (très large)
    weapon_keywords = [
        "sword", "épée", "blade", "sabre", "shamshir", "rapier", "sidesword",
        "estoc", "cutlass", "broadsword", "gladius", "spatha", "xiphos",
        "axe", "hache", "battle axe", "bearded axe", "dane axe", "great axe",
        "lochaber", "poleaxe", "halberd", "bill", "glaive", "voulge",
        "bec de corbin", "lucerne", "military fork", "ranseur", "partisan",
        "mace", "masse", "flanged mace", "morning star", "flail", "fléau",
        "war hammer", "marteau", "maul",
        "spear", "lance", "pike", "javelin", "javelot", "pilum", "verutum",
        "dory", "boar spear", "harpoon",
        "bow", "arc", "longbow", "short bow", "composite bow", "crossbow", "arbalète",
        "cranequin", "handgonne", "arquebus", "musket", "blunderbuss",
        "pistol", "handgonne", "wheellock", "flintlock",
        "dagger", "main-gauche", "seax", "rondel", "knife", "couteau",
        "staff", "bâton", "quarterstaff", "baton", "club", "gourdin", "cudgel",
        "sling", "fronde", "atlatl", "francisca", "throwing", "plumbata",
        "war pick", "pick", "war dart",
        "2 handed sword", "longsword", "two handed", "greatsword"
    ]

    return any(kw in n for kw in weapon_keywords)


def get_weapon_price(name: str, equipment_group: str) -> float:
    """
    Retourne le prix réel de l'arme dans le contexte du personnage :
    - Pour les achats post-kit : final_price_sp (avec surcoût Rare/Très rare)
    - Pour les items du kit : prix du kit (très bas pour le bâton)
    Retourne 0.0 si introuvable.
    """
    if not name:
        return 0.0

    # 1. Essayer d'abord dans le pool du groupe (post-kit ou armes de base ajoutées aux .txt)
    enriched = group_equipment_pools.get_item_with_final_price(equipment_group, name)
    if enriched and "final_price_sp" in enriched:
        return float(enriched["final_price_sp"])

    # 2. Fallback : chercher dans le kit universel
    kit_items = kits.get_universal_starting_kit()
    for item in kit_items:
        if item["name"].lower() == name.lower():
            # Conversion bp → sp
            return round(item["price_bp"] / 10.0, 2)

    # 3. Dernier fallback : prix historique approximatif (rare)
    try:
        corrected = post_kit.price_fix.get_historical_price(name, "10 sp")
        bp = post_kit.kits.parse_price_to_bp(corrected)
        return round(bp / 10.0, 2)
    except Exception:
        return 3.0  # valeur par défaut raisonnable pour une arme moyenne


def get_most_expensive_weapon(char: dict) -> Optional[Tuple[str, float]]:
    """
    Retourne (nom_arme, prix_sp) de l'arme la plus chère du personnage,
    ou None s'il n'a aucune arme offensive.
    """
    equipment_group = char.get("Equipment_Group") or "Groupe1_Cote_des_Epees"

    kit_names = char.get("Starting_Equipment_Kit", []) or []
    post_names = char.get("Post_Kit_Purchases", []) or []

    all_weapons = []
    seen = set()

    # Kit (très peu d'armes offensives actuellement : surtout le bâton)
    for name in kit_names:
        if name not in seen and is_offensive_weapon(name):
            price = get_weapon_price(name, equipment_group)
            all_weapons.append((name, price))
            seen.add(name)

    # Post-kit (la grande majorité des armes)
    for name in post_names:
        if name not in seen and is_offensive_weapon(name):
            price = get_weapon_price(name, equipment_group)
            all_weapons.append((name, price))
            seen.add(name)

    if not all_weapons:
        return None

    # Trier par prix descendant
    all_weapons.sort(key=lambda x: x[1], reverse=True)
    return all_weapons[0]


def run_analysis(count: int = 800, seed: int = 42) -> None:
    if seed is not None:
        random.seed(seed)

    print(f"=== Analyse : Arme la plus chère par personnage ===")
    print(f"Génération de {count} personnages (seed={seed})...\n")

    top_weapons = []
    chars_without_weapon = 0
    total_weapons_considered = 0

    progress_step = max(1, count // 20)

    for i in range(1, count + 1):
        char = generate_character(f"AN-{i:05d}")

        result = get_most_expensive_weapon(char)
        if result is None:
            chars_without_weapon += 1
        else:
            name, price = result
            top_weapons.append(name)
            total_weapons_considered += 1

        if i % progress_step == 0:
            print(f"   - {i:5d} / {count}  (sans arme offensive : {chars_without_weapon})")

    print(f"\n[OK] Génération terminée.")
    print(f"     Personnages sans aucune arme offensive : {chars_without_weapon} ({chars_without_weapon/count:.1%})")

    if not top_weapons:
        print("Aucune arme trouvée.")
        return

    # Comptage
    counter = Counter(top_weapons)
    total = len(top_weapons)

    print(f"\n=== TOP 10 des armes les plus chères du personnage (sur {total} persos avec au moins une arme) ===\n")

    print(f"{'Rang':<5} {'Arme':<45} {'Nombre':>8} {'%':>8}")
    print("-" * 68)

    for rank, (weapon, cnt) in enumerate(counter.most_common(10), 1):
        pct = (cnt / total) * 100
        print(f"{rank:<5} {weapon:<45} {cnt:>8} {pct:>7.2f}%")

    # Sauvegarde d'un petit résumé CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = f"Top_Arme_La_Plus_Chere_{timestamp}.csv"

    with open(summary_file, "w", newline="", encoding="utf-8") as f:
        f.write("Rang,Arme,Nombre,Pourcentage,Total_Personnages_Avec_Arme\n")
        for rank, (weapon, cnt) in enumerate(counter.most_common(20), 1):  # top 20 dans le fichier
            pct = (cnt / total) * 100
            f.write(f'{rank},"{weapon}",{cnt},{pct:.2f},{total}\n')

    print(f"\n[Export] Résumé complet (top 20) -> {summary_file}")

    # Quelques stats bonus
    print(f"\n[Stats bonus]")
    print(f"  - Total personnages analysés          : {count}")
    print(f"  - Personnages avec au moins 1 arme   : {total} ({total/count:.1%})")
    print(f"  - Arme la plus fréquente comme 'plus chère' : {counter.most_common(1)[0][0]} ({counter.most_common(1)[0][1]/total:.1%})")


if __name__ == "__main__":
    # 800 comme dans les analyses précédentes (bon équilibre vitesse / représentativité)
    run_analysis(count=800, seed=42)
