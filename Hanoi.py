# Hanoi.py
from BFS import validation, RootedGraph  

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
# Fonction BFS avec reconstruction de chemin
# =========================
def validation_with_path(rg: RootedGraph, onEntry, opaque=None):
    queue = []
    predecessor = {}  # pour reconstruire le chemin

    for r in rg.roots():
        queue.append(r)
        predecessor[r] = None  # la racine n'a pas de prédécesseur

    marked = []

    while queue:
        v = queue.pop(0)
        if v not in marked:
            marked.append(v)
            terminate, opaque = onEntry(v, opaque)
            if terminate:
                # Reconstruire le chemin
                path = []
                while v is not None:
                    path.append(v)
                    v = predecessor[v]
                path.reverse()
                return marked, path
            for w in rg.neighbors(v):
                if w not in predecessor:
                    predecessor[w] = v
                queue.append(w)
    return marked, []  # si jamais l'objectif n'est pas trouvé

# =========================
# Fonction de détection de l'état final
# =========================
def hanoi_goal(vertex, opaque):
    n = opaque
    goal = ((), (), tuple(range(n, 0, -1)))
    return (vertex == goal, opaque)

# =========================
# Test
# =========================
if __name__ == "__main__":
    n = 3
    hg = HanoiGraph(n)
    visited, path = validation_with_path(hg, hanoi_goal, opaque=n)

    print(f"Nombre d'états visités : {len(visited)}")
    print(f"Chemin de l'état initial à l'état final ({len(path)} mouvements) :")
    for step in path:
        print(step)
