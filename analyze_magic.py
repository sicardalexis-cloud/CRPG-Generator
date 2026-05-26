import random
from collections import Counter
from utils import generate_character


def analyze_magic_proportions(count: int = 5000, seed: int = None):
    """Analyse détaillée des proportions Magie Blanche vs Magie Verte"""
    
    if seed is not None:
        random.seed(seed)

    print(f"🔬 Analyse de {count} personnages en cours...\n")

    magic_stats = Counter()
    subtype_stats = Counter()
    settlement_impact = Counter()

    for i in range(count):
        char = generate_character(f"TEST-{i+1:05d}")
        
        magic_type = char.get("Magic_Type")
        subtype = char.get("Magic_Subtype")
        settlement = char.get("Settlement_Type", "Inconnu")

        if char.get("Magic") == "YES":
            magic_stats[magic_type] += 1
            subtype_stats[subtype] += 1
            settlement_impact[(settlement, subtype)] += 1

    total_magic = sum(magic_stats.values())

    print("="*70)
    print("📊 ANALYSE DES TYPES DE MAGIE")
    print("="*70)
    print(f"Total personnages générés : {count}")
    print(f"Personnages magiques       : {total_magic} ({total_magic/count:.2%})\n")

    # Répartition par type principal
    print("Répartition par Type :")
    for mag_type, nb in sorted(magic_stats.items(), key=lambda x: -x[1]):
        print(f"   • {mag_type:15} : {nb:5d} ({nb/total_magic:.2%})")

    print("\n" + "-"*50)
    print("Détail Magie Théurgique (Blanche / Verte) :")
    print("-"*50)
    
    blanche = subtype_stats.get("Magie Blanche", 0)
    verte = subtype_stats.get("Magie Verte", 0)
    total_theurgique = blanche + verte

    print(f"   Magie Blanche     : {blanche:5d} ({blanche/total_theurgique:.2%} des théurgiques)")
    print(f"   Magie Verte       : {verte:5d} ({verte/total_theurgique:.2%} des théurgiques)")
    print(f"   Total Théurgique  : {total_theurgique:5d}")

    # Impact du type de settlement
    print("\n" + "="*70)
    print("🏘️  INFLUENCE DU TYPE DE SETTLEMENT")
    print("="*70)
    
    for (settlement, sub), nb in sorted(settlement_impact.items(), key=lambda x: -x[1]):
        if sub in ["Magie Blanche", "Magie Verte"]:
            print(f"   {settlement:25} → {sub:15} : {nb:4d}")

    # Top 5 settlements pour chaque
    print("\n🏆 Top Settlements pour Magie Blanche :")
    blanche_sett = {k[0]: v for k, v in settlement_impact.items() if k[1] == "Magie Blanche"}
    for sett, nb in sorted(blanche_sett.items(), key=lambda x: -x[1])[:5]:
        print(f"   • {sett:25} : {nb}")

    print("\n🌲 Top Settlements pour Magie Verte :")
    verte_sett = {k[0]: v for k, v in settlement_impact.items() if k[1] == "Magie Verte"}
    for sett, nb in sorted(verte_sett.items(), key=lambda x: -x[1])[:5]:
        print(f"   • {sett:25} : {nb}")


# ====================== LANCEMENT ======================
if __name__ == "__main__":
    analyze_magic_proportions(count=5000, seed=42)   # seed pour reproductibilité