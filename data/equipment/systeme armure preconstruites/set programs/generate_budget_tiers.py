#!/usr/bin/env python3
"""
Generate equipment sets in 10 separate budget tiers (1sp to 2200sp).

This script re-uses the excellent generate_set() logic and formatting
from generate_sets.py (the random full-kit generator with all the
historical armor/weapon/mount compatibility rules).

Output:
  sets_by_budget/
    sets_001-020sp.txt   (compact, easy to parse later)
    sets_001-020sp.md    (pretty tables)
    ...
    README.md            (index of all tiers)

Usage:
  cd "data/equipment/systeme armure preconstruites/set programs"
  python generate_budget_tiers.py
"""

import random
import sys
from pathlib import Path

# Make sure we can import generate_sets.py from the same directory
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    import generate_sets
except ImportError as e:
    print("ERROR: Could not import generate_sets.py from the same folder.")
    print("Make sure generate_sets.py is in this directory.")
    sys.exit(1)

# =============================================================================
# TIER DEFINITIONS
# =============================================================================

TIERS = [
    # (min_sp, max_sp, folder_name, num_sets)
    (1,     20,   "001_Destitute_1-20sp",      45),
    (21,    50,   "002_Poor_21-50sp",          55),
    (51,   100,   "003_Basic_51-100sp",        55),
    (101,  200,   "004_Comfortable_101-200sp", 130),
    (201,  400,   "005_WellOff_201-400sp",     130),
    (401,  700,   "006_Affluent_401-700sp",    120),
    (701, 1100,   "007_Wealthy_701-1100sp",    35),
    (1101,1500,   "008_Rich_1101-1500sp",      30),
    (1501,1800,   "009_VeryRich_1501-1800sp",  25),
    (1801,2200,   "010_Elite_1801-2200sp",     25),
]

OUTPUT_DIR = SCRIPT_DIR.parent / "sets_by_budget"

def human_range(minb: int, maxb: int) -> str:
    return f"{minb}-{maxb} sp"

def make_header(tier_name: str, minb: int, maxb: int, count: int) -> list[str]:
    lines = []
    lines.append("=" * 70)
    lines.append(f"EQUIPMENT SETS — {tier_name}")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Budget range : {human_range(minb, maxb)}")
    lines.append(f"Number of sets : {count}")
    lines.append("Source : generate_sets.py (random realistic kits with compatibility rules)")
    lines.append("Region focus : Sword Coast / Côte des Épées (Groupe 1) — can be adapted")
    lines.append("")
    lines.append("Rules summary (see generate_sets.py for full details):")
    lines.append("  - Weapons & shield chosen first")
    lines.append("  - Strict layering rules (pauldrons require cuirass/breast+backplate; besagews/tassets/fauld require plate torso, etc.)")
    lines.append("  - Bows/crossbows limited to small shields")
    lines.append("  - Mounts + barding appear at higher budgets")
    lines.append("  - 'Nearly full armor' rule downgrades oversized shields")
    lines.append("  - Side weapon (arming sword, falchion, messer or hand axe) bought before any armor")
    lines.append("  - Gorget / Bevor always over at least fabric protection (aketon/gambison/arming doublet); never directly on skin. Often with mail collar underneath too.")
    lines.append("  - Mounted weapons (Light Hammer, Mace, Flanged Mace, Lance) STRICTLY only when a mount is present.")
    lines.append("    Foot characters (no mount) NEVER receive them — absolute, no exceptions even in low tiers.")
    lines.append("")
    return lines

def generate_tier(min_budget: int, max_budget: int, count: int, seed: int) -> list:
    """Generate 'count' sets with budgets uniformly distributed in [min_budget, max_budget]."""
    rng = random.Random(seed)
    budgets = [rng.randint(min_budget, max_budget) for _ in range(count)]
    budgets.sort()

    results = []
    for i, budget in enumerate(budgets, 1):
        equipment, spent = generate_sets.generate_set(budget)
        results.append({
            "set_num": i,
            "budget": budget,
            "equipment": equipment,
            "spent": spent
        })
    return results

def write_compact_file(path: Path, tier_name: str, minb: int, maxb: int, count: int, results: list):
    """Write the compact one-line format (easy for later parsing or the main generator)."""
    lines = make_header(tier_name, minb, maxb, count)
    lines.append("--- COMPACT FORMAT ---")
    lines.append("")

    for r in results:
        compact = generate_sets.format_set_compact(r["set_num"], r["budget"], r["equipment"], r["spent"])
        lines.append(compact)

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Wrote {path.name}")

def write_markdown_file(path: Path, tier_name: str, minb: int, maxb: int, count: int, results: list):
    """Write pretty Markdown with tables (like the original equipment_sets.md)."""
    lines = []
    lines.append(f"# Equipment Sets — {tier_name}")
    lines.append("")
    lines.append(f"**Budget range:** {human_range(minb, maxb)}")
    lines.append(f"**Sets generated:** {count}")
    lines.append("")
    lines.append("## Rules (abridged)")
    lines.append("")
    lines.append("- Order: Weapons & Shield → Helmet → Body Armor → Rest of armor + horse")
    lines.append("- Pauldrons require proper cuirass (Breastplate + Backplate); Besagews / Fauld / Tassets / Garde-reins require plate torso armor")
    lines.append("- Bow or crossbow as primary weapon → shield size ≤ 3")
    lines.append("- 8+ armor pieces → large shields are downgraded")
    lines.append("- Only one shoulder-carried (2h/polearm) weapon per set")
    lines.append("- Mail legs (chausses) can be worn under plate")
    lines.append("- Side weapon (arming sword, falchion, messer or hand axe) is bought before any armor")
    lines.append("- Gorget / Bevor always over at least fabric protection (aketon/gambison/arming doublet); never directly on skin. Often with mail collar underneath too.")
    lines.append("")

    for r in results:
        md_block = generate_sets.format_set(r["set_num"], r["budget"], r["equipment"], r["spent"])
        lines.append(md_block)

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Wrote {path.name}")

def main():
    random.seed(12345)  # overall reproducibility for the whole batch

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(TIERS)} equipment set tiers into:")
    print(f"  {OUTPUT_DIR}")
    print()

    index_lines = ["# Equipment Sets by Budget Tier", ""]
    index_lines.append("These sets were generated with the realistic random kit generator (`generate_sets.py`).")
    index_lines.append("Each tier is self-contained so you can load only the sets appropriate for a character's wealth.")
    index_lines.append("")
    index_lines.append("| Tier | Budget Range | Sets | File (compact) | File (detailed) |")
    index_lines.append("|------|--------------|------|----------------|-----------------|")

    base_seed = 42

    for idx, (minb, maxb, folder_name, count) in enumerate(TIERS):
        tier_seed = base_seed + idx * 1000   # different but reproducible randomness per tier
        tier_name = folder_name.split("_", 1)[1] if "_" in folder_name else folder_name

        print(f"[{idx+1:2d}/10] {tier_name} ({minb}-{maxb} sp) — {count} sets...")

        results = generate_tier(minb, maxb, count, tier_seed)

        # Filenames
        base = f"sets_{minb:03d}-{maxb:03d}sp"
        compact_path = OUTPUT_DIR / f"{base}.txt"
        md_path      = OUTPUT_DIR / f"{base}.md"

        write_compact_file(compact_path, tier_name, minb, maxb, count, results)
        write_markdown_file(md_path, tier_name, minb, maxb, count, results)

        # Index entry
        index_lines.append(
            f"| {idx+1:2d} | {human_range(minb, maxb):>13} | {count:3d} | `{compact_path.name}` | `{md_path.name}` |"
        )

        print()

    # Write index
    index_path = OUTPUT_DIR / "README.md"
    index_lines.append("")
    index_lines.append("## How to use")
    index_lines.append("")
    index_lines.append("The `.txt` files use a very compact format:")
    index_lines.append("  `#001 [275sp] Palfrey, War Saddle, Lance, ...`")
    index_lines.append("")
    index_lines.append("The `.md` files contain the full tables with slot / item / price.")
    index_lines.append("")
    index_lines.append("These are full kits (weapons + armor + horse + accessories) following the same")
    index_lines.append("historical compatibility rules used in the character generator's 3-phase equipment system.")
    index_path.write_text("\n".join(index_lines), encoding="utf-8")
    print(f"Wrote index: {index_path.name}")

    print("\nDone! All tier files are in:")
    print(f"  {OUTPUT_DIR}")

if __name__ == "__main__":
    main()