import sys
sys.path.insert(0, r'c:\Users\sicar\.grok\worktrees\jdr-crpg-generator\premier-tests-grokvsc')
from utils import generate_character

print('=== RUNNING SMALL GENERATION WITH NEW BUILDER (direct utils) ===')
chars = []
for i in range(1,6):
    c = generate_character(f"CH-TEST{i:03d}")
    chars.append(c)

print('Generated', len(chars), 'chars')
print()

for c in chars:
    print('--- CHAR', c['ID'], '---')
    print('Starting_Capital:', c.get('Starting_Capital'))
    print('Melee / Projectiles:', round(c.get('Melee',0),1), '/', round(c.get('Projectiles',0),1))
    print('Armes_et_Bouclier :', c.get('Armes_et_Bouclier'))
    print('Armure            :', c.get('Armure'))
    print('Phase2_Armor_Cost_BP:', c.get('Phase2_Armor_Cost_BP'))
    print('Phase3_Mount      :', c.get('Phase3_Mount'))
    print('Final_Pocket      :', c.get('Final_Pocket_Money_BP'))
    print('Equipment_Source  :', c.get('Equipment_Source'))
    print()

print('=== ALL OK (no crash, builder integrated, historical sets built live) ===')
