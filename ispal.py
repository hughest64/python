def isPalindrome(aString):
    '''
    assumes aString is a string of lower case leters with no spaces or punctuation.
    '''
    if len(aString) <= 1:
        return True
    else:
       return aString[0] == aString[-1] and isPalindrome(aString[1: -1])
       
       
       
       
def isPalindrome(aString):
    '''
    converts and string to just lower case letters.
    '''
    def makeLower(aString):
        aString = aString.lower()
        ans =''
        alpha = 'abcdefghijklmnopqrstuvwxyz'
        for letter in aString:
            if letter in alpha:
                ans += letter
        return ans
        
    def isPal(aString):    
        if len(aString) <= 1:
            return True
        else:
            return aString[0] == aString[-1] and isPal(aString[1: -1])
            
    return isPal(makeLower(aString))
