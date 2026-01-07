from BFS import RootedGraph


class AB1Graph(RootedGraph):
    def roots(self):
        return [("I", "I")]  # (stateA, stateB)

    def neighbors(self, v):
        a, b = v
        nxt = []

        # Alice
        if a == "I":
            nxt.append(("CS", b))    # a2
        if a == "CS":
            nxt.append(("I", b))     # a1

        # Bob
        if b == "I":
            nxt.append((a, "CS"))    # b2
        if b == "CS":
            nxt.append((a, "I"))     # b1

        return nxt
