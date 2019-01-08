from pathlib import Path

TAG = "HelperMethods: "


def getProjectFolder():
    return Path.cwd()

# TODO, use split() mehod instead of string splitting to retrieve values.
def getDrawShapesData():
    folder = Path.cwd()
    print(TAG + "Current directory is: " + str(folder.resolve()))
    configFile = folder / "MASTER-CONFIG.txt"
    if not configFile.exists():
        print(TAG + "master configuration file not found.")
        return
    # read DrawShapes data only.
    with configFile.open('r') as file:
        data = []
        for line in file:
            if line.__contains__("DRAWSHAPES"):
                line = line[10:]  # 1 more because of equals sign in file. TODO, SPLIT()^^^
                line = line.rstrip('\n')
                data.append(line)
        return data
    print(TAG + "Data could not be read.")


def getSU2Data():
    folder = Path.cwd()
    print(TAG + "Current directory is: " + str(folder.resolve()))
    configFile = folder / "MASTER-CONFIG.txt"
    if not configFile.exists():
        print(TAG + "master configuration file not found.")
        return
    # read SU2 configuration data only.
    with configFile.open('r') as file:
        data = []
        for line in file:
            if line.__contains__("SU2CONTROL"):
                line = line[10:]  # 1 more because of equals sign in file.
                line = line.rstrip('\n')
                data.append(line)
        return data
    print(TAG + "Data could not be read.")


def getSU2MeshPoints():
    folder = Path.cwd()
    print(TAG + "Current directory is: " + str(folder.resolve()))
    meshFile = folder / "mesh.su2"
    if not meshFile.exists():
        print(TAG + "mesh file not found (SU2 format).")
        return
    fileData = []
    with meshFile.open('r') as file:
        # copy the entire file to an array for easier manipulation.

        for line in file:
            line = line.rstrip('\n')
            fileData.append(line)
    # find the line that contains string "NPOIN=", this will get the number of points.
    NPOINIndex = -1
    NPOINLine = ""
    for i in range(0, fileData.__len__()):
        line = fileData[i]
        if line.__contains__("NPOIN"):
            # get the number of points indicated by this line.
            NPOINIndex = i
            NPOINLine = line
            # exit loop.
            break
    # get the number of points.
    numberOfPoints = NPOINLine[6:]
    print(TAG + "number of points in mesh: " + numberOfPoints)
    numberOfPoints = int(numberOfPoints)
    # use the number of points to loop and extract all of the points.
    pointsList = []
    for i in range(NPOINIndex + 1, NPOINIndex + numberOfPoints + 1):
        # pointsList.append(fileData[i])
        # turn the data into a 3D array.
        pointsList.append(fileData[i].split())
        # print(TAG + fileData[i])
    # convert data into float values.
    for i in range(0, pointsList.__len__()):
        pointsList[i][0] = float(pointsList[i][0])
        pointsList[i][1] = float(pointsList[i][1])
        # pointsList[i][0] = float(pointsList[i][0])
    # print(NPOINIndex)
    # print(pointsList)
    return pointsList


def getSU2MeshConnections():
    folder = Path.cwd()
    print(TAG + "Current directory is: " + str(folder.resolve()))
    meshFile = folder / "mesh.su2"
    if not meshFile.exists():
        print(TAG + "mesh file not found (SU2 format).")
        return
    fileData = []
    with meshFile.open('r') as file:
        # copy the entire file to an array for easier manipulation.

        for line in file:
            line = line.rstrip('\n')
            fileData.append(line)
    # find the line that contains string "NELEM=", this will get the number of points.
    NELEMIndex = -1
    NELEMLine = ""
    for i in range(0, fileData.__len__()):
        line = fileData[i]
        if line.__contains__("NELEM"):
            # get the number of points indicated by this line.
            NELEMIndex = i
            NELEMLine = line
            # exit loop.
            break
    # get the number of points.
    numberOfPoints = NELEMLine[6:]
    print(TAG + "number of elements in mesh: " + numberOfPoints)
    numberOfPoints = int(numberOfPoints)
    # use the number of points to loop and extract all of the points.
    elementList = []
    for i in range(NELEMIndex + 1, NELEMIndex + numberOfPoints + 1):
        # turn the data into a 4D array.
        elementList.append(fileData[i].split())
        # print(TAG + fileData[i])
    # convert data into int values.
    for i in range(0, elementList.__len__()):
        elementList[i][1] = int(elementList[i][1])
        elementList[i][2] = int(elementList[i][2])
        elementList[i][3] = int(elementList[i][3])

    return elementList

def getMach():
    folder = Path.cwd()
    print(TAG + "Current directory is: " + str(folder.resolve()))
    meshFile = folder / "MASTER-CONFIG.txt"
    if not meshFile.exists():
        print(TAG + "file not found.")
        return
    fileData = []
    with meshFile.open('r') as file:
        # copy the entire file to an array for easier manipulation.

        for line in file:
            line = line.rstrip('\n')
            fileData.append(line)
    for i in range(0, fileData.__len__()):
        line = fileData[i]
        if line.__contains__("MACH="):
            # get the number of points indicated by this line.
            return line[5:]

def getReynolds():
    folder = Path.cwd()
    print(TAG + "Current directory is: " + str(folder.resolve()))
    meshFile = folder / "MASTER-CONFIG.txt"
    if not meshFile.exists():
        print(TAG + "file not found.")
        return
    fileData = []
    with meshFile.open('r') as file:
        # copy the entire file to an array for easier manipulation.

        for line in file:
            line = line.rstrip('\n')
            fileData.append(line)
    for i in range(0, fileData.__len__()):
        line = fileData[i]
        if line.__contains__("REYNOLDS="):
            # get the number of points indicated by this line.
            return line[9:]

def getTemp():
    folder = Path.cwd()
    print(TAG + "Current directory is: " + str(folder.resolve()))
    meshFile = folder / "MASTER-CONFIG.txt"
    if not meshFile.exists():
        print(TAG + "file not found.")
        return
    fileData = []
    with meshFile.open('r') as file:
        # copy the entire file to an array for easier manipulation.

        for line in file:
            line = line.rstrip('\n')
            fileData.append(line)
    for i in range(0, fileData.__len__()):
        line = fileData[i]
        if line.__contains__("TEMPINF="):
            # get the number of points indicated by this line.
            return line[8:]

def getCFL():
    folder = Path.cwd()
    print(TAG + "Current directory is: " + str(folder.resolve()))
    meshFile = folder / "MASTER-CONFIG.txt"
    if not meshFile.exists():
        print(TAG + "file not found.")
        return
    fileData = []
    with meshFile.open('r') as file:
        # copy the entire file to an array for easier manipulation.

        for line in file:
            line = line.rstrip('\n')
            fileData.append(line)
    for i in range(0, fileData.__len__()):
        line = fileData[i]
        if line.__contains__("CFL="):
            # get the number of points indicated by this line.
            return line[4:]

def setData(machNumber, reynoldsNumber, tempFreestream, CFLNumber):
    folder = Path.cwd()
    print(TAG + "Current directory is: " + str(folder.resolve()))
    su2File = folder / "SU2-CONFIG.cfg"
    if not su2File.exists():
        print(TAG + "file not found.")
        return
    fileData = []
    with su2File.open('r') as file:
        # copy the entire file to an array for easier manipulation.

        for line in file:
            line = line.rstrip('\n')
            fileData.append(line)
    for i in range(0, fileData.__len__()):
        line = fileData[i]
        if line.__contains__("MACH_NUMBER="):
            # delete the number and add the new one.
            line = line[0:13]+ " " + str(machNumber)
            # set the new data in place of old data.
            fileData[i] = line
        elif line.__contains__("REYNOLDS_NUMBER="):
            # delete the number and add the new one.
            line = line[0:17]+ " " + str(reynoldsNumber)
            # set the new data in place of old data.
            fileData[i] = line
        elif line.__contains__("FREESTREAM_TEMPERATURE="):
            # delete the number and add the new one.
            line = line[0:24]+ " " + str(tempFreestream)
            # set the new data in place of old data.
            fileData[i] = line
        elif line.__contains__("CFL_NUMBER="):
            # delete the number and add the new one.
            line = line[0:12]+ " " + str(CFLNumber)
            # set the new data in place of old data.
            fileData[i] = line
    # write data back to file when done.
    # remove old version.
    su2File.unlink()
    su2File = folder / "SU2-CONFIG.cfg"
    with su2File.open('a') as file:
        for data in fileData:
            file.write(data + "\n")
