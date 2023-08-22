# tested with ParaView v5.11
# at first, we create an isocontour where Normals are not computed. Thus,
# no ghost-cells are needed.
# Then, we request Normals, and we demonstrate that the reader re-executes completely
# Tested Mon 24 Jul 15:30:13 CEST 2023 with 4 pvservers

#### import the simple module from the paraview
from paraview.simple import *

from paraview.benchmark import *

logbase.maximize_logs()
paraview.servermanager.SetProgressPrintingEnabled(0)


#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# Create a new 'Render View'
renderView2 = GetRenderView()
renderView2.AxesGrid = 'GridAxes3DActor'
renderView2.Background = [0.32, 0.34, 0.43]
renderView2.BackEnd = 'OSPRay raycaster'
renderView2.OSPRayMaterialLibrary = materialLibrary1

# create a new 'Wavelet'
wavelet1 = Wavelet()
wavelet1.WholeExtent = [0, 99, 0, 99, 0, 99]

# create a new 'Contour'
contour1 = Contour(Input=wavelet1)
contour1.ContourBy = ['POINTS', 'RTData']
contour1.Isosurfaces = [100]
contour1.ComputeNormals = 0
contour1.UpdatePipelineInformation()

# create a new 'Programmable Filter'
programmableFilter1 = ProgrammableFilter(Input=contour1)
programmableFilter1.Script = """
input = inputs[0]
output.DeepCopy(input.VTKObject)
ghost = output.GetCellData().GetArray("vtkGhostType")
# ghost is defined only if Nornals were requested
try:
  ghost.SetName("GhostCells")
except:
    pass
"""

# show data from wavelet1
wavelet1Display = Show(wavelet1, renderView2)

# trace defaults for the display properties.
wavelet1Display.Representation = 'Outline'
wavelet1Display.ColorArrayName = ['POINTS', '']

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
wavelet1Display.ScaleTransferFunction.Points = [-31.108078002929688, 0.0, 0.5, 0.0, 273.05389404296875, 1.0, 0.5, 0.0]

# show data from programmableFilter1
programmableFilter1Display = Show(programmableFilter1, renderView2)

# get color transfer function/color map for 'GhostCells'
ghostCellsLUT = GetColorTransferFunction('GhostCells')
ghostCellsLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
programmableFilter1Display.Representation = 'Surface'
programmableFilter1Display.ColorArrayName = ['CELLS', 'GhostCells']
programmableFilter1Display.LookupTable = ghostCellsLUT

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
programmableFilter1Display.ScaleTransferFunction.Points = [120.97290802001953, 0.0, 0.5, 0.0, 120.98853302001953, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
programmableFilter1Display.OpacityTransferFunction.Points = [120.97290802001953, 0.0, 0.5, 0.0, 120.98853302001953, 1.0, 0.5, 0.0]

# setup the color legend parameters for each legend in this view

# get color legend/bar for ghostCellsLUT in view renderView2
ghostCellsLUTColorBar = GetScalarBar(ghostCellsLUT, renderView2)
ghostCellsLUTColorBar.Title = 'GhostCells'
ghostCellsLUTColorBar.ComponentTitle = ''

# set color bar visibility
ghostCellsLUTColorBar.Visibility = 1

# show color legend
programmableFilter1Display.SetScalarBarVisibility(renderView2, True)

ResetCamera()

contour1.ComputeNormals = 1
Render()
logbase.print_logs()

