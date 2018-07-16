# First argument: base name
# Second argument: method name

import sys
import shutil
#import winsound
import os

# --- Winsound ---

#frequency = 2500  # Set Frequency To 2500 Hertz
#duration = 1000  # Set Duration To 1000 ms == 1 second

# --- Functions ---
def createFoldersIfNonExisting(folders):
  for path in folders:
    try: 
      os.makedirs(path)
    except OSError:
      if not os.path.isdir(path):
        raise

def setupProjectFolder(essentialsFolder, geoName, baseName, globalPath): 
    cfgPath = globalPath + 'CFG/'
    geoPath = globalPath + 'GEO/'
    programPath = globalPath + 'Programs/'
    scriptPath = globalPath + 'Scripts/'

    shutil.copyfile(geoPath+'{0}.geo'.format(geoName),essentialsFolder+'{0}.geo'.format(geoName))
    shutil.copyfile(cfgPath+'{0}.cfg'.format(baseName),essentialsFolder+'{0}.cfg'.format(baseName))

    if os.path.exists(geoPath+'{0}_v0.geo'.format(geoName)):
      shutil.copyfile(geoPath+'{0}_v0.geo'.format(geoName),essentialsFolder+'{0}_v0.geo'.format(geoName))

    runScripts = ['computeGradient.py', 'emailPython.py', 'extractH.py', 'remeshing.py']  #, 'histogram.py'] #, 'convert_msh_su2.py']
    for f in runScripts:
        shutil.copyfile(scriptPath+'{0}'.format(f),essentialsFolder+'{0}'.format(f))

    #runPrograms = ['SU2_CFD.exe', 'SU2_SOL.exe', 'libiomp5md.dll', 'gmsh.exe']
    #for f in runPrograms:
    #    shutil.copyfile(programPath+'{0}'.format(f),essentialsFolder+'{0}'.format(f))


# --- Inputs ---
baseName = str(sys.argv[1]) #'RAE2822_Inv'
methodName = str(sys.argv[2]) #'gradientBased'
                    ## Working = RAE2822_Inv  - RAEInv
                    ##         = RAE2822_Vis  - RAEVis
                    ##         = 30N30P_Inv   - NPInv
                    ##         = 30N30P_Vis   - NPVis

if baseName == 'RAE2822_Inv':
    su2Run = 'RAEInv'
    geoName = 'RAE2822'
elif baseName == 'RAE2822_Vis':
    su2Run = 'RAEVis'
    geoName = 'RAE2822'
elif baseName == '30N30P_Inv':
    su2Run = 'NPInv'
    geoName = '30N30P'
elif baseName == '30N30P_Vis':
    su2Run = 'NPVis'
    geoName = '30N30P'
elif baseName == 'CYLINDER_Inv':
    su2Run = 'CYInv'
    geoName = 'CYLINDER'
elif baseName == 'CYLINDER_Vis':
    su2Run = 'CYVis'
    geoName = 'CYLINDER'
else: 
    print 'Incorrect base name. Please correct and try again. '

if methodName == 'gradientBased':
    methodFolderName = '_Grad'
elif methodName == 'hessianBased':
    methodFolderName='_Hess'
else: 
    print 'Incorrect method name. Please correct and try again.'

globalPath = os.getcwd() + '/'
projectPath = globalPath + 'Runs/'


# --- Setup Project Folder ---
projectFolderApp = 0
projectFolder = projectPath + baseName + methodFolderName+ '/'

while True:
  if os.path.exists(projectFolder):
    projectFolderApp = projectFolderApp + 1
    projectFolder = projectPath + baseName + methodFolderName + "_" + str(projectFolderApp) + '/'
  else:
    break

essentialsFolder = projectFolder + 'Essentials/'

createFoldersIfNonExisting([projectFolder,essentialsFolder])

setupProjectFolder(essentialsFolder, geoName, baseName, globalPath)

os.chdir(essentialsFolder)

os.system('python remeshing.py {0} {1} {2} {3}'.format(su2Run, projectFolder, projectFolderApp, methodName))
