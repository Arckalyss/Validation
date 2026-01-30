# soup/soup.py

from typing import List, Any
from .piece import Piece

class Soup:
    """
    DSL Soup :
    - pieces : liste de Piece
    - initial : état initial
    """

    def __init__(self, pieces: List[Piece], initial_state: Any):
        self.pieces = pieces
        self.initial_state = initial_state

    def enabled_pieces(self, state):
        """Retourne les pièces activables dans l'état courant."""
        return [p for p in self.pieces if p.is_enabled(state)]
