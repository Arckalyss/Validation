from abc import ABC, abstractmethod
from functools import partial
graph = {
    'A': ['B','C'],
    'B': ['D','E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': [],
    'G': [],
}

class RootedGraph(ABC):
    @abstractmethod
    def roots(self):
        pass
    @abstractmethod
    def neighbors(self, vertex):
        pass

class HanoiGraph(RootedGraph):
    def __init__(self, n_disk):
        self.n_disk = n_disk
    
    def roots(self):
        return (tuple(range(3, 0, -1)), (0,0,0), (0,0,0))


def reachable(vertex, target = 'C', opaque = None):
    """
    Appelée sur chaqque nouveau sommet visité.

    Args:
        vertex: Le sommet qui vient d'être découvert
        opaque: Données passées/accumulées (peut être n'importe quoi)
    
    Returns:
        (terminate, new_opaque)
        - terminate: bool - True pour arrêter BFS, False pour continuer
        - new_opaque: Valeur mise à jour de opaque

    """
    # Votre logique ici

    return (vertex==target, target)

lonEntry = lambda vertex,opaque=None : (vertex == "C",opaque)
    




class DictionaryGraph(RootedGraph):
    def __init__(self, graph=None, roots=None):
        self.graph = graph if graph is not None else {}
        self._roots = roots if roots is not None else [] 

    def roots(self):
        return self._roots
    def neighbors(self, vertex):
        return self.graph.get(vertex, [])

def validation(rg:RootedGraph, onEntry, opaque = None):
    queue = []
    for i in rg.roots():
        queue.append(i)
    marked = []
    while len(queue)>0:
        v = queue.pop(0)
        if v not in marked :
            marked.append(v)
            terminate, opaque = onEntry(v)
            if terminate:
                return marked
            for w in rg.neighbors(v):
                queue.append(w)
    return marked

print(validation(DictionaryGraph(graph, ['A']), reachable))
print(validation(DictionaryGraph(graph, ['A']), partial(reachable, target='D')))
print(validation(DictionaryGraph(graph, ['A']), lonEntry))

print(tuple(range(3, 0,-1)))
print((tuple(range(3, 0, -1)), (0,0,0), (0,0,0)))