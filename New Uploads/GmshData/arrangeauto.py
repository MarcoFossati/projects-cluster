import operator as op

with open(
        r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\Gmsh\2D_Globe\2D.msh",
        "r") as searchfile:
    mesh = [x.strip().split() for x in searchfile.readlines()]

with open(
        r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Additional_Models\twp.lsn",
        "r") as searchfile:
    data = [x.strip().split() for x in searchfile.readlines()]

def right_node_arranger(tan_lat,temp_column):
    num = list()
    for i in range(5,856,1):
        x = float(mesh[i][1])
        y = float(mesh[i][2])
        if y > (tan_lat*x) - 0.1 and y <(tan_lat*x) + 0.1 and x > 0:
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

    little = list()
    fixed = sorted(num, key = op.itemgetter(1), reverse= True)

    output = list()
    for i in range(6,31,1):
        temp = float(data[i][temp_column])
        mini = list(fixed[i-6])
        mini.append(temp)
        output.append(mini)

    for p in range(0,len(output)):
        print output[p][0],output[p][1],output[p][2],output[p][3],output[p][4]
    #print '-'*60, 'Nodes:',len(output),'/ 25'

def left_node_arranger(tan_lat,temp_column):
    num = list()
    for i in range(5,856,1):
        x = float(mesh[i][1])
        y = float(mesh[i][2])
        if y > (tan_lat*x) - 0.1 and y <(tan_lat*x) + 0.1 and x < 0:
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

    little = list()
    fixed = sorted(num, key = op.itemgetter(1), reverse= False)

    output = list()
    for i in range(6,31,1):
        temp = float(data[i][temp_column])
        mini = list(fixed[i-6])
        mini.append(temp)
        output.append(mini)

    for p in range(0,len(output)):
        print output[p][0],output[p][1],output[p][2],output[p][3],output[p][4]
    #print '-'*60, 'Nodes:',len(output),'/ 25'

#print 'Right North:'
right_node_arranger(0,9)
right_node_arranger(0.176327,10)
right_node_arranger(0.36397,11)
right_node_arranger(0.57735,12)
right_node_arranger(0.8390996,13)
right_node_arranger(1.191754,14)
right_node_arranger(1.732051,15)
right_node_arranger(2.747477419,16)
right_node_arranger(5.67128,17)

#print ' Right South:'
right_node_arranger(-0.176327,8)
right_node_arranger(-0.36397,7)
right_node_arranger(-0.57735,6)
right_node_arranger(-0.8390996,5)
right_node_arranger(-1.191754,4)
right_node_arranger(-1.732051,3)
right_node_arranger(-2.747477419,2)
right_node_arranger(-5.67128,1)

#print 'Left North:'
left_node_arranger(0,9)
left_node_arranger(-0.176327,10)
left_node_arranger(-0.36397,11)
left_node_arranger(-0.57735,12)
left_node_arranger(-0.8390996,13)
left_node_arranger(-1.191754,14)
left_node_arranger(-1.732051,15)
left_node_arranger(-2.747477419,16)
left_node_arranger(-5.67128,17)
#print ' Left South:'
left_node_arranger(0.176327,8)
left_node_arranger(0.36397,7)
left_node_arranger(0.57735,6)
left_node_arranger(0.8390996,5)
left_node_arranger(1.191754,4)
left_node_arranger(1.732050808,3)
left_node_arranger(2.747477419,2)
left_node_arranger(5.67128,1)

#average = list()
#steps = list()
#for i in range(2,10,1):
#    numero = float(data[30][i])
#    steps.append(float(i))
#    average.append(numero)

#print average
#print steps
#poly = np.polyfit(steps,average,3)
#print poly