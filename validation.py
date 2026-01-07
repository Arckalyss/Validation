from abc import ABC, abstractmethod


graph = {
 "a": ["b","d"],"b": ["d","e"],"c": ["e","f"], "d": [], "e": [], "f" : []
}

class RootedGraph(ABC):
    @abstractmethod
    def roots(self):
        pass
    @abstractmethod
    def neighbors(self, vertex):
        pass


class DictionaryGraph(RootedGraph):
    def __init__(self, graph = None, roots= None):
        self.graph = graph if graph is not None else {}
        self._roots = roots if roots is not None else []

    def roots(self):
        return self._roots

    def neighbors(self, vertex):
        return self.graph.get(vertex, [])
    

def reachability(vertex, opaque):
    #appelée sur chaque nouveau sommet visité
    """
    Args:
        vertex: le sommet qui vient d'être découvert
        opaque: données passées/accumulées (n'importe quoi)
    Returns:
        (terminaten ,new_opaque)
        terminate: bool - True pour arrêter bfs, false pour continuer
        new_opaque: valeur mise à jour de opaque
    """
    target, reachable = opaque
    if vertex == target:  
        return (True, (target, True))
    else:
        return (False, (target, False))
onEntry = lambda vertex,opaque : (vertex == "d" , opaque)


def bfs(rg:RootedGraph, onEntry, opaque):
    queue = rg.roots()
    k = set()
    while len(queue)>0:
        v=queue.pop(0)
        if v not in k:
            k.add(v)
            B,opaque = onEntry(v, opaque)
            if B:
                return (v,opaque)
        for i in rg.neighbors(v):
            queue.append(i)
    return (False,opaque)

#print(bfs((DictionaryGraph(graph, ["a"]))))


print(bfs(DictionaryGraph(graph, ["a"]), onEntry, None))
<<<<<<< HEAD



def HanoïGraph():
    pass
=======
>>>>>>> 7a3391f (I added the Q3 programs.)
