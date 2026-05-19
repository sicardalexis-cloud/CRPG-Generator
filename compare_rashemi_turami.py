# compare_rashemi_turami.py
import random

from race_data import ethnicity_data
from utils import generate_character


def compare_rashemi_turami(n=30000):
    print(f"Comparaison forcée Rashemi vs Turami ({n} personnages chacun)\n")
    
    tcb_rashemi = []
    tcb_turami = []
    
    for i in range(n):
        # Force Rashemi
        char1 = generate_character(f"SIM-R-{i}")
        char1["Ethnicity"] = "Rashemi"
        char1["Race"] = ethnicity_data["Rashemi"]["r"]
        tcb_rashemi.append(char1["Combat_Points"])
        
        # Force Turami
        char2 = generate_character(f"SIM-T-{i}")
        char2["Ethnicity"] = "Turami"
        char2["Race"] = ethnicity_data["Turami"]["r"]
        tcb_turami.append(char2["Combat_Points"])
    
    avg_r = sum(tcb_rashemi) / n
    avg_t = sum(tcb_turami) / n
    
    print(f"Rashemi     → Moyenne TCB : {avg_r:.3f}")
    print(f"Turami      → Moyenne TCB : {avg_t:.3f}")
    print(f"Différence  : {avg_r - avg_t:+.3f} en faveur des Rashemi")
    
    return avg_r, avg_t


if __name__ == "__main__":
    random.seed(42)
    compare_rashemi_turami(n=30000)   # Tu peux monter à 50000 ou 100000