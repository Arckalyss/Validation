# soup/alicebob_validation.py
from __future__ import annotations

from collections import deque
from typing import Deque, Dict, Iterable, List, Optional, Tuple, TypeVar

from alicebob_langagesemantics import (
    AB1LanguageSemantics,
    AB2LanguageSemantics,
    AB3LanguageSemantics,
    violates_mutual_exclusion,
)

State = TypeVar("State")


def successors_with_actions(sem, state):
    """
    Génère les successeurs avec l'action associée.
    Retourne une liste de couples (action, next_state).
    """
    out = []
    for a in sem.actions(state):
        for ns in sem.execute(state, a):
            out.append((a, ns))
    return out


def bfs_find_trace_to_bad_state(sem) -> Optional[List[Tuple[Optional[str], State]]]:
    """
    BFS sur la sémantique pour trouver la première violation d'exclusion mutuelle.
    Retourne une trace minimale sous la forme:
        [(None, s0), (action1, s1), (action2, s2), ...]
    ou None si aucune violation atteignable.
    """
    roots = sem.initials()
    if not roots:
        return None

    queue: Deque[State] = deque()
    seen = set()
    parent: Dict[State, Optional[State]] = {}
    parent_action: Dict[State, Optional[str]] = {}

    for r in roots:
        queue.append(r)
        seen.add(r)
        parent[r] = None
        parent_action[r] = None

        # si l'état initial est déjà mauvais
        if violates_mutual_exclusion(r):
            return [(None, r)]

    while queue:
        s = queue.popleft()

        for action, ns in successors_with_actions(sem, s):
            if ns in seen:
                continue
            seen.add(ns)
            parent[ns] = s
            parent_action[ns] = action

            if violates_mutual_exclusion(ns):
                return reconstruct_trace(ns, parent, parent_action)

            queue.append(ns)

    return None


def bfs_find_trace_to_deadlock(sem) -> Optional[List[Tuple[Optional[str], State]]]:
    """
    BFS sur la sémantique pour trouver le premier deadlock atteignable.
    Deadlock = état atteignable sans successeur.
    Retourne une trace minimale, ou None si aucun deadlock.
    """
    roots = sem.initials()
    if not roots:
        return None

    queue: Deque[State] = deque()
    seen = set()
    parent: Dict[State, Optional[State]] = {}
    parent_action: Dict[State, Optional[str]] = {}

    for r in roots:
        queue.append(r)
        seen.add(r)
        parent[r] = None
        parent_action[r] = None

        # deadlock sur état initial ?
        if len(successors_with_actions(sem, r)) == 0:
            return [(None, r)]

    while queue:
        s = queue.popleft()

        succ = successors_with_actions(sem, s)
        if len(succ) == 0:
            return reconstruct_trace(s, parent, parent_action)

        for action, ns in succ:
            if ns in seen:
                continue
            seen.add(ns)
            parent[ns] = s
            parent_action[ns] = action
            queue.append(ns)

    return None


def reconstruct_trace(target: State,
                      parent: Dict[State, Optional[State]],
                      parent_action: Dict[State, Optional[str]]) -> List[Tuple[Optional[str], State]]:
    """
    Reconstruit la trace [(action, state)] à partir des dictionnaires parent/parent_action.
    Convention: l'état initial est (None, s0).
    """
    seq: List[Tuple[Optional[str], State]] = []
    cur: Optional[State] = target
    while cur is not None:
        seq.append((parent_action[cur], cur))
        cur = parent[cur]
    seq.reverse()

    # force (None, s0) en premier
    if seq and seq[0][0] is not None:
        seq[0] = (None, seq[0][1])
    return seq


def format_trace(trace: List[Tuple[Optional[str], State]]) -> str:
    """
    Affiche une trace de manière lisible.
    """
    lines = []
    for i, (a, s) in enumerate(trace):
        if i == 0:
            lines.append(f"  s0 = {s}")
        else:
            lines.append(f"  --{a}--> {s}")
    return "\n".join(lines)


def run_model_check(name: str, sem):
    print(f"\n=== {name} : vérification (BFS + trace minimale) ===")

    bad_trace = bfs_find_trace_to_bad_state(sem)
    if bad_trace is None:
        print("Exclusion mutuelle : OK (aucun état CS/CS atteignable)")
    else:
        print("Exclusion mutuelle : VIOLÉE (contre-exemple minimal trouvé)")
        print(format_trace(bad_trace))

    dead_trace = bfs_find_trace_to_deadlock(sem)
    if dead_trace is None:
        print("Deadlock : aucun (sur l'espace atteignable)")
    else:
        print("Deadlock : OUI (trace minimale vers un état sans successeurs)")
        print(format_trace(dead_trace))
        print(f"  deadlock_state = {dead_trace[-1][1]}")


if __name__ == "__main__":
    run_model_check("AB1", AB1LanguageSemantics())
    run_model_check("AB2", AB2LanguageSemantics())
    run_model_check("AB3", AB3LanguageSemantics())
