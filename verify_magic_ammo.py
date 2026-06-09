#!/usr/bin/env python
"""Quick verification for the new magic light projectile filtering rule."""
import random
from utils import generate_character, _kit_has_projectile_weapon, _is_magic_light_projectile, _get_ranged_ammo_types, _is_magic_item_allowed_for_kit

random.seed(12345)

def has_ranged_in_kit(kit_items):
    if not kit_items:
        return False
    return _kit_has_projectile_weapon({"items": kit_items})

def analyze_char(c):
    kit_items = c.get("Prebuilt_Kit_Items", []) or []
    has_ranged = has_ranged_in_kit(kit_items)
    ranged_types = _get_ranged_ammo_types({"items": kit_items}) if kit_items else set()

    magic_list = c.get("Starting_Magic_Items", []) or []
    magic_proj = [m for m in magic_list if _is_magic_light_projectile(m)]

    # Check correctness
    violations = []
    for mp in magic_proj:
        name_lower = mp.lower()
        allowed = _is_magic_item_allowed_for_kit({"name": mp.split(" (")[0]}, {"items": kit_items} if kit_items else None)
        if not allowed:
            violations.append(mp)

    return {
        "id": c["ID"],
        "kit_preview": (", ".join(kit_items[:3]) + ("..." if len(kit_items) > 3 else "")) if kit_items else "Aucun",
        "has_ranged": has_ranged,
        "ranged_types": sorted(ranged_types),
        "magic_proj": magic_proj,
        "violations": violations,
        "all_magic": magic_list,
    }

print("=== Generating 8 characters (seed 12345) to test magic ammo filtering ===\n")
results = []
for i in range(8):
    c = generate_character(f"VERIF{i:02d}")
    res = analyze_char(c)
    results.append(res)

for r in results:
    print(f"{r['id']}: ranged={r['has_ranged']} types={r['ranged_types']}")
    print(f"   kit: {r['kit_preview']}")
    print(f"   magic_proj: {r['magic_proj'] or '(none)'}")
    if r['violations']:
        print(f"   !! VIOLATIONS: {r['violations']}")
    print()

# Summary
total_viol = sum(len(r['violations']) for r in results)
any_proj = sum(1 for r in results if r['magic_proj'])
print(f"=== SUMMARY ===")
print(f"Characters with magic light projectiles: {any_proj}/8")
print(f"Total rule violations: {total_viol}")
if total_viol == 0:
    print("SUCCESS: All selected magic projectiles respect the no-ranged / matching-ammo rule.")
else:
    print("FAIL: Some violations detected.")

# Also test the helpers directly on a couple of simulated kits
print("\n=== Direct helper tests ===")
test_kits = [
    ({"items": ["Longbow", "Arrows (12)", "Dagger"]}, "bow kit"),
    ({"items": ["Light Crossbow", "Crossbow Bolts (20)", "Short Sword"]}, "crossbow kit"),
    ({"items": ["Sling", "Sling Bullets (10)", "Dagger"]}, "sling kit"),
    ({"items": ["Javelins (3)", "Shield", "Spear"]}, "javelin kit (ranged)"),
    ({"items": ["Arming Sword", "Heater Shield", "Dagger"]}, "pure melee kit"),
    ({"items": ["Quarterstaff", "Darts (5)"]}, "dart kit"),
]

for kit, label in test_kits:
    has_r = _kit_has_projectile_weapon(kit)
    types = _get_ranged_ammo_types(kit)
    print(f"{label}: has_ranged={has_r}, types={sorted(types)}")

    candidates = [
        "Arrows +1 (Uncommon)",
        "Crossbow Bolts +1 (Uncommon)",
        "Sling Bullets +1 (Uncommon)",
        "Javelins +1 (Uncommon)",
        "Darts +1 (Uncommon)",
    ]
    allowed = []
    disallowed = []
    for c in candidates:
        if _is_magic_item_allowed_for_kit({"name": c}, kit):
            allowed.append(c)
        else:
            disallowed.append(c)
    print(f"   allowed: {allowed}")
    print(f"   disallowed: {disallowed}")
    print()

print("Verification script finished.")