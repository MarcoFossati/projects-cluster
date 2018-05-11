//###################################################################################
//	GEOMETRY MODULE
//###################################################################################
//
//	Function:	STLread3D	
//	Author:		B Parsonage - 2018
//	Input:		gDir:		File path to the folder in which the geometry file is stored
//				STLname:	Name of the geometry file (must be a binary .STL file)
//	Output:		vertices:	3D coordinates of each vertex of the geometry
//				normals:	3D normal vector of each triangle of the geometry
//				COG:		3D coordinates of each triangle of the geometry
//				incentres:	3D coordinates of the incentre of each triangle of the geometry
//
//	Notes:		This function will read any binary STL file representing a 3D geometry
//				Further work will add support for 3D ASCII STL files
//
//	Changelog:	B Parsonage (1/2018) - Integrated into geometry.h header file, included in PASTA v1.1	
//
//	Code Structure:			- Opens the STL file
//							- Reads the header info (name of file, number of triangles etc)
//							- Creates/modifies the necessary vector arrays
//							- For each triangle of the geometry:
//								- Read the normal
//								- Read the vertices
//								- Calculate the centre point
//								- Calculate the incentre
//							- Output results
//
//###################################################################################
//
//	Function:	area	
//	Author:		B Parsonage - 2018
//	Input:		v1:	3D coordinates of the first vertwex of a triangle
//				v2:	3D coordinates of the second vertex of a triangle
//				v3:	3D coordinates of the third vertex of a triangle
//	Output:		area:	The area of the triangle represented by v1, v2, v3
//
//	Notes:		Stablilized Heron's Formula
//
//	Changelog:	B Parsonage (1/2018) - Integrated into geometry.h header file, included in PASTA v1.1	
//	
//	Code Structure:		- Calculate the lengths of each side of the triangle
//						- Sort the lengths so that a<=b<=c (necessary for Stabilized Heron's Formula)
//						- Calcuate the area of the triangle
//						- Output result
//
//###################################################################################
//
//	Function:	centreofgravity
//	Author:		B Parsonage - 2018
//	Input:		incentres:	3D coordinates of the incentre of each triangle of the geometry
//	Output:		CG:			3D coordinates of the centre point of the entire geometry
//	Notes:
//	Changelog:	B Parsonage (1/2018) - Integrated into geometry.h header file, included in PASTA v1.1		
//
//	Code Structure:		- Finds the average x,y and z coordinate of the incentres
//
//
//###################################################################################


std::vector<std::vector<std::vector<double>>> STLread3D(std::string gDir, std::string STLname) {

	std::string STLpath = gDir + STLname;


	//Check if file is Binary or ASCII
	int filetype = 0; //0 for ASCII, 1 for Binary
	std::ifstream file(STLpath.c_str());
	std::string line1, line2, facet = "facet";
	std::getline(file, line1);
	std::getline(file, line2);
	if (strncmp(line2.c_str(), facet.c_str(), facet.size()) == 0) {
		filetype = 1;
	}


	//Read Binary file
	if (filetype == 0) {
		std::ifstream stl_file(STLpath.c_str(), std::ios::in | std::ios::binary);
		if (!stl_file) {
			std::cout << "ERROR: COULD NOT READ FILE" << std::endl;
			assert(false);
		}
		char header_info[80] = "";
		char n_triangles[4];
		stl_file.read(header_info, 80);
		stl_file.read(n_triangles, 4);
		unsigned int* r = (unsigned int*)n_triangles;
		num_triangles = *r;

		//Create Normals array
		normals.resize(num_triangles);
		for (int i = 0; i < num_triangles; ++i)
		{
			normals[i].resize(num_columns);
		}

		//Create Vertices Array
		vertices.resize(num_triangles * 3);
		for (int i = 0; i < num_triangles * 3; ++i)
		{
			vertices[i].resize(num_columns);
		}

		//Create array of COG coordinates
		COG.resize(num_triangles);
		for (int i = 0; i < num_triangles; ++i)
		{
			COG[i].resize(num_columns);
		}

		//Create Areas Array
		areas.resize(num_triangles);

		//create array of incentres
		incentres.resize(num_triangles);
		for (int i = 0; i < num_triangles; ++i)
		{
			incentres[i].resize(num_columns);
		}

		for (unsigned int i = 0; i < num_triangles; i++) {

			//write normals
			std::vector<double> n = parse(stl_file);
			normals[i][0] = n[0];
			normals[i][1] = n[1];
			normals[i][2] = n[2];

			//write vertices
			std::vector<double> v1 = parse(stl_file);
			vertices[3 * i][0] = v1[0];
			vertices[3 * i][1] = v1[1];
			vertices[3 * i][2] = v1[2];
			std::vector<double> v2 = parse(stl_file);
			vertices[3 * i + 1][0] = v2[0];
			vertices[3 * i + 1][1] = v2[1];
			vertices[3 * i + 1][2] = v2[2];
			std::vector<double> v3 = parse(stl_file);
			vertices[3 * i + 2][0] = v3[0];
			vertices[3 * i + 2][1] = v3[1];
			vertices[3 * i + 2][2] = v3[2];

			char dummy[2];
			stl_file.read(dummy, 2);

			//write centre point of each face
			COG[i][0] = (v1[0] + v2[0] + v3[0]) / 3;
			COG[i][1] = (v1[1] + v2[1] + v3[1]) / 3;
			COG[i][2] = (v1[2] + v2[2] + v3[2]) / 3;

			// calculate coordinates of incentre
			double sideA = length(v2, v3);
			double sideB = length(v3, v1);
			double sideC = length(v1, v2);
			double perimeter = sideA + sideB + sideC;
			incentres[i][0] = (sideA*v1[0] + sideB*v2[0] + sideC*v3[0]) / perimeter; //length of the side multiplied by the vertex opposite the side
			incentres[i][1] = (sideA*v1[1] + sideB*v2[1] + sideC*v3[1]) / perimeter;
			incentres[i][2] = (sideA*v1[2] + sideB*v2[2] + sideC*v3[2]) / perimeter;

		}

		std::vector<std::vector<std::vector<double>>> Results = { vertices, normals, COG, incentres };
		return Results;
	}


	//Read ASCII
	if (filetype == 1) {
		num_triangles = 0; 
		std::string header_info, strng1, strng2;
		std::ifstream stl_file(STLpath.c_str());
		std::getline(stl_file, header_info);
		std::string test = "", endsolid = "endsolid";
		std::vector<double> V(3);
		//while (strncmp(test.c_str(), endsolid.c_str(), endsolid.size()) == 1) {
		while(strng1 != endsolid){
			stl_file >> strng1 >> strng2 >> V[0] >> V[1] >> V[2];
			if (strng1 == endsolid) {
				break;
			}
			normals.push_back(V);
			stl_file >> strng1 >> strng2;
			stl_file >> strng1 >> V[0] >> V[1] >> V[2];
			vertices.push_back(V);
			stl_file >> strng1 >> V[0] >> V[1] >> V[2];
			vertices.push_back(V);
			stl_file >> strng1 >> V[0] >> V[1] >> V[2];
			vertices.push_back(V);
			stl_file >> strng1;
			stl_file >> strng1;
			num_triangles = num_triangles + 1;
		}

		//Create array of COG coordinates
		COG.resize(num_triangles);
		for (int i = 0; i < num_triangles; ++i)
		{
			COG[i].resize(num_columns);
		}

		//Create Areas Array
		areas.resize(num_triangles);

		//create array of incentres
		incentres.resize(num_triangles);
		for (int i = 0; i < num_triangles; ++i)
		{
			incentres[i].resize(num_columns);
		}

		for (unsigned int i = 0; i < num_triangles; i++) {
			//write centre point of each face
			COG[i][0] = (vertices[i*3][0] + vertices[i*3 + 1][0] + vertices[i*3 + 2][0]) / 3;
			COG[i][1] = (vertices[i*3][1] + vertices[i*3 + 1][1] + vertices[i*3 + 2][1]) / 3;
			COG[i][2] = (vertices[i*3][2] + vertices[i*3 + 1][2] + vertices[i*3 + 2][2]) / 3;

			// calculate coordinates of incentre
			double sideA = length(vertices[i*3 +1], vertices[i*3 +2]);
			double sideB = length(vertices[i*3 +2], vertices[i*3]);
			double sideC = length(vertices[i*3], vertices[i*3 +1]);
			double perimeter = sideA + sideB + sideC;
			incentres[i][0] = (sideA*vertices[i*3][0] + sideB*vertices[i*3 +1][0] + sideC*vertices[i*3 +2][0]) / perimeter; //length of the side multiplied by the vertex opposite the side
			incentres[i][1] = (sideA*vertices[i*3][1] + sideB*vertices[i*3 +1][1] + sideC*vertices[i*3 +2][1]) / perimeter;
			incentres[i][2] = (sideA*vertices[i*3][2] + sideB*vertices[i*3 +1][2] + sideC*vertices[i*3 +2][2]) / perimeter;
		}
		std::vector<std::vector<std::vector<double>>> Results = { vertices, normals, COG, incentres };
		return Results;
	}

}

double area(std::vector<double> v1, std::vector<double> v2, std::vector<double> v3) {
	double sideA = length(v2, v3);
	double sideB = length(v3, v1);
	double sideC = length(v1, v2);

	//Calculate area from 3 vertices (Heron's formula)

	//		double s = 0.5*perimeter;
	//		areas[i] = sqrt(s*(s - sideA)*(s - sideB)*(s - sideA));		//Classic Heron's Formula

	double a, b, c;							//Sort triangle side lengths so a<=b<=c
	if (sideA >= sideB) {
		if (sideB >= sideC) {
			a = sideA;
			b = sideB;
			c = sideC;
		}
		else if (sideA >= sideC) {
			a = sideA;
			b = sideC;
			c = sideB;
		}
		else {
			a = sideC;
			b = sideA;
			c = sideB;
		}
	}
	else if (sideA >= sideC) {
		a = sideB;
		b = sideA;
		c = sideC;
	}
	else if (sideB >= sideC) {
		a = sideB;
		b = sideC;
		c = sideA;
	}
	else {
		a = sideC;
		b = sideB;
		c = sideA;
	}

	double area = 0.25*sqrt((a + (b + c))*(c - (a - b))*(c + (a - b))*(a + (b - c))); //Stabilized Heron's Formula (Tested OK)
	return area;
}

std::vector<double> centreofgravity(std::vector<std::vector<double>> incentres) {

	//Calculate COG of entire geometry
	std::vector<double> CG(3);
	std::vector<double>colSum(3);

	for (int col = 0; col < num_columns; col++) {
		for (int row = 0; row < num_triangles; row++) {
			colSum[col] += incentres[row][col];
		}
	}

	CG[0] = colSum[0] / num_triangles;
	CG[1] = colSum[1] / num_triangles;
	CG[2] = colSum[2] / num_triangles;

	return CG;
}