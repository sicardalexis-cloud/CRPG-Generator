import re
from pathlib import Path
import statistics

files = {
    'default': 'data/equipment/systeme armure preconstruites/100_kits_XV_siecle_Cote_des_Epees_EN (1).txt',
    'mage': 'data/equipment/systeme armure preconstruites/100_Magician_Kits .txt',
    'druid': 'data/equipment/systeme armure preconstruites/100_Kits_Druide_Complete_100kits.txt'
}

kit_line_re = re.compile(r'^(\d+(?:\.\d+)?)\s*sp\s*-\s*Kit\s*(\d+)', re.IGNORECASE)

for name, path_str in files.items():
    p = Path(path_str)
    prices = []
    if not p.exists():
        print(name + ': FILE NOT FOUND')
        continue
    for line in p.read_text(encoding='utf-8').splitlines():
        m = kit_line_re.match(line.strip())
        if m:
            prices.append(float(m.group(1)))
    if prices:
        prices.sort()
        n = len(prices)
        med = statistics.median(prices)
        p75 = prices[int(0.75 * n)]
        p90 = prices[int(0.90 * n)]
        print(name.upper() + ': ' + str(n) + ' kits')
        print('  min=' + str(min(prices)) + ' max=' + str(max(prices)) + ' median=' + str(med))
        print('  75pct=' + str(p75) + ' 90pct=' + str(p90))
        print('  <=50sp: ' + str(sum(p <= 50 for p in prices)))
        print('  <=150sp: ' + str(sum(p <= 150 for p in prices)))
        print('  <=400sp: ' + str(sum(p <= 400 for p in prices)))
        print('  <=700sp: ' + str(sum(p <= 700 for p in prices)))
        print('  >900sp: ' + str(sum(p > 900 for p in prices)))
        print()
    else:
        print(name + ': 0 kits matched regex')
