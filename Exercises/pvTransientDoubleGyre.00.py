# Demonstration script for paraview version 5.11
# written by Jean M. Favre, Swiss National Supercomputing Centre
# tested Mon Aug 14 12:52:39 PM CEST 2023
# see https://shaddenlab.berkeley.edu/uploads/LCS-tutorial/examples.html
# for reference to the data generation of the vector field
#
# a simple data generator for a 2D transient vector field

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Create a new 'Render View'
renderView1 = GetRenderView()

RequestData = """
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

RequestInfo = """
import numpy as np
executive = self.GetExecutive ()
outInfo = executive.GetOutputInformation(0)

dims = [256,128,1]
outInfo.Set(executive.WHOLE_EXTENT(), 0, dims[0]-1 , 0, dims[1]-1 , 0, dims[2]-1)
outInfo.Set(vtk.vtkDataObject.SPACING(), 2./(dims[0]-1), 1./(dims[1]-1), 1)
outInfo.Set(vtk.vtkDataObject.ORIGIN(), 0,0,0)
outInfo.Set(vtk.vtkAlgorithm.CAN_PRODUCE_SUB_EXTENT(), 1)
timesteps = np.arange(300)*.1
outInfo.Remove(executive.TIME_STEPS())
for timestep in timesteps:
  outInfo.Append(executive.TIME_STEPS(), timestep)
outInfo.Remove(executive.TIME_RANGE())
outInfo.Append(executive.TIME_RANGE(), timesteps[0])
outInfo.Append(executive.TIME_RANGE(), timesteps[-1])
"""

# create a new 'Programmable Source'
programmableSource1 = ProgrammableSource()
programmableSource1.OutputDataSetType = 'vtkImageData'
programmableSource1.Script = RequestData
programmableSource1.ScriptRequestInformation = RequestInfo
programmableSource1.UpdatePipelineInformation()

Show()
ResetCamera()

GetAnimationScene().UpdateAnimationUsingDataTimeSteps()

