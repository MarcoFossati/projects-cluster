R = 0.287

print "Input Pressure (Pa):"
press = (raw_input('> '))
print "Input Temperature (K):"
temp = (raw_input('> '))
print "Input Density (kg/m^3):"
density = (raw_input('> '))

if press == "" and temp == "":
    print "Error: Not enough known variables"
    exit(0)

if density == "" and temp == "":
    print "Error: Not enough known variables"
    exit(0)

if press == "" and density == "":
    print "Error: Not enough known variables"
    exit(0)

if press == "":
    press = float(density) * R * float(temp)
    print "Pressure:", round(press, 2), "kPa"

if temp == "":
    temp = float(press) / (R * float(density))
    print "Temperature:", round(temp, 2), "K"

if density == "":
    density = float(press) / (R * float(temp))
    print "Density:", round(density, 5), "kg/m^3"
