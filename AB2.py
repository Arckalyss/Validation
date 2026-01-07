from BFS import RootedGraph

class AB2Graph(RootedGraph):
    def roots(self):
        return [("I", "I", "DOWN", "DOWN")]  # (a, b, flagA, flagB)

    def neighbors(self, v):
        a, b, fA, fB = v
        nxt = []

        # Alice
        if a == "I":
            nxt.append(("W", b, "UP", fB))           # a1
        if a == "W" and fB == "DOWN":
            nxt.append(("CS", b, fA, fB))            # a2
        if a == "CS":
            nxt.append(("I", b, "DOWN", fB))         # a3

        # Bob
        if b == "I":
            nxt.append((a, "W", fA, "UP"))           # b1
        if b == "W" and fA == "DOWN":
            nxt.append((a, "CS", fA, fB))            # b2
        if b == "CS":
            nxt.append((a, "I", fA, "DOWN"))         # b3

        return nxt
