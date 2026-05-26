import os
from jinja2 import Template
from weasyprint import HTML
from datetime import datetime

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
    
    char_id = f"PERSO-{next_num:03d}"
    output_path = os.path.join(base_folder, f"{char_id}.pdf")
    
    # Mise à jour des données
    character["ID"] = char_id
    character["Generation_Date"] = datetime.now().strftime("%Y-%m-%d")

    # ====================== TEMPLATE ======================
    template_path = os.path.join("templates", "character_sheet.html")
    
    if not os.path.exists(template_path):
        print(f"❌ Template non trouvé : {template_path}")
        return None

    try:
        with open(template_path, encoding="utf-8") as f:
            template = Template(f.read())
        
        html_content = template.render(character=character)
        
        HTML(string=html_content).write_pdf(output_path)
        print(f"✅ Fiche créée : {output_path} ({char_id})")
        return char_id
        
    except Exception as e:
        print(f"❌ Erreur PDF pour {char_id}: {e}")
        return None