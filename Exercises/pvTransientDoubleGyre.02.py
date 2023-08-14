# Demonstration script for paraview version 5.11
# written by Jean M. Favre, Swiss National Supercomputing Centre
# tested Mon Aug 14 12:52:39 PM CEST 2023
# see https://shaddenlab.berkeley.edu/uploads/LCS-tutorial/examples.html
# for reference to the data generation of the vector field

# demonstrates the use of animated particles, and animated pathlines

import paraview
paraview.compatibility.major = 5
paraview.compatibility.minor = 11

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

ImageResolution=[512,300]

# Create a new 'Render View'
renderView1 = GetRenderView()
renderView1.ViewSize = ImageResolution
renderView1.InteractionMode = '2D'
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [1.0, 0.5, 0.0]
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [1.0, 0.5, 4.32]
renderView1.CameraFocalPoint = [1.0, 0.5, 0.0]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 0.68
renderView1.OrientationAxesVisibility = 0
renderView1.BackEnd = 'OSPRay raycaster'

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

# create a new 'Particle Tracer'
particleTracer1 = ParticleTracer(registrationName='ParticleTracer1', Input=vectorField2D,
    SeedSource=maskPoints)
particleTracer1.StaticSeeds = 1
particleTracer1.MeshOverTime = 'Static'
particleTracer1.ForceReinjectionEveryNSteps = 15
particleTracer1.SelectInputVectors = ['POINTS', 'velocity']

# create a new 'Temporal Particles To Pathlines'
temporalParticlesToPathlines1 = TemporalParticlesToPathlines(registrationName='TemporalParticlesToPathlines1', Input=particleTracer1,
    Selection=None)
temporalParticlesToPathlines1.MaskPoints = 1
temporalParticlesToPathlines1.MaxTrackLength = 5
temporalParticlesToPathlines1.MaxStepDistance = [10.0, 10.0, 10.0]
temporalParticlesToPathlines1.IdChannelArray = 'ParticleId'

# create a new 'Evenly Spaced Streamlines 2D'
evenlySpacedStreamlines2D1 = EvenlySpacedStreamlines2D(registrationName='EvenlySpacedStreamlines2D1', Input=vectorField2D)
evenlySpacedStreamlines2D1.Vectors = ['POINTS', 'velocity']
evenlySpacedStreamlines2D1.StartPosition = [1.0, 0.5, 0.0]

# create a new 'Glyph'
glyph1 = Glyph(registrationName='Glyph1', Input=evenlySpacedStreamlines2D1,
    GlyphType='Arrow')
glyph1.OrientationArray = ['POINTS', 'velocity']
glyph1.ScaleArray = ['POINTS', 'No scale array']
glyph1.ScaleFactor = 0.05
glyph1.GlyphTransform = 'Transform2'
glyph1.GlyphMode = 'Every Nth Point'
glyph1.MaximumNumberOfSamplePoints = 300
glyph1.Stride = 2

# show data from vectorField2D
vectorField2DDisplay = Show(vectorField2D, renderView1, 'UniformGridRepresentation')
vectorField2DDisplay.Representation = 'Surface'
ColorBy(vectorField2DDisplay, ['POINTS', 'velocity'])

# get color transfer function/color map for 'velocity'
velocityLUT = GetColorTransferFunction('velocity')

# init the 'Piecewise Function' selected for 'ScaleTransferFunction'
vectorField2DDisplay.ScaleTransferFunction.Points = [-0.31415330492479343, 0.0, 0.5, 0.0, 0.31415330492479343, 1.0, 0.5, 0.0]

# init the 'Piecewise Function' selected for 'OpacityTransferFunction'
vectorField2DDisplay.OpacityTransferFunction.Points = [-0.31415330492479343, 0.0, 0.5, 0.0, 0.31415330492479343, 1.0, 0.5, 0.0]

# init the 'Plane' selected for 'SliceFunction'
vectorField2DDisplay.SliceFunction.Origin = [1.0, 0.5, 0.0]

# show data from particleTracer1
particleTracer1Display = Show(particleTracer1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
particleTracer1Display.Representation = 'Surface'
particleTracer1Display.ColorArrayName = ['POINTS', 'velocity']
particleTracer1Display.LookupTable = velocityLUT
particleTracer1Display.PointSize = 5.0
particleTracer1Display.RenderPointsAsSpheres = 1

# create a new 'Annotate Time Filter'
annotateTimeFilter1 = AnnotateTimeFilter(registrationName='AnnotateTimeFilter1', Input=vectorField2D)

annotateTimeFilter1Display = Show(annotateTimeFilter1)
annotateTimeFilter1Display.Bold = 1
annotateTimeFilter1Display.FontSize = 24

velocityLUTColorBar = GetScalarBar(velocityLUT, renderView1)
velocityLUTColorBar.Orientation = 'Horizontal'
velocityLUTColorBar.WindowLocation = 'Any Location'
velocityLUTColorBar.Position = [0.63, 0.0175]
velocityLUTColorBar.Title = 'velocity'
velocityLUTColorBar.ComponentTitle = 'Magnitude'
velocityLUTColorBar.ScalarBarLength = 0.33

# show color legend
vectorField2DDisplay.SetScalarBarVisibility(renderView1, True)

# show color legend
particleTracer1Display.SetScalarBarVisibility(renderView1, True)

scene = GetAnimationScene()
scene.UpdateAnimationUsingDataTimeSteps()
SetActiveSource(vectorField2D)


# for the exercise
#Show the source data as an outline Bounding box
# Show the temporal particles-to-pathlines
vectorField2DDisplay.Representation = 'Outline'
Hide(particleTracer1)
Pathlines = Show(temporalParticlesToPathlines1)
Particles= Show(OutputPort(temporalParticlesToPathlines1, 1))
Particles.PointSize = 5.0
Particles.RenderPointsAsSpheres = 1
SaveAnimation("foo.png", ImageResolution=ImageResolution)

