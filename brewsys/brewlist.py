import wx
import os
from timer import *
"""
TODO:
add buttons for Open and Close
(open to do the same thing as double click)
fix bug when using the X to close the window
"""
# variable for file path to .xml directory
FPATH = "C:/Users/Todd/Desktop/brewsys/recipes/"

# a class for the list box population the contents of RECIPES
class Recipe(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent,  size=(350, 220))
        self.recipe = ''
        #self.recipe = 'C:/Users/Todd/Desktop/brewsys/recipes/Oktober-16.xml'
        self.RECIPES = os.listdir(FPATH)

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.listbox = wx.ListBox(panel, choices=self.RECIPES)
        hbox.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 20)

        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelect)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        panel.SetSizer(hbox)

        self.SetTitle('Recipe List')

    def OnShow(self, e):
        self.Centre()
        self.Show()

    def OnSelect(self, e):
        sel = self.listbox.GetSelection()
        self.text = self.listbox.GetString(sel)
        self.recipe = FPATH + self.text
        e.Skip()
        self.Hide()

    def GetRecipe(self):
        return self.recipe

    def OnClose(self, e):
        self.Hide()
