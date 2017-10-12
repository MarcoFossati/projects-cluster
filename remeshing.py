#!/usr/bin/env python

# --- Modules ---
import sys, shutil
import os, os.path

import numpy as np
import math
import csv

import threading
import logging
import time


# --- Global variables ---

# - Global user inputs
HPCrun = False
multiThreading = True
remeshOnly = False

if HPCrun:
  gmsh3Cmd='/users/xrb14110/Downloads/gmsh-3.0.4-Linux/bin/gmsh'
  paraviewVersion = 4
else:
  gmsh3Cmd='/home/vincent/Downloads/gmsh-3.0.4-Linux/bin/gmsh'
  paraviewVersion = 5
  

# - Global paths
projectPath = os.getcwd() + '/'

# - Others
maxCharNoLogging = 20 
logging.basicConfig(level=logging.INFO, format=' (%(threadName)-{0}s) %(message)s'.format(str(maxCharNoLogging)))


# --- Functions ---
def createFoldersIfNonExisting(folders):
  for path in folders:
    try: 
      os.makedirs(path)
    except OSError:
      if not os.path.isdir(path):
        raise


def meshCase(Obj, noIter):
  if multiThreading: 
    threads = []
    
    threads.append(threading.Thread(name='Thread_gmshTomsh', target=os.system, args=(gmsh3Cmd + ' {0}_v{1}.geo -{2} -o {3}.msh > log.mshmesh 2>&1'.format(Obj.meshes[noIter].geoFile, str(noIter), str(Obj.caseScenario.noDimensions), Obj.meshes[noIter].geoFile + '_v' + str(noIter)),)))
    threads.append(threading.Thread(name='Thread_gmshTosu2', target=os.system, args=(gmsh3Cmd + ' {0}_v{1}.geo -{2} -o {3}.su2 > log.su2mesh 2>&1'.format(Obj.meshes[noIter].geoFile, str(noIter), str(Obj.caseScenario.noDimensions), Obj.meshes[noIter].geoFile + '_v' + str(noIter)),)))
      
    try:
      for thread in threads:
        thread.start()
      for thread in threads:  
        thread.join()
    except:
      print "{0}ERROR MULTI-THREADING!{1}".format(Bcolors.FAIL, Bcolors.ENDC)
      
  else:
    os.system(gmsh3Cmd + ' {0}_v{1}.geo -{2} -o {3}.msh > log.mshmesh 2>&1'.format(Obj.meshes[noIter].geoFile, str(noIter), str(Obj.caseScenario.noDimensions), Obj.meshes[noIter].geoFile + '_v' + str(noIter)))
    os.system(gmsh3Cmd + ' {0}_v{1}.geo -{2} -o {3}.su2 > log.su2mesh 2>&1'.format(Obj.meshes[noIter].geoFile, str(noIter), str(Obj.caseScenario.noDimensions), Obj.meshes[noIter].geoFile + '_v' + str(noIter)))


def runSU2Computation(Obj):
  if HPCrun:
    os.system('mpirun -np {0} --oversubscribe ./SU2_CFD {1}.cfg > {2}.log'.format(str(Obj.noCPUs), Obj.configurationFile, su2.baseName))
  else:  
    os.system('mpirun -np {0} ./SU2_CFD {1}.cfg > {2}.log'.format(str(Obj.noCPUs), Obj.configurationFile, Obj.baseName))
    
    
def generateSU2Solution(Obj):
  if HPCrun:
    os.system('mpirun -np {0} --oversubscribe ./SU2_SOL {1}.cfg > /dev/null 2>&1'.format(str(Obj.noCPUs), Obj.configurationFile))
  else:
    os.system('mpirun -np {0} ./SU2_SOL {1}.cfg > /dev/null 2>&1'.format(str(Obj.noCPUs), Obj.configurationFile))  


def setupRunFolder(Obj, noIter, baseDir, curRunDir):
  # - Symbolic link to the current mesh
  os.system('ln -s {0}_v{1}.su2 {2}.su2'.format(Obj.meshes[noIter].geoFile, str(noIter), Obj.meshes[noIter].geoFile.rsplit('/', 1)[1]))
  
  # - Symbolic links to SU2 essentials
  su2Essentials = [Obj.configurationFile + '.cfg', 'convergence.gnu', 'SU2_CFD', 'SU2_SOL']
  for f in su2Essentials:
    os.system('ln -s {0}{1} {1}'.format(baseDir, f))
    

def mag(x): 
  return math.sqrt(sum(i**2 for i in x))
  
  
def ave(x):
  return sum(x)/float(len(x))   
    
    
def addNodeDataIntoMsh(viewTag, fieldNodeData):
  """$NodeData
1                      one string tag:
"A scalar view"          the name of the view ("A scalar view")
1                      one real tag:
0.0                      the time value (0.0)
3                      three integer tags:
0                        the time step (0; time steps always start at 0)
1                        1-component (scalar) field
6                        six associated nodal values
1 0.0                  value associated with node #1 (0.0)
2 0.1                  value associated with node #2 (0.1)
3 0.2                  etc.
4 0.0
5 0.2
6 0.4
$EndNodeData
""" # Example
  
  nodeDataStr = """$NodeData
1
"{0}"
1
0.0
3
0
1
{1}
{2}
$EndNodeData
""".format(viewTag, len(fieldNodeData), '\n'.join(str(i+1) + '\t' + str(j) for i, j in enumerate(fieldNodeData)))
  return nodeDataStr


def callAMRTechnique(solutionPath, printPath, Obj, meshIte, meshesFolder, currentFieldIndex):

  cFI = currentFieldIndex
  
  globals()[str(Obj.remeshingTechnique.methodName) + "Paraview"](Obj.remeshingTechnique, solutionPath, printPath)  
    
  cFI = globals()[str(Obj.remeshingTechnique.methodName) + "AMR"](Obj.meshes[meshIte], Obj.meshes[meshIte+1], Obj.remeshingTechnique, meshIte, solutionPath, meshesFolder, currentFieldIndex)
  
  return cFI


def gradientBasedParaview(remeshingInfo, solutionPath, printPath):
  # - Run paraview
  if paraviewVersion == 5:
    for fieldName in remeshingInfo.gradientQuantities:
      os.system('pvpython computeGradient.py {0}soln_volume.vtk {1} {2}'.format(solutionPath, fieldName, printPath))
    for fieldName in np.setdiff1d(remeshingInfo.flowQuantities, remeshingInfo.gradientQuantities):
      os.system('pvpython computeGradient.py {0}soln_volume.vtk {1} {2}'.format(solutionPath, fieldName, printPath))  
  else:
    for fieldName in remeshingInfo.gradientQuantities:
      os.system('pvpython computeGradient_4.1.py {0}soln_volume.vtk {1} {2}'.format(solutionPath, fieldName, printPath))
    for fieldName in np.setdiff1d(remeshingInfo.flowQuantities, remeshingInfo.gradientQuantities):
      os.system('pvpython computeGradient_4.1.py {0}soln_volume.vtk {1} {2}'.format(solutionPath, fieldName, printPath))


def gradientBasedAMR(meshInfo, nextMeshInfo, remeshingInfo, meshIte, solutionPath, meshesFolder, currentFieldIndex):  
  # - Read relevant fields
  os.chdir(solutionPath)
    
  # GRADIENT FIELDS
  gradFields = []
  for f, fieldName in enumerate(remeshingInfo.gradientQuantities):
    gradFields.append([])    
  
    firstDataCol = 0
    with open(fieldName + 'Gradient.csv', 'rb') as csvfile:
      nodeDataReader = csv.reader(csvfile, delimiter=',')
      row1 = next(nodeDataReader)
      for colCnt, c in enumerate(row1):
        if fieldName + 'Gradient:0' in c:
          firstDataCol = colCnt
          break
          
    with open(fieldName + 'Gradient.csv', 'rb') as csvfile:
      nodeDataReader = csv.reader(csvfile, delimiter=',')
      next(nodeDataReader)
      for row in nodeDataReader:
        gradFields[f].append(mag([float(c) for c in row[firstDataCol:firstDataCol+3]])) # magnitude of the gradient
        
  
  # FLOW FIELDS
  fields = []
  for f, fieldName in enumerate(remeshingInfo.flowQuantities):
    fields.append([])    
  
    firstDataCol = 0
    with open(fieldName + 'Gradient.csv', 'rb') as csvfile: # 'Gradient' left deliberately
      nodeDataReader = csv.reader(csvfile, delimiter=',')
      row1 = next(nodeDataReader)
      for colCnt, c in enumerate(row1):
        if fieldName == c:
          firstDataCol = colCnt
          break
          
    with open(fieldName + 'Gradient.csv', 'rb') as csvfile: # 'Gradient' left deliberately
      nodeDataReader = csv.reader(csvfile, delimiter=',')
      next(nodeDataReader)
      for row in nodeDataReader:
        fields[f].append(float(row[firstDataCol])) # flow quantity 
    
  
  # - Edit .msh
  with open(meshInfo.geoFile + '_v{0}.msh'.format(str(meshIte)), 'a') as f:
    for i, field in enumerate(gradFields):
      f.write \
      (
        addNodeDataIntoMsh(remeshingInfo.gradientQuantities[i] + 'Gradient', field)
      )
    
    for i, field in enumerate(fields):
      f.write \
      (
        addNodeDataIntoMsh(remeshingInfo.flowQuantities[i], field)
      )  
  
  
  # - Create a temporary version of the next .geo
  with open(nextMeshInfo.geoFile + '_v{0}.geo'.format(str(meshIte + 1)), 'w') as f:
    f.write \
    ("""
Merge "{0}_v{1}.geo";
Merge "{0}_v{1}.msh";
""".format(nextMeshInfo.geoFile, str(meshIte))
    )
  
    for i in range(len(gradFields)):
      f.write \
      ("""
Save View[{0}] '{1}{2}Gradient_v{3}.pos';
""".format(str(meshIte*(len(gradFields)+len(fields)) + i), meshesFolder, remeshingInfo.gradientQuantities[i], str(meshIte))
      )
      
    for i in range(len(fields)):
      f.write \
      ("""
Save View[{0}] '{1}{2}_v{3}.pos';
""".format(str(meshIte*(len(gradFields)+len(fields)) + len(gradFields) + i), meshesFolder, remeshingInfo.flowQuantities[i], str(meshIte))
      )  
  
  
  # - Remesh for points -
  os.chdir(meshesFolder)
  os.system(gmsh3Cmd + ' {0}_v{1}.geo -0  > log.ptmesh 2>&1'.format(nextMeshInfo.geoFile, meshIte + 1))
  
  
  # - Create the next .geo
  with open(nextMeshInfo.geoFile + '_v{0}.geo'.format(str(meshIte + 1)), 'w') as f:
    f.write \
    ("""
Merge "{0}_v{1}.geo";
""".format(nextMeshInfo.geoFile, str(meshIte))
    )
    
    for i in range(len(gradFields)):
      f.write \
      ("""
Merge "{0}{1}Gradient_v{2}.pos";
""".format(meshesFolder, remeshingInfo.gradientQuantities[i], str(meshIte))
      )
      
    for i in range(len(fields)):
      f.write \
      ("""
Merge "{0}{1}_v{2}.pos";
""".format(meshesFolder, remeshingInfo.flowQuantities[i], str(meshIte))
      )  
    
    f.write \
    ("""
Mesh.CharacteristicLengthMin = {0};
Mesh.CharacteristicLengthMax = {1};
""".format(nextMeshInfo.minMeshSize, nextMeshInfo.maxMeshSize)
    )
    
    for i in range(len(gradFields)):
      f.write \
      ("""
Field[{0}] = PostView;
Field[{0}].IView = {1};
Field[{0}].CropNegativeValues = 0;
""".format(currentFieldIndex + i + 1, meshIte*(len(gradFields)+len(fields)) + i)
      )
      
    for i in range(len(fields)):
      f.write \
      ("""
Field[{0}] = PostView;
Field[{0}].IView = {1};
Field[{0}].CropNegativeValues = 0;
""".format(currentFieldIndex + len(gradFields) + i + 1, meshIte*(len(gradFields)+len(fields)) + len(gradFields) + i)
      )  
    
    lastFieldIndex = currentFieldIndex + len(gradFields) + len(fields)
    
    listOfFields = []
    if currentFieldIndex != 0 and meshIte > 1: # no history for the first & second generations
      # insert history of the previous iteration only
      # NB: currentFieldIndex is the previous background field
      listOfFields.append(currentFieldIndex)
      
      # no history
      #pass
      
    for i in range(len(gradFields)):
      
      listOfFields.append(lastFieldIndex + i + 1)
      
      # Field[gradQ] = lchar1                        / (|gradQ| / max(|gradQ|)) 
      #              = (lc1 / meshIter*gradSmoother) * max(|gradQ|) / |gradQ|
      #              = (lc1 / meshIter*gradSmoother) * max(|gradQ|) / (|gradQ| + 1e-9)
      f.write \
      ("""
Field[{0}] = MathEval;
Field[{0}].F = "{1}*{3}/(F{2}+1e-9)";
""".format(str(lastFieldIndex + i + 1), str(nextMeshInfo.lchar1), str(currentFieldIndex + i + 1), str(max(gradFields[i])))
      )
      
    for i in range(len(fields)):
      
      listOfFields.append(lastFieldIndex + len(gradFields) + i + 1)
      
      # Field[Q] = lchar2                        / (|Qinf-Q| / max(|Qinf-Q|))^2 
      #          = (lc2 / meshIter*flowSmoother) * (max(|Qinf-Q|) / |Qinf-Q|)^2
      #          = (lc2 / meshIter*flowSmoother) * (max(|Qinf-Q|) / (|Qinf-Q| + 1e-9)^2
      f.write \
      ("""
Field[{0}] = MathEval;
Field[{0}].F = "{1}*({3}/(Fabs({4}-F{2})+0.0001*{4}))^2";
""".format(str(lastFieldIndex + len(gradFields) + i + 1), str(nextMeshInfo.lchar2), str(currentFieldIndex + len(gradFields) + i + 1), str(max([abs(remeshingInfo.flowQuantitiesFreestreamValue[i]-Qlocal) for Qlocal in fields[i]])), str(remeshingInfo.flowQuantitiesFreestreamValue[i]))
      )  
      
    lastFieldIndex += len(gradFields) + len(fields)
    
    f.write \
    ("""
Field[{0}] = Min;
Field[{0}].FieldsList = {{{1}}};
Background Field = {0};
""".format(str(lastFieldIndex + 1), ', '.join(str(lOF) for lOF in listOfFields))
    )
    
    lastFieldIndex += 1
    
  currentFieldIndex = lastFieldIndex
  
  return currentFieldIndex
      
  
def firstGenAMRTechnique(Obj, meshIter, lc):
  Obj.meshes[meshIter] = globals()['firstGen_' + Obj.remeshingTechnique.methodName](Obj, meshIter, lc)
  return Obj.meshes[meshIter]
  

def firstGen_gradientBased(Obj, meshIter, lc):
  Obj.meshes[meshIter].lchar1 = lc[0]/Obj.remeshingTechnique.gradientSmoother
  Obj.meshes[meshIter].lchar2 = lc[1]/Obj.remeshingTechnique.flowSmoother
  return Obj.meshes[meshIter]


def nextGenAMRTechnique(Obj, meshIter, lc):
  Obj.meshes[meshIter] = globals()['nextGen_' + Obj.remeshingTechnique.methodName](Obj, meshIter, lc)
  return Obj.meshes[meshIter]
  

def nextGen_gradientBased(Obj, meshIter, lc):
  Obj.meshes[meshIter].lchar1 = lc[0]/(Obj.remeshingTechnique.gradientSmoother*(meshIter+1))
  Obj.meshes[meshIter].lchar2 = lc[1]/(Obj.remeshingTechnique.flowSmoother*(meshIter+1))
  return Obj.meshes[meshIter]


# --- Classes ---

# Class allowing the use of colors in print statements
class Bcolors:
    HEADER = '\033[0;94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        
        
class SU2_setup:
    """A SU2 Simulation is seen as a SU2_setup object"""
    
    def __init__(self, baseName, configurationFile, caseScenario, meshes, remeshingTechnique, firstGeneration=0, noCPUs=1):
      
      # Name of the working folder
      self.baseName = baseName
      
      # Name of the configuration file
      self.configurationFile = configurationFile
      
      # Definition of the case scenario (in terms of physical parameters)
      self.caseScenario = caseScenario
      
      # Meshes used for each generation
      self.meshes = []
      self.meshes.append(meshes)
      
      # Remeshing technique to be employed
      self.remeshingTechnique = remeshingTechnique
      
      self.remeshingTechnique.checkRemeshingMethodArguments(self.caseScenario.noDimensions)
      
      # Index of the first mesh generation to be run (default = 0)
      self.firstGeneration = firstGeneration
      
      # Number of CPUs to be used for the job (default = 1 :: serial)
      self.noCPUs = noCPUs
      
    
    # Add full path info to mesh data (.geo and dependencies)
    def addFullPathToMeshData(self, meshesFolder):
      self.meshes[0].geoFile = meshesFolder + self.meshes[0].geoFile
      self.meshes[0].dependencyFiles = [meshesFolder + dpf for dpf in self.meshes[0].dependencyFiles]
    
    # Returns the last Field entry in the original .geo file  
    def findLastFieldEntryInGeo(self):
      
      lastFieldLine = -1
      with open(self.meshes[self.firstGeneration].geoFile + '_v' + str(self.firstGeneration) + '.geo', 'r') as f:     
        noL = -1
        for line in f:
          noL += 1
          if "Field[" in line:
            lastFieldLine = noL
        
      with open(self.meshes[self.firstGeneration].geoFile + '_v' + str(self.firstGeneration) + '.geo', 'r') as f:  
        noL = -1
        if lastFieldLine != -1:  
          for line in f: 
            noL += 1 
            if noL == lastFieldLine:
              return int(line.lstrip("Field[").split("]", 1)[0])
              break
      
      return 0
                
      
 
class CaseScenario:
    """A SU2 CaseScenario giving physics info about the run"""
    
    def __init__(self, freestreamMach, characteristicLength=1, noDimensions=3):
      
      # Free-stream Mach number
      self.freestreamMach = freestreamMach
      
      # Characteristic length of the body (default = 1 m)
      self.characteristicLength = characteristicLength
      
      # Number of spatial dimensions of the case scenario (default = 3D)
      self.noDimensions = noDimensions   


class GmshMesh:
    """A Gmsh Mesh"""
    
    def __init__(self, geoFile, dependencyFiles=[], minMeshSize=0, maxMeshSize=1e6, lchar1=None, lchar2=None):
      
      # Name of the .geo file
      self.geoFile = geoFile
      
      # Name of the dependency files (if any)
      self.dependencyFiles = []
      self.dependencyFiles.extend(dependencyFiles)
      
      # Minimum size allowed for a mesh element (default = unbounded)
      self.minMeshSize = minMeshSize
      
      # Maximum size allowed for a mesh element (default = unbounded)
      self.maxMeshSize = maxMeshSize
      
      # First characteristic length of a mesh (default = undefined)
      self.lchar1 = lchar1
      
      # Second characteristic length of a mesh (default = undefined)
      self.lchar2 = lchar2
      

class Remeshing:
    """A remeshing technique"""
    
    def __init__(self, methodName, noGenerations=1, gradientSmoother=None, flowSmoother=None, gradientQuantities=None, flowQuantities=None, flowQuantitiesFreestreamValue=None):
      
      # Name of the remeshing method to be utilized
      self.methodName = methodName
      self.checkMethodName()
      
      # Number of generations to perform (default = 1)
      # This number is absolute, defined regarless of the firstGeneration input
      self.noGenerations = noGenerations
      
      # --- Parameters for the gradient based remeshing technique ---
      # Physical quantities involved in gradients calculation (default = undefined)
      self.gradientQuantities = gradientQuantities
      
      # Gradient smoother constant (default = undefined)
      # Proposed values - 2D: 5, 3D: 2.5
      self.gradientSmoother = gradientSmoother
      
      # Physical quantities involved in flow properties calculation
      self.flowQuantities = flowQuantities
      
      # Flow smoother constant (default = undefined)
      # Proposed values - 2D: 1, 3D: 2
      self.flowSmoother = flowSmoother
      
      # Free-stream value for these quantities
      self.flowQuantitiesFreestreamValue = flowQuantitiesFreestreamValue
      
      
    # Checks that the method name is correct
    def checkMethodName(self):
      methodNames = ['gradientBased']
      if self.methodName not in methodNames:
        print '\n{0}{1} is not a valid remeshing method name{2}'.format(Bcolors.FAIL, self.methodName, Bcolors.ENDC)
        print 'Valid entries are: {0}'.format(', '.join([mthd for mthd in methodNames]))
        exit()
        
    # Checks the validity of the arguments given to the remeshing technique
    def checkRemeshingMethodArguments(self, caseDimension):
      if self.methodName == 'gradientBased':
        self.checkGradientBasedRemeshingArguments(caseDimension)
    
    # Checks the validity of the arguments given to the gradient-based remeshing technique
    def checkGradientBasedRemeshingArguments(self, caseDimension):
      
      if self.gradientQuantities is None and self.flowQuantities is None:
        self.gradientQuantities = ['Mach']
        self.flowQuantities = []
        if caseDimension == 2:
          self.gradientSmoother = 5.0
          self.flowSmoother = 1.0
        else:
          self.gradientSmoother = 2.5
          self.flowSmoother = 2.0  
      
      if self.gradientQuantities is None:
        self.gradientSmoother = 1.0
        self.gradientQuantities = []
      else:  
        if self.gradientSmoother is None:
          if caseDimension == 2:
            self.gradientSmoother = 5.0
          else:
            self.gradientSmoother = 2.5
            
      if self.flowQuantities is None:
        self.flowQuantities = []
        self.flowSmoother = 1.0 
      else:  
        if self.flowSmoother is None:
          if caseDimension == 2:
            self.flowSmoother = 1.0 
          else:
            self.flowSmoother = 2.0
            
      self.checkFlowQuantitiesFreestreamValue()      
                     
          
    # Check the validity of the free-stream values for given flow quantities
    def checkFlowQuantitiesFreestreamValue(self):
      if len(self.flowQuantities) == 0 and self.flowQuantitiesFreestreamValue is None:
        self.flowQuantitiesFreestreamValue = []
      
      if len(self.flowQuantities) != 0:
        if self.flowQuantitiesFreestreamValue is None:
          print '\n{0}flowQuantitiesFreestreamValue List is missing{1}'.format(Bcolors.FAIL, Bcolors.ENDC)
          exit()
        elif len(self.flowQuantitiesFreestreamValue) != len(self.flowQuantities):
          print '\n{0}flowQuantitiesFreestreamValue and flowQuantities Lists are not of the same size{1}'.format(Bcolors.FAIL, Bcolors.ENDC)
          exit()  
        

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

# ----------------------------- Input parameters ---------------------------- #

fsplUK = SU2_setup \
(
    baseName = 'M1.1-Ap075-H10',
    configurationFile = 'fsplUK',
    firstGeneration = 0,
    noCPUs = 120,
    caseScenario = CaseScenario \
    (
        noDimensions = 3,
        freestreamMach = 1.1,
        characteristicLength = 6.6169
    ),
    meshes = GmshMesh \
    (
      geoFile = 'postAnsys-Ap075',
      dependencyFiles = ['fsplUK-3B3-75deg.stl'],
      minMeshSize = 1.0e-4,
      maxMeshSize = 10
    ), 
    remeshingTechnique = Remeshing \
    (
        methodName = 'gradientBased',
        noGenerations = 1,
        gradientSmoother = 2.5,
        gradientQuantities = ['Mach', 'Pressure'],
        flowSmoother = 1,
        flowQuantities = ['Mach'],
        flowQuantitiesFreestreamValue = [0.775]
    )
)

# +++++++++++++++

rae = SU2_setup \
(
    baseName = 'rae2822',
    configurationFile = 'RAE2822',
    firstGeneration = 0,
    noCPUs = 4,
    caseScenario = CaseScenario \
    (
        noDimensions = 2,
        freestreamMach = 0.775,
        characteristicLength = 1.0
    ),
    meshes = GmshMesh \
    ( 
        geoFile = 'RAE2822',
        minMeshSize = 1.0e-6,
        maxMeshSize = 40
    ),
    remeshingTechnique = Remeshing \
    (
        methodName = 'gradientBased',
        noGenerations = 4,
        gradientSmoother = 5,
        gradientQuantities = ['Mach', 'Pressure']
    )
)


# +++++++++++++++

# - List of SU2 simulations to run
su2Runs = []

su2Runs.append(rae)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

### ----- BEGIN SU2RUNS LOOP ----- ####
for su2 in su2Runs:

    print "{0}{1} SU2 Simulation{2} ({3})".format(Bcolors.HEADER, su2.baseName, Bcolors.ENDC, time.strftime('%H:%M:%S, %D', time.localtime(time.time())))
    
    # --- Initialisation ---
    baseFolder = projectPath + su2.baseName + '/'

    meshesFolder = baseFolder + 'meshes/'
    runsFolder = baseFolder + 'runs/'
    paraviewFolder = baseFolder + 'paraview/'

    createFoldersIfNonExisting([meshesFolder, runsFolder, paraviewFolder])

    # - Characteristic lengths of the problem
    if su2.caseScenario.noDimensions == 2:
      lc1 = su2.caseScenario.characteristicLength/100
      lc2 = 5e3*lc1
    else:
      lc1 = su2.caseScenario.characteristicLength/50
      lc2 = 1e4*lc1

    # - Mesh info
    su2.addFullPathToMeshData(meshesFolder)
    su2.meshes[0] = firstGenAMRTechnique(su2, 0, [lc1, lc2])

    if su2.firstGeneration == 0:
      shutil.copyfile(su2.meshes[0].geoFile + '.geo', su2.meshes[0].geoFile + '_v0.geo')

    for m in xrange(su2.firstGeneration):
      su2.meshes.append(su2.meshes[-1])
      su2.meshes[m] = nextGenAMRTechnique(su2, m+1, [lc1, lc2])

    # - Determine the last Field number (if any) in the original geo file
    currentFieldIndex = su2.findLastFieldEntryInGeo()


    ### ----- LOOP ----- ####
    for meshIter in xrange(su2.firstGeneration, su2.remeshingTechnique.noGenerations):

        print "{0} Generation {1}{2} ({3})".format(Bcolors.OKGREEN, str(meshIter), Bcolors.ENDC, time.strftime('%H:%M:%S, %D', time.localtime(time.time())))
        
        # --- Meshing ---
        os.chdir(meshesFolder)
        if not remeshOnly:
          meshCase(su2, meshIter)


        # --- Set-up next run folder ---
        createFoldersIfNonExisting([runsFolder + 'run' + str(meshIter)])

        currentRunDir = runsFolder + 'run' + str(meshIter) + '/'
        os.chdir(currentRunDir)
        
        if not remeshOnly:
          setupRunFolder(su2, meshIter, baseFolder, currentRunDir)

          # - SU2 computation
          runSU2Computation(su2)
            
          # - Generate SU2 solution
          generateSU2Solution(su2)


        # --- Update for next generation ---
        su2.meshes.append(su2.meshes[-1])
        su2.meshes[meshIter+1] = nextGenAMRTechnique(su2, meshIter+1, [lc1, lc2])
        
        
        # --- Paraview and AMR technique ---
        os.chdir(paraviewFolder)
        
        currentFieldIndex = callAMRTechnique(currentRunDir, currentRunDir, su2, meshIter, meshesFolder, currentFieldIndex)
        
    ### ----- END LOOP ----- ####

### ----- END SU2RUNS LOOP ----- ####

print "{0}Exiting remeshing.py{1} ({2})\n".format(Bcolors.HEADER, Bcolors.ENDC, time.strftime('%H:%M:%S, %D', time.localtime(time.time())))
 

