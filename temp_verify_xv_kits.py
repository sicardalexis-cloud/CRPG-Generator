import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

p = ROOT / "data/equipment/systeme armure preconstruites/100_kits_XV_siecle_Cote_des_Epees_EN (1).txt"
text = p.read_text(encoding="utf-8")
kit_re = re.compile(r"^(\d+(?:\.\d+)?)\s*sp\s*-\s*Kit\s*(\d+)\s*-\s*(.*?)\s*:\s*(.*)$", re.I)
nums = []
failed = []
for line in text.splitlines():
    s = line.strip()
    if " sp - Kit " not in s:
        continue
    m = kit_re.match(s)
    if not m:
        failed.append(s[:100])
    else:
        nums.append(int(m.group(2)))

from utils import load_100_kits_file

kits = load_100_kits_file(p)
bad = [
    k["kit_id"]
    for k in kits
    if any("limbs" in it.lower() or "sidearm" in it.lower() for it in k["items"])
]

out = [
    f"parsed_lines={len(nums)}",
    f"failed_lines={len(failed)}",
    f"duplicates={[n for n, c in Counter(nums).items() if c > 1]}",
    f"range={min(nums)}-{max(nums)} unique={len(set(nums))}",
    f"load_100_kits_file={len(kits)}",
    f"polluted_kits={bad}",
]
(ROOT / "temp_verify_out.txt").write_text("\n".join(out), encoding="utf-8")