import time
import xml.etree.ElementTree as ET
"""
TODO:
- mash subclass for parsing beer.xml file
"""

class Timer(object):
    """ a collection of timer controls for a brewing system."""
    def __init__(self, mn=0, sec=0):
        self.mn = mn
        self.sec = sec
        self.resetMn = mn
        self.resetSec = sec

        self.status = False
        self.addition = False

        self.brewtype = ''
        self.mashsteps = []

    # should there be an assert to force setting with an int? !!!
    def Set(self, mn=0, sec=0):
        """ Setting the timer. """
        self.mn = mn
        self.sec = sec

        self.resetMn = mn
        self.resetSec = sec

    def Run(self):
        """ The actual count down. """
        if self.sec == 0:
            self.mn -= 1
            self.sec = 59

        else:
            self.sec -= 1

    def Start(self):
        """ A flag for starting the timer. """
        self.status = True

    def Stop(self):
        """ A flag for stopping the timer. """
        self.status = False

    def Reset(self):
        """ Resets the timer to previous self.Set value. """
        self.Set(self.resetMn, self.resetSec)

    def GetDisplay(self):
        """
        Returns a dict of int mn, int sec, string 'mn:sec'
        """
        display = '{:02d}:{:02d}'.format(self.mn, self.sec)

        return display
    # rename IsRunning() !!!
    def GetStatus(self):
        """ Returns the current run status of the timer. """
        return self.status

###################################################################

    def GetXML(self, t):
        """
        Accesses the the desired hop and boil elements
        of a beer.xml file
        TODO:
        add location of brew type (all grain, extract, etc.)
        """
        # if we have a beer.xml file with wich to work
        try:
            # get the recipe element of the xml tree
            self.recipe = t.getroot()[0]
            # the hops element
            self.hops = self.recipe[9]
            # the boil element
            self.boil = self.recipe[7].text
            # the brew type all grain or extract
            self.brewtype = self.recipe[2].text
            # the mash steps
            mash = self.recipe.find('MASH')
            steps = mash.find('MASH_STEPS')
            
            self.mashsteps = []
            for step in steps.findall('MASH_STEP'):

                name = step.find('NAME').text
                time = int(float(step.find('STEP_TIME').text))

                tempsplit = step.find('DISPLAY_STEP_TEMP').text.split()
                temp = (int(float(tempsplit[0])))
                
                # alternative:
                #tempsplit = step.find('DISPLAY_STEP_TEMP').text.split('.')
                #temp = (int(tempsplit[0]))
               
                elements = (name, time, temp)
                self.mashsteps.append(elements)

        # otherwise return empty values
        except:
            self.hops = []
            self.boil = 0
            self.brewtype = ''
            self.mashsteps = []

    def GetBrewType(self):
        return self.brewtype

    def GetBoilTime(self):
        """ Returns the boil time as tuple of (int mn int sec) """
        boil = int(float(self.boil))
        return boil

    def GetHops(self):
        """
        returns a dict with time(int) as the key and a
        tuple of (name(string), amount(int), time(int))
        as the value
        """
        self.boil_hops = {}
        self.first_wort = []
        # if there is a beer.xml file which can be parsed
        try:
            for h in self.hops:
                use = h[5].text
                if use != 'Dry Hop':
                    # time of addition
                    t = int(float(h[6].text))
                    # amonunt of addition converted to ounces
                    a = round(float(h[4].text) * 35.274, 2)
                    # name of the hop
                    n =  h[0].text
                    # a tuple of the collected information
                    l = (n, a, t, use)

                    if use == 'First Wort':
                        self.first_wort.append((n, a, 'FW', use))
                    # add them to a dictionary
                    elif t not in self.boil_hops.keys():
                        # add to to a dictionary inside a list
                        self.boil_hops[t] = [l]
                    else:
                        # otherwise append it to the list
                        self.boil_hops[t].append(l)

            return self.boil_hops
        # return the empty dict if there is no beer.xml file
        except:
            return self.boil_hops

    def GetFirstWort(self):
        return self.first_wort

    def GetAddition(self):
        """
        returns a single hop additon as
        tuple of (name, amt, time)?
        """

        hops = self.GetHops() # our dict of hops
        hop = hops[self.mn]   # values from the current time

        return hop

    def AddHop(self):
        """
        Returns True if the current self.mn value
        is a key in dict from GetHops()
        """
        if self.mn in self.GetHops() and self.sec == 0:
            self.addition = True
        else:
            self.addition = False

        return self.addition

    def GetMashSteps(self):
        return self.mashsteps
#---------------------------------------------------------------------

    def GetAllSteps(self):
        self.GetHops()
        all_steps = {'Mash':self.mashsteps, 'Firstwort':self.first_wort,
                     'Boil':self.boil_hops}

        return all_steps



# tests
if __name__ == '__main__':

    timer = Timer()
    timer.Set(8, 3)
    tree = ET.parse('C:/Users/Todd/Desktop/brewsys/recipes/Furious.xml')
    timer.GetXML(tree)
    hops = timer.GetHops()
    print hops
    hop = timer.GetAddition()
    print hop
    fw = timer.GetFirstWort()
    print fw
    steps = timer.GetAllSteps()
    print steps
    print timer.GetDisplay()['display']
