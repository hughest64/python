import xml.etree.ElementTree as ET
# we fetch the file to be parsed
tree = ET.parse('C:/Users/Todd/Desktop/brewsys/recipes/Furious.xml')

# we access the root element of the tree
root = tree.getroot()
recipe = root[0]
hops = recipe.find('HOPS')
allhops = {}
'''for hop in hops.findall('HOP'):
    n = hop.find('NAME').text
    a = str(round(float(hop.find('AMOUNT').text) * 35.274, 2))
    t = hop.find('TIME').text.split('.')[0]
    allhops[int(t)] = (n,a,t)
print allhops
print'''

mash = recipe.find('MASH')
steps = mash.find('MASH_STEPS')
'''mashsteps = {}
for step in steps.findall('MASH_STEP'):
    info = step[:]
    for i in info:
        mashsteps[i.tag] = i.text'''


'''mashsteps = []
for step in steps.findall('MASH_STEP'):
    info = step
    name = info.find('NAME')
    mashsteps.append(name.text)'''

mashsteps = []
for step in steps.findall('MASH_STEP'):
    info = step
    name = info.find('NAME').text
    time = int(float(info.find('STEP_TIME').text))

    tempsplit = info.find('DISPLAY_STEP_TEMP').text.split()
    temp = (int(float(tempsplit[0])))

    elements = (name, time, temp)
    mashsteps.append(elements)












##############################################################333

#print mashsteps.keys()
print
#print mashsteps.items()
print
print mashsteps
'''print
print len(mashsteps.keys())
print
for count, item in enumerate(mashsteps):
    print count, item'''

# finding the strike temp element may be useful











########################################
