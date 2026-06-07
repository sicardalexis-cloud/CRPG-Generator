import sys
sys.path.insert(0, r'c:\Users\sicar\.grok\worktrees\jdr-crpg-generator\premier-tests-grokvsc')
from data.equipment import armor_sets as armor
from data.equipment import groupe1_prices as grp

print('=== DYNAMIC HISTORICAL ARMOR BUILDER TEST ===')
print('Prices come from master via get_groupe1_price')
print()

test_budgets = [5, 12, 25, 45, 70, 95, 130, 180, 250, 380, 520, 850, 1200]
for b in test_budgets:
    res = armor.build_historical_armor_set(b)
    if res:
        print(f'Budget {b:4} sp -> spent {res["price_sp"]:6.1f} sp')
        print(f'  Armure: {res["name"]}')
        print()
    else:
        print(f'Budget {b:4} sp -> (no armor or minimal fallback)')
        print()

print('=== RULE CHECKS (manual spot) ===')
# Low: expect fabric + light helm or short mail
print('Low budget example (should have fabric + basic helm or mail shirt):')
r = armor.build_historical_armor_set(40)
print(' ', r['name'] if r else None)
print()

# Mid: coat or brig + arms if fabric + better helm
print('Mid budget (coat/brigandine + possible arms/gorget):')
r = armor.build_historical_armor_set(140)
print(' ', r['name'] if r else None)
print()

# High: cuirass + limbs + pauldrons (cuirass present) + high helm
print('High budget (cuirass + full limbs + pauldrons?):')
r = armor.build_historical_armor_set(450)
print(' ', r['name'] if r else None)
print('  items:', r.get('items') if r else None)
print()

# Verify a cuirass set has no pauldrons violation (if no cuirass in items, no pauldrons)
print('=== PAULDRONS RULE CHECK (high budget) ===')
r = armor.build_historical_armor_set(600)
if r:
    has_p = any('pauldrons' in i.lower() for i in r.get('items',[]))
    has_c = any('breastplate + backplate' in i.lower() for i in r.get('items',[]))
    print(f'  has_pauldrons={has_p} has_cuirass={has_c}  (if has_p then has_c must be True)')
    print('  ', r['name'][:150])
print('TEST DONE')
