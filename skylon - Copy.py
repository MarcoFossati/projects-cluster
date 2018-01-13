#Author - Liam Watson
#created 11/11/2017
#updated 13/01/2018

from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton
import FreeCAD, FreeCADGui, Draft
import importAirfoilDAT
import math

App.newDocument("Skylon")
App.setActiveDocument("Skylon")
App.ActiveDocument = App.getDocument("Skylon")
Gui.ActiveDocument = Gui.getDocument("Skylon")

'''
All dimensions are in mm,
unless stated otherwise
'''
'''
fuselage input parameters and calculated parameters
'''
#define the radius of the fuselage at cargo bay
d_cargo = 6300
r_cargo = d_cargo/2
#define the length of the cargo bay
l_cargo = 28000
#define the length of the l_aircraft
l_aircraft = 83133
#define the maximum angle of attack at takeoff in degrees
a_takeoff = 10
#radius of fuselage exhaust
r_exhaust_f = 250
#height of tail above horizontal datum
h_exhaust=(math.tan(math.radians(a_takeoff))*((l_aircraft - l_cargo)/2))/2 + (r_exhaust_f/2)


'''
Engine input parameters and calculated parameters
'''

#distance of engine datum point to the zero datum point (x-axis)
d_front_datum_x = 49207
#distance of engine datum point to the zero datum point (y-axis)
d_from_datum_y = 10917
#distance of engine datum point to the zero datum point (z-axis)
d_from_datum_z = -1350

#diameter of the front of the initial vent
d_back_vent1 = 3694
r_back_vent1 = d_back_vent1/2
#diameter of the front of the initial vents
d_front_vent1 = 3334
r_front_vent1 = d_front_vent1/2
#diameter of the front of the main engine body
d_front_eng2 = 3794
r_front_eng2 = d_front_eng2/2
#diameter of the rear of the engine
d_rear_eng = 4984
r_rear_eng = d_rear_eng/2
#diameter of the base of the cone
d_cone_base = 3234
r_cone_base = d_cone_base/2

#length of the main engine body
l_engine_body = 12047
#length of the initial vent
l_front_vent = 1159
#length of nose cone
l_engine_cone = 2294
#angle of the rear of the engine from engine datum
a_rear_eng = 5
#angle of attack during cruise conditions
a_attack_cruise = 7
#angle of the front of the engine from the engine datum
a_front_eng = a_attack_cruise

#height of 'Rear_eng' from engine datum
h_Rear_eng = -(math.tan(math.radians(a_rear_eng))*l_engine_body/2)
#height of 'mid_eng' from engine datum
h_mid_eng = 0
#height of 'front_eng' from engine datum
h_front_eng = -math.tan(math.radians(a_front_eng))*(l_engine_body/2)
#height of 'front_eng_vent1' from ngine datum
h_front_eng_vent1 = -(math.tan(math.radians(a_front_eng))*((l_engine_body/2) + l_front_vent))
#height of 'cone tip' from engine datum
h_cone_tip = -( math.tan( math.radians( a_front_eng ))* ((l_engine_body/2) + l_front_vent + l_engine_cone))

'''
Wing input parameters and calculated variables
'''
#define input parameters
#aerofoils
bodyaerofoil = str("D:/University/Year 4/Dissertation/Skylon/NACA0010-64.dat")
tipaerofoil = str("D:/University/Year 4/Dissertation/Skylon/NACA0010-64.dat")

#front wing sweep angle
wing_sweep_angle_f = 55
#rear wing sweep angle
wing_sweep_angle_r = 15

#wing root chord
root_chord = 25517
#wing tip chord
tip_chord = 7000
#wing span
span = 21834

#root thickness
root_thick = 1200
#tip thickness
tip_thick = 510
#aerofoil twist @ root (degrees)
twist_root = 0
#aerofoil twist @ tip (degrees)
twist_tip = 0
#diherdral (degrees)
dihedral = 6.273

#distance of wing root to the zero datum point
d_from_datum_wing_root_x = 31473
d_from_datum_wing_root_y = 0.000000
d_from_datum_wing_root_z = -2550

#distance of wing tip to the zero datum point
d_from_datum_wing_tip_x = (d_from_datum_wing_root_x + (math.tan(math.radians(wing_sweep_angle_f))*span/2))
d_from_datum_wing_tip_y = span/2
d_from_datum_wing_tip_z = ((math.tan(math.radians(dihedral))*(span/2))+d_from_datum_wing_root_z)

zk1 = d_from_datum_wing_root_z
zk2 = d_from_datum_wing_tip_z

xk1 = d_from_datum_wing_root_x
xk2 = d_from_datum_wing_tip_x

#kink chords
ck1 = root_chord
ck2 = tip_chord

yk1 = ck1
yk2 = ck2

'''
Canard input variables and calculated parameters
'''
canardaerofoil = str("D:/University/Year 4/Dissertation/Skylon/NACA0010-64.dat")

#angle of canards with respect to fuselage
fuse_alpha = 13
#angle of attack of canard in degrees
c_alpha = -10
zscale = 0
#canard centre distance from the datum point
d_canard_from_x = 4000
d_canard_from_y = (math.tan(math.radians(fuse_alpha))*(d_canard_from_x)) + 150
d_canard_from_z = 0

#canard span
canard_span = 9300
d_span = canard_span/2

#canard base chord
cb_c = 6000
#canard tip chord
ct_c = 1200

#Abbreivations
dc_x = d_canard_from_x
dc_y = d_canard_from_y
dc_z = d_canard_from_z


'''
Tailfin input parameters and calculated variables
'''

tailaerofoil = str("D:/University/Year 4/Dissertation/Skylon/NACA0010-64.dat")
#curvature of fuselage
beta = (math.radians(math.atan((r_cargo - h_exhaust - r_exhaust_f)/((l_aircraft - l_cargo)/2))))

#tailfin angle relative to the airflow
fin_alpha = 0
#tailfin thickness
fin_thick = 300
#tailfin length
fin_length_base = 7261
#tailfin height
fin_height = 4444
#length of the top of the tailfin
fin_length_top = 1500

#distances from zero datum (fin)
d_fin_from_x = 74633
d_fin_from_y = fin_thick/2
d_fin_from_z = r_cargo - beta*(d_fin_from_x - ((l_aircraft+l_cargo)/2))

#Abbreivations for use
fch_b = fin_length_base
fch_t = fin_length_top
df_x = d_fin_from_x
df_y = d_fin_from_y
df_z = d_fin_from_z
fh = fin_height

"""
Creating the fuselage
"""
from FreeCAD import Base
import Part

#creating first cirlce for the fuselage at cargo bay
App.activeDocument().addObject('Sketcher::SketchObject','Cargo1')
App.activeDocument().Cargo1.Placement = App.Placement(App.Vector((l_aircraft - l_cargo)/2, 0.000000,0.000000), App.Rotation(0.500000,0.500000,0.500000,0.500000))
App.ActiveDocument.Cargo1.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_cargo),False)

#creating second cirlce for the fuselage at cargo bay
App.activeDocument().addObject('Sketcher::SketchObject','Cargo2')
App.activeDocument().Cargo2.Placement = App.Placement(App.Vector(l_aircraft/2, 0.000000, 0.000000), App.Rotation(0.500000,0.500000,0.500000,0.500000))
App.ActiveDocument.Cargo2.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_cargo),False)

#creating second cirlce for the fuselage at cargo bay
App.activeDocument().addObject('Sketcher::SketchObject','Cargo3')
App.activeDocument().Cargo3.Placement = App.Placement(App.Vector((l_aircraft + l_cargo)/2, 0.000000, 0.000000), App.Rotation(0.500000,0.500000,0.500000,0.500000))
App.ActiveDocument.Cargo3.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_cargo),False)

#creating nose of the aircraft
App.activeDocument().addObject('Sketcher::SketchObject','nose')
App.activeDocument().nose.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.500000,0.500000,0.500000,0.500000))
App.ActiveDocument.nose.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),0.000001),False)

#creating tail of the aircraft
App.activeDocument().addObject('Sketcher::SketchObject','tail')
App.activeDocument().tail.Placement =                     App.Placement(App.Vector(l_aircraft,0.000000,h_exhaust),App.Rotation(0.500000,0.500000,0.500000,0.500000))
App.ActiveDocument.tail.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_exhaust_f),False)

#recomputing the document
App.ActiveDocument.recompute

#lofting from nose to tail
from FreeCAD import Base
import Part
App.getDocument('Skylon').addObject('Part::Loft','Loft1')
App.getDocument('Skylon').ActiveObject.Sections=[App.getDocument('Skylon').nose, App.getDocument('Skylon').Cargo1, App.getDocument('Skylon').Cargo2, App.getDocument('Skylon').Cargo3, App.getDocument('Skylon').tail, ]
App.getDocument('Skylon').ActiveObject.Solid=True
App.getDocument('Skylon').ActiveObject.Ruled=False
App.getDocument('Skylon').ActiveObject.Closed=False

App.ActiveDocument.recompute

"""
creating the right hand side engine
"""
#creating sketch at the rear of the engine
App.activeDocument().addObject('Sketcher::SketchObject','Rear_eng_r')
App.activeDocument().Rear_eng_r.Placement = App.Placement(App.Vector(d_front_datum_x + l_engine_body/2, d_from_datum_y, d_from_datum_z + h_Rear_eng), App.Rotation(App.Vector(0.000000,1.000,0.00000),(90+a_rear_eng)), App.Vector(0,0,0))
App.activeDocument().Rear_eng_r.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_rear_eng),False)

#creating sketch at the middle of the engine
App.activeDocument().addObject('Sketcher::SketchObject','mid_eng_r')
App.activeDocument().mid_eng_r.Placement = App.Placement(App.Vector(d_front_datum_x, d_from_datum_y, d_from_datum_z + h_mid_eng), App.Rotation(0.500000,0.500000,0.500000,0.500000))
App.ActiveDocument.mid_eng_r.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),(r_rear_eng+r_front_eng2)/2),False)

#creating sketch at the front of the engine
App.activeDocument().addObject('Sketcher::SketchObject','front_eng_r')
App.activeDocument().front_eng_r.Placement = App.Placement(App.Vector(d_front_datum_x - l_engine_body/2, d_from_datum_y, d_from_datum_z + h_front_eng), App.Rotation(App.Vector(0.00000,1.0000,0.00000),90-a_front_eng), App.Vector(0,0,0))
App.activeDocument().front_eng_r.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_front_eng2),False)

from FreeCAD import Base
import Part
App.getDocument('Skylon').addObject('Part::Loft','Loft2')
App.getDocument('Skylon').ActiveObject.Sections=[App.getDocument('Skylon').front_eng_r, App.getDocument('Skylon').mid_eng_r, App.getDocument('Skylon').Rear_eng_r, ]
App.getDocument('Skylon').ActiveObject.Solid=True
App.getDocument('Skylon').ActiveObject.Ruled=False
App.getDocument('Skylon').ActiveObject.Closed=False

App.ActiveDocument.recompute

#creating sketch at the front of the engine for the back of the vent
App.activeDocument().addObject('Sketcher::SketchObject','front_eng_vent2_r')
App.activeDocument().front_eng_vent2_r.Placement = App.Placement(App.Vector(d_front_datum_x - l_engine_body/2, d_from_datum_y, d_from_datum_z + h_front_eng), App.Rotation(App.Vector(0.00000,1.00000,0.00000),90- a_front_eng), App.Vector(0,0,0))
App.activeDocument().front_eng_vent2_r.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_back_vent1),False)

#creating sketch at the front of the engine for the front of the vent
App.activeDocument().addObject('Sketcher::SketchObject','front_eng_vent1_r')
App.activeDocument().front_eng_vent1_r.Placement = App.Placement(App.Vector(d_front_datum_x - l_engine_body/2- l_front_vent, d_from_datum_y, d_from_datum_z + h_front_eng_vent1),App.Rotation(App.Vector(0.00000,1.00000,0.00000),90 - a_front_eng), App.Vector(0,0,0))
App.activeDocument().front_eng_vent1_r.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_front_vent1),False)

#lofting between the front vents
from FreeCAD import Base
import Part
App.getDocument('Skylon').addObject('Part::Loft','Loft3')
App.getDocument('Skylon').ActiveObject.Sections=[App.getDocument('Skylon').front_eng_vent2_r, App.getDocument('Skylon').front_eng_vent1_r, ]
App.getDocument('Skylon').ActiveObject.Solid=True
App.getDocument('Skylon').ActiveObject.Ruled=False
App.getDocument('Skylon').ActiveObject.Closed=False

App.ActiveDocument.recompute

#creating sketch for the base of the engine cone
App.activeDocument().addObject('Sketcher::SketchObject','cone_base_r')
App.activeDocument().cone_base_r.Placement = App.Placement(App.Vector(d_front_datum_x - l_engine_body/2- l_front_vent, d_from_datum_y, d_from_datum_z + h_front_eng_vent1),App.Rotation(App.Vector(0.00000,1.00000,0.00000),90 - a_front_eng), App.Vector(0,0,0))
App.activeDocument().cone_base_r.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_cone_base),False)

#creating sketch at the tip of the cone
App.activeDocument().addObject('Sketcher::SketchObject','cone_tip_r')
App.activeDocument().cone_tip_r.Placement = App.Placement(App.Vector(d_front_datum_x - l_engine_body/2 - l_front_vent - l_engine_cone, d_from_datum_y, d_from_datum_z + h_cone_tip-250),App.Rotation(App.Vector(0.00000,1.00000,0.00000),90 - a_front_eng), App.Vector(0,0,0))
App.activeDocument().cone_tip_r.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1), 0.000001),False)

#lofting to create the engine tip cone
from FreeCAD import Base
import Part
App.getDocument('Skylon').addObject('Part::Loft','Loft4')
App.getDocument('Skylon').ActiveObject.Sections=[App.getDocument('Skylon').cone_base_r, App.getDocument('Skylon').cone_tip_r, ]
App.getDocument('Skylon').ActiveObject.Solid=True
App.getDocument('Skylon').ActiveObject.Ruled=False
App.getDocument('Skylon').ActiveObject.Closed=False

"""
creating the left hand side engine
"""
#creating sketch at the rear of the engine
App.activeDocument().addObject('Sketcher::SketchObject','Rear_eng_l')
App.activeDocument().Rear_eng_l.Placement = App.Placement(App.Vector(d_front_datum_x + l_engine_body/2, -d_from_datum_y, d_from_datum_z + h_Rear_eng), App.Rotation(App.Vector(0.000000,1.000,0.00000),(90+a_rear_eng)), App.Vector(0,0,0))
App.activeDocument().Rear_eng_l.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_rear_eng),False)

#creating sketch at the middle of the engine
App.activeDocument().addObject('Sketcher::SketchObject','mid_eng_l')
App.activeDocument().mid_eng_l.Placement = App.Placement(App.Vector(d_front_datum_x, -d_from_datum_y, d_from_datum_z + h_mid_eng), App.Rotation(0.500000,0.500000,0.500000,0.500000))
App.ActiveDocument.mid_eng_l.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),(r_rear_eng+r_front_eng2)/2),False)

#creating sketch at the front of the engine
App.activeDocument().addObject('Sketcher::SketchObject','front_eng_l')
App.activeDocument().front_eng_l.Placement = App.Placement(App.Vector(d_front_datum_x - l_engine_body/2, -d_from_datum_y, d_from_datum_z + h_front_eng), App.Rotation(App.Vector(0.00000,1.0000,0.00000),90-a_front_eng), App.Vector(0,0,0))
App.activeDocument().front_eng_l.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_front_eng2),False)

from FreeCAD import Base
import Part
App.getDocument('Skylon').addObject('Part::Loft','Loft5')
App.getDocument('Skylon').ActiveObject.Sections=[App.getDocument('Skylon').front_eng_l, App.getDocument('Skylon').mid_eng_l, App.getDocument('Skylon').Rear_eng_l, ]
App.getDocument('Skylon').ActiveObject.Solid=True
App.getDocument('Skylon').ActiveObject.Ruled=False
App.getDocument('Skylon').ActiveObject.Closed=False

App.ActiveDocument.recompute

#creating sketch at the front of the engine for the back of the vent
App.activeDocument().addObject('Sketcher::SketchObject','front_eng_vent2_l')
App.activeDocument().front_eng_vent2_l.Placement = App.Placement(App.Vector(d_front_datum_x - l_engine_body/2, -d_from_datum_y, d_from_datum_z + h_front_eng), App.Rotation(App.Vector(0.00000,1.00000,0.00000),90- a_front_eng), App.Vector(0,0,0))
App.activeDocument().front_eng_vent2_l.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_back_vent1),False)

#creating sketch at the front of the engine for the front of the vent
App.activeDocument().addObject('Sketcher::SketchObject','front_eng_vent1_l')
App.activeDocument().front_eng_vent1_l.Placement = App.Placement(App.Vector(d_front_datum_x - l_engine_body/2 - l_front_vent, -d_from_datum_y, d_from_datum_z + h_front_eng_vent1),App.Rotation(App.Vector(0.00000,1.00000,0.00000),90 - a_front_eng), App.Vector(0,0,0))
App.activeDocument().front_eng_vent1_l.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_front_vent1),False)

#lofting between the front vents
from FreeCAD import Base
import Part
App.getDocument('Skylon').addObject('Part::Loft','Loft6')
App.getDocument('Skylon').ActiveObject.Sections=[App.getDocument('Skylon').front_eng_vent2_l, App.getDocument('Skylon').front_eng_vent1_l, ]
App.getDocument('Skylon').ActiveObject.Solid=True
App.getDocument('Skylon').ActiveObject.Ruled=False
App.getDocument('Skylon').ActiveObject.Closed=False

App.ActiveDocument.recompute

#creating sketch for the base of the engine cone
App.activeDocument().addObject('Sketcher::SketchObject','cone_base_l')
App.activeDocument().cone_base_l.Placement = App.Placement(App.Vector(d_front_datum_x - l_engine_body/2- l_front_vent, -d_from_datum_y, d_from_datum_z + h_front_eng_vent1),App.Rotation(App.Vector(0.00000,1.00000,0.00000),90 - a_front_eng), App.Vector(0,0,0))
App.activeDocument().cone_base_l.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1),r_cone_base),False)

#creating sketch at the tip of the cone
App.activeDocument().addObject('Sketcher::SketchObject','cone_tip_l')
App.activeDocument().cone_tip_l.Placement = App.Placement(App.Vector(d_front_datum_x - l_engine_body/2 - l_front_vent - l_engine_cone, -d_from_datum_y, d_from_datum_z + h_cone_tip-250),App.Rotation(App.Vector(0.00000,1.00000,0.00000),90 - a_front_eng), App.Vector(0,0,0))
App.activeDocument().cone_tip_l.addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0.000000),App.Vector(0,0,1), 0.000001),False)

#lofting to create the engine tip cone
from FreeCAD import Base
import Part
App.getDocument('Skylon').addObject('Part::Loft','Loft7')
App.getDocument('Skylon').ActiveObject.Sections=[App.getDocument('Skylon').cone_base_l, App.getDocument('Skylon').cone_tip_l, ]
App.getDocument('Skylon').ActiveObject.Solid=True
App.getDocument('Skylon').ActiveObject.Ruled=False
App.getDocument('Skylon').ActiveObject.Closed=False

App.ActiveDocument.recompute

'''
Creating wing
'''

#importing, scaling and positioning centre aerofoil
importAirfoilDAT.insert(bodyaerofoil,FreeCAD.ActiveDocument.Name)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(ck1,yk1,zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.ActiveDocument.getObject("DWire").Placement = App.Placement(App.Vector(xk1,0,zk1),App.Rotation(App.Vector(1,0,0),90))
App.ActiveDocument.recompute()

#importing, scaling and positioning tip aerofoils
importAirfoilDAT.insert(tipaerofoil,FreeCAD.ActiveDocument.Name)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(ck2,yk2,zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.ActiveDocument.getObject("DWire001").Placement = App.Placement(App.Vector(xk2,10917,zk2),App.Rotation(App.Vector(1,0,0),90))
App.ActiveDocument.recompute()

importAirfoilDAT.insert(tipaerofoil,FreeCAD.ActiveDocument.Name)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(ck2,yk2,zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.ActiveDocument.getObject("DWire002").Placement = App.Placement(App.Vector(xk2,-10917,zk2),App.Rotation(App.Vector(1,0,0),90))
App.ActiveDocument.recompute()

#lofting bewtween centre aerofoil to outer aerofoils
from FreeCAD import Base
import Part
App.ActiveDocument.addObject('Part::Loft','Loft8')
App.ActiveDocument.ActiveObject.Sections=[App.ActiveDocument.DWire, App.ActiveDocument.DWire001 ]
App.ActiveDocument.ActiveObject.Solid=True
App.ActiveDocument.ActiveObject.Ruled=False
App.ActiveDocument.ActiveObject.Closed=False
App.ActiveDocument.recompute()

App.ActiveDocument.addObject('Part::Loft','Loft9')
App.ActiveDocument.ActiveObject.Sections=[App.ActiveDocument.DWire, App.ActiveDocument.DWire002 ]
App.ActiveDocument.ActiveObject.Solid=True
App.ActiveDocument.ActiveObject.Ruled=False
App.ActiveDocument.ActiveObject.Closed=False
App.ActiveDocument.recompute()

'''
Creating the canards
'''
from FreeCAD import Base
import Part

importAirfoilDAT.insert(canardaerofoil,FreeCAD.ActiveDocument.Name)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(cb_c, cb_c, zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.getDocument("Skylon").DWire003.Placement=App.Placement(App.Vector(dc_x , dc_y, dc_z), App.Rotation(fuse_alpha, c_alpha, 90), App.Vector(0,0,0))
App.ActiveDocument.recompute()

importAirfoilDAT.insert(canardaerofoil,FreeCAD.ActiveDocument.Name)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(ct_c, ct_c, zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.getDocument("Skylon").DWire004.Placement=App.Placement(App.Vector(dc_x + cb_c, d_span, dc_z), App.Rotation(fuse_alpha, c_alpha, 90), App.Vector(0,0,0))
App.ActiveDocument.recompute()

importAirfoilDAT.insert(canardaerofoil,FreeCAD.ActiveDocument.Name)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(cb_c, cb_c, zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.getDocument("Skylon").DWire005.Placement=App.Placement(App.Vector(dc_x , -dc_y, -dc_z), App.Rotation(-fuse_alpha, c_alpha, 90), App.Vector(0,0,0))
App.ActiveDocument.recompute()

importAirfoilDAT.insert(canardaerofoil,FreeCAD.ActiveDocument.Name)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(ct_c, ct_c, zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.getDocument("Skylon").DWire006.Placement=App.Placement(App.Vector(dc_x + cb_c, -d_span, -dc_z), App.Rotation(-fuse_alpha, c_alpha, 90), App.Vector(0,0,0))
App.ActiveDocument.recompute()

App.getDocument('Skylon').addObject('Part::Loft','Loft10')
App.getDocument('Skylon').ActiveObject.Sections=[App.getDocument('Skylon').DWire003, App.getDocument('Skylon').DWire004, ]
App.getDocument('Skylon').ActiveObject.Solid=True
App.getDocument('Skylon').ActiveObject.Ruled=False
App.getDocument('Skylon').ActiveObject.Closed=True

App.getDocument('Skylon').addObject('Part::Loft','Loft11')
App.getDocument('Skylon').ActiveObject.Sections=[App.getDocument('Skylon').DWire005, App.getDocument('Skylon').DWire006, ]
App.getDocument('Skylon').ActiveObject.Solid=True
App.getDocument('Skylon').ActiveObject.Ruled=False
App.getDocument('Skylon').ActiveObject.Closed=True

App.activeDocument().recompute()

'''
creating tailfin
'''

from FreeCAD import Base
import Part

#importing, scaling and positioning aerofoils
importAirfoilDAT.insert(tailaerofoil,FreeCAD.ActiveDocument.Name)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(fch_b, fch_b, zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.ActiveDocument.getObject("DWire007").Placement = App.Placement(App.Vector(df_x, df_y, df_z - 20),App.Rotation(App.Vector(0,1,0),beta*15000))
App.ActiveDocument.recompute()

importAirfoilDAT.insert(tailaerofoil,FreeCAD.ActiveDocument.Name)
Draft.scale(App.ActiveDocument.ActiveObject,delta=App.Vector(fch_t, fch_t, zscale),center=App.Vector(0,0,0),legacy=True)
App.ActiveDocument.recompute()
App.ActiveDocument.getObject("DWire008").Placement = App.Placement(App.Vector(df_x + fch_b, df_y,df_z + fh),App.Rotation(App.Vector(0,0,0),0))
App.ActiveDocument.recompute()

App.getDocument('Skylon').addObject('Part::Loft','Loft12')
App.getDocument('Skylon').ActiveObject.Sections=[App.getDocument('Skylon').DWire007, App.getDocument('Skylon').DWire008, ]
App.getDocument('Skylon').ActiveObject.Solid=True
App.getDocument('Skylon').ActiveObject.Ruled=False
App.getDocument('Skylon').ActiveObject.Closed=True

App.ActiveDocument.recompute()

'''
Creating single entity for STL file
'''

App.activeDocument().addObject("Part::MultiFuse","Fusion")
App.activeDocument().Fusion.Shapes = [App.activeDocument().Loft8,App.activeDocument().Loft9,]
App.ActiveDocument.recompute()

App.activeDocument().addObject("Part::MultiFuse","Fusion001")
App.activeDocument().Fusion001.Shapes = [App.activeDocument().Fusion,App.activeDocument().Loft1,]
App.ActiveDocument.recompute()

App.activeDocument().addObject("Part::MultiFuse","Fusion002")
App.activeDocument().Fusion002.Shapes = [App.activeDocument().Fusion001,App.activeDocument().Loft2,]
App.ActiveDocument.recompute()

App.activeDocument().addObject("Part::MultiFuse","Fusion003")
App.activeDocument().Fusion003.Shapes = [App.activeDocument().Fusion002,App.activeDocument().Loft5,]
App.ActiveDocument.recompute()

App.activeDocument().addObject("Part::MultiFuse","Fusion004")
App.activeDocument().Fusion004.Shapes = [App.activeDocument().Fusion003,App.activeDocument().Loft12,]
App.ActiveDocument.recompute()

__objs__=[]
__objs__.append(FreeCAD.getDocument("Skylon").getObject("Fusion004"))
__objs__.append(FreeCAD.getDocument("Skylon").getObject("Loft10"))
__objs__.append(FreeCAD.getDocument("Skylon").getObject("Loft3"))
__objs__.append(FreeCAD.getDocument("Skylon").getObject("Loft4"))
__objs__.append(FreeCAD.getDocument("Skylon").getObject("Loft11"))
__objs__.append(FreeCAD.getDocument("Skylon").getObject("Loft6"))
__objs__.append(FreeCAD.getDocument("Skylon").getObject("Loft7"))

import Part
Part.export(__objs__,u"D:/University/Year 4/Dissertation/Skylon/skylongmsh1.brep")
Part.export(__objs__,u"D:/University/Year 4/Dissertation/Skylon/skylongmsh1.stl")

del __objs__

App.ActiveDocument.recompute()
