# main.py - Batch Character Generator
import csv
import argparse
import random
from datetime import datetime

from utils import generate_character


def generate_batch(
    count: int = 100,
    output: str = None,
    seed: int = None,
    race_filter: str = None
):
    if seed is not None:
        random.seed(seed)
        print(f"🔒 Seed fixé à {seed} (reproductible)")

    print(f"🎲 Génération de {count} personnages...\n")

    characters = []
    
    for i in range(1, count + 1):
        char = generate_character(f"CH-{i:05d}")
        characters.append(char)
        
        if i % max(10, count // 10) == 0:
            print(f"   → {i:5d} / {count} personnages générés...")

    # ====================== EXPORT CSV ======================
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output or f"Personnages_{timestamp}.csv"

    fieldnames = [
        "ID", "Indice", "Race", "Ethnicity",
        "Weight_Score", "Build_Score", "Height_cm", "Weight_kg", "Size_Score",
        "Balance", "Speed", "Coordination", "Precision", "Endurance",
        "Regeneration", "Vigilance", "Beauty", "Stealth",
        "Grappling", "Melee", "Projectiles", "Fencing",
        "Combat_Points",
        "Magic", "Magic_Type", "Magic_Subtype", "Magic_Description",
        "Skill_Points", "Skill_Bonus", "Special"
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(characters)

    # ====================== RÉSUMÉ ======================
    print(f"\n✅ Génération terminée !")
    print(f"📁 Fichier créé → {filename}")
    print(f"   {count} personnages générés avec succès.\n")

    # Statistiques Magie
    total = len(characters)
    magic_count = sum(1 for c in characters if c.get("Magic") == "YES")
    
    theurgiste = sum(1 for c in characters if c.get("Magic_Type") == "Théurgiste")
    magicien = sum(1 for c in characters if c.get("Magic_Type") == "Magicien")
    double = sum(1 for c in characters if c.get("Magic_Type") == "Double")
    sauvage = sum(1 for c in characters if c.get("Magic_Type") == "Sauvage")

    print("📊 STATISTIQUES MAGIE :")
    print(f"   Magiques totaux        : {magic_count} ({magic_count/total:.1%})")
    print(f"   → Théurgistes          : {theurgiste}")
    print(f"   → Magiciens            : {magicien}")
    print(f"   → Double Talent        : {double}")
    print(f"   → Magie Sauvage        : {sauvage}")


def main():
    parser = argparse.ArgumentParser(
        description="🚀 Générateur de Personnages",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("-n", "--count", type=int, default=100,
                        help="Nombre de personnages à générer")
    parser.add_argument("-o", "--output", type=str,
                        help="Nom du fichier de sortie (CSV)")
    parser.add_argument("-s", "--seed", type=int,
                        help="Seed pour la reproductibilité")
    parser.add_argument("-r", "--race", type=str,
                        help="Filtrer sur une race (ex: Humain)")

    args = parser.parse_args()

    generate_batch(
        count=args.count,
        output=args.output,
        seed=args.seed,
        race_filter=args.race
    )


if __name__ == "__main__":
    main()