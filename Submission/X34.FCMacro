#Author - Liam Watson
#created 16/01/2018

from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton
import FreeCAD, FreeCADGui, Draft
import importAirfoilDAT
import math

App.newDocument("X34")
#all dimensions in mm unless stated
'''
Mesh parameters
'''
#Creating a Netgen or Mefisto Mesh
#xyz=1 for Mefisto
#xyz=0 for Netgen
xyz = 1
#defining the maximum edge length for a mefisto mesh
max_element_edge = 100
#defining the element quality for a netgen mesh, must be between 1 and 6
m_quality = 4

'''
Input fuselage parameters and calculated variables
'''
#aircraft length
length = 16431.26

#distance from zero-datum (x)(square)
d_sq_x = 9320.682
#distance from zero-datum (y)(square)
d_sq_y = 0
#distance from zero-datum (z)(square)
d_sq_z = 0
#length of square fuselage
x_sq = length - d_sq_x
#width of square fuselage
y_sq = 1792.5
#height of square fuselage
z_sq = 1613.25
#radius of fillets on square fuselage
r_fillets = 75
#scaing factor 2 (for curved fuselage section)
sc2 = -40
#radius of nose sphere
nc_s = 300

#inner exhaust diameter
d_i_ex = 1254.75
#outer exhaust diameter
d_o_ex = 1792.25
#length of exhaust cone
l_ex_c = 645.3
#length of exhaust funnel
l_ex_f = 358.5

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
cm = 4302
#tip chord length
ct = 1720.8
#dihedral
dih = 2
zscale = 0
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
cm_x = 10217.25
#mid chord y-positions
cm_y = ((math.tan(math.radians(90 - i_w_s)))*(cm_x - cr_x)) + cr_y
#mid chord z-position
cm_z = math.tan(math.radians(dih))*(cm_y)

#tip chord x-position
ct_x = 12547.7
#tip chord y-position
ct_y = ((math.tan(math.radians(90 - s_w_s)))*(ct_x - cm_x)) + cm_y
#tip chord z-position
ct_z = math.tan(math.radians(2*dih))*(ct_y)

'''
tailfin input parameters and calculated variables
'''

#aerofoil
finaerofoil = str("D:/University/Year 4/Dissertation/Skylon/NACA0010-64.dat")
#distance from zero-datum (x)(base aerofoil)
d_fb_x = 15057
#distance from zero-datum (y)(base aerofoil)
d_fb_y = 0
#distance from zero-datum (z)(base aerofoil)
d_fb_z = z_sq

#angle of tailfin relative to the fuselage
f_beta = 40
#angle of tailfin relative to the airflow
f_alpha = 0
#tailfin height
f_height = 1792.5
#root chord of base aerofoils
f_ch_b = length - d_fb_x
#root chord of the mid aerofoil
f_ch_m = 1792.5
#root chord of the tip aerofoil
f_ch_t = 717

#distance from zero-datum (z)(mid aerofoil)
d_fm_z = z_sq + 300
#distance from zero-datum (x)(mid aerofoil)
d_fm_x = d_fb_x + (math.tan(math.radians(90-f_beta)))*(d_fm_z - z_sq)
#distance from zero-datum (y)(mid aerofoil)
d_fm_y = 0

#distance from zero-datum (z)(tip aerofoil)
d_ft_z = z_sq + f_height
#distance from zero-datum (x)(tip aerofoil)
d_ft_x = d_fb_x + (math.tan(math.radians(90-f_beta)))*(d_ft_z - z_sq)
#distance from zero-datum (y)(tip aerofoil)
d_ft_y = 0


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

App.ActiveDocument.addObject("Part::Fillet","Fillet")
App.ActiveDocument.Fillet.Base = App.ActiveDocument.Shape
__fillets__ = []
__fillets__.append((5,r_fillets,r_fillets))
__fillets__.append((8,r_fillets,r_fillets))
FreeCAD.ActiveDocument.Fillet.Edges = __fillets__
del __fillets__
FreeCADGui.ActiveDocument.Shape.Visibility = False
App.ActiveDocument.recompute()

'''
Creating exhaust vent
'''

App.activeDocument().addObject('Sketcher::SketchObject','front_vent')
App.activeDocument().front_vent.Placement = App.Placement(App.Vector(length, 0.000000, z_sq/2), App.Rotation(0.500000,0.500000,0.500000,0.500000))
App.ActiveDocument.front_vent.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),d_i_ex/2),False)
App.ActiveDocument.recompute()

App.activeDocument().addObject('Sketcher::SketchObject','middle_vent')
App.activeDocument().middle_vent.Placement = App.Placement(App.Vector(length + l_ex_f, 0.000000, z_sq/2), App.Rotation(0.500000,0.500000,0.500000,0.500000))
App.ActiveDocument.middle_vent.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),d_o_ex/2),False)
App.ActiveDocument.recompute()

App.activeDocument().addObject('Sketcher::SketchObject','end_vent')
App.activeDocument().end_vent.Placement = App.Placement(App.Vector(length + l_ex_c + l_ex_f, 0.000000, z_sq/2), App.Rotation(0.500000,0.500000,0.500000,0.500000))
App.ActiveDocument.end_vent.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),d_o_ex/2),False)
App.ActiveDocument.recompute()

from FreeCAD import Base
import Part
App.getDocument('X34').addObject('Part::Loft','Loft')
App.getDocument('X34').ActiveObject.Sections=[App.getDocument('X34').middle_vent, App.getDocument('X34').front_vent, ]
App.getDocument('X34').ActiveObject.Solid=True
App.getDocument('X34').ActiveObject.Ruled=False
App.getDocument('X34').ActiveObject.Closed=False

App.getDocument('X34').addObject('Part::Loft','Loft1')
App.getDocument('X34').ActiveObject.Sections=[App.getDocument('X34').middle_vent, App.getDocument('X34').end_vent, ]
App.getDocument('X34').ActiveObject.Solid=True
App.getDocument('X34').ActiveObject.Ruled=False
App.getDocument('X34').ActiveObject.Closed=False

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
v24 = Base.Vector(0, y_cv/2 +sc2, 0)
v25 = Base.Vector(0, y_cv/2 +sc2, z_cv/2 +sc2)
v26 = Base.Vector(0, 0, z_cv +sc2)
v27 = Base.Vector(0, -y_cv/2 -sc2, z_cv/2 +sc2)
v28 = Base.Vector(0, -y_cv/2 -sc2, 0)

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
boundary between curved and square fuselage
'''

#making points
v20 = Base.Vector(0, y_sq/2, 0)
v21 = Base.Vector(0, y_sq/2, z_sq)
v22 = Base.Vector(0, -y_sq/2, z_sq)
v23 = Base.Vector(0, -y_sq/2, 0)

#making lines from points
l17 = Part.Line(v20,v21)
l18 = Part.Line(v21,v22)
l19 = Part.Line(v22,v23)
l20 = Part.Line(v23,v20)

#making shape from lines
s5 = Part.Shape([l17, l18, l19, l20])
w5 = Part.Wire(s5.Edges)
f5 = Part.Face(w5)
Part.show(f5)

App.getDocument("X34").Shape004.Placement=App.Placement(App.Vector(d_sq_x , 0, 0), App.Rotation(0, 0, 0), App.Vector(0,0,0))
App.ActiveDocument.recompute()

#creating cyclinder inside the fuselage
App.activeDocument().addObject('Sketcher::SketchObject','lofting_fuselage')
App.activeDocument().lofting_fuselage.Placement = App.Placement(App.Vector(d_cv_x + (x_cv)/2, 0.000000,z_sq/2), App.Rotation(0.500000,0.500000,0.500000,0.500000))
App.ActiveDocument.lofting_fuselage.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),500),False)


App.getDocument('X34').addObject('Part::Loft','Loft5')
App.getDocument('X34').ActiveObject.Sections=[App.getDocument('X34').Shape004, App.getDocument('X34').lofting_fuselage, ]
App.getDocument('X34').ActiveObject.Solid=True
App.getDocument('X34').ActiveObject.Ruled=False
App.getDocument('X34').ActiveObject.Closed=False

App.ActiveDocument.recompute()

#filleting the edges of the boundary
FreeCAD.ActiveDocument.addObject("Part::Fillet","Fillet001")
FreeCAD.ActiveDocument.Fillet001.Base = FreeCAD.ActiveDocument.Loft5
__fillets__ = []
__fillets__.append((9,r_fillets,r_fillets))
__fillets__.append((12,r_fillets,r_fillets))
FreeCAD.ActiveDocument.Fillet001.Edges = __fillets__
del __fillets__
FreeCADGui.ActiveDocument.Loft5.Visibility = False

#removing the shape that interrupts the airflow
App.getDocument("X34").removeObject("Shape004")

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
App.activeDocument().Fusion.Shapes = [App.activeDocument().Loft2,App.activeDocument().Fillet001,App.activeDocument().Fillet,]
App.ActiveDocument.recompute()

App.activeDocument().addObject("Part::MultiFuse","Fusion001")
App.activeDocument().Fusion001.Shapes = [App.activeDocument().Sphere,App.activeDocument().Loft4,]
App.ActiveDocument.recompute()

App.activeDocument().addObject("Part::MultiFuse","Fusion002")
App.activeDocument().Fusion002.Shapes = [App.activeDocument().Loft, App.activeDocument().Loft1, App.activeDocument().Loft3, App.activeDocument().Part__Mirroring, App.activeDocument().Part__Mirroring001, App.activeDocument().Loft8, App.activeDocument().Loft9, App.activeDocument().Fusion, App.activeDocument().Fusion001, App.activeDocument().Loft7, App.activeDocument().Loft6,]
App.ActiveDocument.recompute()

'''
exporting as an STL and STEP file
'''

__objs__=[]
__objs__.append(FreeCAD.getDocument("X34").getObject("Fusion002"))

import Part
Part.export(__objs__,u"D:/University/Year 4/Dissertation/X-34/X34gmsh.step")
Part.export(__objs__,u"D:/University/Year 4/Dissertation/X-34/X34gmsh.iges")
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
    __mesh__.Mesh=MeshPart.meshFromShape(Shape=__doc__.getObject("Fusion002").Shape,MaxLength=max_element_edge)
    __mesh__.Label="Fusion002 (Meshed)"
    __mesh__.ViewObject.CreaseAngle=25.0
    del __doc__, __mesh__
    App.ActiveDocument.recompute()
else:
    __doc__=FreeCAD.getDocument("X34")
    __mesh__=__doc__.addObject("Mesh::Feature","Mesh")
    __mesh__.Mesh=MeshPart.meshFromShape(Shape=__doc__.getObject("Fusion002").Shape,Fineness=m_quality,SecondOrder=0,Optimize=1,AllowQuad=0)
    __mesh__.Label="Fusion002 (Meshed)"
    __mesh__.ViewObject.CreaseAngle=25.0
    del __doc__, __mesh__


FreeCAD.ActiveDocument.getObject("Mesh").Mesh.write("D:/University/Year 4/Dissertation/X-34/X34mesh.stl","STL","Fusion002 (Meshed)")
App.ActiveDocument.recompute()
