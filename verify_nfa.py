# verify_nfa.py
"""
Moteur de vérification NFA pour iSoup.
Exploration BFS du produit système × propriété.
"""

import sys
from pathlib import Path

from common.languagesemantics import LanguageSemantics
from common.propertysemantics import PropertySemantics
from common.step import Step, StutteringAction

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
