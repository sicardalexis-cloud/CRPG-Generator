# knowledge_data.py
import random
from typing import Dict
from language_data import generate_languages
from skill_data import get_num_active_skills


# ====================== CRAFT WEIGHTS (52 métiers) ======================
craft_weights: Dict[str, int] = {
    "Maçonnerie": 22, "Forge et métallurgie": 20, "Travail du cuir et tannerie": 18,
    "Charpenterie et travail du bois": 17, "Comptabilité et gestion de biens": 15,
    "Cuisine raffinée": 12, "Herboristerie et préparation de potions": 11,
    "Navigation (terrestre et maritime)": 10, "Architecture": 10,
    "Teinture et coloration": 9, "Ébénisterie et marqueterie": 9,
    "Serrurerie et mécanismes": 8, "Cartographie": 8,
    "Travail du verre et verrerie": 7, "Céramique et poterie": 7,
    "Fabrication d’armes et armures": 7, "Élevage et dressage": 6,
    "Apiculture": 6, "Tissage et filage": 6,
    "Fabrication de chandelles et savon": 5, "Construction navale": 5,
    "Fabrication de voiles et cordages": 5, "Travail de la pierre": 5,
    "Viticulture et vinification": 5, "Brasserie et distillation": 5,
    "Joaillerie et orfèvrerie": 4, "Alchimie théorique et pratique": 4,
    "Broderie et couture fine": 4, "Calligraphie et enluminure": 3,
    "Fabrication d’instruments de musique": 3, "Reliure de livres": 3,
    "Sculpture sur pierre et bois": 3, "Mosaïque et fresque": 3,
    "Horlogerie et mécanismes complexes": 2, "Fabrication de lentilles et optique": 2,
    "Parfumerie et cosmétique": 2, "Taxidermie": 2,
    "Gravure sur métal et gemmes": 2, "Fabrication de feux d’artifice": 2,
    "Travail de l’os et de l’ivoire": 2, "Fabrication de papier et encre": 2,
    "Conserverie et salaison": 2, "Fabrication de teintures rares": 2,
    "Orfèvrerie magique (théorique)": 1, "Herboristerie exotique": 1,
    "Fabrication d’objets rituels": 1,
}

# ====================== MODIFICATEURS (ethnicity + region + settlement) ======================
ethnicity_craft_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== HUMAINS ====================
    "Chondathan":      {"Comptabilité et gestion de biens": 4.0, "Navigation (terrestre et maritime)": 3.5, "Cartographie": 3.0, "Architecture": 2.8, "Teinture et coloration": 2.5},
    "Tethyrian":       {"Maçonnerie": 3.2, "Charpenterie et travail du bois": 3.5, "Élevage et dressage": 3.0, "Comptabilité et gestion de biens": 2.5, "Architecture": 2.5},
    "Calishite":       {"Joaillerie et orfèvrerie": 4.8, "Alchimie théorique et pratique": 4.2, "Parfumerie et cosmétique": 4.0, "Calligraphie et enluminure": 3.5, "Fabrication de teintures rares": 3.0},
    "Damaran":         {"Maçonnerie": 4.2, "Forge et métallurgie": 4.7, "Travail du cuir et tannerie": 3.8, "Fabrication d’armes et armures": 3.5, "Travail de la pierre": 3.0},
    "Illuskan":        {"Navigation (terrestre et maritime)": 4.8, "Construction navale": 4.5, "Fabrication de voiles et cordages": 4.0, "Pêche": 3.8, "Travail du cuir et tannerie": 2.8},
    "Mulan":           {"Comptabilité et gestion de biens": 4.5, "Architecture": 4.0, "Calligraphie et enluminure": 3.8, "Reliure de livres": 3.0},
    "Rashemi":         {"Herboristerie et préparation de potions": 4.8, "Élevage et dressage": 3.5, "Apiculture": 3.2, "Fabrication d’objets rituels": 3.0},
    "Turami":          {"Cuisine raffinée": 4.2, "Viticulture et vinification": 4.0, "Brasserie et distillation": 4.0, "Conserverie et salaison": 2.8},
    "Uthgardt":        {"Travail du cuir et tannerie": 4.0, "Fabrication d’armes et armures": 3.8, "Élevage et dressage": 3.5, "Chasse": 3.5, "Cueillette et survie en milieu sauvage": 3.0},
    "Chultan":         {"Herboristerie et préparation de potions": 4.5, "Alchimie théorique et pratique": 4.0, "Herboristerie exotique": 4.0, "Chasse": 3.2},
    "Shaaran":         {"Élevage et dressage": 4.5, "Chasse": 4.0, "Cueillette et survie en milieu sauvage": 3.8},
    "Ffolk":           {"Cuisine raffinée": 3.5, "Brasserie et distillation": 3.5, "Pêche": 4.0, "Navigation (terrestre et maritime)": 3.0},
    "Sossrim":         {"Élevage et dressage": 4.0, "Chasse": 4.2, "Travail du cuir et tannerie": 3.5, "Cueillette et survie en milieu sauvage": 3.0},
    "Vaasan":          {"Maçonnerie": 4.0, "Forge et métallurgie": 4.0, "Travail de la pierre": 3.8},
    "Bedine":          {"Cueillette et survie en milieu sauvage": 4.5, "Chasse": 3.8, "Fabrication de chandelles et savon": 2.5},

    # ==================== DEMI-ELFES ====================
    "Half-Elf":        {"Herboristerie et préparation de potions": 3.8, "Calligraphie et enluminure": 3.5, "Fabrication d’instruments de musique": 3.5,
                        "Comptabilité et gestion de biens": 3.2, "Navigation (terrestre et maritime)": 3.0, "Architecture": 2.8,
                        "Cuisine raffinée": 2.8, "Reliure de livres": 2.8},
    "Half-Elf Moon":   {"Herboristerie et préparation de potions": 4.0, "Calligraphie et enluminure": 4.0, "Fabrication d’instruments de musique": 3.8},
    "Half-Elf Wood":   {"Herboristerie et préparation de potions": 4.5, "Tissage et filage": 3.5, "Cueillette et survie en milieu sauvage": 3.2},
    "Half-Elf Sun":    {"Calligraphie et enluminure": 4.2, "Joaillerie et orfèvrerie": 3.5, "Fabrication d’instruments de musique": 3.5},

    # ==================== ELFES ====================
    "Elf Moon":        {"Herboristerie et préparation de potions": 4.2, "Calligraphie et enluminure": 4.0, "Fabrication d’instruments de musique": 4.0, "Reliure de livres": 3.0},
    "Elf Sun":         {"Calligraphie et enluminure": 4.5, "Joaillerie et orfèvrerie": 4.0, "Fabrication d’instruments de musique": 3.5},
    "Elf Wood":        {"Herboristerie et préparation de potions": 5.0, "Tissage et filage": 3.8, "Fabrication d’instruments de musique": 3.5, "Sculpture sur pierre et bois": 3.0},
    "Elf Wild":        {"Herboristerie et préparation de potions": 4.8, "Chasse": 4.0, "Cueillette et survie en milieu sauvage": 4.5},
    "Elf Drow":        {"Serrurerie et mécanismes": 4.5, "Alchimie théorique et pratique": 4.5, "Joaillerie et orfèvrerie": 4.0, "Fabrication de teintures rares": 3.5},
    "Elf Sea":         {"Navigation (terrestre et maritime)": 4.5, "Construction navale": 4.0, "Pêche": 4.0, "Fabrication de voiles et cordages": 3.5},
    "Elf Star":        {"Calligraphie et enluminure": 4.2, "Fabrication d’instruments de musique": 4.0, "Fabrication de lentilles et optique": 3.5},
    "Elf Avariel":     {"Fabrication d’instruments de musique": 4.0, "Fabrication de lentilles et optique": 3.8},
    "Elf Lythari":     {"Herboristerie et préparation de potions": 5.0, "Tissage et filage": 3.5, "Fabrication d’instruments de musique": 3.2},

    # ==================== NAINS ====================
    "Nain":            {"Maçonnerie": 5.0, "Forge et métallurgie": 5.5, "Travail de la pierre": 5.0, "Joaillerie et orfèvrerie": 4.2, "Fabrication d’armes et armures": 4.0},
    "Shield Dwarf":    {"Forge et métallurgie": 5.8, "Maçonnerie": 5.2, "Fabrication d’armes et armures": 4.5, "Travail de la pierre": 4.0},
    "Gold Dwarf":      {"Forge et métallurgie": 5.0, "Joaillerie et orfèvrerie": 5.0, "Gravure sur métal et gemmes": 4.0},
    "Gray Dwarf":      {"Serrurerie et mécanismes": 5.0, "Alchimie théorique et pratique": 4.5, "Fabrication d’armes et armures": 4.0},
    "Urdunnir":        {"Maçonnerie": 5.5, "Travail de la pierre": 5.8, "Joaillerie et orfèvrerie": 4.0},

    # ==================== HALFELINS & GNOMES ====================
    "Halfelin":        {"Cuisine raffinée": 4.2, "Brasserie et distillation": 4.0, "Tissage et filage": 3.8, "Broderie et couture fine": 3.5},
    "Lightfoot Halfling": {"Cuisine raffinée": 4.5, "Tissage et filage": 4.0, "Broderie et couture fine": 3.8},
    "Strongheart Halfling": {"Cuisine raffinée": 4.0, "Élevage et dressage": 4.0, "Brasserie et distillation": 3.8},
    "Ghostwise Halfling": {"Herboristerie et préparation de potions": 4.5, "Fabrication d’instruments de musique": 3.5},

    "Gnome":           {"Serrurerie et mécanismes": 4.8, "Horlogerie et mécanismes complexes": 4.5, "Travail du verre et verrerie": 4.0, "Fabrication d’instruments de musique": 3.8},
    "Rock Gnome":      {"Serrurerie et mécanismes": 5.0, "Horlogerie et mécanismes complexes": 5.0, "Travail du verre et verrerie": 4.2},
    "Forest Gnome":    {"Herboristerie et préparation de potions": 4.8, "Fabrication d’instruments de musique": 4.0},

    # ==================== AUTRES RACES ====================
    "Half-Orc":        {"Forge et métallurgie": 4.5, "Travail du cuir et tannerie": 4.0, "Fabrication d’armes et armures": 4.2, "Chasse": 3.5},
    "Orc":             {"Forge et métallurgie": 4.8, "Fabrication d’armes et armures": 4.5, "Travail du cuir et tannerie": 3.8},
    "Gray Orc":        {"Forge et métallurgie": 4.5, "Alchimie théorique et pratique": 3.8},

    "Aasimar":         {"Calligraphie et enluminure": 4.0, "Fabrication d’instruments de musique": 3.5, "Fabrication d’objets rituels": 4.0},
    "Tiefling":        {"Alchimie théorique et pratique": 4.5, "Parfumerie et cosmétique": 4.0, "Fabrication de feux d’artifice": 3.5, "Joaillerie et orfèvrerie": 3.2},
    "Dragonborn":      {"Forge et métallurgie": 4.8, "Fabrication d’armes et armures": 4.5, "Joaillerie et orfèvrerie": 4.0},
    "Firbolg":         {"Herboristerie et préparation de potions": 5.0, "Élevage et dressage": 4.0, "Fabrication d’objets rituels": 3.8},
    "Kenku":           {"Broderie et couture fine": 4.0, "Calligraphie et enluminure": 4.0, "Fabrication d’instruments de musique": 4.5, "Reliure de livres": 3.5},
    "Lizardfolk":      {"Travail du cuir et tannerie": 4.5, "Taxidermie": 4.0, "Alchimie théorique et pratique": 3.8, "Herboristerie et préparation de potions": 3.5},
    "Triton":          {"Navigation (terrestre et maritime)": 4.5, "Construction navale": 4.0, "Pêche": 4.2},
    "Aarakocra":       {"Fabrication d’instruments de musique": 4.0, "Fabrication de lentilles et optique": 3.5},
    "Goliath":         {"Maçonnerie": 4.5, "Forge et métallurgie": 4.0, "Travail de la pierre": 4.2},
    "Centaur":         {"Élevage et dressage": 4.8, "Herboristerie et préparation de potions": 3.8, "Tissage et filage": 3.5},

    # ==================== FALLBACK ====================
    "Default":         {}
}

# ====================== MODIFICATEURS PAR RÉGION (version complète ~133 régions) ======================
region_craft_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== NORTHWEST & SWORD COAST ====================
    "Sword Coast":          {"Navigation (terrestre et maritime)": 4.2, "Construction navale": 4.0, "Pêche": 3.8, "Comptabilité et gestion de biens": 3.0},
    "Waterdeep":            {"Comptabilité et gestion de biens": 4.8, "Calligraphie et enluminure": 3.8, "Joaillerie et orfèvrerie": 3.5, "Architecture": 3.2},
    "Neverwinter":          {"Architecture": 4.2, "Forge et métallurgie": 3.8, "Construction navale": 3.5, "Alchimie théorique et pratique": 3.2},
    "Luskan":               {"Navigation (terrestre et maritime)": 4.5, "Construction navale": 4.2, "Pêche": 4.0, "Fabrication d’armes et armures": 3.5},
    "Baldur's Gate":        {"Comptabilité et gestion de biens": 4.2, "Navigation (terrestre et maritime)": 3.8, "Alchimie théorique et pratique": 3.5},
    "Candlekeep":           {"Calligraphie et enluminure": 5.0, "Reliure de livres": 4.8, "Astronomie et navigation stellaire": 3.5},

    # ==================== NORTH & SAVAGE FRONTIER ====================
    "Silver Marches":       {"Forge et métallurgie": 4.2, "Maçonnerie": 3.8, "Travail de la pierre": 3.5, "Élevage et dressage": 3.0},
    "Icewind Dale":         {"Chasse": 4.5, "Cueillette et survie en milieu sauvage": 4.2, "Travail du cuir et tannerie": 3.8, "Élevage et dressage": 3.5},
    "High Forest":          {"Herboristerie et préparation de potions": 4.8, "Fabrication d’instruments de musique": 4.0, "Tissage et filage": 3.5},
    "Savage Frontier":      {"Chasse": 4.2, "Cueillette et survie en milieu sauvage": 4.0, "Travail du cuir et tannerie": 3.8},
    "Uthgardt Lands":       {"Chasse": 4.5, "Travail du cuir et tannerie": 4.0, "Fabrication d’armes et armures": 3.8},
    "Spine of the World":   {"Chasse": 4.5, "Travail du cuir et tannerie": 4.0, "Forge et métallurgie": 3.8},

    # ==================== HEARTLANDS & DALELANDS ====================
    "Dalelands":            {"Herboristerie et préparation de potions": 4.5, "Élevage et dressage": 4.0, "Apiculture": 3.8, "Tissage et filage": 3.2},
    "Cormyr":               {"Maçonnerie": 4.0, "Architecture": 4.2, "Comptabilité et gestion de biens": 3.8, "Calligraphie et enluminure": 3.5},
    "Sembia":               {"Comptabilité et gestion de biens": 5.0, "Teinture et coloration": 3.8, "Joaillerie et orfèvrerie": 3.5},
    "Thesk":                {"Comptabilité et gestion de biens": 4.2, "Navigation (terrestre et maritime)": 3.5},
    "Impiltur":             {"Forge et métallurgie": 4.0, "Fabrication d’armes et armures": 3.8, "Maçonnerie": 3.5},
    "Western Heartlands":   {"Élevage et dressage": 4.0, "Comptabilité et gestion de biens": 3.5, "Herboristerie et préparation de potions": 3.2},

    # ==================== SOUTH & SHINING SOUTH ====================
    "Calimshan":            {"Joaillerie et orfèvrerie": 5.0, "Alchimie théorique et pratique": 4.5, "Parfumerie et cosmétique": 4.2, "Fabrication de teintures rares": 4.0, "Calligraphie et enluminure": 3.5},
    "Tethyr":               {"Viticulture et vinification": 4.5, "Brasserie et distillation": 4.0, "Cuisine raffinée": 3.8, "Élevage et dressage": 3.5},
    "Amn":                  {"Comptabilité et gestion de biens": 5.0, "Joaillerie et orfèvrerie": 3.8, "Teinture et coloration": 3.5},
    "Chult":                {"Herboristerie exotique": 5.0, "Herboristerie et préparation de potions": 4.5, "Chasse": 4.0, "Cueillette et survie en milieu sauvage": 4.2},
    "Shaar":                {"Élevage et dressage": 4.8, "Chasse": 4.2, "Cueillette et survie en milieu sauvage": 4.0},
    "Halruaa":              {"Alchimie théorique et pratique": 4.8, "Fabrication d’objets rituels": 4.5, "Calligraphie et enluminure": 4.0},
    "Vilhon Reach":         {"Navigation (terrestre et maritime)": 4.0, "Construction navale": 3.8, "Cuisine raffinée": 3.5},
    "Dragon Coast":         {"Navigation (terrestre et maritime)": 4.5, "Pêche": 4.0, "Construction navale": 3.8},

    # ==================== EAST & UNAPPROACHABLE EAST ====================
    "Moonsea":              {"Forge et métallurgie": 4.5, "Fabrication d’armes et armures": 4.2, "Maçonnerie": 3.8},
    "Rashemen":             {"Herboristerie et préparation de potions": 5.0, "Fabrication d’objets rituels": 4.2, "Apiculture": 3.5},
    "Thay":                 {"Alchimie théorique et pratique": 5.0, "Fabrication d’objets rituels": 4.5, "Calligraphie et enluminure": 4.0},
    "Aglarond":             {"Herboristerie et préparation de potions": 4.5, "Fabrication d’instruments de musique": 3.8, "Tissage et filage": 3.5},
    "The Vast":             {"Maçonnerie": 4.0, "Charpenterie et travail du bois": 3.8, "Architecture": 3.5},
    "Mulhorand":            {"Calligraphie et enluminure": 4.5, "Architecture": 4.0, "Reliure de livres": 3.8},
    "Unther":               {"Maçonnerie": 4.0, "Forge et métallurgie": 3.8},
    "Chessenta":            {"Fabrication d’armes et armures": 4.2, "Architecture": 3.8},

    # ==================== INTERIOR & COLD LANDS ====================
    "Anauroch":             {"Cueillette et survie en milieu sauvage": 4.5, "Chasse": 4.0},
    "Damara":               {"Maçonnerie": 4.2, "Forge et métallurgie": 4.0, "Élevage et dressage": 3.8},
    "Vaasa":                {"Maçonnerie": 4.0, "Forge et métallurgie": 4.0, "Travail de la pierre": 3.8},
    "Narfell":              {"Élevage et dressage": 4.5, "Chasse": 4.0, "Travail du cuir et tannerie": 3.8},
    "Great Dale":           {"Herboristerie et préparation de potions": 4.2, "Tissage et filage": 3.8},

    # ==================== FORESTS, MOORS & WILD AREAS ====================
    "Cormanthor":           {"Herboristerie et préparation de potions": 4.5, "Calligraphie et enluminure": 4.0, "Fabrication d’instruments de musique": 3.8},
    "Misty Forest":         {"Herboristerie et préparation de potions": 4.5, "Chasse": 4.0},
    "Ardeep Forest":        {"Herboristerie et préparation de potions": 4.2, "Fabrication d’instruments de musique": 3.5},
    "Luirwood":             {"Herboristerie et préparation de potions": 4.3, "Fabrication d’objets rituels": 3.5},
    "High Moor":            {"Cueillette et survie en milieu sauvage": 4.0, "Chasse": 3.8},
    "Trollclaws":           {"Chasse": 4.2, "Travail du cuir et tannerie": 3.8},
    "Evermoors":            {"Élevage et dressage": 4.0, "Chasse": 3.8},

    # ==================== CITIES & SPECIAL ZONES ====================
    "Silverymoon":          {"Calligraphie et enluminure": 4.2, "Herboristerie et préparation de potions": 4.0, "Architecture": 3.8},
    "Zhentil Keep":         {"Forge et métallurgie": 4.0, "Fabrication d’armes et armures": 4.2, "Alchimie théorique et pratique": 3.5},
    "Elturel":              {"Maçonnerie": 3.8, "Architecture": 3.5, "Comptabilité et gestion de biens": 3.2},
    "Turmish":              {"Maçonnerie": 4.0, "Architecture": 3.8, "Viticulture et vinification": 3.5},
    "Lake of Steam":        {"Pêche": 4.0, "Construction navale": 3.5, "Cuisine raffinée": 3.2},

    # ==================== ISLANDS & REMOTE AREAS ====================
    "Moonshae Isles":       {"Pêche": 4.2, "Construction navale": 4.0, "Fabrication de voiles et cordages": 3.5},
    "Nelanther Isles":      {"Navigation (terrestre et maritime)": 4.5, "Pêche": 4.0, "Construction navale": 3.8},
    "Evermeet":             {"Herboristerie et préparation de potions": 4.5, "Fabrication d’instruments de musique": 4.2, "Calligraphie et enluminure": 4.0},
    "Lantan":               {"Horlogerie et mécanismes complexes": 4.8, "Serrurerie et mécanismes": 4.2, "Fabrication de lentilles et optique": 3.8},
    "Mintarn":              {"Construction navale": 4.5, "Pêche": 4.0},
    "Orlumbor":             {"Construction navale": 4.8, "Fabrication de voiles et cordages": 4.0},

    # ==================== AUTRES RÉGIONS ====================
    "The North":            {"Chasse": 4.2, "Travail du cuir et tannerie": 3.8, "Forge et métallurgie": 3.5},
    "The High Moor":        {"Cueillette et survie en milieu sauvage": 4.0, "Chasse": 3.8},
    "The Trollclaws":       {"Chasse": 4.2, "Travail du cuir et tannerie": 3.8},
    "The Evermoors":        {"Élevage et dressage": 4.0, "Chasse": 3.8},
    "The Great Dale":       {"Herboristerie et préparation de potions": 4.2, "Tissage et filage": 3.8},
    "The Shaar":            {"Élevage et dressage": 4.8, "Chasse": 4.2, "Cueillette et survie en milieu sauvage": 4.0},
    "The Vilhon Reach":     {"Navigation (terrestre et maritime)": 4.0, "Construction navale": 3.8},
    "The Dragon Coast":     {"Navigation (terrestre et maritime)": 4.5, "Pêche": 4.0},
    "The Unapproachable East": {"Alchimie théorique et pratique": 4.0, "Herboristerie et préparation de potions": 3.8},
    "The Cold Lands":       {"Chasse": 4.5, "Travail du cuir et tannerie": 4.0},
    "The Shining South":    {"Joaillerie et orfèvrerie": 4.0, "Alchimie théorique et pratique": 3.8},
    "The Heartlands":       {"Comptabilité et gestion de biens": 4.0, "Élevage et dressage": 3.5},
    "The Sword Coast North": {"Navigation (terrestre et maritime)": 4.2, "Construction navale": 3.8},
    "The Western Heartlands": {"Élevage et dressage": 4.0, "Comptabilité et gestion de biens": 3.5},
    "The Moonsea North":    {"Forge et métallurgie": 4.2, "Fabrication d’armes et armures": 4.0},
    "The Moonsea South":    {"Maçonnerie": 4.0, "Architecture": 3.8},
    "The Dalelands East":   {"Herboristerie et préparation de potions": 4.5, "Élevage et dressage": 4.0},
    "The Dalelands West":   {"Herboristerie et préparation de potions": 4.3, "Apiculture": 3.8},
    "The Forgotten Forest": {"Herboristerie et préparation de potions": 4.5, "Fabrication d’instruments de musique": 3.8},
    "The Chondalwood":      {"Herboristerie et préparation de potions": 4.5, "Tissage et filage": 3.5},
    "The Wealdath":         {"Herboristerie et préparation de potions": 4.8, "Chasse": 4.0},
    "The Forest of Amtar":  {"Herboristerie et préparation de potions": 4.5, "Cueillette et survie en milieu sauvage": 4.0},
    "The Thunder Peaks":    {"Maçonnerie": 4.0, "Travail de la pierre": 3.8},
    "The Desert of Anauroch": {"Cueillette et survie en milieu sauvage": 4.5, "Chasse": 4.0},
    "The Endless Wastes":   {"Cueillette et survie en milieu sauvage": 4.5, "Chasse": 4.2},
    "The Plateau of Thay":  {"Alchimie théorique et pratique": 4.8, "Fabrication d’objets rituels": 4.5},
    "The Lake of Dragons":  {"Navigation (terrestre et maritime)": 4.0, "Pêche": 3.8},
    "The Alamber Sea":      {"Navigation (terrestre et maritime)": 4.5, "Pêche": 4.0},
    "The Inner Sea":        {"Navigation (terrestre et maritime)": 4.2, "Pêche": 3.8},
    "The Trackless Sea":    {"Navigation (terrestre et maritime)": 4.5, "Construction navale": 4.0, "Pêche": 4.0},

    # ==================== FALLBACK ====================
    "Default":              {}
}

# ====================== MODIFICATEURS PAR TYPE DE SETTLEMENT ======================
settlement_craft_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== GRANDES VILLES & MÉTROPOLES ====================
    "Metropolis":          {"Comptabilité et gestion de biens": 4.5, "Joaillerie et orfèvrerie": 4.0, "Calligraphie et enluminure": 3.8, "Alchimie théorique et pratique": 3.5, "Architecture": 3.5},
    "Large City":          {"Comptabilité et gestion de biens": 4.2, "Joaillerie et orfèvrerie": 3.8, "Calligraphie et enluminure": 3.5, "Serrurerie et mécanismes": 3.0, "Architecture": 3.0},
    "Small City":          {"Architecture": 3.5, "Comptabilité et gestion de biens": 3.5, "Serrurerie et mécanismes": 3.2, "Joaillerie et orfèvrerie": 3.0},

    # ==================== VILLES MOYENNES & BOURGS ====================
    "Large Town":          {"Maçonnerie": 3.5, "Charpenterie et travail du bois": 3.5, "Architecture": 3.2, "Comptabilité et gestion de biens": 3.0},
    "Small Town":          {"Maçonnerie": 3.2, "Charpenterie et travail du bois": 3.2, "Herboristerie et préparation de potions": 2.8, "Cuisine raffinée": 2.5},
    "Town":                {"Maçonnerie": 3.0, "Charpenterie et travail du bois": 3.0, "Comptabilité et gestion de biens": 2.8},

    # ==================== PETITS VILLAGES & CAMPAGNE ====================
    "Village":             {"Maçonnerie": 3.5, "Charpenterie et travail du bois": 3.5, "Herboristerie et préparation de potions": 3.0, "Élevage et dressage": 2.8},
    "Hamlet":              {"Maçonnerie": 3.0, "Charpenterie et travail du bois": 3.2, "Herboristerie et préparation de potions": 3.2, "Élevage et dressage": 3.0},
    "Thorp":               {"Charpenterie et travail du bois": 3.5, "Herboristerie et préparation de potions": 3.0, "Élevage et dressage": 3.2},

    # ==================== ZONES RURALES & SPÉCIALISÉES ====================
    "Rural":               {"Élevage et dressage": 4.0, "Apiculture": 3.8, "Herboristerie et préparation de potions": 3.5, "Tissage et filage": 3.0},
    "Farming Village":     {"Élevage et dressage": 4.2, "Herboristerie et préparation de potions": 3.5, "Cuisine raffinée": 3.0},
    "Fishing Village":     {"Pêche": 4.5, "Construction navale": 3.8, "Fabrication de voiles et cordages": 3.5, "Cuisine raffinée": 3.0},
    "Mining Town":         {"Maçonnerie": 4.0, "Travail de la pierre": 4.2, "Forge et métallurgie": 4.0, "Fabrication d’armes et armures": 3.5},

    # ==================== ZONES MILITAIRES & FORTIFIÉES ====================
    "Fortress":            {"Forge et métallurgie": 4.5, "Fabrication d’armes et armures": 4.5, "Maçonnerie": 4.0, "Serrurerie et mécanismes": 3.5},
    "Citadel":             {"Maçonnerie": 4.5, "Forge et métallurgie": 4.2, "Fabrication d’armes et armures": 4.0},
    "Military Outpost":    {"Fabrication d’armes et armures": 4.2, "Forge et métallurgie": 4.0, "Travail du cuir et tannerie": 3.5},

    # ==================== ZONES COMMERCIALES & SPÉCIALES ====================
    "Port City":           {"Navigation (terrestre et maritime)": 4.5, "Construction navale": 4.2, "Pêche": 3.8, "Comptabilité et gestion de biens": 3.5},
    "Trading Post":        {"Comptabilité et gestion de biens": 4.5, "Teinture et coloration": 3.5, "Joaillerie et orfèvrerie": 3.2},
    "Market Town":         {"Comptabilité et gestion de biens": 4.2, "Teinture et coloration": 3.8, "Cuisine raffinée": 3.0},

    # ==================== ZONES RELIGIEUSES & CULTURELLES ====================
    "Monastery":           {"Calligraphie et enluminure": 4.5, "Reliure de livres": 4.2, "Herboristerie et préparation de potions": 3.8, "Fabrication d’objets rituels": 4.0},
    "Temple Complex":      {"Calligraphie et enluminure": 4.2, "Fabrication d’objets rituels": 4.5, "Reliure de livres": 3.8},

    # ==================== ZONES SAUVAGES & FRONTIÈRES ====================
    "Wilderness":          {"Herboristerie et préparation de potions": 4.5, "Cueillette et survie en milieu sauvage": 4.2, "Chasse": 4.0, "Travail du cuir et tannerie": 3.5},
    "Frontier Outpost":    {"Chasse": 4.0, "Travail du cuir et tannerie": 3.8, "Fabrication d’armes et armures": 3.5, "Cueillette et survie en milieu sauvage": 3.5},
    "Nomad Camp":          {"Élevage et dressage": 4.2, "Travail du cuir et tannerie": 4.0, "Cueillette et survie en milieu sauvage": 3.8},

    # ==================== FALLBACK ====================
    "Default":             {}
}


# ====================== KNOWLEDGE WEIGHTS (poids de base - 45 connaissances) ======================
knowledge_weights: Dict[str, int] = {
    "Histoire des Royaumes Oubliés": 18,
    "Géographie de Faerûn": 20,
    "Connaissance des cités et régions majeures": 17,
    "Routes commerciales et voies marchandes": 15,
    "Lois et coutumes des nations": 14,
    "Noblesse et héraldique": 13,
    "Folklore et légendes locales": 12,
    "Fêtes, calendriers et traditions": 11,
    "Étiquette et protocole de cour": 10,
    "Connaissance des guildes et corporations": 12,
    "Culture elfique": 9,
    "Culture naine": 9,
    "Culture gnome": 7,
    "Culture halfeline": 7,
    "Culture orc et gobelinoïde": 6,
    "Genasi et peuples élémentaires": 5,
    "Races anciennes (Netheril, Imaskar...)": 8,
    "Interactions culturelles": 10,
    "Religions et divinités majeures": 16,
    "Mythes et légendes divines": 13,
    "Cultes et ordres religieux": 11,
    "Cosmologie (Weave, Shadow Weave)": 9,
    "Histoire de Netheril": 7,
    "Histoire d’Imaskar": 6,
    "Chute de Myth Drannor": 8,
    "Spellplague et ses conséquences": 8,
    "Royaumes et cités perdues": 7,
    "Ruines et sites archéologiques majeurs": 9,
    "Théorie de la Weave": 8,
    "Histoire de la magie": 10,
    "Écoles et traditions magiques": 9,
    "Artefacts et reliques légendaires": 7,
    "Connaissance des dragons": 8,
    "Connaissance des aberrations": 5,
    "Connaissance des fées et du Feywild": 6,
    "Connaissance des organisations secrètes": 7,
    "Courants politiques et rivalités": 12,
    "Astronomie et navigation stellaire": 8,
}

# ====================== MODIFICATEURS CONNAISSANCES PAR ETHNIE ======================
ethnicity_knowledge_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== HUMAINS ====================
    "Chondathan":      {
        "Routes commerciales et voies marchandes": 4.8, 
        "Connaissance des cités et régions majeures": 4.5, 
        "Courants politiques et rivalités": 4.2,
        "Comptabilité et gestion de biens": 4.0,
        "Lois et coutumes des nations": 3.5,
        "Connaissance des guildes et corporations": 3.8
    },
    "Tethyrian":       {
        "Histoire des Royaumes Oubliés": 4.2,
        "Géographie de Faerûn": 4.0,
        "Lois et coutumes des nations": 3.8,
        "Folklore et légendes locales": 3.5,
        "Noblesse et héraldique": 3.2
    },
    "Calishite":       {
        "Noblesse et héraldique": 4.8,
        "Étiquette et protocole de cour": 4.5,
        "Routes commerciales et voies marchandes": 4.2,
        "Connaissance des cités et régions majeures": 4.0,
        "Courants politiques et rivalités": 3.8
    },
    "Damaran":         {
        "Histoire des Royaumes Oubliés": 4.5,
        "Lois et coutumes des nations": 4.2,
        "Noblesse et héraldique": 3.8,
        "Folklore et légendes locales": 3.5
    },
    "Illuskan":        {
        "Géographie de Faerûn": 4.5,
        "Routes commerciales et voies marchandes": 4.0,
        "Folklore et légendes locales": 3.8,
        "Histoire des Royaumes Oubliés": 3.5
    },
    "Mulan":           {
        "Lois et coutumes des nations": 4.5,
        "Courants politiques et rivalités": 4.2,
        "Connaissance des cités et régions majeures": 4.0,
        "Étiquette et protocole de cour": 3.8,
        "Histoire de la magie": 3.5
    },
    "Rashemi":         {
        "Mythes et légendes divines": 4.5,
        "Folklore et légendes locales": 4.2,
        "Religions et divinités majeures": 4.0,
        "Cosmologie (Weave, Shadow Weave)": 3.8
    },
    "Turami":          {
        "Fêtes, calendriers et traditions": 4.2,
        "Folklore et légendes locales": 4.0,
        "Cuisine raffinée": 3.5,  # indirect via culture
        "Routes commerciales et voies marchandes": 3.2
    },
    "Uthgardt":        {
        "Folklore et légendes locales": 4.5,
        "Culture orc et gobelinoïde": 4.0,
        "Chasse": 3.8,  # même si supprimé, on peut garder pour cohérence
        "Cueillette et survie en milieu sauvage": 3.5
    },
    "Chultan":         {
        "Herboristerie et préparation de potions": 4.5,
        "Connaissance des cités et régions majeures": 3.8,
        "Ruines et sites archéologiques majeurs": 4.0,
        "Folklore et légendes locales": 3.5
    },
    "Shaaran":         {
        "Élevage et dressage": 4.2,
        "Folklore et légendes locales": 3.8,
        "Cueillette et survie en milieu sauvage": 4.0
    },
    "Ffolk":           {
        "Folklore et légendes locales": 4.2,
        "Fêtes, calendriers et traditions": 4.0,
        "Pêche": 3.5
    },
    "Sossrim":         {
        "Folklore et légendes locales": 4.0,
        "Chasse": 4.2,
        "Cueillette et survie en milieu sauvage": 3.8
    },
    "Vaasan":          {
        "Maçonnerie": 3.5,
        "Histoire des Royaumes Oubliés": 3.8,
        "Ruines et sites archéologiques majeurs": 3.5
    },
    "Bedine":          {
        "Cueillette et survie en milieu sauvage": 4.5,
        "Folklore et légendes locales": 4.0,
        "Routes commerciales et voies marchandes": 3.5
    },

    # ==================== DEMI-ELFES ====================
    "Half-Elf":        {
        "Interactions culturelles": 4.5,
        "Culture elfique": 4.0,
        "Histoire des Royaumes Oubliés": 3.8,
        "Connaissance des cités et régions majeures": 3.5
    },
    "Half-Elf Moon":   {"Culture elfique": 4.5, "Mythes et légendes divines": 4.0, "Connaissance des fées et du Feywild": 4.2},
    "Half-Elf Wood":   {"Culture elfique": 4.5, "Connaissance des fées et du Feywild": 4.8, "Herboristerie et préparation de potions": 3.8},
    "Half-Elf Sun":    {"Culture elfique": 4.2, "Étiquette et protocole de cour": 4.0, "Noblesse et héraldique": 3.8},

    # ==================== ELFES ====================
    "Elf Moon":        {"Culture elfique": 5.0, "Connaissance des fées et du Feywild": 4.8, "Mythes et légendes divines": 4.5, "Histoire de la magie": 4.0},
    "Elf Sun":         {"Culture elfique": 4.8, "Noblesse et héraldique": 4.5, "Étiquette et protocole de cour": 4.2, "Artefacts et reliques légendaires": 3.8},
    "Elf Wood":        {"Culture elfique": 5.0, "Connaissance des fées et du Feywild": 5.0, "Herboristerie et préparation de potions": 4.5},
    "Elf Wild":        {"Connaissance des fées et du Feywild": 5.0, "Cueillette et survie en milieu sauvage": 4.5, "Folklore et légendes locales": 4.2},
    "Elf Drow":        {"Connaissance des organisations secrètes": 4.8, "Cosmologie (Weave, Shadow Weave)": 4.5, "Artefacts et reliques légendaires": 4.0},
    "Elf Sea":         {"Routes commerciales et voies marchandes": 4.2, "Géographie de Faerûn": 4.0, "Navigation (terrestre et maritime)": 3.8},
    "Elf Star":        {"Astronomie et navigation stellaire": 4.8, "Cosmologie (Weave, Shadow Weave)": 4.5, "Théorie de la Weave": 4.2},
    "Elf Avariel":     {"Connaissance des fées et du Feywild": 4.5, "Astronomie et navigation stellaire": 4.0},
    "Elf Lythari":     {"Connaissance des fées et du Feywild": 5.0, "Herboristerie et préparation de potions": 4.5},

    # ==================== NAINS ====================
    "Nain":            {"Culture naine": 5.0, "Ruines et sites archéologiques majeurs": 4.5, "Histoire des Royaumes Oubliés": 4.0, "Artefacts et reliques légendaires": 3.8},
    "Shield Dwarf":    {"Culture naine": 5.0, "Histoire des Royaumes Oubliés": 4.2, "Ruines et sites archéologiques majeurs": 4.0},
    "Gold Dwarf":      {"Culture naine": 5.0, "Noblesse et héraldique": 4.2, "Artefacts et reliques légendaires": 4.0},
    "Gray Dwarf":      {"Connaissance des organisations secrètes": 4.5, "Ruines et sites archéologiques majeurs": 4.2},
    "Urdunnir":        {"Culture naine": 5.0, "Ruines et sites archéologiques majeurs": 4.8, "Travail de la pierre": 4.0},

    # ==================== HALFELINS & GNOMES ====================
    "Halfelin":        {"Folklore et légendes locales": 4.5, "Fêtes, calendriers et traditions": 4.2, "Connaissance des guildes et corporations": 3.5},
    "Lightfoot Halfling": {"Folklore et légendes locales": 4.5, "Interactions culturelles": 4.0},
    "Strongheart Halfling": {"Élevage et dressage": 4.0, "Folklore et légendes locales": 4.0},
    "Ghostwise Halfling": {"Connaissance des fées et du Feywild": 4.2, "Folklore et légendes locales": 4.5},

    "Gnome":           {"Connaissance des guildes et corporations": 4.0, "Histoire de la magie": 3.8, "Artefacts et reliques légendaires": 3.5},
    "Rock Gnome":      {"Histoire de la magie": 4.0, "Artefacts et reliques légendaires": 4.2},
    "Forest Gnome":    {"Connaissance des fées et du Feywild": 4.8, "Herboristerie et préparation de potions": 4.5},

    # ==================== AUTRES RACES ====================
    "Half-Orc":        {"Culture orc et gobelinoïde": 5.0, "Histoire des Royaumes Oubliés": 3.5},
    "Orc":             {"Culture orc et gobelinoïde": 5.0},
    "Gray Orc":        {"Culture orc et gobelinoïde": 4.8},

    "Aasimar":         {"Religions et divinités majeures": 4.8, "Mythes et légendes divines": 4.5, "Cosmologie (Weave, Shadow Weave)": 4.0},
    "Tiefling":        {"Connaissance des organisations secrètes": 4.5, "Cosmologie (Weave, Shadow Weave)": 4.2},
    "Dragonborn":      {"Connaissance des dragons": 5.0, "Histoire des Royaumes Oubliés": 3.8},
    "Firbolg":         {"Connaissance des fées et du Feywild": 4.5, "Herboristerie et préparation de potions": 4.2},
    "Kenku":           {"Folklore et légendes locales": 4.2, "Connaissance des organisations secrètes": 3.8},
    "Lizardfolk":      {"Cueillette et survie en milieu sauvage": 4.0, "Herboristerie et préparation de potions": 3.8},
    "Triton":          {"Géographie de Faerûn": 4.0, "Cosmologie (Weave, Shadow Weave)": 3.5},
    "Aarakocra":       {"Astronomie et navigation stellaire": 4.2, "Géographie de Faerûn": 4.0},
    "Goliath":         {"Ruines et sites archéologiques majeurs": 3.8},
    "Centaur":         {"Folklore et légendes locales": 4.0, "Herboristerie et préparation de potions": 3.8},

    # ==================== FALLBACK ====================
    "Default":         {}
}

# ====================== MODIFICATEURS CONNAISSANCES PAR RÉGION ======================
region_knowledge_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== NORTHWEST & SWORD COAST ====================
    "Sword Coast":          {"Routes commerciales et voies marchandes": 4.8, "Connaissance des cités et régions majeures": 4.5, "Géographie de Faerûn": 4.2, "Courants politiques et rivalités": 4.0},
    "Waterdeep":            {"Connaissance des cités et régions majeures": 5.0, "Courants politiques et rivalités": 4.8, "Étiquette et protocole de cour": 4.5, "Connaissance des guildes et corporations": 4.5, "Noblesse et héraldique": 4.0},
    "Neverwinter":          {"Architecture": 4.2, "Histoire des Royaumes Oubliés": 4.0, "Connaissance des cités et régions majeures": 3.8},
    "Luskan":               {"Routes commerciales et voies marchandes": 4.5, "Géographie de Faerûn": 4.0, "Connaissance des cités et régions majeures": 3.8},
    "Baldur's Gate":        {"Routes commerciales et voies marchandes": 4.5, "Connaissance des cités et régions majeures": 4.2, "Courants politiques et rivalités": 4.0},
    "Candlekeep":           {"Histoire de la magie": 5.0, "Artefacts et reliques légendaires": 4.8, "Théorie de la Weave": 4.5, "Histoire des Royaumes Oubliés": 4.2, "Reliure de livres": 4.0},

    # ==================== NORTH & SAVAGE FRONTIER ====================
    "Silver Marches":       {"Ruines et sites archéologiques majeurs": 4.2, "Histoire des Royaumes Oubliés": 4.0, "Culture naine": 3.8},
    "Icewind Dale":         {"Folklore et légendes locales": 4.5, "Chasse": 4.0, "Cueillette et survie en milieu sauvage": 4.0, "Géographie de Faerûn": 3.8},
    "High Forest":          {"Connaissance des fées et du Feywild": 5.0, "Herboristerie et préparation de potions": 4.5, "Folklore et légendes locales": 4.2},
    "Savage Frontier":      {"Cueillette et survie en milieu sauvage": 4.5, "Folklore et légendes locales": 4.2, "Géographie de Faerûn": 4.0},
    "Uthgardt Lands":       {"Folklore et légendes locales": 4.8, "Culture orc et gobelinoïde": 4.5, "Chasse": 4.0},
    "Spine of the World":   {"Ruines et sites archéologiques majeurs": 4.5, "Géographie de Faerûn": 4.2, "Cueillette et survie en milieu sauvage": 4.0},

    # ==================== HEARTLANDS & DALELANDS ====================
    "Dalelands":            {"Folklore et légendes locales": 4.8, "Fêtes, calendriers et traditions": 4.5, "Histoire des Royaumes Oubliés": 4.2, "Herboristerie et préparation de potions": 3.8},
    "Cormyr":               {"Noblesse et héraldique": 4.8, "Étiquette et protocole de cour": 4.5, "Lois et coutumes des nations": 4.2, "Histoire des Royaumes Oubliés": 4.0},
    "Sembia":               {"Routes commerciales et voies marchandes": 5.0, "Comptabilité et gestion de biens": 4.5, "Connaissance des guildes et corporations": 4.2},
    "Thesk":                {"Routes commerciales et voies marchandes": 4.5, "Connaissance des guildes et corporations": 4.0},
    "Impiltur":             {"Histoire des Royaumes Oubliés": 4.0, "Noblesse et héraldique": 3.8},
    "Western Heartlands":   {"Élevage et dressage": 4.0, "Folklore et légendes locales": 3.8, "Routes commerciales et voies marchandes": 3.5},

    # ==================== SOUTH & SHINING SOUTH ====================
    "Calimshan":            {"Routes commerciales et voies marchandes": 5.0, "Noblesse et héraldique": 4.5, "Étiquette et protocole de cour": 4.2, "Connaissance des cités et régions majeures": 4.0},
    "Tethyr":               {"Fêtes, calendriers et traditions": 4.5, "Folklore et légendes locales": 4.2, "Viticulture et vinification": 4.0},
    "Amn":                  {"Routes commerciales et voies marchandes": 5.0, "Comptabilité et gestion de biens": 4.8, "Connaissance des guildes et corporations": 4.5},
    "Chult":                {"Ruines et sites archéologiques majeurs": 4.8, "Herboristerie exotique": 4.5, "Connaissance des cités et régions majeures": 4.0},
    "Shaar":                {"Élevage et dressage": 4.5, "Folklore et légendes locales": 4.0, "Cueillette et survie en milieu sauvage": 4.0},
    "Halruaa":              {"Histoire de la magie": 5.0, "Théorie de la Weave": 4.8, "Artefacts et reliques légendaires": 4.5, "Cosmologie (Weave, Shadow Weave)": 4.2},
    "Vilhon Reach":         {"Routes commerciales et voies marchandes": 4.2, "Connaissance des cités et régions majeures": 4.0},
    "Dragon Coast":         {"Routes commerciales et voies marchandes": 4.5, "Connaissance des cités et régions majeures": 4.0, "Géographie de Faerûn": 3.8},

    # ==================== EAST & UNAPPROACHABLE EAST ====================
    "Moonsea":              {"Courants politiques et rivalités": 4.8, "Histoire des Royaumes Oubliés": 4.5, "Connaissance des cités et régions majeures": 4.2},
    "Rashemen":             {"Mythes et légendes divines": 5.0, "Folklore et légendes locales": 4.8, "Religions et divinités majeures": 4.5, "Cosmologie (Weave, Shadow Weave)": 4.0},
    "Thay":                 {"Histoire de la magie": 5.0, "Théorie de la Weave": 4.8, "Artefacts et reliques légendaires": 4.5, "Connaissance des organisations secrètes": 4.2},
    "Aglarond":             {"Herboristerie et préparation de potions": 4.5, "Connaissance des fées et du Feywild": 4.2, "Folklore et légendes locales": 4.0},
    "The Vast":             {"Histoire des Royaumes Oubliés": 4.0, "Connaissance des cités et régions majeures": 3.8},
    "Mulhorand":            {"Histoire des Royaumes Oubliés": 4.5, "Noblesse et héraldique": 4.2, "Religions et divinités majeures": 4.0},
    "Unther":               {"Histoire des Royaumes Oubliés": 4.2, "Ruines et sites archéologiques majeurs": 4.0},
    "Chessenta":            {"Histoire des Royaumes Oubliés": 4.0, "Noblesse et héraldique": 3.8},

    # ==================== INTERIOR & COLD LANDS ====================
    "Anauroch":             {"Cueillette et survie en milieu sauvage": 4.5, "Ruines et sites archéologiques majeurs": 4.2, "Géographie de Faerûn": 4.0},
    "Damara":               {"Histoire des Royaumes Oubliés": 4.2, "Noblesse et héraldique": 3.8},
    "Vaasa":                {"Ruines et sites archéologiques majeurs": 4.0, "Histoire des Royaumes Oubliés": 3.8},
    "Narfell":              {"Élevage et dressage": 4.2, "Folklore et légendes locales": 4.0},
    "Great Dale":           {"Herboristerie et préparation de potions": 4.5, "Folklore et légendes locales": 4.2},

    # ==================== FORESTS, MOORS & WILD AREAS ====================
    "Cormanthor":           {"Connaissance des fées et du Feywild": 5.0, "Culture elfique": 4.8, "Herboristerie et préparation de potions": 4.5},
    "Misty Forest":         {"Connaissance des fées et du Feywild": 4.8, "Herboristerie et préparation de potions": 4.5},
    "Ardeep Forest":        {"Connaissance des fées et du Feywild": 4.5, "Folklore et légendes locales": 4.0},
    "Luirwood":             {"Herboristerie et préparation de potions": 4.5, "Mythes et légendes divines": 4.0},
    "High Moor":            {"Cueillette et survie en milieu sauvage": 4.5, "Ruines et sites archéologiques majeurs": 4.2},
    "Trollclaws":           {"Cueillette et survie en milieu sauvage": 4.2, "Chasse": 4.0},
    "Evermoors":            {"Élevage et dressage": 4.0, "Folklore et légendes locales": 3.8},

    # ==================== CITIES & SPECIAL ZONES ====================
    "Silverymoon":          {"Histoire de la magie": 4.2, "Connaissance des cités et régions majeures": 4.0, "Étiquette et protocole de cour": 3.8},
    "Zhentil Keep":         {"Courants politiques et rivalités": 4.8, "Connaissance des organisations secrètes": 4.5},
    "Elturel":              {"Lois et coutumes des nations": 4.0, "Religions et divinités majeures": 3.8},
    "Turmish":              {"Routes commerciales et voies marchandes": 4.0, "Connaissance des cités et régions majeures": 3.8},
    "Lake of Steam":        {"Routes commerciales et voies marchandes": 4.2, "Géographie de Faerûn": 4.0},

    # ==================== ISLANDS & REMOTE AREAS ====================
    "Moonshae Isles":       {"Folklore et légendes locales": 4.5, "Fêtes, calendriers et traditions": 4.2, "Pêche": 4.0},
    "Nelanther Isles":      {"Routes commerciales et voies marchandes": 4.5, "Géographie de Faerûn": 4.2},
    "Evermeet":             {"Culture elfique": 5.0, "Connaissance des fées et du Feywild": 5.0, "Histoire des Royaumes Oubliés": 4.2},
    "Lantan":               {"Histoire de la magie": 4.5, "Artefacts et reliques légendaires": 4.2, "Théorie de la Weave": 4.0},

    # ==================== FALLBACK ====================
    "Default":              {}
}

# ====================== MODIFICATEURS CONNAISSANCES PAR SETTLEMENT ======================
settlement_knowledge_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== GRANDES VILLES & MÉTROPOLES ====================
    "Metropolis":          {"Connaissance des cités et régions majeures": 5.0, "Courants politiques et rivalités": 4.8, "Connaissance des guildes et corporations": 4.5, "Étiquette et protocole de cour": 4.5, "Noblesse et héraldique": 4.2, "Routes commerciales et voies marchandes": 4.0},
    "Large City":          {"Connaissance des cités et régions majeures": 4.8, "Courants politiques et rivalités": 4.5, "Connaissance des guildes et corporations": 4.2, "Étiquette et protocole de cour": 4.0, "Noblesse et héraldique": 3.8},
    "Small City":          {"Connaissance des cités et régions majeures": 4.5, "Lois et coutumes des nations": 4.0, "Connaissance des guildes et corporations": 3.8, "Courants politiques et rivalités": 3.5},

    # ==================== VILLES MOYENNES & BOURGS ====================
    "Large Town":          {"Connaissance des cités et régions majeures": 4.0, "Folklore et légendes locales": 3.8, "Fêtes, calendriers et traditions": 3.5, "Lois et coutumes des nations": 3.2},
    "Small Town":          {"Folklore et légendes locales": 4.2, "Fêtes, calendriers et traditions": 4.0, "Connaissance des guildes et corporations": 3.5},
    "Town":                {"Folklore et légendes locales": 4.0, "Fêtes, calendriers et traditions": 3.8, "Lois et coutumes des nations": 3.5},

    # ==================== PETITS VILLAGES & CAMPAGNE ====================
    "Village":             {"Folklore et légendes locales": 4.5, "Fêtes, calendriers et traditions": 4.2, "Herboristerie et préparation de potions": 3.5},
    "Hamlet":              {"Folklore et légendes locales": 4.8, "Fêtes, calendriers et traditions": 4.5, "Herboristerie et préparation de potions": 3.8},
    "Thorp":               {"Folklore et légendes locales": 4.5, "Fêtes, calendriers et traditions": 4.0},

    # ==================== ZONES RURALES & SPÉCIALISÉES ====================
    "Rural":               {"Folklore et légendes locales": 4.2, "Fêtes, calendriers et traditions": 4.0, "Élevage et dressage": 3.5},
    "Farming Village":     {"Folklore et légendes locales": 4.0, "Fêtes, calendriers et traditions": 3.8, "Herboristerie et préparation de potions": 3.5},
    "Fishing Village":     {"Folklore et légendes locales": 4.0, "Géographie de Faerûn": 3.8, "Routes commerciales et voies marchandes": 3.5},
    "Mining Town":         {"Ruines et sites archéologiques majeurs": 4.5, "Histoire des Royaumes Oubliés": 4.0, "Travail de la pierre": 3.5},

    # ==================== ZONES MILITAIRES & FORTIFIÉES ====================
    "Fortress":            {"Lois et coutumes des nations": 4.2, "Courants politiques et rivalités": 4.0, "Histoire des Royaumes Oubliés": 3.8, "Noblesse et héraldique": 3.5},
    "Citadel":             {"Noblesse et héraldique": 4.5, "Histoire des Royaumes Oubliés": 4.2, "Lois et coutumes des nations": 4.0},
    "Military Outpost":    {"Lois et coutumes des nations": 4.0, "Courants politiques et rivalités": 3.8, "Histoire des Royaumes Oubliés": 3.5},

    # ==================== ZONES COMMERCIALES & SPÉCIALES ====================
    "Port City":           {"Routes commerciales et voies marchandes": 4.8, "Connaissance des cités et régions majeures": 4.5, "Géographie de Faerûn": 4.2},
    "Trading Post":        {"Routes commerciales et voies marchandes": 5.0, "Connaissance des guildes et corporations": 4.5, "Connaissance des cités et régions majeures": 4.0},
    "Market Town":         {"Routes commerciales et voies marchandes": 4.5, "Connaissance des guildes et corporations": 4.2, "Connaissance des cités et régions majeures": 4.0},

    # ==================== ZONES RELIGIEUSES & CULTURELLES ====================
    "Monastery":           {"Religions et divinités majeures": 5.0, "Mythes et légendes divines": 4.8, "Cosmologie (Weave, Shadow Weave)": 4.5, "Histoire de la magie": 4.0, "Reliure de livres": 3.8},
    "Temple Complex":      {"Religions et divinités majeures": 5.0, "Mythes et légendes divines": 4.8, "Cultes et ordres religieux": 4.5, "Cosmologie (Weave, Shadow Weave)": 4.2},

    # ==================== ZONES SAUVAGES & FRONTIÈRES ====================
    "Wilderness":          {"Ruines et sites archéologiques majeurs": 4.8, "Connaissance des fées et du Feywild": 4.5, "Cueillette et survie en milieu sauvage": 4.2, "Folklore et légendes locales": 4.0},
    "Frontier Outpost":    {"Ruines et sites archéologiques majeurs": 4.5, "Folklore et légendes locales": 4.0, "Courants politiques et rivalités": 3.8},
    "Nomad Camp":          {"Folklore et légendes locales": 4.5, "Élevage et dressage": 4.0, "Cueillette et survie en milieu sauvage": 3.8},

    # ==================== FALLBACK ====================
    "Default":             {}
}

ethnicity_literacy_modifiers: Dict[str, Dict[str, float]] = {
    # ==================== HUMAINS ====================
    "Chondathan":      {"Thorass": 18.0, "Chondathan": 32.0, "Cormyrian": 8.0, "Sembian": 7.0},
    "Tethyrian":       {"Thorass": 28.0, "Chondathan": 15.0, "Illuskan": 10.0, "Druidic": 6.0},
    "Damaran":         {"Thorass": 30.0, "Chondathan": 10.0, "Draconique": 7.0},
    "Calishite":       {"Mulhorandi": 28.0, "Thorass": 16.0, "Maztican": 7.0, "Chultan": 5.0},
    "Illuskan":        {"Thorass": 22.0, "Illuskan": 14.0, "Maztican": 6.0, "Céleste": 5.0},
    "Mulan":           {"Mulhorandi": 30.0, "Thorass": 14.0, "Céleste": 6.0, "Shou": 5.0},

    # ==================== ELFES & DEMI-ELFES ====================
    "Elf Moon":        {"Espruar": 42.0, "Elven High Speech": 18.0, "Thorass": 8.0, "Céleste": 6.0},
    "Elf Sun":         {"Espruar": 35.0, "Elven High Speech": 32.0, "Céleste": 8.0, "Thorass": 6.0},
    "Elf Wood":        {"Espruar": 45.0, "Sylvestre": 12.0, "Elven High Speech": 10.0, "Thorass": 6.0},
    "Elf Drow":        {"Glifo (Drow)": 40.0, "Undercommon": 10.0, "Sylvestre": 7.0, "Abyssal": 6.0},
    "Half-Elf":        {"Espruar": 28.0, "Thorass": 22.0, "Elven High Speech": 12.0, "Chondathan": 7.0},

    # ==================== NAINS ====================
    "Nain":            {"Nain": 38.0, "Thorass": 10.0, "Draconique": 7.0, "Géant": 6.0},
    "Shield Dwarf":    {"Nain": 40.0, "Thorass": 12.0, "Abyssal": 6.0},
    "Gold Dwarf":      {"Nain": 42.0, "Thorass": 8.0, "Glifo (Drow)": 5.0},

    # ==================== AUTRES RACES ====================
    "Halfelin":        {"Thorass": 30.0, "Tuigan": 8.0, "Chondathan": 7.0, "Illuskan": 6.0},
    "Gnome":           {"Thorass": 24.0, "Nain": 18.0, "Gnomish": 12.0, "Aquan": 6.0},
    "Half-Orc":        {"Orc": 32.0, "Thorass": 18.0, "Goblin": 7.0},
    "Orc":             {"Orc": 38.0, "Goblin": 10.0, "Thorass": 8.0},
    "Tiefling":        {"Infernal": 36.0, "Thorass": 12.0, "Abyssal": 10.0, "Chondathan": 6.0},
    "Dragonborn":      {"Draconique": 40.0, "Thorass": 10.0, "Druidic": 6.0, "Géant": 5.0},

    # ==================== DEFAULT ====================
    "Default":         {"Thorass": 25.0, "Chondathan": 8.0, "Espruar": 6.0, "Nain": 5.0}
}

# ====================== LANGUES ÉCRITES (version minimaliste) ======================
literacy_scripts = {
    "Thorass": "Alphabet Thorass",
    "Chondathan": "Alphabet Thorass",
    "Illuskan": "Alphabet Thorass",
    "Cormyrian": "Alphabet Thorass",
    "Sembian": "Alphabet Thorass",

    "Espruar": "Alphabet Espruar",
    "Elven High Speech": "Alphabet Espruar",
    "Sylvestre": "Alphabet Espruar",
    "Elfique": "Alphabet Espruar",

    "Nain": "Runes Dethek",
    "Draconique": "Alphabet Iokharic",
    "Glifo (Drow)": "Alphabet Glifo",
    "Undercommon": "Alphabet Undercommon",
    "Infernal": "Alphabet Infernal",
    "Céleste": "Alphabet Céleste",
    "Abyssal": "Alphabet Abyssal",
    "Mulhorandi": "Alphabet Mulhorandi",
    "Shou": "Idéogrammes Shou",
    "Tuigan": "Alphabet Tuigan",
    "Chultan": "Pictogrammes Chultans",
    "Maztican": "Pictogrammes Mazticans",
    "Netherese": "Alphabet Netherese",
    "Auran": "Alphabet Auran",
    "Aquan": "Alphabet Aquan",
    "Géant": "Runes Géantes",
    "Orc": "Alphabet Orc",
    "Goblin": "Alphabet Goblin",
    "Yuan-ti": "Glyphes Yuan-ti",
    "Thieves' Cant": "Symboles des Voleurs",
    "Druidic": "Runes Druidiques",
    "Gnomish": "Alphabet Gnomique",
}

# ====================== HELPERS ======================
def _calculate_craft_count(active_count: int) -> int:
    if active_count >= 7: return random.randint(0, 2)
    elif active_count == 6: return random.randint(1, 3)
    elif active_count == 5: return random.randint(1, 4)
    elif active_count == 4: return random.randint(2, 5)
    else: return random.randint(3, 6)

def _calculate_know_count(craft_count: int) -> int:
    """Version réduite : moins de connaissances par personnage"""
    if craft_count >= 6:
        return random.randint(3, 6)      # très spécialisé
    elif craft_count >= 5:
        return random.randint(4, 7)
    elif craft_count >= 4:
        return random.randint(5, 9)
    elif craft_count >= 3:
        return random.randint(6, 10)
    else:  # 0 à 2 crafts → plus érudit
        return random.randint(8, 12)



def _calculate_literacy_count(
    know_count: int, 
    settlement_type: str, 
    ethnicity: str
) -> int:
    """Version drastiquement réduite : beaucoup de personnages ne savent pas lire/écrire"""
    
    # Base très basse
    if know_count >= 11:
        base = random.randint(1, 3)
    elif know_count >= 8:
        base = random.randint(0, 2)
    elif know_count >= 5:
        base = random.randint(0, 1)
    else:
        base = random.randint(0, 1)   # très souvent 0

    # Bonus selon le type de settlement
    if settlement_type in ["Metropolis", "Large City"]:
        base += random.randint(0, 2)
    elif settlement_type in ["Small City", "Large Town"]:
        base += random.randint(0, 1)
    elif settlement_type in ["Town"]:
        base += random.randint(0, 1) if random.random() < 0.4 else 0
    else:  # Village, Rural, Wilderness, etc.
        base += random.randint(0, 1) if random.random() < 0.25 else 0

    # Bonus selon l'ethnie (races naturellement plus lettrées)
    if ethnicity in ["Elf Moon", "Elf Sun", "Elf Star", "Gnome", "Rock Gnome", "Half-Elf", "Aasimar"]:
        base += random.randint(0, 1)

    # On ne dépasse jamais 4 langues (très rare)
    return max(0, min(4, base))

def _get_region_name(region_id: int) -> str:
    region_map = {1: "Sword Coast", 2: "Waterdeep", 3: "Calimshan", 4: "Dalelands", 5: "Moonsea"}
    return region_map.get(region_id, "Default")

# ====================== GÉNÉRATION SECONDAIRE ======================
def generate_secondary_skills(
    ethnicity: str,
    region_id: int,
    settlement_type: str,
    active_count: int = None   # ← Ajout important
) -> Dict:
    """Génère les compétences secondaires (Knowledge, Craft, Literacy)"""
    
    # Si active_count n'est pas fourni, on le calcule
    if active_count is None:
        active_count = get_num_active_skills(settlement_type)
    
    craft_count = _calculate_craft_count(active_count)
    know_count = _calculate_know_count(craft_count)
    literacy_count = _calculate_literacy_count(know_count, settlement_type, ethnicity)

    # ... (le reste de la fonction reste identique)

    region_name = _get_region_name(region_id)

    # ====================== 1. CRAFTS ======================
    eth_mod = ethnicity_craft_modifiers.get(ethnicity, {})
    reg_mod = region_craft_modifiers.get(region_name, {})
    sett_mod = settlement_craft_modifiers.get(settlement_type, {})

    craft_names = list(craft_weights.keys())
    final_craft_weights = []
    
    for craft in craft_names:
        base = craft_weights[craft]
        bias = (eth_mod.get(craft, 0) + reg_mod.get(craft, 0) + sett_mod.get(craft, 0))
        final_weight = max(base + bias * 1.65, 0.5)
        final_craft_weights.append(final_weight)
    
    craft = random.choices(craft_names, weights=final_craft_weights, k=craft_count)

    # ====================== 2. CONNAISSANCES ======================
    eth_know_mod = ethnicity_knowledge_modifiers.get(ethnicity, {})
    reg_know_mod = region_knowledge_modifiers.get(region_name, {})
    sett_know_mod = settlement_knowledge_modifiers.get(settlement_type, {})

    know_names = list(knowledge_weights.keys())
    final_know_weights = []
    
    for know in know_names:
        base = knowledge_weights[know]
        bias = (eth_know_mod.get(know, 0) + reg_know_mod.get(know, 0) + sett_know_mod.get(know, 0))
        final_weight = max(base + bias * 2.4, 0.8)
        final_know_weights.append(final_weight)
    
    knowledge = random.choices(know_names, weights=final_know_weights, k=know_count)

    # ====================== 3. LANGUES ÉCRITES ======================
    eth_lit_mod = ethnicity_literacy_modifiers.get(ethnicity, ethnicity_literacy_modifiers["Default"])
    lang_names = list(literacy_scripts.keys())
    literacy = {}

    if literacy_count > 0:
        # Première langue écrite = première langue parlée (80% de chance)
        spoken_languages = generate_languages(ethnicity, region_id, active_count * 2)
        first_spoken = spoken_languages[0] if spoken_languages else None

        if first_spoken and random.random() < 0.80 and first_spoken in literacy_scripts:
            first_lang = first_spoken
        else:
            favored = list(eth_lit_mod.keys())
            if not favored:
                favored = ["Thorass"]
            native_weights = [eth_lit_mod.get(lang, 5.0) * 3.8 for lang in favored]
            first_lang = random.choices(favored, weights=native_weights, k=1)[0]

        literacy[first_lang] = literacy_scripts.get(first_lang, literacy_scripts["Thorass"])

        # Langues écrites supplémentaires
        remaining = literacy_count - 1
        if remaining > 0:
            final_weights = []
            for lang in lang_names:
                if lang == first_lang:
                    final_weights.append(0.3)
                else:
                    w = eth_lit_mod.get(lang, 1.0) * 4.0
                    final_weights.append(max(w, 0.5))
            
            additional = random.choices(lang_names, weights=final_weights, k=remaining)
            for lang in additional:
                if lang not in literacy:
                    literacy[lang] = literacy_scripts.get(lang, literacy_scripts["Thorass"])

    # ====================== 4. LANGUES PARLÉES ======================
    spoken_languages = generate_languages(
        ethnicity=ethnicity,
        region_id=region_id,
        skill_modifier=active_count * 2
    )

    # ====================== RETURN ======================
    return {
        "active_count": active_count,
        "knowledge": knowledge,
        "craft": craft,
        "literacy": literacy,
        "spoken_languages": spoken_languages,
        "total_knowledge": len(knowledge),
        "total_craft": len(craft),
        "total_literacy": len(literacy),
        "total_spoken": len(spoken_languages)
    }