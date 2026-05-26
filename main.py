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
        
        # Filtre race (optionnel)
        if race_filter and char["Race"].lower() != race_filter.lower():
            continue
            
        characters.append(char)
        
        if i % max(10, count // 10) == 0:
            print(f"   → {i:5d} / {count} personnages générés...")

    # ====================== EXPORT CSV ======================
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output or f"Personnages_{timestamp}.csv"

    fieldnames = [
        "ID", "Race", "Ethnicity", "Origin_Region", "Settlement_Type",
        
        # Compétences
        "Total_Skills", "Outdoor_Count", "Urban_Count",
        "Outdoor_Skills", "Urban_Skills",
        
        # Secondaires
        "Knowledge", "Craft", "Literacy", "Bonus_Languages",
        
        # Combat & Magie
        "Combat_Points", "Magic", "Magic_Type", "Magic_Subtype",
        "Grappling", "Melee", "Projectiles", "Fencing",
        "Skill_Modifier",
        
        # Physiques
        "Height_cm", "Weight_kg", "Size_Score",
        "Balance", "Quickness", "Coordination", "Precision",
        "Endurance", "Vigilance", "Beauty", "Stealth", "Speed",
        
        "Special",
        "Generation_Date"
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for char in characters:
            row = {
                "ID": char["ID"],
                "Race": char["Race"],
                "Ethnicity": char["Ethnicity"],
                "Origin_Region": char["Origin_Region"],
                "Settlement_Type": char["Settlement_Type"],
                
                "Total_Skills": char["Total_Skills"],
                "Outdoor_Count": char["Outdoor_Count"],
                "Urban_Count": char["Urban_Count"],
                
                # Liste → chaîne séparée par |
                "Outdoor_Skills": " | ".join(char.get("Outdoor_Skills", [])),
                "Urban_Skills": " | ".join(char.get("Urban_Skills", [])),
                
                "Knowledge": " | ".join(char.get("Knowledge", [])),
                "Craft": " | ".join(char.get("Craft", [])),
                
                "Literacy": " | ".join(f"{k} ({v})" for k, v in char.get("Literacy", {}).items()),
                "Bonus_Languages": " | ".join(char.get("Bonus_Languages", [])),
                
                "Combat_Points": char["Combat_Points"],
                "Magic": char["Magic"],
                "Magic_Type": char.get("Magic_Type", ""),
                "Magic_Subtype": char.get("Magic_Subtype", ""),
                
                "Grappling": char["Grappling"],
                "Melee": char["Melee"],
                "Projectiles": char["Projectiles"],
                "Fencing": char["Fencing"],
                "Skill_Modifier": char["Skill_Modifier"],
                
                "Height_cm": char["Height_cm"],
                "Weight_kg": char["Weight_kg"],
                "Size_Score": char["Size_Score"],
                
                "Balance": char["Balance"],
                "Quickness": char["Quickness"],
                "Coordination": char["Coordination"],
                "Precision": char["Precision"],
                "Endurance": char["Endurance"],
                "Vigilance": char["Vigilance"],
                "Beauty": char["Beauty"],
                "Stealth": char["Stealth"],
                "Speed": char["Speed"],
                
                "Special": char.get("Special", "Aucun"),
                "Generation_Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            writer.writerow(row)

    print(f"\n✅ Génération terminée !")
    print(f"📁 Fichier créé → {filename}")
    print(f"   {len(characters)} personnages exportés.")

    # Statistiques rapides
    magic_count = sum(1 for c in characters if c.get("Magic") == "YES")
    print(f"\n📊 Magiques : {magic_count}/{len(characters)} ({magic_count/len(characters):.1%})")


def main():
    parser = argparse.ArgumentParser(
        description="🚀 Générateur de Personnages - Export CSV",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("-n", "--count", type=int, default=100, help="Nombre de personnages")
    parser.add_argument("-o", "--output", type=str, help="Nom du fichier CSV")
    parser.add_argument("-s", "--seed", type=int, help="Seed pour reproductibilité")
    parser.add_argument("-r", "--race", type=str, help="Filtrer par race (ex: Human, Elf)")

    args = parser.parse_args()

    generate_batch(
        count=args.count,
        output=args.output,
        seed=args.seed,
        race_filter=args.race
    )


if __name__ == "__main__":
    main()