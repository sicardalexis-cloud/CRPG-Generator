import random
from collections import Counter, defaultdict

from settlement_data import get_random_settlement
from skill_data import get_num_active_skills   # ← Import depuis ton fichier


def test_active_skills_distribution(n_simulations=10000):
    print(f"📊 Test de la distribution des compétences actives sur {n_simulations} simulations...\n")
    
    total_active = 0
    settlement_stats = Counter()
    active_by_settlement = defaultdict(list)
    
    for _ in range(n_simulations):
        region_id = random.randint(1, 133)
        _, settlement_type = get_random_settlement(region_id)
        
        num_skills = get_num_active_skills(settlement_type)
        
        total_active += num_skills
        settlement_stats[settlement_type] += 1
        active_by_settlement[settlement_type].append(num_skills)
    
    # ====================== RÉSULTATS GÉNÉRAUX ======================
    average = total_active / n_simulations
    print(f"✅ Moyenne globale de compétences actives : **{average:.2f}**")
    print("-" * 60)
    
    # ====================== TOP 15 SETTLEMENTS ======================
    print("=== MOYENNE PAR TYPE DE SETTLEMENT (Top 15) ===\n")
    for settlement, count in settlement_stats.most_common(15):
        skills_list = active_by_settlement[settlement]
        avg_skills = sum(skills_list) / len(skills_list)
        print(f"{settlement:35} : {avg_skills:.2f}  ({count:5} occ.)")
    
    # ====================== DISTRIBUTION GLOBALE ======================
    global_dist = Counter()
    for skills_list in active_by_settlement.values():
        for num in skills_list:
            global_dist[num] += 1
    
    print("\n=== DISTRIBUTION GLOBALE DES NOMBRES DE COMPÉTENCES ===")
    for num in sorted(global_dist.keys()):
        perc = global_dist[num] / n_simulations * 100
        bar = "█" * int(perc / 3)
        print(f"{num:2} compétences : {global_dist[num]:5} ({perc:5.1f}%) {bar}")


if __name__ == "__main__":
    random.seed(42)
    test_active_skills_distribution(10000)