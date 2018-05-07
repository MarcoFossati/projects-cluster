with open(
        r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\Gmsh\2D_Globe\2D.pos",
        "r") as searchfile:
    pos_data = [x.strip().split() for x in searchfile.readlines()]

with open(
        r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\GmshData\Temp_July.txt",
        "r") as searchfile:
    temp_data = [x.strip().split() for x in searchfile.readlines()]

pos_list = list()

for i in range(1,len(pos_data)-2,1):
    a = pos_data[i][0]
    b = a.split('(')
    c = b[1].split(',')

    if b[0] == 'ST':
        d = c[8].strip().split('){')
        e = c[10].split('};')
        z = [float(c[0]), float(c[1]), float(c[2]), float(c[3]), float(c[4]),float(c[5]),float(c[6]),float(c[7]), float(d[0]), float(d[1]), float(c[9]), float(e[0])]
        pos_list.append(z)

    elif b[0] == 'SP':
        d = c[2].split('){')
        e = d[1].split('};')
        #print "SP(%r,%r,%r){%r};" %(float(c[0]),float(c[1]),float(d[0]),float(e[0])) #Same format as before
        z = [float(c[0]),float(c[1]),float(d[0]),float(e[0])] #list format for actual data use
        pos_list.append(z)

    elif b[0] == 'SL':
        d = c[5].split('){')
        e = c[6].split('};')
        z = [float(c[0]), float(c[1]),float(c[2]),float(c[3]),float(c[4]), float(d[0]),float(d[1]), float(e[0])]  # list format for actual data use
        pos_list.append(z)

#for i in range(0,len(pos_list),1):
#    print pos_list[i]

#print '\n',len(pos_list),'/',len(pos_data)-3,'lines\n'

#for i in range(0,len(temp_data),1):
#    print temp_data[i]

for i in range(0,len(pos_list),1):
    for m in range(0,len(temp_data),1):
        if len(pos_list[i]) > 0:
            if float(pos_list[i][0]) < float(temp_data[m][1]) + 0.01 and float(pos_list[i][0]) > float(temp_data[m][1]) - 0.01 and float(pos_list[i][1]) < float(temp_data[m][2]) + 0.01 and float(pos_list[i][1]) > float(temp_data[m][2]) - 0.01:
                #print float(pos_list[i][0]),float(pos_list[i][1]),'and',float(temp_data[m][1]),float(temp_data[m][2]),'      .1','     ',[i],[m]
                if len(pos_list[i]) == 4:
                    pos_list[i][3] = float(temp_data[m][4])
                elif len(pos_list[i]) == 8:
                    pos_list[i][6] = float(temp_data[m][4])
                elif len(pos_list[i]) == 12:
                    pos_list[i][9] = float(temp_data[m][4])
        if len(pos_list[i]) >= 6:
            if float(pos_list[i][3]) < float(temp_data[m][1]) + 0.01 and float(pos_list[i][3]) > float(temp_data[m][1]) - 0.01 and float(pos_list[i][4]) < float(temp_data[m][2]) + 0.01 and float(pos_list[i][4]) > float(temp_data[m][2]) - 0.01:
                #print float(pos_list[i][3]), float(pos_list[i][4]), 'and', float(temp_data[m][1]), float(temp_data[m][2]),'      .2','     ',[i],[m]
                if len(pos_list[i]) == 8:
                    pos_list[i][7] = float(temp_data[m][4])
                elif len(pos_list[i]) == 12:
                    pos_list[i][10] = float(temp_data[m][4])
        if len(pos_list[i]) >= 9:
            if float(pos_list[i][6]) < float(temp_data[m][1]) + 0.01 and float(pos_list[i][6]) > float(temp_data[m][1]) - 0.01 and float(pos_list[i][7]) < float(temp_data[m][2]) + 0.01 and float(pos_list[i][7]) > float(temp_data[m][2]) - 0.01:
                #print float(pos_list[i][6]), float(pos_list[i][7]), 'and', float(temp_data[m][1]), float(temp_data[m][2]),'      .3','     ',[i],[m]
                if len(pos_list[i]) == 12:
                    pos_list[i][11] = float(temp_data[m][4])

print 'View "Temperature (K)" {'
for g in range(0,len(pos_list),1):
    if len(pos_list[g]) == 4:
        print 'SP(%r,%r,%r){%r};' %(pos_list[g][0],pos_list[g][1],pos_list[g][2],pos_list[g][3])
    if len(pos_list[g]) == 8:
        print 'SL(%r,%r,%r,%r,%r,%r){%r,%r};' %(pos_list[g][0],pos_list[g][1],pos_list[g][2],pos_list[g][3],pos_list[g][4],pos_list[g][5],pos_list[g][6],pos_list[g][7])
    if len(pos_list[g]) == 12:
        print 'ST(%r,%r,%r,%r,%r,%r,%r,%r,%r){%r,%r,%r};' % (pos_list[g][0], pos_list[g][1], pos_list[g][2], pos_list[g][3], pos_list[g][4], pos_list[g][5], pos_list[g][6],pos_list[g][7],pos_list[g][8],pos_list[g][9],pos_list[g][10],pos_list[g][11])
print 'T2(100000,30,66560){"0km - 120km Atmosphere (July)"};\n};'