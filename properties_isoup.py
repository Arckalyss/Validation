# properties_isoup.py
"""
Définition des propriétés P1 et P2 en iSoup DSL.
Chaque propriété hérite de PropertySemantics.
"""

from common.propertysemantics import PropertySemantics
from common.step import Step, StutteringAction

class P1(PropertySemantics):
    """Propriété : Mutual exclusion (Alice et Bob ne doivent jamais être dans CS simultanément)."""

    def __init__(self):
        pass

    def initials(self):
        # P1 commence dans un état "non violé"
        return [False]  # False = pas de violation

    def actions(self, step: Step, prop_state):
        """
        step: Step venant du système
        prop_state: état courant de la propriété (False=OK, True=violé)
        """
        alice, bob = step.target[0], step.target[1]
        violation = alice == "CS" and bob == "CS"
        # La propriété passe à True si violation détectée
        return [violation]

    def execute(self, prop_action, step: Step, prop_state):
        # La propriété se met à jour avec prop_action
        return prop_action


class P2(PropertySemantics):
    """Propriété : Deadlock Freedom (le système ne doit jamais rester bloqué)."""

    def __init__(self, system):
        self.system = system  # On pourra vérifier si successors existent

    def initials(self):
        return [False]  # False = pas de deadlock

    def actions(self, step: Step, prop_state):
        # Deadlock détecté si aucun successor depuis step.target
        successors = self.system.actions(step.target)
        is_deadlock = len(successors) == 0
        return [is_deadlock]

    def execute(self, prop_action, step: Step, prop_state):
        return prop_action
