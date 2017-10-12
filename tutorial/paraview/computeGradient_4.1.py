# First argument: volume solution path
# Second argument: field
# Third argument: print folder

import sys

#### import the simple module from the paraview
from paraview.simple import *

paraview.simple._DisableFirstRenderCameraReset()

soln_volume_vtk = LegacyVTKReader(FileNames=[str(sys.argv[1])])

GradientOfUnstructuredDataSet1 = GradientOfUnstructuredDataSet()
GradientOfUnstructuredDataSet1.ScalarArray = ['POINTS', str(sys.argv[2])]
GradientOfUnstructuredDataSet1.ResultArrayName = str(sys.argv[2]) + 'Gradient'

writer = paraview.simple.CreateWriter(str(sys.argv[3]) + str(sys.argv[2]) + 'Gradient.csv')
writer.WriteAllTimeSteps = 0
writer.FieldAssociation = "Points"
writer.UpdatePipeline()

