#stepsynchronousproduct.py
from matplotlib.pyplot import step
from languagesemantics import LanguageSemantics
from step import Step, StutteringAction
from propertysemantics import PropertySemantics

class StepSynchronousProduct(LanguageSemantics):
    """
    Produit synchronisé (Système × Propriété).
    - Le système (lhs) génère des steps.
    - La propriété (rhs) lit chaque step et évolue.
    Les états du produit sont des tuples (sys_state, prop_state).
    Les "actions" du produit sont des tuples (Step, prop_action).
    """

    def __init__(self, lhs: LanguageSemantics, rhs: PropertySemantics):
        self.lhs = lhs
        self.rhs = rhs

    def initials(self):
        res = []
        for lc in self.lhs.initials():
            for rc in self.rhs.initials():
                res.append((lc, rc))
        return res

    def actions(self, configuration):
        sys_state, prop_state = configuration
        sync_actions = []

        lhs_actions = self.lhs.actions(sys_state)
        number_of_effective = 0

        # Pour chaque action système, construire des steps (source, a, target)
        for a in lhs_actions:
            targets = self.lhs.execute(sys_state, a)  # chez toi: liste de targets
            if targets:
                number_of_effective += 1
            for t in targets:
                step = Step(sys_state, a, t)
                rhs_actions = self.rhs.actions(step, prop_state)
                for ra in rhs_actions:
                    sync_actions.append((step, ra))

        # Si aucune action système n’est possible : on crée un stuttering step
        if number_of_effective == 0:
            step = Step(sys_state, StutteringAction.instance(), sys_state)
            rhs_actions = self.rhs.actions(step, prop_state)
            for ra in rhs_actions:
                sync_actions.append((step, ra))

        return sync_actions

    def execute(self, state, action):
        sys_state, prop_state = state
        step, prop_action = action
        new_prop = self.rhs.execute(prop_action, step, prop_state)
        return [(step.target, new_prop)]