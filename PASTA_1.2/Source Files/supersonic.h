//###################################################################################
//	SUPERSONIC AERODYNAMICS MODULE
//###################################################################################
//
//	Function:	Aero_ss	
//	Author:		M Kelly - 2018
//	Input:		ATMOS:	Vector of atmospheric properties, as produced by the atmosphere module of PASTA 1.1
//				HSR:	Vector of Hidden Surface Reomval results (i.e. 1 = the triangle IS seen by the flow,
//						0 = the triangle is NOT seen by the flow)	
//	Output:		CD:		Coefficient of Drag
//				CS:		Coefficient of Sideslip
//				CL:		Coefficient of Lift
//				CP:		Distribution vector of Pressure coefficient
//	Notes:
//
//	Changelog:	B Parsonage (1/2018) - Integrated into supersonic_aero.h header file, included in PASTA v1.1	
//
//	Code Structure:		
//
//
//###################################################################################
std::vector<std::vector<double>> Aero_ss(std::vector<double> ATMOS, std::vector<int> HSR) {

	double P = ATMOS[0], T = ATMOS[1], rho = ATMOS[2], Minf = ATMOS[3], R = ATMOS[4], cp = ATMOS[5], gamma = ATMOS[6], Re0 = ATMOS[7], Kn = ATMOS[8], T0 = ATMOS[9], P01 = ATMOS[10], s = ATMOS[11], Cpmax = ATMOS[12];

	double deltamax = 0.1113*pow(Minf, 6) - 2.1468*pow(Minf, 5) + 16.517*pow(Minf, 4) - 63.501*pow(Minf, 3) + 121.43*pow(Minf, 2) - 84.109*Minf + 10.76;
	std::vector<double> CP(num_triangles);

	// VECTORS NEEDED OUTSIDE FOR LOOP
	std::vector<double> Lift(num_triangles);	//create array of lift force
	std::vector<double> Drag(num_triangles);	//create array of drag force
	std::vector<double> Side(num_triangles);	//create array of drag force
	std::vector<double> Cc(3);

	// Zero vectors for now with no heat transfer
	std::vector<double> Q(num_triangles);
	std::vector<double> Total_heat(num_triangles);

	// Variables needed outside loop
	double  gm1 = gamma - 1;
	double  gp1 = gamma + 1;
	double  Msq = pow(Minf, 2); //Mach number squared, regularly used

	//Start of triangles analysis
	for (int t = 0; t < num_triangles; t++) {
		if (HSR[t] == 1) {
			double theta = acosd(dot(vecbyscal(normals[t], -1), Vinfi) / norm(vecbyscal(normals[t], -1)) / norm(Vinfi)); //angle between normal and free stream velocity vector
			double delta = 90 - theta;		//Local Inclination Angle, degrees
			Q[t] = 0;


			if (delta < deltamax)
			{
				// Beta Calculation
				double deltarad = delta * PI / 180;		// Deflection in radians
				double deltarad2 = deltarad * deltarad;	//Squared
				double b1 = pow((Msq - 1), -0.5);		//Coefficients for calculation
				double b2 = gp1 * pow(Msq, 2)*deltarad;
				double b3 = 4 * pow((Msq - 1), 2);
				double b4 = b1 + b2 / b3;
				double b5 = pow((gp1 / 4), 2);
				double b6 = pow(Msq, 4) + 4 * pow(Msq, 3);
				double b7 = pow((Msq - 1), 3.5);
				double b = b4 + (0.5*b5*(b6 / b7)*deltarad2);
				double BetaOS = atand(b);				// Shock wave angle, degrees
			}
			else
			{
				double BetaOS = delta;
			}

			// Pressure Coefficient
			double Mns = ((0.87*Minf - 0.544)*sind(delta)) + 0.53;
			CP[t] = (48 * Mns*Mns*sind(delta)*sind(delta)) / ((23 * Mns*Mns) - 5);

			// Converting to normal
			std::vector<double> Cpnc = vecbyscal(vecbyscal(normals[t], -1), CP[t] * areas[t]);
			Cc = vec_elem_math(Cc, Cpnc, 1);
		}
	}//end of triangles analysis

	Cc = vecbyscal(Cc, (1.0 / Sref)); //these 4 are vector divided by scaler ie *1/scaler ###CHANGE THIS LATER###

	// Calculate coefficients
	double CD = dot(Cc, B2WA[0]);
	double CS = dot(Cc, B2WA[1]);
	double CL = dot(Cc, B2WA[2]);
	double Qav = 0;

	std::vector<double> Results = { CL, CD, CS };
	std::vector<std::vector<double>> FullResults = { CP, Results };
	return FullResults;
}
