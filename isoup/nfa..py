# isoup/nfa.py

from typing import Any, Dict, Iterable, Set, Tuple, Callable

State = Any
Symbol = Any  # typiquement un état système ou une transition système


class NFA:
    """
    Automate non déterministe pour propriétés (sûreté).
    """

    def __init__(
        self,
        states: Set[State],
        initials: Set[State],
        bad_states: Set[State],
        transition: Callable[[State, Symbol], Iterable[State]]
    ):
        self.states = states
        self.initials = initials
        self.bad_states = bad_states
        self.transition = transition

    def next_states(self, state: State, symbol: Symbol) -> Set[State]:
        return set(self.transition(state, symbol))

    def is_bad(self, state: State) -> bool:
        return state in self.bad_states
