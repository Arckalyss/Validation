#ls2rg.py
from rootedgraph import RootedGraph


class LS2RG(RootedGraph):
    """
    Adaptateur : LanguageSemantics -> RootedGraph
    """

    def __init__(self, semantics):
        self._sem = semantics

    def roots(self):
        return self._sem.initials()

    def neighbors(self, state):
        succ = []
        for action in self._sem.actions(state):
            for ns in self._sem.execute(state, action):
                succ.append(ns)
        return succ
