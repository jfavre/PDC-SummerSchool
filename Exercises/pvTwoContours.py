# state file tested using paraview version 5.11.1
# Two different isocontouring methods can be tested
#
# in interactive mode, you can call: paraview --script pvTwoContours.py
# and it will use the default implementation of the iso-contouring method
# in batch mode, you can call: pvbatch pvTwoContours.py -c contour
#                          or: pvbatch pvTwoContours.py -c flyingedge

import argparse
from paraview.simple import *

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--contour', choices=['contour', 'flyingedge'], type=str)
args, unknown = parser.parse_known_args()
isosurf_exec = args.contour

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

if isosurf_exec == "flyingedge":
  LoadPlugin("/local/apps/ParaView/ParaViewBuild/lib/paraview-5.11/plugins/AcceleratedAlgorithms/AcceleratedAlgorithms.so", ns=globals())
  
# Create a new 'Render View'
renderView1 = GetRenderView()
renderView1.CenterOfRotation = [0.5, 0.5, 0.5]
renderView1.CameraPosition = [1310.9443308006853, 549.0690628527462, 939.9242944380775]
renderView1.CameraFocalPoint = [0.5, 0.5, 0.5]
renderView1.CameraViewUp = [-0.33761488792479766, 0.9381406430257493, -0.07686560579843277]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 440

minx = 128 # min value of isocontour
maxx = 255 # min value of isocontour
M = 10     # number of isocontours
Isosurfaces = [minx + (maxx-minx)/(M-1)*i for i in range(M)]

N=255
wavelet1 = Wavelet(registrationName='Wavelet1')
wavelet1.WholeExtent = [-N, N+1, -N, N+1, -N, N+1]
wavelet1.UpdatePipeline()

if isosurf_exec == "flyingedge":
  contour = FlyingEdges3D(registrationName='FlyingEdges3D', Input=wavelet1)
  print("using a FlyingEdges3D method")
else:
# create a new classic 'Contour'
  contour = Contour(registrationName='Contour', Input=wavelet1)
  
contour.ContourBy = ['POINTS', 'RTData']
contour.ComputeScalars = 1
contour.ComputeGradients = 1
contour.Isosurfaces = Isosurfaces

wavelet1Display = Show(wavelet1)

# trace defaults for the display properties.
wavelet1Display.Representation = 'Outline'

ContourDisplay = Show(contour)
ContourDisplay.Representation = 'Surface'
ColorBy(ContourDisplay, ['POINTS', 'RTData'])
ResetCamera()
