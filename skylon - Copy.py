#Author - Liam Watson
#created 11/11/2017
#updated 21/11/2017

from PySide import QtCore, QtGui
from PySide.QtGui import QLineEdit, QRadioButton
import FreeCAD, FreeCADGui, Draft
import math

App.newDocument("Skylon")
App.setActiveDocument("Skylon")
App.ActiveDocument = App.getDocument("Skylon")
Gui.ActiveDocument = Gui.getDocument("Skylon")

#define the radius of the fuselage at cargo bay
d_cargo = 6300
r_cargo = d_cargo/2
#define the length of the cargo bay
l_cargo = 28000
#define the length of the l_aircraft
l_aircraft = 83133
#define the maximum angle of attack at takeoff in degrees
a_takeoff = 10
#height of tail above horizontal datum
h_exhaust=(math.tan(math.radians(a_takeoff))*22000)/2
#radius of fuselage exhaust
r_exhaust_f = 250

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

"""
Creating the fuselage
"""
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
App.activeDocument().front_eng_vent1_l.Placement = App.Placement(App.Vector(d_front_datum_x - l_engine_body/2- l_front_vent, -d_from_datum_y, d_from_datum_z + h_front_eng_vent1),App.Rotation(App.Vector(0.00000,1.00000,0.00000),90 - a_front_eng), App.Vector(0,0,0))
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
