# First argument: volume solution folder
# Second argument: field
# Third argument: version number
# Fourth argument: print folder

# Imports
import sys
import numpy as np
import vtk
from vtk.util import numpy_support
import os
import math
import winsound

frequency = 1250  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second

winsound.Beep(frequency, duration)

for arg in sys.argv:
    print(arg)

# Read flow
reader = vtk.vtkUnstructuredGridReader()
reader.SetFileName(str(sys.argv[1]))
reader.ReadAllScalarsOn()
reader.ReadAllVectorsOn()
reader.Update()

# Compute Flow
data = reader.GetOutput()
flow = numpy_support.vtk_to_numpy(data.GetPointData().GetAbstractArray(str(sys.argv[2])))

# Compute gradient
grad = vtk.vtkGradientFilter()
grad.SetInputConnection(reader.GetOutputPort())

grad.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, str(sys.argv[2]))
grad.SetResultArrayName(str(sys.argv[2]) + 'Gradient')
grad.Update()

Gradient = numpy_support.vtk_to_numpy(grad.GetOutput().GetPointData().GetAbstractArray(str(sys.argv[2]) + 'Gradient'))

# Compute hessian
hess = vtk.vtkGradientFilter()
hess.SetInputConnection(grad.GetOutputPort())

hess.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, str(sys.argv[2]) + 'Gradient')
hess.SetResultArrayName('Hessian')
hess.Update()

Hessian = numpy_support.vtk_to_numpy(hess.GetOutput().GetPointData().GetAbstractArray('Hessian'))

w = np.zeros((Hessian.shape[0],3),dtype=complex)
v = np.zeros((Hessian.shape[0],3,3),dtype=complex)
H = np.zeros((Hessian.shape[0],3,3),dtype=complex)

# Eigenvalues and Eigenvectors
for i in range(Hessian.shape[0]):
    H[i,:,:] = Hessian[i].reshape(3,3)
    w[i,:],v[i,:,:] = np.linalg.eig(H[i,:,:])
    w[i,:] = np.abs(w[i,:])
      
# equalize norm histogram [cut off] (log)
norm = (np.log(np.max(w,1))+1).real
nbox = np.ceil(np.max(norm))
histogram, bins = np.histogram(norm, nbox, normed=True)
cdf = histogram.cumsum()
cdf = (nbox-1) *cdf / cdf[-1]

equalized_norm = np.interp(norm, bins[:-1], cdf)
equalized_norm = np.exp(equalized_norm-1)

w = w / np.transpose(np.tile(norm,(3,1))) * np.transpose(np.tile(equalized_norm,(3,1)))

# Limit ratios / Set cell sizings << DEFORMATION
min_l = 1e-6
res_min_l = 1/min_l
max_l = 40
res_max_l = 1/max_l

for i in range(Hessian.shape[0]):
    for j in range(3):
      if(np.sqrt(w[i,j]).real < res_max_l):
        w[i,j] = pow(max_l,2)
        
      if(np.sqrt(w[i,j]).real > res_min_l):
        w[i,j] = pow(min_l,2)
             
M = np.zeros(Hessian.shape)
for i in range(Hessian.shape[0]):  
  if (np.abs(np.linalg.det(v[i,:,:])) > 1.e-6):
    M[i,:] = (v[i,:,:] * ( np.mat([[w[i,0], 0, 0],[0, w[i,1], 0],[0, 0, w[i,2]]]) * np.linalg.inv(v[i,:,:]))).real.flatten()
  else:
	print("Determinant too small")
	M[i,:] = np.mat([1/pow(max_l,2), 0, 0, 0, 1/pow(max_l,2), 0, 0, 0, 1/pow(max_l,2)]).real.flatten()

# Print flow .pos
flowpos = open('{2}{0}_v{1}.pos'.format(str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4])),"w")
flowpos.write('View "{0}"'.format(str(sys.argv[2])))
flowpos.write(' {\n')

cells = data.GetCells()
cells.InitTraversal()
a = vtk.vtkIdList()

while (cells.GetNextCell(a)):
  if (a.GetNumberOfIds()==3):
    flowpos.write("ST(")
    for i in range(a.GetNumberOfIds()):
      pts = data.GetPoint(a.GetId(i))
      for p in pts:
        flowpos.write(str(p)+" ,")
      flowpos.seek(-2, 1)
      flowpos.write("){") 
      for i in range(a.GetNumberOfIds()):
        tmp_data = flow[a.GetId(i)].real.flatten()
      for j in tmp_data:
        flowpos.write(str(j)  + " ,")
      flowpos.seek(-2, 1)
      flowpos.write("};\n")

  if (a.GetNumberOfIds()==4):
    flowpos.write("SQ(")
    for i in range(a.GetNumberOfIds()):
      pts = data.GetPoint(a.GetId(i))
      for p in pts:
        flowpos.write(str(p)+" ,")
      flowpos.seek(-2, 1)
      flowpos.write("){") 
      for i in range(a.GetNumberOfIds()):
        tmp_data = flow[a.GetId(i)].real.flatten()
      for j in tmp_data:
        flowpos.write(str(j)  + " ,")
      flowpos.seek(-2, 1)
      flowpos.write("};\n")

flowpos.write('};')
flowpos.close()

# Print hessian .pos
hesspos = open('{2}{0}Hessian_v{1}.pos'.format(str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4])),"w")
hesspos.write('View "{0}Hessian"'.format(str(sys.argv[2])))
hesspos.write(' {\n')

cells = data.GetCells()
cells.InitTraversal()
a = vtk.vtkIdList()

while (cells.GetNextCell(a)):
  if (a.GetNumberOfIds()==3):
    hesspos.write("TT(")
    for i in range(a.GetNumberOfIds()):
      pts = data.GetPoint(a.GetId(i))
      for p in pts:
        hesspos.write(str(p)+" ,")
    hesspos.seek(-2, 1)
    hesspos.write("){")
    c=0
    for i in range(a.GetNumberOfIds()):
      tmp_data = M[a.GetId(i)].real.flatten()
      for j in tmp_data:
        c=c+1
        if(c==9):
            c=0
            j='1.0'
        hesspos.write(str(j)  + " ,")
    hesspos.seek(-2, 1)
    hesspos.write("};\n")

  if (a.GetNumberOfIds()==4):
    hesspos.write("TQ(")
    for i in range(a.GetNumberOfIds()):
      pts = data.GetPoint(a.GetId(i))
      for p in pts:
        hesspos.write(str(p)+" ,")
    hesspos.seek(-2, 1)
    hesspos.write("){")
    c=0
    for i in range(a.GetNumberOfIds()):
      tmp_data = M[a.GetId(i)].real.flatten()
      for j in tmp_data:
        c=c+1
        if(c==9):
            c=0
            j='1.0'
        hesspos.write(str(j)  + " ,")
    hesspos.seek(-2, 1)
    hesspos.write("};\n")

hesspos.write('};')
hesspos.close()