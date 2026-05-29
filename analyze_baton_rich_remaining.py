"""
analyze_baton_rich_remaining.py

Question : Dans les personnages les plus riches du sous-groupe "Bâton seulement",
             le montant restant à la fin des achats peut monter jusqu'à combien maximum ?

On cherche :
- Le maximum absolu d'argent restant (Final_Pocket_Money_BP) observé chez les "Bâton seulement".
- Les top 5-10 avec le plus d'argent restant.
- Pour les personnages les plus riches en capital de départ dans ce sous-groupe,
  quel % et quel montant absolu ils gardent.
"""

import random
from collections import defaultdict
from datetime import datetime

from utils import generate_character
from data.equipment import post_kit_purchases as post_kit
from data.equipment import group_equipment_pools
from data.equipment import regional_adventurer_kits as kits

# Copie des helpers prouvés
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

def get_purchase_price(name: str, equipment_group: str) -> float:
    enriched = group_equipment_pools.get_item_with_final_price(equipment_group, name)
    if enriched and "final_price_sp" in enriched:
        return float(enriched["final_price_sp"])
    for item in kits.get_universal_starting_kit():
        if item["name"].lower() == name.lower():
            return round(item["price_bp"] / 10.0, 2)
    return 0.0

def is_baton_only(char: dict) -> bool:
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


def categorize_purchase(name: str) -> str:
    n = name.lower()
    mount_keywords = ["rouncey", "courser", "palfrey", "destrier", "mule", "pony", "camel", "dog sled"]
    if any(kw in n for kw in mount_keywords):
        return "Mobility"
    riding_keywords = ["saddle", "packsaddle", "saddle bags", "draft harness", "war saddle"]
    if any(kw in n for kw in riding_keywords):
        return "RidingGear"
    travel_keywords = ["tent", "camp bed", "lantern", "lamp oil"]
    if any(kw in n for kw in travel_keywords):
        return "TravelGear"
    armor_prio = post_kit.get_armor_purchase_priority(name)
    if armor_prio is not None and armor_prio >= 0:
        return "Armor"
    if post_kit.is_shield(name):
        return "Armor"
    if post_kit.is_weapon_or_armor(name) and not post_kit.is_shield(name):
        armor_keywords = ["breastplate", "hauberk", "brigandine", "gambeson", "plackart",
                          "helmet", "helm", "bascinet", "sallet", "armet", "gauntlet",
                          "greaves", "cuisses", "tassets", "fauld", "gorget"]
        if not any(kw in n for kw in armor_keywords):
            return "Weapons"
    return "Other"


def run_rich_remaining_analysis(count: int = 1500, seed: int = 42):
    if seed is not None:
        random.seed(seed)

    print(f"=== Maximum d'argent restant chez les 'Bâton seulement' les plus riches ===")
    print(f"Génération de {count} personnages (seed={seed}) pour trouver les extrêmes...\n")

    baton_only = []          # liste de dicts enrichis pour le sous-groupe
    progress_step = max(1, count // 25)

    for i in range(1, count + 1):
        char = generate_character(f"RICH-{i:05d}")
        if is_baton_only(char):
            # Enrichir avec des infos utiles
            char["_starting_capital_bp"] = float(char.get("Starting_Capital", 0))
            char["_remaining_bp"] = float(char.get("Final_Pocket_Money_BP", 0))
            char["_spent_bp"] = float(char.get("Post_Kit_Total_Spent_BP", 0))
            if char["_starting_capital_bp"] > 0:
                char["_remaining_pct"] = (char["_remaining_bp"] / char["_starting_capital_bp"]) * 100
            else:
                char["_remaining_pct"] = 0
            baton_only.append(char)

        if i % progress_step == 0:
            print(f"   - {i:5d} / {count}   | 'Bâton seulement' trouvés : {len(baton_only)}")

    print(f"\n[OK] {len(baton_only)} personnages 'Bâton seulement' identifiés sur {count}.\n")

    if not baton_only:
        print("Aucun personnage dans le sous-groupe.")
        return

    # Trier par argent restant absolu (descendant)
    by_remaining = sorted(baton_only, key=lambda c: c["_remaining_bp"], reverse=True)

    print("=" * 75)
    print("TOP 10 DES PERSONNAGES 'BÂTON SEULEMENT' AVEC LE PLUS D'ARGENT RESTANT")
    print("=" * 75)

    print(f"\n{'Rang':<5} {'ID':<12} {'Capital départ':>14} {'Restant':>12} {'% gardé':>9} {'Dépensé':>12} {'Groupe':<22}")
    print("-" * 75)

    top_n = min(10, len(by_remaining))
    for rank, c in enumerate(by_remaining[:top_n], 1):
        cap = c["_starting_capital_bp"]
        rem = c["_remaining_bp"]
        pct = c["_remaining_pct"]
        spent = c["_spent_bp"]
        grp = c.get("Equipment_Group", "")
        cid = c.get("ID", "")
        print(f"{rank:<5} {cid:<12} {cap:>12,.0f} bp {rem:>10,.0f} bp {pct:>8.1f}% {spent:>10,.0f} bp   {grp:<22}")

    # Le maximum absolu
    richest_remaining = by_remaining[0]
    max_remaining_bp = richest_remaining["_remaining_bp"]
    max_remaining_sp = max_remaining_bp / 10.0
    max_start = richest_remaining["_starting_capital_bp"]
    max_pct = richest_remaining["_remaining_pct"]

    print(f"\n>>> MAXIMUM OBSERVÉ D'ARGENT RESTANT DANS LE SOUS-GROUPE :")
    print(f"    {max_remaining_bp:,.0f} bp  ({max_remaining_sp:,.1f} sp)")
    print(f"    (soit {max_pct:.1f}% de son capital de départ de {max_start:,.0f} bp)")

    # Focus sur les "vraiment riches" (capital de départ élevé, disons > 2500 bp ou top 20% du sous-groupe)
    rich_threshold = sorted([c["_starting_capital_bp"] for c in baton_only], reverse=True)
    if len(rich_threshold) >= 5:
        # On prend le seuil du top 15% les plus riches en capital de départ dans le sous-groupe
        top_15_idx = max(1, int(len(rich_threshold) * 0.15))
        high_capital_threshold = rich_threshold[top_15_idx - 1]
    else:
        high_capital_threshold = 2000

    rich_in_subgroup = [c for c in baton_only if c["_starting_capital_bp"] >= high_capital_threshold]
    if rich_in_subgroup:
        rich_in_subgroup_sorted = sorted(rich_in_subgroup, key=lambda c: c["_remaining_bp"], reverse=True)
        print(f"\n--- Parmi les plus riches du sous-groupe (capital depart >= {high_capital_threshold:,.0f} bp, n={len(rich_in_subgroup)}) ---")
        print(f"    Leur argent restant maximum observé : {rich_in_subgroup_sorted[0]['_remaining_bp']:,.0f} bp "
              f"({rich_in_subgroup_sorted[0]['_remaining_pct']:.1f}%)")

        # Moyenne de restant pour ces riches
        avg_rem_rich = sum(c["_remaining_bp"] for c in rich_in_subgroup) / len(rich_in_subgroup)
        print(f"    Moyenne d'argent restant chez ces riches : {avg_rem_rich:,.0f} bp")

    # Quelques détails sur le recordman
    print("\n" + "=" * 75)
    print("PROFIL DU RECORDMAN (plus gros restant dans 'Bâton seulement')")
    print("=" * 75)
    rec = richest_remaining
    print(f"\nID                  : {rec.get('ID')}")
    print(f"Région / Groupe     : {rec.get('Origin_Region')} / {rec.get('Equipment_Group')}")
    print(f"Capital de départ   : {rec['_starting_capital_bp']:,.0f} bp ({rec['_starting_capital_bp']/10:.1f} sp)")
    print(f"Total dépensé       : {rec['_spent_bp']:,.0f} bp")
    print(f"** Restant final    : {rec['_remaining_bp']:,.0f} bp ({rec['_remaining_pct']:.1f}%) **")
    print(f"\nAchats post-kit ({len(rec.get('Post_Kit_Purchases', []))} items) :")
    purchases = rec.get("Post_Kit_Purchases", []) or []
    if purchases:
        # Catégoriser rapidement
        cat_count = defaultdict(int)
        for p in purchases:
            cat_count[categorize_purchase(p)] += 1
        for cat, cnt in sorted(cat_count.items(), key=lambda x: -x[1]):
            print(f"  - {cat:<12} : {cnt} item(s)")
        print("\n  Liste des achats :")
        for p in purchases[:12]:
            print(f"    - {p}")
        if len(purchases) > 12:
            print(f"    ... (+{len(purchases)-12} autres)")
    else:
        print("  (aucun achat post-kit - tres frugal)")

    print(f"\n[Conclusion] Le montant restant le plus élevé observé chez un 'Bâton seulement' très riche")
    print(f"             est de l'ordre de {max_remaining_bp:,.0f} bp ({max_remaining_sp:,.0f} sp).")
    print(f"             Cela reste possible quand le personnage priorise fortement armure + monture")
    print(f"             sans jamais toucher aux armes chères (grâce aux règles N1/N2).")

    # Export simple
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = f"Baton_Rich_Max_Remaining_{ts}.txt"
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"Maximum restant 'Bâton seulement' : {max_remaining_bp:,.0f} bp\n")
        f.write(f"Sur {count} persos (seed {seed})\n")
    print(f"\n[Export] Résumé -> {out}")


if __name__ == "__main__":
    # 1500 pour avoir une bonne chance d'attraper les cas extrêmes riches + frugaux
    run_rich_remaining_analysis(count=1500, seed=42)
