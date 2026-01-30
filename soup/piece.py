# soup/piece.py

from typing import Callable, Any

class Piece:
    """
    Une pièce de Soup :
    - guard(s) : bool
    - effect(s) : s'
    """

    def __init__(
        self,
        name: str,
        effect: Callable[[Any], Any],
        guard: Callable[[Any], bool]
    ):
        self.name = name
        self.effect = effect
        self.guard = guard

    def is_enabled(self, state) -> bool:
        return self.guard(state)

    def apply(self, state):
        return self.effect(state)

    def __repr__(self):
        return f"Piece({self.name})"