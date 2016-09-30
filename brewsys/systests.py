import wx # wxpython is being used for our gui
import xml.etree.ElementTree as ET

from timer import * # the brewing Timer class
from brewlist import *
"""
TODO: !!!
- add box for timer display
- confirmation dialog for when closing the app
- menu item to select a beer xml file for use
- layout management and style
"""
### CONSTANTS ###
SIZE = ((640, 480))
TITLE = 'Brewsys'
DELAY = 100

#LISTBOX = ListBox(None)
#RECIPE = LISTBOX.GetRecipe()

# The beer.xml file to be parsed
TREE = ET.parse('C:/Users/Todd/Desktop/brewsys/bsmith/Oktober-16.xml')
#TREE = ET.parse(RECIPE)

TIMER = Timer()

class World(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(World, self).__init__(*args, **kwargs)

        self.TIMER = TIMER
        try:
            self.TIMER.GetXML(TREE)
            BOILTIME = self.TIMER.GetBoilTime()
        except:
            pass
        # initialize the window and user interface
        self.InitUI()

    def InitUI(self):
        """ Set up the interface """
        #panel = SetTimer(self)

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
        # I think this needs to be self.settimer !!!
        settimer = SetTimer(self)

        # event bindings
        self.Bind(wx.EVT_MENU, self.OnClose, fitemOne)
        cbtn.Bind(wx.EVT_BUTTON, self.OnClose)

        self.Bind(wx.EVT_MENU, settimer.OnShow, fitemTwo)

        self.Bind(wx.EVT_BUTTON, self.OnSaveClick)

        self.Bind(wx.EVT_TIMER, self.OnTimer, self.wxtimer)
        self.stbtn.Bind(wx.EVT_BUTTON, self.OnRunning)
        rbtn.Bind(wx.EVT_BUTTON, self.OnReset)

        # set display details
        self.SetSize(SIZE)
        self.SetTitle(TITLE)
        self.Centre()
        self.Show(True)

        # draw the initial timer
        self.vals = self.TIMER.GetDisplay()
        self.dc.DrawText(self.vals['display'], 260, 50)

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

    def OnRefresh(self, e):
        """ Reset the display. """
        # a dict of {mn=int, sec=int, display=string}
        self.vals = self.TIMER.GetDisplay()
        # clear the previous inforamtion
        self.dc.Clear()
        # redraw the new information
        self.dc.DrawText(self.vals['display'], 260, 50)

    def OnTimer(self, e):
        """ Decrement and redraw the timer """
        if self.vals['mn'] >= 0 and self.TIMER.GetStatus():
            # decrement the timer
            self.TIMER.Run()
            # show a hop dialog if necessary
            self.ShowHopDlg()
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
            self.ShowHopDlg()
        # stop the timer
        else:
            self.TIMER.Stop()
            self.wxtimer.Stop()
            self.stbtn.SetLabel('Start')

    def OnReset(self, e):
        """ Reset the timer """
        self.stbtn.SetLabel('Start')
        self.TIMER.Reset()
        self.OnRefresh(e)

    def OnSaveClick(self, e):
        """ Received wx.EVT_BUTTON event from SetTimer class. """
        print "this is the World class!"
        self.OnRefresh(e)
        e.Skip()

    def OnClose(self, e):
        """ close the app """
        self.Close(True)

class SetTimer(wx.Frame):
    """
    Window for setting the timer manually accesed via
    File -> Set
    """
    def __init__(self, *args, **kwargs):
        super(SetTimer, self).__init__(*args, **kwargs)
        self.TIMER = TIMER
        #buttons
        svbtn = wx.Button(self, label='Save', pos=(20, 120))
        clbtn = wx.Button(self, label='Close', pos=(100, 120))

        #static text labels
        st1 = wx.StaticText(self, label='Min', pos=(50, 20))
        st2 = wx.StaticText(self, label='Sec', pos=(50, 70))

        #spin boxes for setting the timer mn/sec vals
        self.sc1 = wx.SpinCtrl(self, value='0', pos=(80, 15),
        size=(60, -1), min=0, max=120)
        self.sc2 = wx.SpinCtrl(self, value='0', pos=(80, 65),
        size=(60, -1), min=0, max=59)

        #button bindings
        svbtn.Bind(wx.EVT_BUTTON, self.OnSave)
        self.Bind(wx.EVT_BUTTON, self.OnSaveClick)

        clbtn.Bind(wx.EVT_BUTTON, self.OnCancel)

        self.SetSize((250, 250))
        self.SetTitle("Set Timer")
        self.Centre()

    def OnShow(self, e):
        """ Show the window """
        self.sc1.SetValue(0)
        self.sc2.SetValue(0)
        self.Show(True)

    def OnSave(self, e):
        """
        Apply the new timer values, close the window,
        and propigate the event to the class.
        """
        mn = self.sc1.GetValue()
        sec = self.sc2.GetValue()
        self.TIMER.Set(mn, sec)
        print "sending event with {}, {} from the World class".format(mn, sec)
        e.Skip()
        self.Hide()

    def OnSaveClick(self, e):
        """ Propigate the event to the World class """
        print "event received, sending to World"

        e.Skip()

    def OnCancel(self, e):
        """ Close the window without making changes """
        self.Hide()





# run the app
if __name__ == '__main__':
    wo = wx.App()
    World(None)
    wo.MainLoop()

    '''if <somecheck>:
        wo = wx.App()
        World(None)
        wo.MainLoop()
    else:
        <do something else>'''
