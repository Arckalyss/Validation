from abc import ABC, abstractmethod
from functools import partial

# =========================
# Graphe abstrait
# =========================

class RootedGraph(ABC):
    @abstractmethod
    def roots(self):
        pass

    @abstractmethod
    def neighbors(self, vertex):
        pass


# =========================
# BFS générique
# =========================

def validation(rg: RootedGraph, onEntry, opaque=None):
    queue = []
    for r in rg.roots():
        queue.append(r)

    marked = []

    while len(queue) > 0:
        v = queue.pop(0)

        if v not in marked:
            marked.append(v)

            terminate, opaque = onEntry(v, opaque)
            if terminate:
                return marked

            for w in rg.neighbors(v):
                queue.append(w)

    return marked


# =========================
# Graphe dictionnaire
# =========================

class DictionaryGraph(RootedGraph):
    def __init__(self, graph=None, roots=None):
        self.graph = graph if graph is not None else {}
        self._roots = roots if roots is not None else []

    def roots(self):
        return self._roots

    def neighbors(self, vertex):
        return self.graph.get(vertex, [])


# =========================
# Graphe des Tours de Hanoi
# =========================

class HanoiGraph(RootedGraph):
    def __init__(self, n_disk):
        self.n_disk = n_disk

    def roots(self):
        return [(tuple(range(self.n_disk, 0, -1)), (), ())]

    def neighbors(self, vertex):
        neighbors = []

        for i in range(3):
            if not vertex[i]:
                continue

            disk = vertex[i][-1]

            for j in range(3):
                if i == j:
                    continue

                if not vertex[j] or vertex[j][-1] > disk:
                    new_state = [list(t) for t in vertex]
                    new_state[i].pop()
                    new_state[j].append(disk)

                    neighbors.append(tuple(tuple(t) for t in new_state))

        return neighbors


# =========================
# Fonctions onEntry
# =========================

def reachable(vertex, opaque=None, target='C'):
    return (vertex == target, opaque)


def hanoi_goal(vertex, opaque):
    n = opaque
    goal = ((), (), tuple(range(n, 0, -1)))
    return (vertex == goal, opaque)


# =========================
# Tests
# =========================

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': [],
}

print(validation(DictionaryGraph(graph, ['A']), reachable))
print(validation(DictionaryGraph(graph, ['A']), partial(reachable, target='D')))

hg = HanoiGraph(3)
visited = validation(hg, hanoi_goal, opaque=3)
print("États visités (Hanoi) :", len(visited))
