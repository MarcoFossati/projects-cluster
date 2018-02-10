with open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Additional_Models\nhant.lsn","r") as searchfile:
    data1 = [x.strip().split() for x in searchfile.readlines()]

alt = float(raw_input('alt > '))

for i in range(11,82,1):
    if alt <= float(data1[i][2]):
        a=[data1[i][2]]
        b=[data1[i+1][2]]

for x, value in enumerate(a):
    alt_max = float(value)

for x, value in enumerate(b):
    alt_min = float(value)

print alt_max
print alt_min

for i in range(11,82,1):
    if alt_min == float(data1[i][2]):
        c = float(data1[i][3])