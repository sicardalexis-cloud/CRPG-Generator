import random
from collections import Counter, defaultdict
from typing import Dict
from knowledge_data import generate_secondary_skills

def analyze_literacy_by_ethnicity(n_simulations: int = 4000):
    print(f"🚀 Analyse des langues écrites sur {n_simulations} simulations...\n")
    
    literacy_by_eth: Dict[str, Counter] = defaultdict(Counter)
    total_by_eth: Dict[str, int] = defaultdict(int)
    errors = 0
    
    ethnicities = [
        "Chondathan", "Tethyrian", "Calishite", "Damaran", "Illuskan", "Mulan",
        "Elf Moon", "Elf Wood", "Elf Drow", "Elf Sun", "Half-Elf",
        "Nain", "Shield Dwarf", "Gold Dwarf",
        "Halfelin", "Gnome", "Half-Orc", "Orc", "Tiefling", "Dragonborn"
    ]
    
    for i in range(n_simulations):
        try:
            active_count = random.randint(2, 8)
            ethnicity = random.choice(ethnicities)
            region_id = random.randint(1, 5)
            settlement = random.choice(["Metropolis", "Large City", "Village", "Wilderness", "Fortress"])
            
            result = generate_secondary_skills(active_count, ethnicity, region_id, settlement)
            
            if result is None:
                errors += 1
                continue
                
            total_by_eth[ethnicity] += 1
            
            for lang in result.get("literacy", {}):
                literacy_by_eth[ethnicity][lang] += 1
                
        except Exception as e:
            errors += 1
            if errors < 5:  # Afficher seulement les premières erreurs
                print(f"Erreur lors de la simulation {i}: {e}")
    
    print(f"Simulations terminées. Erreurs : {errors}\n")
    
    # ====================== AFFICHAGE ======================
    print("=== LANGUE ÉCRITE LA PLUS COURANTE PAR ETHNIE ===\n")
    
    for eth in sorted(total_by_eth.keys()):
        counter = literacy_by_eth[eth]
        total = total_by_eth[eth]
        
        if total == 0:
            continue
            
        print(f"{eth:18} ({total} pers.)")
        for lang, count in counter.most_common(5):
            perc = count / total * 100
            print(f"   {lang:28} : {count:4} ({perc:5.1f}%)")
        print("-" * 50)
    
    # Statistiques globales sur la première langue
    print("\n=== PREMIÈRE LANGUE ÉCRITE (native) - Répartition globale ===")
    first_lang_counter = Counter()
    
    for _ in range(n_simulations):
        try:
            eth = random.choice(ethnicities)
            result = generate_secondary_skills(4, eth, 1, "Village")
            if result and result.get("literacy"):
                first = list(result["literacy"].keys())[0]
                first_lang_counter[first] += 1
        except:
            pass
    
    for lang, count in first_lang_counter.most_common(12):
        print(f"{lang:28} : {count:5} ({count/n_simulations*100:5.1f}%)")


if __name__ == "__main__":
    random.seed(42)
    analyze_literacy_by_ethnicity(4000)