import wx
import os
import time
import xml.etree.ElementTree as ET

from timer import *
from brewlist import *
from settimer import *
from brewclasses import *

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

        self.InitUI()

    def InitUI(self):

        self.wxtimer = wx.Timer(self)

        # menu bar and menu items
        menubar = wx.MenuBar()
        # file menu
        fileMenu = wx.Menu()
        fitem1 = fileMenu.Append(wx.ID_ANY, 'Open', 'Select a File')
        fitem2 = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        # run menu
        runMenu = wx.Menu()
        runitem1 = runMenu.Append(wx.ID_ANY, 'Set', 'Set the timer')


        runitem2 = runMenu.Append(wx.ID_ANY, 'Mash', 'Run Mash Sequence')
        runitem3 = runMenu.Append(wx.ID_ANY, 'Boil', 'Run Boil Sequence')

        menubar.Append(runMenu, '&Timer')

        self.SetMenuBar(menubar)

        # buttons
        self.stbtn = wx.Button(self, label='Start', pos=(200,125))
        self.rbtn = wx.Button(self, label='Reset', pos=(275,125))
        self.cbtn = wx.Button(self, label='Close', pos=(350,125))

        # event bindings
        self.Bind(wx.EVT_MENU, self.recipe.OnShow, fitem1)

        # menu bindings to access mash/boil xml data
        self.Bind(wx.EVT_MENU, self.CallMash, runitem2) # Mash
        self.Bind(wx.EVT_MENU, self.CallBoil, runitem3) # Boil

        ###
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.CallMash)
        ###

        # close the app
        # add close event binding for confirmation dialog !!!
        self.Bind(wx.EVT_MENU, self.OnClose, fitem2)
        self.cbtn.Bind(wx.EVT_BUTTON, self.OnClose)

        # timer bindings
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.wxtimer)
        self.stbtn.Bind(wx.EVT_BUTTON, self.OnRunning)
        self.rbtn.Bind(wx.EVT_BUTTON, self.OnReset)
        self.Bind(wx.EVT_MENU, self.setTimer.OnShow, runitem1)
        # event triggered from save button in SetTimer class
        self.Bind(wx.EVT_BUTTON, self.SetTime)

        # this may need to be a new method to determine the brew type
        # all grain vs. extract, etc.

        # an object to draw the timer in the window client area
        self.dc = wx.ClientDC(self)
        font = wx.Font(30, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.dc.SetFont(font)

        self.SetSize(SIZE)
        self.SetTitle(TITLE)
        self.Centre()
        self.Show(True)

        self.OnRefresh(None)

#################################################################

    def BrewType(self, e):
        """ load a timer based upon the brewing style """

        self.XML = self.recipe.GetRecipe()
        self.TREE = ET.parse(self.XML)
        self.TIMER.GetXML(self.TREE)
        self.brewType = self.TIMER.GetBrewType()
        # need to set up type in
        if self.brewType == 'All Grain':
        # -or- use boolean if Mashable:
           self.CallMash(e)
        else:
           self.CallBoil(e)

    def CallMash(self, e):
        # finish setting this up !!!
        # call new method from timer module to get mash xml data
        print 'testing mash binding'
        try:
            print 'do the thing'

        except:
            print 'do the other thing'

    def CallBoil(self, e):
        # clean this up !!!
        #self.XML = self.recipe.GetRecipe()

        try:
            # access the beer.xml file
            #self.TREE = ET.parse(self.XML)

            # fetch the pertinnt information for the boil
            #self.TIMER.GetXML(self.TREE)
            # set timer with boil time from beer.xml
            boil = self.TIMER.GetBoilTime()
            self.TIMER.Set(boil[0], boil[1])
            # refresh the display
            self.OnRefresh(None)

        except:
            # a messag dialong would nice here !!!
            # message could be: "Please select a recipe first!"

            print 'Testing error handling'

    def OnClose(self, e):
        """ close the app """
        self.recipe.Destroy()
        self.setTimer.Destroy()
        self.Close(True)

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

################################################################

    def Mashable(self):
        """ Returns True if the brew type is All Grain. """
        self.brewType == 'All Grain'
    # Rename? !!!
    def OnTimer(self, e):
        """ Decrement and redraw the timer """
        if self.vals['mn'] >= 0 and self.TIMER.GetStatus():
            # decrement the timer
            self.TIMER.Run()
            # redraw the display
            self.OnRefresh(e)
            # show a hop dialog if necessary
            self.ShowHopDlg()

            # stop once we are at '00:00'
            if self.vals['display'] == '00:00':
                self.TIMER.Stop()
                self.wxtimer.Stop()
                self.stbtn.SetLabel('Start')

    def OnMashTimer(self, e):
        # similar to OnTimer(), but with a different wx.Timer() and
        # mash specific conditions for proceeding to the next mash step
        pass

    def OnRunning(self, e):
        """ Start and stop the timer. """
        # add check to determine which timer to initiate based
        # upon whether or not the brew type is All Grain !!!

        # start the timer unless we are a '00:00'
        if not self.TIMER.GetStatus() and self.vals['display'] != '00:00':
            self.stbtn.SetLabel('Pause')
            self.wxtimer.Start(DELAY)
            self.TIMER.Start()
            self.ShowHopDlg()
        # This may not be needed !!!
        # stop the timer
        else:
            self.TIMER.Stop()
            self.wxtimer.Stop()
            self.stbtn.SetLabel('Start')


############################################################################

    def SetTime(self, e):
        """ Sets the timer with tuple from SetTimer class """
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
