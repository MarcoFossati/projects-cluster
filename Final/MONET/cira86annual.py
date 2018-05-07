def datacall(halt,hem,lat):

    with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Additional_Models\shant.lsn","r") as searchfile:
        data1 = [x.strip().split() for x in searchfile.readlines()]

    with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Additional_Models\nhant.lsn","r") as searchfile:
        data2 = [x.strip().split() for x in searchfile.readlines()]

    with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Additional_Models\shanw.lsn","r") as searchfile:
        data3 = [x.strip().split() for x in searchfile.readlines()]

    with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Additional_Models\nhanw.lsn","r") as searchfile:
        data4 = [x.strip().split() for x in searchfile.readlines()]

    with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Additional_Models\twp.lsn","r") as searchfile:
        datap = [x.strip().split() for x in searchfile.readlines()]
    #Constants
    y = 1.4
    R = 287.058
    Re = 6356

    alt = (Re * halt) / (Re - halt)

    #Selecting min and max columns to use to interpolate for given latitude in southern hemisphere
    if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's' or hem == '-':
        mag = 'S'
        datat = data1
        dataw = data3
        latl = -0.2*lat + 19
        max_col = int(-0.2 * (int(float(lat)/2)*2) + 19)
        tap = (-0.2 * ((float(lat)/2)*2) + 19)
        if max_col > tap: #Anomaly with standard method when using specific values from tables e.g. 61, 60.4, 10.2, 65.2, 95.1, 106
            max_col = max_col - 1
        min_col = max_col + 1
        if lat == 0:
            min_col = 18
            max_col = 19

    elif hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n' or hem == '+':
        mag = 'N'
        datat = data2
        dataw = data4
        latl = 0.2*lat + 3
        min_col = int(0.2*(int(float(lat)/2)*2) + 3)
        hit = (0.2 * ((float(lat)/2)*2) + 3)
        if min_col > hit: # Same method and anomaly
            min_col = min_col - 1
        max_col = min_col + 1
        if lat == 80:
            min_col = 18
            max_col = 19

    if alt <= 119.7 and alt > 0.1:
        for i in range(11, 82, 1):
            if alt <= float(datat[i][2]):
                a = [datat[i][2]]
                b = [datat[i + 1][2]]

    elif alt <= 0.1:
        a = [datat[80][2]]
        b = [datat[81][2]]

    elif alt > 119.7 and alt <= 123:
        a = [datat[11][2]]
        b = [datat[12][2]]

    for x, value in enumerate(a):
        alt_max = float(value)

    for x, value in enumerate(b):
        alt_min = float(value)

    # Selecting min and max columns to use to interpolate for given latitude in northern hemisphere
    for i in range(11, 82, 1):
        if alt_min == float(datat[i][2]):
            min_temp_min = float(datat[i][min_col])
            min_wind_min = float(dataw[i][min_col])
        if alt_max == float(datat[i][2]):
            max_temp_min = float(datat[i][min_col])
            max_wind_min = float(dataw[i][min_col])
        if alt_min == float(datat[i][2]):
            min_temp_max = float(datat[i][max_col])
            min_wind_max = float(dataw[i][max_col])
        if alt_max == float(datat[i][2]):
            max_temp_max = float(datat[i][max_col])
            max_wind_max = float(dataw[i][max_col])


    temp_min = min_temp_min + ((max_temp_min - min_temp_min)*(alt - alt_min))/(alt_max - alt_min) #Temperature at minimum latitude
    temp_max = min_temp_max + ((max_temp_max - min_temp_max)*(alt - alt_min))/(alt_max - alt_min) #Temperature at maximum latitude
    temp = temp_min + ((temp_max - temp_min)*(latl - min_col))/(max_col - min_col)

    wind_min = min_wind_min + ((max_wind_min - min_wind_min)*(alt - alt_min))/(alt_max - alt_min)
    wind_max = min_wind_max + ((max_wind_max - min_wind_max)*(alt - alt_min))/(alt_max - alt_min)
    wind = wind_min + ((wind_max - wind_min)*(latl - min_col))/(max_col - min_col)

    if alt > 20:
        altp1 = -0.2*halt + 94
        altp4 = -0.2*halt + 385
        altp7 = -0.2*halt + 676
        altp10 = -0.2*halt + 967

        press_max1 = int(-0.2 * (int(float(halt)/2)*2) + 94)
        press_max4 = int(-0.2 * (int(float(halt)/2)*2) + 385)
        press_max7 = int(-0.2 * (int(float(halt)/2)*2) + 676)
        press_max10 = int(-0.2 * (int(float(halt)/2)*2) + 967)

        m = (-0.2 * ((float(halt) / 2) * 2) + 94)
        if press_max1 > m:  # Same method and anomaly
            press_max1 = press_max1 - 1

        q = (-0.2 * ((float(halt) / 2) * 2) + 385)
        if press_max4 > q:  # Same method and anomaly
            press_max4 = press_max4 - 1

        t = (-0.2 * ((float(halt) / 2) * 2) + 676)
        if press_max7 > t:  # Same method and anomaly
            press_max7 = press_max7 - 1

        w = (-0.2 * ((float(halt) / 2) * 2) + 967)
        if press_max10 > w:  # Same method and anomaly
            press_max10 = press_max10 - 1

        press_min1 = press_max1 + 1
        press_min4 = press_max4 + 1
        press_min7 = press_max7 + 1
        press_min10 = press_max10 + 1

        if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
            latl = -0.1 * lat + 9
            maxp_col = int(-0.1 * (int(float(lat) / 2) * 2) + 9)
            tap = (-0.1 * ((float(lat) / 2) * 2) + 9)
            if maxp_col > tap:  # Anomaly with standard method when using specific values from tables e.g. 61, 60.4, 10.2, 65.2, 95.1, 106
                maxp_col = maxp_col - 1
            minp_col = maxp_col + 1

        elif hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
            latl = 0.1 * lat + 9
            minp_col = int(0.1 * (int(float(lat) / 2) * 2) + 9)
            hit = (0.1 * ((float(lat) / 2) * 2) + 9)
            if minp_col > hit:  # Same method and anomaly
                minp_col = minp_col - 1
            maxp_col = minp_col + 1
            if lat == 80:
                minp_col = 16
                maxp_col = 17

        min_press_min1 = 100 * float(datap[press_min1][minp_col])*float(datap[press_min1][18])
        max_press_min1 = 100 * float(datap[press_max1][minp_col])*float(datap[press_max1][18])
        min_press_max1 = 100 * float(datap[press_min1][maxp_col])*float(datap[press_min1][18])
        max_press_max1 = 100 * float(datap[press_max1][maxp_col])*float(datap[press_max1][18])

        press_mina1 = min_press_min1 + ((max_press_min1 - min_press_min1)*(m - press_min1))/(press_max1 - press_min1)
        press_maxa1 = min_press_max1 + ((max_press_max1 - min_press_max1)*(m - press_min1))/(press_max1 - press_min1)
        press1 = press_mina1 + ((press_maxa1 - press_mina1)*(latl - minp_col))/(maxp_col - minp_col)

        min_press_min4 = 100 * float(datap[press_min4][minp_col])*float(datap[press_min4][18])
        max_press_min4 = 100 * float(datap[press_max4][minp_col])*float(datap[press_max4][18])
        min_press_max4 = 100 * float(datap[press_min4][maxp_col])*float(datap[press_min4][18])
        max_press_max4 = 100 * float(datap[press_max4][maxp_col])*float(datap[press_max4][18])

        press_mina4 = min_press_min4 + ((max_press_min4 - min_press_min4)*(q - press_min4))/(press_max4 - press_min4)
        press_maxa4 = min_press_max4 + ((max_press_max4 - min_press_max4)*(q - press_min4))/(press_max4 - press_min4)
        press4 = press_mina4 + ((press_maxa4 - press_mina4)*(latl - minp_col))/(maxp_col - minp_col)

        min_press_min7 = 100 * float(datap[press_min7][minp_col])*float(datap[press_min7][18])
        max_press_min7 = 100 * float(datap[press_max7][minp_col])*float(datap[press_max7][18])
        min_press_max7 = 100 * float(datap[press_min7][maxp_col])*float(datap[press_min7][18])
        max_press_max7 = 100 * float(datap[press_max7][maxp_col])*float(datap[press_max7][18])

        press_mina7 = min_press_min7 + ((max_press_min7 - min_press_min7)*(t - press_min7))/(press_max7 - press_min7)
        press_maxa7 = min_press_max7 + ((max_press_max7 - min_press_max7)*(t - press_min7))/(press_max7 - press_min7)
        press7 = press_mina7 + ((press_maxa7 - press_mina7)*(latl - minp_col))/(maxp_col - minp_col)

        min_press_min10 = 100 * float(datap[press_min10][minp_col]) * float(datap[press_min10][18])
        max_press_min10 = 100 * float(datap[press_max10][minp_col]) * float(datap[press_max10][18])
        min_press_max10 = 100 * float(datap[press_min10][maxp_col]) * float(datap[press_min10][18])
        max_press_max10 = 100 * float(datap[press_max10][maxp_col]) * float(datap[press_max10][18])

        press_mina10 = min_press_min10 + ((max_press_min10 - min_press_min10) * (w - press_min10)) / (press_max10 - press_min10)
        press_maxa10 = min_press_max10 + ((max_press_max10 - min_press_max10) * (w - press_min10)) / (press_max10 - press_min10)
        press10 = press_mina10 + ((press_maxa10 - press_mina10) * (latl - minp_col)) / (maxp_col - minp_col)

        press = (press1 + press4 + press7 + press10) / 4

        dens = round((press / (R * temp)),9)

    elif alt <= 20:
        press = 'N/A'
        dens = 'N/A'

    if alt > 86:
        print 'NOTE: [Density calculated as perfect gas may be inaccurate above 86km]\n'

    print "Altitude:",halt,"km","\nLatitude:",lat,mag,'\n','-'*25,"\nTemperature:",round(temp,2),"K","\nPressure:",press,"Pa"\
        "\nDensity:",dens,"kg/m3","\nZonal Wind Speed:",round(wind,2),"m/s\n",'-'*25,'\nCOSPAR INTERNATIONAL REFERENCE ATMOSPHERE, 1986 (Annual)'