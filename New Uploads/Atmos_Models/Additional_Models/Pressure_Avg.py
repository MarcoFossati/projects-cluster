def presscalc(alt):

    with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Additional_Models\twp.lsn","r") as searchfile:
        datap = [x.strip().split() for x in searchfile.readlines()]

    altp1 = -0.2*alt + 94
    altp4 = -0.2*alt + 385
    altp7 = -0.2*alt + 676
    altp10 = -0.2*alt + 967

    press_max1 = int(-0.2 * (int(float(alt)/2)*2) + 94)
    press_max4 = int(-0.2 * (int(float(alt)/2)*2) + 385)
    press_max7 = int(-0.2 * (int(float(alt)/2)*2) + 676)
    press_max10 = int(-0.2 * (int(float(alt)/2)*2) + 967)

    m = (-0.2 * ((float(alt) / 2) * 2) + 94)
    if press_max1 > m:  # Same method and anomaly
        press_max1 = press_max1 - 1

    q = (-0.2 * ((float(alt) / 2) * 2) + 385)
    if press_max4 > q:  # Same method and anomaly
        press_max4 = press_max4 - 1

    t = (-0.2 * ((float(alt) / 2) * 2) + 676)
    if press_max7 > t:  # Same method and anomaly
        press_max7 = press_max7 - 1

    w = (-0.2 * ((float(alt) / 2) * 2) + 967)
    if press_max10 > w:  # Same method and anomaly
        press_max10 = press_max10 - 1

    press_min1 = press_max1 + 1
    press_min4 = press_max4 + 1
    press_min7 = press_max7 + 1
    press_min10 = press_max10 + 1

    min_press_min1 = 100 * float(datap[press_min1][min_col])*float(datap[press_min1][18])
    max_press_min1 = 100 * float(datap[press_max1][min_col])*float(datap[press_max1][18])
    min_press_max1 = 100 * float(datap[press_min1][max_col])*float(datap[press_min1][18])
    max_press_max1 = 100 * float(datap[press_max1][max_col])*float(datap[press_max1][18])

    press_mina1 = min_press_min1 + ((max_press_min1 - min_press_min1)*(altp - press_min1))/(press_max1 - press_min1)
    press_maxa1 = max_press_min1 + ((max_press_max1 - max_press_min1)*(altp - press_min1))/(press_max1 - press_min1)
    press1 = press_mina1 + ((press_maxa1 - press_mina1)*(latl - min_col))/(max_col - min_col)

    min_press_min4 = 100 * float(datap[press_min4][min_col])*float(datap[press_min4][18])
    max_press_min4 = 100 * float(datap[press_max4][min_col])*float(datap[press_max4][18])
    min_press_max4 = 100 * float(datap[press_min4][max_col])*float(datap[press_min4][18])
    max_press_max4 = 100 * float(datap[press_max4][max_col])*float(datap[press_max4][18])

    press_mina4 = min_press_min4 + ((max_press_min4 - min_press_min4)*(altp - press_min4))/(press_max4 - press_min4)
    press_maxa4 = max_press_min4 + ((max_press_max4 - max_press_min4)*(altp - press_min4))/(press_max4 - press_min4)
    press4 = press_mina4 + ((press_maxa4 - press_mina4)*(latl - min_col))/(max_col - min_col)

    min_press_min7 = 100 * float(datap[press_min7][min_col])*float(datap[press_min7][18])
    max_press_min7 = 100 * float(datap[press_max7][min_col])*float(datap[press_max7][18])
    min_press_max7 = 100 * float(datap[press_min7][max_col])*float(datap[press_min7][18])
    max_press_max7 = 100 * float(datap[press_max7][max_col])*float(datap[press_max7][18])

    press_mina7 = min_press_min7 + ((max_press_min7 - min_press_min7)*(altp - press_min7))/(press_max7 - press_min7)
    press_maxa7 = max_press_min7 + ((max_press_max7 - max_press_min7)*(altp - press_min7))/(press_max7 - press_min7)
    press7 = press_mina7 + ((press_maxa7 - press_mina7)*(latl - min_col))/(max_col - min_col)

    min_press_min10 = 100 * float(datap[press_min10][min_col]) * float(datap[press_min10][18])
    max_press_min10 = 100 * float(datap[press_max10][min_col]) * float(datap[press_max10][18])
    min_press_max10 = 100 * float(datap[press_min10][max_col]) * float(datap[press_min10][18])
    max_press_max10 = 100 * float(datap[press_max10][max_col]) * float(datap[press_max10][18])

    press_mina10 = min_press_min10 + ((max_press_min10 - min_press_min10) * (altp - press_min10)) / (press_max10 - press_min10)
    press_maxa10 = max_press_min10 + ((max_press_max10 - max_press_min10) * (altp - press_min10)) / (press_max10 - press_min10)
    press10 = press_mina10 + ((press_maxa10 - press_mina10) * (latl - min_col)) / (max_col - min_col)

    press = (press1 + press4 + press7 + press10) / 4