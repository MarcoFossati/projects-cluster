alt = raw_input('> ')

searchfile = open(r"C:\Users\Andrew\Documents\University\4th Year\Individual Project\PycharmProjects\Atmos_Models\Model_1\si1py.prt", "r") #Location will need to be changed when downloaded!!!

for line in searchfile:
        list = line.strip().split()
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
            print "Altitude:",alt,"km",'\n','-'*25,"\nSigma:",sigma,"\nDelta:",delta,"\nTheta:",theta,'\n','-'*25,\
                "\nTemperature:",temp,"K","\nPressure:",press,"Pa","\nDensity:",dens,"kg/m^3","\nSoS:",c,"m/s","\nViscosity:",visc,"Pas","\nK. Viscosity:",kvisc,"m^2/s"
            exit(0)
        if list[0] != alt:
            lmin = int(float(alt)/2)*2
            lmax = lmin + 2
            lmins = str(lmin)
            lmaxs = str(lmax)
            if lmins == list[0]:
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
                print "Minimum Altitude:",alt,"km",'\n','-'*25,"\nSigma:",sigma,"\nDelta:",delta,"\nTheta:",theta,'\n','-'*25,\
                "\nTemperature:",temp,"K","\nPressure:",press,"Pa","\nDensity:",dens,"kg/m^3","\nSoS:",c,"m/s","\nViscosity:",visc,"Pas","\nK. Viscosity:",kvisc,"m^2/s"
            if lmaxs == list[0]:
                print "="*45
                alti = list[0]
                sigmai = list[1]
                deltai = list[2]
                thetai = list[3]
                tempi = list[4]
                pressi = list[5]
                densi = list[6]
                ci = list[7]
                visci = list[8]
                kvisci = list[9]
                print "Maximum Altitude:",alti,"km",'\n','-'*25,"\nSigma:",sigmai,"\nDelta:",deltai,"\nTheta:",thetai,'\n','-'*25,\
                "\nTemperature:",tempi,"K","\nPressure:",pressi,"Pa","\nDensity:",densi,"kg/m^3","\nSoS:",ci,"m/s","\nViscosity:",visci,"Pas","\nK. Viscosity:",kvisci,"m^2/s"