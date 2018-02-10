print "Enter Altitude (meters)"
alt = float(raw_input('> ')) #User inputs their desired altitude

if alt in range(0, 11000):
    temp = float(288.15 + (((216.65-288.15)*(alt-0)) / (11000-0))) #Interpolate linear temperature
    print "Temperature:", temp, "K"

    press = float(101.325 * (1-0.0065*(alt/288.15))**5.2561) #Equation taken from source (with proof)
    print "Pressure:", press, "kPa"

    dens = float(press / (0.278*temp)) #Perfect gas law to close equations
    print "Density:", dens, "kg/m^3" #Incorrect Density for some reason?

if alt not in range(0, 11000):
    print "Temperature: N/A" #Out of ISA range
