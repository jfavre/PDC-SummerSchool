# state file tested using paraview version 5.1.1

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Create a new 'Render View'
renderView2 = CreateView('RenderView')
renderView2.ViewSize = [655, 794]
renderView2.CenterOfRotation = [49.5, 49.5, 49.5]
renderView2.CameraPosition = [253.24767267447768, 230.14817513253612, 341.9172097043133]
renderView2.CameraFocalPoint = [84.33143647783308, 80.38248986783933, 99.4898297298046]
renderView2.CameraViewUp = [-0.27825063202038536, 0.8917014825312399, -0.3569944703098983]
renderView2.CameraFocalDisk = 1.0
renderView2.CameraParallelScale = 85.73651497465943
renderView2.Background = [0.32, 0.34, 0.43]

# Create a new 'Render View'
renderView3 = CreateView('RenderView')
renderView3.ViewSize = renderView2.ViewSize
renderView3.CenterOfRotation = renderView2.CenterOfRotation
renderView3.CameraPosition = renderView2.CameraPosition
renderView3.CameraFocalPoint = renderView2.CameraFocalPoint
renderView3.CameraViewUp = renderView2.CameraViewUp
renderView3.CameraFocalDisk = 1.0
renderView3.CameraParallelScale = renderView2.CameraParallelScale
renderView3.Background = renderView2.Background
renderView3.BackEnd = 'OSPRay raycaster'

SetActiveView(None)

# create new layout object 'Layout #1'
layout1_1 = CreateLayout(name='Layout #1')
layout1_1.SplitHorizontal(0, 0.5)
layout1_1.AssignView(1, renderView2)
layout1_1.AssignView(2, renderView3)

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView2)
# ----------------------------------------------------------------

# create a new 'Wavelet'
wavelet1 = Wavelet()
wavelet1.WholeExtent = [0, 99, 0, 99, 0, 99]

# create a new 'Programmable Filter'
programmableFilter1 = ProgrammableFilter(Input=wavelet1)
programmableFilter1.Script = """input = inputs[0]
output.DeepCopy(input.VTKObject)
output.GetCellData().GetArray("vtkGhostType").SetName("GhostCells")"""
programmableFilter1.RequestInformationScript = ''
programmableFilter1.RequestUpdateExtentScript = ''
programmableFilter1.PythonPath = ''

# create a new 'Contour'
contour1 = Contour(Input=wavelet1)
contour1.ContourBy = ['POINTS', 'RTData']
contour1.Isosurfaces = [100.]
contour1.PointMergeMethod = 'Uniform Binning'
contour1.UpdatePipeline()

programmableFilter2 = ProgrammableFilter(Input=contour1)
programmableFilter2.Script = """input = inputs[0]
output.DeepCopy(input.VTKObject)
output.GetCellData().GetArray("vtkGhostType").SetName("GhostCells")"""
programmableFilter2.RequestInformationScript = ''
programmableFilter2.RequestUpdateExtentScript = ''
programmableFilter2.PythonPath = ''

# show data from wavelet1
wavelet1Display = Show(wavelet1, renderView2)

# trace defaults for the display properties.
wavelet1Display.Representation = 'Outline'
wavelet1Display.ColorArrayName = ['POINTS', '']

# show data from programmableFilter1
programmableFilter1Display = Show(programmableFilter1, renderView2)

# get color transfer function/color map for 'GhostCells'
ghostCellsLUT = GetColorTransferFunction('GhostCells')
ghostCellsLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
programmableFilter1Display.Representation = 'Surface'
programmableFilter1Display.ColorArrayName = ['CELLS', 'GhostCells']
programmableFilter1Display.LookupTable = ghostCellsLUT

wavelet1Display_1 = Show(wavelet1, renderView3)

# trace defaults for the display properties.
wavelet1Display_1.Representation = 'Outline'
wavelet1Display_1.ColorArrayName = ['POINTS', '']

# show data from programmableFilter2
programmableFilter2Display = Show(programmableFilter2, renderView3)

# trace defaults for the display properties.
programmableFilter2Display.Representation = 'Surface'
programmableFilter2Display.ColorArrayName = ['CELLS', 'GhostCells']
programmableFilter2Display.LookupTable = ghostCellsLUT

SetActiveSource(programmableFilter1)

AddCameraLink(renderView3, renderView2, 'CameraLink0')
