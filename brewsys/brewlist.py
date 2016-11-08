import wx
import os

"""
TODO:
add buttons for Open and Close
(open to do the same thing as double click)
argparse to set FPATH from the command line!!!
"""
# variable for file path to .xml directory
# FPATH  = os.getcwd() + '/recipes' # !!!
FPATH = "C:/Users/Todd/Desktop/brewsys/recipes/"

# a class for the list box population the contents of recipes
class Recipe(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent,  size=(350, 220))
        self.recipe = ''
        self.recipes = []
        self.GetRecipes()

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.listbox = wx.ListBox(panel, choices=self.recipes)
        hbox.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 20)

        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelect)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        panel.SetSizer(hbox)

        self.SetTitle('Recipe List')

    def GetRecipes(self):
        d = os.listdir(FPATH)
        
        for r in d:
            #self.ext = R[-1] # !!!
            R = r.split('.')
                        
            # if self.ext == 'xml': # or 'bsmx'? if that file type works the same
            if R[-1] == 'xml':
                self.recipes.append(R[0]) # (R[:-1]) # !!!

    def OnShow(self, e):
        self.Centre()
        self.Show()

    def OnSelect(self, e):
        sel = self.listbox.GetSelection()
        self.text = self.listbox.GetString(sel)
        #self.recipe = '{}{}.{}'.format(FPATH, self.text, self.ext) #!!!
        self.recipe = FPATH + self.text + '.xml'
        e.Skip()
        self.Hide()

    def GetRecipe(self):
        return self.recipe

    def OnClose(self, e):
        self.Hide()



if __name__ == '__main__':
    app = wx.App()
    R = Recipe(None)
    R.Show()
    app.MainLoop()
