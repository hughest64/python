import wx

class MashController(wx.Frame): # change to inerit vrom object for actual class
    """
    A class to control temperature inputs for a brewing system.
    """
    def __init__(self): 
        # a Brew class instance representing temp events from an Arduino
        brew = Brew()

        self.sttemp      = 0         # strike temp
        self.atemp       = brew.temp # actual temp(from sensor)
        self.mtemp       = 0         # desired temp(from xml)
        self.act_sp_temp = 0         # actual sparge water temp(from sensor)
        self.diff        = 0         # amount above mash temp to set stemp
        self.sptemp      = 0         # sparge water temp
        
        self.heat        = False     # a flag to control whether or not to fire a burner
        self.sol         = False     # state of the solenoiod(False is closed state)
        self.spark       = False     # state of sparker
        
        # a binding to get the new value
        self.bind(EVT_BUTTON, self.TempCheck)

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
        # if this is triggered periodically, this may not need to be called
        self.SpargeEvent(None)

    def TooHot(self):
        print "the temp is too damn high!"
        # should this change self.diff? If so,
        # it can probably be deprecated
        self.heat = False

    def Maintain(self):
        self.diff = 10
        self.heat = False
        print "We cool"

    def TempCheck(self, e):
        """
        This will need an event to check self.atemp periodically.
        """
        self.atemp = brew.GetTemp()
        
        if self.atemp == '<low condition>': # and timer display != '00:00'
            self.HeatMash()

        elif self.atemp == '<high condition>': # and timer display != '00:00'
            self.TooHot()

        else:
            self.Maintain()

    def SpargeEvent(self, e):
        """
        This will need an event to check self.act_sp_temp
        """
        # heat water to self.sptemp and maintain +/- 2 degrees
        
        if self.heat:
            # if we are -2 degrees below desired temp
            #and self.atemp < self.mtemp - x degrees?
            if self.act_sp_temp < self.mtemp + self.diff - 2:
                # open solenoid
                self.sol = True
                # fire burner, this will need to be timed to stop after x seconds!!!
                self.spark = True
                
            elif self.act_sp_temp > self.mtemp + self.diff + 2:
                # make sure the soloenoid is closed and we aren't sparking
                self.sol = False
                self.spark = False
                
            else:
                self.heat = False
            
#-----------------------------------------------------------------------------------          
            
class Brew(wx.Frame):
    """ 
    Test class to emulate passing temp events to 
    the MashController class. (Pretend it's an Arduino.)
    """
    def __init__(self, *args, **kwargs):
        super(World, self).__init__(*args, **kwargs)
        
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
