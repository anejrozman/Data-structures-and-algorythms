# Naloga 4: 
# Anej Rozman, 27211148
# financna matematika, 3. letnik  
# Python 3.9.7

import sys

#------------------------------------------------------------------------------#

M = 10 ** 9 + 7
def solve(s):
    first = 1
    second = 9 if(s[0] == '*') else(0 if(s[0] == '0') else 1)
 
    for i in range(1,len(s)):
 
        temp = second
 
        # If s[i] == '*' there can be
        # 9 possible values of *
        if (s[i] == '*'):
            second = 9 * second
 
            # If previous character is 1
            # then words that can be formed
            # are K(11), L(12), M(13), N(14)
            # O(15), P(16), Q(17), R(18), S(19)
            if (s[i - 1] == '1'):
                second = (second + 9 * first) % M
 
            # If previous character is 2
            # then the words that can be formed
            # are U(21), V(22), W(23), X(24)Y(25), Z(26)
            elif (s[i - 1] == '2'):
                second = (second + 6 * first) % M
 
            # If the previous digit is * then
            # all 15 2- digit characters can be
            # formed
            elif (s[i - 1] == '*'):
                second = (second + 15 * first) % M
         
        # If s[i] != '*'
        else:
 
            second = second if(s[i] != '0') else 0
 
            # Adding first in second
            # if s[i-1]=1
            if (s[i - 1] == '1'):
                second = (second + first) % M
 
            # Adding first in second if
            # s[i-1] == 2 and s[i]<=l           
            elif (s[i - 1] == '2' and s[i] <= '6'):
                second = (second + first) % M
 
            # if s[i-1] == '*' the union
            # of above 2 cases has to be done
            elif (s[i - 1] == '*'):
                second = (second + (2 if(s[i] <= '6') else 1) * first) % M
        first = temp
    print(second)

#------------------------------------------------------------------------------#

if __name__ == "__main__":

    # Read input
    s = sys.stdin.read()
    
    solve(s)