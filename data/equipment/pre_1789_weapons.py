"""
data/equipment/pre_1789_weapons.py

WEAPONS USED BEFORE THE FRENCH REVOLUTION (PRE-1789)
Maximum plausible strike / muzzle energies in Joules.

Compact format: Joules at start + Name + Description on the same line.
Values are MAXIMUM historically plausible (strike energy for melee/thrown,
muzzle energy for firearms/artillery).

Sources: historical tests, reconstructions, biomechanical models.
Real performance varied with user, conditions, and specific weapon.

One hypothetical/fantasy entry included at the end for comparison.
"""

from typing import List, Dict, Optional, Iterable
import re

# All energies stored as integer Joules (not kJ)
Weapon = Dict[str, object]

PRE_1789_WEAPONS: List[Weapon] = [
    # =============================================================================
    # MELEE WEAPONS (sorted by max energy)
    # =============================================================================
    {
        "energy_j": 600,
        "name": "War Hammer",
        "description": "A hammer-like weapon with a flat striking face on one side and often a pick or spike on the other, mounted on a haft. Evolved in the late medieval and Renaissance periods specifically to defeat plate armor through blunt trauma and penetration. Used by both foot soldiers and mounted knights into the 17th-18th centuries.",
        "category": "Melee",
        "subtype": "blunt / pick",
    },
    {
        "energy_j": 550,
        "name": "Flanged Mace",
        "description": "A blunt weapon with a heavy metal head featuring radiating flanges or ridges, designed to concentrate impact force against plate armor. Popular from the 14th to 17th centuries as swords became less effective against improving armor. Often used by infantry and some cavalry.",
        "category": "Melee",
        "subtype": "blunt",
    },
    {
        "energy_j": 500,
        "name": "Halberd / Poleaxe",
        "description": "A polearm combining an axe blade, spike, and often a hammer face on a long shaft (typically 1.5-2.5 m). Dominant infantry weapon from the 14th to 17th centuries, used in dense formations for thrusting, chopping, and pulling riders from horses. Swiss and German variants were especially famous.",
        "category": "Melee",
        "subtype": "polearm",
    },
    {
        "energy_j": 450,
        "name": "Battle Axe",
        "description": "A single- or double-headed axe with a sturdy haft, used for chopping and hooking in combat from early medieval times through the 17th century. Infantry and some cavalry versions existed. Effective against armor and unarmored targets alike.",
        "category": "Melee",
        "subtype": "axe",
    },
    {
        "energy_j": 450,
        "name": "Crossbow (heavy)",
        "description": "A mechanical bow mounted on a stock, cocked by various means (stirrup, windlass, or cranequin). Used extensively from the 12th century through the 17th-18th centuries in European armies and for hunting. Heavy siege versions existed. Easier to use than longbows but slower to reload.",
        "category": "Ranged (non-firearm)",
        "subtype": "crossbow",
    },
    {
        "energy_j": 400,
        "name": "Longsword (Arming Sword / Knightly Sword)",
        "description": "A straight, double-edged sword typically 80-110 cm long with a cruciform hilt, used primarily by knights and men-at-arms from the 13th to 17th centuries. Versatile for cutting, thrusting, and half-swording techniques against armored and unarmored opponents. Remained in use alongside early firearms into the 17th century.",
        "category": "Melee",
        "subtype": "sword",
    },
    {
        "energy_j": 400,
        "name": "Flail / Morningstar",
        "description": "A weapon with a striking head (spiked or smooth) attached by a chain or hinge to a haft. Used from medieval times into the early modern period, particularly against armored opponents. The flexible design allowed strikes around shields but was harder to control.",
        "category": "Melee",
        "subtype": "flail / blunt",
    },
    {
        "energy_j": 350,
        "name": "Saber (Cavalry Saber)",
        "description": "A curved, single-edged sword designed for slashing from horseback, widely used by cavalry from the 16th through 18th centuries across Europe and beyond. Effective for mounted charges and close combat. Variants like the Hungarian or Polish szabla were iconic.",
        "category": "Melee",
        "subtype": "sword (cavalry)",
    },
    {
        "energy_j": 300,
        "name": "Javelin / Throwing Spear",
        "description": "A light spear designed for throwing, used by infantry, cavalry, and skirmishers from ancient times through the 18th century (e.g., in Roman, medieval, and early modern armies). Often carried in multiples for harassment before melee.",
        "category": "Ranged (non-firearm)",
        "subtype": "thrown",
    },
    {
        "energy_j": 250,
        "name": "Pike / Spear (Infantry)",
        "description": "A long thrusting polearm (pikes often 4-6+ meters) used in dense formations (pike squares or tercio) from ancient times through the 18th century. The dominant infantry weapon until the widespread adoption of the bayonet. Spears were shorter variants for individual use.",
        "category": "Melee",
        "subtype": "polearm",
    },
    {
        "energy_j": 150,
        "name": "Rapier",
        "description": "A slender, sharply pointed thrusting sword popular in the 16th and 17th centuries, especially in civilian dueling and military contexts in Western Europe. Often paired with a parrying dagger. Emphasized precision and reach over cutting power.",
        "category": "Melee",
        "subtype": "sword (civilian/thrusting)",
    },
    {
        "energy_j": 150,
        "name": "Dagger / Stiletto",
        "description": "Short, pointed blade (often under 40 cm) used as a secondary weapon or for close-quarters thrusting. Common from medieval times through the 18th century in both military and civilian contexts. Stilettos were particularly associated with assassination and dueling in Renaissance Italy.",
        "category": "Melee",
        "subtype": "dagger",
    },

    # =============================================================================
    # RANGED PROJECTILE WEAPONS (NON-FIREARM)
    # =============================================================================
    {
        "energy_j": 1500,
        "name": "Sling (expert throw)",
        "description": "A simple projectile weapon consisting of a pouch on cords, swung to hurl stones or lead glandes. Used from prehistoric times through antiquity and into the early modern period by skirmishers and some irregular forces. Extremely portable and cheap. Highly variable depending on user skill and projectile.",
        "category": "Ranged (non-firearm)",
        "subtype": "sling",
    },
    {
        "energy_j": 200,
        "name": "English Longbow",
        "description": "A powerful self-bow made of yew or similar wood, typically 1.8-2 m long with draw weights of 80-180+ lbs. The signature weapon of English armies from the 13th to 16th centuries (and used sporadically later). Required lifelong training but offered high rate of fire.",
        "category": "Ranged (non-firearm)",
        "subtype": "bow",
    },

    # =============================================================================
    # EARLY FIREARMS (PERSONAL)
    # =============================================================================
    {
        "energy_j": 4000,
        "name": "Flintlock Musket (e.g. Brown Bess or Charleville)",
        "description": "The dominant infantry firearm of the 17th and 18th centuries. Smoothbore, muzzle-loading, .69-.75 caliber, using flintlock ignition. Standard weapon of line infantry in conflicts like the Seven Years' War and American Revolutionary War. Slow to reload but reliable in massed volleys. Bayonet attachment common by mid-18th century.",
        "category": "Early Firearm",
        "subtype": "musket",
    },
    {
        "energy_j": 3000,
        "name": "Arquebus",
        "description": "An early smoothbore firearm (matchlock or wheellock ignition) from the 15th-17th centuries, typically .50-.75 caliber. Used by infantry in European wars (Italian Wars, Thirty Years' War, etc.). Required a rest for aiming in early versions. Bridge between hand cannons and true muskets.",
        "category": "Early Firearm",
        "subtype": "arquebus",
    },
    {
        "energy_j": 1500,
        "name": "Flintlock Pistol",
        "description": "Short-barreled, muzzle-loading handgun with flintlock mechanism, common from the late 17th century onward. Used by cavalry, officers, and for personal defense/dueling. Often came in pairs. Lower power and accuracy than muskets but essential for close combat and as a backup weapon.",
        "category": "Early Firearm",
        "subtype": "pistol",
    },

    # =============================================================================
    # ARTILLERY AND SIEGE WEAPONS
    # =============================================================================
    {
        "energy_j": 600000,
        "name": "Field Cannon (e.g. 12-pounder)",
        "description": "Bronze or iron smoothbore muzzle-loading cannon firing round shot, common in 16th-18th century European armies. Organized by the weight of the shot (e.g., 6-pdr, 12-pdr). Provided mobile firepower on battlefields. Used extensively in the wars of Louis XIV, Seven Years' War, and early American conflicts. Crew-served weapon. Larger siege guns reached well over 1 MJ.",
        "category": "Artillery",
        "subtype": "cannon",
    },
    {
        "energy_j": 200000,
        "name": "Trebuchet (Counterweight Siege Engine)",
        "description": "A large medieval siege engine using a counterweight to hurl heavy stones or other projectiles at castle walls. Dominant from the 12th to 15th centuries (and occasionally later). Capable of breaching fortifications or causing massive casualties in sieges. Required large crews and engineering knowledge. Highly variable by design and projectile mass.",
        "category": "Artillery",
        "subtype": "siege engine",
    },

    # =============================================================================
    # HYPOTHETICAL / MAGIC PROJECTILES (fantasy comparison)
    # =============================================================================
    {
        "energy_j": 5000,
        "name": "Magic Projectile",
        "description": "A magically enhanced or conjured projectile (enchanted musket ball, magic arrow, or pure arcane missile) delivering 5000 joules of kinetic energy. Significantly more powerful than a standard flintlock musket (roughly 1.4× to 3× stronger depending on the load). Could represent a high-level spell, enchanted ammunition, or magically accelerated projectile in a fantasy version of the pre-1789 era. Energy could come from arcane sources rather than black powder or human strength.",
        "category": "Hypothetical / Magic",
        "subtype": "magic",
    },
]


def format_weapon(w: Weapon, include_category: bool = False) -> str:
    """Return the weapon in the requested compact format:
    **{energy} J** — Name: Description
    """
    energy = w["energy_j"]
    if energy >= 1000:
        # Show kJ for big numbers but keep the primary value in J for sorting/comparison
        if energy >= 100000:
            energy_str = f"{energy // 1000:,} kJ ({energy:,} J)"
        else:
            energy_str = f"{energy:,} J"
    else:
        energy_str = f"{energy} J"

    line = f"**{energy_str}** — {w['name']}: {w['description']}"
    if include_category:
        line += f"  [Category: {w['category']}]"
    return line


def get_all_weapons() -> List[Weapon]:
    """Return a copy of the full list (in the order defined above)."""
    return list(PRE_1789_WEAPONS)


def get_weapons_by_category(category: str) -> List[Weapon]:
    """Return weapons filtered by exact category (case-sensitive)."""
    return [w for w in PRE_1789_WEAPONS if w["category"] == category]


def get_weapon_by_name(name: str) -> Optional[Weapon]:
    """Case-insensitive lookup by name or partial name."""
    name_lower = name.lower()
    for w in PRE_1789_WEAPONS:
        if name_lower in w["name"].lower():
            return w
    return None


def get_weapons_sorted_by_energy(reverse: bool = True) -> List[Weapon]:
    """Return all weapons sorted by energy (descending by default)."""
    return sorted(PRE_1789_WEAPONS, key=lambda w: w["energy_j"], reverse=reverse)


def print_full_document() -> None:
    """Print the entire list in the exact compact format requested by the user."""
    categories_order = [
        "Melee",
        "Ranged (non-firearm)",
        "Early Firearm",
        "Artillery",
        "Hypothetical / Magic",
    ]

    print("WEAPONS USED BEFORE THE FRENCH REVOLUTION (PRE-1789)")
    print("Joules at start + Name + Description on the same line (compact format)")
    print("=" * 80)
    print()

    for cat in categories_order:
        weapons = get_weapons_by_category(cat)
        if not weapons:
            continue

        # Section headers matching the original document style
        if cat == "Melee":
            print("--------------------------------------------------------------------------------")
            print("MELEE WEAPONS (sorted by max energy)")
            print("--------------------------------------------------------------------------------")
        elif cat == "Ranged (non-firearm)":
            print()
            print("--------------------------------------------------------------------------------")
            print("RANGED PROJECTILE WEAPONS (NON-FIREARM)")
            print("--------------------------------------------------------------------------------")
        elif cat == "Early Firearm":
            print()
            print("--------------------------------------------------------------------------------")
            print("EARLY FIREARMS (PERSONAL)")
            print("--------------------------------------------------------------------------------")
        elif cat == "Artillery":
            print()
            print("--------------------------------------------------------------------------------")
            print("ARTILLERY AND SIEGE WEAPONS")
            print("--------------------------------------------------------------------------------")
        elif cat == "Hypothetical / Magic":
            print()
            print("--------------------------------------------------------------------------------")
            print("HYPOTHETICAL / MAGIC PROJECTILES")
            print("--------------------------------------------------------------------------------")

        print()
        for w in weapons:
            print(format_weapon(w))
            print()

    # Summary section
    print("=" * 80)
    print("SUMMARY - MAXIMUM ENERGIES (Highest to Lowest)")
    print("=" * 80)

    sorted_weapons = get_weapons_sorted_by_energy()
    for w in sorted_weapons:
        energy = w["energy_j"]
        if energy >= 100000:
            e_str = f"{energy // 1000:>7,} kJ"
        else:
            e_str = f"{energy:>7,} J"
        print(f"{e_str}   {w['name']}")

    print()
    print("=" * 80)
    print("END OF DOCUMENT")
    print("Compact format: Joules + Name + Description all starting on the same line.")
    print("Fantasy entry added at user's request.")
    print("=" * 80)


def get_energy_summary() -> Dict[str, int]:
    """Return a simple dict of name -> energy_j for quick reference."""
    return {w["name"]: w["energy_j"] for w in PRE_1789_WEAPONS}


if __name__ == "__main__":
    print_full_document()
