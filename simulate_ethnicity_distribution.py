# simulate_ethnicity_distribution.py
import random
from collections import Counter
from race_data import ethnicity_data
from utils import choose_race_and_ethnicity  # On réutilise ta fonction


def simulate_ethnicity_distribution(nb_simulations=100000):
    print(f"Simulation de {nb_simulations:,} personnages pour analyser la distribution...\n")
    
    ethnicity_count = Counter()
    race_count = Counter()

    for _ in range(nb_simulations):
        race, ethnicity = choose_race_and_ethnicity()
        ethnicity_count[ethnicity] += 1
        race_count[race] += 1

    # ====================== RÉSULTATS ======================
    print("="*80)
    print("DISTRIBUTION RÉELLE DES ETHNIES (sur", nb_simulations, "personnages)")
    print("="*80)

    print("\n--- Par Ethnie (Top 60) ---")
    for eth, count in ethnicity_count.most_common(60):
        percent = (count / nb_simulations) * 100
        print(f"{eth:35} | {count:6,} | {percent:6.2f}%")

    print("\n--- Par Grande Catégorie ---")
    for race, count in race_count.most_common():
        percent = (count / nb_simulations) * 100
        print(f"{race:15} | {count:6,} | {percent:6.2f}%")

    # Vérification des catégories principales
    total = sum(race_count.values())
    print(f"\nTotal simulé : {total:,} personnages")


if __name__ == "__main__":
    random.seed(42)  # reproductible
    simulate_ethnicity_distribution(nb_simulations=100000)   # Tu peux mettre 500000 pour plus de précision