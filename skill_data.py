# skill_data.py
import random
from typing import Dict, List

# =============================================
# COMPÉTENCES PAR ETHNIE (exemple simplifié)
# =============================================
ethnicity_skills = {
    "Chondathan": ["Commerce", "Diplomatie", "Navigation", "Équitation"],
    "Calishite": ["Négociation", "Arcanes", "Escroquerie", "Langue (Shaaran)"],
    "Damaran": ["Survie", "Forgeron", "Combat à l'épée", "Endurance"],
    "Illuskan": ["Navigation", "Pêche", "Survie en milieu froid", "Intimidation"],
    "Rashemi": ["Sorcellerie", "Herboristerie", "Résistance magique", "Combat à mains nues"],
    "Shou": ["Discipline", "Arts martiaux", "Calligraphie", "Stratégie"],
    # Ajoute d'autres ethnies selon tes données
}

default_skills = ["Athlétisme", "Discrétion", "Perception", "Persuasion"]


def generate_skills_for_ethnicity(ethnicity: str, num_skills: int = 4) -> List[str]:
    """Génère une liste de compétences en fonction de l'ethnie"""
    skills_pool = ethnicity_skills.get(ethnicity, default_skills)
    
    # Prend entre 3 et num_skills compétences
    num = random.randint(3, num_skills)
    selected = random.sample(skills_pool, min(num, len(skills_pool)))
    
    return sorted(selected)


def generate_active_skills(region_id: int = 0, ethnicity: str = "Chondathan") -> Dict:
    """Fonction principale appelée par utils.py"""
    skills_list = generate_skills_for_ethnicity(ethnicity)
    
    # Convertit en dict pour compatibilité
    skills_dict = {skill: "Maîtrise" for skill in skills_list}
    
    return {
        "skills": skills_dict,
        "bonus_languages": []  # À compléter plus tard
    }