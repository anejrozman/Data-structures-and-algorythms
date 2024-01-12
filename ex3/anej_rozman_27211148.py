import sys

class Graph:
    def __init__(self) -> None:
        self.nodes = None
        self.edges = None

    def addNodes(self, num):
        self.nodes = list(range(num))
        self.edges = {i: {} for i in range(num)}

    def addEdge(self, u, v, weight):
        self.edges[u][v] = weight
        self.edges[v][u] = weight

    def removeEdge(self, u, v):
        self.edges[u].pop(v)
        self.edges[v].pop(u)

    def connectedComponents(self):
        visited = set()
        components = []

        def dfs(v, component):
            visited.add(v)
            component.add(v)

            for neighbor in self.edges[v]:
                if neighbor not in visited:
                    dfs(neighbor, component)

        for v in self.nodes:
            if v not in visited:
                component = set()
                dfs(v, component)
                components.append(component)

        return components

    def sortedEdges(self, rev):
        duplicates = set()
        edgeList = [
            (u, v, weight)
            for u in self.edges
            for v, weight in self.edges[u].items()
            if frozenset([u, v]) not in duplicates and not duplicates.add(frozenset([u, v]))
        ]

        return sorted(edgeList, key=lambda x: x[2], reverse=rev)


class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX != rootY:
            if self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            elif self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1


def kruskal(G: Graph):
    t = Graph()
    t.addNodes(len(G.nodes))

    edges = G.sortedEdges(False)
    uf = UnionFind(len(t.nodes))

    for u, v, weight in edges:
        if uf.find(u) != uf.find(v):
            t.addEdge(u, v, weight)
            uf.union(u, v)
    return t


def solve(G, K, vertexWeights):
    t = kruskal(G)

    l = len(t.connectedComponents())

    if l > K:
        print('-1')
        return

    edges = t.sortedEdges(True)[:K - l]
    for u, v, _ in edges:
        t.removeEdge(u, v)

    solution = []

    components = t.connectedComponents()

    for c in components:
        segmentSize = len(c)

        s = sum(vertexWeights)
        segmentWeight = 0
        for v in c:
            s -= v
            segmentWeight += vertexWeights[v] * s

        segmentWeight = round(segmentWeight, 4) if segmentWeight != 0 else 0
        solution.append(f"{segmentSize},{segmentWeight}")

    solution.sort(key=lambda x: (int(x.split(',')[0]), float(x.split(',')[1])), reverse=True)

    print('\n'.join(solution))


if __name__ == "__main__":
    G = Graph()

    inputLines = sys.stdin.readlines()
    for c, line in enumerate(inputLines):
        line = [float(x) for x in line.strip().split(',')]

        if c == 0:
            G.addNodes(int(line[0]))
            K = int(line[2])
        elif c == 1:
            vertexWeights = line
        else:
            G.addEdge(int(line[0]), int(line[1]), weight=line[2])

    solve(G, K, vertexWeights)
