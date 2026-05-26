# =============================================
# analyze_skills.py
# =============================================
import random
from collections import Counter, defaultdict

from settlement_data import get_random_settlement
from skill_data import generate_skills   # ← Nouvelle importation


def analyze_skills_distribution(n_simulations=10000, seed=42):
    print(f"📊 Analyse de la distribution des compétences sur {n_simulations} simulations...\n")
    
    random.seed(seed)
    
    total_skills = 0
    outdoor_total = 0
    urban_total = 0
    
    settlement_stats = Counter()
    active_by_settlement = defaultdict(list)
    outdoor_by_settlement = defaultdict(list)
    urban_by_settlement = defaultdict(list)
    
    magic_count = 0  # si tu veux analyser la magie plus tard

    for i in range(n_simulations):
        region_id = random.randint(0, 133)
        _, settlement_type = get_random_settlement(region_id)
        
        # Génération complète avec le nouveau système
        skills_data = generate_skills(
            settlement_type=settlement_type,
            region_id=region_id,
            ethnicity=None  # on peut tester avec ethnicity plus tard
        )
        
        total = skills_data["total"]
        outdoor = skills_data["outdoor_count"]
        urban = skills_data["urban_count"]
        
        total_skills += total
        outdoor_total += outdoor
        urban_total += urban
        
        settlement_stats[settlement_type] += 1
        active_by_settlement[settlement_type].append(total)
        outdoor_by_settlement[settlement_type].append(outdoor)
        urban_by_settlement[settlement_type].append(urban)

    # ====================== STATISTIQUES GLOBALES ======================
    avg_total = total_skills / n_simulations
    avg_outdoor = outdoor_total / n_simulations
    avg_urban = urban_total / n_simulations

    print(f"✅ Moyenne globale de compétences actives : **{avg_total:.2f}**")
    print(f"   → Outdoor : {avg_outdoor:.2f} | Urban : {avg_urban:.2f}")
    print("-" * 70)

    # ====================== PAR TYPE DE SETTLEMENT ======================
    print("=== MOYENNE PAR TYPE DE SETTLEMENT (Top 15) ===\n")
    for settlement, count in settlement_stats.most_common(15):
        totals = active_by_settlement[settlement]
        out = outdoor_by_settlement[settlement]
        urb = urban_by_settlement[settlement]
        
        avg_t = sum(totals) / len(totals)
        avg_o = sum(out) / len(out)
        avg_u = sum(urb) / len(urb)
        
        print(f"{settlement:35} : {avg_t:5.2f}  "
              f"(Outdoor: {avg_o:4.2f} | Urban: {avg_u:4.2f})  ({count:5} occ.)")

    # ====================== DISTRIBUTION GLOBALE ======================
    global_dist = Counter()
    for skills_list in active_by_settlement.values():
        for num in skills_list:
            global_dist[num] += 1

    print("\n=== DISTRIBUTION GLOBALE DU NOMBRE TOTAL DE COMPÉTENCES ===")
    for num in sorted(global_dist.keys()):
        perc = global_dist[num] / n_simulations * 100
        bar = "█" * int(perc / 2.5)
        print(f"{num:2} compétences : {global_dist[num]:5} ({perc:5.1f}%) {bar}")


if __name__ == "__main__":
    analyze_skills_distribution(n_simulations=10000, seed=42)