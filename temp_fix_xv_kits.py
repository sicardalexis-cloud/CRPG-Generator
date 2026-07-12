#!/usr/bin/env python3
"""Clean inline # comments from kit lines and renumber kits sequentially."""
import re
from pathlib import Path

FILE = Path(__file__).parent / (
    "data/equipment/systeme armure preconstruites/"
    "100_kits_XV_siecle_Cote_des_Epees_EN (1).txt"
)

KIT_LINE_RE = re.compile(
    r'^(\d+(?:\.\d+)?)\s*sp\s*-\s*Kit\s*(\d+|XX)\s*-\s*(.*?)\s*:\s*(.*)$',
    re.IGNORECASE,
)


def clean_items_part(items: str) -> str:
    """Remove inline comments; recover Knife/Dagger listed after the comment marker."""
    if "#" not in items:
        return items.strip()

    hash_idx = items.find(" #")
    if hash_idx < 0:
        hash_idx = items.find("   #")
    if hash_idx < 0:
        return items.strip()

    before = items[:hash_idx].rstrip()
    comment = items[hash_idx + 1 :].lstrip("#").strip()

    trailing = re.search(
        r",\s*((?:Knife|Dagger)\s*\(\d+(?:\.\d+)?\))\s*$",
        comment,
        re.IGNORECASE,
    )
    if trailing:
        before = f"{before}, {trailing.group(1)}"

    return before.strip()


def format_kit_num(n: int) -> str:
    if n < 100:
        return f"{n:02d}"
    return str(n)


def main() -> None:
    text = FILE.read_text(encoding="utf-8")
    lines = text.splitlines()
    out: list[str] = []
    kit_counter = 0

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("="):
            out.append(line)
            continue
        if stripped.startswith("#"):
            out.append(line)
            continue
        if " sp - Kit " not in stripped:
            out.append(line)
            continue

        m = KIT_LINE_RE.match(stripped)
        if not m:
            out.append(line)
            continue

        kit_counter += 1
        price, _old_num, desc, items = m.groups()
        items_clean = clean_items_part(items)
        new_num = format_kit_num(kit_counter)
        out.append(f"{price} sp - Kit {new_num} - {desc.strip()} : {items_clean}")

    FILE.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Done: {kit_counter} kits renumbered Kit 01..Kit {format_kit_num(kit_counter)}")


if __name__ == "__main__":
    main()