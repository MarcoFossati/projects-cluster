from subprocess import call
from pathlib import Path

TAG = "Meshing: "
print("Running Meshing.py")
print("Running mesh script...")
# TODO, import data from configuration file.

folder = Path("C:/Users/James/Documents/Programs/Python3/UniversityProject/")
gmshPath = Path("C:/Users/James/gmsh-4.0.2-Windows64/gmsh.exe")
shapes = folder / "shapes.txt"
dimensions = "2"
outputFile = folder / "mesh.su2"


call("{0} {1} -{2} -o {3} -format su2".format(gmshPath, shapes, dimensions, outputFile), shell=True)
# call("{0} {1} -{2} -o {3}".format(gmshPath, shapes, dimensions, outputFile), shell=True)
# TODO, add checking stage
print("Meshing complete.")