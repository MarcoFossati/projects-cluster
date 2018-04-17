# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 20:09:30 2017

@author: wingc
"""
import FreeCAD, Draft, Part
import importAirfoilDAT
import math
from FreeCAD import Base
#
#
FreeCAD.newDocument("BWB")

'''MESH SETTINGS'''
#MESH TYPE
# 1 = NETGEN
#0 = MAX SURFACE DEVIATION
mesh_type=0
#NETGEN
#fineness. Must be between 1 and 6.
mesh_quality = 4
#maximum surface deviation in mm
#Lower = finer. Be aware of computational cost increases for finer meshes.
#1mm was the lowest deviation used in testing
max_surf_dev = 1 



'''
INPUTS
'''

'''WHOLE BWB'''
#sref area
S = 1091e6 #mm^2 Sized from MTOW, Clto, Vstall and air density
AR = 3.86
#whole BWB span
b = pow(AR*S,0.5)

'''CENTRE-BODY'''
CBW = 17800 #mm #CENTRE BODY width
bodysweep = 57.6 #BODYSWEEP ANGLE
cr = 39700 #centreline chord in mm. Used to define passenger and freight box volume. Define with Reynolds number and operating speed.
bodyaerofoil = str("C:/Users/Alex/Documents/University of strathclyde/4th year/me420 dissertation/airfoil dat file library/NACA25112.dat") #AEROFOIL SECTION
bodyorig = 0.12

tbody = 0.189 #CENTRELINE THICKNESS RATIO

'''WINGS'''
#LEADING EDGE SWEEP, optimum aft swept range: 35 <= wingsweep <= 45, upper limit 50
#forward swept range: max -40
wingsweep = 48 #WING SWEEP
taperWING = 0.2284 #outer wing taper. 
twist = 1.5 #tip twist angle
dihedral = 4.6 #define dihedral angle in degrees
wingaerofoil = str("C:/Users/Alex/Documents/University of strathclyde/4th year/me420 dissertation/airfoil dat file library/sc20714.dat") #AEROFOIL SECTION
wingorig = 0.14
ttip = 0.14 #TIP THICKNESS RATIO
nkink = 0.2857 #KINK aerofoil position FUNCTION OF OUTER WING SPAN BD

'''WINGLETS'''
ht = 0.235*b/2 #tail fin height as proportion of total span (defined later)
wingletsweep = 45
taper_winglet = 0.3
cant_winglet = 20
wingletdihedral = 90 - cant_winglet
wingletaerofoil = str("C:/Users/Alex/Documents/University of strathclyde/4th year/me420 dissertation/airfoil dat file library/NACA0012.dat")
wingletorig = 0.12
twinglet = 0.12


'''
CALCULATE DEPENDENT PARAMETERS
'''
#section sweep, coefficients
sweep01 = 0.305*bodysweep
#CENTREBODY SECTION POSITIONS AS FUNCTION OF CENTREBODY WIDTH
a1 = 0.1349 #SECTION 1
a2 = a1 + (1-a1)/5 #SECTION 2
a3 = a1+2*(1-a1)/5
a4 = a1+3*(1-a1)/5
a5 = a1 + 4*(1-a1)/5
#centre body
z0 = 0
z6 = CBW/2
z1 = a1*z6
z2 = a2*z6
z3 = a3*z6
z4 = a4*z6
z5 = a5*z6
#centre-body aft sweep
x1 = z1*(math.tan(sweep01*(math.pi)/180))
x2 = x1 + (z2-z1)*(math.tan(bodysweep*(math.pi)/180))
x3 = x1 + (z3-z1)*(math.tan(bodysweep*(math.pi)/180))
x4 = x1 + (z4-z1)*(math.tan(bodysweep*(math.pi)/180))
x5 = x1 + (z5-z1)*(math.tan(bodysweep*(math.pi)/180))
x6 = x1 + (z6-z1)*(math.tan(bodysweep*(math.pi)/180))
#taper coefficients 
a01 = 0.9975
a02 = 0.985
a03 = 0.97
a04 = 0.94
a05 = 0.9
a06 = 0.8533
#centre body tapers
taper01 = a01*(1 - x1/cr)
taper02 = a02*(1 - x2/cr)
taper03 = a03*(1 - x3/cr)
taper04 = a04*(1-x4/cr)
taper05 = a05*(1-x5/cr)
taperCB = a06*(1-x6/cr)


#additional winglet span as portion of total span
bwt = 2*ht/math.tan(wingletdihedral*(math.pi)/180)


#centre-body area
Scb = 1.04146*(CBW/2 * cr * (1+taperCB))
#wing
Swing = S - Scb # wing area
bw = b - CBW - bwt
ARwing = pow(bw,2)/Swing

#kink section
z7 = z6 + nkink*bw/2
zkblend = z6 + 0.5*(z7-z6)
#wing kink blend position
xkblend = x6 + (zkblend-z6)*(math.tan(wingsweep*(math.pi)/180))
ykblendpos = (zkblend-z6)*(math.tan(dihedral*(math.pi)/180)) + 400
#wink king pos
x7 = x6 + (z7-z6)*(math.tan(wingsweep*(math.pi)/180))
ypos7 = (z7-z6)*(math.tan(dihedral*(math.pi)/180)) + 400


#wing tip position
ztpos = z6 + bw/2
xtpos = x7 + (ztpos-z7)*(math.tan(wingsweep*(math.pi)/180))
ytpos = (ztpos-z6)*(math.tan(dihedral*(math.pi)/180)) + 400

#centre body
c1 = cr*taper01
c2 = cr*taper02
c3 = cr*taper03
c4 = cr*taper04
c5 = cr*taper05
c6 = cr*taperCB

if wingsweep<0:
    ct = taperWING*c6
    c7 = c6 + (ct-c6)/(ztpos-z6)*(z7-z6)
    ctw = 3*ct
    xtwpos = x2 + c2 - ctw
    ytwpos = 0
    ztwpos = z2
    ctwt = ctw*taper_winglet
    ytwtpos = ytwpos + ht
    ztwtpos = ztwpos + bwt/2
    xtwtpos = xtwpos + ht*math.tan(wingletsweep*(math.pi)/180)
    t_ytwt = twinglet
    ytwt = ctwt*(t_ytwt/wingletorig)
    taperKINK = c7/c6
else:
    ct = taperWING*c6
    F = 2*bw/(c6*ARwing)
    taperKINK = F - taperWING - nkink*(1-taperWING)
    c7 = taperKINK*c6
    taper7t = ct/c7
    ##wing - tip blend
    zblendpos = ztpos + 300
    xblendpos = xtpos + (zblendpos-ztpos)*(math.tan(wingsweep*(math.pi)/180))
#    yblendpos = (zblendpos-z6)*(math.tan(dihedral*(math.pi)/180)) + 400
    yblendpos = ytpos+ttip/2*ct*((math.cos(dihedral*(math.pi)/180))-(math.cos(wingletdihedral*(math.pi)/180)))
    #blend
    cblend = ct
    ytwpos = ytpos + ht
    ztwpos = ztpos + bwt/2
    xtwpos = xtpos + ht*(math.tan(wingletsweep*(math.pi)/180))
    ctw = ct*taper_winglet
ckblend = c6 + (c7-c6)/(z7-z6)*(zkblend-z6)

taperKINK_limit = 0.3
taperWING_limit = (taperKINK_limit+nkink-(2*bw/(c6*ARwing)))/(nkink-1)
bw_limit = 80000 - CBW - bwt
ARwing_limit = pow(bw_limit,2)/Swing
Scbmax = 0.55*S
CBWlimit = 1.0562*S/(cr*(1+taperCB))
if b>80000:
    print("WARNING. EXCESSIVE SPAN. REDUCE ASPECT RATIO","span", b,"wing aspect ratio", ARwing,"wing aspect ratio limit", ARwing_limit )
#    exit()
else:
    print ("ACCEPTABLE SPAN","span", b,"wing aspect ratio", ARwing,"wing aspect ratio limit", ARwing_limit)
    
if taperKINK<taperKINK_limit:
    print("OVER-TAPERED KINK REGION. REDUCE ASPECT RATIO OR INCREASE taperWING","taperKINK",taperKINK,"taperWING",taperWING,"taperWING_limit",taperWING_limit)
#    exit()
else:
    print("ACCEPTABLE KINK REGION TAPER","taperKINK",taperKINK,"taperWING",taperWING,"taperWING_limit",taperWING_limit)

if Scb>0.55*S:
    print("EXCESSIVE CENTRE-BODY AREA. REDUCE CENTRE-BODY WIDTH","Scb",Scb,"Scb max", Scbmax,"CBW limit",CBWlimit)
else:
    print("ACCEPTABLE CENTRE-BODY AREA", "Scb",Scb,"Scb max",Scbmax)

print("BWB area",S,"centre-body area",Scb,"wing area",Swing,"whole BWB aspect ratio",AR)
print("BWB span",b,"centre-body width",CBW,"outer wing span",bw,"additional winglet span",bwt)
print("chords",cr,c1,c2,c3,c4,c5,c6,c7,ct,ctw)
print("spanwise positions",z1,z2,z3,z4,z5,z6,z7,ztpos,ztwpos)



#section twist
#SECTION THICKNESS RATIOS
dt = taper01*tbody-ttip
t1 = taper01*tbody
t2 = t1 - dt/(ztpos-z1)*(z2-z1)
t3 = t1 - dt/(ztpos-z1)*(z3-z1)
t4 = t1 - dt/(ztpos-z1)*(z4-z1)
t5 = t1 - dt/(ztpos-z1)*(z5-z1)
t6 = t1 - dt/(ztpos-z1)*(z6-z1)
tkblend = t6 - (t6-ttip)/(z7-z6)*(zkblend-z6)
t7 = ttip
#tblend = ttip
#Y SCALE FACTORS
ybody = cr*(tbody/bodyorig)
y1 = t1/bodyorig * c1
y2 = t2/bodyorig * c2
y3 = t3/bodyorig * c3
y4 = t4/bodyorig * c4
y5 = t5/bodyorig * c5
y6 = t6/bodyorig * c6
ykblend = tkblend/wingorig * ckblend
y7 = t7/wingorig * c7
yt = ct*(ttip/wingorig)
yblend = yt
ytw = ctw*(twinglet/wingletorig)



#import centre body (root) aerofoil data
importAirfoilDAT.insert(bodyaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(cr,ybody,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()

##import kink (outer centrebody) aerofoil from library
#####1
importAirfoilDAT.insert(bodyaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(c1,y1,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.getObject("BSpline001").Placement = FreeCAD.Placement(FreeCAD.Vector(x1,0,z1),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()

#####2
importAirfoilDAT.insert(bodyaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(c2,y2,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.getObject("BSpline002").Placement = FreeCAD.Placement(FreeCAD.Vector(x2,0,z2),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()

__doc__=FreeCAD.ActiveDocument
__doc__.addObject("Part::Mirroring", 'BSpline001_R')
__doc__.ActiveObject.Source=__doc__.getObject("BSpline001")
__doc__.ActiveObject.Label=u"BSpline001_R"
__doc__.ActiveObject.Normal=(0,0,1)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__
__doc__=FreeCAD.ActiveDocument
__doc__.addObject("Part::Mirroring", 'BSpline002_R')
__doc__.ActiveObject.Source=__doc__.getObject("BSpline002")
__doc__.ActiveObject.Label=u"BSpline002_R"
__doc__.ActiveObject.Normal=(0,0,1)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__


###3 start of outer wing
importAirfoilDAT.insert(bodyaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(c3,y3,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.getObject("BSpline003").Placement = FreeCAD.Placement(FreeCAD.Vector(x3,0,z3),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()

#####4
importAirfoilDAT.insert(bodyaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(c4,y4,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.getObject("BSpline004").Placement = FreeCAD.Placement(FreeCAD.Vector(x4,0,z4),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()

##5
importAirfoilDAT.insert(bodyaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(c5,y5,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.getObject("BSpline005").Placement = FreeCAD.Placement(FreeCAD.Vector(x5,0,z5),FreeCAD.Rotation(FreeCAD.Vector(0,0,1),0))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()


##6
importAirfoilDAT.insert(bodyaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(c6,y6,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.getObject("BSpline006").Placement = FreeCAD.Placement(FreeCAD.Vector(x6,0,z6),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-dihedral))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()


#OUTBOARD WING SECTIONS
##kblend
importAirfoilDAT.insert(wingaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(ckblend,ykblend,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.getObject("BSpline007").Placement = FreeCAD.Placement(FreeCAD.Vector(xkblend,ykblendpos,zkblend),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-dihedral))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()

##7
importAirfoilDAT.insert(wingaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(c7,y7,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.getObject("BSpline008").Placement = FreeCAD.Placement(FreeCAD.Vector(x7,ypos7,z7),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-dihedral))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()


##tip
importAirfoilDAT.insert(wingaerofoil,FreeCAD.ActiveDocument.Name)
points = FreeCAD.ActiveDocument.ActiveObject.Points
Draft.makeBSpline(points, closed=True)
Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(ct,yt,0),center=FreeCAD.Vector(0,0,0),legacy=True)
FreeCAD.ActiveDocument.getObject("BSpline009").Placement = FreeCAD.Placement(FreeCAD.Vector(xtpos,ytpos,ztpos),FreeCAD.Rotation(-twist,0,-dihedral),FreeCAD.Vector(0,0,1))
FreeCAD.ActiveDocument.removeObject("DWire")
FreeCAD.ActiveDocument.recompute()

'''loft bewtween surfaces'''
#LEFT WING
FreeCAD.ActiveDocument.addObject('Part::Loft','CENTREBODY_1')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline002_R,FreeCAD.ActiveDocument.BSpline001_R,FreeCAD.ActiveDocument.BSpline,FreeCAD.ActiveDocument.BSpline001,FreeCAD.ActiveDocument.BSpline002 ]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
FreeCAD.ActiveDocument.recompute()
#
FreeCAD.ActiveDocument.addObject('Part::Loft','CENTREBODY_2_L')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline002,FreeCAD.ActiveDocument.BSpline003,FreeCAD.ActiveDocument.BSpline004,FreeCAD.ActiveDocument.BSpline005,FreeCAD.ActiveDocument.BSpline006 ]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
FreeCAD.ActiveDocument.recompute()
#
FreeCAD.ActiveDocument.addObject('Part::Loft','INNER_WING_1_L')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline006,FreeCAD.ActiveDocument.BSpline007]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
FreeCAD.ActiveDocument.recompute()
FreeCAD.ActiveDocument.addObject('Part::Loft','INNER_WING_2_L')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline007,FreeCAD.ActiveDocument.BSpline008]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
FreeCAD.ActiveDocument.recompute()
#
FreeCAD.ActiveDocument.addObject('Part::Loft','OUTER_WING_L')
FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline008,FreeCAD.ActiveDocument.BSpline009]
FreeCAD.ActiveDocument.ActiveObject.Solid=True
FreeCAD.ActiveDocument.ActiveObject.Ruled=False
FreeCAD.ActiveDocument.ActiveObject.Closed=False
FreeCAD.ActiveDocument.recompute()


if wingsweep<0:
    importAirfoilDAT.insert(wingletaerofoil,FreeCAD.ActiveDocument.Name)
    points = FreeCAD.ActiveDocument.ActiveObject.Points
    Draft.makeBSpline(points, closed=True)
    Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(ctw,ytw,0),center=FreeCAD.Vector(0,0,0),legacy=True)
    FreeCAD.ActiveDocument.getObject("BSpline010").Placement = FreeCAD.Placement(FreeCAD.Vector(xtwpos,ytwpos,ztwpos),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-wingletdihedral))
    FreeCAD.ActiveDocument.removeObject("DWire")
    FreeCAD.ActiveDocument.recompute()
    #
    importAirfoilDAT.insert(wingletaerofoil,FreeCAD.ActiveDocument.Name)
    points = FreeCAD.ActiveDocument.ActiveObject.Points
    Draft.makeBSpline(points, closed=True)
    Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(ctwt,ytwt,0),center=FreeCAD.Vector(0,0,0),legacy=True)
    FreeCAD.ActiveDocument.getObject("BSpline011").Placement = FreeCAD.Placement(FreeCAD.Vector(xtwtpos,ytwtpos,ztwtpos),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-wingletdihedral))
    FreeCAD.ActiveDocument.removeObject("DWire")
    FreeCAD.ActiveDocument.recompute()
    #
    FreeCAD.ActiveDocument.addObject('Part::Loft','LEFT_WINGLET')
    FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline010, FreeCAD.ActiveDocument.BSpline011]
    FreeCAD.ActiveDocument.ActiveObject.Solid=True
    FreeCAD.ActiveDocument.ActiveObject.Ruled=False
    FreeCAD.ActiveDocument.ActiveObject.Closed=False
    FreeCAD.ActiveDocument.recompute()
else:
    ##blend L
    importAirfoilDAT.insert(wingletaerofoil,FreeCAD.ActiveDocument.Name)
    points = FreeCAD.ActiveDocument.ActiveObject.Points
    Draft.makeBSpline(points, closed=True)
    Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(cblend,yblend,0),center=FreeCAD.Vector(0,0,0),legacy=True)
    FreeCAD.ActiveDocument.getObject("BSpline010").Placement = FreeCAD.Placement(FreeCAD.Vector(xblendpos,yblendpos,zblendpos),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-wingletdihedral))
    FreeCAD.ActiveDocument.removeObject("DWire")
    FreeCAD.ActiveDocument.recompute()
    #winglet tip L
    importAirfoilDAT.insert(wingletaerofoil,FreeCAD.ActiveDocument.Name)
    points = FreeCAD.ActiveDocument.ActiveObject.Points
    Draft.makeBSpline(points, closed=True)
    Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(ctw,ytw,0),center=FreeCAD.Vector(0,0,0),legacy=True)
    FreeCAD.ActiveDocument.getObject("BSpline011").Placement = FreeCAD.Placement(FreeCAD.Vector(xtwpos,ytwpos,ztwpos),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),-wingletdihedral))
    FreeCAD.ActiveDocument.removeObject("DWire")
    FreeCAD.ActiveDocument.recompute()
    ##tip R
    importAirfoilDAT.insert(wingaerofoil,FreeCAD.ActiveDocument.Name)
    points = FreeCAD.ActiveDocument.ActiveObject.Points
    Draft.makeBSpline(points, closed=True)
    Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(ct,yt,0),center=FreeCAD.Vector(0,0,0),legacy=True)
    FreeCAD.ActiveDocument.getObject("BSpline012").Placement = FreeCAD.Placement(FreeCAD.Vector(xtpos,ytpos,-ztpos),FreeCAD.Rotation(-twist,0,dihedral),FreeCAD.Vector(0,0,1))
    FreeCAD.ActiveDocument.removeObject("DWire")
    FreeCAD.ActiveDocument.recompute()
    ##blend R
    importAirfoilDAT.insert(wingletaerofoil,FreeCAD.ActiveDocument.Name)
    points = FreeCAD.ActiveDocument.ActiveObject.Points
    Draft.makeBSpline(points, closed=True)
    Draft.scale(FreeCAD.ActiveDocument.ActiveObject,delta=FreeCAD.Vector(cblend,yblend,0),center=FreeCAD.Vector(0,0,0),legacy=True)
    FreeCAD.ActiveDocument.getObject("BSpline013").Placement = FreeCAD.Placement(FreeCAD.Vector(xblendpos,yblendpos,-zblendpos),FreeCAD.Rotation(FreeCAD.Vector(1,0,0),wingletdihedral))
    FreeCAD.ActiveDocument.removeObject("DWire")
    FreeCAD.ActiveDocument.recompute()
    #WING TIP BLEND AND WINGLET LOFTS
    FreeCAD.ActiveDocument.addObject('Part::Loft','WING_TIP_BLEND_L')
    FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline009,FreeCAD.ActiveDocument.BSpline010]
    FreeCAD.ActiveDocument.ActiveObject.Solid=True
    FreeCAD.ActiveDocument.ActiveObject.Ruled=False
    FreeCAD.ActiveDocument.ActiveObject.Closed=False
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.ActiveDocument.recompute()
    #
    FreeCAD.ActiveDocument.addObject('Part::Loft','WING_TIP_BLEND_R')
    FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline012,FreeCAD.ActiveDocument.BSpline013]
    FreeCAD.ActiveDocument.ActiveObject.Solid=True
    FreeCAD.ActiveDocument.ActiveObject.Ruled=False
    FreeCAD.ActiveDocument.ActiveObject.Closed=False
    FreeCAD.ActiveDocument.recompute()
    #
    FreeCAD.ActiveDocument.addObject('Part::Loft','LEFT_WINGLET')
    FreeCAD.ActiveDocument.ActiveObject.Sections=[FreeCAD.ActiveDocument.BSpline010, FreeCAD.ActiveDocument.BSpline011]
    FreeCAD.ActiveDocument.ActiveObject.Solid=True
    FreeCAD.ActiveDocument.ActiveObject.Ruled=False
    FreeCAD.ActiveDocument.ActiveObject.Closed=False
    FreeCAD.ActiveDocument.recompute()

    
'''MIRROR PARTS FOR RIGHT WING'''
__doc__=FreeCAD.ActiveDocument
__doc__.addObject("Part::Mirroring", 'RIGHT_WINGLET')
__doc__.ActiveObject.Source=__doc__.getObject("LEFT_WINGLET")
__doc__.ActiveObject.Label=u"RIGHT_WINGLET"
__doc__.ActiveObject.Normal=(0,0,1)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__
__doc__=FreeCAD.ActiveDocument
__doc__.addObject("Part::Mirroring", 'CENTREBODY_2_R')
__doc__.ActiveObject.Source=__doc__.getObject("CENTREBODY_2_L")
__doc__.ActiveObject.Label=u"CENTREBODY_R"
__doc__.ActiveObject.Normal=(0,0,1)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__
__doc__=FreeCAD.ActiveDocument
__doc__.addObject("Part::Mirroring", 'INNER_WING_1_R')
__doc__.ActiveObject.Source=__doc__.getObject("INNER_WING_1_L")
__doc__.ActiveObject.Label=u"INNER_WING_R"
__doc__.ActiveObject.Normal=(0,0,1)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__
__doc__=FreeCAD.ActiveDocument
__doc__.addObject("Part::Mirroring", 'INNER_WING_2_R')
__doc__.ActiveObject.Source=__doc__.getObject("INNER_WING_2_L")
__doc__.ActiveObject.Label=u"INNER_WING_R"
__doc__.ActiveObject.Normal=(0,0,1)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__

__doc__=FreeCAD.ActiveDocument
__doc__.addObject("Part::Mirroring",'OUTER_WING_R')
__doc__.ActiveObject.Source=__doc__.getObject("OUTER_WING_L")
__doc__.ActiveObject.Label=u"OUTER_WING_R"
__doc__.ActiveObject.Normal=(0,0,1)
__doc__.ActiveObject.Base=(0,0,0)
del __doc__

FreeCAD.activeDocument().addObject("Part::Compound","Compound")
FreeCAD.activeDocument().Compound.Links = [FreeCAD.activeDocument().OUTER_WING_L,FreeCAD.activeDocument().OUTER_WING_R,FreeCAD.activeDocument().INNER_WING_2_L,FreeCAD.activeDocument().INNER_WING_2_R,FreeCAD.activeDocument().INNER_WING_1_L,FreeCAD.activeDocument().INNER_WING_1_R,FreeCAD.activeDocument().CENTREBODY_2_L,FreeCAD.activeDocument().CENTREBODY_2_R,FreeCAD.activeDocument().LEFT_WINGLET,FreeCAD.activeDocument().RIGHT_WINGLET,FreeCAD.activeDocument().WING_TIP_BLEND_R,FreeCAD.activeDocument().WING_TIP_BLEND_L,FreeCAD.activeDocument().CENTREBODY_1,]
FreeCAD.ActiveDocument.recompute()

'''
exporting as an STL and STEP file
'''

__objs__=[]
__objs__.append(FreeCAD.ActiveDocument.getObject("Compound"))

import Part
Part.export(__objs__,u"C:/Users/Alex/Documents/University of strathclyde/4th year/me420 dissertation/freecad/BWB.step")
Part.export(__objs__,u"C:/Users/Alex/Documents/University of strathclyde/4th year/me420 dissertation/freecad/BWB.iges")
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
    __mesh__.Mesh=MeshPart.meshFromShape(Shape=__doc__.getObject("Compound").Shape,Fineness=mesh_quality,SecondOrder=0,Optimize=1,AllowQuad=0)
    __mesh__.Label="Compound (Meshed)"
    __mesh__.ViewObject.CreaseAngle=25.0
    del __doc__, __mesh__
else:
    __doc__=FreeCAD.ActiveDocument
    __mesh__=__doc__.addObject("Mesh::Feature","Mesh")
    __mesh__.Mesh=Mesh.Mesh(__doc__.getObject("Compound").Shape.tessellate(max_surf_dev))
    __mesh__.Label="Compound (Meshed)"
    __mesh__.ViewObject.CreaseAngle=25.0
    del __doc__, __mesh__


FreeCAD.ActiveDocument.getObject("Mesh").Mesh.write("C:/Users/Alex/Documents/University of strathclyde/4th year/me420 dissertation/freecad/meshes/BWB mesh.stl","STL","Compound (Meshed)")
FreeCAD.ActiveDocument.recompute()

