import wx
import time
"""
things to think about:
- do we want the burner cycle to run when the timer is paused?
  - probaly
- overide method to run everything manually?
- separate cycle(method) for timing the sparker?
  - shut everything off if not lit in x seconds
"""


class MashController(wx.Frame): # change to inerit from object for actual class!!!
    """
    A class to control temperature inputs for a brewing system.
    """
    def __init__(self, *args, **kwargs):
        # a Brew class instance representing temp events from an Arduino
        super(MashController, self).__init__(*args, **kwargs)
        
        self.brew        = Brew(self)
        self.atemp       = self.brew.temp # actual temp(from sensor)

        self.sttemp      = 0         # strike water temp        
        self.mtemp       = 0         # desired mash temp(from xml)
        self.act_sp_temp = 0         # actual sparge water temp(from sensor)
        self.diff        = 0         # amount above mash temp to set stemp
        self.sptemp      = 0         # sparge water temp
        
        self.heat        = False     # a flag to control whether or not to fire a burner
        self.sol         = False     # state of the solenoiod(False is closed state)
        self.spark       = False     # state of sparker
        self.fire        = False     # is the burner lit?
        
        # a binding to get the new value
        self.Bind(wx.EVT_BUTTON, self.TempCheck)

    def HeatStrike(self):
        # open solenoiod
        # fire burner
        # heat strike water to self.sttemp
        # close solenoid
        pass

    def HeatMash(self):
        """
        Used when self.atemp is more that 1 degree lower
        than self.mtemp or to go to the next mash step
        """
        print "Let's get it fired up!"
        self.diff = 20
        self.heat = True
        # if SpargeEvent triggered periodically, it may not need to be called here
        self.SpargeEvent(None)

    def TooHot(self):
        print "the temp is too damn high!"
        # This can probably be done directly in TempCheck()
        self.heat = False

    def Maintain(self):
        self.diff = 10
        self.heat = True
        print "We cool"

    def TempCheck(self, e):
        """
        This will need an event to check self.atemp periodically.
        """
        self.atemp = brew.GetTemp()
        
        if self.atemp == '<low condition>': # and timer display != '00:00'            
            self.HeatMash() 
            # -or-
            #self.diff = 20
            #self.heat = True
            #print "Let's get it fired up!"

        elif self.atemp == '<high condition>': # and timer display != '00:00'            
            self.TooHot()
            # -or-
            #self.heat = False
            #print "the temp is too damn high!"

        else:            
            self.Maintain()
            # -or-
            #self.diff = 10
            #self.heat = True
            #print "We cool"

    def SpargeEvent(self, e):
        """
        This will need an event to check self.act_sp_temp
        """
        # heat water to self.sptemp and maintain +/- 2 degrees        
        if self.heat:
            # if we are -2 degrees below desired temp
            #and self.atemp < self.mtemp - x degrees?
            if self.act_sp_temp < self.mtemp + self.diff - 2:
                # set/start a spark timer?               
                self.FireBurner()
                
            elif self.act_sp_temp > self.mtemp + self.diff + 2:
                # make sure the soloenoid is closed and we aren't sparking
                self.sol = False
                
        def FireBurner(self):
            """
            Start the burner or just allow it to continue to run.
            """
            self.sol = True
            
            if not self.fire:
                # self.SparkTimer()?
                self.spark = True
                
        def SparkTimer(self, sec):
            """
            Can this be another instace of the Timer class?
            - may need to get the threading module involved!!!
            """
            # time how long we try to SparkTimer
            # set is_lit = True if runs out?
            # this would allow a 'saftey' of sorts
            pass
        
#-----------------------------------------------------------------------------------          
            
class Brew(wx.Frame):
    """ 
    Test class to emulate passing temp events to 
    the MashController class. (Pretend it's an Arduino.)
    """
    def __init__(self, *args, **kwargs):
        super(Brew, self).__init__(*args, **kwargs)
        
        self.temp = 0
        
        panel = wx.Panel(self)
        
        self.num = wx.wx.SpinCtrl(panel, size=(60, -1))
        self.btn = wx.Button(panel, label='Save')
        
        self.btn.Bind(wx.EVENT_BUTTON, self.OnSave)
        
        self.SetSize((100, 100))
        self.SetTitle('Brew Temps')
        self.Centre()
        self.Show()
        
        
        def OnSave(self, e):
            self.temp = self.num.GetValue()
            e.skip()
            print self.temp
            
        def GetTemp(self):
            return self.temp
