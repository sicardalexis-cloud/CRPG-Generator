"""
tools/export_group_equipment.py

Script d'export manuel.

But :
- Lire les fichiers de référence dans :
  premier-tests-grokvsc/data/equipment/systeme groupe/*_Equipement_Complet.txt
- Générer / mettre à jour le fichier :
  premier-tests-grokvsc/data/equipment/group_equipment_pools.py

Règles :
- Ce script est un OUTIL pour le développeur.
- Il est lancé manuellement quand les fichiers .txt sont modifiés.
- Les fichiers .txt restent la source de vérité.
- L'utilisateur (toi) est le seul à modifier les .txt.

Usage typique :
    python tools/export_group_equipment.py

Pour l'instant : version de développement / test de parsing.
"""

import re
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(__file__).parent.parent
REFERENCE_DIR = BASE_DIR / "data" / "equipment" / "systeme groupe"
OUTPUT_FILE = BASE_DIR / "data" / "equipment" / "group_equipment_pools.py"

# Mapping nom de fichier → group_id
FILE_TO_GROUP = {
    "Groupe1_Cote_des_Epees_Equipement_Complet.txt": "Groupe1_Cote_des_Epees",
    "Groupe2_Sud_Marchand_Equipement_Complet.txt": "Groupe2_Sud_Marchand",
    "Groupe3_Coeur_Continental_Equipement_Complet.txt": "Groupe3_Coeur_Continental",
    "Groupe4_Vilhon_Est_Equipement_Complet.txt": "Groupe4_Vilhon_Est",
    "Groupe5_Nord_Sauvage_Equipement_Complet.txt": "Groupe5_Nord_Sauvage",
    "Groupe6_Bloc_Nain_Equipement_Complet.txt": "Groupe6_Bloc_Nain",
    "Groupe7_Marches_Argent_Equipement_Complet.txt": "Groupe7_Marches_Argent",
    "Groupe8_Mulhorand_Equipement_Complet.txt": "Groupe8_Mulhorand",
    "Groupe9_Thay_Equipement_Complet.txt": "Groupe9_Thay",
    "Groupe10_Rashemen_Equipement_Complet.txt": "Groupe10_Rashemen",
    "Groupe11_Moonshae_Isles_Equipement_Complet.txt": "Groupe11_Moonshae",
    "Groupe12_Old_Empires_Equipement_Complet.txt": "Groupe12_Old_Empires",
    "Groupe13_Evermeet_Equipement_Complet.txt": "Groupe13_Evermeet",
    "Groupe14_Underdark_Equipement_Complet.txt": "Groupe14_Underdark",
}

# =============================================================================
# PARSING
# =============================================================================

# Regex améliorée pour une ligne d'item (avec support de la colonne Encombrement)
# Gère :
# - Noms en **bold**
# - Prix avec bp/sp/gp
# - Tech simple ou "Tech 4-5"
# - Rareté : Toujours / Commun / Rare / Très rare
# - Commentaires optionnels entre parenthèses
# - Colonne Encombrement (entier) à la fin de la ligne (nouvelle fonctionnalité)
ITEM_REGEX = re.compile(
    r'^\s*'
    r'\*{0,2}(?P<name>[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9\'\-\s\(\)/,]+?)\*{0,2}'
    r'\s+'
    r'(?P<price>\d+(?:\.\d+)?)\s*(?P<unit>sp|bp|gp)'
    r'\s+'
    r'Tech\s+(?P<tech>\d+(?:-\d+)?)'
    r'\s+'
    r'(?P<rarity>Toujours|Commun|Rare|Très rare)'
    r'(?:\s*\((?P<notes>[^)]+)\))?'
    r'(?:\s+(?P<encumbrance>\d+))?$',
    re.IGNORECASE
)


def normalize_item_name(raw_name: str) -> str:
    """Nettoie le nom de l'item (retire les ** markdown, espaces multiples)."""
    name = raw_name.strip()
    name = name.replace("**", "")
    name = re.sub(r'\s+', ' ', name)
    return name.strip()


def parse_price_to_sp(price: float, unit: str) -> float:
    """Convertit tout en pièces d'argent (sp) pour cohérence."""
    unit = unit.lower()
    if unit == "sp":
        return price
    elif unit == "bp":
        return price / 10.0
    elif unit == "gp":
        return price * 10.0
    return price


def parse_file(filepath: Path) -> list[dict]:
    """Parse un fichier d'équipement complet et retourne une liste d'items."""
    items = []
    text = filepath.read_text(encoding="utf-8", errors="ignore")

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("=") or line.startswith("-") or line.startswith("#"):
            continue

        match = ITEM_REGEX.search(line)
        if match:
            data = match.groupdict()
            item = {
                "name": normalize_item_name(data["name"]),
                "price_sp": round(parse_price_to_sp(float(data["price"]), data["unit"]), 2),
                "tech": data["tech"],
                "rarity": data["rarity"].strip(),
                "notes": data["notes"].strip() if data["notes"] else None,
                "encumbrance": int(data["encumbrance"]) if data.get("encumbrance") else None,
            }
            items.append(item)

    return items


def export_all_groups():
    """Parcourt tous les fichiers et construit la structure finale."""
    result = {}

    for filename, group_id in FILE_TO_GROUP.items():
        filepath = REFERENCE_DIR / filename
        if not filepath.exists():
            print(f"[WARN] Fichier manquant : {filename}")
            result[group_id] = []
            continue

        items = parse_file(filepath)
        result[group_id] = items
        print(f"[OK] {group_id}: {len(items)} items extraits de {filename}")

    return result


def generate_python_code(pools: dict) -> str:
    """Génère le contenu complet du fichier group_equipment_pools.py."""
    lines = [
        '"""',
        'data/equipment/group_equipment_pools.py',
        '',
        'Pools d\'équipement par groupe (14 groupes).',
        '',
        '>>> FICHIER GÉNÉRÉ AUTOMATIQUEMENT <<<',
        '>>> Ne pas éditer manuellement. Utiliser tools/export_group_equipment.py <<<',
        '',
        'Source des données :',
        'premier-tests-grokvsc/data/equipment/systeme groupe/*_Equipement_Complet.txt',
        '"""',
        '',
        'from typing import Dict, List, TypedDict',
        '',
        '',
        'class EquipmentItem(TypedDict):',
        '    name: str',
        '    price_sp: float',
        '    tech: str',
        '    rarity: str',
        '    notes: str | None',
        '    encumbrance: int | None',  # Nouvelle colonne : valeur d'encombrement (1-6)
        '',
        '',
        '# =============================================================================',
        '# POOLS PAR GROUPE',
        '# =============================================================================',
        '',
        'GROUP_EQUIPMENT_POOLS: Dict[str, List[EquipmentItem]] = {',
    ]

    for group_id, items in pools.items():
        lines.append(f'    "{group_id}": [')
        for item in items:
            notes = f'"{item["notes"]}"' if item["notes"] else "None"
            enc = item.get("encumbrance")
            enc_str = str(enc) if enc is not None else "None"
            line = (
                f'        {{"name": "{item["name"]}", '
                f'"price_sp": {item["price_sp"]}, '
                f'"tech": "{item["tech"]}", '
                f'"rarity": "{item["rarity"]}", '
                f'"notes": {notes}, '
                f'"encumbrance": {enc_str}}},'
            )
            lines.append(line)
        lines.append('    ],')
        lines.append('')

    lines.append('}')
    lines.append('')

    # Ajout des fonctions utilitaires
    lines.extend([
        '# =============================================================================',
        '# FONCTIONS UTILITAIRES (générées)',
        '# =============================================================================',
        '',
        'def get_group_pool(group_id: str) -> List[EquipmentItem]:',
        '    """Retourne la liste des items disponibles pour un groupe donné."""',
        '    return GROUP_EQUIPMENT_POOLS.get(group_id, [])',
        '',
        '',
        'def get_item_with_final_price(group_id: str, item_name: str) -> dict | None:',
        '    """',
        '    Retourne l\'item avec son prix final (en tenant compte du surcoût si rare).',
        '    Surcoûts appliqués uniquement pendant les achats post-kit :',
        '        - Rare        → +50%',
        '        - Très rare   → +100%',
        '    """',
        '    pool = get_group_pool(group_id)',
        '    for item in pool:',
        '        if item["name"].lower() == item_name.lower():',
        '            price = item["price_sp"]',
        '            rarity = item["rarity"]',
        '',
        '            if rarity == "Rare":',
        '                final_price = round(price * 1.5, 2)',
        '            elif rarity == "Très rare":',
        '                final_price = round(price * 2.0, 2)',
        '            else:',
        '                final_price = price',
        '',
        '            return {',
        '                **item,',
        '                "final_price_sp": final_price,',
        '                "surcharge_applied": rarity in ("Rare", "Très rare")',
        '            }',
        '    return None',
        '',
        '',
        'def is_item_in_group(group_id: str, item_name: str) -> bool:',
        '    """Vérifie si un item est disponible dans le pool du groupe."""',
        '    pool = get_group_pool(group_id)',
        '    return any(i["name"].lower() == item_name.lower() for i in pool)',
        '',
        '',
        'def get_weapon_encumbrance(group_id: str, item_name: str) -> int | None:',
        '    """Retourne la valeur d\'encombrement d\'une arme dans un groupe donné."""',
        '    pool = get_group_pool(group_id)',
        '    for item in pool:',
        '        if item["name"].lower() == item_name.lower():',
        '            return item.get("encumbrance")',
        '    return None',
        '',
        '',
        'def get_item_with_final_price(group_id: str, item_name: str) -> dict | None:',
        '    """',
        '    Retourne l\'item enrichi avec :',
        '    - final_price_sp (prix avec surcoût Rare/Très rare si applicable)',
        '    - surcharge_applied (bool)',
        '    - encumbrance (valeur d\'encombrement si présente)',
        '    """',
        '    pool = get_group_pool(group_id)',
        '    for item in pool:',
        '        if item["name"].lower() == item_name.lower():',
        '            price = item["price_sp"]',
        '            rarity = item["rarity"]',
        '',
        '            if rarity == "Rare":',
        '                final_price = round(price * 1.5, 2)',
        '            elif rarity == "Très rare":',
        '                final_price = round(price * 2.0, 2)',
        '            else:',
        '                final_price = price',
        '',
        '            return {',
        '                **item,',
        '                "final_price_sp": final_price,',
        '                "surcharge_applied": rarity in ("Rare", "Très rare"),',
        '                "encumbrance": item.get("encumbrance"),',
        '            }',
        '    return None',
    ])

    return '\n'.join(lines)


def write_pools_file(pools: dict):
    """Écrit le fichier group_equipment_pools.py avec les données fraîches."""
    code = generate_python_code(pools)

    # On conserve le header et les imports existants si possible,
    # mais pour simplifier on réécrit tout le fichier.
    OUTPUT_FILE.write_text(code, encoding="utf-8")
    print(f"\n[EXPORT] Fichier mis à jour : {OUTPUT_FILE}")


if __name__ == "__main__":
    print("=== Export des groupes d'équipement ===\n")
    pools = export_all_groups()

    print("\n=== Résumé ===")
    for gid, items in pools.items():
        print(f"{gid}: {len(items)} items")

    write_pools_file(pools)
    print("\n[TERMINÉ] Export réussi.")
