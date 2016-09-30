import wx
import xml.etree.ElementTree as ET

from timer import *
from systests import *
# the file to be parsed
'''tree = ET.parse('C:/Users/Todd/Desktop/brewsys/bsmith/Oktober-16.xml')
# the root element of the tree
root = tree.getroot()
# element where all the useful things are
recipe = root[0]
# accessing the mash element
mash = recipe.find('MASH')
steps = mash.find('MASH_STEPS')
# a dictionary to contain all of the mash step info
mashsteps = {}
for step in steps.findall('MASH_STEP'):
    info = step[:]
    for i in info:
        mashsteps[i.tag] = i.text'''
#####################################################################
### IDEAS FOR MASHING ###
# finding the strike temp element may be useful
"""
TODO:
- move the xml stuff above to timer.py
- setup MashTimer var once timer.py is updated
1. when file is loaded:
 - time is set for the first step time
 - hit start button to fire the burners and start heating
 - send an alert when strike temp is reached and shut off burner
2. after mash in:
 - hit start to start timer and initialize temp control cycle
 - ability to pause and abort automatic control
3: when step is done:
 - start reset timer to next step time
 - fire burners and heat to next step temp
4: when next step temp is reached:
 - start timer automatically
 - reenter temp control cycle
"""
# will be bound to MashTimer sublass from timer.py !!!
MASH = Mash()
#TIMER.Set(5,0)
# create a new class for mash setup
#MASH = Timer()
#MASH.Set(5,2)
class Mash(World):
    """ Inherit from the World superclass. """
    def __init__(self, *args, **kwargs):
        super(Mash, self).__init__(*args, **kwargs)
        self.TIMER = MASH

        # Set method for TimerType class can be
        # used her to set a MashTimer()!!!
        #self.InitUI()

    #def InitUI(self):
        """ Set up the interface """
        panel = SetMashTimer(self)

        # buttons
        self.stbtn = wx.Button(self, label='Start', pos=(200,125))
        rbtn = wx.Button(self, label='Reset', pos=(275,125))
        cbtn = wx.Button(self, label='Close', pos=(350,125))

        # the menu system
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitemOne = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        fitemTwo = fileMenu.Append(wx.ID_ANY, 'Set', 'Set the timer')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        # an object to draw the timer in the window client area
        self.dc = wx.ClientDC(self)
        font = wx.Font(30, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.dc.SetFont(font)

        # intializing the wx.Timer()
        self.wxtimer = wx.Timer(self)
        # an instance of the SetTimer class
        settimer = SetTimer(self)

        # event bindings
        self.Bind(wx.EVT_MENU, self.OnClose, fitemOne)
        self.Bind(wx.EVT_MENU, settimer.OnShow, fitemTwo)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.wxtimer)
        self.stbtn.Bind(wx.EVT_BUTTON, self.OnRunning)
        cbtn.Bind(wx.EVT_BUTTON, self.OnClose)
        rbtn.Bind(wx.EVT_BUTTON, self.OnReset)
        self.Bind(wx.EVT_BUTTON, self.OnSaveClick)

        # set display details
        self.SetSize(SIZE)
        self.SetTitle(TITLE)
        self.Centre()
        self.Show(True)
        # used to set the timer from the beer xml file
        #self.TIMER.Set(BOILTIME, 0)
        # draw the initial timer
        self.vals = self.TIMER.GetDisplay()
        self.dc.DrawText(self.vals['display'], 260, 50)
### unique methods/objects: ###
 # - OnTimer override World class version
 # - OnRunning override World class version
 # - OnRefresh override World class version ?
 # - start/pause button needs extra bindings
 # - temp cycle control - THIS IS A BIG ONE!
 # - auto ramping
 # - switching to manual control

    def OnTimer(self, e):
        """ Decrement and redraw the timer """
        if self.vals['mn'] >= 0 and self.TIMER.GetStatus():
            # decrement the timer
            self.TIMER.Run()
            # change for mash !!!
            #self.ShowHopDlg()
            # redraw the display
            self.OnRefresh(e)

            # stop once we are at '00:00'
            if self.vals['display'] == '00:00':
                self.TIMER.Stop()
                self.wxtimer.Stop()
                self.stbtn.SetLabel('Start')

    def OnRunning(self, e):
        """ Start and stop the timer. """

        # start the timer unless we are a '00:00'
        if not self.TIMER.GetStatus() and self.vals['display'] != '00:00':
            self.stbtn.SetLabel('Pause')
            self.wxtimer.Start(DELAY)
            self.TIMER.Start()
            # change for mash!!!
            #self.ShowHopDlg()
        # stop the timer
        else:
            self.TIMER.Stop()
            self.wxtimer.Stop()
            self.stbtn.SetLabel('Start')

    def OnSaveClick(self, e):
        """ Received wx.EVT_BUTTON event from SetTimer class. """
        print "This is the Mash class!"
        self.OnRefresh(e)

class SetMashTimer(SetTimer):
    def __init__(self, *args, **kwargs):
        super(SetMashTimer, self).__init__(*args, **kwargs)
        self.TIMER = MASH

    def OnShow(self, e):
        """ Show the window """
        self.sc1.SetValue(5)
        self.sc2.SetValue(2)
        self.Show(True)

    def OnSave(self, e):
        """
        Apply the new timer values, close the window,
        and propigate the event to the class.
        """
        mn = self.sc1.GetValue()
        sec = self.sc2.GetValue()
        self.TIMER.Set(mn, sec)
        print "sending event with {}, {} from the Mash class".format(mn, sec)
        e.Skip()
        self.Hide()

    def OnSaveClick(self, e):
        """ Propigate the event to the World class """
        print "event received, sending to Mash"

        e.Skip()


# run the app
if __name__ == '__main__':
    #TIMER = Timer()
    wo = wx.App()
    Mash(None)
    wo.MainLoop()
### end of file ###
