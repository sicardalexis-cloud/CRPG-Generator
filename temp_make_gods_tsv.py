#!/usr/bin/env python3
"""Generate gods_by_region.tsv and gods_by_ethnie.tsv from the raw hierarchy sources."""
import csv
import os
import re
from collections import OrderedDict

magic_dir = os.path.join("data", "magic")
os.makedirs(magic_dir, exist_ok=True)

def parse_region_file(path):
    data = OrderedDict()
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split("\t") if p.strip()]
        if len(parts) < 3:
            continue
        # label after the leading number
        label = parts[1] if parts[0].isdigit() and len(parts) > 1 else parts[0]
        gods = []
        for p in parts[2:]:
            if p and len(p) > 1 and not p.isdigit():
                gods.append(p)
            if len(gods) >= 20:
                break
        if not gods:
            continue
        key = label
        m = re.search(r"\(([^)]+)\)", label)
        if m:
            key = m.group(1).strip()
        if key not in data:
            seen = set()
            uniq = []
            for g in gods:
                if g not in seen:
                    seen.add(g)
                    uniq.append(g)
            data[key] = uniq
    return data

def parse_ethnie_file(path):
    data = OrderedDict()
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split("\t") if p.strip()]
        if len(parts) < 2:
            continue
        eth = parts[0]
        # skip header-like or numeric junk
        if not eth or eth[0].isdigit() and len(eth) < 4:
            continue
        gods = []
        for p in parts[1:]:
            if p and len(p) > 1 and not p.isdigit():
                gods.append(p)
            if len(gods) >= 20:
                break
        if not gods:
            continue
        key = eth
        if key not in data:
            seen = set()
            uniq = []
            for g in gods:
                if g not in seen:
                    seen.add(g)
                    uniq.append(g)
            data[key] = uniq
    return data

reg_path = os.path.join(magic_dir, "gods par region.txt")
eth_path = os.path.join(magic_dir, "gods par ethnie.txt")

reg_data = parse_region_file(reg_path)
eth_data = parse_ethnie_file(eth_path)

reg_tsv = os.path.join(magic_dir, "gods_by_region.tsv")
with open(reg_tsv, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["region", "god"])
    for k, glist in reg_data.items():
        for g in glist:
            w.writerow([k, g])
print(f"Wrote {reg_tsv} with {len(reg_data)} region entries, {sum(len(v) for v in reg_data.values())} total rows")

eth_tsv = os.path.join(magic_dir, "gods_by_ethnie.tsv")
with open(eth_tsv, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["ethnicity", "god"])
    for k, glist in eth_data.items():
        for g in glist:
            w.writerow([k, g])
print(f"Wrote {eth_tsv} with {len(eth_data)} ethnie entries, {sum(len(v) for v in eth_data.values())} total rows")

print("Sample regions:", list(reg_data.keys())[:6])
print("Sample ethnies:", list(eth_data.keys())[:6])
print("Done.")
