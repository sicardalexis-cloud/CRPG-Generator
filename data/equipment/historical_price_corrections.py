"""
data/equipment/historical_price_corrections.py

Ajustements de prix pour plus de réalisme historique (XIIᵉ-XVᵉ siècle).

Source principale :
Document "ÉVOLUTION DES PRIX DES ARMURES DU XIIᵉ AU XVᵉ SIÈCLE"
fourni par l'utilisateur (27 mai 2026).

Système monétaire :
- 1 pièce d’argent = 1 sp = ¼ once troy ≈ 7,78 g d’argent fin
- 1 kg d’argent ≈ 128,6 pièces d’argent
"""

from typing import Dict

# =============================================================================
# CORRECTIONS DE PRIX - RÉALISME HISTORIQUE (basé sur le document utilisateur)
# =============================================================================
# Format : "Nom exact de l'item" : "prix en sp (silver piece = pièce d'argent)"

HISTORICAL_PRICE_OVERRIDES: Dict[str, str] = {
    # Note : Full plate et Half plate ont été retirés des items individuels.
    # Ils seront construits comme des kits à partir des pièces modulaires.
    # Brigandine reste comme pièce unique.

    "Plate mail barding": "900 sp",
    "Subarmalis": "55 sp",
    "Thoracomachus": "48 sp",
    "Aketon": "58 sp",
    "Gambeson": "42 sp",
    "Reinforced Gambeson": "65 sp",
    "Padded Jack": "85 sp",
    "Jack of Plates": "125 sp",
    "Brigandine": "145 sp",
    "Arming Doublet": "95 sp",
    "Coat of plates": "200 sp",
    "Chain hauberk": "220 sp",

    # === PROTECTION DE BASE ===
    "Salet": "42 sp",

    # === DÉCOMPOSITION ARMURE XIVᵉ SIÈCLE (modulaire) ===
    # Pièces de transition du XIVe siècle : armures encore très influencées par la maille,
    # avec des plaques de métal rivetées ou attachées. Moins sophistiquées que les versions gothiques du XVe.
    "Hauberk": "140 sp",
    "Coat of Plates": "85 sp",
    "Pauldrons (Early)": "32 sp",           # 14th century: smaller, simpler shoulder defenses
    "Brassards / Vambraces": "38 sp",
    "Gauntlets (Mitten)": "25 sp",          # 14th century: fingers not individually articulated
    "Cuisses (Early)": "32 sp",             # 14th century: basic thigh protection
    "Poleyns (Early)": "20 sp",             # 14th century: simple knee cops
    "Greaves (Early)": "28 sp",             # 14th century: basic shin protection
    "Sabatons (Pointed)": "20 sp",          # Late 14th–early 15th: characteristic gothic pointed style
    "Bascinet (Early)": "50 sp",            # Early bascinet of the 14th century
    "Aventail": "20 sp",

    # === DÉCOMPOSITION ARMURE XVᵉ SIÈCLE (modulaire) ===
    # Source : document historique (27 mai 2026)
    # Style gothique : formes plus élancées, meilleure articulation, transition vers les harnais complets.
    "Haubergeon / Collerette maille": "50 sp",
    "Breastplate + Backplate (Gothic)": "80 sp",   # Classic 15th century gothic style
    "Gorget (Gothic)": "25 sp",                    # Higher and more protective 15th c. gorget
    "Pauldrons (Gothic)": "30 sp",                 # Larger, reinforced shoulder armor of the 15th century
    "Vambraces + Couter": "35 sp",
    "Gauntlets (Gothic)": "25 sp",                 # Well-articulated finger gauntlets (15th c.)
    "Tassets": "25 sp",
    "Cuisses (Gothic)": "30 sp",                   # Articulated thigh plates of the 15th century
    "Poleyns (Gothic)": "18 sp",                   # Winged knee cops typical of 15th c. Gothic armor
    "Greaves (Gothic)": "25 sp",                   # Better contoured and articulated greaves (15th c.)
    "Sabatons (Pointed)": "20 sp",                 # Characteristic pointed gothic sabatons
    "Sallet ou Armet (Gothic)": "55 sp",           # Classic 15th century gothic sallet or armet

    # === DÉCOMPOSITION ARMURE XVIᵉ SIÈCLE (modulaire) ===
    # Style Maximilian / Renaissance tardive : armures plus massives, souvent conçues pour résister aux débuts des armes à feu.
    "Maille collerette ou manches": "32 sp",
    "Breastplate + Backplate (Maximilian)": "95 sp",   # Heavier 16th c. plates, thicker to resist firearms
    "Gorget (Maximilian)": "27 sp",                    # More rigid and reinforced 16th c. gorget
    "Pauldrons (Maximilian)": "38 sp",                 # Large shoulder defenses with additional guards (16th c.)
    "Vambraces + Couter + Rerebrace": "42 sp",         # Complete arm harness (upper + lower arm)
    "Gauntlets (Maximilian)": "28 sp",                 # Heavier, more robust gauntlets of the 16th century
    "Tassets longs": "32 sp",
    "Cuisses (Maximilian)": "34 sp",                   # Longer and more protective thigh plates (16th c.)
    "Poleyns (Maximilian)": "23 sp",                   # Reinforced knee protection of the Maximilian period
    "Greaves (Maximilian)": "28 sp",                   # Stronger and more resistant shin defenses (16th c.)
    "Sabatons (Broad)": "23 sp",                       # Wider, more functional sabatons of the 16th century
    "Close Helmet (Maximilian)": "65 sp",              # Fully enclosed 16th century helmet with movable visor
    "Burgonet (Maximilian)": "55 sp",                  # 16th century open-faced helmet popular with cavalry and officers

    # === BOUCLIERS HISTORIQUES (remplacés) ===
    # Antiquité
    "Aspis (Hoplon)": "55 sp",
    "Scutum": "60 sp",
    "Clipeus": "40 sp",
    "Parma": "28 sp",

    # Bouclier rond classique (disponible dès l'Âge du Bronze)
    "Round Shield": "30 sp",

    # Moyen Âge central et tardif
    "Kite Shield": "45 sp",
    "Heater Shield": "30 sp",

    # Renaissance
    "Buckler": "22 sp",
    "Pavise": "60 sp",
    "Targe": "32 sp",
    "Rotella": "40 sp",
    "Parade Shield": "115 sp",

    # === ARMURES Ve - XIe SIÈCLE (nouveau document) ===
    # Très pertinent pour régions "Iron Age" et "early Middle Ages"
    # (5th to 11th century)

    # 5th-6th century
    "Lorica squamata": "160 sp",           # Scale armor (wealthy warriors)
    "Spangenhelm (Early)": "55 sp",        # Segmented helmet (5th-6th century style)

    # 7th century
    "Hauberk de maille": "230 sp",         # 180-280 sp
    "Nasal helmet (Early Medieval)": "60 sp",

    # 8th-9th century (Carolingian)
    "Byrnie carolingienne": "210 sp",      # 160-260 sp
    "Spangenhelm (Carolingian)": "50 sp",

    # 10th-11th century
    "Hauberk long": "190 sp",              # 140-240 sp (reaching the knees)
    "Nasal helmet (11th c.)": "45 sp",

    # === CASQUES HISTORIQUES — LISTE COMPLÈTE (document 27 mai 2026) ===
    # Source : "LISTE DES TYPES DE CASQUES HISTORIQUES (Du monde antique au XVIe siècle)"
    # Prix choisis : milieu de fourchette ou valeur conservative pour versions standards.

    # --- Antiquité (Grèce, Rome, Celtes) ---
    "Corinthian Helmet": "65 sp",          # 50-80, classic Greek hoplite helmet (5th-4th c. BC)
    "Attic Helmet": "52 sp",               # 40-65, lighter and more comfortable Greek helmet
    "Phrygian / Thracian Helmet": "45 sp", # 35-55, associated with Thracian and Phrygian cavalry
    "Boeotian Helmet": "42 sp",            # 35-50, open Greek helmet inspired by Boeotian hats, good for cavalry
    "Montefortino Helmet": "57 sp",        # 45-70, standard Roman legionary helmet (3rd c. BC – 1st c. AD)
    "Coolus Helmet": "50 sp",              # 40-60, lighter Roman variant (1st c. BC – 1st c. AD)
    "Imperial Gallic Helmet": "62 sp",     # 50-75, the most widespread Roman helmet of the 1st-2nd c. AD
    "Intercisa Helmet": "32 sp",           # 25-40, late Roman economical helmet (4th-5th c. AD)
    "Celtic Helmet": "45 sp",              # 35-55, various Celtic designs (La Tène style), often with crests

    # --- Haut Moyen Âge ---
    "Spangenhelm (Early)": "42 sp",        # 30-50, segmented helmet (5th-6th c. style)
    "Nasal helmet (Early Medieval)": "52 sp",  # 35-55, with nasal bar (7th c. style)
    "Spangenhelm (Carolingian)": "42 sp",  # 30-50, later evolution (8th-9th c.)
    "Nasal helmet (11th c.)": "45 sp",     # 35-55, classic Norman style (11th century)

    # --- Moyen Âge central et tardif ---
    "Great Helm": "65 sp",                 # 50-80, fully enclosed "bucket" helmet (12th-13th c., tournaments/battle)
    "Cerveliere": "32 sp",                 # 25-40, simple steel skullcap (late 13th-14th c.)
    "Bascinet (early)": "50 sp",           # 40-60, early pointed bascinet (early 14th c.)
    "Bascinet": "55 sp",                   # 45-70, classic pig-faced or rounded bascinet (late 14th c., most common)
    "Sallet": "52 sp",                     # 40-65, iconic 15th c. helmet with tail at the back
    "Armet": "65 sp",                      # 50-80, sophisticated fully enclosed Italian-style helmet (15th c.)

    # --- Renaissance ---
    "Sallet ou Armet (Gothic)": "58 sp",       # Late 15th century transitional style
    "Close Helmet (Maximilian)": "70 sp",      # 16th century fully enclosed helmet (55-85 sp)
    "Burgonet (Maximilian)": "55 sp",          # 16th century open helmet popular with cavalry (45-70 sp)
    "Morion": "45 sp",                         # 35-55 sp (pikemen and arquebusiers, 16th-17th c.)
    "Lobster-tailed Pot": "50 sp",             # 17th century cavalry helmet (40-60 sp)

    # === PIÈCES COURANTES / INFANTERIE (document 27 mai 2026) ===
    # Pièces très répandues chez les troupes de pied et les hommes d'armes moyens.
    "Kettle hat": "28 sp",                 # 20-35 sp - most common helmet 13th-15th c.
    "Mail coif": "22 sp",                  # 15-30 sp - independent mail hood (12th-15th c.)
    "Simple Breastplate": "50 sp",         # 40-60 sp - front torso plate only (late 14th-15th c.)
    "Bronze cuirass": "110 sp",            # Expensive for the period, low tech (Bronze Age / early Iron Age)
    "Bronze greaves": "55 sp",             # Pair, expensive but available very early
    "Fauld": "32 sp",                      # 25-40 sp - lames skirt under the cuirass (15th c.)
    "Besagews (pair)": "20 sp",            # 15-25 sp the pair - armpit protectors (15th c.)

    # === PIÈCES SPÉCIFIQUES (SUITE - document 27 mai 2026) ===
    "Plackart": "40 sp",                   # 30-50 sp - reinforcement on the breastplate (15th c.)
    "Couter (pair)": "16 sp",              # 12-20 sp the pair - separate elbow guards (14th-15th c.)
    "Mail voiders (pair)": "20 sp",        # 15-25 sp the pair - mail under the plates (14th-15th c.)
    "Arming doublet": "55 sp",             # 45-65 sp - structured doublet with attachment points for plates (15th c.)
    "Greaves / Poleyns simples (pair)": "27 sp",  # 20-35 sp the pair - basic leg protection (13th-early 14th c.)
    "Cuir bouilli (jambières)": "25 sp",   # 15-40 sp - boiled leather for light troops
    "Cuir bouilli (brassards)": "18 sp",   # 15-40 sp - boiled leather version for arms

    # === COMPLÉMENTS DE HARNAIS (estimations basées sur les documents historiques) ===
    # Pièces courantes sur les harnais 15th-16th c. mais pas encore intégrées auparavant.
    "Bevor": "28 sp",                      # ~25-35 sp - chin and lower face protection (15th c.)
    "Garde-reins": "35 sp",                # ~30-45 sp - back protection for the kidneys (15th c.)
    "Lance rest": "15 sp",                 # ~12-20 sp - lance stop on the breastplate (late 14th-15th c.)
    "Mail fauld": "24 sp",                 # ~20-30 sp - mail skirt (cheaper alternative to plate fauld, 14th-15th c.)

    # === Protections de jambes rudimentaires (estimations) ===
    # Versions plus simples existant au Moyen Âge et avant les pièces articulées du XIVe
    "Chausses de maille": "95 sp",         # ~80-120 sp (12th-14th c.) - full mail chausses
    "Knee cops (basic)": "16 sp",          # ~12-20 sp (Middle Ages) - simple knee protectors
    "Leather greaves": "20 sp",            # ~15-25 sp (Middle Ages and earlier) - basic leather shin guards

    # === MONTURES (CHEVAUX) — document 27 mai 2026 ===
    # Source : "PRIX DES MONTURES (CHEVAUX) SELON LES SIÈCLES"
    # Prix choisis : milieu de fourchette ou valeur conservative pour versions standards.

    # Most common horses (14th-15th c.)
    "Rouncey": "45 sp",                    # 35-55 sp - most common all-purpose horse
    "Courser": "62 sp",                    # 50-75 sp - fast hunting and light war horse

    # Prestige / parade horses
    "Palfrey": "57 sp",                    # 45-70 sp - lady's and parade horse

    # Heavy war horses (destriers)
    "Destrier": "130 sp",                  # 100-160 sp - good war destrier
    "Destrier (quality)": "200 sp",        # 180-250+ sp - exceptional / royal horse

    # === ARMES HISTORIQUES (document 27 mai 2026) ===
    # Source : "LISTE DES ARMES HISTORIQUES (Du monde antique à la Renaissance)"
    # (Prices kept without century in the name; historical context is in comments above each category when relevant)

    # Armes antiques
    "Gladius": "50 sp",
    "Pilum, Roman": "35 sp",
    "Verutum, Roman Light": "11 sp",
    "Javelin, Iron Leaf-Shaped": "14 sp",
    "Javelin, Iron Bodkin": "18 sp",
    "Spatha": "55 sp",
    "Xiphos": "45 sp",
    "Dory (Spear)": "32 sp",
    "Bow, Composite": "28 sp",             # Arc composite ancien (~2000 av. J.-C.), version early elite
    "Composite Bow": "52 sp",
    "Quiver": "10 sp",                     # Contenant standard pour flèches. Obligatoire avec arc.
    "Celtic Sword": "52 sp",
    "Akinakes": "32 sp",
    "Javelin": "18 sp",
    "Francisca": "24 sp",
    "Throwing Knife": "14 sp",
    "Plumbata": "16 sp",
    "War Pick": "26 sp",
    "Sling": "12 sp",

    # Âge du Bronze et antérieur
    "Javelin, Stone-Tipped": "4 sp",
    "Club, Great": "5 sp",
    "Hand Axe, Stone": "6 sp",
    "Atlatl": "9 sp",
    "Mace, Stone": "10 sp",
    "Javelin, Copper-Tipped": "7 sp",
    "Javelin, Bronze Leaf-Shaped": "12 sp",
    "Javelin, Bronze Socketed": "15 sp",
    "Dagger, Bronze": "12 sp",
    "Axe, Bronze": "20 sp",
    "Sword, Bronze": "38 sp",

    # Haut Moyen Âge
    "Large Sword": "55 sp",
    "Dane Axe": "45 sp",
    "Arming Sword": "45 sp",
    "Mace": "38 sp",
    "War Hammer": "40 sp",
    "Longbow (early)": "28 sp",
    "War Dart, Medieval": "16 sp",
    "Sabre": "42 sp",
    "Rondel Dagger": "28 sp",
    "Seax": "30 sp",
    "Lance": "32 sp",
    "Battle Axe": "35 sp",
    "Bearded Axe": "40 sp",
    "Flail": "42 sp",
    "Quarterstaff": "8 sp",

    # Fin du Moyen Âge
    "Longsword": "65 sp",
    "Falchion": "45 sp",
    "Poleaxe": "70 sp",
    "Halberd": "65 sp",
    "Crossbow": "85 sp",
    "Longbow": "30 sp",
    "Bill": "57 sp",
    "Handgonne": "160 sp",
    "Flanged Mace": "55 sp",
    "Morning Star": "50 sp",
    "Boar Spear": "35 sp",
    "Glaive, Polearm": "55 sp",
    "Voulge": "48 sp",
    "Heavy Crossbow": "95 sp",

    # Renaissance
    "Rapier": "80 sp",
    "Javelin, Renaissance": "22 sp",
    "Wheellock Pistol": "110 sp",
    "Blunderbuss": "75 sp",
    "Shamshir": "58 sp",
    "Sidesword": "65 sp",
    "Pike": "40 sp",
    "Arquebus": "130 sp",
    "Musket": "180 sp",
    "Main-gauche": "32 sp",
    "War Hammer (Renaissance)": "52 sp",
    "Partisan": "52 sp",
    "Cranequin Crossbow": "140 sp",
    "Great Axe": "60 sp",
    "Lochaber Axe": "58 sp",
    "Bec de Corbin": "65 sp",
    "Maul": "45 sp",
    "Lucerne Hammer": "62 sp",
    "Military Fork": "48 sp",
    "Ranseur": "50 sp",
    "Light Crossbow": "55 sp",
    "Composite Crossbow": "75 sp",
    "Broadsword": "55 sp",
    "Cutlass": "48 sp",
    "Estoc": "70 sp",
    "2 Handed Sword": "110 sp",
    "Flintlock Pistol": "85 sp",
}

# =============================================================================
# NOTES SUR LES AJUSTEMENTS
# =============================================================================
"""
Full plate (Harnois complet de chevalier) :
- Prix original : 200 sp
Règles de conversion appliquées :

Source : Document "ÉVOLUTION DES PRIX DES ARMURES DU XIIᵉ AU XVᵉ SIÈCLE"
- 1 pièce d’argent = 1 sp = ¼ once troy ≈ 7,78 g
- 1 kg d’argent ≈ 128,6 pièces d’argent

Prix retenus (moyennes du tableau historique) :
- Full plate (bon harnois XVᵉ)        : 320 sp
- Half plate / early plate            : 260 sp
- Brigandine (la plus courante)       : 195 sp
- Jack of plates                      : 155 sp
- Gambeson                            : 50 sp
- Salet                               : 42 sp
- Chain hauberk (XIIIᵉ-XIVᵉ)          : 220 sp

Ces prix reflètent la réalité historique : la brigandine et le jack of plates
étaient les protections standards de la grande majorité des combattants,
tandis que la full plate restait réservée à la noblesse aisée.
"""

def get_historical_price(item_name: str, original_price: str) -> str:
    """
    Retourne le prix historique corrigé s'il existe,
    sinon retourne le prix original.
    """
    return HISTORICAL_PRICE_OVERRIDES.get(item_name, original_price)


# Pour debug / vérification
if __name__ == "__main__":
    print("=== Corrections de prix historiques (basées sur le document utilisateur) ===\n")
    for item, new_price in HISTORICAL_PRICE_OVERRIDES.items():
        print(f"{item:30} → {new_price}")
    print("\nSource : ÉVOLUTION DES PRIX DES ARMURES DU XIIᵉ AU XVᵉ SIÈCLE")
