import wx
import vtk
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor

class p1(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)

        #to interact with the scene using the mouse use an instance of vtkRenderWindowInteractor.
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

           # open file
            openFileDialog = wx.FileDialog(self, "Open STL file", "", self.filename,
                                       "*.stl", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.filename = openFileDialog.GetPath()
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

class VTKFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(650,600), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        self.sp = wx.SplitterWindow(self)
        self.p1 = p1(self.sp)
        self.p2 = wx.Panel(self.sp,style=wx.SUNKEN_BORDER)

        self.sp.SplitHorizontally(self.p1,self.p2,470)

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("Click on the Load Button to load a STL file")

        self.plotbut = wx.Button(self.p2,-1,"Browse for STL file ", size=(120,20),pos=(10,10))
        self.plotbut.Bind(wx.EVT_BUTTON,self.plot)


    def plot(self,event):
        self.p1.renderthis()
        self.SetTitle("STL File Viewer: "+self.p1.filename)
        self.statusbar.SetStatusText("Use W,S,F,R keys and mouse to interact with the model ")


app = wx.App(redirect=False)
frame = VTKFrame(None,"STL File Viewer")
frame.Show()
app.MainLoop()
