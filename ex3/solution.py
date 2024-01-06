# Naloga 2: Segmenti 
# Anej Rozman, 27211148
# financna matematika, 3. letnik  
# Python 3.9.7


import sys
import networkx as nx # Upam da je dovoljeno, cene lahko implementiram svojo verzijo, ker itak ne uporabim kaj dosti funkcij
#import matplotlib.pyplot as plt


#------------------------------------------------------------------------------#

def kruskal(G):
    '''
        Return a minimum spanning tree using Kruskal's algorithm.
        TC: O(E log E)
    '''
    t = nx.Graph()

    # Add all nodes to the minimum spanning tree
    t.add_nodes_from(G.nodes)

    # Get a sorted list of edges based on weights
    edges = sorted(G.edges(data=True), 
                   key=lambda x: x[2]['weight'])

    # Kruskal's algorithm
    for e in edges:
        u, v, weight = e
        # Check if adding the edge creates a cycle in the minimum spanning tree
        if not nx.has_path(t, u, v):
            # Add the edge to the minimum spanning tree
            t.add_edge(u, v, weight=weight['weight'])

    return t

#------------------------------------------------------------------------------#

def solve(G, K, vertexWeights):
    '''
        Solve the problem.
    '''
    # Get the minimum spanning tree
    t = kruskal(G)

    ##Plot the graph G
    #pos = nx.spring_layout(G) 
    #nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='lightblue', font_color='black', font_size=8, node_size=800)
    #plt.show()
    #
    ## Plot the minimum spanning tree
    #pos = nx.spring_layout(t)  
    #nx.draw(t, pos, with_labels=True, font_weight='bold', node_color='lightblue', font_color='black', font_size=8, node_size=800)
    #plt.show()

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

    sol = ''
    
    # Get the new components of the minimum spanning tree
    components = list(nx.connected_components(t))
    for c in sorted(components, key=len, reverse=True):
        segmentSize = str(len(c)) 
        segmentWeight = 0
        for v in c:
            for u in c:
                if u != v:
                    segmentWeight += vertexWeights[u] * vertexWeights[v]
        sol += segmentSize +',' + str(round(segmentWeight / 2, 4)) + '\n'
    print(sol.strip())

#------------------------------------------------------------------------------#

if __name__ == "__main__":

    # Initialize graph
    G = nx.Graph()

    # Read input
    c = 0
    for line in sys.stdin:

        # Read line
        line = [float(x) for x in line.strip().split(',')]

        if c == 0:
            G.add_nodes_from(range(int(line[0])))
            K = int(line[2])

        elif c == 1:
            vertexWeights = line

        else:
            G.add_edge(int(line[0]), int(line[1]), weight=line[2])
        c += 1

    solve(G, K, vertexWeights)