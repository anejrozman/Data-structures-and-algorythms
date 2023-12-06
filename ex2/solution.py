# Naloga 2: Skladisce  
# Anej Rozman, 27211148
# financna matematika, 3. letnik  
# Python 3.9.7

import sys

def genGraph(shelves):
    '''
    Input: list (str) of shelves
    Output: dictionary (str -> list (str)) of shelves and their neighbors
    '''
    G = {}
    for uv in shelves:
        for wz in shelves: 
            if uv != wz:
                pass
    return G







def solve(shelves, queries, k):
    pass

if __name__ == "__main__":

    # Read input
    data = input()

    with open(data, 'r', encoding='utf-8') as f:
        data.read()
        # Read the first line containing n, p, k
        n, p, k = map(int, f.readline().split())

        # Read the next n lines representing the description of each shelf
        shelves = []
        for _ in range(n):
            shelf = f.readline().strip()
            shelves.append(shelf)

        # Skip the empty line
        f.readline()

        # Read the next p lines representing the queries
        queries = []
        for _ in range(p):
            query = f.readline().strip()
            queries.append(query)

    res = solve(shelves, queries, k)
    print(res)
