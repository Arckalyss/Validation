# BFS_definition.py
from __future__ import annotations
from collections import deque
from typing import Callable, Deque, Iterable, List, Set, Tuple, TypeVar, Generic, Optional

from soup.rootedgraph import RootedGraph

V = TypeVar("V")
Opaque = TypeVar("Opaque")

# onEntry(vertex, opaque) -> (terminate?, opaque_maj)
OnEntry = Callable[[V, Opaque], Tuple[bool, Opaque]]

def BFS(rg: RootedGraph[V], onEntry: OnEntry[V, Opaque], opaque: Opaque) -> Tuple[List[V], Opaque]:
    """
    Parcours en largeur (Breadth-First Search) sur un graphe enraciné.

    Entrées
    - rg: objet RootedGraph avec roots() et neighbors(v)
    - onEntry: callback appelé à chaque nouveau sommet visité:
        (terminate, opaque) = onEntry(v, opaque)
      Si terminate=True, on stoppe immédiatement.
    - opaque: état accumulateur (liste, dict, compteur, etc.)

    Sorties
    - marked: liste des sommets visités (ordre de découverte)
    - opaque: accumulateur final (ou au moment de l'arrêt)
    """
    queue: Deque[V] = deque(rg.roots())
    marked: List[V] = []
    seen: Set[V] = set()  # accélère le "déjà vu" si V est hashable

    while queue:
        v = queue.popleft()

        # Si v n'est pas hashable (rare), set() plantera -> fallback sur liste
        try:
            if v in seen:
                continue
            seen.add(v)
        except TypeError:
            if v in marked:
                continue

        marked.append(v)

        terminate, opaque = onEntry(v, opaque)
        if terminate:
            return marked, opaque

        for w in rg.neighbors(v):
            queue.append(w)

    return marked, opaque
