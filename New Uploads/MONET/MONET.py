#Inputs
alt = float(raw_input('Geopotential Height (0 : 120km) > '))
hem = raw_input('Hemisphere (North : South) > ')
enter_lat = raw_input('Latitude (0 : 80) > ')
mnt = raw_input('Month (Jan : Dec) > ')

print '\n\n'

if enter_lat != '':
    lat = float(enter_lat)

if 86 >= alt >= -2 and hem == '' and enter_lat == '' and mnt == '':
    if 20 >= alt >= 0:
        import us7620
        us7620.datacall(alt)
    else:
        import us7686
        us7686.datacall(alt)

elif alt > 86 and mnt == '':

    if hem == '' or hem == 'North' or hem == 'north' or hem == 'N' or hem == 'n':
        if enter_lat == None:
            hem = 'N'
            lat = 45 #Average of middle-latitude is 45 degrees, N (as opposed to S) selected to be consistent with U.S. 1976 model

    elif hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
        if enter_lat == None:
            lat = 45 #Average of middle-latitude is 45 degrees

    import cira86annual
    cira86annual.datacall(alt, hem, lat)

elif alt >= 20 and mnt == '':

    import cira86annual
    cira86annual.datacall(alt, hem, lat)

elif hem != None and enter_lat != None and mnt == None:

    import cira86annual
    cira86annual.datacall(alt, hem, lat)

elif mnt != '':
    if lat == None:
        lat = 45
        if hem == 'South' or hem == 'south' or hem == 'S' or hem == 's':
            hem = 'S'
        else:
            hem = 'N'
    import cira86monthly
    cira86monthly.datacall(alt, hem, lat, mnt)