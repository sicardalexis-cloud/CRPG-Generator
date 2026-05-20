# simulate_ethnicity_distribution.py
# Simulation de distribution + Calcul de seuils magiques

import random
from collections import Counter

from race_data import ethnicity_data
from ethnicity_weights import category_weights, ethnicity_weights
from utils import choose_race_and_ethnicity, generate_character


# ====================== NOUVELLE FONCTION : CALCUL DE SEUIL ======================
def find_magic_threshold(nb_simulations: int = 50_000, target_percent: float = 50.0):
    """Calcule le seuil exact de Combat Points pour avoir X% de personnages magiques"""
    print(f"🔬 Calcul du seuil pour {target_percent}% de magiques ({nb_simulations:,} simulations)...\n")
    
    cp_list = []
    
    for i in range(nb_simulations):
        char = generate_character(f"SIM-{i:06d}")
        cp_list.append(char["Combat_Points"])
        
        if (i + 1) % 10000 == 0:
            print(f"   → {i+1:,} / {nb_simulations:,} simulations...")

    cp_list.sort()
    index = int(nb_simulations * (target_percent / 100))
    threshold = cp_list[index]
    
    actual_percent = sum(1 for cp in cp_list if cp <= threshold) / nb_simulations * 100

    print("\n" + "="*75)
    print(f"RÉSULTAT - Seuil pour {target_percent}% de personnages magiques")
    print("="*75)
    print(f"Seuil recommandé       : {threshold:.2f} Combat Points")
    print(f"Pourcentage réel       : {actual_percent:.2f}%")
    print(f"Médiane CP             : {cp_list[nb_simulations//2]:.2f}")
    print(f"Min → Max CP           : {min(cp_list):.2f} → {max(cp_list):.2f}")
    print("="*75)
    
    return threshold


# ====================== ANCIENNE FONCTION (conservée intacte) ======================
def simulate_ethnicity_distribution(nb_simulations: int = 100_000):
    """Simule un grand nombre de personnages et affiche les distributions.
    
    Note : Les noms d'ethnies et de catégories sont maintenant en anglais.
    """
    
    print(f"🎲 Simulation de {nb_simulations:,} personnages en cours...\n")
    
    ethnicity_count = Counter()
    race_count = Counter()
    magic_count = 0

    for _ in range(nb_simulations):
        race, ethnicity = choose_race_and_ethnicity()
        
        ethnicity_count[ethnicity] += 1
        race_count[race] += 1

        # Simulation rapide de magie
        if random.random() < 0.18:
            magic_count += 1

    total = sum(ethnicity_count.values())

    print("=" * 95)
    print(f"DISTRIBUTION DES ETHNIES ({nb_simulations:,} personnages)")
    print("=" * 95)

    print("\n--- Top 50 Ethnics ---")
    for eth, count in ethnicity_count.most_common(50):
        percent = (count / total) * 100
        print(f"{eth:32} | {count:7,} | {percent:6.2f}%")

    print("\n--- By Main Category ---")
    for race_name, count in race_count.most_common():
        percent = (count / total) * 100
        print(f"{race_name:15} | {count:7,} | {percent:6.2f}%")

    print("\n" + "=" * 95)
    print(f"Total simulated           : {total:,} characters")
    print(f"Magic percentage          : {magic_count/total:.2%}")
    print("=" * 95)


if __name__ == "__main__":
    random.seed(42)  # Pour des résultats reproductibles
    
    # ====================== TESTS DE SEUILS ======================
    print("=== CALCUL AUTOMATIQUE DES SEUILS MAGIQUES ===\n")
    
    find_magic_threshold(nb_simulations=50_000, target_percent=50.0)   # 50% magiques
    find_magic_threshold(nb_simulations=50_000, target_percent=20.0)   # 20% Arcanistes
    
    # ====================== SIMULATION NORMALE ======================
    print("\n=== SIMULATION DE DISTRIBUTION ===\n")
    simulate_ethnicity_distribution(nb_simulations=30_000)