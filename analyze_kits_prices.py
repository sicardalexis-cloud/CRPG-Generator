import re

with open("data/equipment/systeme armure preconstruites/kits_armes_et_boucliers.txt", encoding="utf-8") as f:
    text = f.read()

prices = [float(m) for m in re.findall(r"(\d+\.\d+)\s*sp", text)]
print(f"Nombre de kits trouvés : {len(prices)}")
print(f"Prix minimum : {min(prices)} sp")
print(f"Prix maximum : {max(prices)} sp")
print(f"Prix médian : {sorted(prices)[len(prices)//2]} sp")
print(f"Prix moyen : {sum(prices)/len(prices):.2f} sp")
