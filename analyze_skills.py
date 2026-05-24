# analyze_skills.py
import random
from collections import Counter

# Imports de tes modules
from skill_data import generate_active_skills, active_skills_list
from ethnicity_weights import ethnicity_weights
from origin_data import get_random_origin, region_names
from settlement_data import get_random_settlement


def analyze_active_skills(nb_simulations: int = 30_000):
    print(f"🔍 Analyse de {nb_simulations:,} personnages en cours...\n")
    
    skill_counter = Counter()
    
    for _ in range(nb_simulations):
        # Choisir une ethnie pondérée
        ethnicity = random.choices(
            list(ethnicity_weights.keys()),
            weights=list(ethnicity_weights.values()),
            k=1
        )[0]
        
        # Région d'origine
        origin_region = get_random_origin(ethnicity)
        
        # Trouver l'ID de la région
        region_id = 0
        for rid, rname in region_names.items():
            if rname == origin_region:
                region_id = rid
                break
        
        # Type de settlement
        _, settlement_type = get_random_settlement(region_id)
        
        # Générer les compétences
        skills = generate_active_skills(
            region_id=region_id,
            ethnicity=ethnicity,
            settlement_type=settlement_type,
            num_skills=5
        )
        
        for skill in skills.keys():
            skill_counter[skill] += 1
    
    # ====================== RÉSULTATS ======================
    total = sum(skill_counter.values())
    
    print("=" * 90)
    print(f"📊 RÉPARTITION DES COMPÉTENCES ACTIVES ({nb_simulations:,} pers.)")
    print("=" * 90)
    print(f"{'Compétence':55} | {'Occurrences':>10} | {'Pourcentage':>10}")
    print("-" * 90)
    
    for skill, count in skill_counter.most_common():
        percent = (count / total) * 100
        print(f"{skill:55} | {count:10,} | {percent:9.2f}%")
    
    print("=" * 90)
    print(f"Total occurrences : {total:,}")
    print(f"Moyenne par personnage : {total / nb_simulations:.2f}")
    print("=" * 90)


if __name__ == "__main__":
    random.seed(42)  # reproductible
    analyze_active_skills(nb_simulations=30_000)