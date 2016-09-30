### This file is for testing purposes for any lil' ol' thing at all ###
import wx # wxpython is being used for our gui
import xml.etree.ElementTree as ET

from timer import * # the brewing Timer class
from brewlist import *

SIZE = ((640, 480))
TITLE = 'Brewsys'
DELAY = 100

# The beer.xml file to be parsed
TREE = ET.parse('C:/Users/Todd/Desktop/brewsys/bsmith/Oktober-16.xml')
#TREE = ET.parse(RECIPE)

TIMER = Timer()

class World(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(World, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        cbtn = wx.Button(self, label='Close', pos=(350,125))
        cbtn.Bind(wx.EVT_BUTTON, self.OnClose)

        self.SetSize(SIZE)
        self.SetTitle(TITLE)
        self.Centre()
        self.Show(True)

    def OnClose(self, e):
        """ close the app """
        self.Close(True)

if __name__ == '__main__':
    wo = wx.App()
    World(None)
    wo.MainLoop()


# end of file #
