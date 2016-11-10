import wx
import os
import shutil

"""
TODO:
- styling
- add other file types to GetRecipes? (.bsm, and/or .bsmx)
- add class for file browsing
  - this will do one of the following:
    1. allow you to select a recipe from anywhere - or
    2. add files to the recipe directory
"""
# variable for file path to .xml directory
FPATH = os.getcwd() +'\\recipes\\'

WILDCARD = ("BeerXML files (*.xml)|*.xml|"
            "All files (*.*)|*.*")

# a class for the list box population the contents of recipes
class Recipe(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent,  size=(250, 220))

        self.InitUI()

    def InitUI(self):
        self.recipe = ''
        self.recipes = []
        self.GetRecipes()

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.addbtn = wx.Button(panel, label='Add')
        self.okbtn = wx.Button(panel, label='OK')
        self.cnclbtn = wx.Button(panel, label="Cancel")
        self.listbox = wx.ListBox(panel, choices=self.recipes)

        hbox1.Add(self.listbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        hbox2.Add(self.addbtn, flag=wx.RIGHT, border=10)
        hbox2.Add(self.okbtn, flag=wx.RIGHT, border=10)
        hbox2.Add(self.cnclbtn, flag=wx.RIGHT, border=20)

        vbox.Add(hbox1, flag=wx.EXPAND|wx.ALL)
        vbox.Add(hbox2, flag=wx.ALIGN_RIGHT)

        panel.SetSizer(vbox)

        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelect)
        self.okbtn.Bind(wx.EVT_BUTTON, self.OnSelect)

        #self.addbtn.Bind(wx.EVT_BUTTON, self.OnAddFile)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.cnclbtn.Bind(wx.EVT_BUTTON, self.OnClose)

        self.SetTitle('Recipe List')

    def GetRecipes(self):
        recipes = os.listdir(FPATH)

        # if self.ext == 'xml': # or 'bsmx'?
        # if that file type works the same !!!
        for recipe in recipes:
            print recipe
            self.ext = recipe.split('.')[-1]
            name = '.'.join(recipe.split('.')[:-1])
            if self.ext == 'xml':
                self.recipes.append(name)

    def OnShow(self, e):
        self.Centre()
        self.Show()

    def OnSelect(self, e):

        sel = self.listbox.GetSelection()
        self.text = self.listbox.GetString(sel)
        self.recipe = FPATH + self.text + '.' + self.ext
        e.Skip()

    def GetRecipe(self):
        return self.recipe

    def OnClose(self, e):
        self.Hide()

    def OnAddFile(self, e):
        """
        Add files to the recipe diretory for use in the app
        """
        dlg = wx.FileDialog(
            self, message="Select a recipe ...",
            defaultDir=FPATH,
            defaultFile="", wildcard=WILDCARD, style=wx.OPEN
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            shutil.copy2(path, FPATH)
            # maybe can do this:
            # self.listbox = wx.ListBox(panel, choices=self.recipes) # then:
            self.GetRecipes() # -or maybe-
            # self.listbox.Append(path) # but this is the entire file path!

        dlg.Destroy()


if __name__ == '__main__':

    app = wx.App()
    R = Recipe(None)
    R.Centre()
    R.Show()
    app.MainLoop()
