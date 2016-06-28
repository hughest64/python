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
