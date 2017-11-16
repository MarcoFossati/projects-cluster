alt = raw_input('> ')

searchfile = open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\si1py.prt", "r") #Location will need to be changed when downloaded!!!
for line in searchfile:
        list = line.strip().split(' ')
        if list[0] == alt:
            alt = list[0]
            sigma = list[1]
            delta = list[2]
            theta = list[3]
            temp = list[4]
            press = list[5]
            dens = list[6]
            c = list[7]
            visc = list[8]
            kvisc = list[9]
            print "Altitude:",alt,"km",'\n','-'*25,"\nSigma:",sigma,"\nDelta:",delta,"\nTheta:",theta,'\n','-'*25,"\nTemperature:",temp,"K"\
                "\nPressure:","Pa",press,"\nSoS:",c,"m/s","\nViscosity:",visc,"Pas","\nK. Viscosity:",kvisc,"m^2/s"
        #else:
            #interpolate to get data between known points
searchfile.close()