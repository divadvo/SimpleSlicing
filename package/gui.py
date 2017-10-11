import wx
import os

import vtk
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor

import stl.stlanalyse
import slicing.slicer
import gcode.gcodehelfer

stl_datei_path = None
stl_data = None
gcode_datei_path = None


class ControlPanel(wx.Panel):
    def __init__(self, parent):
        super(ControlPanel, self).__init__(parent)

        self.InitUI()

    def InitUI(self):
        self.button_stl_to_gcode = wx.Button(self, label='STL -> GCode')
        self.Bind(wx.EVT_BUTTON, self.button_stl_to_gcode_click,
                  self.button_stl_to_gcode)

        fgs = wx.FlexGridSizer(6, 2, 10, 10)

        self.infill_text = wx.StaticText(self, label="Infill")
        self.layer_height_text = wx.StaticText(self, label="layer_height")
        self.nozzle_diameter_text = wx.StaticText(
            self, label="nozzle_diameter")
        self.start_x_text = wx.StaticText(self, label="Start X")
        self.start_y_text = wx.StaticText(self, label="Start Y")

        self.tc1 = wx.TextCtrl(self, value="0.2")
        self.tc2 = wx.TextCtrl(self, value="0.2")
        self.tc3 = wx.TextCtrl(self, value="0.4")
        self.tc4 = wx.TextCtrl(self, value="40")
        self.tc5 = wx.TextCtrl(self, value="40")

        fgs.AddMany([
            (self.infill_text), (self.tc1, 1, wx.EXPAND),
            (self.layer_height_text), (self.tc2, 1, wx.EXPAND),
            (self.nozzle_diameter_text), (self.tc3, 1, wx.EXPAND),
            (self.start_x_text), (self.tc4, 1, wx.EXPAND),
            (self.start_y_text), (self.tc5, 1, wx.EXPAND)
        ])

        fgs.AddGrowableRow(2, 1)
        fgs.AddGrowableCol(1, 1)

        self.dreiecke_text = wx.StaticText(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

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

        self.befehle_text = wx.StaticText(self, label="Befehle:")
        # self.befehle_text.Disable()
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.befehle_text, 0, wx.EXPAND)

        self.SetSizer(self.sizer)

    def aktualisiere_befehle_text(self, befehle_insgesamt):
        self.befehle_text.SetLabel("Befehle: {}".format(befehle_insgesamt))

    def button_stl_to_gcode_click(self, event):
        parameter_slicer = {
            "infill": float(self.tc1.GetValue()),
            "layer_height": float(self.tc2.GetValue()),
            "nozzle_diameter": float(self.tc3.GetValue()),
            "start_x": float(self.tc4.GetValue()),
            "start_y": float(self.tc5.GetValue()),
        }

        global gcode_datei_path

        import time
        timestr = time.strftime("%Y%m%d-%H%M%S")

        sliced = slicing.slicer.slice(stl_data)
        gcode_datei_path = os.path.splitext(
            stl_datei_path)[0] + "_{}.gcode".format(timestr)

        befehle = gcode.gcodehelfer.export(sliced, gcode_datei_path, "/media/divadvo/Data/Projects/3DPrinting/Uni/Uni_Programm/package/config/anfang.gcode",
                                           "/media/divadvo/Data/Projects/3DPrinting/Uni/Uni_Programm/package/config/ende.gcode", mitte_x=parameter_slicer["start_x"], mitte_y=parameter_slicer["start_y"])
        self.aktualisiere_befehle_text(befehle)

    def setze_anzahl_dreiecke(self, anzahl_dreiecke):
        self.dreiecke_text.SetLabel("Anzahl Dreiecke: " + str(anzahl_dreiecke))


class ViewPanel(wx.Panel):
    def __init__(self, parent):
        super(ViewPanel, self).__init__(parent)
        self.InitUI()

    def InitUI(self):
        self.widget = wxVTKRenderWindowInteractor(self, -1)
        self.widget.Enable(1)
        self.widget.AddObserver("ExitEvent", lambda o, e, f=self: f.Close())
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.widget, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Layout()
        self.ren = vtk.vtkRenderer()
        self.filename = ""
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
            coneActor = self.ren.GetActors().GetLastActor()
            self.ren.RemoveActor(coneActor)

        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)
        # Add actor
        self.ren.AddActor(coneActor)
       # print self.ren.GetActors().GetNumberOfItems()

        if not self.isploted:
            axes = vtk.vtkAxesActor()
            self.marker = vtk.vtkOrientationMarkerWidget()
            self.marker.SetInteractor(self.widget._Iren)
            self.marker.SetOrientationMarker(axes)
            self.marker.SetViewport(0.75, 0, 1, 0.25)
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

        self.topSplitter = wx.SplitterWindow(self)
        vSplitter = wx.SplitterWindow(self.topSplitter)

        self.button_panel = wx.Panel(self.topSplitter)

        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.open_button = wx.Button(self.button_panel, label="STL Offnen")
        self.open_button.Bind(wx.EVT_BUTTON, self.on_open)
        h_sizer.Add(self.open_button, 0, wx.CENTER)

        main_sizer.Add((0, 0), 1, wx.EXPAND)
        main_sizer.Add(h_sizer, 0, wx.CENTER)
        main_sizer.Add((0, 0), 1, wx.EXPAND)

        self.button_panel.SetSizer(main_sizer)

        self.view_panel = ViewPanel(vSplitter)
        self.control_panel = ControlPanel(vSplitter)
        vSplitter.SplitVertically(self.view_panel, self.control_panel)
        vSplitter.SetSashGravity(0.5)

        self.topSplitter.SplitHorizontally(self.button_panel, vSplitter)
        self.topSplitter.SetSashGravity(0.1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.topSplitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.view_panel.Hide()
        self.control_panel.Hide()

    def InitUI(self):
        self.erstelle_menu()
        self.erstelle_panels()

        self.SetSize((1280, 720))
        self.SetTitle('STL -> Gcode')
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
        self.control_panel.Show()

        self.button_panel.Hide()

        # self.topSplitter.SetSashGravity(0)
        self.topSplitter.Unsplit(self.button_panel)

    def on_quit(self, e):
        self.Close()

    def on_open(self, e):
        dlg = wx.FileDialog(self, "Datei auswahlen",
                            self.dirname, "", "*.stl", wx.OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
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
