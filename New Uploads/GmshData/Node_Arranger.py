import operator

with open(
        r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\Gmsh\2D_Globe\2D.msh",
        "r") as searchfile:
    mesh = [x.strip().split() for x in searchfile.readlines()]

num = list()
for i in range(6,906,1):
    x = float(mesh[i][1])
    y = float(mesh[i][2])
    if y > (0.17632698*x) - 0.0001 and y <(0.17632698*x) + 0.0001 and y > 0:
        print mesh[i]
        a = float(mesh[i][0])
        b = float(mesh[i][1])
        c = float(mesh[i][2])
        d = float(mesh[i][3])
        little = list()
        little.append(a)
        little.append(b)
        little.append(c)
        little.append(d)
        num.append(little)

print '\n', num

print '\nNodes: ', len(num)

fixed = sorted(num, key = operator.itemgetter(1), reverse= True)

print '\n', fixed, '\n'

with open(
        r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Additional_Models\twp.lsn",
        "r") as searchfile:
    data = [x.strip().split() for x in searchfile.readlines()]

output = list()
for i in range(6,31,1):
    temp = float(data[i][8])
    mini = list(fixed[i-6])
    mini.append(temp)
    output.append(mini)

print '\n','Node No.     Mesh Co-Ordinates(x,y,z)     Temperature Value (K)','\n','-'*70

Data_2D = open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\GmshData\Data_2D.txt",'w')

for p in range(0,len(output)):
    print output[p]
    Data_2D.write(str(output[p]))
    Data_2D.write('\n')
print '\nNodes:', len(num)