# Naloga 2: Skladisce  
# Anej Rozman, 27211148
# financna matematika, 3. letnik  
# Python 3.9.7

import sys
import heapq

# Da malo zagovarjam casovno zahtevnost, ce je k == 0 potem po grafu s 4N vozlisci pozenemo 
# Floyd Warshallov algoritem torej O(N³) in po tem poiscemo ustrezne dolzine. 
# Ce pa je k > 0 pozenemo dijkstraMod, ki je v najslabsem primeru O((k + 1)N³) (ker ga poznenemo 
# na O(n) vozliscih in pregledamo k + 1 moznosti za posebne povezave).
# Naloge sem se lotil, da sem resil primere s k = 0 in potem 
# prilagodil vse za k > 0. Ko pogledam za nazaj je bil to grozen pristop in bi lahko 
# marsikaj izobljsal, najbolj pa verjetno generiranje in predstavitev grafa.

#------------------------------------------------------------------------------#

def dist(p1, p2):
    '''
    Input: two points in the form (x, y) \n
    Output: distance between points \n
    TC: O(1)
    '''
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

#------------------------------------------------------------------------------#

def onSegment(p1, p2, p3): 
    '''
    Input: three points in the form (x, y) \n
    Output: True if p2 is on segment p1p3, False otherwise \n
    TC: O(1)
    '''
    if ((p2[0] <= max(p1[0], p3[0])) and (p2[0] >= min(p1[0], p3[0])) and 
           (p2[1] <= max(p1[1], p3[1])) and (p2[1] >= min(p1[1], p3[1]))): 
        return True
    return False
    
#------------------------------------------------------------------------------#

def orientation(p1, p2, p3): 
    '''
        Input: three points in the form (x, y) \n
        Output: 0 if p1, p2, p3 are collinear, 1 if clockwise, 2 if counterclockwise \n
        TC: O(1)
    '''      
    val = (float(p2[1] - p1[1]) * (p3[0] - p2[0])) - (float(p2[0] - p1[0]) * (p3[1] - p2[1])) 
    if val > 0:  # Clockwise orientation 
        return 1
    elif val < 0: # Counterclockwise orientation 
        return 2
    else: # Collinear orientation 
        return 0

#------------------------------------------------------------------------------#

def intersect(p1,q1,p2,q2): 
    '''
        Input: four points in the form (x, y) \n
        Output: True if line segments p1q1 and p2q2 intersect, False otherwise \n
        TC: O(1)
    '''      
    # Find the 4 orientations required for  
    # the general and special cases 
    o1 = orientation(p1, q1, p2) 
    o2 = orientation(p1, q1, q2) 
    o3 = orientation(p2, q2, p1) 
    o4 = orientation(p2, q2, q1) 
  
    # General case 
    if ((o1 != o2) and (o3 != o4)): 
        return True
  
    # Special Cases 
    # p1, q1 and p2 are collinear and p2 lies on segment p1q1 
    if ((o1 == 0) and onSegment(p1, p2, q1)): 
        return True
  
    # p1, q1 and q2 are collinear and q2 lies on segment p1q1 
    if ((o2 == 0) and onSegment(p1, q2, q1)): 
        return True
  
    # p2, q2 and p1 are collinear and p1 lies on segment p2q2 
    if ((o3 == 0) and onSegment(p2, p1, q2)): 
        return True
  
    # p2, q2 and q1 are collinear and q1 lies on segment p2q2 
    if ((o4 == 0) and onSegment(p2, q1, q2)): 
        return True
    
    return False

#------------------------------------------------------------------------------#

def edgeOnRectangle(start, end, rec, opt):
    '''
        Input: start and end coordinates of edge, rectangle coordinates, optional parameter \n
        for number of rectangles edge can pass through \n
        Output: True if edge is on rectangle, False otherwise
        TC: O(1)
    '''
    # Get rectangle coordinates
    p1, p2, p3, p4 = rec

    # Check if edge is on the border and on rectangle
    if (start == p1 and end == p2 and intersect(start, end, (0, 0), (0, 100))) or \
        (start == p1 and end == p4 and intersect(start, end, (0, 0), (100, 0))) or \
        (start == p2 and end == p1 and intersect(start, end, (0, 0), (0, 100))) or \
        (start == p2 and end == p3 and intersect(start, end, (0, 100), (100, 100))) or \
        (start == p3 and end == p2 and intersect(start, end, (0, 100), (100, 100))) or \
        (start == p3 and end == p4 and intersect(start, end, (100, 100), (100, 0))) or \
        (start == p4 and end == p1 and intersect(start, end, (0, 0), (100, 0))) or \
        (start == p4 and end == p3 and intersect(start, end, (100, 100), (100, 0))):
        return opt == 1, 1
    
    # Check if edge is on rectangle
    if (start == p1 and (end == p2 or end == p4)) or \
        (start == p2 and (end == p1 or end == p3)) \
        or (start == p3 and (end == p2 or end == p4)) \
        or (start == p4 and (end == p1 or end == p3)):
        return True, 0
  
    # Check if edge is inside rectangle
    if (start in [p1, p3] and end in [p1, p3]) \
        or (start in [p2, p4] and end in [p2, p4]):
        return opt == 1, 1
    
#------------------------------------------------------------------------------#

def isEdgeValid(start, end, rectangles, opt):
    '''
    Input: start and end coordinates of edge, list of rectangles, optional parameter 
    for number of rectangles edge can pass through \n
    Output: True if edge passes through <= opt rectangles, False otherwise \n
    TC: O(n), where n is the number of rectangles
    '''
    c = 0
    for rec in rectangles:
        # If edge is on rectangle, easy to check
        if start in rec and end in rec:
            return edgeOnRectangle(start, end, rec, opt)
        p1, p2, p3, p4 = rec

        # If one of the points is on rectangle
        if start in rec or end in rec:
            c1 = 0
            if intersect(start, end, p1, p2):
                c1 += 1
            if intersect(start, end, p2, p3):
                c1 += 1
            if intersect(start, end, p3, p4):
                c1 += 1
            if intersect(start, end, p4, p1):
                c1 += 1
            if c1 > 2:
                c += 1
    
        # All other cases (points are not on rectangle)
        elif intersect(start, end, p1, p2) or intersect(start, end, p2, p3) \
            or intersect(start, end, p3, p4) or intersect(start, end, p4, p1):
            c += 1
    return c <= opt, 1 if c > 0 else 0
   
#------------------------------------------------------------------------------#

def addEdges(v, vertices, rectangles, opt):
    '''
    Input: vertex u in the form (x, y) \n
    Output: dictionary of neighbors connected to u with edge weights \n
    TC: O(n²), where n is the number of rectangles
    '''
    neighbors = {}
    for u in vertices:
        if u != v:
            res, special = isEdgeValid(u, v, rectangles, opt)
            if res:
                neighbors[u] = (dist(u, v), special)
    return neighbors

#------------------------------------------------------------------------------#

def genGraph(rectangles, k):
    '''
    Input: Vertices in the form (x, y) \n
    Output: dictionary {(x, y) -> dict} for graph of shelf paths \n
    TC = O(n³), where n is the number of rectangles
    '''
    G = {}
    opt = 0 if k == 0 else 1

    # Make list of vertices 
    vertices = [v for rec in rectangles for v in rec]
    vertices.extend([(0, 0), (100, 100)])

    # Add edges
    for v in vertices:
        G[v] = addEdges(v, vertices, rectangles, opt)
    return G

#------------------------------------------------------------------------------#

def floydWarshall(G):
    '''
        Input: graph in form {(x, y) -> dict} \n
        Output: distance matrix, vertex mapping \n  
        TC: O(N³)
    '''
    vertices = list(G.keys())
    numVertices = len(vertices)
    
    # Distance matrix
    dist = [[0] * numVertices for _ in range(numVertices)]
    
    # Map matrix indices to vertices
    vertexMap = {vertices[i]: i for i in range(numVertices)}

    # Fill matrix with edge weights
    for i in range(numVertices):
        for j in range(numVertices):
            if i == j:
                dist[i][j] = 0
            elif vertices[j] in G[vertices[i]]:
                dist[i][j] = G[vertices[i]][vertices[j]][0]
            else:
                dist[i][j] = float('inf')

    # Floyd-Warshall 
    for k in range(numVertices):
        for i in range(numVertices):
            for j in range(numVertices):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist, vertexMap

#------------------------------------------------------------------------------#

def dijkstraMod(G, start, k):
    '''
        Input: graph in form {(x, y) -> dict}, start vertex, max number of special edges \n
        Output: dictionary ((x, y) -> float) of distances from start to each vertex \n
        TC: worst case O(N²)
    '''
    # Initialize distances
    distances = {node: {k: float('inf') for k in range(round(k + 1))} for node in G}
    distances[start][0] = 0  

    priorityQ = [(0, 0, start)]  # (distance, numSpecialEdges, node)
    
    while priorityQ:
        currDist, numSpecialEdges, currNode = heapq.heappop(priorityQ)

        # Check if the current path is not the best
        if currDist > distances[currNode][numSpecialEdges]:
            continue

        for neighbor, (weight, isSpecial) in G[currNode].items():
            newDistance = currDist + weight
            newSpecialEdges = numSpecialEdges + isSpecial

            # Update if the new path is better
            if newSpecialEdges <= k and newDistance < distances[neighbor][newSpecialEdges]:
                distances[neighbor][newSpecialEdges] = newDistance
                heapq.heappush(priorityQ, (newDistance, newSpecialEdges, neighbor))

    return distances

#------------------------------------------------------------------------------#
def solve(rectangles, items, k):
    '''
        Input: list of rectangles, list of items, number of 'tunnelings' k \n
        Output: shortest path for each item \n
        TC: if k = 0, O(N³), if k > 0 O((k + 1)N³)
    '''
    G = genGraph(rectangles, k) #O(N³)
    out = []
    if k == 0:
        dist, vertexMap = floydWarshall(G) #O(N³)
        for item in items:
            out.append(
                dist[vertexMap[(0, 0)]][vertexMap[item]] +
                dist[vertexMap[item]][vertexMap[(100, 100)]]
                )
    else:
        start = dijkstraMod(G, (0, 0), k) #O(N²)
        for item in items:
            middle = dijkstraMod(G, item, k)
            minimum = start[item][0] + middle[(100, 100)][k]
            for i in range(1, round(k + 1)):
                if start[item][i] + middle[(100, 100)][k - i] < minimum:
                    minimum = start[item][i] + middle[(100, 100)][k - i]
            out.append(minimum) # whole TC: O((k + 1)N³))
    out = '\n'.join(map(str, out))
    #print(dist)
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


