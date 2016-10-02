import wx

"""
TODO:
- create a panel and add widgets to sizers
"""

class SetTimer(wx.Frame):
    """
    Window for setting the timer manually accesed via
    Timer -> Set
    """

    def __init__(self, parent):
        wx.Frame.__init__(self, parent,  size=(250, 250))

        #buttons
        svbtn = wx.Button(self, label='Save', pos=(20, 120))
        clbtn = wx.Button(self, label='Cancel', pos=(100, 120))

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
        self.Bind(wx.EVT_CLOSE, self.OnCancel)

        self.SetTitle("Set Timer")

    def OnShow(self, e):
        """ Show the window """
        self.sc1.SetValue(0)
        self.sc2.SetValue(0)
        self.Centre()
        self.Show(True)

    def OnSave(self, e):
        """
        Apply the new timer values, close the window,
        and propigate the event to the class.
        """
        self.mn = self.sc1.GetValue()
        self.sec = self.sc2.GetValue()
        e.Skip()
        self.Hide()

    def OnSaveClick(self, e):
        """ Propigate the event to the World class """
        #print "event received, sending to World"
        e.Skip()

    def GetTime(self):
        return (self.mn, self.sec)

    def OnCancel(self, e):
        """ Close the window without making changes """
        self.Hide()


if __name__ == '__main__':
    app = wx.App()
    S = SetTimer(None)
    S.Show()
    app.MainLoop()
