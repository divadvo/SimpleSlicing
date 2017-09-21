import wx
import os
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin

import vtk
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor

import stl.stlanalyse
import slicing.slicer
import gcode.gcodehelfer

stl_datei_path = None
stl_data = None
gcode_datei_path = None
befehle = None

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)

class ControlPanel(wx.Panel):
    def __init__(self, parent):
        super(ControlPanel, self).__init__(parent)

        self.InitUI()

    def InitUI(self):
        self.button_stl_to_gcode = wx.Button(self, label='STL -> GCode')
        self.Bind(wx.EVT_BUTTON, self.button_stl_to_gcode_click, self.button_stl_to_gcode)

        fgs = wx.FlexGridSizer(4, 2, 10, 10)

        self.infill_text = wx.StaticText(self, label="Infill")
        self.layer_height_text = wx.StaticText(self, label="layer_height")
        self.nozzle_diameter_text = wx.StaticText(self, label="nozzle_diameter")

        self.tc1 = wx.TextCtrl(self, value="0.2")
        self.tc2 = wx.TextCtrl(self, value="0.2")
        self.tc3 = wx.TextCtrl(self, value="0.4")

        fgs.AddMany([
            (self.infill_text), (self.tc1, 1, wx.EXPAND),
            (self.layer_height_text), (self.tc2, 1, wx.EXPAND),
            (self.nozzle_diameter_text), (self.tc3, 1, wx.EXPAND)
            ])

        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(1, 1)

        self.dreiecke_text = wx.StaticText(self)

        self.sizer=wx.BoxSizer(wx.VERTICAL)

        self.sizer.AddSpacer(10)

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

        self.button_gcode_to_arduino = wx.Button(self, label='GCode -> Arduino')
        self.Bind(wx.EVT_BUTTON, self.button_gcode_to_arduino_click, self.button_gcode_to_arduino)

        self.befehle_text = wx.StaticText(self, label="Befehle:")
        self.button_gcode_to_arduino.Disable()
        self.befehle_text.Disable()

        self.sizer.Add(self.button_gcode_to_arduino, 0, wx.EXPAND)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.befehle_text, 0, wx.EXPAND)

        self.list = CheckListCtrl(self)
        self.list.InsertColumn(0, '#')
        self.list.InsertColumn(1, 'Art')
        self.list.InsertColumn(2, 'X')
        self.list.InsertColumn(3, 'Y')
        self.list.InsertColumn(4, 'Z')
        self.list.InsertColumn(5, 'E')

        self.list.Disable()


        self.sizer.Add(self.list, 0, wx.EXPAND)

        self.SetSizer(self.sizer)

    def button_gcode_to_arduino_click(self, event):
        self.button_stl_to_gcode.Disable()
        self.button_gcode_to_arduino.Disable()

        def get_zahl(zahl):
            if zahl == None:
                return ""
            else:
                return "{:0.5f}".format(zahl)


        for idx, befehl in enumerate(befehle):
            index = self.list.InsertStringItem(10000, str(idx+1))
            self.list.SetStringItem(index, 1, befehl.art)
            self.list.SetStringItem(index, 2, get_zahl(befehl.x))
            self.list.SetStringItem(index, 3, get_zahl(befehl.y))
            self.list.SetStringItem(index, 4, get_zahl(befehl.z))
            self.list.SetStringItem(index, 5, get_zahl(befehl.e))

        self.list.Enable()

        self.Update()

        import arduino.arduino
        for idx, befehl in enumerate(befehle):
            self.aktualisiere_befehle_text(idx + 1, len(befehle))
            arduino.arduino.sende_befehl(befehl.text)
            self.list.CheckItem(idx)
            self.list.Focus(idx)
            self.Update()

    def aktualisiere_befehle_text(self, befehl_derzeit, befehle_insgesamt):
        prozent = befehl_derzeit * 100.0 / befehle_insgesamt
        self.befehle_text.SetLabel("Befehle: {}/{}  ({:.2f}%)".format(befehl_derzeit, befehle_insgesamt, prozent))

    def button_stl_to_gcode_click(self, event):
        parameter_slicer = {
            "infill": float(self.tc1.GetValue()),
            "layer_height": float(self.tc2.GetValue()),
            "nozzle_diameter": float(self.tc3.GetValue()),
        }

        global gcode_datei_path

        sliced = slicing.slicer.slice(stl_data)
        gcode_datei_path = os.path.splitext(stl_datei_path)[0] + ".gcode"

        global befehle
        befehle = gcode.gcodehelfer.export(sliced, gcode_datei_path)

        self.button_gcode_to_arduino.Enable()
        self.befehle_text.Enable()

    def setze_anzahl_dreiecke(self, anzahl_dreiecke):
        self.dreiecke_text.SetLabel("Anzahl Dreiecke: " + str(anzahl_dreiecke))

class ViewPanel(wx.Panel):
    def __init__(self, parent):
        super(ViewPanel, self).__init__(parent)
        self.InitUI()

    def InitUI(self):
        self.widget = wxVTKRenderWindowInteractor(self, -1)
        self.widget.Enable(1)
        self.widget.AddObserver("ExitEvent", lambda o,e,f=self: f.Close())
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.widget, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Layout()
        self.ren = vtk.vtkRenderer()
        self.filename=""
        self.isploted = False

    def renderthis(self):
            # open a window and create a renderer
            self.widget.GetRenderWindow().AddRenderer(self.ren)

            self.filename = stl_datei_path
            # render the data
            reader = vtk.vtkSTLReader()
            reader.SetFileName(self.filename)

            # To take the polygonal data from the vtkConeSource and
            # create a rendering for the renderer.
            coneMapper = vtk.vtkPolyDataMapper()
            coneMapper.SetInput(reader.GetOutput())

            # create an actor for our scene
            if self.isploted:
                coneActor=self.ren.GetActors().GetLastActor()
                self.ren.RemoveActor(coneActor)

            coneActor = vtk.vtkActor()
            coneActor.SetMapper(coneMapper)
            # Add actor
            self.ren.AddActor(coneActor)
           # print self.ren.GetActors().GetNumberOfItems()

            if not self.isploted:
                axes = vtk.vtkAxesActor()
                self.marker = vtk.vtkOrientationMarkerWidget()
                self.marker.SetInteractor( self.widget._Iren )
                self.marker.SetOrientationMarker( axes )
                self.marker.SetViewport(0.75,0,1,0.25)
                self.marker.SetEnabled(1)

            self.ren.ResetCamera()
            self.ren.ResetCameraClippingRange()
            cam = self.ren.GetActiveCamera()
            cam.Elevation(10)
            cam.Azimuth(70)
            self.isploted = True
            self.ren.Render()

class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def erstelle_menu(self):
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

    def erstelle_panels(self):

        self.sp = wx.SplitterWindow(self)

        self.view_panel = ViewPanel(self.sp)
        self.control_panel = ControlPanel(self.sp)
        self.sp.SplitVertically(self.view_panel, self.control_panel)
        self.sp.SetSashGravity(0.5)

        # self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.sizer.Add(self.view_panel, 0, wx.ALIGN_LEFT, 4)
        # self.sizer.Add(self.control_panel, 0, wx.ALIGN_RIGHT, 4)
        # self.SetSizer(self.sizer)

        self.view_panel.Hide()
        self.control_panel.Hide()

    def InitUI(self):

        self.erstelle_menu()
        self.erstelle_panels()

        self.SetSize((1280, 720))
        self.SetTitle('STL -> Gcode -> 3D Drucker')
        self.Centre()
        self.Show(True)

        self.dirname = ''

    def open_file(self, stl_datei):
        global stl_datei_path
        global stl_data

        stl_datei_path = stl_datei
        stl_data = stl.stlanalyse.stl_analysieren(stl_datei)

        self.control_panel.setze_anzahl_dreiecke(len(stl_data.dreiecke))
        self.view_panel.renderthis()

        self.view_panel.Show()
        print 'View'
        self.control_panel.Show()

    def on_quit(self, e):
        self.Close()

    def on_open(self, e):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.stl", wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            self.filepath = dlg.GetPath()

            self.open_file(self.filepath)
            #self.SetTitle("Editing ... "+self.filepath)
        dlg.Destroy()


def main():
    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
