def checkExpect(func, ans):
''' a function for testing other functions
    takes in a function with given arguments and an expected answer.
    evaluates true if the func evaluation matches the expected answer'''
    if func != ans:
        #show the actual result of func and what was expected
        print 'The value, ' + str(func) + ' differs from the expected value, ' + str(ans)
    else:
        print 'The test passed!'
