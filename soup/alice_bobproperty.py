from propertysemantics import PropertySemantics
from step import StutteringAction


class MutualExclusionProperty(PropertySemantics):
    """
    BAD si Alice et Bob sont simultanément en section critique (CS).
    Ici, l'état système est un tuple: (state_alice, state_bob).
    """

    OK = "OK"
    BAD = "BAD"

    def initials(self):
        return [self.OK]

    def actions(self, step, prop_state):
        return ["tick"]

    def execute(self, prop_action, step, prop_state):
        if prop_state == self.BAD:
            return self.BAD

        sys_target = step.target  # ex: ('CS','I')

        # sys_target est un tuple: (alice_state, bob_state)
        alice = sys_target[0]
        bob = sys_target[1]

        if alice == "CS" and bob == "CS":
            return self.BAD

        return self.OK

    def is_accepting(self, prop_state):
        return prop_state == self.BAD


class DeadlockProperty(PropertySemantics):
    """
    DEAD si le système n'a aucune action (stuttering step).
    """

    OK = "OK"
    DEAD = "DEAD"

    def initials(self):
        return [self.OK]

    def actions(self, step, prop_state):
        return ["tick"]

    def execute(self, prop_action, step, prop_state):
        if prop_state == self.DEAD:
            return self.DEAD

        if isinstance(step.action, StutteringAction):
            return self.DEAD

        return self.OK

    def is_accepting(self, prop_state):
        return prop_state == self.DEAD
