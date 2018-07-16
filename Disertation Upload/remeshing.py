# First argument: baseName
# Second argument: essentialsFolder
# Third argument: projectFolderApp 
# Fourth argument: methodName


# OS selection
windowsOS = False      # True = Windows, False = Ubuntu
emailingMesh = False

# --- Modules ---
import sys, shutil
import os, os.path

import numpy as np
import math
import csv
from matplotlib import pyplot as plt

import time

if windowsOS == True:
  import winsound

if emailingMesh == True:
  import smtplib
  from email.MIMEMultipart import MIMEMultipart
  from email.MIMEText import MIMEText

# --- Global variables ---

# - Global user inputs
externalSimulation = False
thresholdHistogram = True
boundaryCL = False
boundaryQuads = True
weightedAverage = False

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000		# Set Duration To 1000 ms == 1 second
threshold = 0.001	# set convergence threshold 

# - Email Notification Credentials
recieveAddress = 'CalumMYoung@gmail.com'
sendAddress = 'CYoungProject@gmail.com'
sendPassword = 'Strathclyde1967'

# - Global paths
projectPath = sys.argv[2]
essentialsFolder = projectPath + 'Essentials/'

# --- Functions ---
def createFoldersIfNonExisting(folders):
  # - Creates folder if path not found 
  for path in folders:
    try: 
      os.makedirs(path)
    except OSError:
      if not os.path.isdir(path):
        raise


def emailSend(recieveAddress, subject, body, sendAddress, sendPassword):
  fromaddr = str(sendAddress)
  toaddr = str(recieveAddress)
  msg = MIMEMultipart()
  msg['From'] = fromaddr
  msg['To'] = toaddr
  msg['Subject'] = str(subject)
 
  msg.attach(MIMEText(body, 'plain'))
 
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(fromaddr, str(sendPassword))
  text = msg.as_string()
  server.sendmail(fromaddr, toaddr, text)
  server.quit()

  print('Email Send to: ' + str(recieveAddress))
  print('Subject: ' + str(subject))
  print('Contents: ' + str(body))

def checkEmail():
  if recieveAddress == None:
    emailingMesh = False
    print("Please check email credentials")
    exit()

  if sendAddress == None:
    emailingMesh = False
    print("Please check email credentials")
    exit()

  if sendPassword == None:
    emailingMesh = False
    print("Please check email credentials")
    exit()


def emailConfirmMesh(geoFileName, noIter , baseName, methodName, geoFile, meshAttempt, meshType):       
  # - Email to confirm mesh generation success
  if emailingMesh == True:
    try: 
      print ('Sending Email - Successfully meshed: {0}_v{1}.{2}').format(geoFileName, str(noIter), meshType)     
      emailSubject = ('Successfully meshed: {0}_v{1}.{2}').format(geoFileName, str(noIter), meshType)     
      emailContents = ("""Successfully meshed: {0}_v{1}.{6}


In {5} attempts.


Details:      
      Base Name: {2}
      Iteration Number: {1}
      MethodName: {3}
      Printing location: {4}
      
    """).format(geoFileName, noIter, baseName, methodName, geoFile, meshAttempt, meshType)          
      emailSend(recieveAddress, emailSubject, emailContents, sendAddress, sendPassword)        
      print ('Email Sent')
    except: 
      print ('Email send failed')              

def emailAttemptMesh(geoFileName, noIter , baseName, methodName, geoFile, meshAttempt, meshType):       
  # - Email to confirm mesh generation attempt
  if emailingMesh == True:
    try: 
      print ('Sending Email - Meshing: {0}_v{1}.{2}').format(geoFileName, noIter, meshType)           
      emailSubject = ('Meshing: {0}_v{1}.{2}').format(geoFileName, noIter, meshType)                  
      emailContents = ("""Meshing: {0}_v{1}.{6}


Attempt: {5}


Email to follow confirming completion.


Details:      
      Base Name: {2}
      Iteration Number: {1}
      MethodName: {3}
      Printing location: {4}
      
    """).format(geoFileName, noIter, baseName, methodName, geoFile, meshAttempt, meshType)      
      emailSend(recieveAddress, emailSubject, emailContents, sendAddress, sendPassword)    
      print ('Email Sent')
    except: 
      print ('Email send failed')


def meshCase(Obj, noIter, meshFolder):          
  # - Generate mesh for .su2 and .msh
  os.chdir(meshFolder)
  meshTypeName = ['msh','su2']      
  for meshType in meshTypeName:     
    meshAttempt = 0               
    while True:
      if os.path.exists('{0}.{1}'.format(Obj.meshes[noIter].geoFile + '_v' + str(noIter),str(meshType))):     
        emailConfirmMesh(Obj.meshes[0].geoFileName, str(noIter) , Obj.baseName, Obj.remeshingTechnique.methodName, Obj.meshes[noIter].geoFile + '_v' + str(noIter), meshAttempt, str(meshType))    
        break       
      else:
        emailAttemptMesh(Obj.meshes[0].geoFileName, str(noIter) , Obj.baseName, Obj.remeshingTechnique.methodName, Obj.meshes[noIter].geoFile + '_v' + str(noIter), meshAttempt, str(meshType))    
        os.system('gmsh {0}_v{1}.geo -{2} -o {3}.{4}'.format(Obj.meshes[noIter].geoFile, str(noIter), str(Obj.caseScenario.noDimensions), Obj.meshes[noIter].geoFile + '_v' + str(noIter),str(meshType)))        
        meshAttempt = meshAttempt+1  


def runSU2Computation(Obj, noIter, baseDir, meshDir, curRunDir):        
  # - Run SU2 computation
  if Obj.noCPUs >1:       #for parallel comp
    os.system('mpirun -n {1} SU2_CFD {0}.cfg'.format(Obj.configurationFile,Obj.noCPUs))
    os.system('SU2_SOL {0}.cfg'.format(Obj.configurationFile))
  else:
    os.system('SU2_CFD {0}.cfg'.format(Obj.configurationFile))


def setupMeshFolder(Obj,meshDir):       
  # - Copy files to mesh folder
  shutil.copyfile(essentialsFolder+'{0}.geo'.format(Obj.meshes[0].geoFile),'{0}{1}.geo'.format(meshDir, su2.meshes[0].geoFile))
  if os.path.exists(essentialsFolder+'{0}_v0.geo'.format(Obj.meshes[0].geoFile)):     
    shutil.copyfile(essentialsFolder+'{0}_v0.geo'.format(Obj.meshes[0].geoFile),'{0}{1}_v0.geo'.format(meshDir, su2.meshes[0].geoFile))
  else: 
    shutil.copyfile(essentialsFolder+'{0}.geo'.format(Obj.meshes[0].geoFile),'{0}{1}_v0.geo'.format(meshDir, su2.meshes[0].geoFile))
  
  if windowsOS == True:       
    shutil.copyfile(essentialsFolder+'gmsh.exe',meshDir+'gmsh.exe')
  
  
def setupRunFolder(Obj, noIter, baseDir, meshDir, curRunDir):
  os.chdir(curRunDir)    
  # - Copy current meshes to run folder         
  meshTypeName = ['msh','su2']      
  for meshType in meshTypeName:     
    shutil.copyfile('{0}_v{1}.{2}'.format(Obj.meshes[noIter].geoFile, str(noIter), meshType), '{0}{1}.{2}'.format(currentRunDir,Obj.configurationFile, meshType))
  
  # - Copy SU2 essentials to run folder
  if windowsOS == True:
    su2Essentials = [Obj.configurationFile + '.cfg', 'SU2_CFD.exe', 'SU2_SOL.exe', 'libiomp5md.dll']        
  else:
    su2Essentials = [Obj.configurationFile + '.cfg']
  
  for f in su2Essentials:
    shutil.copyfile(essentialsFolder+'{0}'.format(f),'{0}{1}'.format(currentRunDir, f))  

def retrieveMeshes(Obj, noIter, baseDir, meshDir, curRunDir):
  # - Copy current mesh from run folder to meshes folder          
  shutil.copyfile('{0}{1}.su2'.format(currentRunDir,Obj.configurationFile), '{0}_v{1}.su2'.format(Obj.meshes[noIter].geoFile, str(noIter))) 
  shutil.copyfile('{0}{1}.msh'.format(currentRunDir,Obj.configurationFile), '{0}_v{1}.msh'.format(Obj.meshes[noIter].geoFile, str(noIter)))          

def mid(s, offset, amount):
  # return part of string 
  return s[offset:offset+amount]

def mag(x): 
  # return magnitude of value
  return math.sqrt(sum(i**2 for i in x))
  
def ave(x):
  # return average of list
  return sum(x)/float(len(x))   

def getKeyGrad(item):
  return item[3]

def getKeyGradS(item):
  return item[0]

def widen(scale, values, i): #takes in 3 values: how much you want to change the values by, the values and which one it is in refrence to
	tmpkey = list(values) #change the tuple to a list
	low = len(tmpkey[i].split('.')[1]) #find the amount of numbers after the decimal point
	low = 10**(-low) #the smallest significant figure is found
	tmpkey[i] = float(tmpkey[i]) #change the string to a number

	tmpkey[i] = tmpkey[i] + scale*low #change this value by the scale * the smallest sigfig
	tmpkey[i] = str(float('%.5g' % tmpkey[i])) #round this value to 5 sigfigs and update the list
	return(tuple(tmpkey)) #return this list as a tuple

def renameCSV(origionalCSV):
  # rename CSV file 
  print("Looking for: " + origionalCSV + ".csv")
  print(os.path.exists(origionalCSV + ".csv"))
  
  if not os.path.exists(origionalCSV + ".csv"):
    if not os.path.exists(origionalCSV + "_old.csv"):
      print('No CSV file found')
      sys.exit()
  else:
    if not os.path.exists(origionalCSV + "_old.csv"):
      os.rename(origionalCSV + ".csv", origionalCSV + "_old.csv")
    else:
      os.remove(origionalCSV + ".csv")

def reorderCSV(mshFile, csvFile): 
  # reorder csv file 
  renameCSV(csvFile)

  headerText = ""
  try:
    with open(csvFile + '_old.csv', "r") as m: #open the file which needs to be re-ordered
      Gradient = {} #create a dictionary for the lines which will be indexed by the x,y,z coords
      header = True 
      for line in m: #for every line in the file
				if header == True: #ignore the first line as its just titles
				  header = False
				  headerText = line.strip()
				else:
					data = line.strip().split(',') #split the line by commas and insert this in the data list
					dataKey = list(map(float, data[-3::])) #take the last 3 values in the array (x,y,z), convert these to numbers and put in a list
					dataKey = tuple(map(str, [float('%.5g' % elt) for elt in dataKey])) #round each coord to 5 significant figures, change them to a string and combine these to form a tuple
					Gradient[dataKey] = data #add this tuple to the dictionary with it mapping to the line it represents

    with open(mshFile + '.msh') as e: #open the correct order file
      meshData = list(e) #meshData = a list of all the lines
      for i, line in enumerate(meshData): #for each line and its corresponding number
				if line == '$Nodes\n': #if the line is nodes
					length = int(meshData[i+1]) #the length is the integer on the next line
					start = i + 2 #the first line we care about here starts 2 lines after the nodes line

    with open(csvFile + '.csv', 'w') as m: #open the file which needs to be re-ordered
      m.write(headerText + '\n') #write the header to the file
      for val in range(start, start+length): #for every value 
				key = list(map(float, meshData[val].strip().split(' ')[1:])) #get the x,y,z coords from the order file in turn and convert these to numbers
				key = tuple(map(str, [float('%.5g' % elt) for elt in key])) #round these values to 5 significant figures
				try:
					m.write(','.join(Gradient[key]) + '\n') #output the value in the dictionary to the file
				except:
					for i in range(3): #for each coord
						if widen(1,key,i) in Gradient: #if the slightly higher value is in the dictionary
							m.write(','.join(Gradient[widen(1,key,i)]) + '\n') #output this line to the file

						if widen(-1,key,i) in Gradient: #if the slightly lower line is in the dictionary
							m.write(','.join(Gradient[widen(-1,key,i)]) + '\n') #output this line to the file
  except:
		print('msh order file was not found')
		sys.exit()

	#check file length
  origionalCSVLength = sum(1 for row in open(csvFile + '_old.csv'))
  finalCSVLength = sum(1 for row in open(csvFile + '.csv'))
    
  if not (origionalCSVLength == finalCSVLength):
		print ('Original and final CSV file lengths do not match.')
		misisngLines = abs(origionalCSVLength - finalCSVLength)
		print('Lines missing: ' + str(misisngLines))
		sys.exit()
	


def timePrint(timeSec):
  # print time 
  timeMin = 0
  if timeSec >= 60:
    timeMin = round(timeSec/60-0.5,0)
    timeSec = timeSec - timeMin*60
    if timeMin > 1: 
      timePrint = "{0} minutes and {1} seconds".format(str(int(timeMin)),str(round(timeSec,1)))
    else: 
      timePrint = "{0} minute and {1} seconds".format(str(int(timeMin)),str(round(timeSec,1)))
  else: 
    timePrint = "{1} seconds".format(str(int(timeMin)),str(round(timeSec,1)))
  return timePrint

def modifyPos(origionalPos, radius):
  if not os.path.exists(origionalPos + ".pos"):
    if not os.path.exists(origionalPos + "_old.pos"):
      print('pos file not found')
      sys.exit()
  else:
    if not os.path.exists(origionalPos + "_old.pos"):
      os.rename(origionalPos + ".pos", origionalPos + "_old.pos")
    else:
      os.remove(origionalPos + ".pos")

  dist = float(radius)                  
  file = open(origionalPos+ "_old.pos", "r")
  lines = file.readlines()
  file.close()

  sgradval = []
  smod = []

  starttime = time.time()
  for line in lines:
    line = line.strip()
    
    if(line.find("SL") != -1):
      if boundaryQuads == False:
        startpos = line.find("{")
        compos = line.find(",",startpos+1)
        endpos = line.find("}",compos+1)
        sl1 = float(mid(line,startpos+1,compos-startpos-1))
        sl2 = float(mid(line,compos+1,endpos-compos-1))
        sgradval.append(sl1)
        sgradval.append(sl2)
        
    if(line.find("ST") != -1):
        startpos = line.find("{")
        compos1 = line.find(",",startpos+1)
        compos2 = line.find(",",compos1+1)
        endpos = line.find("}",compos2+1)
        
        st1 = float(mid(line,startpos+1,compos1-startpos-1))
        st2 = float(mid(line,compos1+1,compos2-compos1-1))
        st3 = float(mid(line,compos2+1,endpos-compos2-1))
        sgradval.append(st1)
        sgradval.append(st2)
        sgradval.append(st3)

    if(line.find("SQ") != -1):
      if boundaryQuads == False:
        startpos = line.find("{")
        compos1 = line.find(",",startpos+1)
        compos2 = line.find(",",compos1+1)
        compos3 = line.find(",",compos2+1)
        endpos = line.find("}",compos3+1)
        
        sq1 = float(mid(line,startpos+1,compos1-startpos-1))
        sq2 = float(mid(line,compos1+1,compos2-compos1-1))
        sq3 = float(mid(line,compos2+1,compos3-compos2-1))
        sq4 = float(mid(line,compos3+1,endpos-compos3-1))
        sgradval.append(sq1)
        sgradval.append(sq2)
        sgradval.append(sq3)
        sgradval.append(sq4)

  sgradval = sorted(sgradval, reverse=True)
  percentile = 0.1
  position = int(percentile * len(sgradval))
  supercentile = sgradval[position]

  if(supercentile == min(sgradval)):
    supercentile  = max(sgradval)

  sUModGradval = []

  for i in range(len(sgradval)):
    if sgradval[i] < supercentile: 
      sUModGradval.append(sgradval[i])

  plt.xlim([min(sUModGradval), max(sUModGradval)])
  binwidth = max(sUModGradval)/1000
  n, b, patches = plt.hist(sUModGradval, bins=np.arange(min(sUModGradval), max(sUModGradval) + binwidth, binwidth))

  bin_max = 0
  max_bin_val = n[0]
  for i in range(len(n)):
    if n[i]>max_bin_val:
      bin_max=i
      max_bin_val=n[i]

  sUModGradval = sorted(sUModGradval, reverse=False)
  percentile = 0.62
  position = int(percentile * len(sUModGradval)) 
  spercentile = sUModGradval[position]

  if(spercentile == min(sgradval)):
    for i in range(len(sUModGradval)):
      if (sUModGradval[position] > min(sgradval)):
        spercentile = min(sgradval)
        break

  bin_max = 0
  max_bin_val = n[0]
  for i in range(len(n)):
    if b[i]>max_bin_val:
      bin_max=i
      max_bin_val=n[i]

  plt.xlabel('Bins')
  plt.ylabel('Gradient Value')
  plt.title('Histogram of Gradient Values - {0}'.format(origionalPos))
  plt.axis([0, max(sUModGradval), 0, max_bin_val])
  plt.grid(True)

  weAvVal = 0
  
  if (weightedAverage==True):
    data = []
    for pos in range(len(sUModGradval)):
      if (sUModGradval[pos] >= spercentile) and (sUModGradval[pos] <= supercentile):
        data.append(sUModGradval[pos])
    
    xmin = min(data)
    xmax = max(data)
    binsize = binwidth
    
    bins_arange = np.arange(xmin, xmax + 1, binsize)
    counts, edges = np.histogram(data, bins=bins_arange)
    bin_middles = (edges[:-1] + edges[1:]) / 2
    weAvSum = 0
    for pos in range(len(counts)):
      weAvSum = weAvSum + counts[pos]*bin_middles[pos]
    
    if sum(counts) == 0:
      sumcount = 1
    else: 
      sumcount = sum(counts)
    weAvVal = weAvSum/sumcount
    
  if weAvVal == 0: 
    weAvVal = supercentile
    print ("Weighted average value: {0}.".format(str(weAvVal)))

  print ("Lower threshold value: {0}".format(str(spercentile)))
  print ("Upper threshold value: {0}".format(str(supercentile)))


  percentiletime = time.time()
  print ("Time taken to find threshold values: {0}.".format(timePrint(percentiletime-starttime)))

  lastTime = percentiletime
  lineCount = 0
  lastPrintCount = 0

  for line in lines:
    lineCount = lineCount+1
    line = line.strip()

    if lineCount-1000 == lastPrintCount:
      currentTime = time.time()
      print("Calculating threshold values. Read lines {0}/{1}. In {2}.".format(lineCount, len(lines), timePrint(currentTime - percentiletime)))
      lastPrintCount = lineCount
      lastTime = currentTime

    if(line.find("SL") != -1):
      startpos = line.find("{")
      compos = line.find(",",startpos+1)
      endpos = line.find("}",compos+1)
      sl1 = float(mid(line,startpos+1,compos-startpos-1))
      sl2 = float(mid(line,compos+1,endpos-compos-1))
        
        
      if(sl1>=spercentile):
        locstartpos = line.find("(")
        loccompos1 = line.find(",",locstartpos+1)
        loccompos2 = line.find(",",loccompos1+1)
        loccompos3 = line.find(",",loccompos2+1)
        loccompos4 = line.find(",",loccompos3+1)
        loccompos5 = line.find(",",loccompos4+1)
        locendpos = line.find(")",loccompos5+1)
        
        slp1 = float(mid(line,locstartpos+1,loccompos1-locstartpos-1))
        slp2 = float(mid(line,loccompos1+1,loccompos2-loccompos1-1))
        slp3 = float(mid(line,loccompos2+1,loccompos3-loccompos2-1))
        
        if (sl1>supercentile):
          sl1=supercentile

        smod = smod + [[slp1, slp2, slp3, sl1]]

      if(sl2>=spercentile):
        locstartpos = line.find("(")
        loccompos1 = line.find(",",locstartpos+1)
        loccompos2 = line.find(",",loccompos1+1)
        loccompos3 = line.find(",",loccompos2+1)
        loccompos4 = line.find(",",loccompos3+1)
        loccompos5 = line.find(",",loccompos4+1)
        locendpos = line.find(")",loccompos5+1)
        
        slp4 = float(mid(line,loccompos3+1,loccompos4-loccompos3-1))
        slp5 = float(mid(line,loccompos4+1,loccompos5-loccompos4-1))
        slp6 = float(mid(line,loccompos5+1,locendpos-loccompos5-1))
          
        if (sl2>supercentile):
          sl2=supercentile

        smod = smod + [[slp4, slp5, slp6, sl2]]

    if(line.find("ST") != -1):
      startpos = line.find("{")
      compos1 = line.find(",",startpos+1)
      compos2 = line.find(",",compos1+1)
      endpos = line.find("}",compos2+1)
        
      st1 = float(mid(line,startpos+1,compos1-startpos-1))
      st2 = float(mid(line,compos1+1,compos2-compos1-1))
      st3 = float(mid(line,compos2+1,endpos-compos2-1))

      if(st1>=spercentile):
        locstartpos = line.find("(")
        loccompos1 = line.find(",",locstartpos+1)
        loccompos2 = line.find(",",loccompos1+1)
        loccompos3 = line.find(",",loccompos2+1)
          
        stp1 = float(mid(line,locstartpos+1,loccompos1-locstartpos-1))
        stp2 = float(mid(line,loccompos1+1,loccompos2-loccompos1-1))
        stp3 = float(mid(line,loccompos2+1,loccompos3-loccompos2-1))
          
        if (st1>supercentile):
          st1=supercentile

        smod = smod + [[stp1, stp2, stp3, st1]]

      if(st2>=spercentile):
        locstartpos = line.find("(")
        loccompos1 = line.find(",",locstartpos+1)
        loccompos2 = line.find(",",loccompos1+1)
        loccompos3 = line.find(",",loccompos2+1)
        loccompos4 = line.find(",",loccompos3+1)
        loccompos5 = line.find(",",loccompos4+1)
        loccompos6 = line.find(",",loccompos5+1)
          
        stp4 = float(mid(line,loccompos3+1,loccompos4-loccompos3-1))
        stp5 = float(mid(line,loccompos4+1,loccompos5-loccompos4-1))
        stp6 = float(mid(line,loccompos5+1,loccompos6-loccompos5-1))
          
        if (st2>supercentile):
          st2=supercentile

        smod = smod + [[stp4, stp5, stp6, st2]]

      if(st3>=spercentile):
        locstartpos = line.find("(")
        loccompos1 = line.find(",",locstartpos+1)
        loccompos2 = line.find(",",loccompos1+1)
        loccompos3 = line.find(",",loccompos2+1)
        loccompos4 = line.find(",",loccompos3+1)
        loccompos5 = line.find(",",loccompos4+1)
        loccompos6 = line.find(",",loccompos5+1)
        loccompos7 = line.find(",",loccompos6+1)
        loccompos8 = line.find(",",loccompos7+1)
        locendpos = line.find(")",loccompos8+1)
          
        stp7 = float(mid(line,loccompos6+1,loccompos7-loccompos6-1))
        stp8 = float(mid(line,loccompos7+1,loccompos8-loccompos7-1))
        stp9 = float(mid(line,loccompos8+1,locendpos-loccompos8-1))
        
        if (st3>supercentile):
          st3=supercentile

        smod = smod + [[stp7, stp8, stp9, st3]]
    
    if(line.find("SQ") != -1):
      if boundaryQuads == False:
        startpos = line.find("{")
        compos1 = line.find(",",startpos+1)
        compos2 = line.find(",",compos1+1)
        compos3 = line.find(",",compos2+1)
        endpos = line.find("}",compos3+1)
        
        sq1 = float(mid(line,startpos+1,compos1-startpos-1))
        sq2 = float(mid(line,compos1+1,compos2-compos1-1))
        sq3 = float(mid(line,compos2+1,compos3-compos2-1))
        sq4 = float(mid(line,compos3+1,endpos-compos3-1))

        if(st1>=spercentile):
          locstartpos = line.find("(")
          loccompos1 = line.find(",",locstartpos+1)
          loccompos2 = line.find(",",loccompos1+1)
          loccompos3 = line.find(",",loccompos2+1)
          
          sqp1 = float(mid(line,locstartpos+1,loccompos1-locstartpos-1))
          sqp2 = float(mid(line,loccompos1+1,loccompos2-loccompos1-1))
          sqp3 = float(mid(line,loccompos2+1,loccompos3-loccompos2-1))
          
          if (sq1>supercentile):
            sq1=supercentile

          smod = smod + [[sqp1, sqp2, sqp3, sq1]]

        if(sq2>=spercentile):
          locstartpos = line.find("(")
          loccompos1 = line.find(",",locstartpos+1)
          loccompos2 = line.find(",",loccompos1+1)
          loccompos3 = line.find(",",loccompos2+1)
          loccompos4 = line.find(",",loccompos3+1)
          loccompos5 = line.find(",",loccompos4+1)
          loccompos6 = line.find(",",loccompos5+1)
          
          sqp4 = float(mid(line,loccompos3+1,loccompos4-loccompos3-1))
          sqp5 = float(mid(line,loccompos4+1,loccompos5-loccompos4-1))
          sqp6 = float(mid(line,loccompos5+1,loccompos6-loccompos5-1))
            
          if (sq2>supercentile):
            sq2=supercentile

          smod = smod + [[sqp4, sqp5, sqp6, sq2]]
          
        if(sq3>=spercentile):
          locstartpos = line.find("(")
          loccompos1 = line.find(",",locstartpos+1)
          loccompos2 = line.find(",",loccompos1+1)
          loccompos3 = line.find(",",loccompos2+1)
          loccompos4 = line.find(",",loccompos3+1)
          loccompos5 = line.find(",",loccompos4+1)
          loccompos6 = line.find(",",loccompos5+1)
          loccompos7 = line.find(",",loccompos6+1)
          loccompos8 = line.find(",",loccompos7+1)
          loccompos9 = line.find(",",loccompos8+1)
          
          sqp7 = float(mid(line,loccompos6+1,loccompos7-loccompos6-1))
          sqp8 = float(mid(line,loccompos7+1,loccompos8-loccompos7-1))
          sqp9 = float(mid(line,loccompos8+1,loccompos9-loccompos8-1))

          if (sq3>supercentile):
            sq3=supercentile

          smod = smod + [[sqp7, sqp8, sqp9, st3]]

        if(sq4>=spercentile):
          locstartpos = line.find("(")
          loccompos1 = line.find(",",locstartpos+1)
          loccompos2 = line.find(",",loccompos1+1)
          loccompos3 = line.find(",",loccompos2+1)
          loccompos4 = line.find(",",loccompos3+1)
          loccompos5 = line.find(",",loccompos4+1)
          loccompos6 = line.find(",",loccompos5+1)
          loccompos7 = line.find(",",loccompos6+1)
          loccompos8 = line.find(",",loccompos7+1)
          loccompos9 = line.find(",",loccompos8+1)
          loccompos10 = line.find(",",loccompos9+1)
          loccompos11 = line.find(",",loccompos10+1)
          locendpos = line.find(")",loccompos11+1)
          
          sqp10 = float(mid(line,loccompos9+1,loccompos10-loccompos9-1))
          sqp11 = float(mid(line,loccompos10+1,loccompos11-loccompos10-1))
          sqp12 = float(mid(line,loccompos11+1,locendpos-loccompos11-1))
          
          if (sq4>supercentile):
            sq4=supercentile

          smod = smod + [[sqp10, sqp11, sqp12, sq4]]

  smod = sorted(smod, key=getKeyGrad, reverse=True)

  threshtime = time.time()
  print ("Time taken to find threshold points: {0}.".format(timePrint(threshtime-percentiletime)))


  if weightedAverage==True:
    quadVal = weAvVal
  else:
    quadVal = spercentile

  lineCount = 0
  lastPrintCount = 0
  lastTime = threshtime

  with open(origionalPos + ".pos", 'w') as f:
    for line in lines:
      lineCount = lineCount+1
      line = line.strip()
      data = "No Data"

      if lineCount-1000 == lastPrintCount:
        currentTime = time.time()
        print("Calculating value of each point. Completed lines {0}/{1}. Estimated time to finish: {2}".format(lineCount, len(lines), timePrint(((currentTime - lastTime)/1000)*(len(lines)-lineCount))))
        lastPrintCount = lineCount
        lastTime = currentTime

      if(line.find("View") != -1):
        data = line

      if(line.find("SL") != -1):
        gradstartpos = line.find("{")
        gradcompos = line.find(",",gradstartpos+1)
        gradendpos = line.find("}",gradcompos+1)
        
        sl1 = float(mid(line,gradstartpos+1,gradcompos-gradstartpos-1))
        sl2 = float(mid(line,gradcompos+1,gradendpos-gradcompos-1))

        locstartpos = line.find("(")
        loccompos1 = line.find(",",locstartpos+1)
        loccompos2 = line.find(",",loccompos1+1)
        loccompos3 = line.find(",",loccompos2+1)
        loccompos4 = line.find(",",loccompos3+1)
        loccompos5 = line.find(",",loccompos4+1)
        locendpos = line.find(")",loccompos5+1)
          
        slp1 = float(mid(line,locstartpos+1,loccompos1-locstartpos-1))
        slp2 = float(mid(line,loccompos1+1,loccompos2-loccompos1-1))
        slp3 = float(mid(line,loccompos2+1,loccompos3-loccompos2-1))
        slp4 = float(mid(line,loccompos3+1,loccompos4-loccompos3-1))
        slp5 = float(mid(line,loccompos4+1,loccompos5-loccompos4-1))
        slp6 = float(mid(line,loccompos5+1,locendpos-loccompos5-1))

        slFinal1 = sl1
        slFinal2 = sl2

        for pos in range(len(smod)):
          dx = smod[pos][0] - slp1
          dy = smod[pos][1] - slp2
          dz = smod[pos][2] - slp3

          distance = math.sqrt(dx*dx + dy*dy + dz*dz)

          if (distance<=dist):
            if weightedAverage==True:
              slFinal1 = weAvVal
            else:
              slFinal1 = smod[pos][3]
            break

        for pos in range(len(smod)):
          dx = smod[pos][0] - slp4
          dy = smod[pos][1] - slp5
          dz = smod[pos][2] - slp6

          distance = math.sqrt(dx*dx + dy*dy + dz*dz)

          if (distance<=dist):
            if weightedAverage==True:
              slFinal2 = weAvVal
            else:
              slFinal2 = smod[pos][3]
            break

        if slFinal1> supercentile:
          slFinal1 = supercentile
        
        if slFinal2> supercentile:
          slFinal2 = supercentile

        data = ('SL({0},{1},{2},{3},{4},{5})'.format(slp1, slp2, slp3, slp4, slp5, slp6) + '{' + '{0},{1}'.format(slFinal1, slFinal2) + '};')

      if(line.find("ST") != -1):
        startpos = line.find("{")
        compos1 = line.find(",",startpos+1)
        compos2 = line.find(",",compos1+1)
        endpos = line.find("}",compos2+1)
        
        st1 = float(mid(line,startpos+1,compos1-startpos-1))
        st2 = float(mid(line,compos1+1,compos2-compos1-1))
        st3 = float(mid(line,compos2+1,endpos-compos2-1))

        locstartpos = line.find("(")
        loccompos1 = line.find(",",locstartpos+1)
        loccompos2 = line.find(",",loccompos1+1)
        loccompos3 = line.find(",",loccompos2+1)
        loccompos4 = line.find(",",loccompos3+1)
        loccompos5 = line.find(",",loccompos4+1)
        loccompos6 = line.find(",",loccompos5+1)
        loccompos7 = line.find(",",loccompos6+1)
        loccompos8 = line.find(",",loccompos7+1)
        locendpos = line.find(")",loccompos8+1)
          
        stp1 = float(mid(line,locstartpos+1,loccompos1-locstartpos-1))
        stp2 = float(mid(line,loccompos1+1,loccompos2-loccompos1-1))
        stp3 = float(mid(line,loccompos2+1,loccompos3-loccompos2-1))
        stp4 = float(mid(line,loccompos3+1,loccompos4-loccompos3-1))
        stp5 = float(mid(line,loccompos4+1,loccompos5-loccompos4-1))
        stp6 = float(mid(line,loccompos5+1,loccompos6-loccompos5-1))
        stp7 = float(mid(line,loccompos6+1,loccompos7-loccompos6-1))
        stp8 = float(mid(line,loccompos7+1,loccompos8-loccompos7-1))
        stp9 = float(mid(line,loccompos8+1,locendpos-loccompos8-1))

        stFinal1 = st1
        stFinal2 = st2
        stFinal3 = st3

        for pos in range(len(smod)):
          dx = smod[pos][0] - stp1
          dy = smod[pos][1] - stp2
          dz = smod[pos][2] - stp3

          distance = math.sqrt(dx*dx + dy*dy + dz*dz)

          if (distance<=dist):
            if weightedAverage==True:
              stFinal1 = weAvVal
            else:
              stFinal1 = smod[pos][3]
            break

        for pos in range(len(smod)):
          dx = smod[pos][0] - stp4
          dy = smod[pos][1] - stp5
          dz = smod[pos][2] - stp6

          distance = math.sqrt(dx*dx + dy*dy + dz*dz)

          if (distance<=dist):
            if weightedAverage==True:
              stFinal2 = weAvVal
            else:
              stFinal2 = smod[pos][3]
            break
        
        for pos in range(len(smod)):
          dx = smod[pos][0] - stp7
          dy = smod[pos][1] - stp8
          dz = smod[pos][2] - stp9

          distance = math.sqrt(dx*dx + dy*dy + dz*dz)

          if (distance<=dist):
            if weightedAverage==True:
              stFinal3 = weAvVal
            else:
              stFinal3 = smod[pos][3]
            break

        if stFinal1> supercentile:
          stFinal1 = supercentile
        
        if stFinal2> supercentile:
          stFinal2 = supercentile
        
        if stFinal3> supercentile:
          stFinal3 = supercentile

        data = ('ST({0},{1},{2},{3},{4},{5},{6},{7},{8})'.format(str(stp1), str(stp2), str(stp3), str(stp4), str(stp5), str(stp6), str(stp7), str(stp8), str(stp9)) + '{' + '{0},{1},{2}'.format(str(stFinal1), str(stFinal2), str(stFinal3) + '};'))

      if(line.find("SQ") != -1):
        if boundaryQuads == False:
          startpos = line.find("{")
          compos1 = line.find(",",startpos+1)
          compos2 = line.find(",",compos1+1)
          compos3 = line.find(",",compos2+1)
          endpos = line.find("}",compos3+1)
        
          sq1 = float(mid(line,startpos+1,compos1-startpos-1))
          sq2 = float(mid(line,compos1+1,compos2-compos1-1))
          sq3 = float(mid(line,compos2+1,compos3-compos2-1))
          sq4 = float(mid(line,compos3+1,endpos-compos3-1))
          
          locstartpos = line.find("(")
          loccompos1 = line.find(",",locstartpos+1)
          loccompos2 = line.find(",",loccompos1+1)
          loccompos3 = line.find(",",loccompos2+1)
          loccompos4 = line.find(",",loccompos3+1)
          loccompos5 = line.find(",",loccompos4+1)
          loccompos6 = line.find(",",loccompos5+1)
          loccompos7 = line.find(",",loccompos6+1)
          loccompos8 = line.find(",",loccompos7+1)
          loccompos9 = line.find(",",loccompos8+1)
          loccompos10 = line.find(",",loccompos9+1)
          loccompos11 = line.find(",",loccompos10+1)
          locendpos = line.find(")",loccompos11+1)
          
          sqp1 = float(mid(line,locstartpos+1,loccompos1-locstartpos-1))
          sqp2 = float(mid(line,loccompos1+1,loccompos2-loccompos1-1))
          sqp3 = float(mid(line,loccompos2+1,loccompos3-loccompos2-1))
          sqp4 = float(mid(line,loccompos3+1,loccompos4-loccompos3-1))
          sqp5 = float(mid(line,loccompos4+1,loccompos5-loccompos4-1))
          sqp6 = float(mid(line,loccompos5+1,loccompos6-loccompos5-1))
          sqp7 = float(mid(line,loccompos6+1,loccompos7-loccompos6-1))
          sqp8 = float(mid(line,loccompos7+1,loccompos8-loccompos7-1))
          sqp9 = float(mid(line,loccompos8+1,loccompos9-loccompos8-1))
          sqp10 = float(mid(line,loccompos9+1,loccompos10-loccompos9-1))
          sqp11 = float(mid(line,loccompos10+1,loccompos11-loccompos10-1))
          sqp12 = float(mid(line,loccompos11+1,locendpos-loccompos11-1))

          sqFinal1 = sq1
          sqFinal2 = sq2
          sqFinal3 = sq3
          sqFinal4 = sq4

          for pos in range(len(smod)):
            dx = smod[pos][0] - sqp1
            dy = smod[pos][1] - sqp2
            dz = smod[pos][2] - sqp3

            distance = math.sqrt(dx*dx + dy*dy + dz*dz)

            if (distance<=dist):
              if weightedAverage==True:
                sqFinal1 = weAvVal
              else:
                sqFinal1 = smod[pos][3]
              break

          for pos in range(len(smod)):
            dx = smod[pos][0] - sqp4
            dy = smod[pos][1] - sqp5
            dz = smod[pos][2] - sqp6

            distance = math.sqrt(dx*dx + dy*dy + dz*dz)
            
            if (distance<=dist):
              if weightedAverage==True:
                sqFinal2 = weAvVal
              else:
                sqFinal2 = smod[pos][3]
              break
        
          for pos in range(len(smod)):
            dx = smod[pos][0] - sqp7
            dy = smod[pos][1] - sqp8
            dz = smod[pos][2] - sqp9

            distance = math.sqrt(dx*dx + dy*dy + dz*dz)

            if (distance<=dist):
              if weightedAverage==True:
                sqFinal3 = weAvVal
              else:
                sqFinal3 = smod[pos][3]
              break

          for pos in range(len(smod)):
            dx = smod[pos][0] - sqp10
            dy = smod[pos][1] - sqp11
            dz = smod[pos][2] - sqp12

            distance = math.sqrt(dx*dx + dy*dy + dz*dz)

            if (distance<=dist):
              if weightedAverage==True:
                sqFinal4 = weAvVal
              else:
                sqFinal4 = smod[pos][3]
              break

          if sqFinal1> supercentile:
            sqFinal1 = supercentile
        
          if sqFinal2> supercentile:
            sqFinal2 = supercentile
        
          if sqFinal3> supercentile:
            sqFinal3 = supercentile

          if sqFinal4> supercentile:
            sqFinal4 = supercentile

          data = ('SQ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11})'.format(str(sqp1), str(sqp2), str(sqp3), str(sqp4), str(sqp5), str(sqp6), str(sqp7), str(sqp8), str(sqp9), str(sqp10), str(sqp11), str(sqp12)) + '{' + '{0},{1},{2},{3}'.format(str(sqFinal1), str(sqFinal2), str(sqFinal3), str(sqFinal4) + '};'))
        else:
          locstartpos = line.find("(")
          loccompos1 = line.find(",",locstartpos+1)
          loccompos2 = line.find(",",loccompos1+1)
          loccompos3 = line.find(",",loccompos2+1)
          loccompos4 = line.find(",",loccompos3+1)
          loccompos5 = line.find(",",loccompos4+1)
          loccompos6 = line.find(",",loccompos5+1)
          loccompos7 = line.find(",",loccompos6+1)
          loccompos8 = line.find(",",loccompos7+1)
          loccompos9 = line.find(",",loccompos8+1)
          loccompos10 = line.find(",",loccompos9+1)
          loccompos11 = line.find(",",loccompos10+1)
          locendpos = line.find(")",loccompos11+1)
          
          sqp1 = float(mid(line,locstartpos+1,loccompos1-locstartpos-1))
          sqp2 = float(mid(line,loccompos1+1,loccompos2-loccompos1-1))
          sqp3 = float(mid(line,loccompos2+1,loccompos3-loccompos2-1))
          sqp4 = float(mid(line,loccompos3+1,loccompos4-loccompos3-1))
          sqp5 = float(mid(line,loccompos4+1,loccompos5-loccompos4-1))
          sqp6 = float(mid(line,loccompos5+1,loccompos6-loccompos5-1))
          sqp7 = float(mid(line,loccompos6+1,loccompos7-loccompos6-1))
          sqp8 = float(mid(line,loccompos7+1,loccompos8-loccompos7-1))
          sqp9 = float(mid(line,loccompos8+1,loccompos9-loccompos8-1))
          sqp10 = float(mid(line,loccompos9+1,loccompos10-loccompos9-1))
          sqp11 = float(mid(line,loccompos10+1,loccompos11-loccompos10-1))
          sqp12 = float(mid(line,loccompos11+1,locendpos-loccompos11-1))

          sqFinal1 = quadVal
          sqFinal2 = quadVal
          sqFinal3 = quadVal
          sqFinal4 = quadVal

          data = ('SQ({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11})'.format(str(sqp1), str(sqp2), str(sqp3), str(sqp4), str(sqp5), str(sqp6), str(sqp7), str(sqp8), str(sqp9), str(sqp10), str(sqp11), str(sqp12)) + '{' + '{0},{1},{2},{3}'.format(str(sqFinal1), str(sqFinal2), str(sqFinal3), str(sqFinal4) + '};'))
      
      if data == "No Data":
        f.write (line)
      else:
        f.write (data)
      
      f.write \
      ("""
""")

  finishtime = time.time()
  print ("Time taken to write file: {0}.".format(timePrint(finishtime-threshtime)))
    
def addNodeDataIntoMsh(viewTag, fieldNodeData):
  # append mesh data 
  """$NodeData
1                      one string tag:
"A scalar view"          the name of the view ("A scalar view")
1                      one real tag:
0.0                      the time value (0.0)
3                      three integer tags:
0                        the time step (0; time steps always start at 0)
1                        1-component (scalar) field
6                        six associated nodal values
1 0.0                  value associated with node #1 (0.0)
2 0.1                  value associated with node #2 (0.1)
3 0.2                  etc.
4 0.0
5 0.2
6 0.4
$EndNodeData
""" # Example
  
  nodeDataStr = """$NodeData
1
"{0}"
1
0.0
3
0
1
{1}
{2}
$EndNodeData
""".format(viewTag, len(fieldNodeData), '\n'.join(str(i+1) + '\t' + str(j) for i, j in enumerate(fieldNodeData)))
  return nodeDataStr


def callAMRTechnique(solutionPath, printPath, Obj, meshIte, meshesFolder, mathEval, minLevel, historyRestart):
  # call adaptive mesh refinement technique 
  if (Obj.remeshingTechnique.methodName=='hessianBased'):
    computeHessian(solutionPath, Obj.remeshingTechnique.evaluationQuantity, meshIte, meshesFolder)
    createHessGeo(Obj.meshes[meshIte+1].geoFile + '_v{0}.geo'.format(str(meshIte + 1)), Obj.remeshingTechnique.evaluationQuantity[0], str(meshIte), Obj.meshes[0].geoFileName)
  
  if (Obj.remeshingTechnique.methodName=='gradientBased'):
    flowFields = []
    gradFields = []
    flowFields, gradFields, mathEval, minLevel, historyRestart = computeGradient(Obj.remeshingTechnique, solutionPath, printPath, Obj.meshes[meshIte], Obj.meshes[meshIte+1], meshIte, Obj.meshes[0].geoFileName, meshesFolder, mathEval, minLevel, gradFields, flowFields, Obj.caseScenario.characteristicLength, Obj, historyRestart)
    mathEval, historyRestart = createGradGeo(Obj.meshes[meshIte+1].geoFile + '_v{0}.geo'.format(str(meshIte + 1)), Obj.meshes[0].geoFileName, minLevel, meshIte, Obj.remeshingTechnique, Obj.meshes[meshIte+1], gradFields, flowFields, mathEval, historyRestart)
      
  return minLevel, mathEval, historyRestart

def computeHessian(solutionPath, evaluationQuantity, meshIte, meshesFolder):
  # generate hessian 
  os.chdir(essentialsFolder)

  for fieldName in evaluationQuantity:
    os.system('vtkPython extractH.py {0}soln_volume.vtk {1} {2} {3}'.format(solutionPath, fieldName, meshIte, meshesFolder))

def computeGradient(remeshingInfo, solutionPath, printPath, meshInfo, nextMeshInfo, meshIte, geoFileName, meshesFolder, mathEval, minLevel, gradFields, flowFields, characteristicLength, Obj, historyRestart):
  # calculate graidents
  os.chdir(essentialsFolder)
  
  # - Run paraview
  for fieldName in remeshingInfo.evaluationQuantity:
    os.system('pvpython computeGradient.py {0}soln_volume.vtk {1} {2}'.format(solutionPath, fieldName, printPath))
  
  os.chdir(solutionPath)

  # Reorder all .csv files
  #for f, fieldName in enumerate(remeshingInfo.evaluationQuantity):
  #  reorderCSV(Obj.configurationFile, fieldName + 'Gradient')

  # - Read relevant fields
  
  # GRADIENT FIELDS
  for f, fieldName in enumerate(remeshingInfo.evaluationQuantity):
    gradFields.append([])    
  
    firstDataCol = 0
    with open(fieldName + 'Gradient.csv', 'rb') as csvfile:
      nodeDataReader = csv.reader(csvfile, delimiter=',')
      row1 = next(nodeDataReader)
      for colCnt, c in enumerate(row1):
        if fieldName + 'Gradient:0' in c:
          firstDataCol = colCnt
          break
          
    with open(fieldName + 'Gradient.csv', 'rb') as csvfile:
      nodeDataReader = csv.reader(csvfile, delimiter=',')
      next(nodeDataReader)
            
      for row in nodeDataReader:
        gradFields[f].append(mag([float(c) for c in row[firstDataCol:firstDataCol+3]])) # magnitude of the gradient

  # FLOW FIELDS
  for f, fieldName in enumerate(remeshingInfo.evaluationQuantity):
    flowFields.append([])    
  
    firstDataCol = 0
    with open(fieldName + 'Gradient.csv', 'rb') as csvfile: # 'Gradient' left deliberately
      nodeDataReader = csv.reader(csvfile, delimiter=',')
      row1 = next(nodeDataReader)
      for colCnt, c in enumerate(row1):
        if fieldName == c:
          firstDataCol = colCnt
          break
          
    with open(fieldName + 'Gradient.csv', 'rb') as csvfile: # 'Gradient' left deliberately
      nodeDataReader = csv.reader(csvfile, delimiter=',')
      next(nodeDataReader)
      for row in nodeDataReader:
        flowFields[f].append(float(row[firstDataCol]))
    
  # - Edit .msh
  os.chdir(meshesFolder)
  with open(meshInfo.geoFileName + '_v{0}.msh'.format(str(meshIte)), 'a') as f:
    for i, field in enumerate(gradFields):
      f.write \
      (
        addNodeDataIntoMsh(remeshingInfo.evaluationQuantity[i] + 'Gradient', field)
      )
    
    for i, field in enumerate(flowFields):
      f.write \
      (
        addNodeDataIntoMsh(remeshingInfo.evaluationQuantity[i], field)
      )
  
  # - Create a temporary version of the next .geo
  flowCreated = False
  while flowCreated == False: 
    with open(nextMeshInfo.geoFileName + '_v{0}.geo'.format(str(meshIte + 1)), 'w') as f:
      with open("{0}.geo".format(geoFileName)) as g:
        for line in g:
          f.write(line)
        
      f.write \
      ("""
Merge "{0}_v{1}.msh";
""".format(geoFileName, str(meshIte))
      )
    
      for i in range(len(gradFields)):
        f.write \
        ("""
Save View[{0}] '{1}{2}Gradient_v{3}.pos';
""".format(str(i), meshesFolder, remeshingInfo.evaluationQuantity[i], str(meshIte))
        )
           
      for i in range(len(flowFields)):
        f.write \
        ("""
Save View[{0}] '{1}{2}_v{3}.pos';
""".format(str(len(gradFields) + i), meshesFolder, remeshingInfo.evaluationQuantity[i], str(meshIte))
        )
  
    # - Remesh for points - Save views
    os.chdir(meshesFolder)
    os.system('gmsh {0}_v{1}.geo -0'.format(nextMeshInfo.geoFileName, meshIte + 1))

    # - Check all gradients and flows completed
    created = 0

    for i in range(len(gradFields)):
      if os.path.exists('{0}{1}Gradient_v{2}.pos'.format(meshesFolder, remeshingInfo.evaluationQuantity[i], str(meshIte))):
        created = created + 1

    for i in range(len(flowFields)):
      if os.path.exists('{0}{1}_v{2}.pos'.format(meshesFolder, remeshingInfo.evaluationQuantity[i], str(meshIte))):
        created = created + 1

    if created == (len(gradFields) + len(flowFields)):
      flowCreated = True
        
  #if boundaryQuads == True:
  #  for f, fieldName in enumerate(remeshingInfo.evaluationQuantity):
  #    os.system('quadVal.py {0}Gradient_v{1} {2} {3}'.format(fieldName, str(meshIte)))
  #    os.system('quadVal.py {0}_v{1} {2} {3}'.format(fieldName, str(meshIte)))

  file = open("{0}Gradient_v{1}.pos".format(remeshingInfo.evaluationQuantity[1], str(meshIte)), "r")
  lines = file.readlines()
  file.close()
  if ((len(lines) > 30000) and (historyRestart == False) and (meshIte - remeshingInfo.historyLevels >= 1)):  #30000
    historyRestart = True
    Obj.remeshingTechnique.fullHistoryRestartLevel = meshIte

  os.chdir(meshesFolder)

  if thresholdHistogram == True:
    #Modify radius of .pos file 
    for f, fieldName in enumerate(remeshingInfo.evaluationQuantity):
      file = open("{0}Gradient_v{1}.pos".format(fieldName, str(meshIte)), "r")
      lines = file.readlines()
      file.close()
      print ("Number of lines in {0}Gradient_v{1}.pos file: {2}".format(fieldName, str(meshIte), str(len(lines))))
            
      if (len(lines) < 20000):
        modifyPos('{0}Gradient_v{1}'.format(fieldName, str(meshIte)), str(remeshingInfo.histogramRadius[0]*characteristicLength))
      elif ((len(lines) >= 20000) and (len(lines) <= 30000)):
        modifyPos('{0}Gradient_v{1}'.format(fieldName, str(meshIte)), str(1.5*remeshingInfo.histogramRadius[0]*characteristicLength))
      else:
        if historyRestart == False:
          modifyPos('{0}Gradient_v{1}'.format(fieldName, str(meshIte)), str(1.5*remeshingInfo.histogramRadius[0]*characteristicLength))
        
  if (meshIte+1)<remeshingInfo.fullHistoryRestartLevel:
    if (meshIte+1)>remeshingInfo.historyLevels:
      minLevel = (meshIte+1)-remeshingInfo.historyLevels
      del mathEval[0:2*len(remeshingInfo.evaluationQuantity)]
          

  return flowFields, gradFields, mathEval, minLevel, historyRestart

def find_nth(word, letter, n):
  # return nth word of string 
  start = word.find(letter)
  while start >= 0 and n > 1:
    start = word.find(letter, start+len(letter))
    n -= 1
  return start

def createGradGeo(geofileLocation, geoFileName, minLevel, meshIte, remeshingInfo, nextMeshInfo, gradFields, flowFields, mathEval, historyRestart):
  # - Create the next .geo
  os.chdir(meshesFolder)

  lastFieldIndex = 0
  with open(geofileLocation, 'w') as f:
    with open("{0}.geo".format(geoFileName)) as g:
      for line in g:
        f.write(line)

    for j in range(minLevel,meshIte+1):
      for i in range(len(remeshingInfo.evaluationQuantity)):
        f.write \
        ("""
Merge "{0}Gradient_v{1}.pos";
""".format(remeshingInfo.evaluationQuantity[i], str(j))
        )

      for i in range(len(remeshingInfo.evaluationQuantity)):
        f.write \
        ("""
Merge "{0}_v{1}.pos";
""".format(remeshingInfo.evaluationQuantity[i], str(j))
        )  

    f.write \
    ("""
Mesh.CharacteristicLengthMin = {0};
Mesh.CharacteristicLengthMax = {1};
Mesh.CharacteristicLengthFactor = {2};
Mesh.CharacteristicLengthExtendFromBoundary = 0;
Mesh.Algorithm = 6;
""".format(nextMeshInfo.minMeshSize, nextMeshInfo.maxMeshSize,0.25)
    )
    
    for i in range((meshIte-minLevel+1)*2*len(remeshingInfo.evaluationQuantity)):
      f.write \
      ("""
Field[{0}] = PostView;
Field[{0}].IView = {1};
Field[{0}].CropNegativeValues = 0;
""".format(i+1, i)
      )
    
    lastFieldIndex = (meshIte-minLevel+1)*2*len(remeshingInfo.evaluationQuantity)
    
    listOfFields = []
    
    maxGrad=[]
    for fCount, fieldName in enumerate(remeshingInfo.evaluationQuantity):
      maxGrad.append([])
      file = open('{0}Gradient_v{1}'.format(fieldName, str(meshIte))+ ".pos", "r")
      lines = file.readlines()
      file.close()
      maxGradVal = 0
      for line in lines:
        line = line.strip()
    
        if(line.find("SL") != -1):
          startpos = line.find("{")
          compos = line.find(",",startpos+1)
          endpos = line.find("}",compos+1)
          sl1 = float(mid(line,startpos+1,compos-startpos-1))
          sl2 = float(mid(line,compos+1,endpos-compos-1))

          sl = math.sqrt(sl1*sl1+sl2*sl2)         

          if (sl>maxGradVal):
            maxGradVal = sl
        
        if(line.find("ST") != -1):
          startpos = line.find("{")
          compos1 = line.find(",",startpos+1)
          compos2 = line.find(",",compos1+1)
          endpos = line.find("}",compos2+1)
        
          st1 = float(mid(line,startpos+1,compos1-startpos-1))
          st2 = float(mid(line,compos1+1,compos2-compos1-1))
          st3 = float(mid(line,compos2+1,endpos-compos2-1))

          st = math.sqrt(st1*st1+st2*st2+st3*st3)         

          if (st>maxGradVal):
            maxGradVal = st

        if(line.find("SQ") != -1):
          startpos = line.find("{")
          compos1 = line.find(",",startpos+1)
          compos2 = line.find(",",compos1+1)
          compos3 = line.find(",",compos2+1)
          endpos = line.find("}",compos3+1)
        
          sq1 = float(mid(line,startpos+1,compos1-startpos-1))
          sq2 = float(mid(line,compos1+1,compos2-compos1-1))
          sq3 = float(mid(line,compos2+1,compos3-compos2-1))
          sq4 = float(mid(line,compos3+1,endpos-compos3-1))

          sq = math.sqrt(sq1*sq1+sq2*sq2+sq3*sq3+sq4*sq4)         

          if (sq>maxGradVal):
            maxGradVal = sq
      
      maxGrad[fCount] = [maxGradVal]

    gradcl = nextMeshInfo.minMeshSize

    if historyRestart == True:
      gradcl = (nextMeshInfo.lchar1 * 0.25)
    else:
      gradcl = (nextMeshInfo.lchar1)
      
    time.sleep(duration/1000)
    
    for i in range(len(remeshingInfo.evaluationQuantity)):
      mathEval.append("{0}*{2}/((F{1})+1e-3)".format(str(gradcl), str(lastFieldIndex + i - len(remeshingInfo.evaluationQuantity)), str(maxGrad[i][0])))
      
    for i in range(len(remeshingInfo.evaluationQuantity)):
      mathEval.append("{0}*({2}/(Fabs({3}-(F{1})+1e-3)+0.0001*{3}))^2".format(str(nextMeshInfo.lchar2), str(lastFieldIndex + i), str(max([abs(remeshingInfo.evaluationQuantityFreestreamValue[i]-Qlocal) for Qlocal in flowFields[i]])), str(remeshingInfo.evaluationQuantityFreestreamValue[i])))
    
    for i in range((meshIte-minLevel+1)*2*len(remeshingInfo.evaluationQuantity)):
      listOfFields.append(lastFieldIndex + i + 1)
      
      # Field[gradQ] = lchar1                        / (|gradQ| / max(|gradQ|)) 
      #              = (lc1 / meshIter*gradSmoother) * max(|gradQ|) / |gradQ|
      #              = (lc1 / meshIter*gradSmoother) * max(|gradQ|) / (|gradQ| + 1e-9)
      
      mathEvalF = mathEval[i]
      fPos = mathEval[i].index('F')+1
      if find_nth(mathEvalF, 'F', 2)>fPos:
        fPos = find_nth(mathEvalF, 'F', 2)+1
    
      bPos = mathEval[i].index(')')

      f.write \
      ("""
Field[{0}] = MathEval;
Field[{0}].F = "{1}";
""".format(str(lastFieldIndex + i + 1), str(mathEvalF[:fPos] + str(i+1) + mathEvalF[(bPos):]))
      )
      
      # Field[Q] = lchar2                        / (|Qinf-Q| / max(|Qinf-Q|))^2 
      #          = (lc2 / meshIter*flowSmoother) * (max(|Qinf-Q|) / |Qinf-Q|)^2
      #          = (lc2 / meshIter*flowSmoother) * (max(|Qinf-Q|) / (|Qinf-Q| + 1e-9)^2
            
    lastFieldIndex += (meshIte-minLevel+1)*2*len(remeshingInfo.evaluationQuantity)
    
    listOfFields.append(1000)

    f.write \
    ("""
Field[{0}] = Min;
Field[{0}].FieldsList = {{{1}}};
Background Field = {0};
""".format(str(lastFieldIndex + 1), ', '.join(str(lOF) for lOF in listOfFields))
    ) 

    if boundaryCL == True:
      #Append Characteristic Lengths to .geo

      with open("{0}.geo".format(geoFileName)) as g:    
        points = []
        for line in g:
          line = line.strip()
          
          if(line.find("Point on edge with BL") != -1):
            countstartpos = line.find("(")
            countendpos = line.find(")",countstartpos+1)
            locstartpos = line.find("{",countendpos+1)
            loccompos1 = line.find(",",locstartpos+1)
            loccompos2 = line.find(",",loccompos1+1)
            locendpos = line.find("}",loccompos2+1)
          

            pnum = float(mid(line,countstartpos+1,countendpos-countstartpos-1))
            xloc = float(mid(line,locstartpos+1,loccompos1-locstartpos-1))
            yloc = float(mid(line,loccompos1+1,loccompos2-loccompos1-1))
            zloc = float(mid(line,loccompos2+1,locendpos-loccompos2-1))
            
            points = points + [[pnum,xloc,yloc,zloc]]

      cl = nextMeshInfo.lchar1
      if nextMeshInfo.lchar2 < cl:
        cl = nextMeshInfo.lchar2

      if len(points)>0:
        f.write \
        ("""
Characteristic Length {{{0}}} = {1};
""".format(','.join(str(int(poi[0])) for poi in points), str(cl*5)))
      #// Recombine the triangles into quads
      #Recombine Surface 1;

    return mathEval, historyRestart

def createHessGeo(geoFile, evalQuantity, meshIte, geoFileName):
  # - Create the next .geo
  os.chdir(meshesFolder)
  with open(geoFile, 'w') as f:
    with open("{0}.geo".format(geoFileName)) as g:
      for line in g:
        f.write(line)
      
    with open("{0}Hessian_v{1}.pos".format(evalQuantity, meshIte)) as h:
      for line in h:
        f.write(line)
        
    f.write \
    ('''

// Apply the view as the current background mesh
Background Mesh View[0];

// Use bamg
Mesh.Algorithm=7;'''
     )
      
def createDispGeo(geoFileLocation, meshIte, displayQuantities, geoFile, geoFileName):
  # Create geo with Display fields
  with open(geoFileLocation + '_v{0}_Disp.geo'.format(str(meshIte + 1)), 'w') as f:
    with open("{0}.geo".format(geoFileName)) as g:
      for line in g:
        f.write(line)

    for i in range(len(displayQuantities)):
      f.write \
      ("""
Merge "{0}_v{1}.pos";

Merge "{0}Gradient_v{1}.pos";
""".format(displayQuantities[i], str(meshIte))
      )

      with open("{0}Hessian_v{1}.pos".format(displayQuantities[i], str(meshIte))) as h:
        for line in h:
          f.write(line)

  
def firstGenAMRTechnique(Obj, meshIter, lc):
  #  call first generation AMR technique 
  Obj.meshes[meshIter] = globals()['firstGen_' + Obj.remeshingTechnique.methodName](Obj, meshIter, lc)
  return Obj.meshes[meshIter]
  

def firstGen_gradientBased(Obj, meshIter, lc):
  # return characteristic length for first generation gradient based
  Obj.meshes[meshIter].lchar1 = lc[0]/Obj.remeshingTechnique.gradientSmoother
  Obj.meshes[meshIter].lchar2 = lc[1]/Obj.remeshingTechnique.flowSmoother
  return Obj.meshes[meshIter]

def firstGen_hessianBased(Obj, meshIter, lc):
  # return characteristic length for first generation hessian based
  Obj.meshes[meshIter].lchar1 = lc[0]/Obj.remeshingTechnique.gradientSmoother
  Obj.meshes[meshIter].lchar2 = lc[1]/Obj.remeshingTechnique.flowSmoother
  return Obj.meshes[meshIter]


def nextGenAMRTechnique(Obj, meshIter, lc):
  # call next generation AMR technique
  Obj.meshes[meshIter] = globals()['nextGen_' + Obj.remeshingTechnique.methodName](Obj, meshIter, lc)
  return Obj.meshes[meshIter]
  

def nextGen_gradientBased(Obj, meshIter, lc):
  # return characteristic length for next generation gradient based
  Obj.meshes[meshIter].lchar1 = lc[0]/(Obj.remeshingTechnique.gradientSmoother*(meshIter+1))
  Obj.meshes[meshIter].lchar2 = lc[1]/(Obj.remeshingTechnique.flowSmoother*(meshIter+1))
  return Obj.meshes[meshIter]

def nextGen_hessianBased(Obj, meshIter, lc):
  # return characteristic length for next generation hessian based
  Obj.meshes[meshIter].lchar1 = lc[0]/(Obj.remeshingTechnique.gradientSmoother*(meshIter+1))
  Obj.meshes[meshIter].lchar2 = lc[1]/(Obj.remeshingTechnique.flowSmoother*(meshIter+1))
  return Obj.meshes[meshIter]


def printSetupVariables(Obj):
  print('baseName: ' +str(Obj.baseName))
  print('configurationFile: ' +str(Obj.configurationFile))
  print('firstGeneration: ' +str(Obj.firstGeneration))
  print('noDimensions: ' +str(Obj.caseScenario.noDimensions))
  print('freestreamMach: ' +str(Obj.caseScenario.freestreamMach))
  print('characteristicLength: ' +str(Obj.caseScenario.characteristicLength))
  print('geoFile: ' +str(Obj.meshes[0].geoFile))
  print('minMeshSize: ' +str(Obj.meshes[0].minMeshSize))
  print('maxMeshSize: ' +str(Obj.meshes[0].maxMeshSize))
  print('methodName: ' +str(Obj.remeshingTechnique.methodName))
  print('noGenerations: ' +str(Obj.remeshingTechnique.noGenerations))
  print('flowSmoother: ' +str(Obj.remeshingTechnique.flowSmoother))
  print('gradientSmoother: ' +str(Obj.remeshingTechnique.gradientSmoother))
  print('initialFlowMultiplier: ' +str(Obj.remeshingTechnique.initialFlowMultiplier[0]))
  print('initialGradMultiplier: ' +str(Obj.remeshingTechnique.initialGradMultiplier[0]))
  print('histogramRadius: ' +str(Obj.remeshingTechnique.histogramRadius[0]))
  print('displayQuantities: ' +str(Obj.remeshingTechnique.displayQuantities))
  print('evaluationQuantity: ' +str(Obj.remeshingTechnique.evaluationQuantity))
  print('evaluationQuantityFreestreamValue: ' +str(Obj.remeshingTechnique.evaluationQuantityFreestreamValue))
  print('historyLevels: ' +str(Obj.remeshingTechnique.historyLevels))
  print('fullHistoryRestartLevel: ' +str(Obj.remeshingTechnique.fullHistoryRestartLevel))


def printStartup(Obj):
  # print start-up information
  print ("{0} SU2 Simulation ({1})".format(Obj.baseName, time.strftime('%H:%M:%S, %d/%m/%Y', time.localtime(time.time()))))
  if windowsOS == True:
    os.system('title {0}_{1}_Initialisation ({2})'.format(Obj.baseName, str(sys.argv[3]), time.strftime('%H:%M:%S, %d/%m/%Y', time.localtime(time.time()))))


def printCurrentRun(Obj, meshIte):
  print ("Generation {0} ({1})".format(str(meshIte), time.strftime('%H:%M:%S, %d/%m/%Y', time.localtime(time.time()))))
  if windowsOS == True:
    os.system("title {0}_{1}_Run{2} ({3})".format(Obj.baseName, str(sys.argv[3]), meshIte, time.strftime('%H:%M:%S, %d/%m/%Y', time.localtime(time.time()))))


def initialCharLen(Obj):
  lc1 = float(Obj.caseScenario.characteristicLength)
  lc1 = float(Obj.remeshingTechnique.initialGradMultiplier[0])*lc1
  lc2 = float(Obj.caseScenario.characteristicLength)
  lc2 = float(Obj.remeshingTechnique.initialFlowMultiplier[0])*lc2
  return lc1, lc2

def checkConvergence(meshIte):
  currentRunDir = runsFolder + 'run' + str(meshIte) + '/'
  lastRunDir = runsFolder + 'run' + str(meshIte-1) + '/'
  
  print("Checking Convergence")
  clLast, cdLast = findCLCD(lastRunDir)
  clCurrnet, cdCurrent = findCLCD(currentRunDir)

  # calculate delta
  clDelta = clCurrnet - clLast
  cdDelta = cdCurrent - cdLast
  clDelta = abs(clDelta)
  cdDelta = abs(cdDelta)
        
  # check delta below threshold
  print("Convergence - Cl delta: " + str(clDelta) + "		Cd delta: " + str(cdDelta))
  converged = False
  if clDelta<threshold and cdDelta<threshold:
    print("Solution Converged after " + str(meshIte) + " iterations.")
    converged = True
  return converged 


def findBaseName():
  #Select Run
  try: 
    if str(sys.argv[1]) == 'RAEInv':
      su2App = RAEInv
    elif str(sys.argv[1]) == 'RAEVis':
      su2App = RAEVis
    elif str(sys.argv[1]) == 'NPInv':
      su2App = NPInv
    elif str(sys.argv[1]) == 'NPVis':
      su2App = NPVis
    elif str(sys.argv[1]) == 'CYInv':
      su2App = CYInv
    elif str(sys.argv[1]) == 'CYVis':
      su2App = CYVis
  except:
    print('Base name not valid')
  return su2App


def findCLCD(runDir):
  # get data for last iteration
  os.chdir(runDir)
  file = open('forces_breakdown.dat', "r")
  lines = file.readlines()
  file.close()
        
  for line in lines:
    line = line.strip()
          
    if(line.find("Total CL:") != -1):
      startpos = line.find(":")
      endpos = line.find("|",startpos+1)
      cl = float(mid(line,startpos+1,endpos-startpos-1))
          
    if(line.find("Total CD:") != -1):
      startpos = line.find(":")
      endpos = line.find("|",startpos+1)
      cd = float(mid(line,startpos+1,endpos-startpos-1))

  return cl, cd


def getVTK(Obj, meshIte, projPath, meshFolder, curRunDir):
  try:
    input("Insert 'soln_volume.vtk' for current run into {0}, press enter to continue".format(str(curRunDir)))
  except SyntaxError:
    retrieveMeshes(Obj, meshIte, projPath,meshFolder, curRunDir)
    pass

# --- Classes ---
        
class SU2_setup:
  """A SU2 Simulation is seen as a SU2_setup object"""
  
  def __init__(self, baseName, configurationFile, caseScenario, meshes, remeshingTechnique, firstGeneration=0, noCPUs=1):
      
    # Name of the working folder
    self.baseName = baseName
    
    # Name of the configuration file
    self.configurationFile = configurationFile
      
    # Definition of the case scenario (in terms of physical parameters)
    self.caseScenario = caseScenario
     
    # Meshes used for each generation
    self.meshes = []
    self.meshes.append(meshes)
      
      
    # Remeshing technique to be employed
    self.remeshingTechnique = remeshingTechnique
    
    self.remeshingTechnique.checkRemeshingMethodArguments(self.caseScenario.noDimensions)
    
    # Index of the first mesh generation to be run (default = 0)
    self.firstGeneration = firstGeneration
      
    # Number of CPUs to be used for the job (default = 1 :: serial)
    self.noCPUs = noCPUs
      
  # Add full path info to mesh data (.geo and dependencies)
  def addFullPathToMeshData(self, meshesFolder):
    self.meshes[0].geoFile = meshesFolder + self.meshes[0].geoFile ##different 
    self.meshes[0].dependencyFiles = [meshesFolder + dpf for dpf in self.meshes[0].dependencyFiles]
    #return self.meshes[0].geoFile ##different

  # Returns the last Field entry in the original .geo file  
  def findLastFieldEntryInGeo(self):    
    lastFieldLine = -1
    with open(self.meshes[self.firstGeneration].geoFile + '_v' + str(self.firstGeneration) + '.geo', 'r') as f:     
      noL = -1
      for line in f:
        noL += 1
        if "Field[" in line:
          lastFieldLine = noL
        
    with open(self.meshes[self.firstGeneration].geoFile + '_v' + str(self.firstGeneration) + '.geo', 'r') as f:  
      noL = -1
      if lastFieldLine != -1:  
        for line in f: 
          noL += 1 
          if noL == lastFieldLine:
            return int(line.lstrip("Field[").split("]", 1)[0])
            break
      
    return 0
                
      
class CaseScenario:
  """A SU2 CaseScenario giving physics info about the run"""
    
  def __init__(self, freestreamMach, characteristicLength=1, noDimensions=3):
    # Free-stream Mach number
    self.freestreamMach = freestreamMach
      
    # Characteristic length of the body (default = 1 m)
    self.characteristicLength = characteristicLength
      
    # Number of spatial dimensions of the case scenario (default = 3D)
    self.noDimensions = noDimensions   


class GmshMesh:
  """A Gmsh Mesh"""
    
  def __init__(self, geoFile, dependencyFiles=[], minMeshSize=0, maxMeshSize=1e5, lchar1=None, lchar2=None, geoFileName=None):
    # Name of the .geo file
    self.geoFile = geoFile
      
    # Name of the dependency files (if any)
    self.dependencyFiles = []
    self.dependencyFiles.extend(dependencyFiles)
     
    # Minimum size allowed for a mesh element (default = unbounded)
    self.minMeshSize = minMeshSize
     
    # Maximum size allowed for a mesh element (default = unbounded)
    self.maxMeshSize = maxMeshSize
      
    # First characteristic length of a mesh (default = undefined)
    self.lchar1 = lchar1
      
    # Second characteristic length of a mesh (default = undefined)
    self.lchar2 = lchar2

    self.geoFileName=geoFile
      

class Remeshing:
  """A remeshing technique"""
    
  def __init__(self, methodName, noGenerations=1, gradientSmoother=5.0, flowSmoother=1.0, initialGradMultiplier=1.0, initialFlowMultiplier=1.0, histogramRadius=0.01,displayQuantities=None, evaluationQuantity=None, hessianQuantity=None, evaluationQuantityFreestreamValue=None, historyLevels=None, fullHistoryRestartLevel=None):
    # Name of the remeshing method to be utilized
    self.methodName = methodName
    self.checkMethodName()
      
    # Number of generations to perform (default = 1)
    # This number is absolute, defined regardless of the firstGeneration input
    self.noGenerations = noGenerations

    # Physical quantities to be displayed
    self.displayQuantities = displayQuantities

    # Physical quantities to be evaluated
    self.evaluationQuantity = evaluationQuantity
      
    # --- Parameters for the gradient based remeshing technique ---
    # Physical quantities involved in hessian calculation (default = undefined)
    self.hessianQuantity = hessianQuantity
      
    # Gradient smoother constant (default = 5)
    # Proposed values - 2D: 5, 3D: 2.5
    self.gradientSmoother = gradientSmoother
      
    # Flow smoother constant (default = 1)
    # Proposed values - 2D: 1, 3D: 2
    self.flowSmoother = flowSmoother

    # Initial gradient multiplication constant (default = 1)
    # Proposed values - 2D: 1, 3D: 1 
    self.initialGradMultiplier = initialGradMultiplier,
     
    # Initial flow multiplication constant (default = 1)
    # Proposed values - 2D: 1, 3D: 1
    self.initialFlowMultiplier = initialFlowMultiplier,

    # .pos modification radius (default = 1)
    # Proposed values - viscous: 0.05, inviscid: 0.01
    self.histogramRadius = histogramRadius,
      
    # Free-stream value for these quantities
    self.evaluationQuantityFreestreamValue = evaluationQuantityFreestreamValue

    # Full history level
    self.historyLevels = historyLevels

    # Level of full history restart level
    self.fullHistoryRestartLevel = fullHistoryRestartLevel
      
      
  # Checks that the method name is correct
  def checkMethodName(self):
    methodNames = ['gradientBased', 'hessianBased']
    if self.methodName not in methodNames:
      print ('\n{0} is not a valid remeshing method name'.format(self.methodName))
      print ('Valid entries are: {0}'.format(', '.join([mthd for mthd in methodNames])))
      exit()
        
  # Checks the validity of the arguments given to the remeshing technique
  def checkRemeshingMethodArguments(self, caseDimension):
    if self.methodName == 'gradientBased':
      self.checkGradientBasedRemeshingArguments(caseDimension)
    elif self.methodName == 'hessianBased':
      self.checkHessianBasedRemeshingArguments(caseDimension)
    
  # Checks the validity of the arguments given to the gradient-based remeshing technique
  def checkGradientBasedRemeshingArguments(self, caseDimension):
    if self.evaluationQuantity is None:
      self.evaluationQuantity = ['Mach']
      if caseDimension == 2:
        self.gradientSmoother = 5.0
        self.flowSmoother = 1.0
        self.initialGradMultiplier = 1.0
        self.initialFlowMultiplier = 1.0
      else:
        self.gradientSmoother = 2.5
        self.flowSmoother = 2.0  
        self.initialGradMultiplier = 1.0
        self.initialFlowMultiplier = 1.0
     
    self.checkEvaluationQuantityFreestreamValue()
      
  # Checks the validity of the arguments given to the hessian-based remeshing technique
  def checkHessianBasedRemeshingArguments(self, caseDimension):
    if self.evaluationQuantity is None:
      self.evaluationQuantity = ['Mach']
      if caseDimension == 2:
        self.gradientSmoother = 5.0
        self.flowSmoother = 1.0
        self.initialgradMultiplier = 1.0
        self.initialFlowMultiplier = 1.0
      else:
        self.gradientSmoother = 2.5
        self.flowSmoother = 2.0  
        self.initialGradMultiplier = 1.0
        self.initialFlowMultiplier = 1.0
      
    self.checkEvaluationQuantityFreestreamValue()      
                     
          
  # Check the validity of the free-stream values for given flow quantities
  def checkEvaluationQuantityFreestreamValue(self):
    if len(self.evaluationQuantity) == 0 and self.evaluationQuantityFreestreamValue is None:
      self.evaluationQuantityFreestreamValue = []
    
    if len(self.evaluationQuantity) != 0:
      if len(self.evaluationQuantity) > 1:
        for l in range(len(self.evaluationQuantity)):
            if self.evaluationQuantity[l] != self.displayQuantities[l]:
                print ('\EvaluationQuantity must be the first display quantities')
                sys.exit()
      elif len(self.evaluationQuantity)==1:
          if self.evaluationQuantity[0] != self.displayQuantities[0]:
              print ('\EvaluationQuantity must be the first display quantity')
              exit()
        
      if self.evaluationQuantityFreestreamValue is None:
        print ('\n evaluaitonQuantityFreestreamValue List is missing')
        exit()
      elif len(self.evaluationQuantityFreestreamValue) != len(self.evaluationQuantity):
        print ('\n evaluationQuantityFreestreamValue and evaluationQuantity Lists are not of the same size')     
        exit()
        
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

# ----------------------------- Input parameters ---------------------------- #

#fsplUK = SU2_setup \
#(
#    baseName = 'M1.1-Ap075-H10',
#    configurationFile = 'fsplUK',
#    firstGeneration = 0,
#    noCPUs = 120,
#    caseScenario = CaseScenario \
#    (
#        noDimensions = 3,
#        freestreamMach = 1.1,
#        characteristicLength = 6.6169
#    ),
#    meshes = GmshMesh \
#    (
#      geoFile = 'postAnsys-Ap075',
#      dependencyFiles = ['fsplUK-3B3-75deg.stl'],
#      minMeshSize = 1.0e-4,
#      maxMeshSize = 10
#    ), 
#    remeshingTechnique = Remeshing \
#    (
#        methodName = 'gradientBased',
#        noGenerations = 1,
#        gradientSmoother = 2.5,
#        displayQuantities = ['Mach', 'Pressure'],
#        evaluationQuantity = ['Mach'],
#        #flowSmoother = 1,
#        evaluationQuantityFreestreamValue = [0.775]
#    )
#)

# +++++++++++++++

RAEInv = SU2_setup \
(
    baseName = 'rae2822_Inv',
    configurationFile = 'RAE2822_Inv',
    firstGeneration = 0,
    noCPUs = 2,
    caseScenario = CaseScenario \
    (
        noDimensions = 2,
        freestreamMach = 0.729,
        characteristicLength = 1
    ),
    meshes = GmshMesh \
    ( 
        geoFile = 'RAE2822',
        minMeshSize = 0.00005,
        maxMeshSize = 15
    ),
    remeshingTechnique = Remeshing \
    (
        methodName = str(sys.argv[4]),
        noGenerations = 50,  #originally 4
        gradientSmoother = 10,
        flowSmoother = 1,
        initialGradMultiplier = 1,
        initialFlowMultiplier = 50,
        histogramRadius = 0.05,
        displayQuantities = ['Mach', 'Pressure'],
        evaluationQuantity = ['Mach', 'Pressure'],
        #hessianQuantity = ['Mach'],
        evaluationQuantityFreestreamValue = [0.729, 108987.77275],
        historyLevels = 1,     #set to 0 for full history
        fullHistoryRestartLevel = 100
    )
)

RAEVis = SU2_setup \
(
    baseName = 'rae2822_Vis',
    configurationFile = 'RAE2822_Vis',
    firstGeneration = 0,
    noCPUs = 2,
    caseScenario = CaseScenario \
    (
        noDimensions = 2,
        freestreamMach = 0.729,
        characteristicLength = 1
    ),
    meshes = GmshMesh \
    ( 
        geoFile = 'RAE2822',
        minMeshSize = 0.0005,
        maxMeshSize = 15
    ),
    remeshingTechnique = Remeshing \
    (
        methodName = str(sys.argv[4]),
        noGenerations = 45,  #originally 4
        gradientSmoother = 2.5,
        flowSmoother = 1,
        initialGradMultiplier = 0.05,
        initialFlowMultiplier = 10,
        histogramRadius = 0.001,
        displayQuantities = ['Mach', 'Pressure'],
        evaluationQuantity = ['Mach', 'Pressure'],
        #hessianQuantity = ['Mach'],
        evaluationQuantityFreestreamValue = [0.729,38779.2],
        historyLevels = 1,     #set to 0 for full history
        fullHistoryRestartLevel = 99
    )
)

NPInv = SU2_setup \
(
    baseName = '30N30P_Inv',
    configurationFile = '30N30P_Inv',
    firstGeneration = 0,
    noCPUs = 2,
    caseScenario = CaseScenario \
    (
        noDimensions = 2,
        freestreamMach = 0.2,
        characteristicLength = 1.0
    ),
    meshes = GmshMesh \
    ( 
        geoFile = '30N30P',
        minMeshSize = 1.0e-4,
        maxMeshSize = 10
    ),
    remeshingTechnique = Remeshing \
    (
        methodName = str(sys.argv[4]),
        noGenerations = 5,  #originally 4
        gradientSmoother = 5,
        displayQuantities = ['Mach', 'Pressure'],
        evaluationQuantity = ['Mach', 'Pressure'],
        evaluationQuantityFreestreamValue = [0.2, 108987.77275],
        historyLevels = 1,     #set to 0 for full history
        fullHistoryRestartLevel = 99
    )
)

NPVis = SU2_setup \
(
    baseName = '30N30P_Vis',
    configurationFile = '30N30P_Vis',
    firstGeneration = 0,
    noCPUs = 2,
    caseScenario = CaseScenario \
    (
        noDimensions = 2,
        freestreamMach = 0.2,
        characteristicLength = 1.0
    ),
    meshes = GmshMesh \
    ( 
        geoFile = '30N30P',
        minMeshSize = 1.0e-5,
        maxMeshSize = 10
    ),
    remeshingTechnique = Remeshing \
    (
        methodName = str(sys.argv[4]),
        noGenerations = 50,  #originally 4
        gradientSmoother = 5,
        flowSmoother = 15,
        initialGradMultiplier = 0.8,
        initialFlowMultiplier = 2,
        histogramRadius = 0.05,
        displayQuantities = ['Mach', 'Pressure','Y_Plus'],
        evaluationQuantity = ['Mach', 'Pressure','Y_Plus'],
        evaluationQuantityFreestreamValue = [0.2, 108987.77275,0],
        historyLevels = 1,     #set to 0 for full history
        fullHistoryRestartLevel = 99
    )
)

CYInv = SU2_setup \
(
    baseName = 'CYLINDER_Inv',
    configurationFile = 'CYLINDER_Inv',
    firstGeneration = 0,
    noCPUs = 2,
    caseScenario = CaseScenario \
    (
        noDimensions = 2,
        freestreamMach = 8.0,
        characteristicLength = 1.0
    ),
    meshes = GmshMesh \
    ( 
        geoFile = 'CYLINDER',
        minMeshSize = 0.005,
        maxMeshSize = 10
    ),
    remeshingTechnique = Remeshing \
    (
        methodName = str(sys.argv[4]),
        noGenerations = 5,  #originally 4
        gradientSmoother = 5,
        displayQuantities = ['Mach', 'Pressure'],
        evaluationQuantity = ['Mach', 'Pressure'],
        evaluationQuantityFreestreamValue = [8.0, 108987.77275],
        historyLevels = 1,     #set to 0 for full history
        fullHistoryRestartLevel = 99
    )
)

CYVis = SU2_setup \
(
    baseName = 'CYLINDER_Vis',
    configurationFile = 'CYLINDER_Vis',
    firstGeneration = 0,
    noCPUs = 2,
    caseScenario = CaseScenario \
    (
        noDimensions = 2,
        freestreamMach = 5.84,
        characteristicLength = 6.5
    ),
    meshes = GmshMesh \
    ( 
        geoFile = 'CYLINDER',
        minMeshSize = 1.0e-4,
        maxMeshSize = 5
    ),
    remeshingTechnique = Remeshing \
    (
        methodName = str(sys.argv[4]),
        noGenerations = 50,  #originally 4
        gradientSmoother = 5,
        flowSmoother = 15,
        initialGradMultiplier = 0.8,
        initialFlowMultiplier = 5,
        histogramRadius = 0.05,
        displayQuantities = ['Mach', 'Pressure','Y_Plus'],
        evaluationQuantity = ['Mach', 'Pressure','Y_Plus'],
        evaluationQuantityFreestreamValue = [5.84, 6.72567,0],
        historyLevels = 1,     #set to 0 for full history 
        fullHistoryRestartLevel = 100     
    )
)

# +++++++++++++++

# - List of SU2 simulations to run
su2Runs = []
su2App = findBaseName()
su2Runs.append(su2App)
checkEmail()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

### ----- BEGIN SU2RUNS LOOP ----- ####
for su2 in su2Runs:

  printSetupVariables(su2)
  printStartup(su2)

  # --- Initialisation ---
  mathEval= []
  historyRestart = False
  minLevel = 0


  meshesFolder = projectPath + 'Meshes/'
  runsFolder = projectPath + 'Runs/'
  createFoldersIfNonExisting([meshesFolder, runsFolder])
    
  # - Characteristic lengths of the problem
  lc1, lc2 = initialCharLen(su2)

  # - Mesh info
  setupMeshFolder(su2, meshesFolder)
  su2.addFullPathToMeshData(meshesFolder)
  su2.meshes[0] = firstGenAMRTechnique(su2, 0, [lc1, lc2])
  if su2.remeshingTechnique.historyLevels==0:
    su2.remeshingTechnique.historyLevels=su2.remeshingTechnique.noGenerations

  ### ----- LOOP ----- ####
  for meshIter in xrange(su2.firstGeneration, su2.remeshingTechnique.noGenerations):
    printCurrentRun(su2, meshIter)
    currentRunDir = runsFolder + 'run' + str(meshIter) + '/'

    # --- Meshing ---
    meshCase(su2, meshIter, meshesFolder)

    # --- Set-up next run folder ---
    createFoldersIfNonExisting([runsFolder + 'run' + str(meshIter)])        
    setupRunFolder(su2, meshIter, projectPath,meshesFolder, currentRunDir)
        
    if not externalSimulation:
      # - SU2 computation
      runSU2Computation(su2, meshIter,projectPath,meshesFolder, currentRunDir)
    else:
      getVTK(su2, meshIter, projectPath,meshesFolder, currentRunDir)
      
    # --- Check Convergence ---
    if meshIter > su2.firstGeneration:
      if checkConvergence(meshIter) == True:
        break

    # --- Update for next generation ---
    su2.meshes.append(su2.meshes[-1])
    su2.meshes[meshIter+1] = nextGenAMRTechnique(su2, meshIter+1, [lc1, lc2])

    # --- Paraview and AMR technique ---
    minLevel, mathEval, historyRestart = callAMRTechnique(currentRunDir, currentRunDir, su2, meshIter, meshesFolder, mathEval, minLevel, historyRestart)
        
    ### ----- END LOOP ----- ####

### ----- END SU2RUNS LOOP ----- ####

print ("Exiting remeshing.py ({0})\n".format(time.strftime('%H:%M:%S, %d/%m/%Y', time.localtime(time.time()))))
