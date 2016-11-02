import time
import xml.etree.ElementTree as ET
"""
TODO:
- Think about error handling of Get methods
- Rename some methods as noted
- Add methods for temp control as necessary
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
        self.mashsteps = [] # should mn and sec be args for this?

    def Set(self, mn=0, sec=0):
        """ Setting the timer. """
        # we make sure to only set the timer with integers
        assert type(mn) == int and type(sec) == int,\
               'Set() must be called with type int!'

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

#----------------------------------------------

    def SetXML(self, t):
        # future needed elements can easily be added in here
        tree = ET.parse(t)
        self.recipe = tree.getroot()[0]
        # change this to .fine method!!!
        self.hops = self.recipe[9]              #list of hop additions
        mash = self.recipe.find('MASH')         #mash tag
        self.steps = mash.find('MASH_STEPS')    #list of mash steps

        self.boil = self.recipe[7].text         #boil time
        self.brewtype = self.recipe[2].text     #brew type

        self.SetMashSteps()
        self.SetHops()

    def SetMashSteps(self):
        '''
        other elements to consider:
        TYPE, INFUSE_AMOUNT, DECOCTION_AMOUNT, INFUSE_TEMP

        type = 'string TYPE'                        #use to determine if it's a temp, decoct, or infusion step
        strikevol = 'int or float INFUSE_AMOUNT'    #really only need this from first step if temp mashing
        striketemp = 'int INFUSE_TEMP'              #really only need this from first step if temp mashing
        '''
        self.mashsteps = []
        # should this have a try/except?!!!
        for step in self.steps:
            name = step.find('NAME').text
            time = int(float(step.find('STEP_TIME').text))

            tempsplit = step.find('DISPLAY_STEP_TEMP').text.split('.')
            temp = int(tempsplit[0])

            elements = (name, time, temp)
            self.mashsteps.append(elements)

    def SetHops(self):
        self.boil_hops = {}
        self.first_wort = []
        self.dry_hop = [] # may not use this!!!

        #try:
        for hop in self.hops:
            name =  hop[0].text
            amt = round(float(hop[4].text) * 35.274, 2)
            time = int(float(hop[6].text))
            use = hop[5].text
            l = (name, amt, time, use)

            if use == 'First Wort':
                self.first_wort.append(l)

            elif use == 'Dry Hop':
                self.dry_hop.append(l)

            elif time not in self.boil_hops:
                self.boil_hops[time] = [l]

            else:
                self.boil_hops[time].append(l)

        #except:
            #print '<what should this do?>\
                    # \nthere was an error'

    def GetMashSteps(self):
        return self.mashsteps

    def GetBoilHops(self):
        return self.boil_hops

    def GetAddition(self):
        hop = self.boil_hops[self.mn]
        return hop

    def AddHop(self):
        if self.mn in self.boil_hops.keys():
            self.addition = True

        else:
            self.addition = False

        return self.addition

    def GetFirstWort(self):
        return self.first_wort

    def GetDryHop(self):
        return self.dry_hop

    def GetAllSteps(self):
        all_steps = {'Mash':self.mashsteps, 'Firstwort':self.first_wort,
                     'Boil':self.boil_hops, 'Dryhop':self.dry_hop}
        return all_steps

    def GetRecipeName(self):
        name = self.recipe[0].text
        return name

    def GetBoilTime(self): # change this to .find method!!!
        boil = int(float(self.recipe[7].text))
        return boil

    def GetBrewType(self): # change this to .fine method!!!
        brew = self.recipe[2].text
        return brew


# tests
if __name__ == '__main__':
    fpath = 'C:/Users/Todd/Desktop/brewsys/recipes/Furious.xml'
    timer = Timer()
    timer.SetXML(fpath)
    mash = timer.GetMashSteps()
    everything = timer.GetAllSteps()

    print everything
