def isPalindrome(aString):
    '''
    assumes aString is a string of lower case leters with no spaces or punctuation.
    '''
    if len(aString) <= 1:
        return True
    else:
        if aString[0] == aString[-1]:
            return isPalindrome(aString[1: -1])
        else:
            return False
