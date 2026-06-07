"""
data/equipment/groupe1_prices.py

Single source of truth for equipment prices: parses the master list
Groupe1_Cote_des_Epees_Equipement.txt (Bloc Côte des Épées / Sword Coast prices).

All equipment prices in the generator (protocol base kits, mounts, etc.)
should now be looked up here instead of being hardcoded.

Usage:
    from data.equipment import groupe1_prices as prices
    price = prices.get_groupe1_price("Scutum (Size 11)")
"""

from pathlib import Path
from typing import Dict, Optional
import re

BASE_DIR = Path(__file__).parent
PRICE_FILE = BASE_DIR / "systeme armure preconstruites" / "Groupe1_Cote_des_Epees_Equipement.txt"

_PRICE_CACHE: Optional[Dict[str, float]] = None


def _normalize_name(name: str) -> str:
    """Basic normalization for matching."""
    name = name.strip()
    # Remove common prefixes from the matrix section
    name = re.sub(r'^SIZE\s*\d+:\s*', '', name, flags=re.IGNORECASE).strip()
    return name


def _load_groupe1_prices() -> Dict[str, float]:
    """Parse the master price file into a lookup dict (name -> price in sp)."""
    global _PRICE_CACHE
    if _PRICE_CACHE is not None:
        return _PRICE_CACHE

    prices: Dict[str, float] = {}
    if not PRICE_FILE.exists():
        print(f"WARNING: Master price file not found: {PRICE_FILE}")
        _PRICE_CACHE = prices
        return prices

    text = PRICE_FILE.read_text(encoding="utf-8", errors="ignore")

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith('=') or line.startswith('#'):
            continue

        # Find price: number followed by sp (possibly after | or spaces)
        price_match = re.search(r'(\d+(?:\.\d+)?)\s*sp\b', line, re.IGNORECASE)
        if not price_match:
            continue

        price_sp = float(price_match.group(1))

        # Extract the name: everything before the price number
        # Split on the matched price occurrence
        before_price = line[:price_match.start()].strip()

        # Clean common artifacts
        # For lines like "Knife (couteau)               6 sp"
        # before_price will be "Knife (couteau)"
        name = _normalize_name(before_price)

        # Remove trailing colons, dashes, etc.
        name = re.sub(r'[:\-\s]+$', '', name).strip()

        if name:
            # Store under the cleaned name
            prices[name] = price_sp
            # Also store lowercased for case-insensitive lookup
            prices[name.lower()] = price_sp

            # Special: store the shield matrix variants without " (9650 cm²)" etc.
            # e.g. also "Scutum" and "Scutum (Size 11)"
            if "Scutum" in name or "Velites Parma" in name or "Kite Shield" in name or "Heater Shield" in name or "Rotella" in name or "Buckler" in name or "Brocchiere" in name:
                base = re.sub(r'\s*\([^)]*\)\s*$', '', name).strip()
                if base and base != name:
                    prices[base] = price_sp
                    prices[base.lower()] = price_sp

    _PRICE_CACHE = prices
    return prices


def get_groupe1_price(name: str, default: float = 0.0) -> float:
    """
    Return price in silver pieces (sp) for the given item name from the master list.

    Tries exact match, case-insensitive, and some fuzzy matches (contains / base name).
    Returns `default` (0.0) if not found.
    """
    if not name:
        return default

    prices = _load_groupe1_prices()

    # Direct
    if name in prices:
        return prices[name]

    lower = name.lower()
    if lower in prices:
        return prices[lower]

    # Protocol uses friendly names like "Scutum (Size 11)", "Velites Parma (Size 9)" etc.
    # Map them to the matrix entries in the source file.
    protocol_aliases = {
        "scutum (size 11)": "Scutum",
        "velites parma (size 9)": "Velites Parma",
        "kite shield (size 10)": "Kite Shield",
        "heater shield (size 8)": "Heater Shield",
        "large rotella (size 7)": "Large Rotella",
        "rotella (size 6)": "Rotella",
        "small rotella (size 5)": "Small Rotella",
        "large buckler (size 4)": "Large Buckler",
        "buckler (size 3)": "Buckler",
        "small buckler (size 2)": "Small Buckler",
        "brocchiere (size 1)": "Brocchiere",
    }
    alias_key = lower
    if alias_key in protocol_aliases:
        alias_target = protocol_aliases[alias_key]
        if alias_target in prices:
            return prices[alias_target]
        if alias_target.lower() in prices:
            return prices[alias_target.lower()]

    # Try without parenthetical size info for our protocol shields (Size 11 etc.)
    cleaned = re.sub(r'\s*\(Size\s*\d+\)\s*', '', name, flags=re.IGNORECASE).strip()
    if cleaned in prices:
        return prices[cleaned]
    if cleaned.lower() in prices:
        return prices[cleaned.lower()]

    # Also try stripping any (.... cm²) or similar from matrix
    cleaned2 = re.sub(r'\s*\([^)]*cm²[^)]*\)\s*', '', name, flags=re.IGNORECASE).strip()
    if cleaned2 in prices:
        return prices[cleaned2]
    if cleaned2.lower() in prices:
        return prices[cleaned2.lower()]

    # Fuzzy: exact base name match for shields
    for key in list(prices.keys()):
        if key.lower() == lower or key.lower() == cleaned.lower() or key.lower() == cleaned2.lower():
            return prices[key]

    # Last resort: substring match (first match wins)
    for key, val in prices.items():
        if lower in key.lower() or key.lower() in lower:
            return val

    return default


def get_all_prices() -> Dict[str, float]:
    """Return a copy of the full price cache (for debugging / regeneration)."""
    return dict(_load_groupe1_prices())


if __name__ == "__main__":
    print("Testing Groupe1 price loader...")
    tests = [
        "Scutum (Size 11)",
        "Scutum",
        "Velites Parma (Size 9)",
        "Short bow",
        "Longbow",
        "Spear",
        "Club",
        "Knife (couteau)",
        "Hand Axe",
        "Arrows (paire de 12 / carquois plein)",
        "Rouncey",
        "Destrier (quality)",
    ]
    for t in tests:
        p = get_groupe1_price(t)
        print(f"  {t!r}: {p} sp")
    print(f"\nTotal unique items loaded: {len(get_all_prices()) // 2}")  # /2 because we store lower too
