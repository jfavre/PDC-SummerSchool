# Demonstration script for paraview version 5.11
# written by Jean M. Favre, Swiss National Supercomputing Centre
#
# Tested Wed 23 Aug 08:37:00 CEST 2023

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Create a new 'Render View'
renderView1 = GetRenderView()
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [51.0, 46.5, 80.0]
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [-179.45896001387192, -289.7165091461378, 102.23491482516813]
renderView1.CameraFocalPoint = [50.99999999999993, 46.50000000000003, 79.99999999999994]
renderView1.CameraViewUp = [0.07427281593734669, 0.015032414212105032, 0.9971246538601344]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 105.65628234989153

# create a new 'Meta File Series Reader'
reader = MetaFileSeriesReader(registrationName='tooth.mhd', FileNames=['tooth.mhd'])
reader.UpdatePipeline()

# show data from reader
readerDisplay = Show(reader, renderView1, 'UniformGridRepresentation')
readerDisplay.Representation = 'Outline'
readerDisplay.ColorArrayName = ['POINTS', 'MetaImage']
readerDisplay.OSPRayScaleArray = 'MetaImage'

# create a new 'Gradient'
gradient1 = PythonCalculator(registrationName='Gradient', Input=reader)
gradient1.Expression = 'algs.gradient(MetaImage)'
gradient1.ArrayName = 'densityGradient'

# get color transfer function/color map for 'MetaImage'
metaImageLUT = GetColorTransferFunction('MetaImage')
metaImageLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 650.0, 0.865003, 0.865003, 0.865003, 1300.0, 0.705882, 0.0156863, 0.14902]
metaImageLUT.ScalarRangeInitialized = 1.0


# show data from gradient1
gradient1Display = Show(gradient1, renderView1, 'UniformGridRepresentation')

# get separate color transfer function/color map for 'MetaImage'
separate_gradient1Display_MetaImageLUT = GetColorTransferFunction('MetaImage', gradient1Display, separate=True)
separate_gradient1Display_MetaImageLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 650.0, 0.865003, 0.865003, 0.865003, 1300.0, 0.705882, 0.0156863, 0.14902]
separate_gradient1Display_MetaImageLUT.ScalarRangeInitialized = 1.0

# get separate opacity transfer function/opacity map for 'MetaImage'
separate_gradient1Display_MetaImagePWF = GetOpacityTransferFunction('MetaImage', gradient1Display, separate=True)
separate_gradient1Display_MetaImagePWF.Points = [0.0, 0.0, 0.5, 0.0, 102.7579116821289, 0.0, 0.5, 0.0, 371.8353130083263, 1.0, 0.5, 0.0]
separate_gradient1Display_MetaImagePWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
gradient1Display.Representation = 'Volume'
gradient1Display.ColorArrayName = ['POINTS', 'MetaImage']
gradient1Display.LookupTable = separate_gradient1Display_MetaImageLUT
gradient1Display.OSPRayScaleArray = 'densityGradient'
gradient1Display.OSPRayScaleFunction = 'PiecewiseFunction'
gradient1Display.SelectOrientationVectors = 'densityGradient'
gradient1Display.ScaleFactor = 16.0
gradient1Display.ScalarOpacityUnitDistance = 1.0
gradient1Display.SelectScaleArray = 'densityGradient'
gradient1Display.GaussianRadius = 0.8
gradient1Display.SetScaleArray = ['POINTS', 'MetaImageGradient']
gradient1Display.ScaleTransferFunction = 'PiecewiseFunction'
gradient1Display.OpacityArray = ['POINTS', 'MetaImageGradient']
gradient1Display.OpacityTransferFunction = 'PiecewiseFunction'
gradient1Display.DataAxesGrid = 'GridAxesRepresentation'
gradient1Display.PolarAxes = 'PolarAxesRepresentation'
gradient1Display.ScalarOpacityFunction = separate_gradient1Display_MetaImagePWF

# new in version 5.9
# https://blog.kitware.com/paraview-5-9-0-release-notes/#rendering-enhancements
# Volume rendering with a separate opacity array

gradient1Display.UseSeparateOpacityArray = 0 # 1
gradient1Display.OpacityArrayName = ['POINTS', 'densityGradient']
gradient1Display.OpacityComponent = 'Magnitude'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
gradient1Display.ScaleTransferFunction.Points = [-298.0, 0.0, 0.5, 0.0, 276.5, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
gradient1Display.OpacityTransferFunction.Points = [-298.0, 0.0, 0.5, 0.0, 276.5, 1.0, 0.5, 0.0]

# init the 'Plane' selected for 'SliceFunction'
gradient1Display.SliceFunction.Origin = [51.0, 46.5, 80.0]

# set separate color map
gradient1Display.UseSeparateColorMap = True
gradient1Display.RescaleTransferFunctionToDataRange(False, True)

SetActiveSource(gradient1)

