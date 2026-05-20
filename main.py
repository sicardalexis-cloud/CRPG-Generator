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
        "Magic_Type",
        "Combat_Points",
        "Grappling",
        "Melee",
        "Fencing",
        "Skill_Modifier",
        "Projectiles",
        
        # Caractéristiques physiques
        "Weight_Score", "Build_Score", "Height_cm", "Weight_kg", "Size_Score",
        
        # Attributs secondaires
        "Balance", "Quickness", "Coordination", "Precision", "Endurance",
        "Regeneration", "Vigilance", "Beauty", "Stealth",
        
        # Nouveaux attributs dérivés
        "Speed", "Dodge", "Climbing",
        
        # Magie
        "Magic", "Magic_Subtype", "Magic_Description",
        
        "Special"
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(characters)

    print(f"\n✅ Génération terminée !")
    print(f"📁 Fichier créé → {filename}")
    print(f"   {count} personnages générés avec succès.")

        # ====================== STATISTIQUES MAGIE ======================
    total = len(characters)
    magic_count = sum(1 for c in characters if c.get("Magic") == "YES")

    # Comptage par type
    theurgique = sum(1 for c in characters if c.get("Magic_Type") == "Théurgique")
    arcanique  = sum(1 for c in characters if c.get("Magic_Type") == "Arcanique")
    sauvage    = sum(1 for c in characters if c.get("Magic_Type") == "Sauvage")

    # Sous-types les plus courants pour la magie sauvage
    sauvage_subtypes = {}
    for c in characters:
        if c.get("Magic_Type") == "Sauvage" and c.get("Magic_Subtype"):
            subtype = c.get("Magic_Subtype")
            sauvage_subtypes[subtype] = sauvage_subtypes.get(subtype, 0) + 1

    print("\n" + "="*60)
    print("📊 STATISTIQUES MAGIE")
    print("="*60)
    print(f"   Personnages magiques   : {magic_count:4d} ({magic_count/total:.2%})")
    print(f"   → Théurgiques          : {theurgique:4d} ({theurgique/total:.2%})")
    print(f"   → Arcaniques           : {arcanique:4d}  ({arcanique/total:.2%})")
    print(f"   → Sauvages             : {sauvage:4d}   ({sauvage/total:.2%})")
    
    if sauvage > 0 and sauvage_subtypes:
        print("\n   Sous-types Magie Sauvage les plus courants :")
        for subtype, count in sorted(sauvage_subtypes.items(), key=lambda x: x[1], reverse=True)[:6]:
            print(f"      • {subtype:18} : {count:3d} pers. ({count/sauvage:.1%})")

    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description="🚀 Générateur de Personnages",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("-n", "--count", type=int, default=100, help="Nombre de personnages à générer")
    parser.add_argument("-o", "--output", type=str, help="Nom du fichier de sortie (CSV)")
    parser.add_argument("-s", "--seed", type=int, help="Seed pour la reproductibilité")
    parser.add_argument("-r", "--race", type=str, help="Filtrer sur une race (ex: Humain)")

    args = parser.parse_args()

    generate_batch(
        count=args.count,
        output=args.output,
        seed=args.seed,
        race_filter=args.race
    )


if __name__ == "__main__":
    main()