def isPalindrome(aString):
    '''
    assumes aString is a string of lower case leters with no spaces or punctuation.
    '''
    if len(aString) <= 1:
        return True
    else:
       return aString[0] == aString[-1] and isPalindrome(aString[1: -1])
