import csv
import argparse
import random
from datetime import datetime

from utils import generate_character
from character_sheet import generate_character_sheet  # ← Import ajouté


def generate_batch(
    count: int = 100,
    output: str = None,
    seed: int = None,
    race_filter: str = None,
    generate_pdfs: bool = False
):
    if seed is not None:
        random.seed(seed)
        print(f"🔒 Seed fixé à {seed} (reproductible)")

    print(f"🎲 Génération de {count} personnages...\n")

    characters = []
    pdf_count = 0
    
    for i in range(1, count + 1):
        # ID temporaire
        char = generate_character(f"CH-{i:05d}")
        
        if race_filter and char["Race"].lower() != race_filter.lower():
            continue
            
        characters.append(char)
        
        # Génération de la fiche PDF (si activé)
        if generate_pdfs:
            try:
                generate_character_sheet(char)
                pdf_count += 1
            except Exception as e:
                print(f"⚠️ Erreur PDF pour {char['ID']}: {e}")

        if i % max(10, count // 10) == 0:
            print(f"   → {i:5d} / {count} personnages générés...")

    # ====================== EXPORT CSV ======================
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output or f"Personnages_{timestamp}.csv"

    fieldnames = [
        "ID", "Race", "Ethnicity", "Origin_Region", "Settlement_Type",
        "Outdoor_Skills", "Urban_Skills",
        "Knowledge", "Craft", "Literacy", "Spoken_Languages",
        "Combat_Points", "Magic", "Magic_Type", "Magic_Subtype",
        "Grappling", "Melee", "Projectiles", "Fencing", "Skill_Modifier",
        "Height_cm", "Weight_kg", "Size_Score",
        "Balance", "Quickness", "Coordination", "Precision",
        "Endurance", "Vigilance", "Beauty", "Stealth", "Speed",
        "Special", "Generation_Date"
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
                
                "Outdoor_Skills": " | ".join(char.get("Outdoor_Skills", [])),
                "Urban_Skills": " | ".join(char.get("Urban_Skills", [])),
                
                "Knowledge": " | ".join(char.get("Knowledge", [])),
                "Craft": " | ".join(char.get("Craft", [])),
                
                "Literacy": " | ".join(char.get("Literacy", [])) if char.get("Literacy") else "None",
                "Spoken_Languages": " | ".join(char.get("Spoken_Languages", [])),
                
                "Combat_Points": char.get("Combat_Points", ""),
                "Magic": char.get("Magic", "NO"),
                "Magic_Type": char.get("Magic_Type", ""),
                "Magic_Subtype": char.get("Magic_Subtype", ""),
                
                "Grappling": char.get("Grappling", ""),
                "Melee": char.get("Melee", ""),
                "Projectiles": char.get("Projectiles", ""),
                "Fencing": char.get("Fencing", ""),
                "Skill_Modifier": char.get("Skill_Modifier", ""),
                
                "Height_cm": char.get("Height_cm", ""),
                "Weight_kg": char.get("Weight_kg", ""),
                "Size_Score": char.get("Size_Score", ""),
                
                "Balance": char.get("Balance", ""),
                "Quickness": char.get("Quickness", ""),
                "Coordination": char.get("Coordination", ""),
                "Precision": char.get("Precision", ""),
                "Endurance": char.get("Endurance", ""),
                "Vigilance": char.get("Vigilance", ""),
                "Beauty": char.get("Beauty", ""),
                "Stealth": char.get("Stealth", ""),
                "Speed": char.get("Speed", ""),
                
                "Special": char.get("Special", "Aucun"),
                "Generation_Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            writer.writerow(row)

    print(f"\n✅ Export terminé → {filename} ({len(characters)} personnages)")

    if generate_pdfs:
        print(f"📄 {pdf_count} fiches PDF générées dans le dossier 'fiches/'")

    # Statistiques
    magic_count = sum(1 for c in characters if c.get("Magic") == "YES")
    print(f"\n📊 Statistiques :")
    print(f"   Magiques : {magic_count}/{len(characters)} ({magic_count/len(characters):.1%})")


def main():
    parser = argparse.ArgumentParser(
        description="🚀 Générateur de Personnages - Export CSV + PDF",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("-n", "--count", type=int, default=100, help="Nombre de personnages")
    parser.add_argument("-o", "--output", type=str, help="Nom du fichier CSV")
    parser.add_argument("-s", "--seed", type=int, help="Seed pour reproductibilité")
    parser.add_argument("-r", "--race", type=str, help="Filtrer par race (ex: Human, Elf)")
    parser.add_argument("-p", "--pdf", action="store_true", help="Générer aussi les fiches PDF")

    args = parser.parse_args()

    generate_batch(
        count=args.count,
        output=args.output,
        seed=args.seed,
        race_filter=args.race,
        generate_pdfs=args.pdf
    )


if __name__ == "__main__":
    main()