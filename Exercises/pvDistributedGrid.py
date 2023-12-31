# Demonstration script for paraview version 5.11
# written by Jean M. Favre, Swiss National Supercomputing Centre
# Tested Wed 23 Aug 08:37:00 CEST 2023
# You must run a client-server ParaView with a server running 4 MPI tasks
#
#### import the simple module from the paraview
from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()

renderView1 = CreateView('RenderView')
renderView1.CenterOfRotation = [0.3010299956639812, 0.23856062735983122, 0.1505149978319906]
renderView1.CameraPosition = [-0.7440905995976052, 0.9733595044416852, 2.122880782708075]
renderView1.CameraFocalPoint = [1.485716290522814, -0.5943634993900108, -2.085241071261971]
renderView1.CameraViewUp = [0.1532271769887699, 0.9498294045717282, -0.272663775450588]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 1.338885534815494

renderView2 = CreateView('RenderView')
renderView2.CenterOfRotation = renderView1.CenterOfRotation
renderView2.CameraPosition = renderView1.CameraPosition
renderView2.CameraFocalPoint = renderView1.CameraFocalPoint
renderView2.CameraViewUp = renderView1.CameraViewUp
renderView2.CameraFocalDisk = 1.0
renderView2.CameraParallelScale = renderView1.CameraParallelScale

renderView3 = CreateView('RenderView')
renderView3.CenterOfRotation = renderView1.CenterOfRotation
renderView3.CameraPosition = renderView1.CameraPosition
renderView3.CameraFocalPoint = renderView1.CameraFocalPoint
renderView3.CameraViewUp = renderView1.CameraViewUp
renderView3.CameraFocalDisk = 1.0
renderView3.CameraParallelScale = renderView1.CameraParallelScale

renderView4 = CreateView('RenderView')
renderView4.CenterOfRotation = renderView1.CenterOfRotation
renderView4.CameraPosition = renderView1.CameraPosition
renderView4.CameraFocalPoint = renderView1.CameraFocalPoint
renderView4.CameraViewUp = renderView1.CameraViewUp
renderView4.CameraFocalDisk = 1.0
renderView4.CameraParallelScale = renderView1.CameraParallelScale

SetActiveView(renderView1)

SS="""
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)
pid = outInfo.Get(executive.UPDATE_PIECE_NUMBER())
exts = [executive.UPDATE_EXTENT().Get(outInfo, i) for i in range(6)]
whole = [executive.WHOLE_EXTENT().Get(outInfo, i) for i in range(6)]
dims =        [ exts[1]- exts[0]+1,  exts[3]- exts[2]+1,  exts[5]- exts[4]+1]
global_dims = [whole[1]-whole[0]+1, whole[3]-whole[2]+1, whole[5]-whole[4]+1]
output.SetExtent(exts)

print('pvRectilinearGrid: pid = ', pid, ', exts = ', exts)

xaxis = np.log10(np.linspace(1., 4.0, global_dims[0]))[exts[0]:exts[1]+1]
yaxis = np.log10(np.linspace(1., 3.0, global_dims[1]))[exts[2]:exts[3]+1]
zaxis = np.log10(np.linspace(1., 2.0, global_dims[2]))[exts[4]:exts[5]+1]

output.SetXCoordinates(dsa.numpyTovtkDataArray( xaxis , 'X'))
output.SetYCoordinates(dsa.numpyTovtkDataArray( yaxis , 'Y'))
output.SetZCoordinates(dsa.numpyTovtkDataArray( zaxis , 'Z'))

x = np.array([])
for k in range(zaxis.size):
  for j in range(yaxis.size):
    x = np.concatenate((x, xaxis))
output.PointData.append(x, 'x')
"""

BlockMode  = "vtk.vtkExtentTranslator.BLOCK_MODE)"
X_SLABMode = "vtk.vtkExtentTranslator.X_SLAB_MODE)"
Y_SLABMode = "vtk.vtkExtentTranslator.Y_SLAB_MODE)"
Z_SLABMode = "vtk.vtkExtentTranslator.Z_SLAB_MODE)"

SRI="""dims = [40, 30, 20]
executive = self.GetExecutive()
outInfo = executive.GetOutputInformation(0)
outInfo.Set(executive.WHOLE_EXTENT(), 0, dims[0]-1, 0, dims[1]-1, 0, dims[2]-1)
outInfo.Set(vtk.vtkAlgorithm.CAN_PRODUCE_SUB_EXTENT(), 1)
# optionally set the splitting mode. default is 3 (BLOCK_MODE), otherwise [XYZ]_SLAB_MODE = 0, 1, 2
outInfo.Set(vtk.vtkExtentTranslator.UPDATE_SPLIT_MODE(), 
"""

# create a new 'Programmable Source'
programmableSource1 = ProgrammableSource(registrationName='BLOCK_Distribution')
programmableSource1.OutputDataSetType = 'vtkRectilinearGrid'
programmableSource1.Script = SS
programmableSource1.ScriptRequestInformation = f"""{SRI}{BlockMode}"""

# create a new 'Programmable Source'
programmableSource2 = ProgrammableSource(registrationName='X_SLAB_Distribution')
programmableSource2.OutputDataSetType = 'vtkRectilinearGrid'
programmableSource2.Script = SS
programmableSource2.ScriptRequestInformation = f"""{SRI}{X_SLABMode}"""

# create a new 'Programmable Source'
programmableSource3 = ProgrammableSource(registrationName='Y_SLAB_Distribution')
programmableSource3.OutputDataSetType = 'vtkRectilinearGrid'
programmableSource3.Script = SS
programmableSource3.ScriptRequestInformation = f"""{SRI}{Y_SLABMode}"""

# create a new 'Programmable Source'
programmableSource4 = ProgrammableSource(registrationName='Z_SLAB_Distribution')
programmableSource4.OutputDataSetType = 'vtkRectilinearGrid'
programmableSource4.Script = SS
programmableSource4.ScriptRequestInformation = f"""{SRI}{Z_SLABMode}"""

programmableSource1Display = Show(programmableSource1, renderView1, 'UniformGridRepresentation')

# get color transfer function/color map for 'vtkProcessId'
vtkProcessIdLUT = GetColorTransferFunction('vtkProcessId')
vtkProcessIdLUT.InterpretValuesAsCategories = 1
vtkProcessIdLUT.AnnotationsInitialized = 1
vtkProcessIdLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 1.5, 0.865003, 0.865003, 0.865003, 3.0, 0.705882, 0.0156863, 0.14902]
vtkProcessIdLUT.ScalarRangeInitialized = 1.0
vtkProcessIdLUT.Annotations = ['0', '0', '1', '1', '2', '2', '3', '3']
vtkProcessIdLUT.ActiveAnnotatedValues = ['0', '1', '2', '3']
vtkProcessIdLUT.IndexedColors = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
vtkProcessIdLUT.IndexedOpacities = [1.0, 1.0, 1.0, 1.0]

# trace defaults for the display properties.
programmableSource1Display.Representation = 'Surface'
programmableSource1Display.ColorArrayName = ['POINTS', 'vtkProcessId']
programmableSource1Display.LookupTable = vtkProcessIdLUT

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
programmableSource1Display.ScaleTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.6020599913279624, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
programmableSource1Display.OpacityTransferFunction.Points = [0.0, 0.0, 0.5, 0.0, 0.6020599913279624, 1.0, 0.5, 0.0]

# init the 'Plane' selected for 'SliceFunction'
programmableSource1Display.SliceFunction.Origin = [0.3010299956639812, 0.23856062735983122, 0.1505149978319906]

text1 = Text(registrationName='BLOCK_label')
text1.Text = 'Default BLOCK_MODE'
text1Display = Show(text1, renderView1, 'TextSourceRepresentation')
text1Display.WindowLocation = 'Lower Center'

text2 = Text(registrationName='X_SLAB_label')
text2.Text = 'Default X_SLAB_MODE'
text2Display = Show(text2, renderView2, 'TextSourceRepresentation')
text2Display.WindowLocation = 'Lower Center'

text3 = Text(registrationName='Y_SLAB_label')
text3.Text = 'Default Y_SLAB_MODE'
text3Display = Show(text3, renderView3, 'TextSourceRepresentation')
text3Display.WindowLocation = 'Lower Center'

text4 = Text(registrationName='Z_SLAB_label')
text4.Text = 'Default Z_SLAB_MODE'
text4Display = Show(text4, renderView4, 'TextSourceRepresentation')
text4Display.WindowLocation = 'Lower Center'

vtkProcessIdLUTColorBar = GetScalarBar(vtkProcessIdLUT, renderView1)
vtkProcessIdLUTColorBar.Orientation = 'Horizontal'
vtkProcessIdLUTColorBar.WindowLocation = 'Any Location'
vtkProcessIdLUTColorBar.Position = [0.3681981981981981, 0.9059109311740892]
vtkProcessIdLUTColorBar.Title = 'vtkProcessId'
vtkProcessIdLUTColorBar.ScalarBarLength = 0.3

# set color bar visibility
vtkProcessIdLUTColorBar.Visibility = 1

programmableSource1Display.SetScalarBarVisibility(renderView1, True)

programmableSource2Display = Show(programmableSource2, renderView2, 'UniformGridRepresentation')
programmableSource2Display.Representation = 'Surface'
programmableSource2Display.ColorArrayName = ['POINTS', 'vtkProcessId']
programmableSource2Display.LookupTable = vtkProcessIdLUT

programmableSource3Display = Show(programmableSource3, renderView3, 'UniformGridRepresentation')
programmableSource3Display.Representation = 'Surface'
programmableSource3Display.ColorArrayName = ['POINTS', 'vtkProcessId']
programmableSource3Display.LookupTable = vtkProcessIdLUT

programmableSource4Display = Show(programmableSource4, renderView4, 'UniformGridRepresentation')
programmableSource4Display.Representation = 'Surface'
programmableSource4Display.ColorArrayName = ['POINTS', 'vtkProcessId']
programmableSource4Display.LookupTable = vtkProcessIdLUT

SetActiveView(None)

# create new layout object 'Layout #1'
layout1 = CreateLayout(name='Layout #1')
layout1.SplitHorizontal(0, 0.5)
layout1.AssignView(1, renderView1)
layout1.SplitHorizontal(2, 0.5)
layout1.AssignView(5, renderView2)
layout1.SplitHorizontal(6, 0.5)
layout1.AssignView(13, renderView3)
layout1.AssignView(14, renderView4)

layout1.SetSplitFraction(0, 0.25)
layout1.SetSplitFraction(2, 0.3333)
layout1.SetSplitFraction(6, 0.5)

AddCameraLink(renderView2, renderView1, 'CameraLink0')
AddCameraLink(renderView3, renderView1, 'CameraLink1')
AddCameraLink(renderView4, renderView1, 'CameraLink2')
SetActiveView(renderView1)
