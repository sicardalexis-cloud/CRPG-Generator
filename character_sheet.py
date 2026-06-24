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

    candidates = [
        icon_path,
        os.path.join(os.getcwd(), "assets", "icons", icon_name),
        os.path.abspath(os.path.join("assets", "icons", icon_name)),
    ]
    for cand in candidates:
        if os.path.exists(cand):
            icon_path = cand
            break

    if not os.path.exists(icon_path):
        # Auto-generate a simple reach icon if missing
        if icon_name == 'reach.png':
            try:
                from PIL import Image, ImageDraw
                size = 128
                img = Image.new('RGBA', (size, size), (20, 15, 10, 255))
                d = ImageDraw.Draw(img)
                cy = size // 2
                d.line([(8, cy), (size-28, cy)], fill=(235, 220, 188), width=8)
                d.polygon([(size-28, cy-15), (size-2, cy), (size-28, cy+15)], fill=(250, 238, 205))
                d.line([(24, cy-12), (24, cy+12)], fill=(235, 220, 188), width=5)
                with open(icon_path, 'wb') as f:
                    img.save(f, 'PNG')
            except Exception:
                pass
        if not os.path.exists(icon_path):
            print('WARNING: Icon not found :', icon_path)
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

    # Compute remaining capital in sp (after kit and purchases)
    pocket_bp = character.get("Final_Pocket_Money_BP", 0) or 0
    character["Remaining_Capital_Sp"] = int(round(pocket_bp / 10))

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
        "reach": _load_icon_base64("reach.png"),
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