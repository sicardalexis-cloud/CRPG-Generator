import sys
sys.path.insert(0, r"c:\Users\sicar\.grok\worktrees\jdr-crpg-generator\premier-tests-grokvsc")
from data.equipment import armor_sets as a
print("=== Test new level-based armor builder (nouvelles directives) ===")
test_budgets = [10, 20, 50, 100, 150, 200, 300, 400, 550, 650, 750, 1200]
for b in test_budgets:
    res = a.build_historical_armor_set(b)
    if res:
        print(f"Budget {b} sp (level ~{a._get_armor_level(b)}) -> spent {res['price_sp']:.1f}")
        print(f"  Pieces: {res['items'][:6]}...")
        print()
print("Test complete.")