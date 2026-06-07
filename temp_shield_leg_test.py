import sys
sys.path.insert(0, r'c:\Users\sicar\.grok\worktrees\jdr-crpg-generator\premier-tests-grokvsc')
from data.equipment import armor_sets as armor

print("=== SHIELD SIZE REDUCTION UPGRADE TEST (legs, knee, thigh, hips order) ===\n")

def analyze(armor_res, label):
    if not armor_res:
        print(label, "-> no armor")
        return
    shield = armor.get_shield_for_armor_level(armor_res)
    items = armor_res.get("items", [])
    leg_pieces = [i for i in items if any(x in i.lower() for x in ["cuisse","greave","poleyn","tasset","fauld","garde-rein","sabat","schynbald"])]
    print(f"{label}")
    print(f"  Armor spent: {armor_res['price_sp']:.1f} sp")
    print(f"  Key leg/hip pieces: {leg_pieces or '(none)'}")
    print(f"  -> Shield: {shield['name']} (Size {shield['size']})")
    print()

# Low budgets - expect large shields (little/no leg plate)
for b in [20, 50, 90]:
    res = armor.build_historical_armor_set(b, {"specialty": "melee"})
    analyze(res, f"Budget ~{b} (early / minimal leg)")

print("--- Mid (expect Size 6-8, first greaves or basic cuisses) ---")
for b in [140, 200, 280]:
    res = armor.build_historical_armor_set(b, {"specialty": "melee"})
    analyze(res, f"Budget ~{b}")

print("--- High (expect Size 3-5 : thighs + knees + greaves, emerging hips) ---")
for b in [380, 520]:
    res = armor.build_historical_armor_set(b, {"specialty": "melee"})
    analyze(res, f"Budget ~{b}")

print("--- Very high / rich (expect Size 1-2 : full legs + knee + thigh + hips/basin + sabatons) ---")
for b in [750, 1100]:
    res = armor.build_historical_armor_set(b, {"specialty": "melee"})
    analyze(res, f"Budget ~{b}")

print("--- Legacy string tests (old set names) ---")
legacy_tests = [
    ("Old minimal padded + short mail", {"name": "Padded Jack + Mail Shirt", "price_sp": 90, "items": []}),
    ("Old coat of plates + greaves start", {"name": "Coat of Plates + Greaves", "price_sp": 70, "items": []}),
    ("Old full harnois with jambes", {"name": "Harnois Gothic + Jambes complètes + Cuisses + Grèves", "price_sp": 180, "items": []}),
    ("Old brigandine + basic leg", {"name": "Brigandine + Jambes", "price_sp": 110, "items": []}),
]
for label, fake in legacy_tests:
    sh = armor.get_shield_for_armor_level(fake)
    print(f"  {label} -> Size {sh['size']} ({sh['name']})")

print("\n=== TEST COMPLETE ===")
print("Expected trend: higher leg/knee/thigh/hip plate completeness in the builder output -> progressively smaller Size (11 -> 1)")
