import sys, random
sys.path.insert(0, r'c:\Users\sicar\.grok\worktrees\jdr-crpg-generator\premier-tests-grokvsc')
from utils import generate_character

print("=== PROTOCOL + BUILDER + NEW LEG-DRIVEN SHIELD TEST (melee focused) ===\n")
print("We force melee by giving high Melee score via monkey-patch on the fly if needed.\n")

# To see the progression clearly we generate several and also manually inspect
# the internal armor + shield choice isn't directly exposed, but the final
# "Armes_et_Bouclier" will show the reduced shield name for melee chars.

random.seed(1234)

results = []
for i in range(8):
    c = generate_character(f"CH-LEG-{i:02d}")
    results.append(c)

for c in results:
    cap = c["Starting_Capital"]
    armes = c["Armes_et_Bouclier"]
    armure = c["Armure"]
    is_melee = c["Melee"] >= c["Projectiles"]
    shield_in_armes = None
    for sz_name in ["Scutum (Size 11)", "Kite Shield (Size 10)", "Velites Parma (Size 9)",
                    "Heater Shield (Size 8)", "Large Rotella (Size 7)", "Rotella (Size 6)",
                    "Small Rotella (Size 5)", "Large Buckler (Size 4)", "Buckler (Size 3)",
                    "Small Buckler (Size 2)", "Brocchiere (Size 1)"]:
        if sz_name.split(" (")[0] in armes or sz_name in armes:
            shield_in_armes = sz_name
            break
    # Detect lower body indicators in the final Armure string
    arm_lower = armure.lower()
    has_g = any(x in arm_lower for x in ["greaves", "schynbald"])
    has_p = "poleyn" in arm_lower
    has_c = "cuisses" in arm_lower
    has_t = "tassets" in arm_lower
    has_f = any(x in arm_lower for x in ["fauld", "garde-reins"])
    has_s = "sabatons" in arm_lower
    leg_bits = []
    if has_g: leg_bits.append("G")
    if has_p: leg_bits.append("P")
    if has_c: leg_bits.append("C")
    if has_t: leg_bits.append("T")
    if has_f: leg_bits.append("F")
    if has_s: leg_bits.append("S")
    leg_str = "".join(leg_bits) if leg_bits else "none"
    print(f"Cap {cap:5.0f} | Melee? {is_melee} | LegBits:{leg_str:6} | Shield: {shield_in_armes or 'N/A (proj?)'}")
    print(f"         Armure: {armure[:110]}...")
    print()

print("Look for: as more 'Greaves / Poleyns / Cuisses / Tassets longs / Fauld / Garde-reins / Sabatons' appear in Armure,")
print("the shield in Armes_et_Bouclier should get smaller (Size 11 -> ... -> 1).")
print("=== DONE ===")
