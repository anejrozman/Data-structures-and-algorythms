# Naloga 2: Skladisce  
# Anej Rozman, 27211148
# financna matematika, 3. letnik  
# Python 3.9.7

import sys
import heapq

#------------------------------------------------------------------------------#

def dist(p1, p2):
    '''
    Input: two points in the form (x, y)
    Output: distance between points
    TC: O(1)
    '''
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

#------------------------------------------------------------------------------#

def onSegment(p1, p2, p):
    '''
    Input: three points in the form (x, y)
    Output: True if p is on line segment p1p2, False otherwise
    TC: O(1)
    '''
    return min(p1[0], p2[0]) <= p[0] <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= p[1] <= max(p1[1], p2[1])

#------------------------------------------------------------------------------#

def direction(p1, p2, p3):
    '''
    Input: three points in the form (x, y)
    Output: direction of p3 from line p1p2
    TC: O(1)
    '''
    return (p3[0] - p1[0]) * (p2[1] - p1[1]) - (p2[0] - p1[0]) * (p3[1] - p1[1])

#------------------------------------------------------------------------------#

def intersect(p1, p2, p3, p4):
    '''
    Input: two edges in the form (x1, y1), (x2, y2); (x3, y3), (x4, y4)
    Output: True if edges intersect, False otherwise
    TC: O(1)
    '''
    d1 = direction(p3, p4, p1)
    d2 = direction(p3, p4, p2)
    d3 = direction(p1, p2, p3)
    d4 = direction(p1, p2, p4)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) \
        and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    elif d1 == 0 and onSegment(p3, p4, p1):
        return True
    elif d2 == 0 and onSegment(p3, p4, p2):
        return True
    elif d3 == 0 and onSegment(p1, p2, p3):
        return True
    elif d4 == 0 and onSegment(p1, p2, p4):
        return True
    else:
        return False
    
#------------------------------------------------------------------------------#

def isEdgeValid(start, end, rectangles, opt=0):
    '''
    Input: start and end coordinates of edge, list of rectangles
    Output: True if edge passes through <= 1 rectangle, False otherwise
    TC: O(n), where n is the number of rectangles
    '''
    #if intersect(start, end, (0, 0), (0, 100)) or intersect(start, end, (0, 0), (100, 0)) \
    #    or intersect(start, end, (100, 0), (100, 100)) or intersect(start, end, (0, 100), (100, 100)):
    #    return False
    c = 0
    for rectangle in rectangles:
        p1, p2, p3, p4 = rectangle
        if intersect(start, end, p1, p2) or intersect(start, end, p2, p3) \
        or intersect(start, end, p3, p4) or intersect(start, end, p4, p1):
            c += 1
    return c <= opt + 2

#------------------------------------------------------------------------------#

def addEdges(v, vertices, rectangles):
    '''
    Input: vertex u in the form (x, y)
    Output: dictionary of neighbors connected to u with edge weights
    TC: O(n), where n is the number of rectangles
    '''
    neighbors = {}
    for u in vertices:
        if u != v and isEdgeValid(u, v, rectangles):
            neighbors[u] = dist(u, v)
    return neighbors

#------------------------------------------------------------------------------#

def genGraph(rectangles, k):
    '''
    Input: Vertices in the form (x, y)
    Output: dictionary (str -> list (str)) for graph of shelf paths
    TC = O(n^2), where n is the number of rectangles
    '''
    G = {}
    vertices = [v for rec in rectangles for v in rec]
    vertices.extend([(0, 0), (100, 100)])
    for v in vertices:
        G[v] = addEdges(v, vertices, rectangles)
    return G


#------------------------------------------------------------------------------#

def dijkstra(G, start):
    '''
        Input: graph in form {str -> list (str)}, start vertex
        Output: dictionary (str -> float) of distances from start to each vertex
        TC: O((|V| + |E|)log|V|), where |V| is the number of vertices and |E| is the number of edges
    '''
    dist = {node: float('inf') for node in G}
    dist[start] = 0
    pred = {node: None for node in G}
    
    # Priority queue of vertices to visit
    priorityQ = [(0, start)]

    while priorityQ:
        currentDistance, currentNode = heapq.heappop(priorityQ)

        # Check if the current path is shorter than the stored distance
        if currentDistance > dist[currentNode]:
            continue

        for neighbor, weight in G[currentNode].items():
            distance = currentDistance + weight

            # Update the distance and predecessor if a shorter path is found
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                pred[neighbor] = currentNode
                heapq.heappush(priorityQ, (distance, neighbor))

    return dist, pred

#------------------------------------------------------------------------------#

def alg1(item, G):
    '''
        Input: item coordinates (x, y), graph G
        Output: shortest path from (0, 0) to (100, 100) that item is on
        TC: 2x Dijkstra's algorithm so O((|V| + |E|)log|V|)
    '''
    l1, d1 = dijkstra(G, (0, 0))
    l2, d2 = dijkstra(G, item)
    return l1[item] + l2[(100, 100)]

#------------------------------------------------------------------------------#

def solve(rectangles, items, k):
    G = genGraph(rectangles, k)
    out = []
    if k == 0:
        for item in items:
            out.append(alg1(item, G))
    else:
        pass
    out = '\n'.join(map(str, out))
    print(out)


#------------------------------------------------------------------------------#

if __name__ == "__main__":

    params = None
    rectangles = []
    items = []

    # Read input
    c = 0
    for line in sys.stdin:

        if line == "\n":
            c = 1
            continue

        # Read coordinates
        coord = [float(x) for x in line.strip().split(',')]

        # First line contains parameters
        if params is None:
            params = coord
        
        # Add rectangles and items
        elif c == 0:
            rectangles.append(
                [(coord[0], coord[1]),  #bottom left corner
                (coord[0], coord[3]),   #top left corner
                (coord[2], coord[3]),   #top right corner
                (coord[2], coord[1])]   #bottom right corner
            )
        else:
            items.append((coord[0], coord[1]))
            
    solve(rectangles, items, params[2])


#rectangle1 = [(5, 5), (5, 15), (15, 15), (15, 5)]
#rectangle2 = [(20, 10), (20, 20), (30, 20), (30, 10)]
#rectangle3 = [(35, 5), (35, 15), (45, 15), (45, 5)]
#
## Combine all rectangles into a single list
#all_rectangles = [rectangle1, rectangle2, rectangle3]
#
#edgesToVisit = [(5, 15), (30, 20), (45, 15)]
#
#solve(all_rectangles, edgesToVisit, 0)