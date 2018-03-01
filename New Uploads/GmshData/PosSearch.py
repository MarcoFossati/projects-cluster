with open(
        r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\Gmsh\2D_Globe\2D.pos",
        "r") as searchfile:
    pos_data = [x.strip().split() for x in searchfile.readlines()]

for i in range(1,len(pos_data)-2,1):
    a = pos_data[i][0]
    b = a.split('(')
    c = b[1].split(',')
    if b[0] == 'ST':
        d = c[8].strip().split('){')
        e = c[10].split('};')
        z = [float(c[0]), float(c[1]), float(c[2]), float(c[3]), float(c[4]),float(c[5]),float(c[6]),float(c[7]), float(d[0]), float(d[1]), float(c[9]), float(e[0])]
        print z
    elif b[0] == 'SP':
        d = c[2].split('){')
        e = d[1].split('};')
        #print "SP(%r,%r,%r){%r};" %(float(c[0]),float(c[1]),float(d[0]),float(e[0])) #Same format as before
        z = [float(c[0]),float(c[1]),float(d[0]),float(e[0])] #list format for actual data use
        print z
    elif b[0] == 'SL':
        d = c[5].split('){')
        e = c[6].split('};')
        z = [float(c[0]), float(c[1]),float(c[2]),float(c[3]),float(c[4]), float(d[0]),float(d[1]), float(e[0])]  # list format for actual data use
        print z