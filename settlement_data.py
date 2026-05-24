# settlement_data.py
import random
from typing import Tuple, Dict

# =============================================
# TYPES D'IMPLANTATION
# =============================================
settlement_types = {
    1: "Capitale / Grande Métropole",
    2: "Grande Ville portuaire",
    3: "Grande Ville marchande",
    4: "Ville fortifiée",
    5: "Ville moyenne",
    6: "Bourg / Petite ville",
    7: "Village rural",
    8: "Village côtier / de pêcheurs",
    9: "Village forestier",
    10: "Village de montagne",
    11: "Hameau agricole",
    12: "Hameau isolé",
    13: "Ferme isolée / Domaine",
    14: "Caravansérail / Oasis",
    15: "Avant-poste militaire",
    16: "Camp minier",
    17: "Monastère / Couvent isolé",
    18: "Camp de bûcherons",
    19: "Tribu nomade",
    20: "Colonie frontalière",
    21: "Port de contrebande",
    22: "Ruines habitées",
    23: "Cité souterraine",
    24: "Tour / Manoir isolé",
    25: "Village lacustre / sur pilotis",
    26: "Forteresse naine / Enclave naine",
    27: "Enclave elfique",
    28: "Sanctuaire / Lieu saint",
    29: "Refuge / Campement permanent",
    30: "Poste de commerce isolé"
}

# =============================================
# PROBABILITÉS PAR RÉGION (version stable)
# =============================================
origin_settlement_weights: Dict[int, Dict[int, int]] = {
    0: {5: 25, 6: 25, 7: 20, 11: 15, 12: 15},  # Default
    
    # Exemples (tu peux compléter plus tard)
    1: {1: 25, 2: 30, 3: 20, 5: 15, 14: 5, 21: 5},   # Calimshan
    4: {2: 35, 5: 25, 6: 15, 8: 15, 21: 10},         # Baldur's Gate
    5: {1: 40, 2: 25, 5: 20, 6: 10, 15: 5},          # Waterdeep
    19: {2: 35, 5: 25, 8: 20, 21: 15, 22: 5},        # Luskan
    21: {10: 30, 11: 25, 12: 20, 18: 15, 30: 10},    # Icewind Dale
    24: {9: 35, 8: 25, 18: 20, 20: 10, 30: 10},      # Chult
}

# =============================================
# FONCTION PRINCIPALE
# =============================================
def get_random_settlement(region_id: int) -> Tuple[str, str]:
    """Retourne (nom_région, type_implantation)"""
    from origin_data import region_names
    
    region_name = region_names.get(region_id, "Région inconnue")
    
    weights = origin_settlement_weights.get(region_id, origin_settlement_weights[0])
    
    settlement_idx = random.choices(
        list(weights.keys()),
        weights=list(weights.values()),
        k=1
    )[0]
    
    settlement_name = settlement_types.get(settlement_idx, "Implantation inconnue")
    
    return region_name, settlement_name