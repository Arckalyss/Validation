# rootedgraph.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterable, Protocol, TypeVar, Generic, List

V = TypeVar("V")  # type des sommets (vertex)

class RootedGraph(ABC, Generic[V]):
    """Interface d'un graphe enraciné : racines + voisins."""
    
    @abstractmethod
    def roots(self) -> Iterable[V]:
        """Retourne les sommets racines (points de départ du parcours)."""
        raise NotImplementedError

    @abstractmethod
    def neighbors(self, vertex: V) -> Iterable[V]:
        """Retourne les voisins/successeurs d'un sommet."""
        raise NotImplementedError
