# simulate_max_cp.py
import random
from race_data import ethnicity_data

from utils import roll_6d6
from rules import (
    calculate_weight,
    calculate_height,
    calculate_size_score,
    calculate_grappling,
    calculate_melee,
    calculate_fencing,
    calculate_projectiles,
    calculate_combat_points
)


def simulate_max_cp_per_ethnie(nb_simulations=20000):
    print(f"Simulation de {nb_simulations:,} personnages par ethnie...\n")
    
    results = []

    for eth_name, data in ethnicity_data.items():
        max_tcb = float('-inf')

        w_mod = data.get("w", 0)
        b_mod = data.get("b", 0)
        bal_mod = data.get("bal", 0)
        qui_mod = data.get("spd", 0)
        coo_mod = data.get("coo", 0)
        pre_mod = data.get("pre", 0)

        for _ in range(nb_simulations):
            weight_score = roll_6d6() - 21 + w_mod
            build_score  = roll_6d6() - 21 + b_mod
            balance      = roll_6d6() - 21 + bal_mod
            quickness    = roll_6d6() - 21 + qui_mod
            coordination = roll_6d6() - 21 + coo_mod
            precision    = roll_6d6() - 21 + pre_mod

            weight_kg = calculate_weight(weight_score)
            height_cm = calculate_height(weight_kg, build_score)
            size_score = calculate_size_score(height_cm)

            # Combat capacities
            grappling   = calculate_grappling(weight_score, balance, quickness)
            melee       = calculate_melee(weight_score, size_score, coordination, balance, quickness)
            projectiles = calculate_projectiles(precision)
            fencing     = calculate_fencing(size_score, weight_score, coordination, quickness, balance)

            tcb = calculate_combat_points(grappling, melee, projectiles, fencing)
            tcb += data.get("cp", 0.0)

            if tcb > max_tcb:
                max_tcb = tcb

        results.append({
            "Idx": data.get("idx", 999),
            "Ethnie": eth_name,
            "Race": data.get("r", "Inconnu"),
            "Max_TCB": round(max_tcb, 2)
        })

        print(f"→ {eth_name:32} | Max TCB = {round(max_tcb, 2):6.2f}")

    results.sort(key=lambda x: x["Max_TCB"], reverse=True)

    print("\n" + "="*100)
    print("CLASSEMENT FINAL - MAX TCB PAR ETHNIE")
    print("="*100)
    for r in results[:30]:
        print(f"{r['Idx']:3d} | {r['Ethnie']:35} | {r['Race']:12} | Max TCB = {r['Max_TCB']:6.2f}")


if __name__ == "__main__":
    random.seed(42)
    simulate_max_cp_per_ethnie(nb_simulations=20000)