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
        "Origin_Region",
        "Settlement_Type",
        "Bonus_Languages",
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
        "Speed", "Dodge", "Climbing",
        
        # Magie
        "Magic", "Magic_Subtype", "Magic_Description",
        
        "Special",
        "Active Skills"
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for char in characters:
            row = char.copy()

            # Formatage des colonnes spéciales
            row["Origin_Region"] = char.get("Origin_Region", "")
            row["Settlement_Type"] = char.get("Settlement_Type", "")
            row["Bonus_Languages"] = " + ".join(char.get("Bonus_Languages", []))

            # Formatage des compétences actives
            skills_dict = char.get("Skills", {})
            if isinstance(skills_dict, dict) and skills_dict:
                row["Active Skills"] = "\n".join(skills_dict.keys())
            else:
                row["Active Skills"] = ""

            # Nettoyage des clés inutiles
            row.pop("Skills", None)

            # Remplacer les points par des virgules pour les nombres flottants
            for key, value in list(row.items()):
                if isinstance(value, float):
                    row[key] = str(value).replace('.', ',')
                elif value is None:
                    row[key] = ""
                elif key not in fieldnames:
                    row.pop(key, None)

            writer.writerow(row)

    print(f"\n✅ Génération terminée !")
    print(f"📁 Fichier créé → {filename}")
    print(f"   {count} personnages générés.")

    # ====================== STATISTIQUES MAGIE ======================
    total = len(characters)
    magic_count = sum(1 for c in characters if c.get("Magic") == "YES")

    theurgique = sum(1 for c in characters if c.get("Magic_Type") == "Théurgique")
    arcanique  = sum(1 for c in characters if c.get("Magic_Type") == "Arcanique")
    sauvage    = sum(1 for c in characters if c.get("Magic_Type") == "Sauvage")

    print("\n" + "="*60)
    print("📊 STATISTIQUES MAGIE")
    print("="*60)
    print(f"   Personnages magiques   : {magic_count:4d} ({magic_count/total:.2%})")
    print(f"   → Théurgiques          : {theurgique:4d} ({theurgique/total:.2%})")
    print(f"   → Arcaniques           : {arcanique:4d}  ({arcanique/total:.2%})")
    print(f"   → Sauvages             : {sauvage:4d}   ({sauvage/total:.2%})")
    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description="🚀 Générateur de Personnages",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("-n", "--count", type=int, default=100, help="Nombre de personnages à générer")
    parser.add_argument("-o", "--output", type=str, help="Nom du fichier de sortie (CSV)")
    parser.add_argument("-s", "--seed", type=int, help="Seed pour la reproductibilité")
    parser.add_argument("-r", "--race", type=str, help="Filtrer sur une race (ex: Human)")

    args = parser.parse_args()

    generate_batch(
        count=args.count,
        output=args.output,
        seed=args.seed,
        race_filter=args.race
    )


if __name__ == "__main__":
    main()