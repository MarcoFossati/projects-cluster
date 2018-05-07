#Inputs
alt = float(raw_input('Geopotential Height (0 : 120km) > '))
hem = raw_input('Hemisphere (North : South) > ')
lat = float(raw_input('Latitude (0 : 80) > '))
mnt = raw_input('Month (Jan : Dec) > ')
print '\n\n'

if hem == '' and lat == '' and mnt == '':
    import