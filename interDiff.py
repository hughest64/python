def dict_interdiff(d1, d2):
    interDict = {}
    diffDict = {}
    for key in d1.keys():
        if key in d2.keys():
            interDict[key] = f(d1[key], d2[key])
            #print interDict
        elif key not in d2.keys():
            diffDict[key] = d1[key]
    for key in d2.keys():
        if key not in d1.keys():
            diffDict[key] = d2[key]
            
    return (interDict, diffDict)
