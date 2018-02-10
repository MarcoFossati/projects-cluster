print "Enter Altitude (meters)"
alt = float(raw_input('> '))

if alt in range(0,11000):
    btmT = 288.15
    topT = 216.65
    btmA = 0
    topA = 11000

elif alt in range(11000, 20000):
    temp = 216.65
    print "Temperature:", temp, "K"

elif alt in range(20000, 32000):
    btmT = 216.65
    topT = 228.65
    btmA = 2000
    topA = 32000

elif alt in range(32000, 47000):
    btmT = 228.65
    topT = 270.65
    btmA = 32200
    topA = 47300

elif alt in range(47000, 51000):
    temp = 270.65
    print "Temperature:", temp, "K"

elif alt in range(51000, 71000):
    btmT = 270.65
    topT = 214.65
    btmA = 51000
    topA = 71000

elif alt in range(71000, 85000):
    btmT = 214.65
    topT = 186.95
    btmA = 71000
    topA = 85000

if alt < 85000 and not alt in range(11000, 20000) and not alt in range(47000, 51000):
    temp = float(btmT + ((topT - btmT) * (alt - btmA) / (topA - btmA)))
    print "Temperature:", round(temp, 2), "K"

elif alt >= 85000:
    print "Error: alt >= 85000"
    exit(0)

if alt < 11000:
    press = float(101.3*(temp/288.08)**5.256) #Change pressure values and calculations?
    print "Pressure:",round(press, 2), "kPa"

elif alt in range(11000, 25000):
    press = float(22.65 * 2.71828**(1.73-0.000157*alt))
    print "Pressure:", round(press, 2), "kPa"

elif alt >= 25000:
    press = float(2.488*(temp/216.6)**(-11.388))
    print "Pressure:", round(press, 2), "kPa"

dens = press / (temp * 0.287)
print "Density:", round(dens, 5), "kg/m^3"

sound = (1.4 * 287 * temp)**0.5
print "Speed of Sound:", round(sound, 2), "m/s"

dyn_visc = ((0.000001458)*temp**1.5)/(temp+110.4)
print "Dynamic Viscosity:", round(dyn_visc, 7), "kg/ms"