# verify_nfa.py
"""
Moteur de vérification NFA pour iSoup.
Exploration BFS du produit système × propriété.
"""

import sys
from pathlib import Path

# Ajouter le dossier "common" dans sys.path pour les imports
sys.path.insert(0, str(Path(__file__).parent / "common"))

from languagesemantics import LanguageSemantics
from propertysemantics import PropertySemantics
from step import Step, StutteringAction

# Ajouter le dossier courant pour trouver ls2rg, bfs, stepsynchronousproduct
sys.path.insert(0, str(Path(__file__).parent))

from ls2rg import LS2RG
from stepsynchronousproduct import StepSynchronousProduct
from bfs import bfs_safety


def verify_property(system_semantics, property_semantics):
    """
    Vérifie une propriété sur un modèle iSoup.
    Retourne None si propriété satisfaite, sinon trace jusqu'à violation.
    """
    product = StepSynchronousProduct(system_semantics, property_semantics)
    rg = LS2RG(product)

    # BFS pour trouver un état "bad" (violation)
    trace = bfs_safety(rg, lambda s: s[1] is True)  # prop_state est True si violation
    return trace


if __name__ == "__main__":
    print("Le moteur NFA est prêt. ⚡")
