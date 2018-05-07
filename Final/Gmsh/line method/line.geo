SetFactory("OpenCASCADE");
Point(1) = {-150, 0, 0, 1.0};
//+
Point(2) = {150, 0, 0, 1.0};
//+
Point(3) = {0, -150, 0, 1.0};
//+
Point(4) = {0, 150, 0, 1.0};
//+
Point(5) = {-30, 0, 0, 1.0};
//+
Point(6) = {30, 0, 0, 1.0};
//+
Point(7) = {0, -30, 0, 1.0};
//+
Point(8) = {0, 30, 0, 1.0};
//+
Point(11) = {0, 0, 0, 1.0};
//+
Circle(1) = {3, 11, 2};
//+
Circle(2) = {2, 11, 4};
//+
Circle(3) = {4, 11, 1};
//+
Circle(4) = {1, 11, 3};
//+
Circle(5) = {7, 11, 6};
//+
Circle(6) = {6, 11, 8};
//+
Circle(7) = {8, 11, 5};
//+
Circle(8) = {5, 11, 7};
//+
Line(9) = {7, 3};
//+
Line(10) = {6, 2};
//+
Line(11) = {8, 4};
//+
Line(12) = {5, 1};
//+
Transfinite Line {5} = 10 Using Progression 1;
//+
Transfinite Line {6} = 10 Using Progression 1;
//+
Transfinite Line {7} = 10 Using Progression 1;
//+
Transfinite Line {8} = 10 Using Progression 1;
//+
Transfinite Line {1} = 10 Using Progression 1;
//+
Transfinite Line {2} = 10 Using Progression 1;
//+
Transfinite Line {3} = 10 Using Progression 1;
//+
Transfinite Line {4} = 10 Using Progression 1;
//+
Transfinite Line {9} = 25 Using Progression 1;
//+
Transfinite Line {10} = 25 Using Progression 1;
//+
Transfinite Line {11} = 25 Using Progression 1;
//+
Transfinite Line {12} = 25 Using Progression 1;
//+
Line Loop(1) = {9, 1, -10, -5};
//+
Plane Surface(1) = {1};
//+
Line Loop(2) = {10, 2, -11, -6};
//+
Plane Surface(2) = {2};
//+
Line Loop(3) = {11, 3, -12, -7};
//+
Plane Surface(3) = {3};
//+
Line Loop(4) = {12, 4, -9, -8};
//+
Plane Surface(4) = {4};
//+
Transfinite Surface {4};
//+
Transfinite Surface {1};
//+
Transfinite Surface {2};
//+
Transfinite Surface {3};
//+
Recombine Surface {4};
//+
Recombine Surface {1};
//+
Recombine Surface {2};
//+
Recombine Surface {3};
