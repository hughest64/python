def satisfiesF(L):    
    L2 = []
    for x in L:
        if f(x) == True:
            L2.append(x)
        
    L = L2
    return len(L)
