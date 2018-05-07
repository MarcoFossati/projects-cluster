#Inputs
alt = float(raw_input('Geopotential Altitude (0 : 120km) > '))

lat = raw_input('Latitude (-80 : 80) > ')

if list(lat) == True:
    if list(lat)[0] == '+':
        hem = 'North'
        lat = str(float(lat))

    elif abs(float(lat))/float(lat) != -1:
        hem = raw_input('Hemisphere (North : South) > ')
    else:
        hem = 'South'
        lat = str(abs(float(lat)))
else:
    hem = raw_input('Hemisphere (North : South) > ')
    if hem == '':
        hem = 'North'
mnt = raw_input('Month (Jan : Dec) > ')

print '\n\n'

if lat != '':
    lat = float(lat)

if 86 >= alt >= -2 and hem == 'North' and lat == '' and mnt == '':
    if 20 >= alt >= 0:
        import us7620
        us7620.datacall(alt)
    else:
        import us7686
        us7686.datacall(alt)

elif mnt == '':

    if hem == '' or hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if lat == '':
            hem = 'N'
            lat = 45 #Average of middle-latitude is 45 degrees, N (as opposed to S) selected to be consistent with U.S. 1976 model

    elif hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if lat == '':
            lat = 45 #Average of middle-latitude is 45 degrees

    import cira86annual
    cira86annual.datacall(alt, hem, lat)

elif mnt != '':
    if lat == '':
        lat = 45
        if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
            hem = 'S'
        else:
            hem = 'N'

    import cira86monthly
    cira86monthly.datacall(alt, hem, lat, mnt)