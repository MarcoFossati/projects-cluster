# First argument: volume solution path
# Second argument: field
# Third argument: print folder

import sys

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Legacy VTK Reader'
soln_volumevtk = LegacyVTKReader(FileNames=[sys.argv[1]])

# get active view
#renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1063, 860]

# get color transfer function/color map for 'Conservative1'
#conservative1LUT = GetColorTransferFunction('Conservative1')

# show data in view
#soln_volumevtkDisplay = Show(soln_volumevtk, renderView1)
# trace defaults for the display properties.
#soln_volumevtkDisplay.AmbientColor = [0.0, 0.0, 0.0]
#soln_volumevtkDisplay.ColorArrayName = ['POINTS', 'Conservative_1']
#soln_volumevtkDisplay.LookupTable = conservative1LUT
#soln_volumevtkDisplay.GlyphType = 'Arrow'
#soln_volumevtkDisplay.CubeAxesColor = [0.0, 0.0, 0.0]
#soln_volumevtkDisplay.ScalarOpacityUnitDistance = 1.6100342973236723
#soln_volumevtkDisplay.SetScaleArray = ['POINTS', 'Conservative_1']
#soln_volumevtkDisplay.ScaleTransferFunction = 'PiecewiseFunction'
#soln_volumevtkDisplay.OpacityArray = ['POINTS', 'Conservative_1']
#soln_volumevtkDisplay.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
#soln_volumevtkDisplay.ScaleTransferFunction.Points = [0.9001803994178772, 0.0, 0.5, 0.0, 3.3216006755828857, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
#soln_volumevtkDisplay.OpacityTransferFunction.Points = [0.9001803994178772, 0.0, 0.5, 0.0, 3.3216006755828857, 1.0, 0.5, 0.0]

# reset view to fit data
#renderView1.ResetCamera()

# show color bar/color legend
#soln_volumevtkDisplay.SetScalarBarVisibility(renderView1, True)

# get opacity transfer function/opacity map for 'Conservative1'
#conservative1PWF = GetOpacityTransferFunction('Conservative1')

# create a new 'Gradient Of Unstructured DataSet'
gradientOfUnstructuredDataSet1 = GradientOfUnstructuredDataSet(Input=soln_volumevtk)
#gradientOfUnstructuredDataSet1.ScalarArray = ['POINTS', sys.argv[2]]

# Properties modified on gradientOfUnstructuredDataSet1
gradientOfUnstructuredDataSet1.ScalarArray = ['POINTS', sys.argv[2]]
gradientOfUnstructuredDataSet1.ResultArrayName = sys.argv[2] + 'Gradient'

# show data in view
#gradientOfUnstructuredDataSet1Display = Show(gradientOfUnstructuredDataSet1, renderView1)
# trace defaults for the display properties.
#gradientOfUnstructuredDataSet1Display.AmbientColor = [0.0, 0.0, 0.0]
#gradientOfUnstructuredDataSet1Display.ColorArrayName = ['POINTS', sys.argv[2]]
#gradientOfUnstructuredDataSet1Display.LookupTable = conservative1LUT
#gradientOfUnstructuredDataSet1Display.GlyphType = 'Arrow'
#gradientOfUnstructuredDataSet1Display.CubeAxesColor = [0.0, 0.0, 0.0]
#gradientOfUnstructuredDataSet1Display.ScalarOpacityUnitDistance = 1.6100342973236723
#gradientOfUnstructuredDataSet1Display.SetScaleArray = ['POINTS', sys.argv[2]]
#gradientOfUnstructuredDataSet1Display.ScaleTransferFunction = 'PiecewiseFunction'
#gradientOfUnstructuredDataSet1Display.OpacityArray = ['POINTS', sys.argv[2]]
#gradientOfUnstructuredDataSet1Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
#gradientOfUnstructuredDataSet1Display.ScaleTransferFunction.Points = [0.9001803994178772, 0.0, 0.5, 0.0, 3.3216006755828857, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
#gradientOfUnstructuredDataSet1Display.OpacityTransferFunction.Points = [0.9001803994178772, 0.0, 0.5, 0.0, 3.3216006755828857, 1.0, 0.5, 0.0]

# hide data in view
#Hide(soln_volumevtk, renderView1)

# show color bar/color legend
#gradientOfUnstructuredDataSet1Display.SetScalarBarVisibility(renderView1, True)

# set scalar coloring
#ColorBy(gradientOfUnstructuredDataSet1Display, ('POINTS', sys.argv[2] + 'Gradient'))

# rescale color and/or opacity maps used to include current data range
#gradientOfUnstructuredDataSet1Display.RescaleTransferFunctionToDataRange(True)

# show color bar/color legend
#gradientOfUnstructuredDataSet1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for '...Gradient'
#machGradientLUT = GetColorTransferFunction(sys.argv[2] + 'Gradient')

# get opacity transfer function/opacity map for '...Gradient'
#machGradientPWF = GetOpacityTransferFunction(sys.argv[2] + 'Gradient')

# create a new 'Gradient Of Unstructured DataSet'
gradientOfUnstructuredDataSet2 = GradientOfUnstructuredDataSet(Input=gradientOfUnstructuredDataSet1)
#gradientOfUnstructuredDataSet2.ScalarArray = ['POINTS', sys.argv[2]]

# Properties modified on gradientOfUnstructuredDataSet2
gradientOfUnstructuredDataSet2.ScalarArray = ['POINTS', sys.argv[2] + 'Gradient']
gradientOfUnstructuredDataSet2.ResultArrayName = sys.argv[2] + 'Hessian'

# show data in view
#gradientOfUnstructuredDataSet2Display = Show(gradientOfUnstructuredDataSet2, renderView1)
# trace defaults for the display properties.
#gradientOfUnstructuredDataSet2Display.AmbientColor = [0.0, 0.0, 0.0]
#gradientOfUnstructuredDataSet2Display.ColorArrayName = ['POINTS', 'Conservative_1']
#gradientOfUnstructuredDataSet2Display.LookupTable = conservative1LUT
#gradientOfUnstructuredDataSet2Display.GlyphType = 'Arrow'
#gradientOfUnstructuredDataSet2Display.CubeAxesColor = [0.0, 0.0, 0.0]
#gradientOfUnstructuredDataSet2Display.ScalarOpacityUnitDistance = 1.6100342973236723
#gradientOfUnstructuredDataSet2Display.SetScaleArray = ['POINTS', 'Conservative_1']
#gradientOfUnstructuredDataSet2Display.ScaleTransferFunction = 'PiecewiseFunction'
#gradientOfUnstructuredDataSet2Display.OpacityArray = ['POINTS', 'Conservative_1']
#gradientOfUnstructuredDataSet2Display.OpacityTransferFunction = 'PiecewiseFunction'

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
#gradientOfUnstructuredDataSet2Display.ScaleTransferFunction.Points = [0.9001803994178772, 0.0, 0.5, 0.0, 3.3216006755828857, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
#gradientOfUnstructuredDataSet2Display.OpacityTransferFunction.Points = [0.9001803994178772, 0.0, 0.5, 0.0, 3.3216006755828857, 1.0, 0.5, 0.0]

# hide data in view
#Hide(gradientOfUnstructuredDataSet1, renderView1)

# show color bar/color legend
#gradientOfUnstructuredDataSet2Display.SetScalarBarVisibility(renderView1, True)

# set scalar coloring
#ColorBy(gradientOfUnstructuredDataSet2Display, ('POINTS', sys.argv[2] + 'Hessian'))

# rescale color and/or opacity maps used to include current data range
#gradientOfUnstructuredDataSet2Display.RescaleTransferFunctionToDataRange(True)

# show color bar/color legend
#gradientOfUnstructuredDataSet2Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for '...Hessian'
#machHessianLUT = GetColorTransferFunction(sys.argv[2] + 'Hessian')

# get opacity transfer function/opacity map for '....Hessian'
#machHessianPWF = GetOpacityTransferFunction(sys.argv[2] + 'Hessian')

# save data
SaveData(sys.argv[3] + sys.argv[2] + 'Hessian.csv', proxy=gradientOfUnstructuredDataSet2)
