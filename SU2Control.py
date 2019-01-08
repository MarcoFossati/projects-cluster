from subprocess import call
from HelperMethods import *
from pathlib import Path

TAG = "SU2Control: "
print(TAG + "Starting SU2 configuration...")

# TODO, get data from setup.
# TODO, monitor su2 output and detect failure.
folder = getProjectFolder()
# su2Path = "C:\Users\James\su2-windows-latest\ExecSequential\bin\SU2_CFD.exe"
su2Path = Path("C:/Users/James/su2-windows-latest/ExecSequential/bin/SU2_CFD.exe")
configPath = folder / "SU2-CONFIG.cfg"
complete = False

mach = getMach()
reynolds= getReynolds()
temp = getTemp()
cfl = getCFL()
setData(mach, reynolds, temp, cfl)
# start SU2 on given case.
call("{0} {1}".format(str(su2Path.resolve()), str(configPath.resolve())), shell=True)

if complete == True:
    print("Simulation complete.")
else:
    print("Simulation did not finish.")