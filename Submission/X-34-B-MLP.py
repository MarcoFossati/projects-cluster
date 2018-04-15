#Author - Liam Watson
#created 29/01/2018

from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton
import FreeCAD, FreeCADGui, Draft
import importAirfoilDAT
import math


App.newDocument("X34")

#parameters that should always be zero
zero_p = 0

'''
Mesh parameters
'''
#Creating a Netgen or Mefisto Mesh
#xyz=1 for Mefisto
#xyz=0 for Netgen
xyz = 1
#defining the maximum edge length for a mefisto mesh
max_element_edge = 500
#defining the element quality for a netgen mesh, must be between 1 and 6
m_quality = 2

'''
Export parameters
'''
#CAD files destination
cad = D:/University/Year 4/Dissertation/X-34
#Mesh destination
mesh = D:/University/Year 4/Dissertation/X-34
#CAD file name
name_c = X34mesh_basicMLP
#Mesh naem
name_m = X34mesh_basicMLP

'''
Input fuselage parameters and calculated variables
'''
#aircraft length
length = 16431.26

#distance from zero-datum (x)(square)
d_sq_x = 9320.682
#distance from zero-datum (y)(square)
d_sq_y = zero_p
#distance from zero-datum (z)(square)
d_sq_z = zero_p
#length of square fuselage
x_sq = length - d_sq_x
#width of square fuselage
y_sq = 1792.5
#height of square fuselage
z_sq = y_sq
#radius of nose sphere
nc_s = y_sq/6

#length of curved fuselage
x_cv = 6094.5
#width of curved fuselage
y_cv = y_sq
#height of curved fuselage
z_cv = z_sq
#distance from zero-datum (x)(curved)
d_cv_x = 3226.5
#distance from zero-datum (y)(curved)
d_cv_y = d_sq_y
#distance from zero-datum (z)(curved)
d_cv_z = d_sq_z

#length of nose cone
x_nc = d_cv_x
#width of nose cone
y_nc = y_sq
#height of nose cone
z_nc = z_sq
#distance from zero-datum (x)(nose cone)
d_nc_x = d_cv_x
#distance from zero-datum (y)(nose cone)
d_nc_y = d_sq_y
#distance from zero-datum (z)(nose cone)
d_nc_z = d_sq_z

'''
Wing input variables and calculaed parameters
'''
#aerofoil
bodyaerofoil = str("D:/University/Year 4/Dissertation/Skylon/NACA0010-64.dat")

#root chord length
cr = 9821
#mid chord length
cm = cr/2
#tip chord length
ct = cr/4
#dihedral
dih = 6
zscale = zero_p
yscale = 0.1

#fuselage width
f_width = y_sq
#initial wing sweep angle
i_w_s = 80
#second wing sweep angle
s_w_s = 45

#root chord x-position
cr_x = 4943.5
#root chord y-position
cr_y = f_width/2
#wing root thickness
th_m = 0.05
#root chord z-position
cr_z = (cr/yscale)*th_m/20

#mid chord x-position
cm_x = 2*cr_x
#mid chord y-position
cm_y = ((math.tan(math.radians(90 - i_w_s)))*(cm_x - cr_x)) + cr_y
#mid chord z-position
cm_z = math.tan(math.radians(dih))*(cm_y)

#tip chord x-position
ct_x = 2.5*cr_x
#tip chord y-position
ct_y = ((math.tan(math.radians(90 - s_w_s)))*(ct_x - cm_x)) + cr_y + cm_y
#tip chord z-position
ct_z = math.tan(math.radians(dih))*(ct_y)

'''
tailfin input parameters and calculated variables
'''

#aerofoil
finaerofoil = str("D:/University/Year 4/Dissertation/Skylon/NACA0010-64.dat")
#distance from zero-datum (x)(base aerofoil)
d_fb_x = 15057
#distance from zero-datum (y)(base aerofoil)
d_fb_y = zero_p
#distance from zero-datum (z)(base aerofoil)
d_fb_z = z_sq

#angle of tailfin relative to the fuselage
f_beta = s_w_s
#tailfin height
f_height = y_sq
#root chord of base aerofoils
f_ch_b = length - d_fb_x
#root chord of the mid aerofoil
f_ch_m = f_height - 200
#root chord of the tip aerofoil
f_ch_t = f_height/2

#distance from zero-datum (z)(mid aerofoil)
d_fm_z = z_sq + 300
#distance from zero-datum (x)(mid aerofoil)
d_fm_x = d_fb_x + (math.tan(math.radians(90-f_beta)))*(d_fm_z - z_sq)
#distance from zero-datum (y)(mid aerofoil)
d_fm_y = d_fb_y

#distance from zero-datum (z)(tip aerofoil)
d_ft_z = z_sq + f_height
#distance from zero-datum (x)(tip aerofoil)
d_ft_x = d_fb_x + (math.tan(math.radians(90-f_beta)))*(d_ft_z - z_sq)
#distance from zero-datum (y)(tip aerofoil)
d_ft_y = d_fb_y


'''
creating square fuselage
'''
from FreeCAD import Base
import Part

#making points
v1 = Base.Vector(0, y_sq/2, 0)
v2 = Base.Vector(0, y_sq/2, z_sq)
v3 = Base.Vector(0, -y_sq/2, z_sq)
v4 = Base.Vector(0, -y_sq/2, 0)

#making lines from points
l1 = Part.Line(v1,v2)
l2 = Part.Line(v2,v3)
l3 = Part.Line(v3,v4)
l4 = Part.Line(v4,v1)

#making shape from lines
s1 = Part.Shape([l1, l2, l3, l4])
w1 = Part.Wire(s1.Edges)
f1 = Part.Face(w1)
P = f1.extrude(Base.Vector(x_sq,0,0))
Part.show(P)

App.getDocument("X34").Shape.Placement=App.Placement(App.Vector(d_sq_x , d_sq_y, d_sq_z), App.Rotation(0, 0, 0), App.Vector(0,0,0))

App.ActiveDocument.recompute()


'''
Creating curved fuselage section
'''

#making points
v5 = Base.Vector(0, y_cv/2, 0)
v6 = Base.Vector(0, y_cv/2, z_cv/2)
v7 = Base.Vector(0, 0, z_cv)
v8 = Base.Vector(0, -y_cv/2, z_cv/2)
v9 = Base.Vector(0, -y_cv/2, 0)

#making lines from points
l5 = Part.Line(v5,v6)
l6 = Part.Arc(v6,v7,v8)
l7 = Part.Line(v8,v9)
l8 = Part.Line(v9,v5)

#making shape from lines
s2 = Part.Shape([l5, l6, l7, l8])
w2 = Part.Wire(s2.Edges)
f2 = Part.Face(w2)
Part.show(f2)

App.ActiveDocument.recompute()

App.getDocument("X34").Shape001.Placement=App.Placement(App.Vector(d_sq_x , d_sq_y, d_sq_z), App.Rotation(0, 0, 0), App.Vector(0,0,0))

App.ActiveDocument.recompute()

'''
middle of curved fuselage
'''
#making points
v29 = Base.Vector(0, y_cv/2, 0)
v30 = Base.Vector(0, y_cv/2, z_cv/2)
v31 = Base.Vector(0, 0, z_cv)
v32 = Base.Vector(0, -y_cv/2, z_cv/2)
v33 = Base.Vector(0, -y_cv/2, 0)

#making lines from points
l25 = Part.Line(v29,v30)
l26 = Part.Arc(v30,v31,v32)
l27 = Part.Line(v32,v33)
l28 = Part.Line(v33,v29)

#making shape from lines
s7 = Part.Shape([l25, l26, l27, l28])
w7 = Part.Wire(s7.Edges)
f7 = Part.Face(w7)
Part.show(f7)

App.ActiveDocument.recompute()

App.getDocument("X34").Shape002.Placement=App.Placement(App.Vector(cr_x, d_cv_y, d_cv_z), App.Rotation(0, 0, 0), App.Vector(0,0,0))

App.ActiveDocument.recompute()

'''
making end of curved fuselage
'''
#making points
v24 = Base.Vector(0, y_cv/2 -40, 0)
v25 = Base.Vector(0, y_cv/2 -40, z_cv/2 -40)
v26 = Base.Vector(0, 0, z_cv -40)
v27 = Base.Vector(0, -y_cv/2 +40, z_cv/2 -40)
v28 = Base.Vector(0, -y_cv/2 +40, 0)

#making lines from points
l21 = Part.Line(v24,v25)
l22 = Part.Arc(v25,v26,v27)
l23 = Part.Line(v27,v28)
l24 = Part.Line(v28,v24)

#making shape from lines
s6 = Part.Shape([l21, l22, l23, l24])
w6 = Part.Wire(s6.Edges)
f6 = Part.Face(w6)
Part.show(f6)

App.ActiveDocument.recompute()

App.getDocument("X34").Shape003.Placement=App.Placement(App.Vector(d_cv_x , d_cv_y, d_cv_z), App.Rotation(0, 0, 0), App.Vector(0,0,0))

App.ActiveDocument.recompute()

App.getDocument('X34').addObject('Part::Loft','Loft2')
App.getDocument('X34').ActiveObject.Sections=[ App.getDocument('X34').Shape002, App.getDocument('X34').Shape001,]
App.getDocument('X34').ActiveObject.Solid=True
App.getDocument('X34').ActiveObject.Ruled=False
App.getDocument('X34').ActiveObject.Closed=False

App.ActiveDocument.recompute()

'''
creating nose cone
'''

#making sphere for nose cone
App.ActiveDocument.addObject("Part::Sphere","Sphere")
FreeCAD.getDocument("X34").getObject("Sphere").Radius = nc_s
FreeCAD.getDocument("X34").getObject("Sphere").Angle3 = 180.00
App.getDocument("X34").Sphere.Placement=App.Placement(App.Vector(nc_s,0,2*nc_s), App.Rotation(App.Vector(0,0,1),90), App.Vector(0,0,0))
App.ActiveDocument.recompute()

#making circle for lofting  to nose cone
App.activeDocument().addObject('Sketcher::SketchObject','n_cone')
App.ActiveDocument.getObject("n_cone").Placement = App.Placement(App.Vector(nc_s, 0, 2*nc_s ),App.Rotation(App.Vector(0,1,0),90))
App.activeDocument().n_cone.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),nc_s),False)

#lofting to create nose cone
from FreeCAD import Base
import Part
App.getDocument('X34').addObject('Part::Loft','Loft3')
App.getDocument('X34').ActiveObject.Sections=[ App.getDocument('X34').Shape002, App.getDocument('X34').Shape003,]
App.getDocument('X34').ActiveObject.Solid=True
App.getDocument('X34').ActiveObject.Ruled=False
App.getDocument('X34').ActiveObject.Closed=False

App.ActiveDocument.recompute()

App.getDocument('X34').addObject('Part::Loft','Loft4')
App.getDocument('X34').ActiveObject.Sections=[App.getDocument('X34').n_cone, App.getDocument('X34').Shape003, ]
App.getDocument('X34').ActiveObject.Solid=True
App.getDocument('X34').ActiveObject.Ruled=False
App.getDocument('X34').ActiveObject.Closed=False

App.ActiveDocument.recompute()


'''
creating wing
'''

from FreeCAD import Base
import Part

#importing, scaling and positioning root aerofoil
importAirfoilDAT.insert(bodyaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(cr, (cr/yscale)*th_m, zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.ActiveDocument.getObject("BSpline").Placement = App.Placement(App.Vector(cr_x, cr_y, cr_z),App.Rotation(App.Vector(1,0,0),90))
FreeCAD.ActiveDocument.removeObject("DWire")
App.ActiveDocument.recompute()

#importing, scaling and positioning mid aerofoil
importAirfoilDAT.insert(bodyaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(cm, cm, zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.ActiveDocument.getObject("BSpline001").Placement = App.Placement(App.Vector(cm_x, cm_y, cm_z),App.Rotation(App.Vector(1,0,0),90))
FreeCAD.ActiveDocument.removeObject("DWire")
App.ActiveDocument.recompute()

#importing, scaling and positioning tip aerofoil
importAirfoilDAT.insert(bodyaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(ct, ct, zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.ActiveDocument.getObject("BSpline002").Placement = App.Placement(App.Vector(ct_x, ct_y, ct_z),App.Rotation(App.Vector(1,0,0),90))
FreeCAD.ActiveDocument.removeObject("DWire")
App.ActiveDocument.recompute()

from FreeCAD import Base
import Part
App.getDocument('X34').addObject('Part::Loft','Loft6')
App.getDocument('X34').ActiveObject.Sections=[App.getDocument('X34').BSpline, App.getDocument('X34').BSpline001, ]
App.getDocument('X34').ActiveObject.Solid=True
App.getDocument('X34').ActiveObject.Ruled=False
App.getDocument('X34').ActiveObject.Closed=False

App.getDocument('X34').addObject('Part::Loft','Loft7')
App.getDocument('X34').ActiveObject.Sections=[App.getDocument('X34').BSpline001, App.getDocument('X34').BSpline002, ]
App.getDocument('X34').ActiveObject.Solid=True
App.getDocument('X34').ActiveObject.Ruled=False
App.getDocument('X34').ActiveObject.Closed=False

App.ActiveDocument.recompute()

#mirroring th wing
__doc__=FreeCAD.getDocument("X34")
__doc__.addObject("Part::Mirroring")
__doc__.ActiveObject.Source=__doc__.getObject("Loft6")
__doc__.ActiveObject.Label=u"Loft6 (Mirror #1)"
__doc__.ActiveObject.Normal=(0,1,0)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__

__doc__=FreeCAD.getDocument("X34")
__doc__.addObject("Part::Mirroring")
__doc__.ActiveObject.Source=__doc__.getObject("Loft7")
__doc__.ActiveObject.Label=u"Loft7 (Mirror #2)"
__doc__.ActiveObject.Normal=(0,1,0)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__

App.ActiveDocument.recompute()

'''
creating the Tailfin
'''
from FreeCAD import Base
import Part

#importing, scaling and positioning fin  aerofoils
importAirfoilDAT.insert(finaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(f_ch_b, f_ch_b, zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.ActiveDocument.getObject("BSpline003").Placement = App.Placement(App.Vector(d_fb_x, d_fb_y, d_fb_z ),App.Rotation(App.Vector(0,0,1),0))
FreeCAD.ActiveDocument.removeObject("DWire")
App.ActiveDocument.recompute()

importAirfoilDAT.insert(finaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(f_ch_m, f_ch_m, zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.ActiveDocument.getObject("BSpline004").Placement = App.Placement(App.Vector(d_fm_x, d_fm_y,  d_fm_z),App.Rotation(App.Vector(0,0,1),0))
FreeCAD.ActiveDocument.removeObject("DWire")
App.ActiveDocument.recompute()

importAirfoilDAT.insert(finaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(f_ch_t, f_ch_t, zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.ActiveDocument.getObject("BSpline005").Placement = App.Placement(App.Vector(d_ft_x, d_ft_y, d_ft_z),App.Rotation(App.Vector(0,0,1),0))
FreeCAD.ActiveDocument.removeObject("DWire")
App.ActiveDocument.recompute()

App.getDocument('X34').addObject('Part::Loft','Loft8')
App.getDocument('X34').ActiveObject.Sections=[App.getDocument('X34').BSpline003, App.getDocument('X34').BSpline004,]
App.getDocument('X34').ActiveObject.Solid=True
App.getDocument('X34').ActiveObject.Ruled=False
App.getDocument('X34').ActiveObject.Closed=False
App.ActiveDocument.recompute()

App.getDocument('X34').addObject('Part::Loft','Loft9')
App.getDocument('X34').ActiveObject.Sections=[App.getDocument('X34').BSpline004, App.getDocument('X34').BSpline005,]
App.getDocument('X34').ActiveObject.Solid=True
App.getDocument('X34').ActiveObject.Ruled=False
App.getDocument('X34').ActiveObject.Closed=False
App.ActiveDocument.recompute()

'''
fusing the model together
'''

App.activeDocument().addObject("Part::MultiFuse","Fusion")
App.activeDocument().Fusion.Shapes = [App.activeDocument().Shape, App.activeDocument().Loft2, App.activeDocument().Loft3, App.activeDocument().Sphere, App.activeDocument().Loft4, App.activeDocument().Part__Mirroring, App.activeDocument().Part__Mirroring001, App.activeDocument().Loft6, App.activeDocument().Loft7, App.activeDocument().Loft8, App.activeDocument().Loft9,]
App.ActiveDocument.recompute()

'''
exporting as an STL and STEP file
'''

__objs__=[]
__objs__.append(FreeCAD.getDocument("X34").getObject("Fusion"))

import Mesh
Mesh.export(__objs__,u"D:/University/Year 4/Dissertation/X-34/X34mesh_basicMLP.stl")
import ImportGui
ImportGui.export(__objs__,u"D:/University/Year 4/Dissertation/X-34/X34mesh_basicMLP.step")

del __objs__

App.ActiveDocument.recompute()

'''
creating mesh and exporting it
'''

import Mesh
import MeshPart

if xyz == 1:
    __doc__=FreeCAD.getDocument("X34")
    __mesh__=__doc__.addObject("Mesh::Feature","Mesh")
    __mesh__.Mesh=MeshPart.meshFromShape(Shape=__doc__.getObject("Fusion").Shape,MaxLength=max_element_edge)
    __mesh__.Label="Fusion002 (Meshed)"
    __mesh__.ViewObject.CreaseAngle=25.0
    del __doc__, __mesh__
    App.ActiveDocument.recompute()
else:
    __doc__=FreeCAD.getDocument("X34")
    __mesh__=__doc__.addObject("Mesh::Feature","Mesh")
    __mesh__.Mesh=MeshPart.meshFromShape(Shape=__doc__.getObject("Fusion").Shape,Fineness=m_quality,SecondOrder=0,Optimize=1,AllowQuad=0)
    __mesh__.Label="Fusion002 (Meshed)"
    __mesh__.ViewObject.CreaseAngle=25.0
    del __doc__, __mesh__


FreeCAD.ActiveDocument.getObject("Mesh").Mesh.write("D:/University/Year 4/Dissertation/X-34/X34mesh_basicMLP.stl","STL","Fusion (Meshed)"")
App.ActiveDocument.recompute()
