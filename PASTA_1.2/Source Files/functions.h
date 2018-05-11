//###################################################################################
//	FUNCTIONS MODULE
//###################################################################################
//
//	Functions:	parse_float, parse, dot, cosd, sind, acosd, asind, tand, atand, norm, 
//				vecbyscal, length, vec_elem_math, cross
//	Author:		B Parsonage - 2018		
//	Notes:
//	Changelog:				
//
//###################################################################################


float parse_float(std::ifstream& s) {
	char f_buf[sizeof(float)];
	s.read(f_buf, 4);
	float* fptr = (float*)f_buf;
	return *fptr;
}

std::vector<double> parse(std::ifstream& s) {
	double x = (double)parse_float(s);
	double y = (double)parse_float(s);
	double z = (double)parse_float(s);
	std::vector<double> points = { x,y,z };
	return points;
}

double dot(std::vector<double> v1, std::vector<double> v2) { //dot product of v1 and v2 (assuming 1*3 vectors)
	double dotproduct = (v1[0] * v2[0]) + (v1[1] * v2[1]) + (v1[2] * v2[2]);
	return dotproduct;
}

double cosd(double A) { //cosine of an angle in degrees
	double value = cos((PI / 180)*A);
	return value;
}

double sind(double A) { //sine of an angle in degrees
	double value = sin((PI / 180)*A);
	return value;
}

double acosd(double A) { //inverse cosine, returns an angle in degrees
	double value = acos(A);
	return value*(180 / PI);
}

double asind(double A) { //inverse sine, returns an angle in degrees
	double value = asin(A);
	return value*(180 / PI);
}

double tand(double A) { //tan of an angle in degrees
	double value = tan((PI / 180)*A);
	return value;
}

double atand(double A) { //inverse tan, returns an angle in degrees
	double value = atan(A);
	return value*(180 / PI);
}

double norm(std::vector<double> v) { //Euclidean length of 1*3 vector v
	double value = sqrt(pow(v[0], 2) + pow(v[1], 2) + pow(v[2], 2));
	return value;
}

std::vector<double> vecbyscal(std::vector<double> A, double B) { //Multiplys vector A by scalar B
	std::vector<double> values(3);
	values[0] = A[0] * B;
	values[1] = A[1] * B;
	values[2] = A[2] * B;
	return values;
}

double length(std::vector<double> v1, std::vector<double> v2) { //calculates the length between two 3D coordinates (tested OK)
	double value = sqrt(pow(v2[0] - v1[0], 2) + pow(v2[1] - v1[1], 2) + pow(v2[2] - v1[2], 2));
	return value;
}

std::vector<double> vec_elem_math(std::vector<double> v1, std::vector<double> v2, int A) { //element-wise maths - A( 1=add, 2=subract, 3=multiply, 4=divide) 
	std::vector<double> values(3);
	if (A == 1) {
		values[0] = v1[0] + v2[0];
		values[1] = v1[1] + v2[1];
		values[2] = v1[2] + v2[2];
	}
	else if (A == 2) {
		values[0] = v1[0] - v2[0];
		values[1] = v1[1] - v2[1];
		values[2] = v1[2] - v2[2];
	}
	else if (A == 3) {
		values[0] = v1[0] * v2[0];
		values[1] = v1[1] * v2[1];
		values[2] = v1[2] * v2[2];
	}
	else if (A == 4) {
		values[0] = v1[0] / v2[0];
		values[1] = v1[1] / v2[1];
		values[2] = v1[2] / v2[2];
	}
	return values;
}

std::vector<double> cross(std::vector<double> v1, std::vector<double> v2) {
	std::vector<double> values(3);
	values[0] = (v1[1] * v2[2]) - (v1[2] * v2[1]);
	values[1] = (v1[2] * v2[0]) - (v1[0] * v2[2]);
	values[2] = (v1[0] * v2[1]) - (v1[1] * v2[0]);
	return values;
}


//std::vector<double> NRLMSISE00(double altitude); //declare atmosphere function

//std::vector<double> Aero_hyp(double s, double T, double Cpmax, std::vector<int> BFC); // Declare hypersonic aerodynamics function

//std::vector<std::vector<double>> Aerothermo_hyp(std::vector<double> ATMOS, std::vector<int> BFC);

//std::vector<double> Aero_ss(double T, double P, double rho, double cp, double gamma, double T0, double P01, double Minf, double R);

