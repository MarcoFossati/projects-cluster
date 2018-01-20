# File location will need to be changed when downloaded
with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Model_1\si1py.prt", "r") as searchfile:
    data = [x.strip().split() for x in searchfile.readlines()]

qalt = float(raw_input('Enter Altitude (-2 : 86km) > '))

lnum = int(0.5 * qalt + 3)
flnum = (0.5 * qalt + 3)
lnum_min = int(0.5 * (int(float(qalt)/2)*2) + 3)
lnum_max = int(lnum_min + 1)
all_alts = [item[0] for item in data]

if data[lnum][0] == all_alts[lnum] and flnum == lnum_min:
    #Calling all values for tabulated alt values
    alt = float(data[lnum][0])
    sigma = float(data[lnum][1])
    delta = float(data[lnum][2])
    theta = float(data[lnum][3])
    temp = float(data[lnum][4])
    press = float(data[lnum][5])
    dens = float(data[lnum][6])
    c = float(data[lnum][7])
    visc = float(data[lnum][8])
    kvisc = float(data[lnum][9])

    print "\n\nAltitude:",alt,"km",'\n','-'*25,"\nSigma:",sigma,"\nDelta:",delta,"\nTheta:",theta,'\n','-'*25,\
    "\nTemperature:",temp,"K","\nPressure:",press,"Pa","\nDensity:",dens,"kg/m^3","\nSoS:",c,"m/s","\nViscosity:",visc,"Pas","\nK. Viscosity:",kvisc,"m^2/s"


if data[lnum][0] == all_alts[lnum] and flnum != lnum_min:
    #Find minimum values to interpolate from
    alt_min = float(data[lnum_min][0])
    sigma_min = float(data[lnum_min][1])
    delta_min = float(data[lnum_min][2])
    theta_min = float(data[lnum_min][3])
    temp_min = float(data[lnum_min][4])
    press_min = float(data[lnum_min][5])
    dens_min = float(data[lnum_min][6])
    c_min = float(data[lnum_min][7])
    visc_min = float(data[lnum_min][8])
    kvisc_min = float(data[lnum_min][9])

    #Find maximum values to interpolate from
    alt_max = float(data[lnum_max][0])
    sigma_max = float(data[lnum_max][1])
    delta_max = float(data[lnum_max][2])
    theta_max = float(data[lnum_max][3])
    temp_max = float(data[lnum_max][4])
    press_max = float(data[lnum_max][5])
    dens_max = float(data[lnum_max][6])
    c_max = float(data[lnum_max][7])
    visc_max = float(data[lnum_max][8])
    kvisc_max = float(data[lnum_max][9])

    #Interpolating values for alts not tabulated
    alt = qalt
    sigma = sigma_min + ((sigma_max - sigma_min) * (qalt - alt_min) / (alt_max - alt_min))
    delta = delta_min + ((delta_max - delta_min) * (qalt - alt_min) / (alt_max - alt_min))
    theta = theta_min + ((theta_max - theta_min) * (qalt - alt_min) / (alt_max - alt_min))
    temp = temp_min + ((temp_max - temp_min) * (qalt - alt_min) / (alt_max - alt_min))
    press = press_min + ((press_max - press_min) * (qalt - alt_min) / (alt_max - alt_min))
    dens = dens_min + ((dens_max - dens_min) * (qalt - alt_min) / (alt_max - alt_min))
    c = c_min + ((c_max - c_min) * (qalt - alt_min) / (alt_max - alt_min))
    visc = visc_min + ((visc_max - visc_min) * (qalt - alt_min) / (alt_max - alt_min))
    kvisc = kvisc_min + ((kvisc_max - kvisc_min) * (qalt - alt_min) / (alt_max - alt_min))

    print "\n\nAltitude:",alt,"km",'\n','-'*25,"\nSigma:",sigma,"\nDelta:",delta,"\nTheta:",theta,'\n','-'*25,\
    "\nTemperature:",temp,"K","\nPressure:",press,"Pa","\nDensity:",dens,"kg/m^3","\nSoS:",c,"m/s","\nViscosity:",visc,"Pas","\nK. Viscosity:",kvisc,"m^2/s"

#Lots of repeated processes
#Find way to implement user-defined functions to not have repeated lines