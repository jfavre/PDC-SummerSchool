# Demonstration script for paraview version 5.11
# written by Jean M. Favre, Swiss National Supercomputing Centre
# at first, we create an isocontour where Normals are not computed. Thus,
# no ghost-cells are needed.
# Then, we request Normals, and we demonstrate that the reader re-executes completely
#
# mpiexec -n 4 pvbatch pvMakeGhostCellsLog.py | grep "Execute Wavelet1 id"
# mpiexec -n 4 pvbatch pvMakeGhostCellsLog.py --ghostcells | grep "Execute Wavelet1 id"
#
# Tested Wed 23 Aug 08:37:00 CEST 2023
# You must run pvbatch with 4 MPI tasks

#### import the simple module from the paraview
from paraview.simple import *

from paraview.benchmark import *

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-g', '--ghostcells', action=argparse.BooleanOptionalAction)
args, unknown = parser.parse_known_args()

logbase.maximize_logs()
paraview.servermanager.SetProgressPrintingEnabled(0)

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Create a new 'Render View'
renderView2 = GetRenderView()

renderView2.Background = [0.32, 0.34, 0.43]

# create a new 'Wavelet'
wavelet1 = Wavelet()
wavelet1.WholeExtent = [0, 99, 0, 99, 0, 99]

# create a new 'Contour'
contour1 = Contour(Input=wavelet1)
contour1.ContourBy = ['POINTS', 'RTData']
contour1.Isosurfaces = [100]
contour1.ComputeNormals = 0
contour1.UpdatePipelineInformation()

# show data from wavelet1
wavelet1Display = Show(wavelet1)

# trace defaults for the display properties.
wavelet1Display.Representation = 'Outline'
wavelet1Display.ColorArrayName = ['POINTS', '']

# show data from contour1
contour1Display = Show(contour1)
contour1Display.Representation = 'Surface'

if args.ghostcells:
  contour1.ComputeNormals = 1
  Render()
logbase.print_logs()

