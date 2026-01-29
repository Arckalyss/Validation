# soup/alicebob_languagesemantics.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Union

from languagesemantics import LanguageSemantics


# --- Types d'états ---
AB1State = Tuple[str, str]                          # (a, b)
AB2State = Tuple[str, str, str, str]                # (a, b, fA, fB)


def violates_mutual_exclusion(state) -> bool:
    """
    Propriété de sûreté (safety) : exclusion mutuelle.
    On viole si Alice et Bob sont en section critique en même temps.
    Fonctionne pour AB1 (a,b) ou AB2/AB3 (a,b,fA,fB).
    """
    a = state[0]
    b = state[1]
    return (a == "CS") and (b == "CS")


class AB1LanguageSemantics(LanguageSemantics):
    """
    Version sémantique de AB1.
    Etat: (a,b) avec a,b in {I,CS}
    Actions: a1,a2,b1,b2
    """

    def initials(self) -> List[AB1State]:
        return [("I", "I")]

    def actions(self, state: AB1State) -> List[str]:
        a, b = state
        acts: List[str] = []

        # Alice
        if a == "CS":
            acts.append("a1")  # CS -> I
        if a == "I":
            acts.append("a2")  # I -> CS

        # Bob
        if b == "CS":
            acts.append("b1")  # CS -> I
        if b == "I":
            acts.append("b2")  # I -> CS

        return acts

    def execute(self, state: AB1State, action: str) -> List[AB1State]:
        a, b = state

        if action == "a1" and a == "CS":
            return [("I", b)]
        if action == "a2" and a == "I":
            return [("CS", b)]

        if action == "b1" and b == "CS":
            return [(a, "I")]
        if action == "b2" and b == "I":
            return [(a, "CS")]

        # Action non applicable -> aucun successeur
        return []

    def is_solution(self, state: AB1State) -> bool:
        # Ici on cherche un contre-exemple : "solution" = état mauvais.
        return violates_mutual_exclusion(state)


class AB2LanguageSemantics(LanguageSemantics):
    """
    Version sémantique de AB2.
    Etat: (a,b,fA,fB)
    Actions: a1,a2,a3,b1,b2,b3
    """

    def initials(self) -> List[AB2State]:
        return [("I", "I", "DOWN", "DOWN")]

    def actions(self, state: AB2State) -> List[str]:
        a, b, fA, fB = state
        acts: List[str] = []

        # Alice
        if a == "I":
            acts.append("a1")
        if a == "W" and fB == "DOWN":
            acts.append("a2")
        if a == "CS":
            acts.append("a3")

        # Bob
        if b == "I":
            acts.append("b1")
        if b == "W" and fA == "DOWN":
            acts.append("b2")
        if b == "CS":
            acts.append("b3")

        return acts

    def execute(self, state: AB2State, action: str) -> List[AB2State]:
        a, b, fA, fB = state

        # Alice
        if action == "a1" and a == "I":
            return [("W", b, "UP", fB)]
        if action == "a2" and a == "W" and fB == "DOWN":
            return [("CS", b, fA, fB)]
        if action == "a3" and a == "CS":
            return [("I", b, "DOWN", fB)]

        # Bob
        if action == "b1" and b == "I":
            return [(a, "W", fA, "UP")]
        if action == "b2" and b == "W" and fA == "DOWN":
            return [(a, "CS", fA, fB)]
        if action == "b3" and b == "CS":
            return [(a, "I", fA, "DOWN")]

        return []

    def is_solution(self, state: AB2State) -> bool:
        return violates_mutual_exclusion(state)


class AB3LanguageSemantics(AB2LanguageSemantics):
    """
    AB3 = AB2 + backoff Bob (b4).
    """

    def actions(self, state: AB2State) -> List[str]:
        acts = super().actions(state)
        a, b, fA, fB = state

        # Bob backoff
        if b == "W" and fA == "UP":
            acts.append("b4")

        return acts

    def execute(self, state: AB2State, action: str) -> List[AB2State]:
        if action == "b4":
            a, b, fA, fB = state
            if b == "W" and fA == "UP":
                return [(a, "I", fA, "DOWN")]
            return []
        return super().execute(state, action)
