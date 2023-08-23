# Demonstration script for paraview version 5.11
# written by Jean M. Favre, Swiss National Supercomputing Centre
# tested Fri 18 Aug 16:07:30 CEST 2023
#
from paraview.simple import *

sphere1 = Sphere()
nbprocs = servermanager.ActiveConnection.GetNumberOfDataPartitions()

pid = ProcessIdScalars(Input=sphere1)

rep = Show(pid)

rep.RescaleTransferFunctionToDataRange(False, True)

ResetCamera()

SaveScreenshot(format("sphere.procs=%02d.png" % nbprocs))
