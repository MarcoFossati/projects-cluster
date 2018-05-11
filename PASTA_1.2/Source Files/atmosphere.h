//###################################################################################
//	ATMOSPHERE MODULE
//###################################################################################
//
//	Function:	NRLMSISE00
//	Author:		B Parsonage - 2018
//	Input:		altitude:	User specified altitude (km)
//	Output:		P:			Atmospheric Pressure (N/m2)			
//				T:			Atmospheric Temperature (K)
//				rho:		Density (kg/m3)
//				Minf:		Mach Number
//				R:			gas constant (kg m2 s - 2 k - 1 mol - 1)
//				cp:			Specific heat capacity at constant Pressure (for air) (J/kgK)
//				gamma:		Ratio of specific heat capacities (for air)
//				Re0:		Reynolds Number
//				Kn:			Knudsen Number
//				T0:			Free Stream Stagnation point Temperature
//				P01:		Free Stream Stagnation point Pressure
//				s:			Speed Ratio
//				Cpmax:		Maximum Pressure Coefficient 
//
//	Notes:		Calculates atmospheric conditions at 1 specific time point (1/1/2000)
//
//	Changelog:	B Parsonage (1/2018) - Integrated into atmosphere.h header file, included in PASTA v1.1	
//
//	Code Structure:			Specify constants
//							Read data from atmospheric data table
//							Interpolate data table values
//							Calculate gas densities 
//							Calculate atmospheric properties
//
//###################################################################################


std::vector<double> NRLMSISE00(double altitude) {

	double cp = 1004.7;						//specific heat at constant pressure(AIR)[J / kgK]
	double Kb = 1.3806488e-23;				//boltzmann constant, m2 kg s - 2 k - 1
	double Nav = 6.023e23;					//avogadro constant
	double f = 1.660539040e-27;				//conversion factor atomic mass unit - kg
	double omega = 0.78;					//temperature viscosity power law coefficient
	double C1 = 1.458e-6;					//sutherland's law coefficient, kg/m-s-k^-0.5
	double C2 = 110.4;						//sutherland's law coefficient, k


	//molecular weights
	double mN2 = 28.01340;					//molar mass of nitrogen molecule, grams / mole
	double mO2 = 31.99880;					//molar mass of oxygen molecule, grams / mole
	double mO = mO2 / 2;					//molar mass of oxygen atom, grams / mole
	double mN = mN2 / 2;					//molar mass of Nitrogen atom, grams / mole
	double mAr = 39.9480;					//molar mass of Argon molecule, grams / mole
	double mHe = 4.0026020;					//molar mass of helium molecule, grams / mole
	double mH = 1.007940;					//molar mass of Hydrogen molecule, grams / mole

	//Read NRLMSISE-00 database
	std::ifstream input;
	input.open(mainDir + "NRLMSISE-00.txt"); //text file of 1000*9 database
	std::vector<std::vector<double>> NRLMSISE;
	NRLMSISE.resize(1000);
	for (int i = 0; i < 1000; ++i)
	{
		NRLMSISE[i].resize(9);
	}
	for (int L = 0; L<1000; L++) {
		input >> NRLMSISE[L][0] >> NRLMSISE[L][1] >> NRLMSISE[L][2] >> NRLMSISE[L][3] >> NRLMSISE[L][4] >> NRLMSISE[L][5] >> NRLMSISE[L][6] >> NRLMSISE[L][7] >> NRLMSISE[L][8];
	}

	//assign values from database
	std::vector<std::vector<double>> rhoi;
	rhoi.resize(1000);
	for (int i = 0; i < 1000; ++i)
	{
		rhoi[i].resize(7);
	}
	std::vector<double> Ti;
	Ti.resize(1000);
	for (int i = 0;i < 1000;i++) {
		rhoi[i][0] = NRLMSISE[i][5] * 1E6;
		rhoi[i][1] = NRLMSISE[i][1] * 1E6;
		rhoi[i][2] = NRLMSISE[i][2] * 1E6;
		rhoi[i][3] = NRLMSISE[i][3] * 1E6;
		rhoi[i][4] = NRLMSISE[i][6] * 1E6;
		rhoi[i][5] = NRLMSISE[i][7] * 1E6;
		rhoi[i][6] = NRLMSISE[i][8] * 1E6;
		Ti[i] = NRLMSISE[i][4];
	}

	//Interpolation to find values from database at the input altitude
	int x = floor(altitude);
	double arr1[] = { rhoi[x][0],rhoi[x][1],rhoi[x][2],rhoi[x][3],rhoi[x][4],rhoi[x][5],rhoi[x][6] };
	std::vector<double> valuesx(arr1, arr1 + sizeof(arr1) / sizeof(arr1[0]));
	double arr2[] = { rhoi[x + 1][0],rhoi[x + 1][1],rhoi[x + 1][2],rhoi[x + 1][3],rhoi[x + 1][4],rhoi[x + 1][5],rhoi[x + 1][6] };
	std::vector<double> valuesy(arr2, arr2 + sizeof(arr2) / sizeof(arr2[0]));
	std::vector<double> rhon(7);
	for (int i = 0;i < 7;i++) {
		rhon[i] = valuesx[i] + (altitude - x)*(valuesy[i] - valuesx[i]) / 1; //assuming database rows are per km
	}
	double Tx1 = Ti[x];
	double Tx2 = Ti[x + 1];
	double T = Tx1 + (altitude - x)*(Tx2 - Tx1) / 1; //assuming database rows are per km
	double sumRhon = rhon[0] + rhon[1] + rhon[2] + rhon[3] + rhon[4] + rhon[5] + rhon[6];

	//calculate percentages of gas densities
	std::vector<double> percentual(7);
	for (int i = 0; i < 7;i++) {
		percentual[i] = rhon[i] / sumRhon;
	}
	std::vector<double> coeffs1 = { 5.0 / 3.0, 5.0 / 3.0, 1.4, 1.4, 5.0 / 3.0, 5.0 / 3.0, 5.0 / 3.0 };
	double gamma = 0;
	for (int i = 0;i < 7;i++) {
		gamma += percentual[i] * coeffs1[i];
	}
	
	//fraction disitribution
	double xN2 = percentual[2];
	double xO2 = percentual[3];
	double xO = percentual[1];
	double xN = percentual[6];
	double xAr = percentual[4];
	double xHe = percentual[0];
	double xH = percentual[5];

	double m = mN2*xN2 + mO2*xO2 + mO*xO + mN*xN + mAr*xAr + mHe*xHe + mH*xH;	//atmosphere molecular weight
	double rho = 0;
	std::vector<double> mw = { mHe, mO, mN2, mO2, mAr, mH, mN };
	for (int i = 0;i < 7;i++) {
		rho += rhon[i] * mw[i] / 6.022169e26;									//atmospheric density
	}
	
	double R = cp * (gamma - 1) / gamma;										//gas constant, kg m2 s - 2 k - 1 mol - 1
	double P = rho*R*T;															//atmospheric pressure

	double amu = 1.66053892e-27;												//fmf properties 
	double mg = m*amu;
	double k = 2.64638e-3 * pow(T, 1.5) / (T + 245 * pow(10, (-12 / T)));		//thermal conductivity coefficient
	double mu = 1.458e-6 * pow(T, 1.5) / (T + 110.4);							//dynamic viscosity
	double c = sqrt((gamma*P) / rho);											//speed of sound

	double Minf = norm(Vinfi) / c;												//mach number

	//Free Stream Stagnation Pressure and Temperature
	double P01 = P * pow((1 + 0.5*(gamma - 1)*pow(Minf, 2)), (gamma / (gamma - 1)));
	double T0 = T * (1 + 0.5 * (gamma - 1)*pow(Minf, 2));

	double Tw = T*(1 + (gamma - 1) / (2 * pow(Minf, 2)));	//Surface Temperature(original formula)

	double mu_T0 = mu* pow((T0 / T), omega);
	double rhos = rho*pow((T0 / T), (1. / (gamma - 1)));
	double rhow = P / R / Tw;								//Assuming constant pressure in the boundary layer
	double mu_w = (C1*pow(Tw, (3.0 / 2.0))) / (Tw + C2);
	double hw = cp*Tw;
	double h0 = cp*T0;

	//Stagnation Pressure after Normal Shock
	double P02 = P01 * pow((((gamma + 1)*pow(Minf, 2)) / ((gamma - 1)*pow(Minf, 2) + 2)), (gamma / (gamma - 1))) * pow(((gamma + 1) / (2 * gamma*pow(Minf, 2) - (gamma - 1))), (1 / (gamma - 1)));
	double Cpmax = (2 / (gamma*pow(Minf, 2)))*((P02 / P - 1)); //Cp maximum

	//FMF properties 
	double vmp = sqrt(2 * Kb*T / mg);
	double s = Vinf / vmp;							//Speed ratio
	double l = (mu / P)*sqrt(PI*Kb*T / (2 * mg));	//Mean free path [m]
	double Kn = l / lref;							//Knudsen Number
	double Pr = mu*cp / k;							//Prandtl number
	double Re0 = rho *Vinf * rN / mu_T0;			//Reynolds Number

	//Heat Transfer Models
	double dudx = (1 / rN)*sqrt(2 * (P01 - P) / rhos);									//Fay and Riddell Parameter
	double Qsfr = 0.76*(pow(Pr, -0.6))*(pow((rhos*mu_T0), 0.4))*(pow(rhow*mu_w, 0.1))*sqrt(dudx)*(h0 - hw);
	double Qsfr1 = 0.94*(pow(rho*mu, 0.4))*(pow(rhow*mu_w, 0.1))*sqrt(dudx)*(h0 - hw);	//Fay Riddell
	double Qsfr2 = 0.94*(pow(rho*mu, 0.5))*sqrt(dudx)*(h0 - hw);						//Van Driest

	//Compile function output
	std::vector<double> ATMOS = { P, T, rho, Minf, R, cp, gamma, Re0, Kn, T0, P01, s, Cpmax };
	return ATMOS;
}

//###################################################################################
//
//	Function:	USSA76
//	Author:		B Parsonage - 2018
//	Input:		altitude:	User specified altitude (km)
//	Output:		P:			Atmospheric Pressure (N/m2)			
//				T:			Atmospheric Temperature (K)
//				rho:		Density (kg/m3)
//				Minf:		Mach Number
//				R:			gas constant (kg m2 s - 2 k - 1 mol - 1)
//				cp:			Specific heat capacity at constant Pressure (for air) (J/kgK)
//				gamma:		Ratio of specific heat capacities (for air)
//				Re0:		Reynolds Number
//				Kn:			Knudsen Number
//				T0:			Free Stream Stagnation point Temperature
//				P01:		Free Stream Stagnation point Pressure
//				s:			Speed Ratio
//				Cpmax:		Maximum Pressure Coefficient 
//
//	Notes:		
//
//	Changelog:	B Parsonage (1/2018) - Integrated into atmosphere.h header file, included in PASTA v1.2
//
//	Code Structure:			Specify constants
//							Read data from atmospheric data table
//							Interpolate data table values
//							Calculate gas densities 
//							Calculate atmospheric properties
//
//###################################################################################

std::vector<double> USSA76(double altitude) {

	//Constants
	double cp = 1004.7;						//specific heat at constant pressure(AIR)[J / kgK]
	double gamma = 1.4;						//Ratio of specific heat for air
	double Kb = 1.3806488e-23;				//boltzmann constant, m2 kg s - 2 k - 1
	double Nav = 6.023e23;					//avogadro constant
	double f = 1.660539040e-27;				//conversion factor atomic mass unit - kg
	double omega = 0.78;					//temperature viscosity power law coefficient
	double C1 = 1.458e-6;					//sutherland's law coefficient, kg/m-s-k^-0.5
	double C2 = 110.4;						//sutherland's law coefficient, k
	double m = 28.9644;						//Mean molecular weight [kg/kmol] - Homogenously mixed							

	//Read NRLMSISE-00 database
	std::ifstream input;
	input.open(mainDir + "USSA76.txt"); //text file of 1000*4 database
	std::vector<std::vector<double>> USSA;
	USSA.resize(1000);
	for (int i = 0; i < 1000; ++i)
	{
		USSA[i].resize(4);
	}
	for (int L = 0; L<1000; L++) {
		input >> USSA[L][0] >> USSA[L][1] >> USSA[L][2] >> USSA[L][3];
	}

	/*
	//assign values from database
	std::vector<double> Ti;		//Temperature matrix
	std::vector<double> Pi;		//Pressure Matrix
	std::vector<double> rhoi;	//Densiy Matrix
	std::vector<double> ci;		//Speed of Sound Matrix

	Ti.resize(1000);
	Pi.resize(1000);
	rhoi.resize(1000);
	ci.resize(1000);
	
	
	for (int i = 0;i < 1000;i++) {
		Ti[i] = USSA[i][0];
		Pi[i] = USSA[i][1];
		rhoi[i] = USSA[i][2];
		ci[i] = USSA[i][3];
	}
	*/

	//Interpolation to find values from database at the input altitude
	std::vector<double> values(4);
	int upper = (int)ceil(altitude);
	int lower = (int)floor(altitude);

	for (int i = 0;i < 4;i++) {
		if (upper == lower) {
			values[i] = USSA[upper][i];
		}
		else {
			double valuesx = USSA[lower][i];
			double valuesy = USSA[upper][i];
			values[i] = valuesx + (altitude - lower)*(valuesy - valuesx) / (upper - lower);
		}
	}

	double T = values[0];
	double P = values[1];
	double rho = values[2];
	double c = values[3];


	//Calculations
	double R = cp * (gamma - 1) / gamma;
	double Minf = norm(Vinfi) / c;														//mach number
	double P01 = P * pow((1 + 0.5*(gamma - 1)*pow(Minf, 2)), (gamma / (gamma - 1)));	//Free stream stagnation pressure
	double T0 = T * (1 + 0.5 * (gamma - 1)*pow(Minf, 2));								//Free stream stagnation temperature
	double P02 = P01 * pow((((gamma + 1)*pow(Minf, 2)) / ((gamma - 1)*pow(Minf, 2) + 2)), (gamma / (gamma - 1))) * pow(((gamma + 1) / (2 * gamma*pow(Minf, 2) - (gamma - 1))), (1 / (gamma - 1))); //Stagnation Pressure after normal shock
	double Cpmax = (2 / (gamma*pow(Minf, 2)))*((P02 / P - 1));							//Cp maximum

	double amu = 1.66053892e-27;												//fmf properties 
	double mg = m * amu;
	double k = 2.64638e-3 * pow(T, 1.5) / (T + 245 * pow(10, (-12 / T)));		//thermal conductivity coefficient
	double mu = 1.458e-6 * pow(T, 1.5) / (T + 110.4);							//dynamic viscosity
	double mu_T0 = mu * pow((T0 / T), omega);

	double vmp = sqrt(2 * Kb*T / mg);
	double s = Vinf / vmp;							//Speed ratio
	double l = (mu / P)*sqrt(PI*Kb*T / (2 * mg));	//Mean free path [m]
	double Kn = l / lref;							//Knudsen Number
	double Pr = mu * cp / k;						//Prandtl number
	double Re0 = rho * Vinf * rN / mu_T0;			//Reynolds Number


	//Compile function output
	std::vector<double> ATMOS = { P, T, rho, Minf, R, cp, gamma, Re0, Kn, T0, P01, s, Cpmax };
	return ATMOS;
}