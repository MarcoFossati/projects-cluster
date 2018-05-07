Dens = (raw_input('Density (kg/m^3): '))
Temp = (raw_input('Temperature (K): '))
Press = (raw_input('Pressure (Pa): '))
print " "
C_Air = float(287.058)

if Dens == '?':
    Dens = (float(Press) / (C_Air * float(Temp)))
    print "Density:", round(Dens, 3), "kg/m^3"

elif Temp == '?':
    Temp = (float(Press) / (float(Dens) * C_Air))
    print "Temperature:", round(Temp, 3), "K"

elif Press == '?':
    Press = (float(Dens) * C_Air * float(Temp))
    print "Pressure:", round(Press, 3), "Pa"