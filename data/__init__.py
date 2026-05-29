"""
Package data - Données de configuration et modifiers pour le générateur CRPG.

Ce package centralise les données statiques (modifiers, etc.) afin de réduire
la taille des fichiers de logique et de faciliter la maintenance.
"""

# Ré-exports principaux pour simplifier les imports
from .modifiers import (
    ethnicity_craft_modifiers,
    region_craft_modifiers,
    settlement_craft_modifiers,
    ethnicity_knowledge_modifiers,
    region_knowledge_modifiers,
    settlement_knowledge_modifiers,
    ethnicity_literacy_modifiers,
)
