# Demonstration script for paraview version 5.11
# written by Jean M. Favre, Swiss National Supercomputing Centre
# tested Mon Aug 14 12:52:39 PM CEST 2023
# see https://shaddenlab.berkeley.edu/uploads/LCS-tutorial/examples.html
# for reference to the data generation of the vector field

# demonstrates the use of streamlines, evenly-spaced streamlines, and glyphs
# representations

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
renderView1.InteractionMode = '2D'
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [1.0, 0.5, 0.0]
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [1.0, 0.5, 4.32]
renderView1.CameraFocalPoint = [1.0, 0.5, 0.0]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 0.68
renderView1.BackEnd = 'OSPRay raycaster'
renderView1.OSPRayMaterialLibrary = materialLibrary1

# create a new 'Programmable Source'
vectorField2D = ProgrammableSource(registrationName='VectorField2D')
vectorField2D.OutputDataSetType = 'vtkImageData'
vectorField2D.Script = """
from vtk.numpy_interface import algorithms as algs
import numpy as np
import math
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)
exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
whole = [executive.WHOLE_EXTENT().Get(outInfo, i) for i in range(6)]
ts = executive.UPDATE_TIME_STEP().Get(outInfo)
dims = (exts[1]-exts[0]+1, exts[3]-exts[2]+1, exts[5]-exts[4]+1)

output.SetExtent(exts)
xaxis = np.linspace(0, 2., dims[0])
yaxis = np.linspace(0,1., dims[1])
zaxis = np.linspace(0,1., dims[2])
[xc,yc, zc] = np.meshgrid(xaxis,yaxis, zaxis,indexing="xy")

A = 0.1
w = 2*np.pi/10.
E = 0.25

At = E*math.sin(w*ts)
Bt = 1 - 2*At
Ft = At*xc*xc + Bt * xc
fft = 2*At*xc + Bt
Vx = -np.pi * A * np.sin(np.pi*Ft) * np.cos(np.pi*yc)
Vy =  np.pi * A * np.cos(np.pi*Ft) * np.sin(np.pi*yc)*fft

Vz = np.zeros(Vy.shape)

output.PointData.append(Vx.ravel(), "u")
output.PointData.append(Vy.ravel(), "v")

output.PointData.append(algs.make_vector(Vx.ravel(), Vy.ravel(), Vz.ravel()), "velocity")

"""
vectorField2D.ScriptRequestInformation = """
import numpy as np
executive = self.GetExecutive ()
outInfo = executive.GetOutputInformation(0)

dims = [256,128,1]
outInfo.Set(executive.WHOLE_EXTENT(), 0, dims[0]-1 , 0, dims[1]-1 , 0, dims[2]-1)
outInfo.Set(vtk.vtkDataObject.SPACING(), 2./(dims[0]-1), 1./(dims[1]-1), 1)
outInfo.Set(vtk.vtkDataObject.ORIGIN(), 0,0,0)
outInfo.Set(vtk.vtkAlgorithm.CAN_PRODUCE_SUB_EXTENT(), 1)
time_increment = 0.1
Nb_of_timesteps = 300
timesteps = np.arange(Nb_of_timesteps) * time_increment
outInfo.Remove(executive.TIME_STEPS())
for timestep in timesteps:
  outInfo.Append(executive.TIME_STEPS(), timestep)
outInfo.Remove(executive.TIME_RANGE())
outInfo.Append(executive.TIME_RANGE(), timesteps[0])
outInfo.Append(executive.TIME_RANGE(), timesteps[-1])
"""
vectorField2D.UpdatePipelineInformation()


# create a new 'Evenly Spaced Streamlines 2D'
evenlySpacedStreamlines2D1 = EvenlySpacedStreamlines2D(registrationName='EvenlySpacedStreamlines2D1', Input=vectorField2D)
evenlySpacedStreamlines2D1.Vectors = ['POINTS', 'velocity']
evenlySpacedStreamlines2D1.StartPosition = [1.0, 0.5, 0.0]
evenlySpacedStreamlines2D1.UpdatePipelineInformation()

# create a new 'Glyph'
glyph1 = Glyph(registrationName='Glyph1', Input=evenlySpacedStreamlines2D1,
    GlyphType='Arrow')
glyph1.OrientationArray = ['POINTS', 'velocity']
glyph1.ScaleArray = ['POINTS', 'No scale array']
glyph1.ScaleFactor = 0.05
glyph1.GlyphTransform = 'Transform2'
glyph1.MaximumNumberOfSamplePoints = 150
glyph1.Stride = 7

# create a new 'Mask Points'
maskPoints = MaskPoints(registrationName='MaskPoints', Input=vectorField2D)
maskPoints.MaximumNumberofPoints = 100
maskPoints.RandomSampling = 1
maskPoints.RandomSamplingMode = 'Random Sampling'

# create a new 'Stream Tracer With Custom Source'
streamTracerWithCustomSource1 = StreamTracerWithCustomSource(registrationName='StreamTracerWithCustomSource1', Input=vectorField2D,
    SeedSource=maskPoints)
streamTracerWithCustomSource1.Vectors = ['POINTS', 'velocity']
streamTracerWithCustomSource1.MaximumStreamlineLength = 2.0

# show data from vectorField2D
vectorField2DDisplay = Show(vectorField2D, renderView1, 'UniformGridRepresentation')

# get color transfer function/color map for 'velocity'
velocityLUT = GetColorTransferFunction('velocity')
velocityLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 0.15707665246239672, 0.865003, 0.865003, 0.865003, 0.31415330492479343, 0.705882, 0.0156863, 0.14902]
velocityLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'velocity'
velocityPWF = GetOpacityTransferFunction('velocity')
velocityPWF.Points = [0.0, 0.0, 0.5, 0.0, 0.31415330492479343, 1.0, 0.5, 0.0]
velocityPWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
vectorField2DDisplay.Representation = 'Surface'
vectorField2DDisplay.ColorArrayName = ['POINTS', 'velocity']
vectorField2DDisplay.LookupTable = velocityLUT

vectorField2DDisplay.OSPRayScaleArray = 'u'
vectorField2DDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
vectorField2DDisplay.Orient = 1
vectorField2DDisplay.SelectOrientationVectors = 'velocity'
vectorField2DDisplay.Scaling = 1
vectorField2DDisplay.ScaleMode = 'Magnitude'
vectorField2DDisplay.ScaleFactor = 0.02
vectorField2DDisplay.SelectScaleArray = 'None'
vectorField2DDisplay.GlyphType = 'Arrow'
vectorField2DDisplay.GlyphTableIndexArray = 'None'
vectorField2DDisplay.GaussianRadius = 0.01
vectorField2DDisplay.SetScaleArray = ['POINTS', 'u']
vectorField2DDisplay.ScaleTransferFunction = 'PiecewiseFunction'
vectorField2DDisplay.OpacityArray = ['POINTS', 'u']
vectorField2DDisplay.OpacityTransferFunction = 'PiecewiseFunction'
vectorField2DDisplay.DataAxesGrid = 'GridAxesRepresentation'
vectorField2DDisplay.PolarAxes = 'PolarAxesRepresentation'
vectorField2DDisplay.ScalarOpacityUnitDistance = 0.07015151185016112
vectorField2DDisplay.ScalarOpacityFunction = velocityPWF
vectorField2DDisplay.OpacityArrayName = ['POINTS', 'u']
vectorField2DDisplay.ColorArray2Name = ['POINTS', 'u']
vectorField2DDisplay.SliceFunction = 'Plane'
vectorField2DDisplay.SelectInputVectors = ['POINTS', 'velocity']
vectorField2DDisplay.LICIntensity = 0.7
vectorField2DDisplay.EnhanceContrast = 'Color Only'


# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
vectorField2DDisplay.ScaleTransferFunction.Points = [-0.31415330492479343, 0.0, 0.5, 0.0, 0.31415330492479343, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
vectorField2DDisplay.OpacityTransferFunction.Points = [-0.31415330492479343, 0.0, 0.5, 0.0, 0.31415330492479343, 1.0, 0.5, 0.0]

# init the 'Plane' selected for 'SliceFunction'
vectorField2DDisplay.SliceFunction.Origin = [1.0, 0.5, 0.0]

# get color legend/bar for velocityLUT in view renderView1
velocityLUTColorBar = GetScalarBar(velocityLUT, renderView1)
velocityLUTColorBar.Title = 'velocity'
velocityLUTColorBar.ComponentTitle = 'Magnitude'

# set color bar visibility
velocityLUTColorBar.Visibility = 1

# show color legend
vectorField2DDisplay.SetScalarBarVisibility(renderView1, True)

SetActiveSource(vectorField2D)

