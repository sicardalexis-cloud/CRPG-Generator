"""
analyze_baton_only_spending.py

Analyse ciblée sur le sous-groupe identifié précédemment :
"Les personnages qui n'ont que le Bâton de marche comme arme la plus chère de leur inventaire"

Questions :
- Dans quoi ont-ils dépensé leur capital ?
- Combien leur reste-t-il à la fin des achats post-kit ?

On regarde uniquement les achats post-kit (le kit de base est gratuit).
"""

import random
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

from utils import generate_character
from data.equipment import post_kit_purchases as post_kit
from data.equipment import group_equipment_pools
from data.equipment import regional_adventurer_kits as kits

# =============================================================================
# FILTRE "ARME OFFENSIVE" (identique au script précédent pour cohérence)
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
    """Retourne True si c'est une arme offensive (pas bouclier, pas armure)."""
    if not name:
        return False
    n = name.lower()

    if post_kit.is_shield(name):
        return False
    if any(kw in n for kw in ARMOR_KEYWORDS):
        return False
    if not post_kit.is_weapon_or_armor(name):
        return False

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


# =============================================================================
# CATÉGORISATION DES ACHATS (basée sur la logique interne de post_kit_purchases)
# =============================================================================

def get_purchase_price(name: str, equipment_group: str) -> float:
    """Prix réel payé (sp) avec surcoût si applicable."""
    enriched = group_equipment_pools.get_item_with_final_price(equipment_group, name)
    if enriched and "final_price_sp" in enriched:
        return float(enriched["final_price_sp"])

    # Fallback kit
    for item in kits.get_universal_starting_kit():
        if item["name"].lower() == name.lower():
            return round(item["price_bp"] / 10.0, 2)
    return 0.0


def categorize_purchase(name: str) -> str:
    """
    Retourne la catégorie principale de la dépense :
    - Armor
    - Weapons (offensives seulement)
    - Mobility (chevaux, mules, chameaux, dog sled...)
    - TravelGear (tentes, lits de camp, lanternes...)
    - RidingGear (selles, harnais, sacoches...)
    - Other
    """
    n = name.lower()

    # === MOBILITY (montures) ===
    mount_keywords = ["rouncey", "courser", "palfrey", "destrier", "mule", "pony", "camel", "dog sled"]
    if any(kw in n for kw in mount_keywords):
        return "Mobility"

    # === RIDING GEAR (harnachement) ===
    riding_keywords = ["saddle", "packsaddle", "saddle bags", "draft harness", "war saddle"]
    if any(kw in n for kw in riding_keywords):
        return "RidingGear"

    # === TRAVEL GEAR ===
    travel_keywords = ["tent", "camp bed", "lantern", "lamp oil"]
    if any(kw in n for kw in travel_keywords):
        return "TravelGear"

    # === ARMOR (pièces d'armure + boucliers) ===
    # On utilise la fonction existante de priorité armure
    armor_prio = post_kit.get_armor_purchase_priority(name)
    if armor_prio is not None and armor_prio >= 0:
        return "Armor"

    # Boucliers (ils sont considérés comme armure défensive)
    if post_kit.is_shield(name):
        return "Armor"

    # === WEAPONS (offensives) ===
    if post_kit.is_weapon_or_armor(name) and not post_kit.is_shield(name):
        # On exclut les pièces d'armure qui auraient pu passer au travers
        armor_keywords = ["breastplate", "hauberk", "brigandine", "gambeson", "plackart",
                          "helmet", "helm", "bascinet", "sallet", "armet", "gauntlet",
                          "greaves", "cuisses", "tassets", "fauld", "gorget"]
        if not any(kw in n for kw in armor_keywords):
            return "Weapons"

    # === Autres (outils, nourriture, vêtements, etc. qui ne sont pas dans les catégories ci-dessus)
    return "Other"


def is_baton_only(char: dict) -> bool:
    """Le personnage n'a aucune arme plus chère que le Bâton de marche."""
    equipment_group = char.get("Equipment_Group") or "Groupe1_Cote_des_Epees"
    kit_names = char.get("Starting_Equipment_Kit", []) or []
    post_names = char.get("Post_Kit_Purchases", []) or []

    all_weapons = []
    seen = set()

    for name in kit_names + post_names:
        if name not in seen and is_offensive_weapon(name):
            price = get_purchase_price(name, equipment_group)
            all_weapons.append((name, price))
            seen.add(name)

    if not all_weapons:
        return False

    all_weapons.sort(key=lambda x: x[1], reverse=True)
    most_expensive = all_weapons[0][0]
    return "bâton de marche" in most_expensive.lower() or "walking staff" in most_expensive.lower()


def run_baton_only_analysis(count: int = 800, seed: int = 42):
    if seed is not None:
        random.seed(seed)

    print("=== Analyse ciblée : Personnages qui n'ont QUE le Bâton comme arme ===")
    print(f"Génération de {count} personnages (seed={seed})...\n")

    baton_only_chars = []
    progress_step = max(1, count // 20)

    for i in range(1, count + 1):
        char = generate_character(f"BT-{i:05d}")
        if is_baton_only(char):
            baton_only_chars.append(char)

        if i % progress_step == 0:
            print(f"   - {i:5d} / {count}  (trouvés avec seulement le bâton : {len(baton_only_chars)})")

    total = len(baton_only_chars)
    pct = (total / count) * 100 if count > 0 else 0

    print(f"\n[OK] {total} personnages ({pct:.2f}%) n'ont que le Bâton de marche comme arme la plus chère.\n")

    if total == 0:
        print("Aucun personnage dans ce sous-groupe.")
        return

    # =============================================================================
    # ANALYSE DES DÉPENSES DANS LE SOUS-GROUPE
    # =============================================================================

    category_spending = defaultdict(float)   # total sp dépensé par catégorie
    category_counts = Counter()              # nombre d'achats par catégorie
    item_counter = Counter()                 # items les plus achetés
    remaining_bp_list = []
    spent_bp_list = []
    capital_list = []

    for char in baton_only_chars:
        group = char.get("Equipment_Group") or "Groupe1_Cote_des_Epees"
        purchases = char.get("Post_Kit_Purchases", []) or []

        spent = float(char.get("Post_Kit_Total_Spent_BP", 0))
        remaining = float(char.get("Final_Pocket_Money_BP", 0))
        capital = float(char.get("Starting_Capital", 0))

        spent_bp_list.append(spent)
        remaining_bp_list.append(remaining)
        capital_list.append(capital)

        for item_name in purchases:
            cat = categorize_purchase(item_name)
            price = get_purchase_price(item_name, group)

            category_spending[cat] += price
            category_counts[cat] += 1
            item_counter[item_name] += 1

    # =============================================================================
    # AFFICHAGE DES RÉSULTATS
    # =============================================================================

    print("=" * 70)
    print("RÉPARTITION DES DÉPENSES (sous-groupe 'Bâton seulement')")
    print("=" * 70)

    total_spent_sp = sum(category_spending.values())
    print(f"\nDépenses totales du sous-groupe : {total_spent_sp:,.1f} sp")

    # Tri par montant dépensé
    sorted_cats = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)

    print(f"\n{'Catégorie':<15} {'Montant (sp)':>12} {'% du total':>10} {'Nb achats':>10}")
    print("-" * 50)
    for cat, amount in sorted_cats:
        pct_cat = (amount / total_spent_sp * 100) if total_spent_sp > 0 else 0
        print(f"{cat:<15} {amount:>12,.1f} {pct_cat:>9.1f}% {category_counts[cat]:>10}")

    # =============================================================================
    # ARGENT RESTANT
    # =============================================================================

    print("\n" + "=" * 70)
    print("ARGENT RESTANT À LA FIN DES ACHATS")
    print("=" * 70)

    avg_remaining = sum(remaining_bp_list) / len(remaining_bp_list)
    median_remaining = sorted(remaining_bp_list)[len(remaining_bp_list) // 2]
    avg_capital = sum(capital_list) / len(capital_list)
    avg_spent = sum(spent_bp_list) / len(spent_bp_list)

    avg_remaining_pct = (avg_remaining / avg_capital * 100) if avg_capital > 0 else 0

    print(f"\nCapital de départ moyen (sous-groupe) : {avg_capital:,.0f} bp  ({avg_capital/10:.1f} sp)")
    print(f"Dépense moyenne post-kit             : {avg_spent:,.0f} bp  ({avg_spent/10:.1f} sp)")
    print(f"Argent restant moyen                 : {avg_remaining:,.0f} bp  ({avg_remaining/10:.1f} sp)")
    print(f"Pourcentage moyen gardé              : {avg_remaining_pct:.1f} %")

    # Distribution de l'argent restant
    high_remaining = sum(1 for r in remaining_bp_list if r >= 0.7 * avg_capital)
    medium_remaining = sum(1 for r in remaining_bp_list if 0.4 * avg_capital <= r < 0.7 * avg_capital)
    low_remaining = sum(1 for r in remaining_bp_list if r < 0.4 * avg_capital)

    print(f"\nDistribution de l'argent restant :")
    print(f"  - Ont garde 70% ou plus du capital : {high_remaining:3d} ({high_remaining/total*100:5.1f}%)")
    print(f"  - Ont garde entre 40 et 70%        : {medium_remaining:3d} ({medium_remaining/total*100:5.1f}%)")
    print(f"  - Ont garde moins de 40%           : {low_remaining:3d} ({low_remaining/total*100:5.1f}%)")

    # =============================================================================
    # TOP ITEMS ACHETÉS PAR CE SOUS-GROUPE
    # =============================================================================

    print("\n" + "=" * 70)
    print("TOP 15 DES ACHATS LES PLUS FRÉQUENTS (sous-groupe Bâton seulement)")
    print("=" * 70)

    print(f"\n{'Rang':<5} {'Item':<45} {'Nb fois acheté':>14}")
    print("-" * 65)
    for rank, (item, cnt) in enumerate(item_counter.most_common(15), 1):
        print(f"{rank:<5} {item:<45} {cnt:>14}")

    # =============================================================================
    # PROFIL TYPE
    # =============================================================================

    print("\n" + "=" * 70)
    print("PROFIL TYPE DU PERSONNAGE 'BÂTON SEULEMENT'")
    print("=" * 70)

    print(f"""
- Ils représentent {pct:.1f}% de la population.
- Ils dépensent relativement peu en armes (souvent 0 ou très peu, car ils n'achètent rien de mieux que le bâton).
- Leurs dépenses principales vont dans : Armor (pièces de protection, boucliers, casques) et parfois Mobility (une monture correcte).
- Ils gardent en moyenne {avg_remaining_pct:.1f}% de leur capital de départ.
- Beaucoup sont "raisonnables" ou frugaux : ils s'équipent correctement en protection et en mobilité sans tout claquer dans du matériel de combat cher.
""")

    # Sauvegarde optionnelle d'un résumé
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = f"Baton_Only_Spending_Analysis_{timestamp}.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"Analyse 'Bâton seulement' - {total} personnages sur {count}\n")
        f.write(f"Date : {datetime.now()}\n\n")
        f.write("Top catégories de dépenses :\n")
        for cat, amount in sorted_cats:
            f.write(f"  {cat}: {amount:.1f} sp ({amount/total_spent_sp*100:.1f}%)\n")
        f.write(f"\nArgent restant moyen : {avg_remaining:.0f} bp ({avg_remaining_pct:.1f}% du capital)\n")

    print(f"\n[Export] Résumé texte -> {out_file}")


if __name__ == "__main__":
    run_baton_only_analysis(count=800, seed=42)
