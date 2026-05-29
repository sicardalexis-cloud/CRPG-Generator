"""
data/equipment/regional_economy.py

Système économique régional pour le calcul des salaires médians et du capital de départ.

RÈGLES (cohérentes avec les fichiers DAILY WAGES & WORTH CHART + listes d'équipement) :
- Salaire médian défini manuellement par région (pas de "niveaux techno" purs, Faerûn est hybride).
- Capital de départ cible : **1 an** de salaire médian local (≈ 300 jours effectifs).
- Le kit de base régional (équipement porté + 14 jours de rations) est **fourni gratuitement** à la création.
- TOUT est calculé en bronze pieces (bp) Rolemaster (même unité que les kits d'équipement).
- Pas de référence D&D gp dans les calculs finaux.

Le capital (1 an) représente l'argent liquide + capacité à faire des achats supplémentaires
(montures, charettes, armure supérieure, etc.) avant de quitter son lieu d'origine.
"""

import random

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
    "Waterdeep": 0.28,
    "Baldur's Gate": 0.24,
    "Sembia": 0.26,
    "Calimshan": 0.22,
    "Lantan": 0.32,           # Plus avancé technologiquement
    "Halruaa": 0.25,

    # === Régions riches / fortement commerçantes ===
    "Amn": 0.18,
    "Cormyr": 0.17,
    "Tethyr": 0.16,
    "Impiltur": 0.15,
    "Turmish": 0.15,
    "Vilhon Reach": 0.16,
    "Chondath": 0.14,
    "Chessenta": 0.15,

    # === Régions moyennes / civilisées classiques ===
    "The Dalelands": 0.11,
    "Moonsea": 0.12,
    "Aglarond": 0.10,
    "Damara": 0.09,
    "The Shaar": 0.09,
    "Lake of Steam": 0.11,
    "Border Kingdoms": 0.10,
    "Luiren": 0.11,
    "Mulhorand": 0.12,
    "Unther": 0.10,
    "Rashemen": 0.09,
    "Thesk": 0.12,

    # === Régions plus pauvres ou frontalières ===
    "Vaasa": 0.06,
    "Icewind Dale": 0.05,
    "Le Nord (The North)": 0.07,
    "Spine of the World": 0.05,
    "Anauroch": 0.06,
    "Chult": 0.07,
    "Jungle de Mhair": 0.06,
    "Hordelands (The Endless Wastes)": 0.05,
    "Great Glacier": 0.03,
    "Sossal": 0.04,

    # === Régions spéciales / instables ===
    "Thay": 0.13,             # Riche mais très inégalitaire
    "Evermeet": 0.18,         # Riche mais isolée
    "Underdark": 0.09,        # Très variable selon la cité
    "Kara-Tur": 0.14,

    # === Régions 51+ (souvent plus spécifiques ou sauvages) ===
    "Old Empires": 0.10,
    "Unapproachable East": 0.09,
    "Western Heartlands": 0.11,
    "Sword Coast": 0.13,
    "Sword Coast North": 0.08,
    "Dragon Coast": 0.12,
    "Great Glacier": 0.03,
    "Inner Sea (Sea of Fallen Stars)": 0.12,
    "Dambrath": 0.08,
    "Estagund": 0.09,
    "Var the Golden": 0.10,
    "Shaarmid": 0.09,
    "Thindol": 0.07,
    "Samarach": 0.07,
    "Tashalar": 0.10,
    "The Shining South": 0.09,
    "Ymber": 0.06,
    "Nelanther Isles": 0.08,
    "The Whalebones": 0.05,
    "The Trackless Sea": 0.06,
    "The Cold Lands": 0.05,
    "The Endless Wastes": 0.05,
    "The Great Dale": 0.08,
    "The Plateau of Thay": 0.11,
    "The Easting Reach": 0.10,
    "The Forgotten Forest": 0.07,
    "The Lone Rock": 0.06,
    "The Reaching Woods": 0.08,
    "The Thunder Peaks": 0.09,
    "The Ride": 0.07,
    "Aglarondine": 0.09,
    "Bedine": 0.05,
    "Barakuir": 0.07,
    "Chondalwood": 0.06,
    "Citadelles du Nord": 0.08,
    "Cité Drow": 0.10,
    "Cité Souterraine Mixte": 0.08,
    "Eauprofonde": 0.09,
    "Épine dorsale (Nains arctiques)": 0.06,
    "Forêt d’Amtar / Methwood": 0.07,
    "Forteresses isolées": 0.07,
    "Gracklstugh": 0.09,
    "Grande Faille": 0.08,
    "Grand Glacier": 0.03,
    "Glacière éternelle": 0.03,
    "Ruathym": 0.07,
    "Luirwood": 0.06,
    "Myth Drannor": 0.08,
    "Evereska": 0.12,
    "Valbise": 0.07,
    "Vallée de la Flamme": 0.06,
    "Les Vaux": 0.08,
    "Vast": 0.09,
    "Zakharans": 0.10,
    "Pics Gris": 0.05,
    "Outreterre tropicale": 0.06,
    "Forêts du Nord (Gnomes)": 0.07,
    "Éternelle-Rencontre": 0.09,
    "Lunargent": 0.10,
    "Bois de Yuir": 0.08,
    "Montagnes du Shaar": 0.07,
    "Vil Adanrath": 0.05,
    "Tymanther": 0.09,
    "Icerim Mountains": 0.04,
    "Montagnes Theskiennes": 0.07,
    "Montagnes de Cuivre": 0.08,
    "Kara-Tur": 0.14,
    "Pics de Mir": 0.06,
    "Bois de Shaar": 0.06,
    "Outreterre profonde": 0.07,
    "Lycanthropes": 0.05,
    "Wemics": 0.04,
    "Yuan-ti": 0.06,
    "Centaure": 0.05,
    "Homme-lézard": 0.04,
    "Tanarukks": 0.05,
    "Fey’ri": 0.07,
    "Sagespectres": 0.06,
    "Vaillants": 0.08,
    "Kir-lanan": 0.05,
    "Reflets (Shades)": 0.07,

    # Fallback
    "Default": 0.08,
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
# On les convertit en bronze pieces (bp) Rolemaster pour cohérence avec les kits.
# Le capital final correspond à 1 an de salaire local.
CAPITAL_BP_MULTIPLIER = 40.0


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
    variance: bool = True
) -> int:
    """
    Calcule le capital de départ visé pour un personnage "aisé mais pas riche".

    Cible : 1 an de salaire médian local, exprimé en bronze pieces (bp) Rolemaster.
    Le kit de base régional est fourni gratuitement (ne réduit pas ce capital).
    """
    daily_wage = get_median_daily_wage(region_name, settlement_type)

    # 1 an de salaire (300 jours effectifs)
    # 300 jours/an est conservateur (maladies, fêtes, voyages, etc.)
    annual_wage = daily_wage * 300

    # Conversion en bp réels + variance
    capital = annual_wage * CAPITAL_BP_MULTIPLIER

    if variance:
        capital *= random.uniform(0.80, 1.20)

    # Minimum absolu décent (même un miséreux du Grand Glacier a de quoi survivre)
    capital = max(80, capital)

    return int(round(capital))


def get_economic_summary(region_name: str, settlement_type: str) -> dict:
    """Retourne un résumé lisible pour debug / compréhension (unités bp)."""
    daily_abstract = get_median_daily_wage(region_name, settlement_type)
    daily_bp = get_median_daily_wage_bp(region_name, settlement_type)
    capital = calculate_starting_capital(region_name, settlement_type, variance=False)

    return {
        "region": region_name,
        "settlement": settlement_type,
        "median_daily_wage_abstract": daily_abstract,
        "median_daily_wage_bp": daily_bp,
        "estimated_annual_wage_bp": round(daily_bp * 300),
        "target_starting_capital_1year_bp": capital,
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

    capital = calculate_starting_capital(region_name, settlement_type, variance=False)
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

    print("=== Tests du système économique régional (capital en bp Rolemaster) ===\n")

    for region, settlement in test_cases:
        summary = get_economic_summary(region, settlement)
        capital = calculate_starting_capital(region, settlement)
        check = check_kit_fits_capital(region, settlement)

        print(f"Région      : {region}")
        print(f"Settlement  : {settlement}")
        print(f"Salaire/jour : {summary['median_daily_wage_bp']:.1f} bp")
        print(f"Capital 1 an (sans variance) : {capital} bp")
        print(f"Kit régional (gratuit) : {check['kit_cost_bp']} bp")
        print(f"Capital restant pour achats supplémentaires : {capital} bp")
        print("-" * 60)
