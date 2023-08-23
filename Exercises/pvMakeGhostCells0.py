# Demonstration script for paraview version 5.11
# written by Jean M. Favre, Swiss National Supercomputing Centre
#
# Left view holds an isocontour where Normals were not computed. Thus,
# no ghost-cells were needed.
#
# Right View holds an isocontour with Normals=ON
# ghosts cells were computed. They can be viewed, except that by default
# ParaView does not show them. We use a trick whereby a Programmable Filter
# makes a copy of the structure (The extracted ghost cells) without data,
# and it can be viewed on the screen. Go to the right view, hide the "Contour"
# object and make the "GhostCells" object visible
#
# Tested Wed 23 Aug 08:37:00 CEST 2023
# You must run a client-server ParaView with a server running 4 MPI tasks

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

RightView = CreateView('RenderView')
RightView.AxesGrid = 'GridAxes3DActor'
RightView.CenterOfRotation = [35.15753173828125, 31.602006912231445, 33.624698638916016]
RightView.CameraPosition = [306.28275083455515, 175.10668474182037, 280.49530142845566]
RightView.CameraFocalPoint = [151.95041963700476, 93.4196637372208, 139.96940066698758]
RightView.CameraViewUp = [-0.24011760645342517, 0.9303538776161575, -0.27710142091959394]
RightView.CameraFocalDisk = 1.0
RightView.CameraParallelScale = 58.011716380114954

# Create a new 'Render View'
LeftView = CreateView('RenderView')
LeftView.AxesGrid = 'GridAxes3DActor'
LeftView.CenterOfRotation = RightView.CenterOfRotation
LeftView.CameraPosition = RightView.CameraPosition
LeftView.CameraFocalPoint = RightView.CameraFocalPoint
LeftView.CameraViewUp = RightView.CameraViewUp
LeftView.CameraFocalDisk = 1.0
LeftView.CameraParallelScale = RightView.CameraParallelScale

SetActiveView(None)

layout1 = CreateLayout(name='My layout')
layout1.SplitHorizontal(0, 0.5)
layout1.AssignView(1, LeftView)
layout1.AssignView(2, RightView)
SetActiveView(LeftView)

waveletLeft = Wavelet(registrationName='WaveletLeft')
waveletLeft.WholeExtent = [0, 99, 0, 99, 0, 99]
waveletLeft.UpdatePipeline()

contourLeft = Contour(registrationName='ContourNoNormals', Input=waveletLeft)
contourLeft.ContourBy = ['POINTS', 'RTData']
contourLeft.Isosurfaces = [100.0]
contourLeft.ComputeNormals = 0
contourLeft.ComputeScalars = 0
contourLeft.UpdatePipeline()

waveletLeftDisplay = Show(waveletLeft, LeftView, 'UniformGridRepresentation')
waveletLeftDisplay.Representation = 'Outline'
waveletLeftDisplay.ColorArrayName = ['POINTS', '']
waveletLeftDisplay.ScaleTransferFunction.Points = [-31.108078002929688, 0.0, 0.5, 0.0, 273.05389404296875, 1.0, 0.5, 0.0]
waveletLeftDisplay.OpacityTransferFunction.Points = [-31.108078002929688, 0.0, 0.5, 0.0, 273.05389404296875, 1.0, 0.5, 0.0]

# get color transfer function/color map for 'vtkProcessId'
vtkProcessIdLUT = GetColorTransferFunction('vtkProcessId')
vtkProcessIdLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 1.5, 0.865003, 0.865003, 0.865003, 3.0, 0.705882, 0.0156863, 0.14902]
vtkProcessIdLUT.ScalarRangeInitialized = 1.0

# show data from contourLeft
contourLeftDisplay = Show(contourLeft, LeftView, 'GeometryRepresentation')
contourLeftDisplay.Representation = 'Surface'
contourLeftDisplay.ColorArrayName = ['POINTS', 'vtkProcessId']
contourLeftDisplay.LookupTable = vtkProcessIdLUT
contourLeftDisplay.ScaleTransferFunction.Points = [120.97290802001953, 0.0, 0.5, 0.0, 120.98853302001953, 1.0, 0.5, 0.0]
contourLeftDisplay.OpacityTransferFunction.Points = [120.97290802001953, 0.0, 0.5, 0.0, 120.98853302001953, 1.0, 0.5, 0.0]

SetActiveView(RightView)

waveletRight = Wavelet(registrationName='WaveletRight')
waveletRight.WholeExtent = [0, 99, 0, 99, 0, 99]

contourRight = Contour(registrationName='ContourWithNormals', Input=waveletRight)
contourRight.ContourBy = ['POINTS', 'RTData']
contourRight.ComputeNormals = 1
contourRight.Isosurfaces = [100.0]
contourRight.ComputeScalars = 0

SetActiveSource(contourRight)

selection = QuerySelect(QueryString='(vtkGhostType == 1)', FieldType='CELL', InsideOut=0)

extractSelection1 = ExtractSelection(Selection=selection, registrationName='ExtractSelection1', Input=contourRight)
extractSelection1.UpdatePipeline()

GhostCells = ProgrammableFilter(registrationName='GhostCells', Input=extractSelection1)
GhostCells.OutputDataSetType = 'Same as Input'
GhostCells.Script = """\"\"\"
By default, the input structure, without data, is copied to the output
\"\"\""""


# show data from contour1
contourRightDisplay = Show(contourRight, RightView, 'GeometryRepresentation')
contourRightDisplay.Representation = 'Surface'
contourRightDisplay.ColorArrayName = ['POINTS', 'vtkProcessId']
contourRightDisplay.LookupTable = vtkProcessIdLUT

ghost_cells = Show(GhostCells, RightView, 'GeometryRepresentation')
ghost_cells.Representation = 'Surface'

# show data from wavelet1
waveletRightDisplay = Show(waveletRight, RightView, 'UniformGridRepresentation')
waveletRightDisplay.Representation = 'Outline'
waveletRightDisplay.ColorArrayName = ['POINTS', '']
waveletRightDisplay.ScaleTransferFunction.Points = [-31.108078002929688, 0.0, 0.5, 0.0, 273.05389404296875, 1.0, 0.5, 0.0]
waveletRightDisplay.OpacityTransferFunction.Points = [-31.108078002929688, 0.0, 0.5, 0.0, 273.05389404296875, 1.0, 0.5, 0.0]

# setup the color legend parameters for each legend in this view

# get color legend/bar for vtkProcessIdLUT in view RightView
vtkProcessIdLUTColorBar = GetScalarBar(vtkProcessIdLUT, RightView)
vtkProcessIdLUTColorBar.Title = 'vtkProcessId'
vtkProcessIdLUTColorBar.ComponentTitle = ''

# set color bar visibility
vtkProcessIdLUTColorBar.Visibility = 1

# show color legend
contourRightDisplay.SetScalarBarVisibility(RightView, True)

Hide(GhostCells)
AddCameraLink(LeftView, RightView, 'CameraLink0')
SetActiveView(LeftView)
