import wx
import os

class ControlPanel(wx.Panel):
    def __init__(self, parent):
        super(ControlPanel, self).__init__(parent)

        self.InitUI()

    def InitUI(self):
        self.button_anfang_gcode = wx.Button(self, label='Anfang Code')
        self.button_ende_gcode = wx.Button(self, label='Ende Code')
        self.line = wx.StaticLine(self)
        self.button_stl_to_gcode = wx.Button(self, label='STL -> GCode')

        fgs = wx.FlexGridSizer(4, 2, 10, 10)

        self.infill_text = wx.StaticText(self, label="Infill")
        author = wx.StaticText(self, label="layer_height")
        review = wx.StaticText(self, label="nozzle_diameter")

        self.tc1 = wx.TextCtrl(self, value="0.2")
        tc2 = wx.TextCtrl(self, value="0.2")
        tc3 = wx.TextCtrl(self, value="0.4")

        fgs.AddMany([
            (self.infill_text), (self.tc1, 1, wx.EXPAND),
            (author),(tc2, 1, wx.EXPAND),
            (review), (tc3, 1, wx.EXPAND),
            (self.button_anfang_gcode), (self.button_ende_gcode, 1, wx.EXPAND)
            ])

        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(1, 1)

        sld = wx.Slider(self, value=200, minValue=150, maxValue=500, pos=(20, 20),
            size=(250, -1), style=wx.SL_HORIZONTAL)
        sld.Bind(wx.EVT_SCROLL, self.OnSliderScroll)

        self.layer_text = wx.StaticText(self, label="Layer: ")

        sld.Disable()
        self.layer_text.Disable()
        #self.button_stl_to_gcode.Disable()


        self.dreiecke_text = wx.StaticText(self, label="Anzahl Dreiecke: " + str(0))

        self.sizer=wx.BoxSizer(wx.VERTICAL)

        self.sizer.Add(self.dreiecke_text, 0, wx.EXPAND)

        self.sizer.AddSpacer(10)
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
        self.sizer.AddSpacer(10)

        self.sizer.Add(fgs, 0, wx.EXPAND)

        self.sizer.AddSpacer(10)
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
        self.sizer.AddSpacer(10)

        self.sizer.Add(self.button_stl_to_gcode, 0, wx.EXPAND)

        self.sizer.AddSpacer(10)
        self.sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
        self.sizer.AddSpacer(10)

        self.sizer.Add(sld, 0, wx.ALL)
        self.sizer.Add(self.layer_text, 0, wx.EXPAND)

        self.SetSizer(self.sizer)

    def OnSliderScroll(self, e):

        obj = e.GetEventObject()
        val = obj.GetValue()

        self.layer_text.SetLabel("Layer: " + str(val))

class ViewPanel(wx.Panel):
    def __init__(self, parent):
        super(ViewPanel, self).__init__(parent)

        self.InitUI()

    def InitUI(self):
        button = wx.Button(self, label='LOL')

class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_OPEN, '&Open')
        fileMenu.AppendSeparator()

        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+W')
        fileMenu.AppendItem(qmi)

        self.Bind(wx.EVT_MENU, self.on_quit, qmi)
        wx.EVT_MENU(self, wx.ID_OPEN, self.on_open)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        #self.control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
        self.control_panel = ControlPanel(self)
        self.panel2 = ViewPanel(self)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        #self.fgs = wx.FlexGridSizer(1, 2, 10, 10)


        #self.fgs.Add(self.panel2)
        #self.fgs.Add(self.control_panel)

        #self.sizer.Add(self.fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)

        self.sizer.Add(self.panel2, 0, wx.ALIGN_LEFT, 4)
        self.sizer.Add(self.control_panel, 0, wx.ALIGN_RIGHT, 4)

        self.SetSizer(self.sizer)

        self.SetSize((1280, 720))
        self.SetTitle('STL -> Gcode')
        self.Centre()
        self.Show(True)

        self.dirname = ''

    def on_quit(self, e):
        self.Close()

    def on_open(self,e):
        # In this case, the dialog is created within the method because
        # the directory name, etc, may be changed during the running of the
        # application. In theory, you could create one earlier, store it in
        # your frame object and change it when it was called to reflect
        # current parameters / values
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.filepath = dlg.GetPath()

            # Open the file, read the contents and set them into
            # the text edit window
            filehandle=open(os.path.join(self.dirname, self.filename),'r')
            self.control.SetValue(filehandle.read())
            filehandle.close()


            # Report on name of latest file read
            self.SetTitle("Editing ... "+self.filepath)
            # Later - could be enhanced to include a "changed" flag whenever
            # the text is actually changed, could also be altered on "save" ...
        dlg.Destroy()


def main():

    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
