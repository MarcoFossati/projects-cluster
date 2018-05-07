def datacall(halt):

    # File location will need to be changed when downloaded
    with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Model_1\US76-86.prt", "r") as searchfile:
        data = [x.strip().split() for x in searchfile.readlines()]

    Re = 6356

    alt = (Re*halt)/(Re - halt)

    lnum_min = int(0.5 * alt + 3)

    if lnum_min > len(data)-2:
        lnum_min = lnum_min - 1

    lnum_max = int(lnum_min + 1)

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
    sigma = sigma_min + ((sigma_max - sigma_min) * (alt - alt_min) / (alt_max - alt_min))
    delta = delta_min + ((delta_max - delta_min) * (alt - alt_min) / (alt_max - alt_min))
    theta = theta_min + ((theta_max - theta_min) * (alt - alt_min) / (alt_max - alt_min))
    temp = temp_min + ((temp_max - temp_min) * (alt - alt_min) / (alt_max - alt_min))
    press = press_min + ((press_max - press_min) * (alt - alt_min) / (alt_max - alt_min))
    dens = dens_min + ((dens_max - dens_min) * (alt - alt_min) / (alt_max - alt_min))
    c = c_min + ((c_max - c_min) * (alt - alt_min) / (alt_max - alt_min))
    visc = visc_min + ((visc_max - visc_min) * (alt - alt_min) / (alt_max - alt_min))
    kvisc = kvisc_min + ((kvisc_max - kvisc_min) * (alt - alt_min) / (alt_max - alt_min))

    print "Altitude:",halt,"km",'\n','-'*25,"\nTemperature:",temp,"K","\nPressure:",press,"Pa"" \
    ""\nDensity:",dens,"kg/m3","\nSoS:",c,"m/s","\nD. Viscosity:",visc,"Pas","\nK. Viscosity:",kvisc,"m2/s\n",'-'*25, '\nU.S. STANDARD ATMOSPHERE, 1976'

    #Lots of repeated processes
    #Find way to implement user-defined functions to not have repeated lines