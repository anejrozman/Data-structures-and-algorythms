# Naloga 4: Dekodiranje
# Anej Rozman, 27211148
# financna matematika, 3. letnik  
# Python 3.9.7

import sys

#------------------------------------------------------------------------------#

def solve(s):

    # Base case
    if len(s) == 1: print(m[s]); return

    curr, prev = m[s[0]], 1

    for i in range(1, len(s)):
        newCurr = (m[s[i]]*curr + m.get(s[i-1:i+1],0)*prev) % M
        prev, curr = curr, newCurr
        if not curr: print(0); return
        
    print(newCurr)        

#------------------------------------------------------------------------------#

if __name__ == "__main__":

    # Read input
    s = sys.stdin.read().strip()

    # Mod
    M = 10**9 + 7
    
    # Set up map 
    m = {'0':0, '*': 9, '**': 15, '1*': 9, '2*': 6}
    m.update({str(i):1 for i in range(1, 27)})
    m.update({"*"+str(i):(2 if i<7 else 1) for i in range(10)})
    
    # Solve
    solve(s)