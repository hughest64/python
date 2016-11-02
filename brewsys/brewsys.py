import wx

from timer import *
from brewlist import *
from settimer import *

"""
TODO:
- finish ParseErrDlg() method
- helper method for setting step labels
- clean up LoadSteps - rename - and HopDlg parsing if possible
- doc strings!
"""

app = wx.App()

### CONSTANTS ###
SIZE = (640, 480)
TITLE = 'Brewsys'
DELAY = 1000

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

        self.step_count = 0

        self.InitUI()

        self.SetSize(SIZE)
        self.SetTitle(TITLE)
        self.Centre()
        self.Show()

    def InitUI(self):

        panel = wx.Panel(self)
        self.grid = wx.GridBagSizer(VGAP, HGAP)
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

        self.step_text = wx.StaticText(panel)
        self.step_text.SetFont(LABEL_FONT)
        self.grid.Add(self.step_text, pos=(0, 1), flag=wx.ALIGN_CENTER)

        self.step_text2 = wx.StaticText(panel)
        self.step_text2.SetFont(LABEL_FONT)
        self.grid.Add(self.step_text2, pos=(1, 1), flag=wx.ALIGN_CENTER)

        self.time_text = wx.StaticText(panel, label='00:00')
        self.time_text.SetFont(TIMER_FONT)
        self.grid.Add(self.time_text, pos=(2, 1), flag=wx.ALIGN_CENTER)

        mashtext = wx.StaticText(panel, label='Mash Steps')
        mashtext.SetFont(LABEL_FONT)
        self.grid.Add(mashtext, pos=(4, 0), flag=wx.ALIGN_CENTER)

        boiltext = wx.StaticText(panel, label='Boil Steps')
        boiltext.SetFont(LABEL_FONT)
        self.grid.Add(boiltext, pos=(4, 2), flag=wx.ALIGN_CENTER)

        self.mashlist = wx.ListBox(panel)
        self.mashlist.SetFont(LIST_FONT)
        self.grid.Add(self.mashlist, pos=(5, 0), span=(3, 1), flag=wx.EXPAND)

        # buttons
        self.stbtn = wx.Button(panel, label='Start', size=BTN_SIZE)
        self.stbtn.SetFont(LABEL_FONT)
        self.grid.Add(self.stbtn, pos=(5, 1), flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.rbtn = wx.Button(panel, label='Reset', size=BTN_SIZE)
        self.rbtn.SetFont(LABEL_FONT)
        self.grid.Add(self.rbtn, pos=(6, 1), flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.nxtbtn = wx.Button(panel, label='Next', size=BTN_SIZE)
        self.nxtbtn.SetFont(LABEL_FONT)
        self.grid.Add(self.nxtbtn, pos=(7,1), flag=wx.ALIGN_CENTER_HORIZONTAL)

        self.boillist = wx.ListBox(panel)
        self.boillist.SetFont(LIST_FONT)
        self.grid.Add(self.boillist, pos=(5, 2), span=(3, 1), flag=wx.EXPAND)

        self.grid.Add(wx.StaticText(panel), pos=(8, 0))

        self.grid.AddGrowableCol(0)
        self.grid.AddGrowableCol(2)
        self.grid.AddGrowableRow(7)
        self.grid.AddGrowableRow(8)

        vbox.Add(self.grid, proportion=1, flag=wx.ALIGN_CENTER|wx.EXPAND|wx.ALL,
                 border=BORDER)

        # event bindings
        self.Bind(wx.EVT_MENU, self.recipe.OnShow, fitem1)
        self.Bind(wx.EVT_MENU, self.CallMash, runitem2) # Mash
        self.Bind(wx.EVT_MENU, self.CallBoil, runitem3) # Boil

        self.Bind(wx.EVT_LISTBOX_DCLICK, self.LoadRecipe)

        # close the app
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

    def SetTime(self, e):
        """ Sets the timer with tuple from SetTimer class """
        self.StopTimer()
        vals = self.setTimer.GetTime()
        self.TIMER.Set(vals[0], vals[1])
        self.UpdateTimer()

    def OnTimerToggle(self, e):

        if self.vals != '00:00' and not self.TIMER.GetStatus():
            self.StartTimer()

        else:
            self.StopTimer()

    def StartTimer(self):
        """ Start the timer."""
        self.stbtn.SetLabel('Pause')
        self.wx_timer.Start(DELAY)
        self.TIMER.Start()
        if self.step_count == 99:
            self.ShowHopDlg()

    def StopTimer(self):
        """ Stop the timer."""
        self.stbtn.SetLabel('Start')
        self.TIMER.Stop()
        self.wx_timer.Stop()

    def OnTimerRun(self, e):
        """ Decrement and redraw the timer """
        # stop once we are at '00:00'
        if self.vals == '00:00':
            try:
                self.CallSteps()
            except:
                #pass
                self.StopTimer()

        else:
            # decrement the timer
            self.TIMER.Run()
            # redraw the display
            self.UpdateTimer()
            # show a hop dialog if necessary
            if self.step_count == 99:
                self.ShowHopDlg()
    # update and rename !!!
    def UpdateTimer(self):
        """ Reset the display. """
        self.vals = self.TIMER.GetDisplay()
        self.time_text.SetLabel(self.vals)

    def LoadRecipe(self, e):
        """ load a timer based upon the brewing style """
        # rename OnRecipSelect !!!
        #try:
        self.StopTimer()
        self.XML = self.recipe.GetRecipe()
        #self.TREE = ET.parse(self.XML) # remove!!!
        self.TIMER.SetXML(self.XML)

        self.all_steps = self.TIMER.GetAllSteps()
        self.mash_steps = self.all_steps['Mash']
        self.first_wort = self.all_steps['Firstwort']
        self.boil_steps = self.all_steps['Boil']
        self.steps = len(self.mash_steps)
        self.step_count = 0

        self.LoadSteps()
        self.CallSteps() # rename !!!

        #except:
            # may need to raise parse error dialog if fpath is bad!!!
            #self.RecipeErrDlg()

    def LoadSteps(self):
        self.mashlist.Clear()
        self.boillist.Clear()

        for count, info in enumerate(self.mash_steps):
            step = '{}: {} {} degrees'.format((count+1), info[0], info[2])
            self.mashlist.Append(step)

        for one in self.first_wort:
            addition = '{2}, {1} oz {0}'.format(one[0], one[1], one[2])
            self.boillist.Append(addition)

        # hop is a key from the sorted dict
        hopskeys = sorted(self.boil_steps.keys(), reverse=True)

        for hop in hopskeys:
            # for each value in the dict
            for info in self.boil_steps[hop]:
                #self.hopslist.append(info)
                addition = '{2} min, {1} oz {0}'.format(info[0], info[1], info[2])
                self.boillist.Append(addition)
    # add helper function!!!
    def CallSteps(self):
        boil_time = self.TIMER.GetBoilTime()
        self.StopTimer()

        if self.step_count < self.steps:
            step = self.mash_steps[self.step_count]
            self.TIMER.Set(self.mash_steps[self.step_count][1])
            self.UpdateTimer()
            self.step_count += 1

            # helper function !!!
            label = step[0]
            label2 = str(step[1]) + ' Minutes'
            self.step_text.SetLabel(label)
            self.step_text2.SetLabel(label2)
            self.grid.Layout()

        elif self.first_wort != [] and self.step_count != 99:
            self.TIMER.Set(boil_time)
            self.UpdateTimer()
            self.HopDlg(self.first_wort)
            self.step_count = 99

            # helper function !!!
            label = 'Boil'
            label2 = str(boil_time) + ' Minutes'
            self.step_text.SetLabel(label)
            self.step_text2.SetLabel(label2)
            self.grid.Layout()

        elif self.step_count != 99:
            self.TIMER.Set(boil_time)
            self.UpdateTimer()
            self.step_count = 99

            # helper function !!!
            label = 'Boil'
            label2 = str(boil_time) + ' Minutes'
            self.step_text.SetLabel(label)
            self.step_text2.SetLabel(label2)
            self.grid.Layout()

    def CallMash(self, e):
        try:
            self.step_count = 0
            self.StopTimer()
            self.CallSteps()

        except:

            self.RecipeErrDlg()

    def CallBoil(self, e):
        try:
            self.step_count = self.steps
            self.StopTimer()
            self.CallSteps()

        except:
            self.RecipeErrDlg()

    def OnReset(self, e):
        """ Reset the timer """
        self.StopTimer()
        self.TIMER.Reset()
        self.UpdateTimer()

    def OnNextStep(self, e):
        try:
            self.CallSteps()

        except:
            pass
    # finish this !!!
    def ParseErrDlg(self):
        """ This will need a pop up dialog!!! """
        print "The file path is incorrect"

    def RecipeErrDlg(self):
            msg = "Please select a recipe first!"
            dlg = wx.MessageDialog(self, msg, "No Recipe Selected",
            wx.OK|wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
    # can this be more efficient? !!!
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
        if self.TIMER.AddHop():
            hop = self.TIMER.GetAddition()
            self.HopDlg(hop)

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

if __name__ == '__main__':
    World(None)
    app.MainLoop()
