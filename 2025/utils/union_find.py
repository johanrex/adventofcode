class UnionFind:
    """
    Implements the canonical UnionFind data structure with path compression and union by size.
    Use when you need to efficiently track and merge disjoint sets.
    Uses 0-based indexing for elements. This means you typically need to map your elements to 0-based integers first.
    """

    def __init__(self, n: int):
        if n <= 0:
            raise ValueError("n must be positive")
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        # returns the representative root of the set containing x

        # Path compression: flattens the tree for future queries
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]  # path halving
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        # Returns True if merged; False if already in the same set
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False

        # Union by size: attach smaller tree under larger tree
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        return self.find(a) == self.find(b)

    def component_size(self, x: int) -> int:
        return self.size[self.find(x)]


# Example use:
# uf = UnionFind(5)      # elements: 0..4
# uf.union(0, 1)
# uf.union(3, 4)
# assert uf.connected(0, 1)
# assert not uf.connected(1, 2)
# uf.union(1, 2)
# assert uf.connected(0, 2)
# print("components:", uf.components)         # e.g., 2
# print("size of set containing 0:", uf.component_size(0))  # e.g., 3
