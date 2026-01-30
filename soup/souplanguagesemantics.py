# soup/souplanguagesemantics.py

from typing import List, Any
from common.languagesemantics import LanguageSemantics
from .soup import Soup
from .piece import Piece

class SoupLanguageSemantics(LanguageSemantics):
    """
    Sémantique opérationnelle d'une Soup.
    """

    def __init__(self, soup: Soup):
        self.soup = soup

    def initials(self) -> List[Any]:
        return [self.soup.initial_state]

    def actions(self, state) -> List[Piece]:
        # actions = pièces activables
        return self.soup.enabled_pieces(state)

    def execute(self, state, action: Piece) -> List[Any]:
        # action = Piece
        return [action.apply(state)]
