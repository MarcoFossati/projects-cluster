#File location will need to be changed when downloaded
with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Model_2\twp.lsn", "r") as searchfile:
    data = [x.strip().split() for x in searchfile.readlines()]

qalt = float(raw_input('Enter Altitude (0 : 120km) > '))
lat = float(raw_input('Enter Latitude (0 : 80) > '))
hem = raw_input('Enter Hemisphere (N/S) > ')
mnt = raw_input('Enter Month (Jan : Dec) > ')

#January
if mnt == 'January' or mnt == 'january' or mnt == 'jan' or mnt == 'Jan':
    temp_line_start = 30
    wind_line_start = 62
    press_line_start = 94
    grad = qalt/(-5)
    temp_line = int(grad + temp_line_start)
    wind_line = int(grad + wind_line_start)
    press_line = int(grad + press_line_start)
    if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if lat == 80:
            col = 1
        if lat == 70:
            col = 2
        if lat == 60:
            col = 3
        if lat == 50:
            col = 4
        if lat == 40:
            col = 5
        if lat == 30:
            col = 6
        if lat == 20:
            col = 7
        if lat == 10:
            col = 8
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if lat == 10:
            col = 10
        if lat == 20:
            col = 11
        if lat == 30:
            col = 12
        if lat == 40:
            col = 13
        if lat == 50:
            col = 14
        if lat == 60:
            col = 15
        if lat == 70:
            col = 16
        if lat == 80:
            col = 17
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == '' or hem == 'equator' or hem == 'Equator' or hem == '0' or hem == 'N/A' or hem == 'n/a':
        col = 9
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press

#February
if mnt == 'February' or mnt == 'february' or mnt =='feb' or mnt == 'Feb':
    temp_line_start = 127
    wind_line_start = 159
    press_line_start = 191
    grad = qalt/(-5)
    temp_line = int(grad + temp_line_start)
    wind_line = int(grad + wind_line_start)
    press_line = int(grad + press_line_start)
    if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if lat == 80:
            col = 1
        if lat == 70:
            col = 2
        if lat == 60:
            col = 3
        if lat == 50:
            col = 4
        if lat == 40:
            col = 5
        if lat == 30:
            col = 6
        if lat == 20:
            col = 7
        if lat == 10:
            col = 8
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if lat == 10:
            col = 10
        if lat == 20:
            col = 11
        if lat == 30:
            col = 12
        if lat == 40:
            col = 13
        if lat == 50:
            col = 14
        if lat == 60:
            col = 15
        if lat == 70:
            col = 16
        if lat == 80:
            col = 17
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == '' or hem == 'equator' or hem == 'Equator' or hem == '0' or hem == 'N/A' or hem == 'n/a':
        col = 9
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press

#March
if mnt == 'March' or mnt == 'march' or mnt =='mar' or mnt == 'Mar':
    temp_line_start = 224
    wind_line_start = 256
    press_line_start = 288
    grad = qalt/(-5)
    temp_line = int(grad + temp_line_start)
    wind_line = int(grad + wind_line_start)
    press_line = int(grad + press_line_start)
    if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if lat == 80:
            col = 1
        if lat == 70:
            col = 2
        if lat == 60:
            col = 3
        if lat == 50:
            col = 4
        if lat == 40:
            col = 5
        if lat == 30:
            col = 6
        if lat == 20:
            col = 7
        if lat == 10:
            col = 8
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if lat == 10:
            col = 10
        if lat == 20:
            col = 11
        if lat == 30:
            col = 12
        if lat == 40:
            col = 13
        if lat == 50:
            col = 14
        if lat == 60:
            col = 15
        if lat == 70:
            col = 16
        if lat == 80:
            col = 17
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == '' or hem == 'equator' or hem == 'Equator' or hem == '0' or hem == 'N/A' or hem == 'n/a':
        col = 9
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press

#April
if mnt == 'April' or mnt == 'april' or mnt =='apr' or mnt == 'Apr':
    temp_line_start = 321
    wind_line_start = 353
    press_line_start = 385
    grad = qalt/(-5)
    temp_line = int(grad + temp_line_start)
    wind_line = int(grad + wind_line_start)
    press_line = int(grad + press_line_start)
    if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if lat == 80:
            col = 1
        if lat == 70:
            col = 2
        if lat == 60:
            col = 3
        if lat == 50:
            col = 4
        if lat == 40:
            col = 5
        if lat == 30:
            col = 6
        if lat == 20:
            col = 7
        if lat == 10:
            col = 8
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if lat == 10:
            col = 10
        if lat == 20:
            col = 11
        if lat == 30:
            col = 12
        if lat == 40:
            col = 13
        if lat == 50:
            col = 14
        if lat == 60:
            col = 15
        if lat == 70:
            col = 16
        if lat == 80:
            col = 17
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == '' or hem == 'equator' or hem == 'Equator' or hem == '0' or hem == 'N/A' or hem == 'n/a':
        col = 9
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press

#May
if mnt == 'May' or mnt == 'may':
    temp_line_start = 418
    wind_line_start = 450
    press_line_start = 482
    grad = qalt/(-5)
    temp_line = int(grad + temp_line_start)
    wind_line = int(grad + wind_line_start)
    press_line = int(grad + press_line_start)
    if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if lat == 80:
            col = 1
        if lat == 70:
            col = 2
        if lat == 60:
            col = 3
        if lat == 50:
            col = 4
        if lat == 40:
            col = 5
        if lat == 30:
            col = 6
        if lat == 20:
            col = 7
        if lat == 10:
            col = 8
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if lat == 10:
            col = 10
        if lat == 20:
            col = 11
        if lat == 30:
            col = 12
        if lat == 40:
            col = 13
        if lat == 50:
            col = 14
        if lat == 60:
            col = 15
        if lat == 70:
            col = 16
        if lat == 80:
            col = 17
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == '' or hem == 'equator' or hem == 'Equator' or hem == '0' or hem == 'N/A' or hem == 'n/a':
        col = 9
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press

#June
if mnt == 'June' or mnt == 'june' or mnt == 'Jun' or mnt == 'jun':
    temp_line_start = 515
    wind_line_start = 547
    press_line_start = 579
    grad = qalt/(-5)
    temp_line = int(grad + temp_line_start)
    wind_line = int(grad + wind_line_start)
    press_line = int(grad + press_line_start)
    if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if lat == 80:
            col = 1
        if lat == 70:
            col = 2
        if lat == 60:
            col = 3
        if lat == 50:
            col = 4
        if lat == 40:
            col = 5
        if lat == 30:
            col = 6
        if lat == 20:
            col = 7
        if lat == 10:
            col = 8
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if lat == 10:
            col = 10
        if lat == 20:
            col = 11
        if lat == 30:
            col = 12
        if lat == 40:
            col = 13
        if lat == 50:
            col = 14
        if lat == 60:
            col = 15
        if lat == 70:
            col = 16
        if lat == 80:
            col = 17
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == '' or hem == 'equator' or hem == 'Equator' or hem == '0' or hem == 'N/A' or hem == 'n/a':
        col = 9
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press

#July
if mnt == 'July' or mnt == 'july' or mnt == 'Jul' or mnt == 'jul':
    temp_line_start = 612
    wind_line_start = 644
    press_line_start = 676
    grad = qalt/(-5)
    temp_line = int(grad + temp_line_start)
    wind_line = int(grad + wind_line_start)
    press_line = int(grad + press_line_start)
    if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if lat == 80:
            col = 1
        if lat == 70:
            col = 2
        if lat == 60:
            col = 3
        if lat == 50:
            col = 4
        if lat == 40:
            col = 5
        if lat == 30:
            col = 6
        if lat == 20:
            col = 7
        if lat == 10:
            col = 8
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if lat == 10:
            col = 10
        if lat == 20:
            col = 11
        if lat == 30:
            col = 12
        if lat == 40:
            col = 13
        if lat == 50:
            col = 14
        if lat == 60:
            col = 15
        if lat == 70:
            col = 16
        if lat == 80:
            col = 17
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == '' or hem == 'equator' or hem == 'Equator' or hem == '0' or hem == 'N/A' or hem == 'n/a':
        col = 9
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press

#August
if mnt == 'August' or mnt == 'august' or mnt == 'Aug' or mnt == 'aug':
    temp_line_start = 709
    wind_line_start = 741
    press_line_start = 773
    grad = qalt/(-5)
    temp_line = int(grad + temp_line_start)
    wind_line = int(grad + wind_line_start)
    press_line = int(grad + press_line_start)
    if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if lat == 80:
            col = 1
        if lat == 70:
            col = 2
        if lat == 60:
            col = 3
        if lat == 50:
            col = 4
        if lat == 40:
            col = 5
        if lat == 30:
            col = 6
        if lat == 20:
            col = 7
        if lat == 10:
            col = 8
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if lat == 10:
            col = 10
        if lat == 20:
            col = 11
        if lat == 30:
            col = 12
        if lat == 40:
            col = 13
        if lat == 50:
            col = 14
        if lat == 60:
            col = 15
        if lat == 70:
            col = 16
        if lat == 80:
            col = 17
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == '' or hem == 'equator' or hem == 'Equator' or hem == '0' or hem == 'N/A' or hem == 'n/a':
        col = 9
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press

#September
if mnt == 'September' or mnt == 'september' or mnt == 'Sep' or mnt == 'sep':
    temp_line_start = 806
    wind_line_start = 838
    press_line_start = 870
    grad = qalt/(-5)
    temp_line = int(grad + temp_line_start)
    wind_line = int(grad + wind_line_start)
    press_line = int(grad + press_line_start)
    if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if lat == 80:
            col = 1
        if lat == 70:
            col = 2
        if lat == 60:
            col = 3
        if lat == 50:
            col = 4
        if lat == 40:
            col = 5
        if lat == 30:
            col = 6
        if lat == 20:
            col = 7
        if lat == 10:
            col = 8
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if lat == 10:
            col = 10
        if lat == 20:
            col = 11
        if lat == 30:
            col = 12
        if lat == 40:
            col = 13
        if lat == 50:
            col = 14
        if lat == 60:
            col = 15
        if lat == 70:
            col = 16
        if lat == 80:
            col = 17
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == '' or hem == 'equator' or hem == 'Equator' or hem == '0' or hem == 'N/A' or hem == 'n/a':
        col = 9
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press

#October
if mnt == 'October' or mnt == 'october' or mnt == 'oct' or mnt == 'Oct':
    temp_line_start = 903
    wind_line_start = 935
    press_line_start = 967
    grad = qalt/(-5)
    temp_line = int(grad + temp_line_start)
    wind_line = int(grad + wind_line_start)
    press_line = int(grad + press_line_start)
    if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if lat == 80:
            col = 1
        if lat == 70:
            col = 2
        if lat == 60:
            col = 3
        if lat == 50:
            col = 4
        if lat == 40:
            col = 5
        if lat == 30:
            col = 6
        if lat == 20:
            col = 7
        if lat == 10:
            col = 8
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if lat == 10:
            col = 10
        if lat == 20:
            col = 11
        if lat == 30:
            col = 12
        if lat == 40:
            col = 13
        if lat == 50:
            col = 14
        if lat == 60:
            col = 15
        if lat == 70:
            col = 16
        if lat == 80:
            col = 17
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == '' or hem == 'equator' or hem == 'Equator' or hem == '0' or hem == 'N/A' or hem == 'n/a':
        col = 9
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press

#November
if mnt == 'November' or mnt == 'november' or mnt == 'Nov' or mnt == 'nov':
    temp_line_start = 1000
    wind_line_start = 1032
    press_line_start = 1064
    grad = qalt/(-5)
    temp_line = int(grad + temp_line_start)
    wind_line = int(grad + wind_line_start)
    press_line = int(grad + press_line_start)
    if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if lat == 80:
            col = 1
        if lat == 70:
            col = 2
        if lat == 60:
            col = 3
        if lat == 50:
            col = 4
        if lat == 40:
            col = 5
        if lat == 30:
            col = 6
        if lat == 20:
            col = 7
        if lat == 10:
            col = 8
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if lat == 10:
            col = 10
        if lat == 20:
            col = 11
        if lat == 30:
            col = 12
        if lat == 40:
            col = 13
        if lat == 50:
            col = 14
        if lat == 60:
            col = 15
        if lat == 70:
            col = 16
        if lat == 80:
            col = 17
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == '' or hem == 'equator' or hem == 'Equator' or hem == '0' or hem == 'N/A' or hem == 'n/a':
        col = 9
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press

#December
if mnt == 'December' or mnt == 'december' or mnt == 'Dec' or mnt == 'dec':
    temp_line_start = 1097
    wind_line_start = 1129
    press_line_start = 1161
    grad = qalt/(-5)
    temp_line = int(grad + temp_line_start)
    wind_line = int(grad + wind_line_start)
    press_line = int(grad + press_line_start)
    if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if lat == 80:
            col = 1
        if lat == 70:
            col = 2
        if lat == 60:
            col = 3
        if lat == 50:
            col = 4
        if lat == 40:
            col = 5
        if lat == 30:
            col = 6
        if lat == 20:
            col = 7
        if lat == 10:
            col = 8
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if lat == 10:
            col = 10
        if lat == 20:
            col = 11
        if lat == 30:
            col = 12
        if lat == 40:
            col = 13
        if lat == 50:
            col = 14
        if lat == 60:
            col = 15
        if lat == 70:
            col = 16
        if lat == 80:
            col = 17
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press
    if hem == '' or hem == 'equator' or hem == 'Equator' or hem == '0' or hem == 'N/A' or hem == 'n/a':
        col = 9
        temp = data[temp_line][col]
        wind = data[wind_line][col]
        press = data[press_line][col]
        print temp
        print wind
        print press