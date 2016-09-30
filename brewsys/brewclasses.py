import wx
import os
import time
import xml.etree.ElementTree as ET

from brewsys import *
from timer import *
from brewlist import *
from settimer import *


class Boil(object):
    def __init__(self):
        pass




class Mash(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(Boil, self).__init__(*args, **kwargs)
        # create a mash/boil Timer() object
        self.TIMER = MashTimer()


        self.TREE = self.recipe.GetRecipe()
        print self.TREE
        self.TIMER.GetXML(self.TREE)

        #self.vals = self.TIMER.GetDisplay()
        #self.dc.DrawText(self.vals['display'], 260, 50)
        #self.OnRefresh(None)









if __name__ == "__main__":
    app = wx.App()
    Boil(None)
    app.MainLoop()
