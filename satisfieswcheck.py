

def checkExpect(func, ans):
    '''
    a function for testing other functions
    func: function with given arguments 
    ans: the expected result of evaluating func
    returns a  string 
    '''
    if func != ans:
        #show the actual result of func and what was expected
        print 'The value, ' + str(func), 
        print ' differs from the expected value, ' + str(ans)
    else:
        # the evaluation of func matches the expected answer
        print 'The test passed!'

#______________________________________________________________#

def f(s): #s is a string
    return 'a' in s
      
def satisfiesF(L): 
    '''
    mutate L to contain only values of s that are already in L
    do this by making f(s) return True
    '''
    def satisfiesF(L):  
    L2 = list(L)
    for s in L=2:
        if f(s) == False:
            L.remove(s)
    return len(L)
    
#satisfiesF(['a', 'b', 'a']) #single test

# multiple tests      
checkExpect(satisfiesF(['a', 'b', 'a']), 2)
checkExpect(satisfiesF(['a', 'a', 'a']), 3)
checkExpect(satisfiesF([]), 0)
checkExpect(satisfiesF(['c', 'b', 'af']), 1)
checkExpect(satisfiesF(['a', 'b', 'da']), 2)
checkExpect(satisfiesF(['f', 'q', 'j', 'd', 'e', 'l']), 0)
