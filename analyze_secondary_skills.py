import random
from collections import Counter, defaultdict
from typing import Dict

from knowledge_data import generate_secondary_skills
from settlement_data import get_random_settlement   # ← Important

def analyze_languages(n_simulations: int = 4000):
    print(f"🚀 Analyse des langues (parlées + écrites) sur {n_simulations} simulations...\n")
    
    spoken_by_eth: Dict[str, Counter] = defaultdict(Counter)
    written_by_eth: Dict[str, Counter] = defaultdict(Counter)
    total_by_eth: Dict[str, int] = defaultdict(int)
    settlement_counter = Counter()
    
    ethnicities = [
        "Chondathan", "Tethyrian", "Calishite", "Damaran", "Illuskan", "Mulan",
        "Elf Moon", "Elf Wood", "Elf Drow", "Elf Sun", "Half-Elf",
        "Nain", "Shield Dwarf", "Gold Dwarf",
        "Halfelin", "Gnome", "Half-Orc", "Orc", "Tiefling", "Dragonborn"
    ]
    
    for _ in range(n_simulations):
        ethnicity = random.choice(ethnicities)
        region_id = random.randint(1, 133)
        
        # === Utilisation du vrai système pondéré ===
        region_name, settlement_type = get_random_settlement(region_id)
        settlement_counter[settlement_type] += 1
        
        result = generate_secondary_skills(ethnicity, region_id, settlement_type)
        
        if not result:
            continue
            
        total_by_eth[ethnicity] += 1
        
        # Langues parlées
        for lang in result.get("spoken_languages", []):
            spoken_by_eth[ethnicity][lang] += 1
        
        # Langues écrites
        for lang in result.get("literacy", {}):
            written_by_eth[ethnicity][lang] += 1
    
    # ====================== DISTRIBUTION SETTLEMENTS ======================
    print("=== DISTRIBUTION RÉALISTE DES SETTLEMENTS ===\n")
    total = sum(settlement_counter.values())
    for sett, count in settlement_counter.most_common():
        perc = count / total * 100
        print(f"{sett:30} : {count:5} ({perc:5.1f}%)")
    
    # ====================== LANGUES ======================
    print("\n=== LANGUES PARLÉES PAR ETHNIE (top 5) ===\n")
    for eth in sorted(total_by_eth.keys()):
        counter = spoken_by_eth[eth]
        total = total_by_eth[eth]
        print(f"{eth:18} ({total} pers.)")
        for lang, count in counter.most_common(5):
            perc = count / total * 100
            print(f"   {lang:28} : {count:4} ({perc:5.1f}%)")
        print("-" * 50)
    
    print("\n=== LANGUES ÉCRITES PAR ETHNIE (top 5) ===\n")
    for eth in sorted(total_by_eth.keys()):
        counter = written_by_eth[eth]
        total = total_by_eth[eth]
        print(f"{eth:18} ({total} pers.)")
        for lang, count in counter.most_common(5):
            perc = count / total * 100
            print(f"   {lang:28} : {count:4} ({perc:5.1f}%)")
        print("-" * 50)


if __name__ == "__main__":
    random.seed(42)
    analyze_languages(4000)