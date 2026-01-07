class AB3Graph(RootedGraph):
    def roots(self):
        return [("I", "I", "DOWN", "DOWN")]

    def neighbors(self, v):
        a, b, fA, fB = v
        nxt = []

        # Alice (identique AB2)
        if a == "I":
            nxt.append(("W", b, "UP", fB))           # a1
        if a == "W" and fB == "DOWN":
            nxt.append(("CS", b, fA, fB))            # a2
        if a == "CS":
            nxt.append(("I", b, "DOWN", fB))         # a3

        # Bob (AB2 + b4)
        if b == "I":
            nxt.append((a, "W", fA, "UP"))           # b1
        if b == "W" and fA == "DOWN":
            nxt.append((a, "CS", fA, fB))            # b2
        if b == "CS":
            nxt.append((a, "I", fA, "DOWN"))         # b3
        if b == "W" and fA == "UP":
            nxt.append((a, "I", fA, "DOWN"))         # b4 (back off)

        return nxt
