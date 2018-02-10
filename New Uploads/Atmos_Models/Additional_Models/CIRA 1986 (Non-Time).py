with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Additional_Models\shant.lsn","r") as searchfile:
    data1 = [x.strip().split() for x in searchfile.readlines()]

with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Additional_Models\nhant.lsn","r") as searchfile:
    data2 = [x.strip().split() for x in searchfile.readlines()]

with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Additional_Models\shanw.lsn","r") as searchfile:
    data3 = [x.strip().split() for x in searchfile.readlines()]

with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Additional_Models\nhanw.lsn","r") as searchfile:
    data4 = [x.strip().split() for x in searchfile.readlines()]

#Constants
y = 1.4
R = 287.058

#Inputs
alt = float(raw_input('GP Height (0 : 120km) >'))
hem = raw_input('Hemisphere (North : South) > ')
slat = float(raw_input('Latitude (0 : 80) > '))
lat = abs(slat)
div = slat / lat

#Selecting min and max columns to use to interpolate for given latitude in southern hemisphere
if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's' or hem == '-' or div == -1:
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

elif hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n' or hem == '+' or div == 1:
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

elif alt > 119.7 and alt <= 120:
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
wind_max = max_wind_min + ((max_wind_max - max_wind_min)*(alt - alt_min))/(alt_max - alt_min)
wind = wind_min + ((wind_max - wind_min)*(latl - min_col))/(max_col - min_col)

print "\n\nAltitude:",alt,"km","\nLatitude:",lat,mag,'\n','-'*25,"\nTemperature:",temp,"K","\nZonal Wind Speed:",wind,"m/s"