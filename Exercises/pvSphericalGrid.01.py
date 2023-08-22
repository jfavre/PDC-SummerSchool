# Demonstration script for paraview version 5.9
#
# Creates a spherical grid with a Python ProgrammableSource.
# Works also in parallel by splitting the extents
#
# written by Jean M. Favre, Swiss National Supercomputing Centre
#
# See http://mathworld.wolfram.com/SphericalCoordinates.html

from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

viewSG = GetRenderView()

ReqDataScript = """
import numpy as np
from vtk.numpy_interface import algorithms as algs
from vtkGridConstructors import vtkStructuredGridFromArrays

executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)
exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
whole = [executive.WHOLE_EXTENT().Get(outInfo, i) for i in range(6)]

global_dims = ([whole[1]-whole[0]+1, whole[3]-whole[2]+1, whole[5]-whole[4]+1])
print(global_dims)
output.SetExtent(exts)
print(exts)
Raxis = np.linspace(1., 2., global_dims[0])[exts[0]:exts[1]+1]
#print('Raxis=', Raxis)
# only use 3/4 of the full longitude in order to view the inside of the sphere
Thetaaxis = np.linspace(0.,np.pi*1.5, global_dims[1])[exts[2]:exts[3]+1]
#print('Theta=', Thetaaxis)
Phiaxis = np.linspace(0.,np.pi*1.0, global_dims[2])[exts[4]:exts[5]+1]
#print('Phi=', Phiaxis)
p, t, r = np.meshgrid(Phiaxis, Thetaaxis, Raxis, indexing="ij")
X = r * np.cos(t) * np.sin(p)
Y = r * np.sin(t) * np.sin(p)
Z = r * np.cos(p)

G = vtkStructuredGridFromArrays()

G.SetCoordinates(X, Y, Z)
G.AddArray(r.ravel(), "radius")
G.AddArray(t.ravel(), "theta")
G.AddArray(p.ravel(), "phi")
# reduce dimension of array by 1 in all directions
G.AddCellArray(p[1:,1:,1:].ravel(), "phi")

V = algs.make_vector(X.ravel(),
                   Y.ravel(),
                   Z.ravel())
                   
# V is a 2D array of shape(np.prod(global_dims), 3)
G.AddArray(V, "Velocity")

# reduce dimension of array by 1 in all directions, except the last to keep velocity a 3-tuple
Vcell = V.reshape(global_dims[2],global_dims[1],global_dims[0],3)[1:,1:,1:,:].reshape((global_dims[0]-1)*(global_dims[1]-1)*(global_dims[2]-1), 3)
G.AddCellArray(Vcell, "Velocity")

output.ShallowCopy(G.GetOutput())
"""

ReqInfoScript = """
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)
# A 3D spherical mesh
dims = [55, 99, 77] # radius, theta(east-west longitude), phi(north-south latitude)
outInfo.Set(executive.WHOLE_EXTENT(), 0, dims[0]-1 , 0, dims[1]-1 , 0, dims[2]-1)
outInfo.Set(vtk.vtkAlgorithm.CAN_PRODUCE_SUB_EXTENT(), 1)
"""

programmableSource1 = ProgrammableSource()
programmableSource1.OutputDataSetType = 'vtkStructuredGrid'
programmableSource1.Script = ReqDataScript
programmableSource1.ScriptRequestInformation = ReqInfoScript
programmableSource1.PythonPath = '"/users/jfavre/Projects/ParaView/Python"'
rep2 = Show()
rep2.Representation = 'Surface With Edges'
Render()


# create a new 'Glyph'
glyph1 = Glyph(registrationName='Glyph1', Input=programmableSource1,
    GlyphType='Arrow')
glyph1.OrientationArray = ['POINTS', 'Velocity']
glyph1.ScaleArray = ['POINTS', 'No scale array']
glyph1.ScaleFactor = 0.4
glyph1.GlyphMode = 'All Points'

glyph1Display = Show(glyph1)
