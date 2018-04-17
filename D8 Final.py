# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 19:13:16 2017

@author: Alex
"""

from FreeCAD import Base
import Part
import importAirfoilDAT
import math
import FreeCAD, Draft

FreeCAD.newDocument("D8")

'''MESH SETTINGS'''
#MESH TYPE
# 1 = METFISTO
#2 = NETGEN
#0 = MAX SURFACE DEVIATION
mesh_type=0
#maximum surface deviation in mm
#Lower = finer. Be aware of computational cost increases for finer meshes.
#1mm was the lowest deviation used in testing
max_surf_dev = 100 
#max element edge length for METFISTO mesh in mm.
#Lower = finer. Be aware of computational cost increases for finer meshes.
#48mm edge length was the minimum used in testing
max_edge_length = 48  
#NETGEN
#fineness. Must be between 1 and 6.
mesh_quality = 4


'''
MODEL INPUTS
The following inputs are fundamental to the model generation.
All dimensions in mm unless otherwise stated
'''
'''operating conditions'''
#Cruise. lift coeff.
Clcr = 0.706
#Operating (cruise) Mach
Mcr = 0.74
#max take-off /angle (deg) (DEFINES REAR FUSELAGE ANGLE
#TO HORIZONTAL FOR GROUND CLEARANCE)
psi = 11

'''FUSELAGE'''
#fuselage length
Lf = 33000
#Fuselage width
Wf = 5300
#NOSE 
Ln = 0.2*Lf

'''WING'''
'''wing aerofoil data'''
wingaerofoil = str("C:/Users/Alex/Documents/University of strathclyde/4th year/me420 dissertation/airfoil dat file library/sc20714.dat")
#original thickness ratios
t_aero = 0.14
#position of max thickness %chord
c_tmax = 0.37
'''wing geometry'''
#wing positioning
x0 = 0.6*Lf #longitudinal (fore-aft)
#POSITION DATUMS
#Wing area
S = 108e6
#Aspect Ratio
AR = 24.85
#Span
b = pow(S*AR,0.5) #VERIFY ACCEPTABILITY OF SPAN FOR REQUIREMENTS
#Sweep
sweep_O = 12.6
#taper
taperWING = 0.4 #overall wing taper

'''TAIL'''
finaerofoil = str("C:/Users/Alex/Documents/University of strathclyde/4th year/me420 dissertation/airfoil dat file library/NACA0012.dat")
tf0 = 0.12 #original thickness ratio of fin aerofoil
ARht = 13
Sht = 18e6

'''
SECONDARY PARAMETERS
The following parameters can be specified independently or left as the given relations.
'''
'''FUSELAGE'''
#fuselage height
Hf = 0.7302*Wf
#cabin radius
R = Hf/2 #CONSTANT RELATION. GIVEN HERE TO ENSURE FUNCTIONALITY OF FURTHER CODE
#Y-POS
h0 = 0
top = h0 + 0.8*R
middle = 0
bottom = h0-0.8*R
y0 = bottom #vertical top = R, middle = 0, bottom = R
#FUSELAGE; NOSE, CABIN & REAR
#nose cone scale coeffs and no. sections
ayn = 0.05
ayn1 = 0.7
ayn2 = 0.95
 
azn = 0.2 
azn1 = 0.8
azn2 = 0.97

#rear fuselage scale and positioning coefficients
ayr = 0.07
ayr1 = 0.85
ayr2 = 0.6
ayr3 = 0.3

azr = 0.8

#NOSE y-offset relative to cabin datum
hn = 0.4*R
#CABIN 
Lcabin = 0.6*Lf
#REAR FUSELAGE 
Lrear = 0.2*Lf
if Ln + Lcabin + Lrear == Lf:
    print ("ACCEPTABLE VALUES")
else:
    print ("UNACCEPTABLE VALUES. ADJUST UNTIL FUSELAGE LENGTH CONDITION IS MET")


'''WINGS'''
#KINK POSITION
nkink = 0.4
#WING THIKNESS RATIO
t0 = t_aero
#Wingtip dihedral
dihedral = 5 #total, set to 0 if not required
AoAi = 2 #AoA at Clcr (take from aerofoil data)
#Twist
twist = 5 #total at wingtip, set to zero if not required
#kink taper
taperKINK = 0.6

'''TAIL'''
tailplaneaerofoil = str("C:/Users/Alex/Documents/University of strathclyde/4th year/me420 dissertation/airfoil dat file library/NACA25112.dat")
c_tmax_f = 0.3 #position along chord of max thickness
sweep_fin = 2*sweep_O
di_fin = 70 #relative to horizontal
sweep_tail = sweep_O
taper_fin = 0.7 # Range 0.6 - 0.7
taper_tail = taperWING
#tail height difference relative to rear fuselage, hrear
ht = b/10

'''
DEPENDENT PARAMETERS
FUSELAGE PARAMETER CALCULATIONS
'''
#X-POS
X0 = 0
#1/2 fuselage width
D = Wf/2
#centre separation (centre rectangle)
d = D - R
#fuselage x pos
Xcabin = X0 + Ln
print (Xcabin)
Xshell = Xcabin + Lcabin
Xbulkhead = Xshell - 1000
Xrear = Lf
Xcap1 = X0+6650
Xcap2 = Xrear+6600
tan_psi = math.tan(psi*(math.pi)/180)
#nose cone section x positions
Xn1 = X0 + 0.36*Ln
Xn2 = X0 + 0.8*Ln
#nose cone section heights
hn1 = h0 + 0.517*(hn)
hn2 = h0 + 0.125*(hn)
#rear fuselage section x pos
Nr = 4
dXr = Lrear/Nr
Xr1 = Xshell + dXr
Xr2 = Xshell + 2*dXr
Xr3 = Xshell + 3*dXr
#tail section scales
azr1 = 1 - (1-azr)*1/Nr
azr2 = 1 - (1-azr)*2/Nr
azr3 = 1 - (1-azr)*3/Nr
#rear fuselage section radii
R1 = ayr1*R
R2 = ayr2*R
R3 = ayr3*R
Rr = ayr*R
#rear fuselage section offsets from datum
hr1 = h0 - R + dXr*tan_psi + R1
hr2 = hr1 - R1 + 1.56*dXr*tan_psi + R2
hr3 = hr2 - R2 + 1.56*dXr*tan_psi + R3
hrear = hr3 - R3 + 2*dXr*tan_psi + Rr
'''
WING PARAMETER CALCULATIONS
'''
b0 = Wf #fuselage centreline - wing root
#sweep
sweep_I = 1.1*sweep_O #inner wing sweep
sweep_t_I = (math.tan(sweep_I*(math.pi)/180))
sweep_t_O = (math.tan(sweep_O*(math.pi)/180))
sweep_c = (math.cos(sweep_O*(math.pi)/180))
#twist per unit length for half span
eps = 2*twist/b
#Taper ratios
taperO = taperWING/taperKINK #outer
Clcreff = Clcr * sweep_c
Mcreff = Mcr*pow(sweep_c,0.5)
#tip/root thickness ratio
#wing z-pos relative to fuselage centre line
z0 = d
#chords
c0 = 2*b/(AR*((1-taperWING)*nkink+taperKINK+taperWING)) #root 
ck = taperKINK*c0 #kink
ct = taperO*ck #tip
#section coordinates
zk = nkink*b/2
zt = b/2
xk = x0 + (zk - z0)*sweep_t_I #kink
xt = xk + (zt - zk)*sweep_t_O #tip
yk = y0 #kink
yt = yk + (zt - zk)*(math.tan(dihedral*(math.pi)/180)) #tip
teff = t0/sweep_c 
y_scale_0 = teff/t_aero*c0
#effective kink thickness ratio
tk = 0.95*teff
y_scale_k = tk/t_aero*ck
#effective tip thickness ratio
tt = tk
y_scale_t = tt/t_aero*ct
#max thickness at %c
t_max = t0*c_tmax*c0

'''
TAIL PARAMETER CALCULATIONS
'''
#span
bht = pow(Sht*ARht,0.5)
#tail plane sweep
sweep_fin_t = math.tan(math.pi*sweep_fin/180)
sweep_tail_t = math.tan(math.pi*sweep_tail/180)
#thickness ratios
#FIN
tf = tf0 
tf1 = tf*0.95
tft = tf1*0.95
#TAIL-PLANE
thr = t0
tht = thr*0.95
#fin height
htail = hrear + ht

#fin pos
dxt = Xrear - Xr2
dxt2 = Xrear - Xbulkhead
dyt1 = hrear - hr2
dyt2 = (dyt1/dxt)*dxt2
dzt = (1-azr)*z0
ctf = pow(pow(dxt2,2)+pow(dyt2,2),0.5)
#max thickness at %c
t_max_f = tf*c_tmax_f*ctf
#tail chords
chtr = (2*bht/ARht)*1/(1+taper_tail)
chtt = chtr*taper_tail
#fin chords
ctft = chtr
ctf1 = chtr/taper_fin
hf1 = hrear + 0.5*ht
#fin pos
xfr = Xr3 + 650
xf1 = xfr + dxt2 + (hf1-hrear)*sweep_fin_t - ctf1
xft = xfr + dxt2 + ht*sweep_fin_t - ctft
yfr = hrear - 1.2*dyt2
zfr = b0/2 - 3.5*t_max_f
zf1 = b0/2
zft = zf1
zht = zft + 2*tft*ctft
zhtt = zft + 0.5*(bht-2*z0)

#fin root setting angle
theta_z = math.atan(dyt2/dxt2)*180/math.pi
theta_y = math.atan((zfr-0.99*azr*b0/2)/dxt2)*180/math.pi
#tail tip pos
xhtt = xft + zht*sweep_tail_t

#y-scales
y_scale_tf = tf/tf0*ctf
y_scale_tf1 = tf1/tf0*ctf1
y_scale_tft = tft/tf0*ctft
y_scale_htr = thr/t_aero*chtr
y_scale_htt = tht/t_aero*chtt


########################## FUSELAGE CONSTRUCTION ##############################
##NOSE SECTION
V1 = Base.Vector(Xcabin,h0 + R,-d)
V2 = Base.Vector(Xcabin,h0 + R,d)
V3 = Base.Vector(Xcabin,h0 - R,-d)
V4 = Base.Vector(Xcabin,h0 - R,d)
VC1 = Base.Vector(Xcabin,h0,-D)
VC2 = Base.Vector(Xcabin,h0,D)

#connecting points with LINES & ARCS
L1 = Part.Line(V1,V2)
L2 = Part.Line(V3,V4)
C1 = Part.Arc(V1,VC1,V3)
C2 = Part.Arc(V2,VC2,V4)


#converting lines into shape
S1 = Part.Shape([L1,L2,C1,C2])
W1 = Part.Wire(S1.Edges)
F1 = Part.Face(W1)
Part.show(F1)
FreeCAD.ActiveDocument.Shape.Placement = FreeCAD.Placement(FreeCAD.Vector(Xbulkhead,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))

Draft.clone(FreeCAD.ActiveDocument.Shape)
FreeCAD.ActiveDocument.getObject("Clone").Scale = (1.00, ayn, azn)
FreeCAD.ActiveDocument.Clone.Placement = FreeCAD.Placement(FreeCAD.Vector(X0,hn,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.recompute()
Draft.clone(FreeCAD.ActiveDocument.Shape)
FreeCAD.ActiveDocument.getObject("Clone001").Scale = (1.00, ayn1, azn1)
FreeCAD.ActiveDocument.Clone001.Placement = FreeCAD.Placement(FreeCAD.Vector(Xn1,hn1,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.recompute()
Draft.clone(FreeCAD.ActiveDocument.Shape)
FreeCAD.ActiveDocument.getObject("Clone002").Scale = (1.00, ayn2, azn2)
FreeCAD.ActiveDocument.Clone002.Placement = FreeCAD.Placement(FreeCAD.Vector(Xn2,hn2,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.recompute()
Draft.clone(FreeCAD.ActiveDocument.Shape)
FreeCAD.ActiveDocument.getObject("Clone003").Scale = (1.00, 1, 1)
FreeCAD.ActiveDocument.Clone003.Placement = FreeCAD.Placement(FreeCAD.Vector(Xcabin,h0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.recompute()

##FUSELAGE array
Draft.clone(FreeCAD.ActiveDocument.Shape)
FreeCAD.ActiveDocument.Clone004.Placement = FreeCAD.Placement(FreeCAD.Vector(Xshell,0,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.recompute()

##REAR FUSELAGE section
Draft.clone(FreeCAD.ActiveDocument.Shape)
FreeCAD.ActiveDocument.getObject("Clone005").Scale = (1.00, ayr1, azr1)
FreeCAD.ActiveDocument.Clone005.Placement = FreeCAD.Placement(FreeCAD.Vector(Xr1,hr1,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.recompute()
Draft.clone(FreeCAD.ActiveDocument.Shape)
FreeCAD.ActiveDocument.getObject("Clone006").Scale = (1.00, ayr2, azr2)
FreeCAD.ActiveDocument.Clone006.Placement = FreeCAD.Placement(FreeCAD.Vector(Xr2,hr2,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.recompute()
Draft.clone(FreeCAD.ActiveDocument.Shape)
FreeCAD.ActiveDocument.getObject("Clone007").Scale = (1.00, ayr3, azr3)
FreeCAD.ActiveDocument.Clone007.Placement = FreeCAD.Placement(FreeCAD.Vector(Xr3,hr3,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.recompute()
Draft.clone(FreeCAD.ActiveDocument.Shape)
FreeCAD.ActiveDocument.getObject("Clone008").Scale = (1.00, ayr, azr)
FreeCAD.ActiveDocument.Clone008.Placement = FreeCAD.Placement(FreeCAD.Vector(Xrear,hrear,0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.recompute()

##LOFT between all NOSE sections
FreeCAD.ActiveDocument.addObject('Part::Loft','NOSE_CONE_LOFT')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.Clone, FreeCAD.ActiveDocument.Clone001, FreeCAD.ActiveDocument.Clone002, FreeCAD.ActiveDocument.Clone003]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
FreeCAD.ActiveDocument.recompute()
#FUSELAGE LOFT
FreeCAD.ActiveDocument.addObject('Part::Loft','CABIN_LOFT')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.Clone003, FreeCAD.ActiveDocument.Shape]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
FreeCAD.ActiveDocument.recompute()
#REAR FUSELAGE LOFT
FreeCAD.ActiveDocument.addObject('Part::Loft','REAR_FUSELAGE_LOFT')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.Shape,FreeCAD.ActiveDocument.Clone004, FreeCAD.ActiveDocument.Clone005, FreeCAD.ActiveDocument.Clone006, FreeCAD.ActiveDocument.Clone007, FreeCAD.ActiveDocument.Clone008]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
FreeCAD.ActiveDocument.recompute()

#NOSE AND TAIL CAPS
#NOSE
FreeCAD.ActiveDocument.addObject("Part::Revolution","NOSE_CAP")
FreeCAD.ActiveDocument.NOSE_CAP.Source = FreeCAD.ActiveDocument.Clone
FreeCAD.ActiveDocument.NOSE_CAP.Axis = (0.00,0.00,1.00)
FreeCAD.ActiveDocument.NOSE_CAP.Base = (Xcap1,hn,0.00)
FreeCAD.ActiveDocument.NOSE_CAP.Angle = 180.00
FreeCAD.ActiveDocument.NOSE_CAP.Solid = True
FreeCAD.ActiveDocument.recompute()

#TAIL
FreeCAD.ActiveDocument.addObject("Part::Revolution","TAIL_CAP")
FreeCAD.ActiveDocument.TAIL_CAP.Source = FreeCAD.ActiveDocument.Clone008
FreeCAD.ActiveDocument.TAIL_CAP.Axis = (0.00,0.00,1.00)
FreeCAD.ActiveDocument.TAIL_CAP.Base = (Xcap2,hrear,0.00)
FreeCAD.ActiveDocument.TAIL_CAP.Angle = 180.00
FreeCAD.ActiveDocument.TAIL_CAP.Solid = True
FreeCAD.ActiveDocument.recompute()


#############################################################################

########################### WING CONSTRUCTION ###############################
##LEFT WING model code
##import root  aerofoil from library
importAirfoilDAT.insert(wingaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(c0,y_scale_0,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.getObject("BSpline").Placement = FreeCAD.Placement(FreeCAD.Vector(x0,y0,z0),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),-AoAi))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()

#RIGHT root aerofoil
__doc__=FreeCAD.ActiveDocument
__doc__.addObject("Part::Mirroring",'BSpline_R')
__doc__.ActiveObject.Source=__doc__.getObject("BSpline")
__doc__.ActiveObject.Label=u"BSpline_R"
__doc__.ActiveObject.Normal=(0,0,1)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__
FreeCAD.ActiveDocument.recompute()

##import kink  aerofoil from library
importAirfoilDAT.insert(wingaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(ck,y_scale_k,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.getObject("BSpline001").Placement = FreeCAD.Placement(FreeCAD.Vector(xk,yk,zk),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),-AoAi))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()

##import tip  aerofoil from library
importAirfoilDAT.insert(wingaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(ct,y_scale_t,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.getObject("BSpline002").Placement = FreeCAD.Placement(FreeCAD.Vector(xt,yt,zt),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),-AoAi))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()

#CENTRE section loft
FreeCAD.ActiveDocument.addObject('Part::Loft','Centre')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline_R, FreeCAD.ActiveDocument.BSpline ]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
FreeCAD.ActiveDocument.recompute()

FreeCAD.ActiveDocument.addObject('Part::Loft','L_Wing_I')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline, FreeCAD.ActiveDocument.BSpline001 ]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
FreeCAD.ActiveDocument.recompute()

FreeCAD.ActiveDocument.addObject('Part::Loft','L_Wing_O')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline001, FreeCAD.ActiveDocument.BSpline002 ]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
FreeCAD.ActiveDocument.recompute()


#RIGHT wing - mirror left
__doc__=FreeCAD.ActiveDocument
__doc__.addObject("Part::Mirroring", "R_wing_I")
__doc__.ActiveObject.Source=__doc__.getObject("L_Wing_I")
__doc__.ActiveObject.Label=u"R_wing_I"
__doc__.ActiveObject.Normal=(0,0,1)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__
FreeCAD.ActiveDocument.recompute()

__doc__=FreeCAD.ActiveDocument
__doc__.addObject("Part::Mirroring","R_wing_O")
__doc__.ActiveObject.Source=__doc__.getObject("L_Wing_O")
__doc__.ActiveObject.Label=u"R_wing_O"
__doc__.ActiveObject.Normal=(0,0,1)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__
FreeCAD.ActiveDocument.recompute()

#############################################################################
#TAIL AND FIN CONSTRUCTION
#IMPORT FIN ROOT AEROFOIL
importAirfoilDAT.insert(finaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(ctf,y_scale_tf,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.getObject("BSpline003").Placement = FreeCAD.Placement(FreeCAD.Vector(xfr,yfr,zfr),FreeCAD.Rotation(theta_z,theta_y,-di_fin),FreeCAD.Vector(0,0,1))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()
#IMPORT FIN KINK AEROFOIL
importAirfoilDAT.insert(finaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(ctf1,y_scale_tf1,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.recompute()
FreeCAD.ActiveDocument.getObject("BSpline004").Placement = FreeCAD.Placement(FreeCAD.Vector(xf1,hf1,zf1),FreeCAD.Rotation(0,0,-di_fin),FreeCAD.Vector(0,0,1))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()
#IMPORT FIN TIP AEROFOIL
importAirfoilDAT.insert(finaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(ctft,y_scale_tft,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.recompute()
FreeCAD.ActiveDocument.getObject("BSpline005").Placement = FreeCAD.Placement(FreeCAD.Vector(xft,htail,zft),FreeCAD.Rotation(0,0,90),FreeCAD.Vector(0,0,1))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()
#LOFT FIN
FreeCAD.ActiveDocument.addObject('Part::Loft','fin_root_kink_loft')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline004, FreeCAD.ActiveDocument.BSpline003, ]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
FreeCAD.ActiveDocument.addObject('Part::Loft','fin_kink_tip_loft')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline005,FreeCAD.ActiveDocument.BSpline004, ]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
FreeCAD.ActiveDocument.recompute()

#FUSE FIN LOFTS
FreeCAD.activeDocument().addObject("Part::MultiFuse","LEFT_FIN_FUSION")
FreeCAD.activeDocument().LEFT_FIN_FUSION.Shapes = [FreeCAD.activeDocument().fin_root_kink_loft,FreeCAD.activeDocument().fin_kink_tip_loft,]
FreeCAD.ActiveDocument.recompute()
#MIRROR FIN
__doc__=FreeCAD.ActiveDocument
__doc__.addObject("Part::Mirroring",'RIGHT_FIN_FUSION')
__doc__.ActiveObject.Source=__doc__.getObject("LEFT_FIN_FUSION")
__doc__.ActiveObject.Label=u"RIGHT_FIN_FUSION"
__doc__.ActiveObject.Normal=(0,0,1)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__
FreeCAD.ActiveDocument.recompute()

#horizontal tail
#left
importAirfoilDAT.insert(tailplaneaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(chtr,y_scale_htr,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.recompute()
FreeCAD.ActiveDocument.getObject("BSpline006").Placement = FreeCAD.Placement(FreeCAD.Vector(xft,htail,zht),FreeCAD.Rotation(0,0,0),FreeCAD.Vector(0,0,1))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()
#tip
importAirfoilDAT.insert(tailplaneaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(chtt,y_scale_htt,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.recompute()
FreeCAD.ActiveDocument.getObject("BSpline007").Placement = FreeCAD.Placement(FreeCAD.Vector(xhtt,htail,zhtt),FreeCAD.Rotation(0,0,0),FreeCAD.Vector(0,0,1))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()
#right
#MIRROR FIN
__doc__=FreeCAD.ActiveDocument
__doc__.addObject("Part::Mirroring",'BSpline_006_R')
__doc__.ActiveObject.Source=__doc__.getObject("BSpline006")
__doc__.ActiveObject.Label=u"BSpline_006_R"
__doc__.ActiveObject.Normal=(0,0,1)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__
FreeCAD.ActiveDocument.recompute()

#TAILPLANE LOFTS
#CENTRE
FreeCAD.ActiveDocument.addObject('Part::Loft','CENTRE_TAILPLANE')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline006, FreeCAD.ActiveDocument.BSpline_006_R, ]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
#OUTER
FreeCAD.ActiveDocument.addObject('Part::Loft','LEFT_OUTER_TAILPLANE')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline006,FreeCAD.ActiveDocument.BSpline007, ]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False

#MIRROR TAIL
__doc__=FreeCAD.ActiveDocument
__doc__.addObject("Part::Mirroring",'RIGHT_TAILPLANE_OUTER')
__doc__.ActiveObject.Source=__doc__.getObject("LEFT_OUTER_TAILPLANE")
__doc__.ActiveObject.Label=u"RIGHT_TAILPLANE_OUTER"
__doc__.ActiveObject.Normal=(0,0,1)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__
FreeCAD.ActiveDocument.recompute()
#
#AIRCRAFT LOFTS
FreeCAD.activeDocument().addObject("Part::MultiFuse","TAILPLANE_FUSION")
FreeCAD.activeDocument().TAILPLANE_FUSION.Shapes = [FreeCAD.activeDocument().RIGHT_TAILPLANE_OUTER,FreeCAD.activeDocument().CENTRE_TAILPLANE,FreeCAD.activeDocument().LEFT_OUTER_TAILPLANE,FreeCAD.activeDocument().RIGHT_FIN_FUSION,FreeCAD.activeDocument().LEFT_FIN_FUSION,FreeCAD.activeDocument().REAR_FUSELAGE_LOFT]
FreeCAD.ActiveDocument.recompute()
FreeCAD.activeDocument().addObject("Part::MultiFuse","CABIN_WING_FUSION")
FreeCAD.activeDocument().CABIN_WING_FUSION.Shapes = [FreeCAD.activeDocument().Centre,FreeCAD.activeDocument().L_Wing_I,FreeCAD.activeDocument().R_wing_I,FreeCAD.activeDocument().L_Wing_O,FreeCAD.activeDocument().R_wing_O,FreeCAD.activeDocument().CABIN_LOFT,]
FreeCAD.activeDocument().addObject("Part::MultiFuse","AIRCRAFT_FUSION")
FreeCAD.activeDocument().AIRCRAFT_FUSION.Shapes = [FreeCAD.activeDocument().NOSE_CONE_LOFT,FreeCAD.activeDocument().CABIN_WING_FUSION,FreeCAD.activeDocument().TAILPLANE_FUSION]
FreeCAD.ActiveDocument.recompute()
###############################################################
'''
exporting as an STL and STEP file
'''

__objs__=[]
__objs__.append(FreeCAD.ActiveDocument.getObject("AIRCRAFT_FUSION"))

import Part
Part.export(__objs__,u"C:/Users/Alex/Documents/University of strathclyde/4th year/me420 dissertation/freecad/D8.step")
Part.export(__objs__,u"C:/Users/Alex/Documents/University of strathclyde/4th year/me420 dissertation/freecad/D8.iges")
del __objs__
FreeCAD.ActiveDocument.recompute()

'''
creating mesh and exporting it
'''
import Mesh
import MeshPart


if mesh_type == 1: 
    __doc__=FreeCAD.ActiveDocument
    __mesh__=__doc__.addObject("Mesh::Feature","Mesh")
    __mesh__.Mesh=MeshPart.meshFromShape(Shape=__doc__.getObject("AIRCRAFT_FUSION").Shape,MaxLength=max_edge_length)
    __mesh__.Label="AIRCRAFT_FUSION (Meshed)"
    __mesh__.ViewObject.CreaseAngle=25.0
    del __doc__, __mesh__
    FreeCAD.ActiveDocument.recompute()
elif mesh_type == 2:
    __doc__=FreeCAD.getDocument("X34")
    __mesh__=__doc__.addObject("Mesh::Feature","Mesh")
    __mesh__.Mesh=MeshPart.meshFromShape(Shape=__doc__.getObject("Fusion002").Shape,Fineness=mesh_quality,SecondOrder=0,Optimize=1,AllowQuad=0)
    __mesh__.Label="Fusion002 (Meshed)"
    __mesh__.ViewObject.CreaseAngle=25.0
    del __doc__, __mesh__
else:
    __doc__=FreeCAD.ActiveDocument
    __mesh__=__doc__.addObject("Mesh::Feature","Mesh")
    __mesh__.Mesh=Mesh.Mesh(__doc__.getObject("AIRCRAFT_FUSION").Shape.tessellate(max_surf_dev))
    __mesh__.Label="AIRCRAFT_FUSION (Meshed)"
    __mesh__.ViewObject.CreaseAngle=25.0
    del __doc__, __mesh__
    FreeCAD.ActiveDocument.recompute()
FreeCAD.ActiveDocument.getObject("Mesh").Mesh.write("C:/Users/Alex/Documents/University of strathclyde/4th year/me420 dissertation/freecad/meshes/AIRCRAFT_FUSION (Meshed).stl","STL","AIRCRAFT_FUSION (Meshed)")
FreeCAD.ActiveDocument.recompute()





