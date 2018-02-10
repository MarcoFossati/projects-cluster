#Boundary Temperatures
t0 = 288.15
t1 = 216.65
t2 = 196.65
t3 = 139.05
t4 = 270.65
t5 = 413.45
t6 = 356.65

#Boundary Pressures
p0 = 101325
p1 = 22632.06
p2 = 5474.889
p3 = 868.0187
p4 = 110.9063
p5 = 66.93887
p6 = 3.95642

#Constants
dt0 = -6.5
dt1 = 1
dt2 = 2.8
dt3 = -2.8
dt4 = -2
cp = 34.1632
e = 2.71828
R = 287.058
y = 1.4

#Input
qalt = float(raw_input('Enter Altitude (0 : 120km) > '))

#0 - 11 km
if qalt in range(0,11):
    temp = t0 + dt0*qalt
    press = p0*(t0/(t0 + dt0*qalt))**(cp/dt0)

#11 - 20 km
elif qalt in range(11,20):
    temp = t1
    press = p1*e**(-cp*(qalt-11)/t1)

elif qalt in range(20,32):
    temp = t2 + dt1*qalt
    press = p2*(t1/(t1+(qalt-20)))**(cp)

elif qalt in range(32,47):
    temp = t3 + dt2*qalt
    press = p3*(t1/(t1+dt2*(qalt-32)))**(cp/dt2)

elif qalt in range(47,51):
    temp = t4
    press = p4*e**(-cp*(qalt-47)/t4)

elif qalt in range(51,71):
    temp = t5 + dt3*qalt
    press = p5*(t4/(t4 + dt3*(qalt-51)))**(cp/dt3)

elif qalt >= 71 and qalt <= 86:
    temp = t6 + dt4*qalt
    press = p6*(214.65/(214.56+dt4*(qalt-71)))**(cp/dt4)

dens = press/(temp*R)
c = (y*R*temp)**0.5
visc =
kvisc =

print "\n\nAltitude:",alt,"km",'\n','-'*25,"\nTemperature:",temp,"K","\nPressure:",press,"Pa"" \
""\nDensity:",dens,"kg/m^3","\nSoS:",c,"m/s","\nViscosity:",visc,"Pas","\nK. Viscosity:",kvisc,"m^2/s",'\n','-'*25