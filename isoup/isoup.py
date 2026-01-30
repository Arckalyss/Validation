# isoup/isoup.py

from typing import Callable, Any, List, Set
from .nfa import NFA


class IRule:
    """
    Règle de transition de propriété :
    - guard(sys_state) -> bool
    - from_state -> to_state
    """

    def __init__(
        self,
        from_state: Any,
        to_state: Any,
        guard: Callable[[Any], bool]
    ):
        self.from_state = from_state
        self.to_state = to_state
        self.guard = guard


class ISoup:
    """
    DSL iSoup pour propriétés.
    """

    def __init__(
        self,
        states: Set[Any],
        initial: Any,
        bad: Any,
        rules: List[IRule]
    ):
        self.states = states
        self.initial = initial
        self.bad = bad
        self.rules = rules

    def to_nfa(self) -> NFA:
        """
        Compile iSoup en NFA.
        """

        def transition(prop_state, sys_state):
            for rule in self.rules:
                if rule.from_state == prop_state and rule.guard(sys_state):
                    yield rule.to_state

        return NFA(
            states=self.states,
            initials={self.initial},
            bad_states={self.bad},
            transition=transition
        )
