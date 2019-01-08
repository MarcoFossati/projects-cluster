import math

# class to model the Point type in Gmsh.
class GPoint:
    def __init__(self):
        self.x = 0 # x-coord
        self.y = 0 # y-coord
        self.z = 0 # z-coord
        self.r = 0 # used for local refinement, usually leave as undefined.
        self.id = 0

# class to model the Line type in Gmsh.
class GLine:
    # a line is defined by 2 points and the ID for Gmsh.
    def __init__(self):
        self.p1 = 0
        self.p2 = 0
        self.id = 0

# class to model the Ellipse type in Gmsh.
class GEllipse:
    def __init__(self):
        self.p1 = 0
        self.p2 = 0
        self.p3 = 0
        self.p4 = 0
        self.id = 0

# class that can transform an array of points. Used to add angles of attack or could be extended for use in optimisation.
class Transform:
    def __init__(self):
        self.alpha = 0

    def rotate(self, inArray):
        outArray = []
        angle = math.radians(-self.alpha)
        for point in inArray:
            newPoint = GPoint()
            newPoint.x = point.x*math.cos(angle) - point.y*math.sin(angle)
            newPoint.y = point.y*math.cos(angle) + point.x*math.sin(angle)
            newPoint.z = point.z
            newPoint.r = point.r
            newPoint.id = point.id
            outArray.append(newPoint)
        return outArray
