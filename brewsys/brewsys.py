import wx
import xml.etree.ElementTree as ET

from timer import *
from brewlist import *
from settimer import *

app = wx.App()

### CONSTANTS ###
SIZE = (640, 480)
TITLE = 'Brewsys'
DELAY = 1000
# depricate once list population is complete!!!
TESTLIST = ['step 1', 'step 2', 'step 3',
            'Remove this param']

TMR_PT_SIZE = 40
LBL_PT_SIZE = 12
LST_PT_SIZE = 10
TIMER_FONT = wx.Font(TMR_PT_SIZE, wx.ROMAN, wx.NORMAL, wx.BOLD)
LABEL_FONT = wx.Font(LBL_PT_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL)
LIST_FONT = wx.Font(LST_PT_SIZE, wx.SWISS, wx.NORMAL, wx.NORMAL)
VGAP = 10
HGAP = 10
BORDER = 20
BTN_SIZE = (90, 30)

class World(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(World, self).__init__(*args, **kwargs)

        self.setTimer = SetTimer(self)
        self.recipe = Recipe(self)

        self.wx_timer = wx.Timer(self)
        self.TIMER = Timer()
        self.vals = self.TIMER.GetDisplay()

        self.mash_steps = []
        self.mash_flag = False
        self.boil_flag = True
        self.step_count = 0

        self.InitUI()

        self.SetSize(SIZE)
        self.SetTitle(TITLE)
        self.Centre()
        self.Show()

    def InitUI(self):

        panel = wx.Panel(self)
        grid = wx.GridBagSizer(VGAP, HGAP)
        vbox = wx.BoxSizer(wx.VERTICAL)
        # menu bar and menu items
        menubar = wx.MenuBar()
        # file menu
        fileMenu = wx.Menu()
        fitem1 = fileMenu.Append(wx.ID_ANY, '&Open', 'Select a File')
        fitem2 = fileMenu.Append(wx.ID_EXIT, '&Exit', 'Quit Brewing')
        # run menu
        runMenu = wx.Menu()
        runitem1 = runMenu.Append(wx.ID_ANY, '&Set', 'Set the timer')
        runitem2 = runMenu.Append(wx.ID_ANY, '&Mash', 'Run Mash Sequence')
        runitem3 = runMenu.Append(wx.ID_ANY, '&Boil', 'Run Boil Sequence')

        menubar.Append(fileMenu, '&File')
        menubar.Append(runMenu, '&Timer')

        self.SetMenuBar(menubar)

        step_text = wx.StaticText(panel, label="Step Text")
        step_text.SetFont(LABEL_FONT)
        grid.Add(step_text, pos=(0, 1), flag=wx.ALIGN_CENTER)

        self.time_text = wx.StaticText(panel, label='00:00')
        self.time_text.SetFont(TIMER_FONT)
        grid.Add(self.time_text, pos=(1, 1), flag=wx.ALIGN_CENTER)

        mashtext = wx.StaticText(panel, label='Mash Steps')
        mashtext.SetFont(LABEL_FONT)
        grid.Add(mashtext, pos=(3, 0), flag=wx.ALIGN_CENTER)

        boiltext = wx.StaticText(panel, label='Boil Steps')
        boiltext.SetFont(LABEL_FONT)
        grid.Add(boiltext, pos=(3, 2), flag=wx.ALIGN_CENTER)

        self.mashlist = wx.ListBox(panel)
        self.mashlist.SetFont(LIST_FONT)
        grid.Add(self.mashlist, pos=(4, 0), span=(3, 1), flag=wx.EXPAND)

        # buttons
        self.stbtn = wx.Button(panel, label='Start', size=BTN_SIZE)
        self.stbtn.SetFont(LABEL_FONT)
        grid.Add(self.stbtn, pos=(4, 1), flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.rbtn = wx.Button(panel, label='Reset', size=BTN_SIZE)
        self.rbtn.SetFont(LABEL_FONT)
        grid.Add(self.rbtn, pos=(5, 1), flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.nxtbtn = wx.Button(panel, label='Next', size=BTN_SIZE)
        self.nxtbtn.SetFont(LABEL_FONT)
        grid.Add(self.nxtbtn, pos=(6,1), flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.boillist = wx.ListBox(panel)
        self.boillist.SetFont(LIST_FONT)
        grid.Add(self.boillist, pos=(4, 2), span=(3, 1), flag=wx.EXPAND)

        grid.Add(wx.StaticText(panel), pos=(7, 0))

        grid.AddGrowableCol(0)
        #grid.AddGrowableCol(1)!!!
        grid.AddGrowableCol(2)
        grid.AddGrowableRow(6)
        grid.AddGrowableRow(7)

        vbox.Add(grid, proportion=1, flag=wx.ALIGN_CENTER|wx.EXPAND|wx.ALL,
                 border=BORDER)

        # event bindings
        self.Bind(wx.EVT_MENU, self.recipe.OnShow, fitem1)
        self.Bind(wx.EVT_MENU, self.LoadRecipe, runitem2) # Mash
        self.Bind(wx.EVT_MENU, self.CallBoil, runitem3) # Boil

        self.Bind(wx.EVT_LISTBOX_DCLICK, self.LoadRecipe)

        # close the app
        # add close event binding for confirmation dialog !!!
        self.Bind(wx.EVT_MENU, self.CloseDlg, fitem2)
        self.Bind(wx.EVT_CLOSE, self.CloseDlg) #!!!

        # timer bindings
        self.Bind(wx.EVT_TIMER, self.OnTimerRun, self.wx_timer)

        self.stbtn.Bind(wx.EVT_BUTTON, self.OnTimerToggle)
        self.rbtn.Bind(wx.EVT_BUTTON, self.OnReset)
        self.nxtbtn.Bind(wx.EVT_BUTTON, self.OnNextStep)
        self.Bind(wx.EVT_MENU, self.setTimer.OnShow, runitem1)
        # event triggered from save button in SetTimer class
        self.Bind(wx.EVT_BUTTON, self.SetTime)
        # AndFit auto sizes the window to fit all widgets
        # do I need this? !!!
        panel.SetSizer(vbox)

#################################################################

    def LoadRecipe(self, e):
        """ load a timer based upon the brewing style """
        # rename OnRecipSelect !!!
        try:
            self.XML = self.recipe.GetRecipe()
            self.TREE = ET.parse(self.XML)
            self.TIMER.GetXML(self.TREE)
            self.brew_type = self.TIMER.GetBrewType()
            self.mash_steps = self.TIMER.GetMashSteps()[:]
            self.steps = len(self.mash_steps)
            self.step_count = 0
            self.mash_flag = False
            self.boil_flag = True

            self.LoadSteps()
            #self.first_wort = self.TIMER.GetFirstWort()

            if self.IsMashable:
               self.CallMash(None)
            else:
               self.CallBoil(None)

        except:
            # may need to raise parse error dialog if fpath is bad!!!
            self.RecipeErrDlg()

    def IsMashable(self):
        # should patial mash and biab be included? !!!
        """ Returns True if the brew type is All Grain. """
        return self.brew_type == 'All Grain'

    def CallMash(self, e):
        self.StopTimer()
        try:
            if self.mash_steps != [] and self.step_count < self.steps:
                self.mash_flag = True
                step = self.mash_steps[self.step_count]
                self.TIMER.Set(step[1])
                self.UpdateTimer()
                self.step_count += 1

            elif self.boil_flag == True:
                self.CallBoil(None)
                self.mash_flag = False
        except:

            self.RecipeErrDlg()

    def CallBoil(self, e):
        self.StopTimer()
        self.mash_flag = False
        self.boil_flag = True

        try:
            boil = self.TIMER.GetBoilTime()
            self.TIMER.Set(boil)
            # refresh the display
            self.UpdateTimer()
            self.step_count = 99

            if self.first_wort != []:
                self.HopDlg(self.first_wort)

        except:
            # a message dialong would nice here !!!
            self.RecipeErrDlg()

    def OnNextStep(self, e):
        if self.step_count == 99:
            self.StopTimer()
            self.TIMER.Set(0)
            self.UpdateTimer()

        elif self.mash_steps != []:
            self.StopTimer()
            self.CallMash(None)

    def LoadSteps(self):
        self.mashlist.Clear()
        self.boillist.Clear()
        for count, info in enumerate(self.mash_steps):
            step = '{}: {} {} degrees'.format((count+1), info[0], info[2])

            self.mashlist.Append(step)

        hops = self.TIMER.GetHops()
        self.first_wort = self.TIMER.GetFirstWort()
        hopskeys = sorted(hops.keys(), reverse=True)

        for one in self.first_wort:
            addition = '{2}, {1} oz {0}'.format(one[0], one[1], one[2])
            self.boillist.Append(addition)
        # hop is a key form the sorted dict
        for hop in hopskeys:
            # for each value in the dict
            for info in hops[hop]:
                #self.hopslist.append(info)
                addition = '{2} min, {1} oz {0}'.format(info[0], info[1], info[2])
                self.boillist.Append(addition)

    def ParseErrDlg(self):
        """ This will need a pop up dialog!!! """
        print "The file path is incorrect"

    def RecipeErrDlg(self):
        msg = "Please select a recipe first!"
        dlg = wx.MessageDialog(self, msg, "No Recipe Selected",
                               wx.OK|wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()

################################################################

    def OnTimerToggle(self, e):
        if not self.TIMER.GetStatus() and self.vals['display'] != '00:00':
            self.StartTimer()

        else:
            self.StopTimer()

    def StartTimer(self):
        """ Start the timer."""
        self.stbtn.SetLabel('Pause')
        self.wx_timer.Start(DELAY)
        self.TIMER.Start()
        self.ShowHopDlg()

    def StopTimer(self):
        """ Stop the timer."""
        self.stbtn.SetLabel('Start')
        self.TIMER.Stop()
        self.wx_timer.Stop()

    def OnTimerRun(self, e):
        """ Decrement and redraw the timer """
        # stop once we are at '00:00'
        if self.vals['display'] == '00:00':
            self.StopTimer()
            if self.mash_flag == False:
                self.boil_flag = False
                self.mash_flag = True
            self.CallMash(None)

        if self.vals['mn'] >= 0 and self.TIMER.GetStatus():
            # decrement the timer
            self.TIMER.Run()
            # redraw the display
            self.UpdateTimer()
            # show a hop dialog if necessary
            self.ShowHopDlg()

############################################################################

    def SetTime(self, e):
        # can this be used elsewhere? !!!
        """ Sets the timer with tuple from SetTimer class """
        self.StopTimer()
        vals = self.setTimer.GetTime()
        self.TIMER.Set(vals[0], vals[1])
        self.UpdateTimer()

###########################################################################

    def UpdateTimer(self):
        """ Reset the display. """
        # a dict of {mn=int, sec=int, display=string}
        self.vals = self.TIMER.GetDisplay()
        self.time_text.SetLabel(self.vals['display'])

    def OnReset(self, e):
        """ Reset the timer """
        self.StopTimer()
        self.TIMER.Reset()
        self.UpdateTimer()

    def OnClose(self, e):
        """ close the app """
        self.recipe.Destroy()
        self.setTimer.Destroy()
        self.Destroy()

    def CloseDlg(self, e):
        msg = "Are you sure you want to stop brewing?"
        dlg = wx.MessageDialog(self, msg, "Confim Close",
                               wx.OK | wx.CANCEL| wx.ICON_QUESTION)

        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.OnClose(None)
            dlg.Destroy()

#################################################################

    def HopDlg(self, msg):
        """ Dialog box for a reminder to add some hops """
        hops = ''
        for one in msg:
            hops += '{} oz {}\n'.format(one[1], one[0])

        addition = '{} Add: \n{}'.format(one[2], hops)

        dlg = wx.MessageDialog(self, addition, "Hop Addition",
                               wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def ShowHopDlg(self):
        # show the hop dialog when it's time to add hops
        if self.TIMER.AddHop() and self.mash_flag == False:
            hop = self.TIMER.GetAddition()
            self.HopDlg(hop)

    def FWHDlg(self):
        # a string to display hop information
        info = self.first_wort[0]
        msg = 'Add First Wort Hops!\n{} oz {}'.format(info[1], info[0])
        # the dialog box object
        dlg = wx.MessageDialog(self, msg, "Hop Addition",
                               wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == '__main__':
    World(None)
    app.MainLoop()
