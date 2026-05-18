# ethnicity_weights.py - Pondération détaillée par ethnie

ethnicity_weights = {
     # ==================== HUMAINS ====================
    "Chondathans":     27,   # Le plus répandu
    "Tethyrians":      23,   # Très nombreux sur la Sword Coast
    "Calishites":      14,   # Ajusté (était trop haut)
    "Damarans":        9,
    "Illuskans":       8,    # Inclut Northlanders
    "Mulan":           8,
    "Rashemi":         5,
    "Turami":          3,
    
    # Ethnies du Nord et îles
    "Ffolk":           2,
    "Sossrim":         1.2,
    "Uthgardt":        0.1,  # Très petit groupe
    
    # Ethnies régionales / spéciales
    "Chultan":         2.5,
    "Shaaryens":       1.0,
    "Nar":             0.6,
    "Gûr":             0.5,
    "Halruéens":       0.5,
    "Arkaiuns":        0.4,
    "Durpari":         0.4,
    "Imaskari":        0.35,
    "Lantannas":       0.35,
    "Raumviriens":     0.3,
    "Tashaliens":      0.35,
    "Lapalis":         0.25,
    "Nubari":          0.25,
    "Talfir":          0.25,

    # ==================== HALFLINGS ====================
    "Strongheart":     45,
    "Lightfoot":       45,
    "Ghostwalk":       10,
    "Tallfellow":      5,

    # ==================== NAINS ====================
    "Nain d'écu":      60,
    "Nain d'or":       30,
    "Nain gris":       4,
    "Nain arctique":   3,
    "Nain sauvages":   2,
    "Urdunnir":        1,

    # ==================== GNOMES ====================
    "Gnome des roches":     80,
    "Gnome des forêts":     15,
    "Gnome des profondeurs": 5,

    # ==================== DEMI-ELFES ====================
    "Demi-elfe des bois":    35,
    "Demi-elfe de la lune":  32,
    "Demi-elfe du soleil":   12,
    "Demi-elfe sauvage":     8,
    "Demi-elfe noir":        6,
    "Demi-elfe de la mer":   4,
    "Demi-elfe des étoiles": 2,
    "Demi-avariel":          0.5,
    "Demi-lythari":          0.5,

    # ==================== ELFES ====================
    "Elfe des bois":     35,
    "Elfe de la lune":   30,
    "Elfe du soleil":    12,
    "Elfe sauvage":      8,
    "Elfe noir":         6,
    "Elfe de la mer":    4,
    "Elfe des étoiles":  2,
    "Avariel":           1,
    "Lythari":           0.5,

    # ==================== DEMI-ORCS ====================
    "Mountain Orc": 70,
    "Gray Orc":     25,
    "Orogs":        5,

    # ==================== AUTRES ====================
    "Orc":               20,
    "Tiefling":          20,
    "Goblin":            10,
    "Hobgoblin":         10,
    "Protector Aasimar": 4,
    "Scourge Aasimar":   4,
    "Fallen Aasimar":    3,
    "Goliath":           1,
    "Centaur":           1,
    "Minotaur":          1,
}

# ====================== PONDERATION DES GRANDES CATÉGORIES ======================
category_weights = {
    "Humain":     82,
    "Nain":       7.5,
    "Elfe":       3.0,
    "Demi-elfe":  2.0,
    "Halfelin":   2.0,
    "Gnome":      1.2,
    "Demi-orc":   1.3,
    "Autre":      1.0
}