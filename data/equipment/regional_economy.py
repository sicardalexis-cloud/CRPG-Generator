"""
data/equipment/regional_economy.py

Système économique régional pour le calcul des salaires médians et du capital de départ.

RÈGLES (cohérentes avec les fichiers DAILY WAGES & WORTH CHART + listes d'équipement) :
- Salaire médian défini manuellement par région (pas de "niveaux techno" purs, Faerûn est hybride).
- Capital de départ = **5 ans de salaire médian local × niveau du personnage** (doublé par rapport à la version précédente).
- Le kit de base régional (équipement porté + 14 jours de rations) est **fourni gratuitement** à la création.
- TOUT est calculé en bronze pieces (bp) Rolemaster pour les kits, mais le capital final est exprimé en **pièces d'argent (sp)**.
- Équivalent d'une règle « X pièces d'argent par niveau » (base ~250 sp pour un perso moyen de niveau 1 avec 5 ans).

Le capital représente l'argent liquide + la capacité à faire des achats supplémentaires
(montures, charettes, armure supérieure, etc.) avant de quitter son lieu d'origine.
"""

import random
from typing import Dict

# =============================================================================
# MULTIPLICATEURS SELON LE TYPE DE SETTLEMENT
# =============================================================================
# Les gros centres urbains paient mieux.

SETTLEMENT_WAGE_MULTIPLIER: Dict[str, float] = {
    "Metropolis":           1.55,
    "Major Port City":      1.40,
    "Major Trade City":     1.45,
    "Fortified City":       1.20,
    "Large Town":           1.05,
    "Small Town":           0.92,
    "Rural Village":        0.78,
    "Fishing Village":      0.75,
    "Forest Village":       0.72,
    "Mountain Village":     0.80,
    "Farming Hamlet":       0.68,
    "Isolated Hamlet":      0.62,
    "Caravan Oasis":        0.82,
    "Military Outpost":     0.85,
    "Mining Camp":          0.90,
    "Logging Camp":         0.76,
    "Remote Trading Post":  0.88,
    "Frontier Colony":      0.80,
    "Smuggler's Port":      1.00,
    "Inhabited Ruins":      0.70,
    "Permanent Encampment": 0.65,
    "Isolated Tower":       0.80,
    "Lake Village":         0.74,
    "Remote Monastery":     0.75,
    "Dwarven Fortress":     1.05,
    "Elven Enclave":        0.90,
    "Underdark City":       0.95,
    "Default":              0.80,
}

# =============================================================================
# SALAIRE MÉDIAN JOURNALIER PAR RÉGION (en pièces d'or)
# =============================================================================
# Valeurs jugées appropriées selon le lore des Royaumes Oubliés + le tableau
# "DAILY WAGES & WORTH CHART" que tu as fourni.

REGION_MEDIAN_DAILY_WAGE_GP: Dict[str, float] = {
    # === Centres économiques majeurs (très riches) ===
    "Waterdeep": 0.56,
    "Baldur's Gate": 0.48,
    "Sembia": 0.52,
    "Calimshan": 0.44,
    "Lantan": 0.64,           # Plus avancé technologiquement
    "Halruaa": 0.50,

    # === Régions riches / fortement commerçantes ===
    "Amn": 0.36,
    "Cormyr": 0.34,
    "Tethyr": 0.32,
    "Impiltur": 0.30,
    "Turmish": 0.30,
    "Vilhon Reach": 0.32,
    "Chondath": 0.28,
    "Chessenta": 0.30,

    # === Régions moyennes / civilisées classiques ===
    "The Dalelands": 0.22,
    "Moonsea": 0.24,
    "Aglarond": 0.20,
    "Damara": 0.18,
    "The Shaar": 0.18,
    "Lake of Steam": 0.22,
    "Border Kingdoms": 0.20,
    "Luiren": 0.22,
    "Mulhorand": 0.24,
    "Unther": 0.20,
    "Rashemen": 0.18,
    "Thesk": 0.24,

    # === Régions plus pauvres ou frontalières ===
    "Vaasa": 0.12,
    "Icewind Dale": 0.10,
    "Le Nord (The North)": 0.14,
    "Spine of the World": 0.10,
    "Anauroch": 0.12,
    "Chult": 0.14,
    "Jungle de Mhair": 0.12,
    "Hordelands (The Endless Wastes)": 0.10,
    "Great Glacier": 0.06,
    "Sossal": 0.08,

    # === Régions spéciales / instables ===
    "Thay": 0.26,             # Riche mais très inégalitaire
    "Evermeet": 0.36,         # Riche mais isolée
    "Underdark": 0.18,        # Très variable selon la cité
    "Kara-Tur": 0.28,

    # === Régions 51+ (souvent plus spécifiques ou sauvages) ===
    "Old Empires": 0.20,
    "Unapproachable East": 0.18,
    "Western Heartlands": 0.22,
    "Sword Coast": 0.26,
    "Sword Coast North": 0.16,
    "Dragon Coast": 0.24,
    "Great Glacier": 0.06,
    "Inner Sea (Sea of Fallen Stars)": 0.24,
    "Dambrath": 0.16,
    "Estagund": 0.18,
    "Var the Golden": 0.20,
    "Shaarmid": 0.18,
    "Thindol": 0.14,
    "Samarach": 0.14,
    "Tashalar": 0.20,
    "The Shining South": 0.18,
    "Ymber": 0.12,
    "Nelanther Isles": 0.16,
    "The Whalebones": 0.10,
    "The Trackless Sea": 0.12,
    "The Cold Lands": 0.10,
    "The Endless Wastes": 0.10,
    "The Great Dale": 0.16,
    "The Plateau of Thay": 0.22,
    "The Easting Reach": 0.20,
    "The Forgotten Forest": 0.14,
    "The Lone Rock": 0.12,
    "The Reaching Woods": 0.16,
    "The Thunder Peaks": 0.18,
    "The Ride": 0.14,
    "Aglarondine": 0.18,
    "Bedine": 0.10,
    "Barakuir": 0.14,
    "Chondalwood": 0.12,
    "Citadelles du Nord": 0.16,
    "Cité Drow": 0.20,
    "Cité Souterraine Mixte": 0.16,
    "Eauprofonde": 0.18,
    "Épine dorsale (Nains arctiques)": 0.12,
    "Forêt d’Amtar / Methwood": 0.14,
    "Forteresses isolées": 0.14,
    "Gracklstugh": 0.18,
    "Grande Faille": 0.16,
    "Grand Glacier": 0.06,
    "Glacière éternelle": 0.06,
    "Ruathym": 0.14,
    "Luirwood": 0.12,
    "Myth Drannor": 0.16,
    "Evereska": 0.24,
    "Valbise": 0.14,
    "Vallée de la Flamme": 0.12,
    "Les Vaux": 0.16,
    "Vast": 0.18,
    "Zakharans": 0.20,
    "Pics Gris": 0.10,
    "Outreterre tropicale": 0.12,
    "Forêts du Nord (Gnomes)": 0.14,
    "Éternelle-Rencontre": 0.18,
    "Lunargent": 0.20,
    "Bois de Yuir": 0.16,
    "Montagnes du Shaar": 0.14,
    "Vil Adanrath": 0.10,
    "Tymanther": 0.18,
    "Icerim Mountains": 0.08,
    "Montagnes Theskiennes": 0.14,
    "Montagnes de Cuivre": 0.16,
    "Kara-Tur": 0.28,
    "Pics de Mir": 0.12,
    "Bois de Shaar": 0.12,
    "Outreterre profonde": 0.14,
    "Lycanthropes": 0.10,
    "Wemics": 0.08,
    "Yuan-ti": 0.12,
    "Centaure": 0.10,
    "Homme-lézard": 0.08,
    "Tanarukks": 0.10,
    "Fey’ri": 0.14,
    "Sagespectres": 0.12,
    "Vaillants": 0.16,
    "Kir-lanan": 0.10,
    "Reflets (Shades)": 0.14,

    # Fallback
    "Default": 0.16,
}

# =============================================================================
# 3. NIVEAU TECHNOLOGIQUE PAR RÉGION (ou groupes de régions)
# =============================================================================
# On assigne un niveau technologique à chaque région.
# La plupart de Faerûn est "Middle Ages" ou "Renaissance".
# Certaines zones sont plus primitives, d'autres plus avancées.

REGION_TECH_LEVEL: Dict[str, int] = {
    # === Niveaux technologiques (0 à 8) ===
    # 0 = Stone Age
    # 1 = Copper Age
    # 2 = Bronze Age
    # 3 = Iron Age
    # 4 = Middle Ages
    # 5 = Late Middle Ages
    # 6 = Early Renaissance
    # 7 = Late Renaissance
    # 8 = Age of Reason

    # === Zones les plus avancées ===
    "Lantan": 8,           # Age of Reason
    "Halruaa": 7,          # Renaissance (Late)

    # === Zones très développées commercialement ===
    "Waterdeep": 7,
    "Baldur's Gate": 7,
    "Sembia": 7,
    "Calimshan": 7,
    "Amn": 7,

    # === Zones développées ===
    "Cormyr": 4,
    "Tethyr": 4,
    "Impiltur": 4,
    "Thesk": 4,
    "Turmish": 4,
    "Vilhon Reach": 4,
    "Chondath": 4,
    "Chessenta": 4,
    "Mulhorand": 4,
    "Unther": 4,

    # === Zones moyennes ===
    "The Dalelands": 4,
    "Aglarond": 4,
    "Moonsea": 4,
    "Damara": 4,
    "Rashemen": 4,
    "The Shaar": 4,
    "Lake of Steam": 4,
    "Border Kingdoms": 4,
    "Luiren": 4,

    # === Zones plus primitives / frontalières ===
    "Chult": 3,            # Iron Age
    "Jungle de Mhair": 3,
    "Anauroch": 3,
    "Hordelands (The Endless Wastes)": 3,
    "Icewind Dale": 3,
    "Spine of the World": 3,
    "Great Glacier": 0,    # Stone Age
    "Sossal": 3,
    "Vaasa": 3,

    # === Zones spéciales ===
    "Thay": 7,             # Technologie + magie (Late Renaissance)
    "Evermeet": 7,
    "Underdark": 4,        # Très variable selon la cité
    "Kara-Tur": 7,

    # Fallback
    "Default": 4,          # Middle Ages
}

# =============================================================================
# CONVERSION & UNITÉS
# =============================================================================
# Les valeurs REGION_MEDIAN_DAILY_WAGE_GP sont des "unités abstraites".
# Le capital est calculé comme (salaire journalier × 300) × niveau → pièces d'argent (sp).
# Le CAPITAL_BP_MULTIPLIER sert encore pour get_median_daily_wage_bp() (legacy/debug).
CAPITAL_BP_MULTIPLIER = 40.0

# Nombre d'années de salaire qui constituent le capital de départ d'un personnage
STARTING_CAPITAL_YEARS = 5.0

# =============================================================================
# CAPITAL DE DÉPART : PIÈCES D'ARGENT PAR NIVEAU
# =============================================================================
# Le capital de base (5 ans de salaire médian local) représente le montant
# "normal" pour un personnage de niveau 1 (doublé par rapport à la version 2.5 ans).
# Pour un personnage de niveau N, on multiplie par le niveau.
#
# Avec 5 ans, la cible médiane pour un perso moyen de niveau 1 est
# autour de 250 sp.
BASE_SILVER_PIECES_PER_LEVEL = 250  # mis à jour pour 5 ans de salaire (doublé)


def get_median_daily_wage(region_name: str, settlement_type: str) -> float:
    """
    Calcule le salaire médian journalier (en "unités abstraites").
    Utilisez get_median_daily_wage_bp() pour la valeur en bp réels.
    """
    base_wage = REGION_MEDIAN_DAILY_WAGE_GP.get(region_name, REGION_MEDIAN_DAILY_WAGE_GP["Default"])

    settlement_mult = SETTLEMENT_WAGE_MULTIPLIER.get(
        settlement_type, SETTLEMENT_WAGE_MULTIPLIER["Default"]
    )

    return round(base_wage * settlement_mult, 3)


def get_median_daily_wage_bp(region_name: str, settlement_type: str) -> float:
    """Salaire médian journalier en bronze pieces (bp) Rolemaster."""
    abstract = get_median_daily_wage(region_name, settlement_type)
    return round(abstract * CAPITAL_BP_MULTIPLIER, 2)


def calculate_starting_capital(
    region_name: str,
    settlement_type: str,
    ethnicity: str = None,   # Pour l'instant on ne l'utilise pas ici (sera ajouté plus tard)
    variance: bool = True,
    level: int = 1,
) -> int:
    """
    Calcule le capital de départ d'un personnage en **pièces d'argent (sp)**.

    Règle : 5 ans de salaire médian local × niveau du personnage (doublé).
    Le kit de base régional est fourni gratuitement (ne réduit pas ce capital).

    C'est l'équivalent d'une règle "X pièces d'argent par niveau", où X
    dépend de la région + du type de settlement (autour de 250 sp pour un
    personnage "moyen" de niveau 1 avec 5 ans).
    """
    daily_wage = get_median_daily_wage(region_name, settlement_type)

    # 5 ans de salaire local = base pour un perso de niveau 1
    DAYS_PER_YEAR = 300
    base_for_level_1 = daily_wage * DAYS_PER_YEAR * STARTING_CAPITAL_YEARS * 1.5 + 200

    capital = base_for_level_1 * max(1, level)

    if variance:
        capital *= random.uniform(0.80, 1.20)

    return int(round(capital))


def get_economic_summary(region_name: str, settlement_type: str, level: int = 1) -> dict:
    """Retourne un résumé lisible pour debug / compréhension."""
    daily_abstract = get_median_daily_wage(region_name, settlement_type)
    daily_bp = get_median_daily_wage_bp(region_name, settlement_type)
    capital = calculate_starting_capital(region_name, settlement_type, variance=False, level=level)

    return {
        "region": region_name,
        "settlement": settlement_type,
        "level": level,
        "median_daily_wage_abstract": daily_abstract,
        "median_daily_wage_bp": daily_bp,
        "estimated_annual_wage_sp": round(daily_abstract * 300),  # 1 an en unités "sp-like"
        "target_starting_capital_sp": capital,  # 5 ans × niveau
        "base_sp_per_level": BASE_SILVER_PIECES_PER_LEVEL,  # cible pour 5 ans (~250 sp)
    }


# =============================================================================
# VÉRIFICATION KIT vs CAPITAL (intégration avec regional_adventurer_kits)
# =============================================================================

def check_kit_fits_capital(region_name: str, settlement_type: str, kit_cost_bp: float = None) -> Dict:
    """
    Vérifie si le kit régional rentre dans le capital de départ.
    Retourne un dict avec les marges.
    """
    import data.equipment.regional_adventurer_kits as kits

    capital = calculate_starting_capital(region_name, settlement_type, variance=False, level=1)
    if kit_cost_bp is None:
        kit_cost_bp = kits.calculate_kit_cost_bp(region_name)

    margin = capital - kit_cost_bp
    ratio = (kit_cost_bp / capital * 100) if capital > 0 else 999

    kit_key = kits.REGION_TO_KIT.get(region_name, "temperate_middle_ages")
    return {
        "region": region_name,
        "settlement": settlement_type,
        "capital_bp": capital,
        "kit_cost_bp": round(kit_cost_bp, 1),
        "margin_bp": round(margin, 1),
        "kit_percent_of_capital": round(ratio, 1),
        "kit_type": kit_key,
        "fits_comfortably": margin > (capital * 0.25),  # Au moins 25% de marge
        "fits_strict": margin >= 0,
    }


if __name__ == "__main__":
    import random
    random.seed(42)

    test_cases = [
        ("Calimshan", "Metropolis"),
        ("The Shaar", "Caravan Oasis"),
        ("Spine of the World", "Isolated Hamlet"),
        ("Waterdeep", "Metropolis"),
        ("Chult", "Jungle Village"),           # fallback settlement
        ("Lantan", "Major Port City"),
        ("Great Glacier", "Isolated Hamlet"),
        ("Grand Glacier", "Farming Hamlet"),
        ("Hordelands (The Endless Wastes)", "Permanent Encampment"),
        ("Sembia", "Major Trade City"),
    ]

    print("=== Tests du système économique régional (capital en pièces d'argent sp) ===\n")

    for region, settlement in test_cases:
        summary = get_economic_summary(region, settlement)
        capital = calculate_starting_capital(region, settlement)
        check = check_kit_fits_capital(region, settlement)

        lvl = summary.get("level", 1)
        print(f"Région      : {region}")
        print(f"Settlement  : {settlement}")
        print(f"Salaire/jour : {summary['median_daily_wage_abstract']:.3f} (abstract)  |  {summary['median_daily_wage_bp']:.1f} bp")
        print(f"Capital niveau {lvl} (5 ans × niveau, sans variance) : {capital} sp")
        print(f"Kit régional (gratuit) : {check['kit_cost_bp']} bp")
        print(f"Capital restant (sp) : {capital} sp")
        print("-" * 60)


def estimate_median_starting_capital(n: int = 5000, level: int = 1, seed: int = 42) -> dict:
    """
    Estime la médiane réelle du starting capital en générant n personnages
    avec le vrai système (ethnicity -> région -> settlement + variance 0.8-1.2).
    C'est la méthode la plus précise.
    """
    import random
    if seed is not None:
        random.seed(seed)

    from utils import generate_character
    from statistics import median, mean

    caps = []
    for i in range(n):
        char = generate_character(f'STATS-{i:05d}', level=level)
        caps.append(char.get('Starting_Capital', 0))

    caps.sort()
    return {
        'n_samples': n,
        'level': level,
        'median_sp': median(caps),
        'mean_sp': round(mean(caps)),
        'min_sp': min(caps),
        'max_sp': max(caps),
        'p25_sp': caps[int(n * 0.25)],
        'p75_sp': caps[int(n * 0.75)],
    }


def get_theoretical_max_starting_capital(level: int = 1) -> int:
    """Retourne le capital de départ **maximum théorique** possible pour un niveau donné.

    Cela correspond à :
    - Le salaire journalier le plus élevé (Lantan = 0.64)
    - Le multiplicateur de settlement le plus élevé (Metropolis = 1.55)
    - 300 jours
    - STARTING_CAPITAL_YEARS (actuellement 5.0)
    - Variance maximale (+20%)
    """
    max_daily = max(REGION_MEDIAN_DAILY_WAGE_GP.values())
    max_mult = max(SETTLEMENT_WAGE_MULTIPLIER.values())

    daily = max_daily * max_mult
    base = daily * 300 * STARTING_CAPITAL_YEARS * max(1, level)
    max_cap = base * 1.20
    return int(round(max_cap))


if __name__ == "__main__":
    import random
    random.seed(42)

    test_cases = [
        ("Calimshan", "Metropolis"),
        ("The Shaar", "Caravan Oasis"),
        ("Spine of the World", "Isolated Hamlet"),
        ("Waterdeep", "Metropolis"),
        ("Chult", "Jungle Village"),
        ("Lantan", "Major Port City"),
        ("Great Glacier", "Isolated Hamlet"),
        ("Grand Glacier", "Farming Hamlet"),
        ("Hordelands (The Endless Wastes)", "Permanent Encampment"),
        ("Sembia", "Major Trade City"),
    ]

    print("=== Tests du système économique régional (capital en pièces d'argent sp) ===\n")

    for region, settlement in test_cases:
        summary = get_economic_summary(region, settlement)
        capital = calculate_starting_capital(region, settlement)
        check = check_kit_fits_capital(region, settlement)

        lvl = summary.get("level", 1)
        print(f"Région      : {region}")
        print(f"Settlement  : {settlement}")
        print(f"Salaire/jour : {summary['median_daily_wage_abstract']:.3f} (abstract)  |  {summary['median_daily_wage_bp']:.1f} bp")
        print(f"Capital niveau {lvl} (5 ans × niveau, sans variance) : {capital} sp")
        print(f"Kit régional (gratuit) : {check['kit_cost_bp']} bp")
        print(f"Capital restant (sp) : {capital} sp")
        print("-" * 60)

    print("\n=== Médiane réelle du Starting Capital ===")
    stats = estimate_median_starting_capital(n=4000, level=1, seed=42)
    print(f"Basé sur {stats['n_samples']} personnages générés (niveau {stats['level']}):")
    print(f"  Médiane : {stats['median_sp']} sp")
    print(f"  Moyenne : {stats['mean_sp']} sp")
    print(f"  25e-75e percentile : {stats['p25_sp']} - {stats['p75_sp']} sp")
    print(f"  Min / Max : {stats['min_sp']} / {stats['max_sp']} sp")
    print()

    max_theo = get_theoretical_max_starting_capital(level=1)
    print("=== Maximum théorique du Starting Capital ===")
    print(f"  Niveau 1 : {max_theo} sp")
    print(f"  Niveau N : {max_theo} × N sp")
    print()
    print("Le système est calibré pour une médiane autour de ~250 sp au niveau 1 (5 ans de salaire).")
    print("(BASE_SILVER_PIECES_PER_LEVEL = 250)")
