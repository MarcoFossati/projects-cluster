from pathlib import Path
from subprocess import call
from GData import GPoint, GLine, GEllipse, Transform
from HelperMethods import getDrawShapesData
########################################################################################################################
# TODO, remove before final version. For test only.
import AllClear

TAG = "DrawShapes: "
print(TAG + "Running DrawShapes.py...")
print(TAG + "Beginning shape creation...")
# get data from project configuration.
# data imported as single string array.
# TODO, import data and set variables from it
inputData = getDrawShapesData()
for line in inputData:
    print(TAG + line)

# variables to draw the shapes, given by user.
shape = "ELLIPSE"  # TODO, handle circle
dimensions = [3, 0.5]  # x-diameter, y-diameter
aoa = 0
backShape = "RECT"
backDims = [5, 5]
folder = Path("C:/Users/James/Documents/Programs/Python3/UniversityProject/")
gmshPath = Path("C:/Users/James/gmsh-4.0.2-Windows64/gmsh.exe")
count = 1  # 1 is the lowest number Gmsh will accept.
alpha = 15  # angle of attack, defined in degrees and will clockwise rotation +ve.


########################################################################################################################
# non-memory manipulating methods for this script.
def getID():
    global count
    ID = count
    count = count + 1
    return ID


########################################################################################################################
# variables for script, defined in script.
# backPoints = None
writeString = []
########################################################################################################################
# # create background
# # can handle "RECT"
# if backShape == "RECT":
#     backPoints = [(0-backDims[0]/2), (0-backDims[1]/2),
#                   (0-backDims[0]/2),(0+backDims[1]/2),
#                   (0+backDims[0]/2),(0+backDims[1]/2),
#                   (0+backDims[0]/2),(0-backDims[1]/2)]
#     backLines = [(1),(2),
#                  (2),(3),
#                  (3),(4),
#                  (4),(1)]
#
# # draw background points
# counter = 1
# #length = backPoints.__len__()
# for i in range(0, backPoints.__len__(), 2): # will be 8 for RECT
#     writeString.append("Point ({0}) = {{{1},{2}, 0}};".format(counter, backPoints[i], backPoints[i+1]))
#     # print("Adding background point " + writeString[i])
#     counter = counter + 1
# for i in range(0, backLines.__len__(), 2): # will be 8 for RECT
#     writeString.append("Line ({0}) = {{ {1},{2} }};".format(counter, backLines[i], backLines[i+1]))
#     # print("Adding background point " + writeString[i])
#     counter = counter + 1
########################################################################################################################
# shape needs the points it's defined by and record of the number assigned to each point for Gmsh.
# Will use OOP approach.
# rectangular background needs 4 points.
p1 = GPoint()
p2 = GPoint()
p3 = GPoint()
p4 = GPoint()
# set their coordinates. There is no need to set the z-coordinate for 2D shapes.
p1.x = (0 - backDims[0] / 2)
p1.y = (0 - backDims[1] / 2)

p2.x = (0 - backDims[0] / 2)
p2.y = (0 + backDims[1] / 2)

p3.x = (0 + backDims[0] / 2)
p3.y = (0 + backDims[1] / 2)

p4.x = (0 + backDims[0] / 2)
p4.y = (0 - backDims[1] / 2)
# give each point a number according to the counter.
# assemble the background points into an array for easier counting.
backgroundPoints = [p1, p2, p3, p4]
# new method to assign IDs to the points.
for point in backgroundPoints:
    point.id = getID()
# create lines for shape outline.
l1 = GLine()
l2 = GLine()
l3 = GLine()
l4 = GLine()
# set the points contained in the lines from the background points.
# TODO, do this in loop using backgroundPoints array.
l1.p1 = p1
l1.p2 = p2

l2.p1 = p2
l2.p2 = p3

l3.p1 = p3
l3.p2 = p4

l4.p1 = p4
l4.p2 = p1
# assemble the lines into an array for easier counting.
backgroundLines = [l1, l2, l3, l4]
# give lines IDs.
for line in backgroundLines:
    line.id = getID()
# add the points to the writable string.
for point in backgroundPoints:
    writeString.append("Point ({0}) = {{ {1},{2}, {3} }};".format(point.id, point.x, point.y, point.z))
# add the linies to the writable string.
for line in backgroundLines:
    writeString.append("Line ({0}) = {{ {1},{2} }};".format(line.id, line.p1.id, line.p2.id))
########################################################################################################################
# # create shape for flow around
# frontPoints = None
# if shape == "ELLIPSE":
#     # centre, top, right, bottom, left
#     frontPoints = [(0),(0),
#                    (0),(dimensions[1]/2),
#                    (dimensions[0]/2),(0),
#                    (0),(-dimensions[1]/2),
#                    (-dimensions[0]/2),(0)]
#     frontLines = [(13),(9),(13),(10), # TL
#                   (10),(9),(10),(11), # TR
#                   (11),(9),(11),(12), # BR
#                   (12),(9),(12),(13),] # BL, start, centre, major ,end
#
# for i in range(0, frontPoints.__len__(), 2): # will be 8 for RECT
#     writeString.append("Point ({0}) = {{{1},{2}, 0}};".format(counter, frontPoints[i], frontPoints[i+1]))
#     counter = counter + 1
# for i in range(0, frontLines.__len__(), 4): # will be 8 for RECT
#     writeString.append("Ellipse ({0}) = {{ {1},{2},{3},{4} }};".format(counter, frontLines[i], frontLines[i+1], frontLines[i+2], frontLines[i+3]))
#     counter = counter + 1
########################################################################################################################
# create shape for flow around using OOP approach.
# elliptical shape needs 5 points: centre, top, right, bottom, left.
pf1 = GPoint()  # centre
pf2 = GPoint()  # top
pf3 = GPoint()  # right
pf4 = GPoint()  # bottom
pf5 = GPoint()  # left
# set the coordinates of the points.
pf1.x = 0
pf1.y = 0

pf2.x = 0
pf2.y = (dimensions[1] / 2)

pf3.x = (dimensions[0] / 2)
pf3.y = 0

pf4.x = 0
pf4.y = (-dimensions[1] / 2)

pf5.x = (-dimensions[0] / 2)
pf5.y = 0
# assemble the points into array for counting.
foregroundPoints = [pf1, pf2, pf3, pf4, pf5]
# give the points IDs.
for point in foregroundPoints:
    point.id = getID()
########################################################################################################################
transform = Transform()
# set the angle of attack, got from input data file.
transform.alpha = alpha
# transform the points by given angle.
foregroundPoints = transform.rotate(foregroundPoints)
########################################################################################################################
# create the ellipses
# 4 ellipses are needed to define the shape.
e1 = GEllipse()  # TL
e2 = GEllipse()  # TR
e3 = GEllipse()  # BR
e4 = GEllipse()  # BL
# set the points that each ellipse needs.
# needed for definition: start, centre, major ,end
# order of points created: centre 1, top 2, right 3, bottom 4, left 5.
e1.p1 = pf5
e1.p2 = pf1
e1.p3 = pf3
e1.p4 = pf2

e2.p1 = pf2
e2.p2 = pf1
e2.p3 = pf4
e2.p4 = pf3

e3.p1 = pf3
e3.p2 = pf1
e3.p3 = pf5
e3.p4 = pf4

e4.p1 = pf4
e4.p2 = pf1
e4.p3 = pf2
e4.p4 = pf5
# assemble the ellipses into an array for counting.
foregroundLines = [e1, e2, e3, e4]
# give curves IDs.
for line in foregroundLines:
    line.id = getID()
# add the points to the writable string.
for point in foregroundPoints:
    writeString.append("Point ({0}) = {{ {1},{2}, {3} }};".format(point.id, point.x, point.y, point.z))
# add the lines to the writable string.
for line in foregroundLines:
    writeString.append(
        "Ellipse ({0}) = {{ {1},{2},{3},{4} }};".format(line.id, line.p1.id, line.p2.id, line.p3.id, line.p4.id))
########################################################################################################################
# # create loops.
# if shape == "ELLIPSE" and backShape == "RECT":
#     writeString.append("Line Loop({0}) = {{ 5,6,7,8 }};".format(counter))
#     counter = counter + 1
#     writeString.append("Curve Loop({0}) = {{ 14,15,16,17 }};".format(counter))
########################################################################################################################
# create the loops to connect the lines.
writeString.append("Line Loop({0}) = {{ {1},{2},{3},{4} }};".format(getID(), backgroundLines[0].id, backgroundLines[1].id,
                                                                    backgroundLines[2].id, backgroundLines[3].id))
outerID = count - 1

writeString.append(
    "Curve Loop({0}) = {{ {1},{2},{3},{4} }};".format(getID(), foregroundLines[0].id, foregroundLines[1].id,
                                                      foregroundLines[2].id, foregroundLines[3].id))
innerID = count - 1
########################################################################################################################
# TODO, create surfaces so that SU2 can detect edges.
# define surfaces.
# define plane surface of interior.
writeString.append("Plane Surface({0})={{ {1},{2} }};".format(getID(), innerID, outerID))
# count = count + 1
# writeString.append("Physical Curve(""inlet"")={{ {0} }};".format(backgroundLines[0].id))
# writeString.append("Physical Curve(""outlet"")={{ {0} }};".format(backgroundLines[2].id))
# writeString.append("Physical Curve(""upper_wall"")={{ {0} }};".format(backgroundLines[1].id))
# writeString.append("Physical Curve(""lower_wall"")={{ {0} }};".format(backgroundLines[3].id))
# writeString.append("Physical Curve(""airfoil"")={{ {0} }};".format(innerID))
# Physical Curve("inlet")={1}; //inlet
# Physical Curve("outlet")={2};
# Physical Curve("upper_wall")={3};
# Physical Curve("lower_wall")={4};
# Physical Curve("airfoil")={10}; //internal
########################################################################################################################
# write the data to text file for Gmsh.
print(TAG + "Creating shapes file...")
file = folder / "shapes.txt"
print(TAG + "Writing shapes to file...")

with file.open(mode='a') as f:
    for i in range(0, writeString.__len__()):
        f.write(writeString[i] + "\n")
        print("Writing " + writeString[i])

print(TAG + "Shapes file done writing.")
print(TAG + "Shape creation done.")
########################################################################################################################
# run Gmsh with the text file so that it can be re-saved in the appropriate format.
# print("Converting data to .geo file...")
# # print(gmshPath.resolve())
# outputName = folder / "shapes.geo"
# call("{0} -open {1} -a".format(gmshPath.resolve(), file), shell=True)
# print("Saving .geo file to " + str(outputName))
# call("{0} -save -o {1}".format(gmshPath.resolve(), outputName), shell=True)
userIn = input(TAG + "Open shapes.txt in Gmsh? y/n : ")
if userIn == "y":
    print(TAG + "Opening Gmsh...")
    call("{0} -open {1} -a".format(gmshPath.resolve(), file), shell=True)
print(TAG + "Shape creation complete.")
