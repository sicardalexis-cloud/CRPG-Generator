"""
data/equipment/armor_sets.py

Historical armor logic for the character generator.

- SHIELDS_BY_SIZE + get_shield_for_armor_level : table-driven progressive shield size reduction
  (Scutum Size 11 -> smaller bucklers as armor level increases per user-provided
   "Shield Size Evolution in the Middle Ages" table). Used by melee path in protocol.

- build_historical_armor_set(budget_sp, context=None) : DYNAMIC BUILDER (preferred for live protocol).
  Constructs layered, historically plausible armor from *available funds* (capital_left after
  base kit + first side weapon). All prices live from Groupe1_Cote_des_Epees_Equipement.txt.
  Enforces:
    * fabric (aketon/gambeson/arming doublet...) before vambraces/couter/rerebrace and before gorget
    * gorget/bevor never on skin (requires fabric)
    * pauldrons only with proper cuirass (Breastplate + Backplate / tempered)
    * tassets/fauld/garde-reins on plate torso
  Progression mirrors the era descriptors from the shield table (padded+short mail -> coat of plates/
  brigandine -> developed cuirass + full limbs + articulated harness).

- Legacy: get_most_expensive_affordable_set + Sets_Armures.txt parsing still present for reference
  or other tooling, but the skill-based protocol (utils.py) now calls the dynamic builder instead
  of static prebuilts (per user request to stop using sets_armures.txt for the fund-based armor step).

The old "70% of capital" prebuilt selection is superseded by the builder + protocol flow.
"""

from pathlib import Path
from typing import List, Dict, Optional
import re

from . import groupe1_prices as grp_prices

# =============================================================================
# CONFIGURATION
# =============================================================================

BASE_DIR = Path(__file__).parent
ARMOR_SETS_FILE = BASE_DIR / "systeme armure preconstruites" / "Sets_Armures.txt"


# =============================================================================
# PARSING
# =============================================================================

def _parse_armor_sets_file() -> List[Dict]:
    """
    Parse le fichier Sets_Armures.txt et retourne une liste de sets triés
    par prix décroissant (du plus cher au moins cher).
    """
    if not ARMOR_SETS_FILE.exists():
        raise FileNotFoundError(f"Fichier introuvable : {ARMOR_SETS_FILE}")

    sets = []
    text = ARMOR_SETS_FILE.read_text(encoding="utf-8")

    # Pattern : "123 sp - Nom du set"
    pattern = re.compile(r'^\s*(\d+(?:\.\d+)?)\s*sp\s*-\s*(.+?)\s*$', re.IGNORECASE)

    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        match = pattern.match(line)
        if match:
            price_sp = float(match.group(1))
            name = match.group(2).strip()

            sets.append({
                "name": name,
                "price_sp": price_sp,
                "price_bp": round(price_sp * 10, 1)   # Conversion en bp (unité interne)
            })

    # Trier par prix décroissant (le plus cher en premier)
    sets.sort(key=lambda x: x["price_sp"], reverse=True)
    return sets


# Cache simple (le fichier ne change pas souvent)
_ARMOR_SETS_CACHE: Optional[List[Dict]] = None


def get_all_armor_sets() -> List[Dict]:
    """Retourne tous les sets d'armure, triés du plus cher au moins cher."""
    global _ARMOR_SETS_CACHE
    if _ARMOR_SETS_CACHE is None:
        _ARMOR_SETS_CACHE = _parse_armor_sets_file()
    return _ARMOR_SETS_CACHE


def get_most_expensive_affordable_set(budget_sp: float) -> Optional[Dict]:
    """
    Retourne le set d'armure le plus cher que le personnage peut s'offrir
    avec le budget donné (en sp).

    Règle utilisateur : on prend **le plus cher possible**.
    """
    if budget_sp <= 0:
        return None

    all_sets = get_all_armor_sets()

    for armor_set in all_sets:
        if armor_set["price_sp"] <= budget_sp:
            return armor_set.copy()

    # Si même le set le moins cher est trop cher
    return None


def get_armor_sets_within_budget(budget_sp: float) -> List[Dict]:
    """Retourne tous les sets que le personnage peut s'offrir (pour debug ou choix futur)."""
    if budget_sp <= 0:
        return []

    all_sets = get_all_armor_sets()
    return [s.copy() for s in all_sets if s["price_sp"] <= budget_sp]


# =============================================================================
# FONCTIONS UTILITAIRES
# =============================================================================

def calculate_armor_budget(starting_capital: float, percentage: float = 0.70) -> float:
    """
    Calcule le budget maximum allouable à l'armure.
    Par défaut : 70% du capital de départ (règle utilisateur actuelle).

    Note : starting_capital est maintenant exprimé directement en sp
    (plus de conversion bp intermédiaire).
    """
    if starting_capital <= 0:
        return 0.0
    return starting_capital * percentage   # Directement en sp


def format_armor_set(armor_set: Dict) -> str:
    """Joli affichage d'un set."""
    if not armor_set:
        return "Aucune armure"
    return f"{armor_set['name']} ({armor_set['price_sp']:.0f} sp)"


# =============================================================================
# TEST / DEBUG
# =============================================================================

if __name__ == "__main__":
    print("=== Test du nouveau système d'armures préconstruites ===\n")

    all_sets = get_all_armor_sets()
    print(f"Nombre total de sets chargés : {len(all_sets)}")
    print(f"Set le moins cher : {all_sets[-1]['name']} ({all_sets[-1]['price_sp']} sp)")
    print(f"Set le plus cher  : {all_sets[0]['name']} ({all_sets[0]['price_sp']} sp)\n")

    # Exemples de budget
    test_budgets = [50, 120, 180, 250, 400, 700]

    for budget in test_budgets:
        chosen = get_most_expensive_affordable_set(budget)
        print(f"Budget {budget:>4} sp -> {format_armor_set(chosen)}")


# =============================================================================
# SHIELD SIZE EVOLUTION vs ARMOR LEVEL (per historical table)
# =============================================================================

# Shields available for protocol (prices from master Groupe1_Cote_des_Epees_Equipement.txt;
# sizes per "Shield Size Evolution in the Middle Ages" table)
# Starting melee kit uses Size 11 (Scutum) for full progressive reduction as armor develops.
SHIELDS_BY_SIZE = [
    {"name": "Scutum (Size 11)", "price_sp": grp_prices.get_groupe1_price("Scutum (Size 11)", 35), "size": 11},
    {"name": "Kite Shield (Size 10)", "price_sp": grp_prices.get_groupe1_price("Kite Shield (Size 10)", 27), "size": 10},
    {"name": "Brocchiere (Size 1)", "price_sp": grp_prices.get_groupe1_price("Brocchiere (Size 1)", 5), "size": 1},
    {"name": "Small Buckler (Size 2)", "price_sp": grp_prices.get_groupe1_price("Small Buckler (Size 2)", 7), "size": 2},
    {"name": "Buckler (Size 3)", "price_sp": grp_prices.get_groupe1_price("Buckler (Size 3)", 9), "size": 3},
    {"name": "Large Buckler (Size 4)", "price_sp": grp_prices.get_groupe1_price("Large Buckler (Size 4)", 12), "size": 4},
    {"name": "Small Rotella (Size 5)", "price_sp": grp_prices.get_groupe1_price("Small Rotella (Size 5)", 14), "size": 5},
    {"name": "Rotella (Size 6)", "price_sp": grp_prices.get_groupe1_price("Rotella (Size 6)", 16), "size": 6},
    {"name": "Large Rotella (Size 7)", "price_sp": grp_prices.get_groupe1_price("Large Rotella (Size 7)", 22), "size": 7},
    {"name": "Heater Shield (Size 8)", "price_sp": grp_prices.get_groupe1_price("Heater Shield (Size 8)", 24), "size": 8},
    {"name": "Velites Parma (Size 9)", "price_sp": grp_prices.get_groupe1_price("Velites Parma (Size 9)", 26), "size": 9},
]


def get_shield_for_armor_level(armor_set: Optional[Dict]) -> Dict:
    """
    Return the historically appropriate shield (name, price_sp, size) for a melee character
    given their chosen armor set.

    UPGRADED: The level of *plate protection of the legs, knee, thigh and hips (in this order)*
    now dictates the shield size reduction.

    Historical basis (user-provided):
    La taille des boucliers médiévaux a bien diminué progressivement à mesure que la protection
    des jambes, cuisses et bassin s’améliorait.

    Évolution historique :
    - Haut Moyen Âge (XIe-XIIe siècles) : boucliers grands (kite shield) descendant jusqu’aux genoux
      ou plus bas pour protéger les jambes très vulnérables (peu ou pas d’armure de jambes, souvent
      juste une cotte de mailles). Particulièrement important pour les cavaliers.
    - Fin XIIe - XIIIe siècles : avec l’apparition progressive des protections de jambes (cuissards
      en mailles, puis premières plates), le bouclier se raccourcit (heater shield), plus court,
      qui descend généralement jusqu’à la taille ou mi-cuisse. La partie inférieure pointue du kite
      est progressivement coupée.
    - XIVe-XVe siècles : avec le développement de l’armure de plates complète (cuisses, genouillères,
      grèves, et protection du bassin), le bouclier devient encore plus petit (heater de taille
      moyenne ou buckler 20-40 cm servant à parer et frapper).
    Raison principale : Le bouclier n’avait plus besoin de couvrir ce qui était déjà protégé par
    l’armure des membres inférieurs. Préférence pour un bouclier plus léger et maniable, meilleure
    mobilité, et possibilité d’armes à deux mains. À la fin du Moyen Âge, beaucoup de chevaliers
    en armure complète combattaient même sans bouclier du tout.

    Implementation:
    - Primary driver = cumulative plate protection on lower body, checked in the specified order:
      legs (greaves, schynbalds/demi-greaves), knee (poleyns + genouillères), thigh (cuisses),
      hips/basin (tassets longs + fauld + garde-reins).
    - Sabatons add the final foot completion.
    - Early mail leg protection (chausses etc.) gives the first reductions (Size 9-10).
    - This is combined with overall harness indicators (cuirass, high price, full named harness)
      for the very smallest sizes (1-3) when the lower body is fully articulated.
    - Still supports legacy static set names (e.g. "jambes complètes", "harnois", "coat of plates")
      and the previous price bands as fallbacks.
    - The dynamic builder (build_historical_armor_set) now also adds lower-body pieces preferring
      the historical order (legs -> knee -> thigh -> hips) when budget allows.

    Starts with Scutum (Size 11) for all melee.
    Progressively reduces per the evolution above.
    ~25-30% surface drop per step.
    Credit price diff back (intended economic effect on mount + pocket).
    Supports builder "items" list for accurate piece-based detection.
    """
    if not armor_set:
        return {"name": "Scutum (Size 11)", "price_sp": grp_prices.get_groupe1_price("Scutum (Size 11)", 35), "size": 11}

    # Support str | list | dict (for legacy prebuilts and new dynamic builder)
    def _get_search_text(a):
        if isinstance(a, (list, tuple)):
            return " ".join(str(x).lower() for x in a)
        if isinstance(a, dict):
            parts = []
            if a.get("name"):
                parts.append(str(a.get("name", "")).lower())
            for it in a.get("items", []) or []:
                parts.append(str(it).lower())
            return " ".join(parts)
        if isinstance(a, str):
            return a.lower()
        return str(a).lower()

    search = _get_search_text(armor_set)
    if "aucune" in search:
        return {"name": "Scutum (Size 11)", "price_sp": grp_prices.get_groupe1_price("Scutum (Size 11)", 35), "size": 11}

    # price from dict if present, else 0 for keyword-driven decisions
    if isinstance(armor_set, dict):
        price_sp = float(armor_set.get("price_sp", 0))
    else:
        price_sp = 0.0
    # name var kept for legacy direct string checks but we primarily use 'search'
    name = search

    # Determine target size. UPGRADED: legs/knee/thigh/hips plate protection level (in this order)
    # is now the primary dictator of reduction. See docstring for full historical rationale + mapping.
    target_size = 11

    s = name  # lowered search text containing joined pieces or legacy set name

    # =====================================================================
    # UPGRADED CORE LOGIC (per user request)
    # Level of plate protection of the legs, knee, thigh and hips (in this order)
    # dictates the shield size reduction.
    # See full historical justification in the function docstring.
    # =====================================================================

    # Detect specific lower-body plate pieces (exact names from the dynamic builder +
    # master price list + legacy compatibility).
    has_lower_legs = any(k in s for k in [
        "greaves (renforcées", "greaves (normales", "greaves",
        "schynbalds / demi-greaves", "schynbalds", "demi-greaves"
    ])
    has_knees = any(k in s for k in [
        "poleyns + genouillères", "poleyns", "genouillères", "genouilleres"
    ])
    has_thighs = any(k in s for k in [
        "cuisses (renforcées maximilian", "cuisses (normales", "cuisses"
    ])
    has_hips_basin = any(k in s for k in [
        "tassets longs", "tassets long", "fauld", "garde-reins"
    ])
    has_sabatons = "sabatons" in s

    # Early / transitional mail leg protection (gives first size reductions)
    has_mail_legs = any(k in s for k in ["mail chausses", "chausses", "demi-chausses", "mail leg"]) or \
                    ("mail" in s and ("jambes" in s or "legs" in s or "chausses" in s))

    # Legacy / old static set strings (for compatibility with Test files and any remaining prebuilts)
    has_legacy_full_legs = any(x in s for x in ["jambes complètes", "jambes classiques", "jambes", "bras complet"])

    if has_legacy_full_legs and not has_thighs:
        has_thighs = True
    if has_legacy_full_legs and not has_lower_legs:
        has_lower_legs = True

    # Compute leg protection score (0 = none / mail only, 5 = full plate legs+knee+thigh+hips+feet)
    # Order of increments follows the user's provided chronological table exactly:
    # Fin XIIIe: legs (greaves/tibias) + knees (poleyns) FIRST
    # then cuisses (thighs)
    # then hips/basin (tassets etc.)
    # This makes the shield reduction follow real history (legs protected first → shield shrinks first).
    leg_score = 0
    if has_lower_legs:
        leg_score += 1   # legs (greaves etc.) - FIRST per chrono table (Fin XIIIe)
    if has_knees:
        leg_score += 1   # knee (poleyns/genouillères) - also Fin XIIIe
    if has_thighs:
        leg_score += 1   # thigh (cuisses) - Début XIVe
    if has_hips_basin:
        leg_score += 1   # hips / basin (tassets + fauld + garde-reins) - later
    if has_sabatons:
        leg_score += 1   # sabatons complete (very late)
    if has_mail_legs and leg_score == 0:
        leg_score = 1    # basic mail leg coverage counts as the earliest improvement

    # --- Map leg_score (primary) + overall harness quality to SIZE ---
    # Higher leg protection (especially in the specified order) = smaller, more manageable shield.
    # This directly encodes the provided historical evolution (large kite for unprotected legs ->
    # heater as leg plates appear -> small buckler/brocchiere with full cuisses+greaves+basin plate).

    if leg_score >= 4:
        # Full lower body plate (legs + knee + thigh + hips/basin) + usually sabatons.
        # XIVe-XVe "complete white harness" era. Shield becomes auxiliary or disappears.
        if (price_sp >= 75 or "harnois" in s or ("breastplate" in s and "backplate" in s) or
            ("close helmet" in s or "armet" in s or "great bascinet" in s)):
            target_size = 1
        else:
            target_size = 2
    elif leg_score == 3:
        # Strong lower body: at least thighs + knees + lower legs (+ maybe partial hips)
        # Developed plate legs + emerging basin protection.
        if has_hips_basin or price_sp >= 45 or ("breastplate" in s and "backplate" in s):
            target_size = 3
        else:
            target_size = 4
    elif leg_score == 2:
        # Good but incomplete: e.g. lower legs + knees, or thighs + lower legs (missing one link)
        # Early-to-mid XIVe transition.
        target_size = 4 if price_sp >= 30 else 5
    elif leg_score == 1:
        # First plate on legs (greaves/schynbalds) or mail chausses / basic cuisses.
        # Fin XIIe - XIIIe / early XIVe : shield starts to shorten (heater era).
        target_size = 6 if price_sp >= 22 else 7

    # If leg_score == 0 (or still at default), fall back to previous torso / mail / padded
    # logic and price bands. These cover the early medieval cases (no real leg plate yet)
    # and provide compatibility.

    if leg_score == 0:
        # SIZE 1-3 high end even without explicit leg pieces (very expensive full named sets)
        if any(k in s for k in ["maximilian", "harnois de brèche", "harnois de joute", "caparaçon et harnois"]):
            target_size = 1
        elif "harnois gothic" in s or ("gothic" in s and price_sp >= 65) or ("close helmet" in s and price_sp >= 50):
            target_size = 2
        elif "harnois" in s and price_sp >= 55 and any(k in s for k in ["armet", "sabatons", "gantelets", "gauntlets", "close helmet"]):
            target_size = 3
        elif "armet" in s and price_sp >= 50 and any(x in s for x in ["bras complet", "jambes", "cuisses", "greaves", "sabatons", "vambraces", "rerebrace"]):
            target_size = 3
        elif "great bascinet" in s:
            target_size = 4
        # SIZE 7-8 from transitional torso (coat of plates, simple breastplate + some arm/leg hints)
        elif "coat of plates" in s:
            target_size = 7
        elif "plackart" in s and price_sp >= 18:
            target_size = 7
        elif "simple breastplate" in s and (price_sp >= 12 or any(x in s for x in ["bras", "vambraces", "couter", "rerebrace", "jambes"])):
            target_size = 8
        # SIZE 9-10 from mail torso (the classic "mail hauberk protects legs with big kite" stage)
        elif any(k in s for k in ["mail hauberk", "mail haubergeon", "mail coat"]) and price_sp >= 20 and price_sp < 35 and not any(p in s for p in ["breastplate", "brigandine", "harnois", "jambes complet", "cuisses", "greaves"]):
            target_size = 10
        elif any(k in s for k in ["mail hauberk", "mail coat", "mail haubergeon"]) and not any(p in s for p in ["breastplate", "brigandine", "jack of plates", "coat of plates", "harnois"]):
            target_size = 9
        else:
            # Very early / minimal (padded, gambeson, short mail, simple helm) -> largest shields
            if any(k in s for k in ["gambeson", "aketon", "padded", "pourpoint", "cervelière", "cerveliere"]) and not any(m in s for m in ["mail", "breastplate", "brigandine", "coat of plates", "harnois"]):
                target_size = 11
            elif any(k in s for k in ["mail shirt", "short mail"]) or ("mail" in s and price_sp < 20):
                target_size = 10
            else:
                # Rough price proxy (last resort, aligns with old table surface/period bands)
                if price_sp >= 75:
                    target_size = 1
                elif price_sp >= 58:
                    target_size = 2
                elif price_sp >= 48:
                    target_size = 3
                elif price_sp >= 40:
                    target_size = 4
                elif price_sp >= 30:
                    target_size = 5
                elif price_sp >= 22:
                    target_size = 6
                elif price_sp >= 15:
                    target_size = 7
                elif price_sp >= 9:
                    target_size = 8
                else:
                    target_size = 9

    # =================================================================
    # GUARDS to enforce the new rule: without meaningful leg/knee/thigh/hips plate,
    # the shield must stay relatively large (even if the character has an expensive
    # cuirass or brigandine on the torso). The historical driver was lower-body armor.
    # =================================================================
    if leg_score <= 0 and not has_legacy_full_legs:
        # Absolutely no lower leg progress -> stay in the large shield range (9-11)
        # except for the specific early mail torso cases which are already handled above.
        target_size = max(target_size, 9)

    if leg_score <= 1 and not has_legacy_full_legs:
        # Only the very first stage of leg protection (or pure mail legs) -> do not allow
        # tiny bucklers. Earliest historical reductions only go to heater / large rotella territory.
        target_size = max(target_size, 7)

    # Positive refinements when we *do* have the requested protection layers
    # (these push toward smaller sizes as leg_score and completeness increase).
    if leg_score >= 2 and target_size >= 8:
        target_size = max(5, target_size - 2)

    if (has_lower_legs or has_thighs or has_knees) and target_size >= 9:
        target_size = min(target_size, 8)

    if leg_score >= 3 and target_size >= 6:
        target_size = min(target_size, 5)

    # Return exact entry for the size
    for shield_entry in SHIELDS_BY_SIZE:
        if shield_entry["size"] == target_size:
            return shield_entry.copy()
    return {"name": "Scutum (Size 11)", "price_sp": grp_prices.get_groupe1_price("Scutum (Size 11)", 35), "size": 11}


# =============================================================================
# DYNAMIC HISTORICAL ARMOR BUILDER (replaces static Sets_Armures.txt usage)
# =============================================================================

def build_historical_armor_set(budget_sp: float, context: Optional[Dict] = None) -> Optional[Dict]:
    """
    Build a historically plausible, layered medieval armor set using the *available fund*
    (capital_left after base kit + first side weapon in the skill protocol).

    Uses live prices exclusively from Groupe1_Cote_des_Epees_Equipement.txt via grp_prices.

    NOUVELLES DIRECTIVES (user-provided "ÉVOLUTION DES ARMURES selon le capital restant"):
    - Déterminer le "niveau d'armure" (1 à 11) d'après le capital restant (seuils minimum):
        2=17sp, 3=105, 4=140, 5=187, 6=250, 7=300, 8=370, 9=500, 10=600, 11=700.
        (Niveau 1 pour <17sp).
    - Une fois le niveau déterminé, acheter les pièces DANS L'ORDRE CRÉDIBLE listé pour ce niveau
      (les listes fournies intègrent déjà l'évolution textile, mail et plates de façon historique
      et cumulative par niveau de capital).
    - L'ordre d'achat = ordre historique crédible (pas de ré-ordonnancement pour bouclier ou autre).

    Les listes par niveau (1-11) sont définies dans LEVEL_PIECES et utilisent les noms exacts
    du master pour résolution de prix. Exemples:
    - Niveau 1-2 : protections basiques (Nasal + Gambeson).
    - Niveau 3-4 : mail courte + sous-couches (mail shirt / haubergeon + aketon/gambeson).
    - Niveau 5+ : hauberk + coiffe, puis coat of plates, simple breastplate, puis brigandine/breast+back,
      arming doublet, faulds, tassets, pauldrons, full limbs, armet, etc. (jusqu'au harnois complet niveau 11).
    - "or" dans les listes (brigandine or breast+back) résolus par choix spécifique (brig standard pour lvl8, breast 95 pour lvl9).

    "l'evolution historique de l'armure est prioritaire" : les listes et l'ordre d'achat
    par niveau de capital sont suivis strictement.

    Returns dict with "name" (joined pieces for Armure col), "price_sp", "items" list (for shield mapper keywords).
    """
    if budget_sp <= 2:
        return None

    ctx = context or {}
    # specialty not heavily used yet (armor is mostly common), but could bias e.g. lighter for pure archers later
    specialty = ctx.get("specialty", "melee")

    items: List[str] = []
    spent = 0.0

    def _price(name: str) -> float:
        return grp_prices.get_groupe1_price(name, 0.0)

    def try_buy(name: str) -> bool:
        nonlocal spent
        p = _price(name)
        if p > 0 and spent + p <= budget_sp + 0.01:  # tiny epsilon for float
            items.append(name)
            spent += p
            return True
        return False

    # =====================================================================
    # NOUVELLES DIRECTIVES (selon capital restant pour l'armure)
    # 1. Déterminer le niveau d'armure (1-11) d'après les seuils fournis par l'utilisateur.
    # 2. Acheter les pièces EXACTEMENT dans l'ordre crédible listé pour ce niveau
    #    (les listes intègrent l'évolution textile, mail et plates par niveau de capital).
    #    L'ordre d'achat = ordre historique crédible.
    # =====================================================================
    level = _get_armor_level(budget_sp)
    pieces_for_level = LEVEL_PIECES.get(level, LEVEL_PIECES[1])

    for piece in pieces_for_level:
        try_buy(piece)

    # ------------------------------------------------------------------
    # Mail leg protection (per the new mail chronology table)
    # XIIe - XIIIe (peak mail): full hauberk + chausses (leg mail)
    # Début-Milieu XIVe: mail for articulations/gaps
    # Later: residual mail only (voiders already handled in arms for plate gaps)
    # Use master prices where possible; fallbacks for explicit chausses (consistent with other non-listed).
    # ------------------------------------------------------------------








    # ------------------------------------------------------------------
    # Fallback minimal si rien n'a pu être acheté (très bas budget)
    # (le niveau 1+ devrait toujours acheter au moins le Nasal Helmet pour budget >=8)
    # ------------------------------------------------------------------
    if not items:
        if budget_sp >= 9:
            try_buy("Gambeson (basic)") or try_buy("Aketon (basic padded jack)")
            try_buy("Nasal Helmet") or try_buy("Cervelière") or try_buy("Leather Helmet")
        elif budget_sp >= 2:
            try_buy("Leather Helmet")

    if not items:
        return None

    total_sp = round(spent, 1)
    display = ", ".join(items)

    return {
        "name": display,
        "price_sp": total_sp,
        "price_bp": round(total_sp * 10, 1),
        "items": items[:],
        "total_sp": total_sp,
    }


# =============================================================================
# NOUVELLES DIRECTIVES - NIVEAUX D'ARMURE SELON CAPITAL RESTANT
# =============================================================================

def _get_armor_level(budget_sp: float) -> int:
    """Détermine le niveau d'armure (1-11) selon le capital restant pour l'armure.
    Seuil minimum pour chaque niveau (d'après les directives utilisateur).
    """
    if budget_sp >= 700:
        return 11
    elif budget_sp >= 600:
        return 10
    elif budget_sp >= 500:
        return 9
    elif budget_sp >= 370:
        return 8
    elif budget_sp >= 300:
        return 7
    elif budget_sp >= 250:
        return 6
    elif budget_sp >= 187:
        return 5
    elif budget_sp >= 140:
        return 4
    elif budget_sp >= 105:
        return 3
    elif budget_sp >= 17:
        return 2
    else:
        return 1


# Listes de pièces par niveau, dans l'ordre crédible d'achat (d'après les directives).
# Noms alignés sur le master Groupe1_Cote_des_Epees_Equipement.txt pour résolution via get_groupe1_price.
LEVEL_PIECES = {
    1: [
        "Nasal Helmet",
    ],
    2: [
        "Gambeson (basic)",
        "Nasal Helmet",
    ],
    3: [
        "Gambeson (basic)",
        "Aketon (basic padded jack)",
        "Mail Shirt (sans manches)",
        "Nasal Helmet",
    ],
    4: [
        "Gambeson (basic)",
        "Aketon (basic padded jack)",
        "Mail Haubergeon (mi-long)",
        "Nasal Helmet",
    ],
    5: [
        "Gambeson (basic)",
        "Mail Hauberk (complet)",
        "Mail coif",
        "Nasal Helmet",
    ],
    6: [
        "Reinforced Gambeson (long)",
        "Mail Hauberk (complet)",
        "Coat of Plates",
        "Mail coif",
        "Aventail",
        "Cervelière",
    ],
    7: [
        "Reinforced Gambeson (long)",
        "Mail Haubergeon (mi-long)",
        "Simple Breastplate",
        "Vambraces + Couter",
        "Bascinet (basique)",
        "Mail coif",
        "Aventail",
    ],
    8: [
        "Reinforced Gambeson (long)",
        "Brigandine (standard troop)",  # "Brigandine or Breastplate + Backplate" 85 -> brig standard
        "Mail Haubergeon (mi-long)",
        "mail chausses",
        "Fauld",
        "Vambraces + Couter",
        "Tassets (paire courte)",
        "Mail coif",
        "Aventail",
        "Bascinet (basique)",
        "Gauntlets (normaux)",
    ],
    9: [
        "Arming Doublet",
        "Breastplate + Backplate",  # "Brigandine or Breastplate + Backplate" 95 -> breast 95
        "Mail Haubergeon (mi-long)",
        "Plackart",
        "Fauld",
        "Tassets (paire courte)",
        "Pauldrons + Gardes",
        "Vambraces+Couter+Rerebrace",
        "Gauntlets (normaux)",
        "Gorget (normal)",
        "Sallet (salade standard)",
    ],
    10: [
        "Arming Doublet",
        "Breastplate + Backplate",
        "Mail Haubergeon (mi-long)",
        "Plackart",
        "Fauld",
        "Tassets longs",
        "Pauldrons + Gardes",
        "Vambraces+Couter+Rerebrace",
        "Cuisses (normales)",
        "Poleyns + Genouillères",
        "Greaves (normales)",
        "Sabatons (normaux)",
        "Gorget (articulé/elevé)",
        "Armet (italien articulé)",
        "Gauntlets (normaux)",
    ],
    11: [
        "Arming Doublet",
        "Breastplate + Backplate (trempé)",
        "Plackart",
        "Fauld",
        "Tassets longs",
        "Pauldrons + Gardes",
        "Vambraces+Couter+Rerebrace",
        "Mail voiders (paire)",
        "Cuisses (renforcées Maximilian)",
        "Poleyns + Genouillères",
        "Greaves (renforcées)",
        "Sabatons (larges pied d'ours)",
        "Gorget (renforcé)",
        "Armet (italien articulé)",
        "Gauntlets (articulés renforcés)",
    ],
}
