import os
import base64
from jinja2 import Template
from weasyprint import HTML
from datetime import datetime

def _load_icon_base64(icon_name: str) -> str:
    """Charge une icône PNG depuis assets/icons/ et la retourne en data URI base64."""
    # Chemin relatif au fichier character_sheet.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "assets", "icons", icon_name)
    
    if not os.path.exists(icon_path):
        print(f"⚠️ Icône non trouvée : {icon_path}")
        return ""
    
    with open(icon_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def generate_character_sheet(character: dict, base_folder: str = "fiches"):
    """Génère une fiche PDF avec numérotation automatique"""
    
    # Création du dossier
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    
    # Numérotation automatique
    existing_files = [f for f in os.listdir(base_folder) if f.endswith('.pdf')]
    
    if not existing_files:
        next_num = 1
    else:
        numbers = []
        for f in existing_files:
            try:
                num = int(f.split('-')[-1].replace('.pdf', ''))
                numbers.append(num)
            except:
                pass
        next_num = max(numbers) + 1 if numbers else 1
    
    sheet_id = f"PERSO-{next_num:03d}"
    output_path = os.path.join(base_folder, f"{sheet_id}.pdf")
    
    # On n'écrase pas l'ID original du générateur (utile pour le CSV)
    # On ajoute des infos pour le template
    character["Sheet_ID"] = sheet_id
    if "ID" not in character or not character.get("ID"):
        character["ID"] = sheet_id
    if not character.get("Generation_Date"):
        character["Generation_Date"] = datetime.now().strftime("%Y-%m-%d")

    # ====================== TEMPLATE ======================
    template_path = os.path.join("templates", "character_sheet.html")
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé : {template_path}")
        return None

    # Charger les icônes en base64
    icons = {
        "grappling": _load_icon_base64("grappling.png"),
        "melee": _load_icon_base64("melee.png"),
        "fencing": _load_icon_base64("fencing.png"),
        "projectile": _load_icon_base64("projectile.png"),
    }

    try:
        with open(template_path, encoding="utf-8") as f:
            template = Template(f.read())
        
        html_content = template.render(character=character, icons=icons)
        
        HTML(string=html_content).write_pdf(output_path)
        print(f"✅ Fiche créée : {output_path} ({sheet_id})")
        return sheet_id
        
    except Exception as e:
        print(f"❌ Erreur PDF pour {sheet_id}: {e}")
        return None