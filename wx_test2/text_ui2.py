import os
import wx

class MyPanel(wx.Panel):
    def __init__(self, parent):
        super(MyPanel, self).__init__(parent)

        sizer = wx.BoxSizer()
        self.SetSizer(sizer)

    def AddChild(self, child):
        sizer = self.GetSizer()
        sizer.Add(child, 0, wx.ALIGN_LEFT|wx.ALL, 0)
        return super(MyPanel, self).AddChild(child)


class MyVirtualPanel(wx.PyPanel):
    """Class that automatically adds children contorols to sizer layout"""
    def __init__(self, parent):
        super(MyVirtualPanel, self).__init__(parent)

        sizer = wx.BoxSizer()
        self.SetSizer(sizer)

    def AddChild(self, child):
        sizer = self.GetSizer()
        sizer.Add(child, 0, wx.ALIGN_LEFT|wx.ALL, 0)
        return super(MyVirtualPanel, self).AddChild(child)



