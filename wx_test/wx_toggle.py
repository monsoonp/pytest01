import wx


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        menubar = wx.MenuBar()
        viewMenu = wx.Menu()

        self.shst = viewMenu.Append(wx.ID_ANY, 'Show statusbar',
            'Show Statusbar', kind=wx.ITEM_CHECK)
        self.shtl = viewMenu.Append(wx.ID_ANY, 'Show toolbar',
            'Show Toolbar', kind=wx.ITEM_CHECK)

        viewMenu.Check(self.shst.GetId(), True)
        viewMenu.Check(self.shtl.GetId(), True)

        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shst)
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self.shtl)

        menubar.Append(viewMenu, '&View')
        self.SetMenuBar(menubar)

        self.toolbar = self.CreateToolBar()
        image = wx.Bitmap(wx.Bitmap('../data/image/exit.jpg').ConvertToImage().Scale(50, 50, wx.IMAGE_QUALITY_HIGH))
        self.toolbar.AddTool(wx.ID_UNDO, 'Exit', image)
        self.toolbar.Realize()

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        self.SetSize((450, 350))
        self.SetTitle('Check menu item')
        self.Centre()

        toolbar1 = wx.ToolBar(self)
        toolbar1.AddTool(wx.ID_ANY, '',  wx.Bitmap(wx.Bitmap('../data/image/exit.jpg').ConvertToImage().Scale(50, 50, wx.IMAGE_QUALITY_HIGH)))
        toolbar1.AddTool(wx.ID_ANY, '',  wx.Bitmap(wx.Bitmap('../data/image/exit.jpg').ConvertToImage().Scale(50, 50, wx.IMAGE_QUALITY_HIGH)))
        toolbar1.AddTool(wx.ID_ANY, '',  wx.Bitmap(wx.Bitmap('../data/image/exit.jpg').ConvertToImage().Scale(50, 50, wx.IMAGE_QUALITY_HIGH)))
        toolbar1.Realize()

    def ToggleStatusBar(self, e):

        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def ToggleToolBar(self, e):

        if self.shtl.IsChecked():
            self.toolbar.Show()
            # self.toolbar.EnableTool(wx.ID_UNDO, True)
        else:
            self.toolbar.Hide()
            # self.toolbar.EnableTool(wx.ID_UNDO, False)


def main():

    app = wx.App()
    ex = Example(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()