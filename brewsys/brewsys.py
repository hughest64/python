import wx
import xml.etree.ElementTree as ET

from timer import *
from brewlist import *
from settimer import *

### CONSTANTS ###
SIZE = ((640, 480))
TITLE = 'Brewsys'
DELAY = 1000

class World(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(World, self).__init__(*args, **kwargs)

        self.TIMER = Timer()
        self.setTimer = SetTimer(self)
        self.recipe = Recipe(self)
        self.mashSteps = []
        self.mashFlag = False

        self.InitUI()

    def InitUI(self):

        self.wxtimer = wx.Timer(self)
        self.mashTimer = wx.Timer(self)

        # menu bar and menu items
        menubar = wx.MenuBar()
        # file menu
        fileMenu = wx.Menu()
        fitem1 = fileMenu.Append(wx.ID_ANY, '&Open', 'Select a File')
        fitem2 = fileMenu.Append(wx.ID_EXIT, '&Exit', 'Exit application')
        # run menu
        runMenu = wx.Menu()
        runitem1 = runMenu.Append(wx.ID_ANY, '&Set', 'Set the timer')
        runitem2 = runMenu.Append(wx.ID_ANY, '&Mash', 'Run Mash Sequence')
        runitem3 = runMenu.Append(wx.ID_ANY, '&Boil', 'Run Boil Sequence')

        menubar.Append(fileMenu, '&File')
        menubar.Append(runMenu, '&Timer')

        self.SetMenuBar(menubar)

        # buttons
        self.stbtn = wx.Button(self, label='Start', pos=(200,125))
        self.rbtn = wx.Button(self, label='Reset', pos=(275,125))
        # depricate? !!!
        self.cbtn = wx.Button(self, label='Close', pos=(350,125))

        # an object to draw the timer in the window client area
        self.dc = wx.ClientDC(self)
        font = wx.Font(30, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.dc.SetFont(font)

        # event bindings
        self.Bind(wx.EVT_MENU, self.recipe.OnShow, fitem1)
        self.Bind(wx.EVT_MENU, self.BrewType, runitem2) # Mash
        self.Bind(wx.EVT_MENU, self.CallBoil, runitem3) # Boil

        self.Bind(wx.EVT_LISTBOX_DCLICK, self.BrewType)

        # close the app
        # add close event binding for confirmation dialog !!!
        self.Bind(wx.EVT_MENU, self.OnClose, fitem2)
        self.cbtn.Bind(wx.EVT_BUTTON, self.OnClose)

        # timer bindings
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.wxtimer)
        self.Bind(wx.EVT_TIMER, self.OnMashTimer, self.mashTimer)

        self.stbtn.Bind(wx.EVT_BUTTON, self.OnRunning)
        self.rbtn.Bind(wx.EVT_BUTTON, self.OnReset)
        self.Bind(wx.EVT_MENU, self.setTimer.OnShow, runitem1)
        # event triggered from save button in SetTimer class
        self.Bind(wx.EVT_BUTTON, self.SetTime)

        self.SetSize(SIZE)
        self.SetTitle(TITLE)
        self.Centre()
        self.Show(True)

        self.OnRefresh(None)

#################################################################

    def BrewType(self, e):
        """ load a timer based upon the brewing style """
        try:
            self.XML = self.recipe.GetRecipe()
            self.TREE = ET.parse(self.XML)
            self.TIMER.GetXML(self.TREE)
            self.brewType = self.TIMER.GetBrewType()
            self.mashSteps = self.TIMER.GetMashSteps()[:]
            if self.Mashable:
               self.CallMash(e)

        except:
           self.CallBoil(e)

    def CallMash(self, e):

        if self.mashSteps != []:
            self.mashFlag = True
            step = self.mashSteps.pop(0)
            self.TIMER.Set(step[1], 0)
            self.OnRefresh(None)
        else:
            self.CallBoil(None)
            self.mashFlag = False

    def CallBoil(self, e):
        self.mashFlag = False
        try:
            boil = self.TIMER.GetBoilTime()
            self.TIMER.Set(boil[0], boil[1])
            # refresh the display
            self.OnRefresh(None)

        except:
            # a messag dialong would nice here !!!
            # message could be: "Please select a recipe first!"
            pass

    def Mashable(self):
        """ Returns True if the brew type is All Grain. """
        return self.brewType == 'All Grain'

################################################################

    def OnRefresh(self, e):
        """ Reset the display. """
        # a dict of {mn=int, sec=int, display=string}
        self.vals = self.TIMER.GetDisplay()
        # clear the previous inforamtion
        self.dc.Clear()
        # redraw the new information
        self.dc.DrawText(self.vals['display'], 260, 50)

    def OnReset(self, e):
        """ Reset the timer """
        self.stbtn.SetLabel('Start')
        self.TIMER.Reset()
        self.OnRefresh(e)

    def OnClose(self, e):
        """ close the app """
        self.recipe.Destroy()
        self.setTimer.Destroy()
        self.Destroy()

    def OnTimer(self, e):
        # rename RunTimer? !!!
        """ Decrement and redraw the timer """
        # stop once we are at '00:00'
        if self.vals['display'] == '00:00':
            self.TIMER.Stop()
            self.wxtimer.Stop()
            self.stbtn.SetLabel('Start')

        if self.vals['mn'] >= 0 and self.TIMER.GetStatus():
            # decrement the timer
            self.TIMER.Run()
            # redraw the display
            self.OnRefresh(e)
            # show a hop dialog if necessary
            self.ShowHopDlg()

    def OnMashTimer(self, e):
        """ doc string """
        # rename RunMashTimer? !!!
        # stop once we are at '00:00'
        if self.vals['display'] == '00:00':
            self.TIMER.Stop()
            self.mashTimer.Stop()
            self.stbtn.SetLabel('Start')
            self.CallMash(None)

        if self.vals['mn'] >= 0 and self.TIMER.GetStatus():
            # decrement the timer
            self.TIMER.Run()
            # redraw the display
            self.OnRefresh(e)


    def OnRunning(self, e):
        """ Start and stop the timer. """
        # rename OnTimerSta#t?
        # split this into two methods? !!!
        # - add OnMashTimerStart? !!!
        # upon wether or not the brew type is All Grain !!!
        if self.Mashable and self.mashFlag:
        # start the timer unless we are a '00:00'
            if not self.TIMER.GetStatus() and self.vals['display'] != '00:00':
                self.stbtn.SetLabel('Pause')
                self.mashTimer.Start(DELAY)
                self.TIMER.Start()

            # stop the timer
            else:
                self.TIMER.Stop()
                self.mashTimer.Stop()
                self.stbtn.SetLabel('Start')

        else:
            if not self.TIMER.GetStatus() and self.vals['display'] != '00:00':
                self.stbtn.SetLabel('Pause')
                self.wxtimer.Start(DELAY)
                self.TIMER.Start()
                self.ShowHopDlg()
            else:
                self.TIMER.Stop()
                self.wxtimer.Stop()
                self.stbtn.SetLabel('Start')

############################################################################

    def SetTime(self, e):
        # can this be used elsewhere? !!!
        """ Sets the timer with tuple from SetTimer class """
        if self.TIMER.GetStatus():
            self.OnRunning(None)

        vals = self.setTimer.GetTime()
        self.TIMER.Set(vals[0], vals[1])
        self.OnRefresh(e)

###########################################################################

    def HopDlg(self):
        """ Dialog box for a reminder to add some hops """
        # a string to display hop information
        msg = self.GetMessage()
        # the dialog box object
        dlg = wx.MessageDialog(self, msg, "Hop Addition",
                               wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def GetMessage(self):
        """ Information about one hop from the beer.xml doc. """
        # a tuple of (name(string), amount(int), time(int)) for a hop
        s = self.TIMER.GetAddition()
        return '{2} Minutes!\n Add {1} oz of {0}'.format(s[0], s[1], s[2])

    def ShowHopDlg(self):
        # show the hop dialog when it's time to add hops
        if self.TIMER.AddHop() and self.TIMER.GetHops() != {}:
            self.HopDlg()




if __name__ == '__main__':
    app = wx.App()
    World(None)
    app.MainLoop()
