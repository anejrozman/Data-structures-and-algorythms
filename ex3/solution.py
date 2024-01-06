# Naloga 2: Segmenti 
# Anej Rozman, 27211148
# financna matematika, 3. letnik  
# Python 3.9.7


import sys
from itertools import combinations
import networkx as nx
from networkx.utils import UnionFind

#------------------------------------------------------------------------------#

def kruskal(G):
    '''
        Input: graph G \n
        Output: minimum spanning tree using Kruskal's algorithm. \n
        TC: O(E log E)
    '''
    t = nx.Graph()
    t.add_nodes_from(G.nodes)
    
    edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    uf = UnionFind(t.nodes)

    for u, v, weight in edges:
        if uf[u] != uf[v]:
            t.add_edge(u, v, weight=weight['weight'])
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
    l = len(list(nx.connected_components(t)))
    if l > K:
        print('-1')
        return
    
    edges = sorted(t.edges(data=True), 
                   key=lambda x: x[2]['weight'], 
                   reverse=True)
    
    for e in edges[:K - l]:
        t.remove_edge(e[0], e[1])

    sol = []
    
    # Get the new components of the minimum spanning tree
    components = list(nx.connected_components(t))
    for c in components:
        segmentSize = len(c)
        segmentWeight = sum(vertexWeights[u] * vertexWeights[v] for u, v in combinations(list(c), 2))
        segmentWeight = round(segmentWeight, 4) if segmentWeight != 0 else 0
        sol.append(f"{segmentSize},{segmentWeight}")

    def custom_key(s):
        parts = s.split(',')
        return (int(parts[0]), float(parts[1]))
    
    sol = sorted(sol, key=custom_key, reverse=True)

    print('\n'.join(sol))

#------------------------------------------------------------------------------#

if __name__ == "__main__":

    # Initialize graph
    G = nx.Graph()

    # Read input
    for c, line in enumerate(sys.stdin):
        line = [float(x) for x in line.strip().split(',')]

        if c == 0:
            G.add_nodes_from(range(int(line[0])))
            K = int(line[2])
        elif c == 1:
            vertexWeights = line
        else:
            G.add_edge(int(line[0]), int(line[1]), weight=line[2])

    solve(G, K, vertexWeights)
