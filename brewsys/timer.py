import time
import xml.etree.ElementTree as ET
"""
TODO:
- mash subclass for parsing beer.xml file
"""

class Timer(object):
    """ a collection of timer controls for a brewing system."""
    def __init__(self):
        # defualt values #
        # minutes - (int), second(int)
        self.mn = 0
        self.sec = 0
        # timer reset values - minutes (int), second(int)
        self.resetMn = 0
        self.resetSec = 0
        # False if the timer is not running
        self.status = False
        # Is the current self.mn in a dict of hops?
        self.addition = False

        # add comment !!!
        self.brewtype = ''

    def Set(self, mn, sec):
        """ Setting the timer. """
        # int mn, int sec for the countdown
        self.mn = mn
        self.sec = sec
        # vaues stored away for Reset() method
        self.resetMn = mn
        self.resetSec = sec

    def Run(self):
        """ The actual count down. """
        if self.sec == 0:
            self.mn -= 1
            self.sec = 59

        else:
            self.sec -= 1
        # can be used to set a timer delay
        #time.sleep(1)

    def GetDisplay(self):
        """
        Returns a dict of int mn, int sec, string 'mn:sec'
        """
        # add a '0' to maintain two digit places
        if self.mn < 10:
            strMn = '0' + str(self.mn)
        else:
            strMn = str(self.mn)
        # add a '0' to maintain two digit places
        if self.sec < 10:
           strSec = '0' + str(self.sec)
        else:
           strSec = str(self.sec)

        disp = (strMn + ':' + strSec)
        # dictionary for use in the main program module
        timerVals = {'mn':self.mn, 'sec':self.sec, 'display':disp}
        return timerVals

    def Start(self):
        """ A flag for starting the timer. """
        self.status = True

    def Stop(self):
        """ A flag for stopping the timer. """
        self.status = False

    def GetStatus(self):
        """ Returns the current run status of the timer. """
        return self.status

    def Reset(self):
        """ Resets the timer to previous self.Set value. """
        # stop the timer first
        if self.status:
            self.status = False
        # reset mn/sec values
        self.Set(self.resetMn, self.resetSec)

###################################################################
    ### THIS MUST BE IN THE PARENT FILE WITH A BEER XML ARG ###
    def GetXML(self, t):
        """
        Accesses the the desired hop and boil elements
        of a beer.xml file
        TODO:
        add location of brew type (all grain, extract, etc.)
        """
        # if we have a beer.xml file with wich to work
        try:
            # get the root of the xml tree
            self.root = t.getroot()
            # the hops element
            self.hops = self.root[0][9]
            # the boil eleemnt
            self.boil = self.root[0][7].text
            # the brew type all grain or extract
            self.brewtype = self.root[0][2].text
        # if we don't have a beer.xml file return empty values
        except:
            self.hops = []
            self.boil = 0
            self.brewtype = ''

    def GetBoilTime(self):
       """ Returns the length of the boil as tuple of int, int. """
       boil = (int(float(self.boil)), 0)
       return boil

    def GetBrewType(self):
       return self.brewtype

    def GetHops(self):
        """
        returns a dict with time(int) as the key and a
        tuple of (name(string), amount(int), time(int))
        as the value
        """
        hops = {}
        # if there is a beer.xml file which can be parsed
        try:
            for h in self.hops:
                # time of addition
                t = int(float(h[6].text))
                # amonunt of addition converted to ounces
                a = round(float(h[4].text) * 35.274, 2)
                # name of the hop
                n =  h[0].text
                # a tuple of the collected information
                l = (n,a,t)
                # add them to a dictionary
                hops[t] = l
            return hops
        # return the empty dict if there is no beer.xml file
        except:
            return hops

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

######################################################################

    def GetMashXML(self):
        pass


























# tests
if __name__ == '__main__':

    timer = Timer()
    timer.Set(60, 0)
    tree = ET.parse('C:/Users/Todd/Desktop/brewsys/bsmith/Oktober-16.xml')
    timer.GetXML(tree)
    vals = timer.GetDisplay()
    #print timer.GetHops()
    print timer.GetBoilTime()
    print timer.GetBrewType()
    while vals['mn'] >= 0:
        if timer.AddHop():
            print vals['display']
            print timer.GetAddition()
        timer.Run()
        vals = timer.GetDisplay()

### End of File ###
