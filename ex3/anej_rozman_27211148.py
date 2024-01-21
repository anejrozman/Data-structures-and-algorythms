# Naloga 3: Segmenti 
# Anej Rozman, 27211148
# financna matematika, 3. letnik  
# Python 3.9.7


import sys

# Po veckratnem podrobnem pregledu funckij menim da je casovna zahtevnost pod mejo v navodilih. Ampak
# vecji primeri se vedno porabijo prevec casa za izvajanje. Upam da nisem naredil napake. Verjamem 
# pa, da bi lahko marsikaj izboljsal, saj sem naknadno implementiral grafe, da nadomestim knjiznjico 
# networx. V prihodnosti bi predlagal da v navodila podate priblizno koliko casa naj bi vzeli 
# primeri (vecji in manjsi).

#------------------------------------------------------------------------------#

# Implementation of a graph data structure similar to networx

class Graph:

    def __init__(self) -> None:
        self.nodes = None
        self.edges = None

    def addNodes(self, num): 
        self.nodes = [i for i in range(num)]
        self.edges = {i:{} for i in range(num)}

    def addEdge(self, u, v, weight):   # O(1)
        self.edges[u][v] = weight
        self.edges[v][u] = weight
            
    def removeEdge(self, u, v): # O(1)
        del self.edges[u][v]
        del self.edges[v][u]

    def connectedComponents(self): # O(V + E)
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
    
    def sortedEdges(self, rev): # O(E log E)
        duplicates = set()
        edgeList = []
        for u in self.edges:
            for v, weight in self.edges[u].items():
                if frozenset([u, v]) in duplicates:
                    continue 
                duplicates.add(frozenset([u, v]))
                edgeList.append((u, v, weight))
        
        return sorted(edgeList, key=lambda x: x[2], reverse=rev) 
        
#------------------------------------------------------------------------------#
    
class UnionFind:

    def __init__(self, n): 
        self.parent = [i for i in range(n)]
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
        
#------------------------------------------------------------------------------#

def kruskal(G:Graph):
    '''
        Input: graph G \n
        Output: minimum spanning tree using Kruskal's algorithm. \n
        TC: O(E log E)
    '''
    t = Graph()
    t.addNodes(len(G.nodes))
    
    edges = G.sortedEdges(False)
    uf = UnionFind(len(t.nodes))

    for u, v, weight in edges:
        if uf.find(u) != uf.find(v):
            t.addEdge(u, v, weight)
            uf.union(u, v)
    return t

#------------------------------------------------------------------------------#

def solve(G, K, vertexWeights):
    '''
        Input: graph G, integer K, list of vertex weights \n
        Output: print the number of segments in each cluster and the total weight of each cluster \n
        TC: O(E log E)
    '''
    # Get the minimum spanning tree
    t = kruskal(G)

    # Get the number of components in the minimum spanning tree
    l = len(t.connectedComponents())

    # Check if solution is possible
    if l > K:
        print('-1')
        return
    
    # Remove the most expensive edges
    edges = t.sortedEdges(True)
    for e in edges[:K - l]:
        t.removeEdge(e[0], e[1])

    solution = []
    
    # Get the new components of the minimum spanning tree
    components = t.connectedComponents()

    # Calculate solution
    for c in components:
        segmentSize = len(c)
        s = sum(vertexWeights)
        segmentWeight = 0
        for v in c:
            s -= v
            segmentWeight += vertexWeights[v] * s

        segmentWeight = round(segmentWeight, 4) if segmentWeight != 0 else 0
        solution.append(f"{segmentSize},{segmentWeight}")

    def customKey(s):
        parts = s.split(',')
        return (int(parts[0]), float(parts[1]))
    
    solution = sorted(solution, key=customKey, reverse=True)

    print('\n'.join(solution))

#------------------------------------------------------------------------------#

if __name__ == "__main__":

    # Initialize graph
    G = Graph()

    # Read input
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
