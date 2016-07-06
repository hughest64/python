aList = [1, [2, 3], [4, 5, 6]]

def flatten(aList):
    newList = []
    if aList == []:
        return newList
    else:
        if type(aList[0]) == list:
            newList = flatten(aList[0])
        else:
            newList = [aList[0]]
        return newList + flatten(aList[1:])
