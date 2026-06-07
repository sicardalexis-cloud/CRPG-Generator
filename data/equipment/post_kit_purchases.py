"""
data/equipment/post_kit_purchases.py

Système de "Dépenses Post-Kit" – Achats supplémentaires avec le capital de départ (1 an).

NOUVELLE APPROCHE (en cours de développement) :
Un personnage riche n'achète pas forcément une monture.
Il a souvent plus de chances d'investir dans :
- Pièces d'armure (breastplate, hauberk, etc.)
- Armes de meilleure qualité ou supplémentaires (épée, hache, lance, bouclier...)
- Équipement de voyage de qualité (tentes, sellerie, outils)

Le système doit être :
- Multi-catégories
- Probabiliste et varié
- Fortement influencé par la richesse restante ET la région
- Généreux mais réaliste

Ce fichier est en pleine évolution car le sujet est vaste et complexe.
"""

from typing import Dict, List, Tuple, Optional
import random

from . import regional_adventurer_kits as kits
from . import historical_price_corrections as price_fix
from .regional_economy import REGION_TECH_LEVEL
from . import equipment_groups
from . import group_equipment_pools
from . import groupe1_prices as grp_prices

# =============================================================================
# RÈGLES DE PRIORITÉ D'ARMES - NIVEAU 1 + NIVEAU 2 (implémentés)
# =============================================================================
# NIVEAU 1 (implémenté) :
# - Bloquer l'achat de Main-gauche et petits boucliers (PARRYING_WEAPONS)
#   tant que le personnage n'a pas encore d'arme principale une main.
# - Donner une très forte priorité aux PRIMARY_ONE_HANDED_WEAPONS.
#
# NIVEAU 2 (implémenté) :
# - Règle historique d'encombrement : "pas 2 armes lourdes sans animal
#   pour stocker la deuxieme".
# - Une arme avec encumbrance >= 4 (Longsword, polearms, gros 2H, arquebuse...)
#   ne compte pas dans les 7 points, mais doit être portée à la main.
# - Sans monture (Rouncey, Mule, Camel...), impossible de transporter
#   une seconde arme de ce type pendant les achats post-kit.
# - Implémentation proactive (filtrage des candidats dans la boucle Weapons)
#   + garde-fou final dans enforce_no_mount_carry_limits.
# =============================================================================

# Armes principales à une main (ce qu'on considère comme "bonne arme primaire")
PRIMARY_ONE_HANDED_WEAPONS = {
    "Arming Sword", "Sidesword", "Rapier", "Sabre", "Shamshir",
    "Broadsword", "Cutlass", "Scimitar", "Estoc",
    "Battle Axe", "Bearded Axe", "Mace", "Flanged Mace",
    "War Hammer", "Morning Star"
}

# Armes "secondaires / défensives" qui ne devraient pas être achetées en premier
PARRYING_WEAPONS = {
    "Main-gauche",
    "Buckler", "Targe", "Rotella"   # petits boucliers considérés comme "parrying"
}

# =============================================================================
# NOUVELLE APPROCHE : CATÉGORIES D'ACHATS
# =============================================================================
# Un personnage riche n'achète pas forcément une monture.
# Il a souvent plus tendance à s'équiper en armure, armes, et matériel de qualité.

CATEGORIES = ["Armor", "Weapons", "Mobility", "TravelGear", "RidingGear"]

# Items réels extraits des listes d'équipement (prix en Rolemaster)
# Ces listes vont s'enrichir progressivement.

ARMOR_UPGRADES: List[Tuple[str, str]] = [
    # === ARMURES TEXTILES & MATELASSÉES (évolution historique) ===
    # Descriptions détaillées pour bien différencier chaque type.
    ("Subarmalis", "55 sp"),               # Roman Empire (1st–5th c.): Quilted padded vest made of layered linen or felt, often fitted with pteryges (shoulder and waist flaps). Worn directly under lorica segmentata or hamata to absorb blunt force trauma and prevent chafing.
    ("Thoracomachus", "48 sp"),            # Late Roman / Early Medieval (4th–8th c.): Felt-padded protective garment, sometimes covered with leather for waterproofing. Designed to cushion the body from the weight and friction of heavy metal armor. Mentioned in late Roman military treatises.
    ("Aketon", "58 sp"),                   # High Middle Ages (12th–13th c.): Classic padded armor made of layered linen or cotton (from Arabic *al-qutn*). Lighter and more fitted than later gambesons. Primarily worn under chainmail, but can also serve as light standalone protection.
    ("Gambeson", "42 sp"),                 # Early to Late Middle Ages: Simple thick padded tunic. The most basic and affordable version. Good entry-level protection, often worn alone or under mail.
    ("Reinforced Gambeson", "65 sp"),      # Late Middle Ages (14th c.): Classic thick and well-quilted gambeson (linen + wool). The most common and versatile model used across Europe. Can be worn standalone or under plate.
    ("Padded Jack", "85 sp"),              # Late Middle Ages → Early Renaissance: Heavier and more rigid padded armor with many layers (18–30+). Often worn alone by infantry and archers. Offers better standalone protection than a standard gambeson.
    ("Jack of Plates", "125 sp"),          # Renaissance (15th–16th c.): Padded jack with small iron plates sewn inside the lining. Excellent protection while remaining relatively flexible. A major evolution in textile armor.
    ("Brigandine", "145 sp"),              # Late Middle Ages → Renaissance (14th–16th c.): Fabric coat with small overlapping metal plates riveted to the inside. Much better protection against thrusts and arrows than pure padded armor. Visually and mechanically distinct from all other textile armors.
    ("Arming Doublet", "95 sp"),           # Late Renaissance (late 15th–16th c.): Finely tailored and structured garment designed specifically to be worn under a full plate harness. Features lacing points to attach armor plates. Less padded, more technical.

    # === PIÈCES COURANTES / INFANTERIE (document 27 mai 2026) ===
    # Très répandues chez les fantassins, archers et hommes d'armes moyens.
    ("Kettle hat", "28 sp"),               # 20-35 sp - le casque le plus commun XIIIe-XVe
    ("Mail coif", "22 sp"),                # 15-30 sp - coif de maille indépendant (distinct de l'Aventail)
    ("Simple Breastplate", "50 sp"),       # 40-60 sp - plastron avant seulement (fin XIVe-XVe)
    ("Bronze cuirass", "110 sp"),          # Cher, mais disponible dès l'Antiquité (Bronze Age / début Iron Age). Lourde et prestigieuse.
    ("Bronze greaves", "55 sp"),           # Paire de jambières de bronze - cher pour l'époque, tech faible (disponible tôt).
    ("Fauld", "32 sp"),                    # 25-40 sp - jupe de lames horizontales sous la cuirasse
    ("Besagews (pair)", "20 sp"),          # 15-25 sp la paire - protections d'aisselles (XVe)

    # === PIÈCES SPÉCIFIQUES (SUITE - document 27 mai 2026) ===
    # Plackart, voiders, couters séparés, protections précoces et cuir bouilli
    ("Plackart", "40 sp"),                           # 30-50 sp - renfort sur plastron (XVe)
    ("Couter (pair)", "16 sp"),                      # 12-20 sp la paire - garde-coudes seuls
    ("Mail voiders (pair)", "20 sp"),                # 15-25 sp la paire - maille sous les plates
    ("Greaves / Poleyns simples (pair)", "27 sp"),   # 20-35 sp la paire - versions précoces XIIIe-XIVe
    ("Cuir bouilli (jambières)", "25 sp"),           # 15-40 sp - cuir bouilli (troupes légères)
    ("Cuir bouilli (brassards)", "18 sp"),           # 15-40 sp - version brassards

    # === Protections de jambes rudimentaires (Moyen Âge et avant) ===
    # Versions plus simples et plus anciennes que les pièces articulées du XIVe+
    ("Chausses de maille", "95 sp"),         # ~80-120 sp - jambières de maille (XIIe-XIVe)
    ("Knee cops (basic)", "16 sp"),          # ~12-20 sp - simples protège-genoux (Moyen Âge)
    ("Leather greaves", "20 sp"),            # ~15-25 sp - jambières de cuir simple (Moyen Âge et avant)

    # === COMPLÉMENTS DE HARNAIS (estimés d'après documents historiques) ===
    # Pièces fréquentes sur les harnais complets du XVe-XVIe mais encore absentes
    ("Fauld", "32 sp"),                      # 25-40 sp (XVe) - jupe de lames sous la cuirasse (déjà présent)
    ("Bevor", "28 sp"),                      # ~25-35 sp (XVe) - protection menton / bas du visage
    ("Garde-reins", "35 sp"),                # ~30-45 sp (XVe) - protection des reins dans le dos
    ("Lance rest", "15 sp"),                 # ~12-20 sp (fin XIVe-XVe) - arrêt de lance sur le plastron
    ("Mail fauld", "24 sp"),                 # ~20-30 sp (XIVe-XVe) - jupe de maille (alternative au fauld de plates)

    # === DÉCOMPOSITION ARMURE XIVᵉ SIÈCLE (modulaire) ===
    # Descriptions pour distinguer les versions par période et sophistication.
    ("Hauberk", "140 sp"),                # Full mail shirt, long and heavy. The dominant torso protection before and during the early plate transition.
    ("Coat of Plates", "85 sp"),          # Early transitional torso armor: metal plates riveted inside a fabric or leather covering. Precursor to true plate harness.
    ("Pauldrons (simples)", "32 sp"),     # 14th c.: Smaller, lighter shoulder defenses. Limited coverage, often just a simple plate over the shoulder.
    ("Pauldrons (renforcés)", "30 sp"),   # 15th c.: Larger and more protective pauldron, especially the left one for jousting. Better coverage of the shoulder joint.
    ("Brassards / Vambraces", "38 sp"),   # Arm defenses covering the forearm. Can be simple or articulated depending on the period.
    ("Gauntlets (moufles)", "25 sp"),     # 14th c.: Gauntlets with minimal finger articulation (often mitten style). Simpler and heavier to use.
    ("Gauntlets (articulés)", "25 sp"),   # 15th c.: Much better finger separation and articulation. More dexterous than earlier mitten versions.
    ("Gauntlets (renforcés)", "28 sp"),   # 16th c.: Heavier and more robust gauntlets, sometimes with extra reinforcements for jousting.
    ("Cuisses (simples)", "32 sp"),       # 14th c.: Basic thigh protection. Often attached to mail or leather chausses rather than fully independent.
    ("Cuisses (articulées)", "30 sp"),    # 15th c.: Well-articulated thigh plates offering good protection and mobility.
    ("Cuisses (renforcées)", "34 sp"),    # 16th c.: Longer and more protective cuisses, sometimes integrated with tassets for better overall coverage.
    ("Poleyns (basiques)", "20 sp"),      # 14th c.: Simple knee cops with limited articulation.
    ("Poleyns (ailés)", "18 sp"),         # 15th c.: Knee cops with lateral "wings" for better side protection.
    ("Greaves (simples)", "28 sp"),       # 14th c.: Basic shin protection, often flatter and less anatomical.
    ("Greaves (articulées)", "25 sp"),    # 15th c.: Better shaped to the leg, improved articulation with poleyns.
    ("Greaves (renforcées)", "28 sp"),    # 16th c.: More robust greaves, sometimes with additional reinforcements.
    ("Sabatons (pointus)", "20 sp"),      # 14th–15th c.: Gothic style sabatons with elongated pointed toes. Less practical for walking.
    ("Sabatons (larges)", "23 sp"),       # 16th c.: Wider, more rounded sabatons. Better stability and comfort.
    ("Aventail", "20 sp"),                # Mail neck and shoulder defense attached to a helmet (basically a mail curtain).

    # === DÉCOMPOSITION ARMURE XVᵉ SIÈCLE (modulaire) ===
    # Source : document historique détaillé (27 mai 2026)
    ("Haubergeon / Collerette maille", "50 sp"),   # Mail shirt or collar used as secondary defense under or with plate.
    ("Breastplate + Backplate (classique)", "80 sp"),  # Classic 15th c. gothic style breastplate + backplate. Good balance of protection and mobility.
    ("Gorget (élevé)", "25 sp"),                   # 15th c.: Higher and more protective gorget than earlier versions.
    ("Vambraces + Couter", "35 sp"),               # Combined forearm and elbow defense.
    ("Tassets", "25 sp"),                          # Hanging plate skirts protecting the upper thighs and groin area.
    ("Sallet ou Armet (classique)", "55 sp"),      # Classic 15th c. gothic sallet or armet helmet.

    # === DÉCOMPOSITION ARMURE XVIᵉ SIÈCLE (modulaire) ===
    # Source : document historique détaillé (27 mai 2026)
    ("Maille collerette ou manches", "32 sp"),     # Mail collar or sleeves as secondary defense.
    ("Breastplate + Backplate (renforcé)", "95 sp"),  # Heavier 16th c. breastplate + backplate, thicker to resist early firearms.
    ("Gorget (renforcé)", "27 sp"),                # 16th c.: Higher and more rigid gorget than previous versions.
    ("Pauldrons + Gardes", "38 sp"),               # Larger pauldron with additional shoulder guards.
    ("Vambraces + Couter + Rerebrace", "42 sp"),   # Full arm harness (upper + lower arm + elbow).
    ("Gauntlets (renforcés)", "28 sp"),            # Heavier, more robust gauntlets, sometimes optimized for jousting or battlefield use.
    ("Tassets longs", "32 sp"),                    # Longer tassets for better upper leg protection.
    ("Cuisses (renforcées)", "34 sp"),             # More protective and integrated thigh defenses.
    ("Poleyns + Genouillères", "23 sp"),           # Knee protection, sometimes with additional knee cops.
    ("Greaves (renforcées)", "28 sp"),             # Stronger and more resistant shin defenses.
    ("Sabatons (larges)", "23 sp"),                # Wider, more functional sabatons for better stability.
    ("Close Helmet (Maximilian)", "65 sp"),        # Fully enclosed helmet with movable visor, typical of the 16th century.
    ("Burgonet (Maximilian)", "55 sp"),            # Open-faced helmet with a peak and cheek pieces, popular in the 16th century.

    # === MAILLES ANCIENNES (Ve-XIIIᵉ) ===
    ("Chain hauberk", "220 sp"),           # Standard riveted mail shirt, mid-length.
    ("Hauberk de maille", "230 sp"),       # Full-length mail shirt (often longer than hauberk).
    ("Byrnie carolingienne", "210 sp"),    # Early medieval shorter mail shirt (Carolingian period).
    ("Hauberk long", "190 sp"),            # Very long mail coat reaching the knees or below.
    ("Lorica squamata", "160 sp"),         # Scale armor (bronze or iron scales sewn on a backing). Common in Antiquity and early Middle Ages.

    # === PROTECTION DE BASE ===

    # === CASQUES HISTORIQUES — LISTE COMPLÈTE (document 27 mai 2026) ===
    # Descriptions pour bien distinguer les différents styles et périodes.
    # Antiquité (Grèce / Rome / Celtes)
    ("Corinthian Helmet", "65 sp"),            # Iconic Greek helmet (5th–4th c. BC). Fully enclosed with narrow eye slits and a distinctive T-shaped face opening. Excellent protection but limited vision and hearing.
    ("Attic Helmet", "52 sp"),                 # Greek helmet with a more open face and raised cheek guards. Better vision and ventilation than the Corinthian.
    ("Phrygian / Thracian Helmet", "45 sp"),   # Distinctive forward-curving crest. Associated with Thracian and Phrygian warriors. Good mobility.
    ("Boeotian Helmet", "42 sp"),              # Open-faced Greek helmet with a wide brim, inspired by Boeotian hats. Excellent all-around vision.
    ("Montefortino Helmet", "57 sp"),          # Common Roman helmet (3rd c. BC – 1st c. AD). Simple bowl shape with a neck guard and knob on top.
    ("Coolus Helmet", "50 sp"),                # Roman helmet (1st c. BC – 1st c. AD). Similar to Montefortino but with a wider neck guard.
    ("Imperial Gallic Helmet", "62 sp"),       # Classic Roman helmet of the 1st–2nd century AD. Features prominent brow guards and cheek pieces.
    ("Intercisa Helmet", "32 sp"),             # Late Roman helmet (4th–5th c.). Simpler, cheaper construction with a two-piece bowl and minimal neck protection.
    ("Celtic Helmet", "45 sp"),                # General term for various Celtic designs, often with elaborate crests or horns. Good protection with regional variations.

    # Haut Moyen Âge
    ("Spangenhelm (Ve-VIe)", "42 sp"),         # Early medieval segmented helmet made of iron plates riveted to a framework. Common among Germanic and Frankish warriors.
    ("Nasal helmet (VIIe)", "52 sp"),          # Helmet with a single nasal bar for nose protection. Typical of the Viking and Carolingian eras.
    ("Spangenhelm (VIIIe-IXe)", "42 sp"),      # Later evolution of the spangenhelm, often with a more rounded shape.
    ("Nasal helmet (XIe)", "45 sp"),           # Classic Norman-style nasal helmet seen at Hastings. Simple but effective.

    # Moyen Âge central et tardif
    ("Great Helm", "65 sp"),                   # Fully enclosed "bucket" helmet of the 12th–14th centuries. Excellent protection but very poor ventilation and vision. Worn over a mail coif or cerveliere.
    ("Cerveliere", "32 sp"),                   # Simple steel skullcap worn under the great helm or alone. Lightweight head protection.
    ("Bascinet (early)", "50 sp"),             # Early bascinet (mid-14th c.): pointed or rounded skull with a movable visor. Much better than the great helm for mobility.
    ("Bascinet", "55 sp"),                     # Classic 14th–15th c. bascinet with a pointed "pig-faced" or rounded visor. One of the most common helmets of the Hundred Years' War.
    ("Sallet", "52 sp"),                       # Iconic 15th c. helmet with a distinctive "tail" at the back. Excellent protection and good vision when the visor is raised.
    ("Armet", "65 sp"),                        # Sophisticated 15th–16th c. helmet that fully encloses the head. Features hinged cheek pieces that lock together. Very high protection.

    # Renaissance (XVIe)
    ("Sallet ou Armet (amélioré)", "58 sp"),   # Improved transitional sallet or armet with better ventilation and locking systems.
    ("Close Helmet (Maximilian)", "70 sp"),    # Fully enclosed helmet with a pivoting visor. The standard for high-quality 16th century harnesses.
    ("Burgonet (Maximilian)", "55 sp"),        # Open-faced helmet with a peak and cheek pieces. Popular with light cavalry and officers. Good visibility.
    ("Morion", "45 sp"),                       # Distinctive 16th c. open helmet with a high comb and brim. Iconic of Spanish and German pikemen and arquebusiers.
    ("Lobster-tailed Pot", "50 sp"),           # 17th c. cavalry helmet with a sliding nasal bar and articulated neck defense (looks like a lobster tail).

    # === BOUCLIERS HISTORIQUES ===
    # Descriptions pour bien distinguer les différents types et usages.

    # Antiquité
    ("Aspis (Hoplon)", "55 sp"),           # Large round Greek hoplite shield (5th–4th c. BC). Made of wood and bronze. Used in tight phalanx formations. Very heavy but excellent coverage.
    ("Scutum", "60 sp"),                   # Large rectangular Roman legionary shield. Curved to wrap around the body. Extremely effective in formation fighting.
    ("Clipeus", "40 sp"),                  # Smaller round Roman shield, often used by officers and cavalry. More maneuverable than the scutum.
    ("Parma", "28 sp"),                    # Light round Roman shield used by light troops and auxiliaries.

    # Bouclier rond classique — disponible dès l'Âge du Bronze (simplifié en une seule version)
    ("Round Shield", "30 sp"),             # Classic round shield used across many cultures from Bronze Age to early Middle Ages. Versatile and relatively light.

    # Moyen Âge central et tardif
    ("Kite Shield", "45 sp"),              # Long, almond-shaped shield (11th–12th c.). Designed to protect the body while on horseback or in shield wall. Gradually shortened over time.
    ("Heater Shield", "30 sp"),            # Classic triangular shield of the 13th–15th centuries. Smaller and lighter than the kite shield. The shape most associated with medieval knights and heraldry.

    # Renaissance et duel
    ("Buckler", "22 sp"),                  # Small round shield used for fencing and dueling (especially with sword or rapier). Highly maneuverable, used for parrying rather than blocking heavy blows.
    ("Pavise", "60 sp"),                   # Large rectangular shield used mainly by archers and crossbowmen. Often propped up on the ground as mobile cover.
    ("Targe", "32 sp"),                    # Scottish oval or round shield, often used with a dirk or broadsword. Frequently had a central spike.
    ("Rotella", "40 sp"),                  # Italian round shield of the 16th century, commonly paired with the rapier. Larger than a buckler, used for both defense and binding the opponent's blade.

    # Parade / luxe
    ("Parade Shield", "115 sp"),           # Highly decorated and ornate shield meant for display, tournaments, or ceremonial use rather than serious combat.
]

# =============================================================================
# CLASSIFICATION DES BOUCLIERS (pour la logique comportementale)
# =============================================================================
# Règle utilisateur :
# - Urbain OU armure très performante → souvent petits boucliers (Buckler, Rotella, Targe...)
# - Rural → grands boucliers (ronds de préférence)
# - Sans armure très coûteuse → souvent de grands boucliers ronds

SMALL_SHIELDS = {
    "Buckler",
    "Rotella",
    "Targe",
    "Parma",
    "Clipeus",
}

LARGE_ROUND_SHIELDS = {
    "Aspis (Hoplon)",
    "Scutum",
    "Round Shield",
}

LARGE_SHIELDS = {
    "Aspis (Hoplon)",
    "Scutum",
    "Round Shield",
    "Kite Shield",
    "Heater Shield",
    "Pavise",
}

ALL_SHIELDS = SMALL_SHIELDS | LARGE_SHIELDS

# =============================================================================
# ARMES D'HAST (POLE WEAPONS) — Règle de port sans monture
# =============================================================================
# Un personnage à pied ne peut raisonnablement transporter plus d'une arme d'hast longue.
# Les javelins restent autorisés en plusieurs exemplaires (légers, jetables, historiquement courants).
POLE_WEAPONS = {
    "Pike",
    "Halberd",
    "Poleaxe",
    "Bill",
    "Glaive, Polearm",
    "Voulge",
    "Bec de Corbin",
    "Lucerne Hammer",
    "Military Fork",
    "Ranseur",
    "Partisan",
    "Dory (Spear)",
    "Lance",
    "Boar Spear",
}

# Arcs (pour forcer l'achat d'un carquois)
BOWS = {
    "Short bow",
    "Longbow (early)",
    "Longbow",
    "Bow, Composite",
    "Composite Bow",
    "Light Crossbow",   # On considère les arbalètes légères comme nécessitant aussi un "carquois" (étui)
    "Crossbow",
    "Heavy Crossbow",
    "Composite Crossbow",
    "Cranequin Crossbow",
}

def is_pole_weapon(item_name: str) -> bool:
    """Retourne True si l'item est une arme d'hast longue et encombrante."""
    return item_name in POLE_WEAPONS


def is_bow(item_name: str) -> bool:
    """Retourne True si l'item est un arc ou une arbalète."""
    return item_name in BOWS or "bow" in item_name.lower() or "crossbow" in item_name.lower()


# =============================================================================
# ENCOMBREMENT DES ARMES (Weapon Encumbrance)
# =============================================================================
# Échelle : 1 (très léger) à 6 (extrêmement encombrant)
#
# RÈGLES SPÉCIALES (actuelles) :
# - Capacité de base "prêt à l'emploi" sans monture : **7 points fixes**.
# - Sac à dos et Force **ne donnent aucun bonus** à cette capacité.
# - Les armes d'encombrement 4 et plus :
#     • Ne peuvent être portées qu'à la main.
#     • Maximum 1 de ces armes.
#     • NE COMPTENT PAS dans les 7 points d'encombrement autorisés.
# - Les javelots peuvent être portés par faisceaux (règle à part).
# =============================================================================

WEAPON_ENCUMBRANCE: Dict[str, int] = {
    # === 1 - Très léger (ceinture / facile à porter en grand nombre) ===
    "Dagger, Bronze": 1,
    "Main-gauche": 1,
    "Rondel Dagger": 1,
    "Throwing Knife": 1,
    "Plumbata": 1,
    "Sling": 1,

    # === 2 - Léger ===
    "Javelin, Stone-Tipped": 2,
    "Javelin, Copper-Tipped": 2,
    "Javelin, Bronze Leaf-Shaped": 2,
    "Javelin, Bronze Socketed": 2,
    "Javelin, Iron Leaf-Shaped": 2,
    "Javelin, Iron Bodkin": 2,
    "Javelin, Renaissance": 2,
    "Javelin": 2,                           # Version générique
    "Francisca": 2,
    "War Dart, Medieval": 2,
    "Hand Axe, Stone": 2,
    "War Pick": 2,
    "Atlatl": 2,
    "Seax": 2,

    # === 3 - Moyen (la majorité des armes une main + arcs moyens) ===
    "Gladius": 3,
    "Spatha": 3,
    "Xiphos": 3,
    "Akinakes": 3,
    "Celtic Sword": 3,
    "Arming Sword": 3,
    "Sabre": 3,
    "Shamshir": 3,
    "Sidesword": 3,
    "Rapier": 3,
    "Cutlass": 3,
    "Estoc": 3,
    "Broadsword": 3,
    "Axe, Bronze": 3,
    "Battle Axe": 3,
    "Bearded Axe": 3,
    "Dane Axe": 3,
    "Mace": 3,
    "Mace, Stone": 3,
    "Flanged Mace": 3,
    "War Hammer": 3,
    "War Hammer (Renaissance)": 3,
    "Flail": 3,
    "Morning Star": 3,
    "Boar Spear": 3,
    "Dory (Spear)": 3,
    "Lance": 3,
    "Quarterstaff": 3,

    # Arcs et arbalètes légères/moyennes
    "Bow, Composite": 3,
    "Composite Bow": 3,
    "Quiver": 1,                           # Léger, se porte à la ceinture ou dans le dos
    "Longbow (early)": 3,
    "Longbow": 3,
    "Light Crossbow": 3,
    "Crossbow": 3,

    # === 4 et + : Encombrement spécial (ne comptent PAS dans les 7 points) ===
    # Règle : Max 1 à la main, ne consomme pas la capacité de 7 points
    "Longsword": 4,
    "2 Handed Sword": 4,
    "Great Axe": 4,
    "Lochaber Axe": 4,
    "Glaive, Polearm": 4,
    "Poleaxe": 4,
    "Halberd": 4,
    "Bill": 4,
    "Voulge": 4,
    "Bec de Corbin": 4,
    "Lucerne Hammer": 4,
    "Military Fork": 4,
    "Ranseur": 4,
    "Partisan": 4,
    "Heavy Crossbow": 4,
    "Composite Crossbow": 4,
    "Cranequin Crossbow": 4,
    "Blunderbuss": 4,
    "Pike": 5,                              # Très longue, particulièrement encombrante
    "Maul": 4,
    "Handgonne": 4,
    "Arquebus": 4,
    "Musket": 4,
    "Wheellock Pistol": 2,                  # Arme de poing → léger
    "Flintlock Pistol": 2,                  # Arme de poing → léger
}


def get_weapon_encumbrance(item_name: str) -> int:
    """Retourne le niveau d'encombrement d'une arme (1-5). Défaut = 3."""
    return WEAPON_ENCUMBRANCE.get(item_name, 3)


def is_high_encumbrance_weapon(item_name: str) -> bool:
    """Retourne True si l'arme a un encombrement ≥ 4 (règle spéciale)."""
    return get_weapon_encumbrance(item_name) >= 4


def calculate_total_encumbrance(items: list) -> int:
    """Calcule l'encombrement total d'une liste d'items (seulement les armes 1-3)."""
    total = 0
    for item in items:
        name = item["name"] if isinstance(item, dict) else str(item)
        enc = get_weapon_encumbrance(name)
        if enc < 4:  # Les armes ≥4 ne comptent pas dans le pool normal
            total += enc
    return total



def is_shield(item_name: str) -> bool:
    """Vérifie si un item est un bouclier historique."""
    return item_name in ALL_SHIELDS

def get_high_performance_armor_keywords() -> list:
    """Mots-clés pour détecter une armure 'très performante' (XIVe+ ou équivalent de qualité)."""
    return [
        "brigandine", "breastplate", "coat of plates", "hauberk", "haubergeon",
        "plate", "great helm", "bascinet", "sallet", "armet", "close helmet", "burgonet",
        "corinthian", "imperial gallic", "montefortino",
        "vambraces", "gauntlets", "pauldrons", "cuisses", "greaves", "sabatons",
        "bevor", "garde-reins", "fauld", "lance rest"
    ]

def has_high_performance_armor(purchases: list) -> bool:
    """Retourne True si le personnage a déjà acheté une armure de haute performance."""
    keywords = get_high_performance_armor_keywords()
    for p in purchases:
        name = (p.get("name") if isinstance(p, dict) else str(p)).lower()
        if any(kw in name for kw in keywords):
            return True
    return False

def get_shield_preference(settlement_type: str, purchases: list) -> str:
    """
    Détermine la préférence de bouclier selon les règles :
    - Un personnage urbain ou avec une armure très performante prend souvent des petits boucliers.
    - Les personnages ruraux ont de grands boucliers.
    - Sans armure très coûteuse, les personnages prennent souvent de grands boucliers ronds.

    Retourne : "small", "large_round", "large", ou "neutral"
    """
    settlement = (settlement_type or "").lower()

    # Détection urbain / rural (basée sur les vrais types de settlement_data.py)
    urban_keywords = [
        "metropolis", "major port", "major trade", "fortified city", "large town"
    ]
    rural_keywords = [
        "hamlet", "rural village", "fishing village", "forest village",
        "mountain village", "farming hamlet", "isolated hamlet", "isolated farmstead",
        "logging camp", "nomad camp", "frontier colony", "permanent encampment"
    ]

    is_urban = any(kw in settlement for kw in urban_keywords)
    is_rural = any(kw in settlement for kw in rural_keywords)

    has_good_armor = has_high_performance_armor(purchases)

    # Priorité haute : armure très performante → petit bouclier (même en rural)
    if has_good_armor:
        return "small"

    # Urbain sans armure lourde → petit bouclier souvent
    if is_urban:
        return "small"

    # Rural (ou neutre) sans armure lourde → grand bouclier rond de préférence
    if is_rural:
        return "large_round"

    # Cas neutre (ex: Small Town, Military Outpost, etc.) → léger biais rond si pas d'armure chère
    if not has_good_armor:
        return "large_round"

    return "neutral"


def get_preferred_shield_pool(preference: str) -> set:
    """Retourne l'ensemble de boucliers favorisés pour une préférence donnée."""
    if preference == "small":
        return SMALL_SHIELDS
    elif preference == "large_round":
        return LARGE_ROUND_SHIELDS
    elif preference == "large":
        return LARGE_SHIELDS
    else:
        # Neutre : on favorise légèrement les grands ronds (comportement par défaut historique)
        return LARGE_ROUND_SHIELDS | LARGE_SHIELDS


def choose_biased_shield(candidates: List[Tuple[str, str]], preference: str) -> Tuple[str, str]:
    """
    Choisit un bouclier parmi les candidats en appliquant le biais comportemental.
    Si des boucliers du type préféré sont disponibles, ils sont fortement favorisés.
    """
    if not candidates:
        return None, None

    pref_pool = get_preferred_shield_pool(preference)

    # Séparer les candidats shields selon préférence
    preferred = [c for c in candidates if c[0] in pref_pool]
    other_shields = [c for c in candidates if c[0] in ALL_SHIELDS and c not in preferred]

    # Si on a des preferred, très forte chance de les prendre (sauf si tech les bloque)
    if preferred:
        # 80% de chance de prendre dans le pool préféré, 20% autre (variété)
        if random.random() < 0.80:
            return random.choice(preferred)
        else:
            pool = preferred + other_shields if other_shields else preferred
            return random.choice(pool)

    # Pas de preferred dispo (tech ou région) → fallback sur n'importe quel bouclier dispo
    all_shield_candidates = [c for c in candidates if c[0] in ALL_SHIELDS]
    if all_shield_candidates:
        return random.choice(all_shield_candidates)

    # Ne devrait pas arriver
    return random.choice(candidates)


def has_mount(purchases: list) -> bool:
    """Retourne True si le personnage possède au moins un animal de monte ou de bât."""
    mount_keywords = ["rouncey", "courser", "palfrey", "destrier", "mule", "pony", "camel"]
    for p in purchases:
        if any(kw in p["name"].lower() for kw in mount_keywords):
            return True
    return False


def has_pack_capacity(purchases: list) -> bool:
    """
    Retourne True si le personnage peut transporter du matériel lourd.
    Actuellement : avoir une monture (mule, poney, cheval, chameau...) est suffisant.
    Dog sled compte aussi comme capacité autonome.
    """
    if has_mount(purchases):
        return True
    for p in purchases:
        if "dog sled" in p["name"].lower():
            return True
    return False


def enforce_no_mount_carry_limits(purchases: list) -> tuple:
    """
    Système d'encombrement des armes.

    Règles (sans monture) :
    - Capacité de base : **7 points** d'encombrement fixes.
    - Sac à dos et Force **ne donnent aucun bonus** à cette capacité (règle actuelle).
    - Les armes d'encombrement ≥ 4 :
        • Ne peuvent être portées qu'à la main.
        • Maximum 1 de ces armes.
        • NE COMPTENT PAS dans les 7 points d'encombrement.
    - Les javelots (toutes versions) restent autorisés en grand nombre.

    Retourne : (purchases_filtrées, montant_remboursé_bp)
    """
    if has_mount(purchases):
        return purchases, 0

    base_capacity = 7   # Capacité fixe sans monture (pas de bonus sac/force)

    filtered = []
    current_encumbrance = 0
    high_encumbrance_count = 0
    shields_found = 0
    refunded = 0

    for p in purchases:
        name = p["name"]
        cost = p.get("price_bp", 0)
        enc = get_weapon_encumbrance(name)

        # Règle spéciale : armes très encombrantes (≥4)
        if is_high_encumbrance_weapon(name):
            if high_encumbrance_count < 1:
                filtered.append(p)
                high_encumbrance_count += 1
            else:
                refunded += cost
            continue

        # Boucliers (règle conservée pour l'instant)
        if is_shield(name):
            if shields_found < 1:
                filtered.append(p)
                shields_found += 1
            else:
                refunded += cost
            continue

        # Armes normales (encombrement 1-3)
        if current_encumbrance + enc <= base_capacity:
            filtered.append(p)
            current_encumbrance += enc
        else:
            refunded += cost

    return filtered, round(refunded, 1)


def is_weapon_or_armor(item_name: str) -> bool:
    """Retourne True si l'item est clairement une arme ou une pièce d'armure."""
    name = item_name.lower()

    # Explicitement pas des armes/armures
    non_combat = [
        "tent", "lantern", "camp bed", "backpack", "bedroll", "blanket",
        "canteen", "waterskin", "flint", "tinder", "tinderbox", "rations",
        "hardtack", "waybread", "pork", "beef", "fish", "food",
        "cloak", "coat", "pants", "hat", "boots", "gloves", "jerkin",
        "rope", "hammer", "saddle", "packsaddle", "saddle bags",
        "draft harness", "camel", "pony", "rouncey", "courser", "palfrey",
        "sleeping furs", "sleeping fur"
    ]
    if any(kw in name for kw in non_combat):
        return False

    if is_shield(item_name):
        return True

    prio = get_armor_purchase_priority(item_name)
    if prio is not None and prio >= 0:
        return True

    # Armes (élargi)
    weapon_keywords = [
        "sword", "axe", "hammer", "mace", "flail", "spear", "lance", "pike", "halberd", "poleaxe", "bill",
        "bow", "crossbow", "arquebus", "musket", "handgonne", "javelin", "sling",
        "dagger", "knife", "seax", "gladius", "rapier", "longsword", "arming sword",
        "falchion", "sidesword", "estoc", "cutlass", "broadsword", "large sword", "2 handed sword",
        "quarterstaff", "staff", "club", "pick axe", "fire-starting bow",
        "short bow", "short sword", "target shield", "leather jerkin",
        "quiver"
    ]
    return any(kw in name for kw in weapon_keywords)


# =============================================================================
# NOUVELLE RÈGLE : PRIORITÉ D'ACHAT DANS LA CATÉGORIE ARMOR
# =============================================================================
# Règle utilisateur :
# Quand un personnage achète des pièces d'armure, la priorité est souvent :
# 1. Bouclier
# 2. Casque
# 3. Protection du torse
# 4. Le reste (bras, jambes, etc.)

def get_armor_purchase_priority(item_name: str) -> int:
    """
    Retourne le niveau de priorité d'achat pour une pièce d'armure.
    Plus le nombre est élevé, plus la pièce est prioritaire.
    """
    name = item_name.lower()

    # 3 = Bouclier (priorité la plus haute)
    if is_shield(item_name):
        return 3

    # 2 = Casque
    helmet_keywords = [
        "helmet", "helm", "bascinet", "sallet", "armet", "spangenhelm", "nasal",
        "burgonet", "close helmet", "salet", "great helm", "cerveliere", "morion",
        "kettle hat", "lobster", "corinthian", "attic", "phrygian", "boeotian",
        "montefortino", "coolus", "imperial gallic", "intercisa", "celtic"
    ]
    if any(kw in name for kw in helmet_keywords):
        return 2

    # 1 = Protection du torse (hauberk, breastplate, brigandine, gambeson, plackart...)
    torso_keywords = [
        "breastplate", "hauberk", "brigandine", "gambeson", "plackart",
        "coat of plates", "jack of plates", "lorica", "byrnie",
        "chain hauberk", "haubergeon", "arming doublet", "simple breastplate",
        "maille collerette", "hauberk de maille"
    ]
    if any(kw in name for kw in torso_keywords):
        return 1

    # 0 = Membres (bras/jambes) → toujours considéré comme armure
    # -1 = Pas une armure ni une arme (tente, selle, lanterne, sac, couverture, etc.)
    non_armor_keywords = [
        "tent", "lantern", "camp bed", "backpack", "bedroll", "blanket", 
        "canteen", "waterskin", "flint", "tinder", "rations", "food", 
        "saddle", "packsaddle", "saddle bags", "draft harness", "harness"
    ]
    if any(kw in name for kw in non_armor_keywords):
        return -1

    return 0  # Membres et autres pièces d'armure


WEAPON_UPGRADES: List[Tuple[str, str]] = [
    # === ARMES PRIMITIVES (Stone Age) ===
    ("Javelin, Stone-Tipped", "4 sp"),
    ("Club, Great", "5 sp"),               # Grosse massue en bois dur. Arme primitive très répandue.
    ("Hand Axe, Stone", "6 sp"),           # Hache de main en pierre taillée.
    ("Atlatl", "9 sp"),                    # Propulseur de javelots (augmente considérablement la puissance).

    # === ARMES CUIVRE (Copper Age) ===
    ("Javelin, Copper-Tipped", "7 sp"),
    ("Mace, Stone", "10 sp"),              # Masse à tête de pierre.

    # === ARMES BRONZE (Bronze Age) ===
    ("Javelin, Bronze Leaf-Shaped", "12 sp"),
    ("Javelin, Bronze Socketed", "15 sp"),
    ("Dagger, Bronze", "12 sp"),           # Poignard en bronze, arme courante de l'âge du bronze.
    ("Axe, Bronze", "20 sp"),              # Hache de combat en bronze.
    ("Sword, Bronze", "38 sp"),            # Épée courte en bronze (rare et précieuse).

    # === ARMES ANTIQUES (Iron Age) ===
    ("Gladius", "50 sp"),
    ("Pilum, Roman", "35 sp"),             # Le pilum romain légendaire (tige en fer qui se tord).
    ("Verutum, Roman Light", "11 sp"),     # Javelot léger romain (utilisé par les vélites).
    ("Javelin, Iron Leaf-Shaped", "14 sp"),     # Version la plus répandue chez Celtes, Grecs, Germains.
    ("Javelin, Iron Bodkin", "18 sp"),          # Pointe pyramidale très pénétrante (anti-armure légère).
    ("Spatha", "55 sp"),
    ("Xiphos", "45 sp"),
    ("Dory (Spear)", "32 sp"),
    ("War Pick", "26 sp"),                 # Pic de guerre / maillet perforant. Excellent contre les armures.
    ("Bow, Composite", "28 sp"),           # Arc composite ancien (dès ~2000 av. J.-C.). Puissant mais fabrication très longue et coûteuse. Réservé aux guerriers d'élite et nobles.
    ("Composite Bow", "52 sp"),
    ("Quiver", "10 sp"),                   # Contenant standard pour transporter des flèches. Obligatoire avec tout arc.
    ("Celtic Sword", "52 sp"),
    ("Akinakes", "32 sp"),
    ("Javelin", "18 sp"),                  # Version générique (rétrocompatibilité)
    ("Francisca", "24 sp"),                # Hache de jet franque. Icône des peuples germaniques.
    ("Throwing Knife", "14 sp"),           # Couteau de jet équilibré.
    ("Plumbata", "16 sp"),                 # Dard plombé romain (lourd et très efficace).
    ("Sling", "12 sp"),

    # === ARMES HAUT MOYEN ÂGE (Middle Ages) ===
    ("Large Sword", "55 sp"),              # Broad 'spatula' blade sword of the Viking Age and early Middle Ages. Flat, wide cutting blade (less tapered than later knightly swords). Often used one-handed from horseback or with a shield. The classic 'Viking sword' profile.
    ("Dane Axe", "45 sp"),
    ("Arming Sword", "45 sp"),             # One-handed knightly sword (épée à une main de chevalier). The standard sidearm of the armored warrior throughout the Middle Ages; balanced for cutting and thrusting, almost always paired with a shield in battle.
    ("Mace", "38 sp"),
    ("War Hammer", "40 sp"),
    ("Longbow (early)", "28 sp"),
    ("War Dart, Medieval", "16 sp"),
    ("Sabre", "42 sp"),                    # Sabre droit ou légèrement courbé. Arme de cavalerie et d'infanterie légère.
    ("Rondel Dagger", "28 sp"),            # Dague à section triangulaire. Excellente pour percer les armures et les mailles.
    ("Seax", "30 sp"),
    ("Lance", "32 sp"),
    ("Battle Axe", "35 sp"),
    ("Bearded Axe", "40 sp"),
    ("Flail", "42 sp"),
    ("Quarterstaff", "8 sp"),

    # === ARMES FIN DU MOYEN ÂGE (Late Middle Ages) ===
    ("Longsword", "65 sp"),                # Two-handed knightly sword (épée à deux mains de chevalier). Longer blade of the 14th-15th centuries, optimized for powerful cuts, thrusts, and half-sword techniques against armored opponents. Can be used with one or two hands depending on technique and armor.
    ("Falchion", "45 sp"),                 # One-handed anti-peasant / infantry sword (épée à une main anti-paysans). Heavy, broad, single-edged blade specialized in brutal chopping cuts. Far more effective against unarmored or lightly protected foes (peasants, archers, militia) than against plate. Common among common soldiers.
    ("Poleaxe", "70 sp"),
    ("Halberd", "65 sp"),
    ("Crossbow", "85 sp"),
    ("Longbow", "30 sp"),
    ("Bill", "57 sp"),
    ("Handgonne", "160 sp"),
    ("Flanged Mace", "55 sp"),
    ("Morning Star", "50 sp"),
    ("Boar Spear", "35 sp"),
    ("Glaive, Polearm", "55 sp"),          # Glaive sur hampe (polearm), à ne pas confondre avec l'épée courte parfois appelée glaive.
    ("Voulge", "48 sp"),
    ("Heavy Crossbow", "95 sp"),
    ("Great Axe", "60 sp"),
    ("Lochaber Axe", "58 sp"),
    ("Bec de Corbin", "65 sp"),
    ("Maul", "45 sp"),
    ("Lucerne Hammer", "62 sp"),
    ("Military Fork", "48 sp"),
    ("Ranseur", "50 sp"),
    ("Light Crossbow", "55 sp"),
    ("Composite Crossbow", "75 sp"),

    # === ARMES RENAISSANCE (Early / Late Renaissance) ===
    ("Rapier", "80 sp"),
    ("Javelin, Renaissance", "22 sp"),
    ("Wheellock Pistol", "110 sp"),        # Pistolet à rouet. Arme de poing de luxe pour officiers et riches (fin XVIe).
    ("Blunderbuss", "75 sp"),              # Tromblon à canon évasé. Arme de poing ou d'épaule courte, très efficace à courte distance.
    ("Shamshir", "58 sp"),                 # Sabre courbe oriental très efficace (persan / ottoman).
    ("Sidesword", "65 sp"),
    ("Pike", "40 sp"),
    ("Arquebus", "130 sp"),
    ("Musket", "180 sp"),
    ("Main-gauche", "32 sp"),
    ("War Hammer (Renaissance)", "52 sp"),
    ("Partisan", "52 sp"),
    ("Cranequin Crossbow", "140 sp"),
    ("Broadsword", "55 sp"),
    ("Cutlass", "48 sp"),
    ("Estoc", "70 sp"),
    ("2 Handed Sword", "110 sp"),
    ("Flintlock Pistol", "85 sp"),         # Pistolet à silex. Arme de poing standard de l'Âge de la Raison.
]

MOBILITY: List[Tuple[str, str]] = [
    # === CHEVAUX HISTORIQUES (document 27 mai 2026) ===
    ("Rouncey", "45 sp"),                  # Cheval polyvalent le plus courant (guerre + voyage)
    ("Courser", "62 sp"),                  # Cheval rapide de chasse et de guerre
    ("Palfrey", "57 sp"),                  # Cheval de parade et de dame
    ("Destrier", "130 sp"),                # Cheval de guerre lourd de qualité
    ("Destrier (quality)", "200 sp"),      # Destrier exceptionnel (très rare)

    # Montures alternatives
    ("Mule", "40 sp"),
    ("Pony", "40 sp"),
    ("Camel, riding", "15 gp"),
    ("Dog sled", "7 gp"),
]

TRAVEL_GEAR: List[Tuple[str, str]] = [
    ("Tent, 2-man leather", "15 sp"),
    ("Tent, 4-man leather", "25 sp"),
    ("Camp bed, leather & wood", "35 sp"),
    ("Lantern, hooded (Iron Age)", "5 bp"),   # plusieurs lanternes
]

RIDING_GEAR: List[Tuple[str, str]] = [
    ("Riding saddle", "15 sp"),
    ("War saddle", "30 sp"),
    ("Packsaddle", "10 sp"),
    ("Saddle bags, large", "12 sp"),
    ("Draft harness", "75 sp"),
]

# Regroupement
ALL_UPGRADE_ITEMS: Dict[str, List[Tuple[str, str]]] = {
    "Armor": ARMOR_UPGRADES,
    "Weapons": WEAPON_UPGRADES,
    "Mobility": MOBILITY,
    "TravelGear": TRAVEL_GEAR,
    "RidingGear": RIDING_GEAR,
}

# =============================================================================
# PACKAGES D'ACHATS PAR TIER + RÉGION (à enrichir progressivement)
# =============================================================================
# Format : liste de tuples (nom_item, prix_str) exactement comme dans les listes
# On peut avoir plusieurs packages par tier ; on en choisit un (ou plusieurs petits) selon le capital.

# Les anciens packages ont été retirés au profit du système multi-catégories ci-dessus.
# On garde uniquement les listes d'items par catégorie pour plus de flexibilité.

# =============================================================================
# NIVEAU TECHNOLOGIQUE ET DISPONIBILITÉ
# =============================================================================

TECH_LEVEL_ORDER = [
    "Stone Age",           # 0
    "Copper Age",          # 1
    "Bronze Age",          # 2
    "Iron Age",            # 3
    "Middle Ages",         # 4
    "Late Middle Ages",    # 5
    "Early Renaissance",   # 6
    "Late Renaissance",    # 7
    "Age of Reason"        # 8
]

# Conversion temporaire ancien nom → nouvel index (0-8)
# À supprimer une fois la migration terminée
OLD_TECH_TO_INDEX = {
    "Stone Age": 0,
    "Copper Age": 1,
    "Bronze Age": 2,
    "Iron Age": 3,
    "Middle Ages": 4,
    "Late Middle Ages": 5,
    "Early Renaissance": 6,
    "Late Renaissance": 7,
    "Renaissance": 7,           # On mappe "Renaissance" sur Late Renaissance
    "Age of Reason": 8,
    # Anciens noms avec siècles (legacy)
    "Roman Empire": 3,
    "Late Roman / Early Medieval": 3,
    "High Middle Ages": 4,
    "Early Middle Ages": 4,
}

def get_tech_level(region: str) -> int:
    """Retourne le niveau technologique d'une région (0 à 8)."""
    return REGION_TECH_LEVEL.get(region, REGION_TECH_LEVEL["Default"])

def tech_level_index(tech) -> int:
    """Retourne l'index du niveau technologique (0-8).
    Accepte int ou ancien nom string (via OLD_TECH_TO_INDEX).
    """
    if isinstance(tech, int):
        return max(0, min(8, tech))

    # Conversion depuis ancien nom
    if tech in OLD_TECH_TO_INDEX:
        return OLD_TECH_TO_INDEX[tech]

    # Fallback sur l'ancien système de liste
    try:
        return TECH_LEVEL_ORDER.index(tech)
    except ValueError:
        return 4  # Middle Ages par défaut

# Items qui ont une exigence technologique minimale
# Format : nom de l'item -> tech level minimum requis
ITEM_MIN_TECH: Dict[str, int] = {
    # Note : Full plate et Half plate ont été retirés des items individuels.
    # Ils seront désormais construits comme des kits à partir des pièces modulaires.
    # Brigandine reste disponible comme pièce unique.

    "Plate mail barding": 7,   # Late Renaissance

    # === Armures textiles & matelassées ===
    "Subarmalis": 3,               # Iron Age (équivalent)
    "Thoracomachus": 3,
    "Aketon": 4,
    "Gambeson": 4,
    "Reinforced Gambeson": 5,
    "Padded Jack": 5,
    "Jack of Plates": 7,
    "Brigandine": 5,
    "Arming Doublet": 7,
    "Coat of plates": 5,

    # === Décomposition armure XIVᵉ (modulaire) ===
    "Hauberk": 5,
    "Coat of Plates": 5,
    "Brassards / Vambraces": 5,
    "Aventail": 5,

    # === Décomposition armure XVᵉ (modulaire) — Early Renaissance ===
    "Haubergeon / Collerette maille": 6,
    "Vambraces + Couter": 6,
    "Tassets": 6,
    "Sallet ou Armet (classique)": 6,
    "Sallet ou Armet (amélioré)": 6,

    # === Décomposition armure XVIᵉ (modulaire) — Late Renaissance ===
    "Maille collerette ou manches": 7,
    "Vambraces + Couter + Rerebrace": 7,
    "Tassets longs": 7,

    # === Protection de base ===
    "Salet": 4,
    "Sallet": 5,
    "Cerveliere": 5,

    # === Pièces courantes / infanterie (nouveau document 27 mai 2026) ===
    "Kettle hat": 5,
    "Mail coif": 5,
    "Simple Breastplate": 5,
    "Bronze cuirass": 2,       # Disponible très tôt, cher
    "Bronze greaves": 2,       # Disponible très tôt, cher
    "Fauld": 6,
    "Besagews (pair)": 6,

    # === Pièces spécifiques (SUITE - document 27 mai 2026) ===
    "Plackart": 6,
    "Couter (pair)": 6,
    "Mail voiders (pair)": 6,
    "Arming doublet": 6,
    "Greaves / Poleyns simples (pair)": 5,
    "Cuir bouilli (jambières)": 4,
    "Cuir bouilli (brassards)": 4,

    # Compléments de harnais (estimations)
    "Bevor": 6,
    "Garde-reins": 6,
    "Lance rest": 4,
    "Mail fauld": 4,

    # Protections de jambes rudimentaires (Moyen Âge et avant)
    "Chausses de maille": 4,
    "Knee cops (basic)": 4,
    "Leather greaves": 4,

    # === Maille (VIIIᵉ-XIIIᵉ) ===
    "Chain hauberk": 4,
    "Hauberk de maille": 3,
    "Byrnie carolingienne": 3,
    "Hauberk long": 4,

    # === Armures anciennes (Ve-VIIe) ===
    "Lorica squamata": 3,
    "Spangenhelm (Ve-VIe)": 3,         # 5th-6th century (Iron Age equivalent)
    "Nasal helmet (VIIe)": 3,          # 7th century
    "Spangenhelm (VIIIe-IXe)": 3,      # 8th-9th century
    "Nasal helmet (XIe)": 4,           # 11th century (Middle Ages)

    # === Casques historiques complets (nouveau document 27 mai 2026) ===
    # Antiquité (Grèce/Rome/Celtes)
    "Corinthian Helmet": 3,
    "Attic Helmet": 3,
    "Phrygian / Thracian Helmet": 3,
    "Boeotian Helmet": 3,
    "Montefortino Helmet": 3,
    "Coolus Helmet": 3,
    "Imperial Gallic Helmet": 3,
    "Intercisa Helmet": 3,
    "Celtic Helmet": 3,

    # Moyen Âge
    "Great Helm": 4,
    "Bascinet (early)": 5,
    "Bascinet": 5,
    "Armet": 6,

    # Renaissance
    "Sallet ou Armet (classique)": 6,
    "Sallet ou Armet (amélioré)": 6,
    "Morion": 7,
    "Lobster-tailed Pot": 7,

    # Armures intermédiaires
    "Breastplate, iron": 3,
    "Breastplate, bronze": 2,

    # === Armes de qualité ===
    # === Armes primitives (Stone Age / Copper Age) ===
    "Javelin, Stone-Tipped": 0,
    "Club, Great": 0,
    "Hand Axe, Stone": 0,
    "Atlatl": 0,
    "Javelin, Copper-Tipped": 1,
    "Mace, Stone": 1,

    # === Armes Bronze (Bronze Age) ===
    "Javelin, Bronze Leaf-Shaped": 2,
    "Javelin, Bronze Socketed": 2,
    "Dagger, Bronze": 2,
    "Axe, Bronze": 2,
    "Sword, Bronze": 2,

    # === Armes antiques (Iron Age) ===
    "Gladius": 3,
    "Pilum, Roman": 3,
    "Verutum, Roman Light": 3,
    "Javelin, Iron Leaf-Shaped": 3,
    "Javelin, Iron Bodkin": 3,
    "Spatha": 3,
    "Xiphos": 3,
    "Dory (Spear)": 3,
    "Bow, Composite": 2,        # Premier arc composite historique (~2000 av. J.-C.)
    "Composite Bow": 3,
    "Quiver": 2,
    "Celtic Sword": 3,
    "Akinakes": 3,
    "Javelin": 3,
    "Francisca": 3,
    "Throwing Knife": 3,
    "Plumbata": 3,
    "War Pick": 3,
    "Sling": 3,

    # === Armes Haut Moyen Âge (Middle Ages) ===
    "Large Sword": 4,
    "Dane Axe": 4,
    "Arming Sword": 4,
    "Mace": 4,
    "War Hammer": 4,
    "Longbow (early)": 4,
    "War Dart, Medieval": 4,
    "Sabre": 4,
    "Rondel Dagger": 5,
    "Seax": 4,
    "Lance": 4,
    "Battle Axe": 4,
    "Bearded Axe": 4,
    "Flail": 5,
    "Quarterstaff": 4,

    # === Armes Fin du Moyen Âge (Late Middle Ages) ===
    "Longsword": 5,
    "Falchion": 5,
    "Poleaxe": 5,
    "Halberd": 5,
    "Crossbow": 5,
    "Longbow": 5,
    "Bill": 5,
    "Handgonne": 5,
    "Flanged Mace": 5,
    "Morning Star": 5,
    "Boar Spear": 5,
    "Glaive, Polearm": 5,
    "Voulge": 5,
    "Heavy Crossbow": 5,

    # === Armes Renaissance ===
    "Rapier": 6,
    "Javelin, Renaissance": 7,
    "Wheellock Pistol": 7,
    "Blunderbuss": 7,
    "Shamshir": 7,
    "Sidesword": 6,
    "Pike": 6,
    "Arquebus": 7,
    "Musket": 7,
    "Main-gauche": 6,
    "War Hammer (Renaissance)": 7,
    "Partisan": 6,
    "Cranequin Crossbow": 7,
    "Great Axe": 5,
    "Lochaber Axe": 5,
    "Bec de Corbin": 6,
    "Maul": 5,
    "Lucerne Hammer": 5,
    "Military Fork": 5,
    "Ranseur": 5,
    "Light Crossbow": 5,
    "Composite Crossbow": 5,
    "Broadsword": 6,
    "Cutlass": 6,
    "Estoc": 6,
    "2 Handed Sword": 7,
    "Wheellock Pistol": 7,
    "Blunderbuss": 7,
    "Flintlock Pistol": 8,

    # === Montures et animaux (chevaux historiques) ===
    "Rouncey": 3,
    "Courser": 4,
    "Palfrey": 4,
    "Destrier": 4,
    "Destrier (quality)": 7,
    "Horse, heavy": 4,
    "Warhorse, lesser": 4,
    "Warhorse, greater": 7,
    "Camel, riding": 3,

    # === Sellerie et harnachement avancé ===
    "War saddle": 4,
    "Draft harness": 3,

    # === Boucliers historiques ===
    "Aspis (Hoplon)": 3,
    "Scutum": 3,
    "Clipeus": 3,
    "Parma": 3,
    "Round Shield": 2,
    "Kite Shield": 4,
    "Heater Shield": 4,
    "Buckler": 4,
    "Pavise": 4,
    "Targe": 4,
    "Rotella": 7,
    "Parade Shield": 7,
}

# Normalisation des niveaux technologiques
# On garde la possibilité de normaliser d'anciens noms, mais "Late Middle Ages" est maintenant un niveau réel.
TECH_NORMALIZATION = {}

def is_item_available(item_name: str, region_tech) -> bool:
    """
    Vérifie si un item est disponible dans une région selon son niveau technologique.
    region_tech peut être un int (0-8) ou un ancien nom string.
    """
    min_tech = ITEM_MIN_TECH.get(item_name)
    if not min_tech:
        return True  # Pas de restriction

    # Normalisation temporaire
    min_tech = TECH_NORMALIZATION.get(min_tech, min_tech)

    return tech_level_index(region_tech) >= tech_level_index(min_tech)


def get_available_items_for_region(items: List[Tuple[str, str]], region: str, rarity_chance: float = 0.08) -> List[Tuple[str, str]]:
    """
    Filtre les items selon le niveau technologique de la région.
    Avec une petite chance (rarity_chance) d'avoir des items d'un niveau supérieur
    (import, butin, commande spéciale, etc.).
    """
    region_tech = get_tech_level(region)
    available = []

    for item in items:
        item_name = item[0]
        if is_item_available(item_name, region_tech):
            available.append(item)
        else:
            # Petite chance d'avoir quand même l'item (très rare)
            if random.random() < rarity_chance:
                available.append(item)

    return available if available else items  # fallback si rien n'est dispo


# =============================================================================
# NOUVEAU SYSTÈME : FILTRAGE PAR GROUPE D'ÉQUIPEMENT (14 Groupes)
# =============================================================================

def get_equipment_group_for_region(region: str) -> str:
    """Retourne l'ID du groupe d'équipement correspondant à une région."""
    return equipment_groups.get_equipment_group(region)


def get_available_items_for_equipment_group(group_id: str) -> List[Tuple[str, float]]:
    """
    Retourne la liste des items disponibles pour un groupe donné,
    avec leur prix final (incluant le surcoût si l'item est Rare ou Très rare).

    Format de retour : List[ (name, final_price_sp) ]
    """
    pool = group_equipment_pools.get_group_pool(group_id)
    result = []

    for item in pool:
        name = item["name"]
        # On utilise la fonction qui applique déjà le surcoût
        enriched = group_equipment_pools.get_item_with_final_price(group_id, name)
        if enriched:
            final_price = enriched.get("final_price_sp", item["price_sp"])
            result.append((name, final_price))

    return result


def get_available_items_for_group_or_region(group_id: str, region: str) -> List[Tuple[str, float]]:
    """
    Version hybride (transition) :
    Essaie d'abord de retourner les items du groupe.
    Si le groupe n'a pas encore de données riches, fallback sur l'ancien système tech.
    """
    group_items = get_available_items_for_equipment_group(group_id)

    if len(group_items) > 20:   # Seuil arbitraire : si le groupe a une vraie liste
        return group_items

    # Fallback sur l'ancien système (tech par région)
    # On prend les listes globales et on filtre par tech
    all_items = []
    for cat_items in ALL_UPGRADE_ITEMS.values():
        all_items.extend(cat_items)

    tech_filtered = get_available_items_for_region(all_items, region, rarity_chance=0.05)

    # On convertit en (name, price) en utilisant les prix historiques
    result = []
    for name, price_str in tech_filtered:
        bp = price_fix.parse_price_to_bp(price_str) if hasattr(price_fix, 'parse_price_to_bp') else 0
        # Conversion bp → sp approximative
        price_sp = bp / 10.0
        result.append((name, round(price_sp, 2)))

    return result


def get_final_price_for_purchase(group_id: str, item_name: str, fallback_price_str: str) -> tuple[float, str]:
    """
    Retourne le prix final à utiliser pour un achat post-kit + la rareté.
    Priorité :
    1. Si l'item existe dans le pool du groupe → prix avec surcoût (Rare +50%, Très rare +100%)
    2. Sinon → prix historique normal (fallback)
    """
    enriched = group_equipment_pools.get_item_with_final_price(group_id, item_name)
    if enriched:
        return enriched["final_price_sp"], enriched.get("rarity", "Commun")

    # Fallback ancien système
    corrected = price_fix.get_historical_price(item_name, fallback_price_str)
    cost_bp = kits.parse_price_to_bp(corrected)
    return round(cost_bp / 10.0, 2), "Commun"


def has_primary_one_handed_weapon(purchases: list) -> bool:
    """Vérifie si le personnage a déjà une arme principale à une main."""
    for p in purchases:
        if p["name"] in PRIMARY_ONE_HANDED_WEAPONS:
            return True
    return False


def get_item_encumbrance(equipment_group: str, item_name: str) -> int:
    """
    Retourne le niveau d'encombrement d'un item.
    Priorité : valeur du pool du groupe (source .txt) > fallback local WEAPON_ENCUMBRANCE.
    """
    enc = group_equipment_pools.get_weapon_encumbrance(equipment_group, item_name)
    if enc is not None:
        return enc
    return get_weapon_encumbrance(item_name)  # fallback


def has_heavy_weapon(purchases: list, equipment_group: str = None) -> bool:
    """Retourne True si le personnage possède déjà au moins une arme lourde (encumbrance >= 4)."""
    for p in purchases:
        name = p["name"]
        if equipment_group:
            enc = get_item_encumbrance(equipment_group, name)
        else:
            enc = get_weapon_encumbrance(name)
        if enc >= 4:
            return True
    return False


# =============================================================================
# RESTRICTIONS MAGIQUES
# =============================================================================

def get_magic_restrictions(magic_type: str, magic_subtype: str) -> dict:
    """
    Retourne les restrictions d'équipement selon le type de magie.
    """
    restrictions = {
        "forbidden_categories": set(),
        "forbidden_keywords": set(),
        "max_armor_type": None   # "Gambeson" ou "Light" par exemple
    }

    magic_type = (magic_type or "None").lower()
    subtype = (magic_subtype or "").lower()

    # Magie Verte / Sauvage Verte → aucune armure métallique
    if "verte" in magic_type or "verte" in subtype:
        restrictions["forbidden_keywords"].update(["plate", "hauberk", "chain", "mail", "brigandine", "breastplate", "iron", "bronze", "steel"])
        restrictions["max_armor_type"] = "Gambeson"

    # Magie Arcanique → armure max = vêtements d'hiver (Gambeson)
    elif "arcanique" in magic_type or "magicien" in subtype:
        restrictions["forbidden_keywords"].update(["plate", "hauberk", "chain", "mail", "brigandine", "breastplate", "iron", "bronze", "steel"])
        restrictions["max_armor_type"] = "Gambeson"

    return restrictions


def filter_items_by_magic(items: List[Tuple[str, str]], magic_type: str, magic_subtype: str) -> List[Tuple[str, str]]:
    """Filtre les items selon les restrictions magiques."""
    restrictions = get_magic_restrictions(magic_type, magic_subtype)
    if not restrictions["forbidden_keywords"]:
        return items

    forbidden = restrictions["forbidden_keywords"]
    filtered = []

    for item in items:
        name_lower = item[0].lower()
        if any(kw in name_lower for kw in forbidden):
            continue
        filtered.append(item)

    return filtered if filtered else items  # fallback


# =============================================================================
# NOUVELLE LOGIQUE : SÉLECTION MULTI-CATÉGORIES
# =============================================================================
# Un personnage riche a de fortes chances d'acheter de l'armure et des armes,
# pas forcément (ou pas seulement) une monture.

def get_regional_category_weights(region: str) -> Dict[str, float]:
    """
    Poids de base par région.
    Certaines régions ont une forte préférence culturelle pour la mobilité (montures, traîneaux, chameaux)
    même quand le personnage est riche.
    """
    weights = {
        "Armor": 1.0,
        "Weapons": 0.9,
        "Mobility": 1.0,
        "TravelGear": 0.7,
        "RidingGear": 0.6,
    }

    is_arctic = any(x in region for x in ["Glacier", "Icewind", "Spine of the World", "Sossal", "Cold Lands", "Icerim"])
    is_desert = region in ["Anauroch", "Bedine", "Calimshan", "The Shaar", "Dambrath"]
    is_steppe = "Hordelands" in region or "The Ride" in region or "Endless Wastes" in region
    is_underdark = "Underdark" in region or "Drow" in region or "Gracklstugh" in region
    is_civilized_rich = region in ["Waterdeep", "Baldur's Gate", "Sembia", "Amn", "Halruaa", "Lantan", "Cormyr", "Tethyr", "Impiltur"]

    if is_arctic:
        weights["Mobility"] = 2.8      # Très fort (traîneaux, chiens)
        weights["Armor"] = 0.5
        weights["Weapons"] = 0.65
    elif is_steppe:
        weights["Mobility"] = 2.6      # Nomades → chevaux et mobilité avant tout
        weights["Armor"] = 0.6
        weights["Weapons"] = 0.85
    elif is_desert:
        weights["Mobility"] = 2.4      # Chameaux très importants
        weights["Armor"] = 0.7
    elif is_underdark:
        weights["Mobility"] = 0.12
        weights["Armor"] = 2.1
        weights["Weapons"] = 1.8
        weights["TravelGear"] = 1.5
    elif is_civilized_rich:
        weights["Armor"] = 1.45
        weights["Weapons"] = 1.35
        weights["Mobility"] = 0.85     # Moins prioritaire que l'équipement martial

    return weights


def get_wealth_bias(remaining_bp: int) -> Dict[str, float]:
    """
    Quand le capital restant est élevé, on pousse fortement vers l'armement et l'armure.
    Mais ce biais n'écrase pas complètement les préférences régionales.
    """
    if remaining_bp < 800:
        return {"Armor": 1.0, "Weapons": 1.0, "Mobility": 1.0, "TravelGear": 1.0, "RidingGear": 1.0}

    # Plus le capital est haut, plus Armor et Weapons deviennent attractifs
    armor_boost = min(2.8, 1.0 + (remaining_bp / 2200))
    weapons_boost = min(2.5, 1.0 + (remaining_bp / 2600))

    return {
        "Armor": armor_boost,
        "Weapons": weapons_boost,
        "Mobility": 1.0,
        "TravelGear": 1.0 + min(0.8, remaining_bp / 5000),
        "RidingGear": 1.0 + min(0.6, remaining_bp / 6000),
    }


def select_post_kit_purchases(
    region: str, 
    remaining_bp: int, 
    seed: int = None,
    magic_type: str = "None",
    magic_subtype: str = None,
    settlement_type: str = None,
    equipment_group: str = None   # Nouveau : groupe d'équipement explicite (prioritaire sur la résolution depuis la région)
) -> Dict:
    """
    Logique d'achats post-kit plus réaliste :
    - La majorité des personnages (surtout ceux avec un capital modéré) gardent une grande partie de leur argent.
    - Seuls ~10-15% des personnages "dépensiers" ou dans des contextes particuliers vont vraiment investir lourdement.
    - Restrictions magiques fortes :
        * Magie Verte / Sauvage Verte → aucune armure métallique.
        * Magie Arcanique → armure maximale = vêtements d'hiver (Gambeson tout au plus).
    - Biais comportemental boucliers (règle utilisateur) :
        * Urbain ou armure très performante → petits boucliers (Buckler/Rotella/Targe)
        * Rural ou sans armure chère → grands boucliers ronds (Aspis/Scutum/Round Shield)
    - Priorité d'achat dans la catégorie Armor (règle utilisateur) :
        * 1. Bouclier
        * 2. Casque
        * 3. Protection du torse (hauberk, breastplate, brigandine, gambeson, plackart...)
        * 4. Membres et reste (bras, jambes, etc.)
    - Priorité d'armes N1 + N2 :
        * N1 : pas de parrying (Main-gauche, buckler...) avant une vraie arme primaire une main.
        * N2 : pas deux armes lourdes (enc >=4) sans monture pour transporter la seconde.
    """
    if seed is not None:
        random.seed(seed)

    if remaining_bp < 280:
        return {
            "tier": 0,
            "tier_name": "None",
            "purchases": [],
            "total_spent_bp": 0,
            "final_remaining_bp": remaining_bp,
        }

    # === NOUVEAU : Résolution du groupe d'équipement (14 groupes) ===
    if equipment_group is None:
        equipment_group = get_equipment_group_for_region(region)

    regional_weights = get_regional_category_weights(region)
    wealth_bias = get_wealth_bias(remaining_bp)

    # === COMPORTEMENT DÉPENSES (selon ta correction) ===
    # La majorité des personnages qui ont de l'argent la dépensent en matériel utile
    # (montures, armure, sellerie, camping, etc.) quand c'est possible.
    # Seuls ~10-12% des personnages sont "frugaux" et gardent la majeure partie de leur capital.

    is_frugal = random.random() < 0.11   # ~11% des personnages gardent la plupart de leur argent

    if is_frugal:
        # Les rares personnages frugaux dépensent peu
        max_spend_ratio = 0.30
        max_items = random.randint(0, 2)
    else:
        # La grande majorité dépense agressivement ce qu'elle peut
        max_spend_ratio = 0.85
        max_items = min(6, 2 + remaining_bp // 550)

    # Combinaison des deux influences (région + richesse)
    final_weights = {}
    for cat in ALL_UPGRADE_ITEMS.keys():
        final_weights[cat] = regional_weights.get(cat, 1.0) * wealth_bias.get(cat, 1.0)

    purchases = []
    total_spent = 0.0

    categories = list(ALL_UPGRADE_ITEMS.keys())

    # Récupération des restrictions magiques
    magic_restr = get_magic_restrictions(magic_type, magic_subtype)

    for _ in range(max_items):
        if (remaining_bp - total_spent) < 180:
            break
        if total_spent > remaining_bp * max_spend_ratio:
            break

        # Choix pondéré par région + richesse
        weights_list = [final_weights.get(c, 1.0) for c in categories]
        cat = random.choices(categories, weights=weights_list, k=1)[0]

        # Filtrage : priorité au pool du groupe d'équipement (nouvelle stratégie)
        # Si le groupe a une liste riche, on l'utilise principalement.
        raw_items = ALL_UPGRADE_ITEMS[cat]
        group_items = get_available_items_for_equipment_group(equipment_group)

        # On garde les items qui sont à la fois dans la liste globale de la catégorie
        # et dans le pool du groupe (ou on prend le pool du groupe s'il est suffisant)
        if len(group_items) > 15:
            # On utilise principalement le pool du groupe (nouveaux prix avec surcoût inclus)
            # On filtre pour ne garder que les items qui existent aussi dans la catégorie choisie
            category_names = {raw[0] for raw in raw_items}
            candidates_from_group = [item for item in group_items if item[0] in category_names]
            tech_filtered = candidates_from_group if candidates_from_group else group_items
        else:
            # Fallback sur l'ancien système tech
            tech_filtered = get_available_items_for_region(raw_items, region, rarity_chance=0.05)

        # Filtrage magique (très important pour Magie Verte et Arcanique)
        magic_filtered = filter_items_by_magic(tech_filtered, magic_type, magic_subtype)

        if not magic_filtered:
            continue

        # Éviter les doublons
        already_bought_names = [p["name"] for p in purchases]
        candidates = [it for it in magic_filtered if it[0] not in already_bought_names]
        if not candidates:
            candidates = magic_filtered

        # === RÈGLES DE PRIORITÉ D'ARMES - NIVEAU 1 ===
        if cat == "Weapons" and len(candidates) > 1:
            has_primary = has_primary_one_handed_weapon(purchases)

            if not has_primary:
                # Le personnage n'a encore aucune arme principale une main
                # → On bloque les armes "parrying" (Main-gauche, petits boucliers)
                candidates = [it for it in candidates if it[0] not in PARRYING_WEAPONS]

                # → On donne une très forte priorité aux armes primaires une main
                if candidates:
                    primary_candidates = [it for it in candidates if it[0] in PRIMARY_ONE_HANDED_WEAPONS]
                    if primary_candidates:
                        candidates = primary_candidates

        # === RÈGLES DE PRIORITÉ D'ARMES - NIVEAU 2 ===
        # Règle utilisateur explicite : "pas 2 armes lourdes sans animal pour stocker la deuxieme"
        # Une arme lourde (encumbrance >= 4) ne peut être portée qu'à la main.
        # Sans monture, impossible de transporter une seconde arme de ce type.
        # On applique la restriction de manière proactive (comme N1) pour éviter
        # les achats inutiles qui seraient remboursés ensuite par enforce_no_mount_carry_limits.
        if cat == "Weapons" and len(candidates) > 1:
            already_has_heavy = has_heavy_weapon(purchases, equipment_group)
            has_animal = has_mount(purchases)

            if already_has_heavy and not has_animal:
                # Bloquer toute nouvelle arme lourde
                candidates = [
                    it for it in candidates
                    if get_item_encumbrance(equipment_group, it[0]) < 4
                ]

        # === PRIORITÉ D'ACHAT ARMOR (nouvelle règle utilisateur) ===
        # Bouclier > Casque > Torse > Membres / Autres
        if cat == "Armor" and len(candidates) > 1:
            priorities = [get_armor_purchase_priority(it[0]) for it in candidates]
            # Poids forts pour respecter l'ordre de priorité
            weights = [
                4.0 if p == 3 else   # Bouclier
                3.2 if p == 2 else   # Casque
                2.2 if p == 1 else   # Torso
                1.0                  # Membres (ou non-armure)
                for p in priorities
            ]
            item_name, price_str = random.choices(candidates, weights=weights, k=1)[0]

        elif cat == "TravelGear" and len(candidates) > 1:
            # Règle réaliste : matériel lourd (tente 4 places, lit de camp) seulement si on a une monture
            if not has_mount(purchases):
                heavy_travel = ["Tent, 4-man leather", "Camp bed, leather & wood"]
                candidates = [it for it in candidates if it[0] not in heavy_travel]

            if candidates:
                # Biais vers la tente plus petite (2-man est bien plus courant pour un aventurier seul)
                weights = []
                for it in candidates:
                    if "2-man" in it[0]:
                        weights.append(3.5)
                    elif "4-man" in it[0]:
                        weights.append(1.0)
                    else:
                        weights.append(1.8)
                item_name, price_str = random.choices(candidates, weights=weights, k=1)[0]
            else:
                # Aucun item léger disponible → on retombe sur un choix normal (rare)
                item_name, price_str = random.choice(magic_filtered)

        elif cat == "RidingGear" and len(candidates) > 1:
            # Règle réaliste : harnais lourds (Draft harness, War saddle, Packsaddle)
            # ne peuvent être achetés que si on a déjà une monture.
            heavy_harness = ["Draft harness", "War saddle", "Packsaddle"]
            if not has_mount(purchases):
                candidates = [it for it in candidates if it[0] not in heavy_harness]

            if candidates:
                item_name, price_str = random.choice(candidates)
            else:
                item_name, price_str = random.choice(magic_filtered)

        else:
            item_name, price_str = random.choice(candidates)

        # === CALCUL DU PRIX FINAL AVEC SURCOÛT GROUPE (nouveau système) ===
        # On calcule ici le prix réel que le personnage va payer, en tenant compte
        # du surcoût si l'objet est Rare ou Très rare dans son groupe.
        final_price_sp, rarity = get_final_price_for_purchase(equipment_group, item_name, price_str)
        cost = final_price_sp * 10.0
        display_price = f"{round(final_price_sp, 1)} sp" + (f" ({rarity})" if rarity not in ("Commun", "Toujours") else "")

        # === BIAIS COMPORTEMENTAL BOUCLIERS (règle utilisateur explicite) ===
        # Un personnage urbain ou avec armure très performante prend souvent des petits boucliers.
        # Un rural (ou sans armure chère) prend souvent de grands boucliers ronds.
        if cat == "Armor" and is_shield(item_name):
            pref = get_shield_preference(settlement_type, purchases)
            biased = choose_biased_shield(candidates, pref)
            if biased and biased[0] != item_name:
                item_name, price_str = biased

        # Budget : on laisse une petite réserve seulement (sauf pour les frugaux)
        if is_frugal:
            budget_ratio = 0.55
        else:
            # La majorité dépense jusqu'à 90-95% de ce qui reste, surtout sur armure/armes
            # Ratio un peu plus généreux pour Armor afin d'augmenter les chances d'avoir bouclier/casque/torse
            budget_ratio = 0.93 if cat in ("Armor", "Weapons") else 0.85

        if cost > (remaining_bp - total_spent) * budget_ratio:
            continue

        purchases.append({
            "name": item_name,
            "price_str": display_price,           # Prix final affiché (avec mention de rareté si applicable)
            "price_bp": round(cost, 1),
            "category": cat,
            "original_price_str": price_str,
            "final_price_sp": round(final_price_sp, 2),
            "rarity": rarity,
            "surcharge_applied": rarity in ("Rare", "Très rare")
        })
        total_spent += cost

    final_remaining = int(round(remaining_bp - total_spent))

    # === FALLBACK DÉFENSIF POUR BOUCLIER ===
    # Il est normal que presque tous les aventuriers aient un bouclier.
    # Les seules vraies exceptions sont les personnages qui ont investi dans une
    # armure de torse très performante et chère (Brigandine, Breastplate haut de gamme,
    # bon Hauberk, Plackart, Coat of Plates...). Avec les prix historiques actuels,
    # ces cas sont rares.
    has_shield = any(is_shield(p["name"]) for p in purchases)

    if not has_shield and final_remaining >= 240:
        # Si le personnage a déjà une armure de torse chère, la chance de prendre
        # aussi un bouclier en fallback est très faible (il mise sur sa protection).
        expensive_torso = any(
            any(kw in p["name"].lower() for kw in [
                "brigandine", "breastplate", "plackart", "coat of plates",
                "hauberk", "haubergeon"
            ])
            for p in purchases
        )

        chance = 0.06 if expensive_torso else 0.36

        if random.random() < chance:
            available_shields = [
                item for item in ARMOR_UPGRADES
                if is_shield(item[0]) and is_item_available(item[0], get_tech_level(region))
            ]
            if available_shields:
                def shield_cost(it):
                    corr = price_fix.get_historical_price(it[0], it[1])
                    return kits.parse_price_to_bp(corr)
                available_shields.sort(key=shield_cost)
                for candidate in available_shields:
                    corr_price = price_fix.get_historical_price(candidate[0], candidate[1])
                    c = kits.parse_price_to_bp(corr_price)
                    if c <= final_remaining * 0.95:
                        purchases.append({
                            "name": candidate[0],
                            "price_str": corr_price,
                            "price_bp": round(c, 1),
                            "category": "Armor",
                            "original_price_str": None
                        })
                        final_remaining -= int(c)
                        total_spent += c
                        break

    # === NOUVELLE RÈGLE : Limites de port sans monture ===
    # Un personnage sans monture ne peut pas transporter plusieurs boucliers
    # ni plusieurs armes d'hast longues. Les javelins restent en multiples.
    # On rembourse l'argent des objets retirés.
    purchases, refunded = enforce_no_mount_carry_limits(purchases)
    if refunded > 0:
        total_spent -= refunded
        final_remaining += int(round(refunded))

    # === NOUVELLE RÈGLE : Carquois obligatoire avec arc/arbalète ===
    # Un personnage qui possède un arc ou une arbalète doit obligatoirement
    # avoir un carquois (ou un étui pour arbalète). On l'ajoute gratuitement
    # si le budget restant le permet, sinon on le force quand même.

    # === GARANTIE ARME DE BASE (nouvelle règle demandée) ===
    # On veut que très peu de personnages commencent sans aucune arme.
    # Si après tous les achats le personnage n'a aucune arme, on lui force
    # l'achat de l'arme de mêlée la moins chère disponible dans son groupe
    # (généralement une lance, un gourdin, un bâton ou une hache rudimentaire).
    has_any_weapon = any(is_weapon_or_armor(p["name"]) for p in purchases)

    if not has_any_weapon and final_remaining >= 50:
        # Cherche l'arme de mêlée la moins chère dans le pool du groupe
        group_pool = group_equipment_pools.get_group_pool(equipment_group)

        basic_melee = []
        primary_melee = []

        for item in group_pool:
            name = item["name"]
            name_lower = name.lower()
            price = item.get("final_price_sp", item["price_sp"])

            if price <= 60 and any(kw in name_lower for kw in [
                "spear", "lance", "club", "gourdin", "staff", "baton", "quarterstaff",
                "axe", "hache", "mace", "masse", "hammer", "marteau"
            ]):
                basic_melee.append((name, price))

                # On préfère les vraies armes primaires une main quand on force
                if name in PRIMARY_ONE_HANDED_WEAPONS:
                    primary_melee.append((name, price))

        # On privilégie une arme primaire si possible
        candidates_to_force = primary_melee if primary_melee else basic_melee

        if candidates_to_force:
            candidates_to_force.sort(key=lambda x: x[1])
            cheapest_name, cheapest_price = candidates_to_force[0]

            if cheapest_price * 10 <= final_remaining * 0.95:
                purchases.append({
                    "name": cheapest_name,
                    "price_str": f"{cheapest_price} sp (arme de base forcée)",
                    "price_bp": round(cheapest_price * 10, 1),
                    "category": "Weapons",
                    "original_price_str": None,
                    "final_price_sp": cheapest_price,
                    "rarity": "Commun",
                    "surcharge_applied": False,
                    "forced_basic_weapon": True
                })
                final_remaining -= int(round(cheapest_price * 10))
                total_spent += cheapest_price * 10
    has_bow = any(is_bow(p["name"]) for p in purchases)
    has_quiver = any(p["name"].lower() == "quiver" for p in purchases)

    if has_bow and not has_quiver:
        quiver_price = grp_prices.get_groupe1_price("Quiver / Bolt case (carquois vide)", 1.5)  # from master, fallback approx
        quiver_bp = 40

        purchases.append({
            "name": "Quiver",
            "price_str": "10 sp",
            "price_bp": quiver_bp,
            "category": "Weapons",
            "original_price_str": None
        })
        total_spent += quiver_bp
        final_remaining -= quiver_bp

    tier = 0
    if total_spent > 2200:
        tier = 3
    elif total_spent > 950:
        tier = 2
    elif total_spent > 320:
        tier = 1

    tier_names = ["None", "Modest", "Comfortable", "Wealthy", "Rich"]

    return {
        "tier": tier,
        "tier_name": tier_names[min(tier, 4)],
        "purchases": purchases,
        "total_spent_bp": round(total_spent, 1),
        "final_remaining_bp": final_remaining,
    }


if __name__ == "__main__":
    print("=== Test du système Post-Kit Purchases ===\n")

    test_cases = [
        ("Great Glacier", 500),
        ("Great Glacier", 1200),
        ("Waterdeep", 4500),
        ("Waterdeep", 12000),
        ("Hordelands (The Endless Wastes)", 1800),
        ("Chult", 2200),
        ("Anauroch", 900),
        ("Underdark", 1500),
    ]

    for region, remaining in test_cases:
        result = select_post_kit_purchases(region, remaining, seed=42)
        print(f"{region:35} | Remaining: {remaining:5} bp → Tier {result['tier']} ({result['tier_name']})")
        if result["purchases"]:
            for p in result["purchases"]:
                print(f"    + {p['name']:25} {p['price_str']:>8} ({p['price_bp']:6.1f} bp)")
            print(f"    Total dépensé : {result['total_spent_bp']} bp | Restant : {result['final_remaining_bp']} bp")
        else:
            print("    (aucun achat significatif)")
        print()
