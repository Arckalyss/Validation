#bfs.py

from collections import deque
from typing import Dict, List, Tuple, Optional, Set, TypeVar

from rootedgraph import RootedGraph

V = TypeVar("V")  # typiquement (sys_state, prop_state)

def breadth_first_search(
    rg: RootedGraph[V],
    on_entry: callable,
    opaque=None
) -> Tuple[List[V], Set[V]]:
    """
    Parcours BFS classique d'un graphe enraciné.
    
    - rg : RootedGraph
    - on_entry(v, opaque) : fonction appelée à l'entrée d'un sommet
      Retourne True si on veut arrêter le BFS
    - opaque : objet passé à on_entry pour accumuler des infos
    
    Retour :
    - trace : liste des sommets visités dans l'ordre de découverte
    - visited : set de tous les sommets visités
    """
    from collections import deque

    queue = deque()
    visited: Set[V] = set()
    trace: List[V] = []

    for r in rg.roots():
        queue.append(r)
        visited.add(r)

    while queue:
        v = queue.popleft()
        trace.append(v)

        if on_entry(v, opaque):
            break

        for w in rg.neighbors(v):
            if w not in visited:
                visited.add(w)
                queue.append(w)

    return trace, visited


def bfs_safety(
    rg: RootedGraph[V],
    is_bad: callable
) -> Optional[List[V]]:
    """
    BFS de model checking (propriété de sûreté).

    - rg : graphe enraciné (produit synchrone système × propriété)
    - is_bad(v) : True si l'état v viole la propriété

    Retour :
    - une trace (liste d'états) menant à un état BAD
    - None si la propriété est respectée
    """

    queue = deque()
    visited: Set[V] = set()
    parent: Dict[V, Optional[V]] = {}

    # Initialisation
    for r in rg.roots():
        queue.append(r)
        visited.add(r)
        parent[r] = None

    # BFS
    while queue:
        v = queue.popleft()

        # Test propriété
        if is_bad(v):
            return _reconstruct_trace(parent, v)

        for w in rg.neighbors(v):
            if w not in visited:
                visited.add(w)
                parent[w] = v
                queue.append(w)

    return None


def _reconstruct_trace(
    parent: Dict[V, Optional[V]],
    target: V
) -> List[V]:
    trace = []
    cur = target
    while cur is not None:
        trace.append(cur)
        cur = parent[cur]
    trace.reverse()
    return trace
