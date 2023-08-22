# state file generated using paraview version 5.11.1
import paraview
paraview.compatibility.major = 5
paraview.compatibility.minor = 11

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

materialLibrary1 = GetMaterialLibrary()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [602, 694]
renderView1.CameraPosition = [-54.47643526962459, 23.794744044111386, 49.667920914671136]
renderView1.CameraFocalPoint = [16.635689582705172, -7.2662973202741155, -15.167294087165265]
renderView1.CameraViewUp = [0.21403072167261797, 0.9514801035681589, -0.22108021778129314]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 26.694689865756892
renderView1.BackEnd = 'OSPRay raycaster'
renderView1.OSPRayMaterialLibrary = materialLibrary1

# Create a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.ViewSize = [601, 694]
renderView2.CameraPosition = renderView1.CameraPosition
renderView2.CameraFocalPoint = renderView1.CameraFocalPoint
renderView2.CameraViewUp = renderView1.CameraViewUp
renderView2.CameraFocalDisk = 1.0
renderView2.CameraParallelScale = renderView1.CameraParallelScale
renderView2.BackEnd = 'OSPRay raycaster'
renderView2.OSPRayMaterialLibrary = materialLibrary1

SetActiveView(None)

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.SplitHorizontal(0, 0.5)
layout1.AssignView(1, renderView1)
layout1.AssignView(2, renderView2)
layout1.SetSize(1204, 694)

SetActiveView(renderView1)

# create a new 'Fast Uniform Grid'
fastUniformGrid1 = FastUniformGrid(registrationName='FastUniformGrid1')
fastUniformGrid1.GenerateSwirlVectors = 0
fastUniformGrid1.EnableSMP = 1

# create a new 'PassArrays'
passArrays1 = PassArrays(registrationName='PassArrays1', Input=fastUniformGrid1)

# create a new 'Contour'
contour1 = Contour(registrationName='Contour1', Input=fastUniformGrid1)
contour1.ContourBy = ['POINTS', 'DistanceSquared']
contour1.Isosurfaces = [100.0, 150.0, 200.0]
contour1.PointMergeMethod = 'Uniform Binning'

# show data from fastUniformGrid1
fastUniformGrid1Display = Show(fastUniformGrid1, renderView1, 'UniformGridRepresentation')

# get 2D transfer function for 'DistanceSquared'
distanceSquaredTF2D = GetTransferFunction2D('DistanceSquared')
distanceSquaredTF2D.ScalarRangeInitialized = 1
distanceSquaredTF2D.Range = [0.0, 300.0, 0.0, 1.0]

# get color transfer function/color map for 'DistanceSquared'
distanceSquaredLUT = GetColorTransferFunction('DistanceSquared')
distanceSquaredLUT.TransferFunction2D = distanceSquaredTF2D
distanceSquaredLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 150.0, 0.865003, 0.865003, 0.865003, 300.0, 0.705882, 0.0156863, 0.14902]
distanceSquaredLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'DistanceSquared'
distanceSquaredPWF = GetOpacityTransferFunction('DistanceSquared')
distanceSquaredPWF.Points = [0.0, 0.0, 0.5, 0.0, 300.0, 1.0, 0.5, 0.0]
distanceSquaredPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
fastUniformGrid1Display.Representation = 'Volume'
fastUniformGrid1Display.ColorArrayName = ['POINTS', 'DistanceSquared']
fastUniformGrid1Display.LookupTable = distanceSquaredLUT

fastUniformGrid1Display.BlendMode = 'Isosurface'
fastUniformGrid1Display.IsosurfaceValues = [100.0, 150.0, 200.0]

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
fastUniformGrid1Display.ScaleTransferFunction.Points = [-10.0, 0.0, 0.5, 0.0, 10.0, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
fastUniformGrid1Display.OpacityTransferFunction.Points = [-10.0, 0.0, 0.5, 0.0, 10.0, 1.0, 0.5, 0.0]

# show data from passArrays1
passArrays1Display = Show(passArrays1, renderView1, 'UniformGridRepresentation')

# trace defaults for the display properties.
passArrays1Display.Representation = 'Outline'

# show data from fastUniformGrid1
fastUniformGrid1Display_1 = Show(fastUniformGrid1, renderView2, 'UniformGridRepresentation')

# trace defaults for the display properties.
fastUniformGrid1Display_1.Representation = 'Outline'

# show data from contour1
contour1Display = Show(contour1, renderView2, 'GeometryRepresentation')

# trace defaults for the display properties.
contour1Display.Representation = 'Surface'
contour1Display.ColorArrayName = ['POINTS', 'DistanceSquared']
contour1Display.LookupTable = distanceSquaredLUT


# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
contour1Display.ScaleTransferFunction.Points = [100.0, 0.0, 0.5, 0.0, 200.0, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
contour1Display.OpacityTransferFunction.Points = [100.0, 0.0, 0.5, 0.0, 200.0, 1.0, 0.5, 0.0]

SetActiveSource(fastUniformGrid1)

AddCameraLink(renderView1, renderView2, 'CameraLink12')
