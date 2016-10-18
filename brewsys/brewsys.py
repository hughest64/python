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

        mashlist = wx.ListBox(panel, choices=TESTLIST)
        mashlist.SetFont(LIST_FONT)
        grid.Add(mashlist, pos=(4, 0), span=(2, 1), flag=wx.EXPAND)

        # buttons
        self.stbtn = wx.Button(panel, label='Start', size=BTN_SIZE)
        self.stbtn.SetFont(LABEL_FONT)
        grid.Add(self.stbtn, pos=(4, 1), flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.rbtn = wx.Button(panel, label='Reset', size=BTN_SIZE)
        self.rbtn.SetFont(LABEL_FONT)
        grid.Add(self.rbtn, pos=(5, 1), flag=wx.ALIGN_CENTER_HORIZONTAL)

        boillist = wx.ListBox(panel, choices=TESTLIST)
        boillist.SetFont(LIST_FONT)
        grid.Add(boillist, pos=(4, 2), span=(2, 1), flag=wx.EXPAND)

        grid.Add(wx.StaticText(panel), pos=(6, 0))
        
        grid.AddGrowableCol(0)
        grid.AddGrowableCol(1)
        grid.AddGrowableCol(2)
        grid.AddGrowableRow(5)
        grid.AddGrowableRow(6)

        vbox.Add(grid, proportion=1, flag=wx.ALIGN_CENTER|wx.EXPAND|wx.ALL,
                 border=BORDER)

        # event bindings
        self.Bind(wx.EVT_MENU, self.recipe.OnShow, fitem1)
        self.Bind(wx.EVT_MENU, self.CallMash, runitem2) # Mash
        self.Bind(wx.EVT_MENU, self.CallBoil, runitem3) # Boil

        self.Bind(wx.EVT_LISTBOX_DCLICK, self.BrewType)

        # close the app
        # add close event binding for confirmation dialog !!!
        self.Bind(wx.EVT_MENU, self.CloseDlg, fitem2)
        self.Bind(wx.EVT_CLOSE, self.CloseDlg) #!!!

        # timer bindings
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.wx_timer)

        self.stbtn.Bind(wx.EVT_BUTTON, self.OnRunning)
        self.rbtn.Bind(wx.EVT_BUTTON, self.OnReset)
        self.Bind(wx.EVT_MENU, self.setTimer.OnShow, runitem1)
        # event triggered from save button in SetTimer class
        self.Bind(wx.EVT_BUTTON, self.SetTime)
        # AndFit auto sizes the window to fit all widgets
        # do I need this? !!!
        panel.SetSizerAndFit(vbox)

#################################################################

    def BrewType(self, e):
        """ load a timer based upon the brewing style """
        try:
            self.XML = self.recipe.GetRecipe()
            self.TREE = ET.parse(self.XML)
            self.TIMER.GetXML(self.TREE)
            self.brewType = self.TIMER.GetBrewType()
            self.mash_steps = self.TIMER.GetMashSteps()[:]
            if self.Mashable:
               self.CallMash(None)
            else:
               self.CallBoil(None)

        except:
            # may need to raise parse error dialog if fpath is bad!!!
            self.RecipeErrDlg()


    def CallMash(self, e):
        try:
            if self.mash_steps != []:
                self.mash_flag = True
                step = self.mash_steps.pop(0)
                self.TIMER.Set(step[1], 0)
                self.OnRefresh(None)
            else:
                self.CallBoil(None)
                self.mash_flag = False
        except:

            self.RecipeErrDlg()

    def CallBoil(self, e):
        self.mash_flag = False
        try:
            boil = self.TIMER.GetBoilTime()
            self.TIMER.Set(boil[0], boil[1])
            # refresh the display
            self.OnRefresh(None)

        except:
            # a messag dialong would nice here !!!
            self.RecipeErrDlg()

    def Mashable(self):
        # should patial mash and biab be included? !!!
        """ Returns True if the brew type is All Grain. """
        return self.brewType == 'All Grain'

    def OnParseErr(self):
        """ This will need a pop up dialog!!! """
        return "The file path is incorrect"

################################################################

    def OnRefresh(self, e):
        """ Reset the display. """
        # a dict of {mn=int, sec=int, display=string}
        self.vals = self.TIMER.GetDisplay()
        self.time_text.SetLabel(self.vals['display'])
        self.time_text.Refresh()

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

    def CloseDlg(self, e):
        msg = "Are you sure you want to quit?"
        dlg = wx.MessageDialog(self, msg, "Are you sure?",
                               wx.OK | wx.CANCEL| wx.ICON_QUESTION)

        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.OnClose(None)
            dlg.Destroy()

    def OnTimer(self, e):
        # rename RunTimer? !!!
        """ Decrement and redraw the timer """
        # stop once we are at '00:00'
        if self.vals['display'] == '00:00':
            self.TIMER.Stop()
            self.wx_timer.Stop()
            self.stbtn.SetLabel('Start')
            self.CallMash

        if self.vals['mn'] >= 0 and self.TIMER.GetStatus():
            # decrement the timer
            self.TIMER.Run()
            # redraw the display
            self.OnRefresh(e)
            # show a hop dialog if necessary
            self.ShowHopDlg()

    def OnRunning(self, e):
        """ Start and stop the timer. """
        # rename OnTimerStart? !!!
        # start the timer unless we are a '00:00'
        if not self.TIMER.GetStatus() and self.vals['display'] != '00:00':
            self.stbtn.SetLabel('Pause')
            self.wx_timer.Start(DELAY)
            self.TIMER.Start()
            self.ShowHopDlg()

        # stop the timer
        else:
            self.TIMER.Stop()
            self.wx_timer.Stop()
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
        if self.TIMER.AddHop() and self.TIMER.GetHops() != {} \
        and self.mash_flag == False:
            self.HopDlg()

    def RecipeErrDlg(self):
        msg = "Please select a recipe first!"
        dlg = wx.MessageDialog(self, msg, "No Recipe Selected",
                               wx.OK|wx.ICON_EXCLAMATION)

        dlg.ShowModal()
        dlg.Destroy()



if __name__ == '__main__':
    #app = wx.App()
    World(None)
    app.MainLoop()
