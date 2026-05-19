import random
import statistics
from collections import Counter

from race_data import ethnicity_data
from ethnicity_weights import category_weights, ethnicity_weights
from utils import generate_character


def simulate_top_ethnicities(n: int = 50000):
    print(f"Simulation de {n:,} personnages en cours...\n")
    
    stats = {}
    count = Counter()
    
    for i in range(n):
        char = generate_character(f"SIM-{i}")
        eth = char["Ethnicity"]
        count[eth] += 1
        
        if eth not in stats:
            stats[eth] = {
                "tcb": [], "grapple": [], "melee": [], 
                "fencing": [], "projectiles": []
            }
        
        stats[eth]["tcb"].append(char["Combat_Points"])
        stats[eth]["grapple"].append(char["Grappling"])
        stats[eth]["melee"].append(char["Melee"])
        stats[eth]["fencing"].append(char["Fencing"])
        stats[eth]["projectiles"].append(char["Projectiles"])
    
    # Top 30 les plus fréquents
    top = count.most_common(30)
    
    print(f"{'Rang':<3} {'Ethnie':<30} {'Fréquence':<8} {'%':<7} {'TCB Moy':<9} {'Grap':<7} {'Melee':<7} {'Fence':<7} {'Proj':<7}")
    print("-" * 110)
    
    for rank, (eth, freq) in enumerate(top, 1):
        s = stats[eth]
        tcb_mean = statistics.mean(s["tcb"])
        print(f"{rank:<3} {eth:<30} {freq:<8} {(freq/n*100):6.2f}%  {tcb_mean:7.2f}   "
              f"{statistics.mean(s['grapple']):6.2f}  "
              f"{statistics.mean(s['melee']):6.2f}  "
              f"{statistics.mean(s['fencing']):6.2f}  "
              f"{statistics.mean(s['projectiles']):6.2f}")
    
    print(f"\n→ TCB le plus élevé parmi les 30 : {max(statistics.mean(s['tcb']) for s in stats.values()):.2f}")


if __name__ == "__main__":
    random.seed(42)   # Pour des résultats reproductibles
    simulate_top_ethnicities(n=50000)   # Tu peux mettre 100000 pour plus de précision