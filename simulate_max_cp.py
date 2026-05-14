# simulate_max_cp.py
import random
from race_data import ethnicity_data
from utils import generate_character  # on réutilise ta fonction existante

def simulate_max_cp_per_ethnie(nb_simulations=10000):
    print(f"Simulation de {nb_simulations:,} personnages par ethnie en cours...\n")
    
    results = []

    for eth_name, data in ethnicity_data.items():
        max_tcb = float('-inf')
        best_char = None

        for i in range(nb_simulations):
            # On force l'ethnie
            char = generate_character(f"SIM-{i}")
            # On remplace l'ethnie générée par celle qu'on veut tester
            char["Ethnicity"] = eth_name
            char["Race"] = data["r"]
            
            tcb = char["Combat_Points"]
            
            if tcb > max_tcb:
                max_tcb = tcb
                best_char = char

        results.append({
            "Ethnie": eth_name,
            "Race": data["r"],
            "Max_TCB": round(max_tcb, 2),
            "Idx": data["idx"]
        })

        print(f"→ {eth_name:30} | Max TCB = {round(max_tcb, 2):6.2f}")

    # Tri par Max TCB descendant
    results.sort(key=lambda x: x["Max_TCB"], reverse=True)

    print("\n" + "="*80)
    print("CLASSEMENT FINAL - MAXIMUM TCB PAR ETHNIE")
    print("="*80)
    for r in results:
        print(f"{r['Idx']:3d} | {r['Ethnie']:35} | {r['Race']:12} | Max TCB = {r['Max_TCB']:6.2f}")

    return results


if __name__ == "__main__":
    random.seed(42)          # pour reproductibilité
    simulate_max_cp_per_ethnie(nb_simulations=20000)   # tu peux monter à 50000+ si tu veux plus de précision