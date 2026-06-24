import csv
import argparse
import random
from datetime import datetime

from utils import generate_character
from data.equipment import post_kit_purchases as post_kit


def _build_armes_et_bouclier(char: dict) -> str:
    """Combine regular 'Armes_et_Bouclier' with starting magic items for CSV export."""
    armes = char.get("Armes_et_Bouclier", "Aucun") or "Aucun"
    magic = char.get("Starting_Magic_Items", []) or []
    if not magic:
        return armes if armes else "Aucun"
    magic_str = " | ".join(magic)
    if armes and armes != "Aucun":
        return f"{armes} | {magic_str}"
    return magic_str

# Optional PDF character sheet support (heavy deps: jinja2 + weasyprint)
# The feature was previously wired in batch_generator.py
try:
    from character_sheet import generate_character_sheet
    _HAS_SHEET_SUPPORT = True
except Exception:
    _HAS_SHEET_SUPPORT = False
    generate_character_sheet = None  # will be checked at use time


def generate_batch(
    count: int = 100,
    output: str = None,
    seed: int = None,
    race_filter: str = None,
    level: int = 1,
    generate_pdfs: bool = False
):
    if seed is not None:
        random.seed(seed)
        print(f"[SEED] Seed fixé à {seed} (reproductible)")

    print(f"[BATCH] Génération de {count} personnages...\n")

    characters = []
    
    for i in range(1, count + 1):
        char = generate_character(f"CH-{i:05d}", level=level)
        
        if race_filter and char["Race"].lower() != race_filter.lower():
            continue
            
        characters.append(char)
        
        # Génération des fiches PDF (si demandé et support disponible)
        if generate_pdfs:
            if _HAS_SHEET_SUPPORT and generate_character_sheet is not None:
                try:
                    generate_character_sheet(char)
                except Exception as e:
                    print(f"⚠️ Erreur génération fiche pour {char.get('ID', '?')}: {e}")
            else:
                print("⚠️ Support fiches PDF non disponible (installe jinja2 + weasyprint)")
        
        if i % max(10, count // 10) == 0:
            print(f"   -> {i:5d} / {count} personnages générés...")

    # ====================== EXPORT CSV ======================
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output or f"Personnages_{timestamp}.csv"

    # === Colonnes sans Total_Skills / Outdoor_Count / Urban_Count ===
    fieldnames = [
        "ID", "Level", "Race", "Ethnicity", "Origin_Region", "Settlement_Type", "Equipment_Group",
        
        # Compétences détaillées
        "Outdoor_Skills", 
        "Urban_Skills",
        
        # Secondaires
        "Knowledge", 
        "Craft", 
        "Literacy", 
        "Spoken_Languages",
        "Starting_Capital",
        "Magic_Item_Capital",
        "Final_Pocket_Money_BP",
        
        # Equipment kit (100 kits XV siecle Cote des Epees EN selection; full details in Armes_et_Bouclier)
        "Armes_et_Bouclier",
        
        "Prebuilt_Kit_Tier",
        "Prebuilt_Kit_Cost_Sp",
        "Prebuilt_Kit_Source",
        
        # Combat & Magie
        "Combat_Points", 
        "Magic", 
        "Magic_Type", 
        "Magic_Subtype",
        "Magic_And_Spells",
        "God",
        "Grappling", 
        "Melee", 
        "Projectiles", 
        "Fencing",
        "Reach",
        "Skill_Modifier",
        
        # Physiques
        "Height_cm", 
        "Weight_kg", 
        "Size_Score",
        "Balance", 
        "Quickness", 
        "Coordination", 
        "Precision",
        "Endurance", 
        "Regeneration",
        "Vigilance", 
        "Beauty", 
        "Stealth", 
        "Speed",
        
        "Special",
        "Generation_Date"
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for char in characters:
            # === Séparation des équipements ===
            kit_items = char.get("Starting_Equipment_Kit", []) or []
            post_items = char.get("Post_Kit_Purchases", []) or []
            all_equipment = kit_items + post_items

            armes_armures = []
            autre_equipement = []

            for item in all_equipment:
                if post_kit.is_weapon_or_armor(item):
                    armes_armures.append(item)
                else:
                    autre_equipement.append(item)

            row = {
                "ID": char["ID"],
                "Level": char.get("Level", 1),
                "Race": char["Race"],
                "Ethnicity": char["Ethnicity"],
                "Origin_Region": char["Origin_Region"],
                "Settlement_Type": char["Settlement_Type"],
                "Equipment_Group": char.get("Equipment_Group", ""),
                
                "Outdoor_Skills": " | ".join(char.get("Outdoor_Skills", [])),
                "Urban_Skills": " | ".join(char.get("Urban_Skills", [])),
                
                "Knowledge": " | ".join(char.get("Knowledge", [])),
                "Craft": " | ".join(char.get("Craft", [])),
                
                "Literacy": " | ".join(char.get("Literacy", [])) if char.get("Literacy") else "None",
                "Spoken_Languages": " | ".join(char.get("Spoken_Languages", [])),
                "Starting_Capital": char.get("Starting_Capital", 0),
                "Magic_Item_Capital": char.get("Magic_Item_Budget", 0),
                "Final_Pocket_Money_BP": char.get("Final_Pocket_Money_BP", 0),
                
                "Armes_et_Bouclier": _build_armes_et_bouclier(char),
                
                "Prebuilt_Kit_Tier": char.get("Prebuilt_Kit_Tier", ""),
                "Prebuilt_Kit_Cost_Sp": char.get("Prebuilt_Kit_Cost_Sp", 0),
                "Prebuilt_Kit_Source": char.get("Prebuilt_Kit_Source", ""),
                
                "Combat_Points": char["Combat_Points"],
                "Magic": char["Magic"],
                "Magic_Type": char.get("Magic_Type", ""),
                "Magic_Subtype": char.get("Magic_Subtype", ""),
                "Magic_And_Spells": char.get("Magic_And_Spells", ""),
                "God": char.get("God", "None"),
                
                "Grappling": char["Grappling"],
                "Melee": char["Melee"],
                "Projectiles": char["Projectiles"],
                "Fencing": char["Fencing"],
                "Reach": char.get("Reach", ""),
                "Skill_Modifier": char["Skill_Modifier"],
                
                "Height_cm": char["Height_cm"],
                "Weight_kg": char["Weight_kg"],
                "Size_Score": char.get("Size_Score", ""),
                
                "Balance": char["Balance"],
                "Quickness": char["Quickness"],
                "Coordination": char["Coordination"],
                "Precision": char["Precision"],
                "Endurance": char["Endurance"],
                "Regeneration": char["Regeneration"],
                "Vigilance": char["Vigilance"],
                "Beauty": char["Beauty"],
                "Stealth": char["Stealth"],
                "Speed": char["Speed"],
                
                "Special": char.get("Special", "Aucun"),
                "Generation_Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            writer.writerow(row)

    print(f"\n[OK] Export terminé -> {filename} ({len(characters)} personnages)")

    if generate_pdfs and _HAS_SHEET_SUPPORT:
        print("📄 Fiches PDF générées dans le dossier 'fiches/' (PERSO-XXX.pdf)")

    # Statistiques rapides
    magic_count = sum(1 for c in characters if c.get("Magic") == "YES")
    print(f"\n[STATS] Magiques : {magic_count}/{len(characters)} ({magic_count/len(characters):.1%})")


def main():
    parser = argparse.ArgumentParser(
        description="[CRPG] Générateur de Personnages - Export CSV (+ fiches PDF optionnelles)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("-n", "--count", type=int, default=100, help="Nombre de personnages")
    parser.add_argument("-o", "--output", type=str, help="Nom du fichier CSV")
    parser.add_argument("-s", "--seed", type=int, help="Seed pour reproductibilité")
    parser.add_argument("-r", "--race", type=str, help="Filtrer par race (ex: Human, Elf)")
    parser.add_argument("-l", "--level", type=int, default=1, help="Niveau du personnage (capital = pièces d'argent × niveau)")
    parser.add_argument("-p", "--pdf", action="store_true", help="Générer les fiches PDF dans fiches/ (PERSO-XXX.pdf). Inclut les sorts connus des Magicien. Nécessite jinja2 + weasyprint.")

    args = parser.parse_args()

    generate_batch(
        count=args.count,
        output=args.output,
        seed=args.seed,
        race_filter=args.race,
        level=args.level,
        generate_pdfs=args.pdf
    )


if __name__ == "__main__":
    main()