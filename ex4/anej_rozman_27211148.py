# Naloga 4: 
# Anej Rozman, 27211148
# financna matematika, 3. letnik  
# Python 3.9.7

import sys

#------------------------------------------------------------------------------#

def solve(s):
    if len(s) == 0:
        return 0
    res = 9 if s[0] == '*' else 1
    prev = s[0]
    for i in range(1, len(s)):

        prev = s[i]
        
    print(res % (10^9 + 7))

#------------------------------------------------------------------------------#

if __name__ == "__main__":

    # Read input
    s = sys.stdin.read()
    
    solve(s)