import os
import wx


class MyApp(wx.App):
    def OnInit(self):  # This method is overridden and used as the main entry point for initializing this application.
        self.frame = MyFrame(None, title="The Main Frame")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        # wx.MessageBox("Hello wxPython", "wxApp") # popup
        return True


class MyFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name="MyFrame", *args, **kwargs):
        super(MyFrame, self).__init__(parent, id, title, pos, size, style, name)

        # Attributes

        # panel
        self.panel = wx.Panel(self)
        # self.panel.SetBackgroundColour(wx.BLACK)  # background color
        # self.button = wx.Button(self.panel, label="Push Me", pos=(50, 50))
        button = wx.Button(self.panel, label="Get Children", pos=(50, 50))
        self.btnId = button.GetId()
        ok_btn = wx.Button(self.panel, wx.ID_OK)
        cancel_btn = wx.Button(self.panel, wx.ID_CANCEL, pos=(100, 0))

        # menu_bar
        menu_bar = wx.MenuBar()
        edit_menu = wx.Menu()
        edit_menu.Append(wx.ID_ANY, "Test")
        edit_menu.Append(wx.ID_PREFERENCES)
        menu_bar.Append(edit_menu, "Edit")
        self.SetMenuBar(menu_bar)

        img_path = os.path.abspath("../data/image/triangle.png")
        # bitmap
        # bitmap = wx.Bitmap(img_path, type=wx.BITMAP_TYPE_PNG)
        # self.bitmap = wx.StaticBitmap(self.panel, bitmap=bitmap)

        # icon
        icon = wx.Icon(img_path, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton, button)

    def OnButton(self, event):
        """Called when the Button is clicked"""
        print("\nFrame GetChildren:")
        for child in self.GetChildren():
            print(f"{repr(child)}")

        print("\nPanel FindWindowById:")
        button = self.panel.FindWindowById(self.btnId)
        print(f"{repr(button)}")

        # Change Button's label
        button.SetLabel("Changed Label")

        print("\nButton GetParent:")
        panel = button.GetParent()
        print(f"repr{panel}")

        print("\nGet the Application Object:")
        frame = app.GetTopWindow()
        print(f"repr{frame}")

    def SetClipboardText(text):
        """Put text in the clipboard
        @param text: string
        """
        data_o = wx.TextDataObject()
        data_o.SetText(text)
        if wx.TheClipboard.IsOpend() or wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data_o)
            wx.TheClipboard.Close()

    def GetClipboardText(self):
        """Get text from the clipboard
        @return: string
        """
        text_obj = wx.TextDataObject()
        rtext = ""
        if wx.TheClipboard.IsOpend() or wx.TheClipboard.Open():
            if wx.TheClipboard.GetData(text_obj):
                rtext = text_obj.GetText()
            wx.TheClipboard.Close()
        return rtext


class FileAndTextDropTarget(wx.PyDropTarget):
    """Drop target capable of acception dropped files and text"""
    def __init__(self, file_callback, text_callback):
        assert callable(file_callback)
        assert callable(text_callback)
        super(FileAndTextDropTarget, self).__init__()

        # Attributes
        self.fcallback = file_callback  # Drop File Callback
        self.tcallback = text_callback  # Drop Text Callback
        self._data = None
        self.txtdo = None
        self.filedo = None

        # Setup
        self.InitObjects()

    def InitObjects(self):
        """Initializes the text and file data objects"""
        self._data = wx.DataObjectComposite()
        self.txtdo = wx.TextDataObject()
        self.filedo = wx.FileDataObject()
        self._data.Add(self.txtdo, False)
        self._data.Add(self.filedo, True)
        self.SetDataObject(self._data)

    def OnData(self, x_cord, y_cord, drag_result):
        """Called by the framework when data is dropped on the tartget"""
        if self.GetData():
            data_format = self._data.GetReceivedFormat()
            if data_format.GetType() == wx.DF_FILENAME:
                self.fcallback(self.filedo.GetFilenames())
            else:
                self.tcallback(self.txtdo.GetText())

        return drag_result


class DropTargetFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE, name="DropTargetFrame"):
        super(DropTargetFrame, self).__init__(parent, id, title, pos, size, style, name)

        # Attributes
        choices = ["Drag and Drop Text or Files here",]
        self.list = wx.ListBox(self, choices=choices)
        self.dt = FileAndTextDropTarget(self.OnFileDrop, self.OnTextDrop)
        self.list.SetDropTarget(self.dt)

        # Setup
        self.CreateStatusBar()

    def OnFileDrop(self, files):
        self.PushStatusText("Files Droppped")
        for f in files:
            self.list.Append(f)

    def OnTextDrop(self, text):
        self.PushStatusText("Text Droppped")
        self.list.Append(text)


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
