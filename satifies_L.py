def satisfiesF(L):    
    for s in L:
        if f(s) == False:
            L.remove(s)
    return len(L)
