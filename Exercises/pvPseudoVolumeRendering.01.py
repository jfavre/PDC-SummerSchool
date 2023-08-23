# Demonstration script for paraview version 5.11
# written by Jean M. Favre, Swiss National Supercomputing Centre
#
import paraview
paraview.compatibility.major = 5
paraview.compatibility.minor = 11

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

materialLibrary1 = GetMaterialLibrary()

# Create a new 'Render View'
renderView1 = GetRenderView()
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [51.0, 46.5, 80.0]
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [-30.520522965963707, 444.359331197335, 121.34757096779862]
renderView1.CameraFocalPoint = [51.0, 46.5, 80.0]
renderView1.CameraViewUp = [-0.0074621018162650855, -0.10487802234807803, 0.9944570968447256]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 105.65628234989153
renderView1.BackEnd = 'OSPRay raycaster'
renderView1.OSPRayMaterialLibrary = materialLibrary1

reader = MetaFileSeriesReader(registrationName='tooth.mhd', FileNames=['./tooth.mhd'])

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=reader)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
N=50 #(distance from mid-plane in Y direction)
# generate slices every delta_y = 1 from -N to +N
slice1.SliceOffsetValues = [(i-N) for i in range(2*N+1)]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [51.0, 46.5, 80.0]
slice1.SliceType.Normal = [0.0, 1.0, 0.0]

# show data from reader
readerDisplay = Show(reader, renderView1, 'UniformGridRepresentation')

# trace defaults for the display properties.
readerDisplay.Representation = 'Outline'


# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
readerDisplay.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1300.0, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
readerDisplay.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 1300.0, 1.0, 0.5, 0.0]

# init the 'Plane' selected for 'SliceFunction'
readerDisplay.SliceFunction.Origin = [51.0, 46.5, 80.0]

# show data from slice1
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

# get color transfer function/color map for 'MetaImage'
metaImageLUT = GetColorTransferFunction('MetaImage')
metaImageLUT.EnableOpacityMapping = 1

metaImageLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 646.0, 0.865003, 0.865003, 0.865003, 1292.0, 0.705882, 0.0156863, 0.14902]
metaImageLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['POINTS', 'MetaImage']
slice1Display.LookupTable = metaImageLUT
slice1Display.OSPRayScaleArray = 'MetaImage'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectScaleArray = 'MetaImage'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'MetaImage'
slice1Display.SetScaleArray = ['POINTS', 'MetaImage']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = ['POINTS', 'MetaImage']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
slice1Display.ScaleTransferFunction.Points = [19.0, 0.0, 0.5, 0.0, 1280.0, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
slice1Display.OpacityTransferFunction.Points = [19.0, 0.0, 0.5, 0.0, 1280.0, 1.0, 0.5, 0.0]

# get color legend/bar for metaImageLUT in view renderView1
metaImageLUTColorBar = GetScalarBar(metaImageLUT, renderView1)
metaImageLUTColorBar.Title = 'MetaImage'
metaImageLUTColorBar.ComponentTitle = ''

# set color bar visibility
metaImageLUTColorBar.Visibility = 1

# show color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get opacity transfer function/opacity map for 'MetaImage'
metaImagePWF = GetOpacityTransferFunction('MetaImage')
metaImagePWF.Points = [0.0, 0.0, 0.5, 0.0, 446.8379386225833, 0.0, 0.5, 0.0, 1292.0, 1.0, 0.5, 0.0]
metaImagePWF.ScalarRangeInitialized = 1

SetActiveSource(slice1)

