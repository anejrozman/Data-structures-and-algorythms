# Naloga 1: Kavbojci    
# Anej Rozman, 27211148
# financna matematika, 3. letnik  
# Python 3.9.7


# O(n) implementation using stack
def cowboysR(li):
    '''
    Input: list (int) of heights 
    Output: list (int) indexes of cowboys that get shot from the right
    '''
    s = []
    res = [None] * len(li)
    for i in range(len(li)):
        while s and li[i] >= li[s[-1]]:
            j = s.pop()
            res[j] = i  
        s.append(i)
    return res

def cowboysL(li):
    '''
    Input: list (int) of heights 
    Output: list (int) indexes of cowboys that get shot from the left
    '''
    s = []
    res = [None] * len(li)
    for i in range(len(li) - 1, -1, -1):
        while s and li[i] >= li[s[-1]]:
            j = s.pop()
            res[j] = i  
        s.append(i)
    return res


def duel(li):
    L = cowboysL(li)
    R = cowboysR(li)
    L = ' '.join(map(str, L))
    R = ' '.join(map(str, R))
    return L, R


if __name__ == "__main__":
    # Read input
    data = input()

    # Change data type
    data = data.split(' ')
    data = list(map(int, data))

    # Run solution
    L,R = duel(data)
    print(L,'\n',R, sep='')




    
