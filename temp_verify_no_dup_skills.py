import random
from collections import Counter
from skill_data import generate_skills

print("=== Verification after fix ===")

# Test urban (high count case - most likely to duplicate before)
random.seed(42)
urban_dup = 0
outdoor_dup = 0
examples = []
for i in range(400):
    res = generate_skills('Metropolis', region_id=10, ethnicity='Calishite')
    u = res['urban_skills']
    o = res['outdoor_skills']
    if len(u) != len(set(u)):
        urban_dup += 1
        if not examples: examples.append(('URBAN', u))
    if len(o) != len(set(o)):
        outdoor_dup += 1
        if not examples: examples.append(('OUTDOOR', o))

print(f'After fix - 400 Metropolis gens: urban_dups={urban_dup}, outdoor_dups={outdoor_dup}')
if examples:
    print('  First example of issue (should be none):', examples[0])
else:
    print('  No problematic examples — good.')

# Rural high outdoor count
random.seed(123)
urban_dup = 0
outdoor_dup = 0
for i in range(400):
    res = generate_skills('Forest Village', region_id=7, ethnicity='Wood Elf')
    u = res['urban_skills']
    o = res['outdoor_skills']
    if len(u) != len(set(u)): urban_dup += 1
    if len(o) != len(set(o)): outdoor_dup += 1

print(f'After fix - 400 rural gens:   urban_dups={urban_dup}, outdoor_dups={outdoor_dup}')

print()
print('If both counters are 0, duplicates are now impossible for fresh generations.')
print('Old CSVs may still contain them (they were generated before the fix).')
