//###################################################################################
//	HYPERSONIC AERODYNAMICS MODULE
//###################################################################################
//
//	Function:	Aero_hyp	
//	Author:		B Parsonage - 2018
//	Input:		ATMOS:	Vector of atmospheric properties, as produced by the atmosphere module of PASTA 1.1
//				HSR:	Vector of Hidden Surface Reomval results (i.e. 1 = the triangle IS seen by the flow,
//						0 = the triangle is NOT seen by the flow)
//	Output:		CDc:	Coefficient of Drag, continuum regime
//				CSc:	Coefficient of Sideslip, continuum regime
//				CLc:	Coefficient of Lift, continuum regime
//				CDfm:	Coefficient of Drag, free-molecular regime
//				CSfm:	Coefficient of Sideslip, free- molecular regime
//				CLfm:	Coefficient of Lift, free-molecular regime
//				Mlc:	Rolling moment coefficient, continuum regime		
//				Mmc:	Pitching moment coefficient, continuum regime			
//				Mnc:	Yaw moment coefficient, continuum regime		
//				Mlfm:	Rolling moment coefficient, free-molecular regime	
//				Mmfm:	Pitching moment coefficient, free-molecular regime		
//				Mnfm:	Yaw moment coefficient, free-molecuar regime	
//				CP:		Distribution vector of Pressure coefficient
//
//	Notes:
//
//	Changelog:		B Parsonage (1/2018) - Integrated into hypersonic_aero.h header file, included in PASTA v1.1	
//
//	Code Structure:		For each triangle:
//							if the triangle is 'seen':
//								Calculate local incliation angle
//								Continuum aerodynamic calculations (Modified Newtonian Theory)
//								Free-Molecular aerodynamic calculations (Schaaf and Chambre's analytical model)
//						Compile final coefficients
//						Output results
//
//
//###################################################################################

std::vector<std::vector<double>> Aero_hyp(std::vector<double> ATMOS, std::vector<int> HSR) {

	 double T = ATMOS[1], s = ATMOS[11], Cpmax = ATMOS[12];


	std::vector<double> Cc(3), Cfm(3), Mc(3), Mfm(3);
	std::vector<double> Cpc(num_triangles);
	std::vector<double> Cpfm(num_triangles);
	std::vector<double> r(3);

	for (int t = 0; t < num_triangles; t++) {

		if (HSR[t] == 1) {

			double theta = acosd(dot(vecbyscal(normals[t], -1), Vinfi) / norm(vecbyscal(normals[t], -1)) / norm(Vinfi)); //angle between normal and free stream veocity vector
			double delta = 90 - theta;											//Local Inclination Angle
			r = vec_elem_math(incentres[t], CG, 2);		//Moment Arm (incentre of triangle - COG of ENTIRE GEOMETRY)

			//Continuum Aerodynamics
			if (delta > 0) {
				Cpc[t] = Cpmax*pow(sind(delta), 2);
			}
			std::vector<double> Cpnc = vecbyscal(vecbyscal(normals[t], -1), Cpc[t] * areas[t]);
			Cc = vec_elem_math(Cc, Cpnc, 1);
			Mc = vec_elem_math(Mc, cross(r, Cpnc), 1);

			//Free-Molecular Aerodynamics 
			double thetaA = asind(dot(vecbyscal(Vinfni, -1), normals[t]));

			std::vector<double> tt = { 0, 0, 0 };
			//double Cpfm = 0;
			double Ctfm = 0;
			double Cpfm1, Cpfm2;

			if (thetaA == 0) {
				tt = vecbyscal((vec_elem_math(vecbyscal(normals[t], dot(Vinfi, normals[t])), Vinfi, 2)), 1.0 / (sqrt(1 - pow(dot(Vinfi, normals[t]), 2)))); //sorry this is overly confusing ###FIX THIS LATER###
				Ctfm = -(ST*cosd(thetaA) / s / sqrt(PI)) * (exp(-pow(s*sind(thetaA), 2) + sqrt(PI) * s *sind(thetaA)*(1 + erf(s*sind(thetaA))))); //double check erf is correct 
			}
			else if (thetaA == 90) {
				Cpfm1 = exp(-pow((s*sind(thetaA)), 2)) * ((2 - SN)*s*sind(thetaA) / sqrt(PI) + SN*sqrt(Twi / T) / 2);
				Cpfm2 = (1 + erf(s*sind(thetaA))) * ((2 - SN) * (pow((s*sind(thetaA)), 2) + 0.5) + 0.5*SN*s*sind(thetaA)*sqrt(PI*Twi / T));
				Cpfm[t] = (Cpfm1 + Cpfm2) / pow(s, 2);
			}
			else if ((thetaA != 0) && (thetaA != 90) && (thetaA != -90)) {
				tt = vecbyscal((vec_elem_math(vecbyscal(normals[t], dot(Vinfni, normals[t])), Vinfni, 2)), 1.0 / (sqrt(1 - pow(dot(Vinfni, normals[t]), 2))));
				Cpfm1 = exp(-pow(s*sind(thetaA), 2)) * ((2 - SN)*s*sind(thetaA) / sqrt(PI) + SN*sqrt(Twi / T) / 2);
				Cpfm2 = (1 + erf(s*sind(thetaA))) * ((2 - SN) * (pow(s*sind(thetaA), 2) + 0.5) + 0.5*SN*s*sind(thetaA)*sqrt(PI*Twi / T));
				Cpfm[t] = (Cpfm1 + Cpfm2) / pow(s, 2);
				Ctfm = -(ST*cosd(thetaA) / s / sqrt(PI)) * (exp(-pow(s*sind(thetaA), 2)) + sqrt(PI) *s *sind(thetaA)*(1 + erf(s*sind(thetaA))));
			}

			std::vector<double> Cpnfm = vecbyscal(vecbyscal(normals[t], -1), Cpfm[t] * areas[t]);
			std::vector<double> Cttfm = vecbyscal(tt, areas[t] * Ctfm);
			Cfm = vec_elem_math(vec_elem_math(Cfm, Cpnfm, 1), Cttfm, 1); //really annoying but this is just Cfm + Cpnfm + Cttfm
			Mfm = vec_elem_math(Mfm, cross(r, vec_elem_math(Cpnfm, Cttfm, 1)), 1);
		}
	}

	//Computation of Aerodynamics bridging parameters
	Cc = vecbyscal(Cc, 1.0 / Sref); //these 4 are vector divided by scaler ie *1/scaler ###CHANGE THIS LATER###
	Cfm = vecbyscal(Cfm, 1.0 / Sref);
	Mc = vecbyscal(Mc, 1.0 / Sref / lref);
	Mfm = vecbyscal(Mfm, 1.0 / Sref / lref);
	double CDc = dot(Cc, B2WA[0]);
	double CSc = dot(Cc, B2WA[1]);
	double CLc = dot(Cc, B2WA[2]);
	double CDfm = dot(Cfm, B2WA[0]);
	double CSfm = dot(Cfm, B2WA[1]);
	double CLfm = dot(Cfm, B2WA[2]);
	double Mlc = dot(Mc, B2WA[0]);
	double Mmc = dot(Mc, B2WA[1]);
	double Mnc = dot(Mc, B2WA[2]);
	double Mlfm = dot(Mfm, B2WA[0]);
	double Mmfm = dot(Mfm, B2WA[1]);
	double Mnfm = dot(Mfm, B2WA[2]);

	std::vector<double> Results = { CDc, CSc, CLc, CDfm, CSfm, CLfm, Mlc, Mmc, Mnc, Mlfm, Mmfm, Mnfm };
	std::vector<std::vector<double>> FullResults = { Cpc, Cpfm, Results };
	return FullResults;
}

//##################################################################################
//
//	Function:	Aerothermo_hyp	
//	Author:		B Parsonage - 2018
//	Input:		ATMOS:	Vector of atmospheric properties, as produced by the atmosphere module of PASTA 1.1
//				HSR:	Vector of Hidden Surface Reomval results (i.e. 1 = the triangle IS seen by the flow,
//						0 = the triangle is NOT seen by the flow)
//	Output:		Total_heat:		Total heat transferred by each triangle (W)
//				Q:				Heat transfer coefficient for each triangle (W/m2)
//				St:				Stanton number for each triangle 
//
//	Notes:		- Transition regime aerothermodynamics are handles within PASTA 1.1, as these calculations
//				require the evaluation of continuum and free molecular values
//
//				- In the continuum regime, the Stanton number for each triangle is evaluated using the FOSTRAD 2.0 aerothermodynamics model. 
//				The XXX, XXX and XXX models are included for completeness, but are not used. To use any of these models 
//				in the heat transfer calcukations, simply replace the necessary stanton number reference in line XXX. 
//
//	Changelog:	B Parsonage (1/2018) - Integrated into hypersonic_aerothermo.h header file, 
//				included in PASTA v1.1	
//
//	Code Structure:		
//
//
//###################################################################################

std::vector<std::vector<double>> Aerothermo_hyp(std::vector<double> ATMOS, std::vector<int> HSR) {

	double P = ATMOS[0], T = ATMOS[1], rho = ATMOS[2], Minf = ATMOS[3], R = ATMOS[4], cp = ATMOS[5], gamma = ATMOS[6], Re0 = ATMOS[7], Kn = ATMOS[8], T0 = ATMOS[9], P01 = ATMOS[10], s = ATMOS[11], Cpmax = ATMOS[12];

	double Qstfm;
	std::vector<double> Q_fm(num_triangles), Stfm(num_triangles), Stfm1(num_triangles), Total_heat_fm(num_triangles), Chfm(num_triangles);
	std::vector<double> Q_c(num_triangles), Stsc(num_triangles), Stc(num_triangles), Stcfr(num_triangles), Stcfr_KDR(num_triangles), Stcfr_FOSTRAD20(num_triangles), Total_heat_c(num_triangles), Chc(num_triangles);
	std::vector<double> Q_Sc(num_triangles), Qfr(num_triangles), Q_KDR(num_triangles), Q_FOSTRAD20(num_triangles);

	std::vector<std::vector<double>> Results;

	for (int t = 0; t < num_triangles; t++) {

		if (HSR[t] == 1) {

			double theta = acosd(dot(vecbyscal(normals[t], -1), Vinfi) / norm(vecbyscal(normals[t], -1)) / norm(Vinfi)); //angle between normal and free stream veocity vector
			double delta = 90 - theta;											//Local Inclination Angle
			std::vector<double> r = vec_elem_math(incentres[t], COG[t], 2);		//Moment Arm (incentre of triangle - COG of ENTIRE GEOMETRY)

																				//Continuum Aerothermodynamics
			if (Kn < limKn_inf) {
				Stsc[t] = 2.1 / sqrt(Re0);													//Stagnation Point Stanton Number - SCARAB
																							//double Stsfr = Qsfr / rho / Vinf / (h0 - hw);								//Stanton Number - Fay Riddel
				if ((theta >= 0) && (theta <= 90)) {
					Stc[t] = Stsc[t] * (0.7*sind(delta));									//CHECK THIS FORMULA
					Stcfr[t] = Stsc[t] * (0.1 + 0.9*cosd(theta));							//Modified Lees(SCARAB)
					Stcfr_KDR[t] = Stsc[t] * pow(cosd(theta / 2), 5.27);					//Kemp Rose Detra
					Stcfr_FOSTRAD20[t] = Stsc[t] * 0.74 / 2.1 * (0.1 + 0.9*cosd(theta));	//FOSTRAD2.0
					if (Stcfr_FOSTRAD20[t] < 0) {
						Stcfr_FOSTRAD20[t] = 0;
					}
				}
				else {
					Stc[t] = 0;
					Stcfr[t] = 0;
					Stcfr_KDR[t] = 0;
					Stcfr_FOSTRAD20[t] = 0;
				}

				//Computing continuum heat transfer(Q[W / m ^ 2]) for different models
				Q_Sc[t] = Stc[t] * rho * Vinf* cp * (T0 - Twi);						//Scarab formulation[W / m ^ 2]
				Qfr[t] = Stcfr[t] * rho * Vinf * cp * (T0 - Twi);
				Q_KDR[t] = Stcfr_KDR[t] * rho * Vinf * cp * (T0 - Twi);
				Q_FOSTRAD20[t] = Stcfr_FOSTRAD20[t] * rho * Vinf * cp * (T0 - Twi);
				Q_c[t] = Q_FOSTRAD20[t];											//Heat Transfer[W / m ^ 2] continuum
				Total_heat_c[t] = Q_c[t] * areas[t];								//Therml flow (J / sec)
				Chc[t] = 2 * Q_c[t] / (rho*pow(Vinf, 3));							//Heat Transfer Coefficient

				Results = { Total_heat_c, Q_c , Stcfr_FOSTRAD20, Chc };
			}

			//FMF Aerothermodynamics 
			if (Kn >= limKn_sup) {
				Qstfm = 0.5 * AC * rho * pow(Vinf, 3);
				Q_fm[t] = (Qstfm / pow(s, 3) / 2 / sqrt(PI))*((pow(s, 2) + gamma / (gamma - 1) - ((gamma + 1)*Twi / 2 / (gamma - 1) / T))*(exp(-pow((s*sind(delta)), 2)) + sqrt(PI)*s*sind(delta)*(1 + erf(s*sind(delta)))) - 0.5*exp(-pow(s*sind(delta), 2))); //Kempra Fay Riddel,
				Stfm[t] = Q_fm[t] / (rho * Vinf * cp * (T0 - Twi));		//Heat Transfer Coefficient fm
				Stfm1[t] = Q_fm[t] / ((rho / 2)*pow(Vinf, 3));
				Total_heat_fm[t] = Q_fm[t] * areas[t];
				Chfm[t] = 2 * Q_fm[t] / (rho*pow(Vinf, 3));				//Heat Transfer Coefficient

				Results = { Total_heat_fm, Q_fm, Stfm1, Chfm };

			}
		}
	}
	return Results;
}
