# main.py

from collections import deque
from AB2 import AB2Graph
from AB3 import AB3Graph


def is_up(x):
    return x == "UP" or x == 1

def is_down(x):
    return x == "DOWN" or x == 0



# Q4:  exploration 


def explore_all_states(rg):
    """Explore tous les états atteignables depuis roots() (BFS/queue)."""
    seen = set()
    q = deque(rg.roots())
    while q:
        v = q.popleft()
        if v in seen:
            continue
        seen.add(v)
        for w in rg.neighbors(v):
            if w not in seen:
                q.append(w)
    return seen

def exclusion_violated(v):
    """Exclusion violée si Alice et Bob sont simultanément en CS."""
    # AB1: (a,b)
    # AB2/AB3: (a,b,fA,fB)
    a, b = v[0], v[1]
    return (a == "CS") and (b == "CS")

def find_exclusion_counterexample(states):
    for v in states:
        if exclusion_violated(v):
            return v
    return None

def find_deadlock_state(rg, states):
    for v in states:
        if len(rg.neighbors(v)) == 0:
            return v
    return None


# Q5: BFS avec reconstruction de trace

def bfs_trace(roots, neighbors_labeled, goal):
    q = deque(roots)
    seen = set(roots)
    parent = {}  

    while q:
        v = q.popleft()

        if goal(v):
            actions = []
            cur = v
            while cur in parent:
                prev, act = parent[cur]
                actions.append(act)
                cur = prev
            actions.reverse()
            return actions

        for act, w in neighbors_labeled(v):
            if w not in seen:
                seen.add(w)
                parent[w] = (v, act)
                q.append(w)

    return None


def labeled_neighbors_AB1(v):
    a, b = v
    out = []
    # Alice
    if a == "I":
        out.append(("a2: I->CS", ("CS", b)))
    if a == "CS":
        out.append(("a1: CS->I", ("I", b)))
    # Bob
    if b == "I":
        out.append(("b2: I->CS", (a, "CS")))
    if b == "CS":
        out.append(("b1: CS->I", (a, "I")))
    return out


def labeled_neighbors_AB2_like(v, has_b4=False):
    a, b, fA, fB = v
    out = []

    if a == "I":
        out.append(("a1: I->W, fA:=UP", ("W", b, "UP" if isinstance(fA, str) else 1, fB)))
    if a == "W" and is_down(fB):
        out.append(("a2: W->CS if fB==DOWN", ("CS", b, fA, fB)))
    if a == "CS":
        out.append(("a3: CS->I, fA:=DOWN", ("I", b, "DOWN" if isinstance(fA, str) else 0, fB)))

    if b == "I":
        out.append(("b1: I->W, fB:=UP", (a, "W", fA, "UP" if isinstance(fB, str) else 1)))
    if b == "W" and is_down(fA):
        out.append(("b2: W->CS if fA==DOWN", (a, "CS", fA, fB)))
    if b == "CS":
        out.append(("b3: CS->I, fB:=DOWN", (a, "I", fA, "DOWN" if isinstance(fB, str) else 0)))

    if has_b4 and b == "W" and is_up(fA):
        out.append(("b4: W->I if fA==UP, fB:=DOWN", (a, "I", fA, "DOWN" if isinstance(fB, str) else 0)))

    return out



# MAIN

def run_Q4():
    print("Q4")

    # AB1
    rg1 = AB1Graph()
    s1 = explore_all_states(rg1)
    ce1 = find_exclusion_counterexample(s1)
    dl1 = find_deadlock_state(rg1, s1)
    print(f"[AB1] nb_etats={len(s1)}  exclusion_OK={ce1 is None}  deadlock_OK={dl1 is None}")
    if ce1 is not None:
        print("  contre-exemple exclusion:", ce1)
    if dl1 is not None:
        print("  deadlock:", dl1)

    # AB2
    rg2 = AB2Graph()
    s2 = explore_all_states(rg2)
    ce2 = find_exclusion_counterexample(s2)
    dl2 = find_deadlock_state(rg2, s2)
    print(f"[AB2] nb_etats={len(s2)}  exclusion_OK={ce2 is None}  deadlock_OK={dl2 is None}")
    if ce2 is not None:
        print("  contre-exemple exclusion:", ce2)
    if dl2 is not None:
        print("  deadlock:", dl2)

    # AB3
    rg3 = AB3Graph()
    s3 = explore_all_states(rg3)
    ce3 = find_exclusion_counterexample(s3)
    dl3 = find_deadlock_state(rg3, s3)
    print(f"[AB3] nb_etats={len(s3)}  exclusion_OK={ce3 is None}  deadlock_OK={dl3 is None}")
    if ce3 is not None:
        print("  contre-exemple exclusion:", ce3)
    if dl3 is not None:
        print("  deadlock:", dl3)

    print()


def run_Q5():
    print("Q5")

    # AB1: violation exclusion (CS,CS)
    trace_ab1 = bfs_trace(
        roots=[("I", "I")],
        neighbors_labeled=labeled_neighbors_AB1,
        goal=exclusion_violated
    )
    print("[AB1] trace -> violation exclusion:", trace_ab1)

    # AB2: deadlock = aucun voisin
    rg2 = AB2Graph()
    root2 = rg2.roots()[0]
    trace_ab2 = bfs_trace(
        roots=[root2],
        neighbors_labeled=lambda v: labeled_neighbors_AB2_like(v, has_b4=False),
        goal=lambda v: len(rg2.neighbors(v)) == 0
    )
    print("[AB2] trace -> deadlock:", trace_ab2)

    # (optionnel) AB3: normalement pas de deadlock
    rg3 = AB3Graph()
    root3 = rg3.roots()[0]
    trace_ab3 = bfs_trace(
        roots=[root3],
        neighbors_labeled=lambda v: labeled_neighbors_AB2_like(v, has_b4=True),
        goal=lambda v: len(rg3.neighbors(v)) == 0
    )
    print("[AB3] trace -> deadlock (devrait être None):", trace_ab3)

    print()


if __name__ == "__main__":
    run_Q4()
    run_Q5()