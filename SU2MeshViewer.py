from tkinter import Tk, Canvas, Frame, BOTH
import tkinter
from HelperMethods import getSU2MeshPoints, getSU2MeshConnections

TAG = "SU2MeshViewer: "


class SU2Read():
    # def __init__(self):
    # self.points = getSU2MeshPoints() # returns 3D array, x:y:z
    # self.connections = getSU2MeshConnections() # returns 5D array, type:p1:p2:p3:index
    # self.lines = self.makeLines()

    def getPoints(self):
        return getSU2MeshPoints()

    def getElements(self):
        return getSU2MeshConnections()

    def makeLines(self, points, connections):
        # iterate through all connections in the mesh.
        lineCoords = []
        count = 0
        # for connection in connections:
        # print(len(connections))
        for i in range(0, len(connections)):  # TODO, change to for in.
            # plus 1 on index as there is an identifier in zeroth place.
            # point1 = points[connection[1]-1]
            # point2 = points[connection[2]-1]
            # point3 = points[connection[3]-1]
            point1 = points[connections[i][1]]
            point2 = points[connections[i][2]]
            point3 = points[connections[i][3]]
            # add line 1-2
            lineCoords.append(point1[0])
            lineCoords.append(point1[1])
            lineCoords.append(point2[0])
            lineCoords.append(point2[1])
            # add line 2-3
            lineCoords.append(point2[0])
            lineCoords.append(point2[1])
            lineCoords.append(point3[0])
            lineCoords.append(point3[1])
            # add line 3-1
            lineCoords.append(point3[0])
            lineCoords.append(point3[1])
            lineCoords.append(point1[0])
            lineCoords.append(point1[1])
            # print(count)
            # count = count + 1
            # print(lineCoords)
        return lineCoords


# class Example(Frame):
#
#     def __init__(self):
#         super().__init__()
#
#         self.initUI()
#
#     def initUI(self):
#         self.master.title("Lines")
#         self.pack(fill=BOTH, expand=1)
#
#         canvas = Canvas(self)
#         canvas.pack()
#         data = SU2Read()
#         points = data.getPoints()
#         elems = data.getElements()
#         print(elems)
#         lines = data.makeLines(points, elems)
#         # convert lines float values to integers for test.
#         # multiply the coordinates to scale them.
#         for i in range(0, len(lines)):
#             lines[i] = lines[i]*100
#         # get most negative x.
#         mostX = 0
#         for i in range(0, len(lines), 2):
#             current = lines[i]
#             if current < mostX:
#                 mostX = current
#         # get most negative y.
#         mostY = 0
#         for i in range(1, len(lines), 2):
#             current = lines[i]
#             if current < mostY:
#                 mostY = current
#         mostX = -1*mostX
#         mostY = -1*mostY
#         for i in range(0, len(lines), 2):
#             lines[i] = lines[i] + mostX
#             lines[i+1] = lines[i+1] + mostY
#         # adjust for the coordinate system.
#         print(lines)
#         for i in range(0, len(lines), 4):
#             canvas.create_line(lines[i], lines[i+1], lines[i+2], lines[i+3],fill='black')
#
#
#
#
# def main():
#     root = Tk()
#     ex = Example()
#
#
#     root.geometry("1000x600+1000+600")
#     root.mainloop()
#
#
# if __name__ == '__main__':
#     main()

window = tkinter.Tk()
window.title("Mesh Viewer")
canvas = tkinter.Canvas(window, width=2500, height=1000)
canvas.pack()
data = SU2Read()
points = data.getPoints()
elems = data.getElements()
# print(elems)
lines = data.makeLines(points, elems)
# convert lines float values to integers for test. TODO. remove.
# multiply the coordinates to scale them.
for i in range(0, len(lines)):
    lines[i] = lines[i] * 100 # 100 is a scaling factor.
# get most negative x.
mostX = 0
for i in range(0, len(lines), 2):
    current = lines[i]
    if current < mostX:
        mostX = current
# get most negative y.
mostY = 0
for i in range(1, len(lines), 2):
    current = lines[i]
    if current < mostY:
        mostY = current
mostX = -1 * mostX
mostY = -1 * mostY
for i in range(0, len(lines), 2):
    lines[i] = lines[i] + mostX
    lines[i + 1] = lines[i + 1] + mostY
# adjust for the coordinate system.
# print(lines)
for i in range(0, len(lines), 4):
    canvas.create_line(lines[i], lines[i + 1], lines[i + 2], lines[i + 3], fill='black')

window.mainloop()
