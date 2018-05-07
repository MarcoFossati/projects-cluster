//Points
Point(1) = {0, 0, 0, 1.0};
Point(2) = {30, 0, 0, 1.0};
Point(3) = {150, 0, 0, 1.0};
Point(4) = {-5.20944533, 29.54423259, 0, 1.0};
Point(5) = {-26.04722665, 147.721163, 0, 1.0};
Point(6) = {-5.20944533, -29.54423259, 0, 1.0};
Point(7) = {-26.04722665, -147.721163, 0, 1.0};
Point(8) = {5.20944533, 29.54423259, 0, 1.0};
Point(9) = {26.04722665, 147.721163, 0, 1.0};
Point(10) = {26.04722665, -147.721163, 0, 1.0};
Point(11) = {5.20944533, -29.54423259, 0, 1.0};
Point(12) = {-30, 0, 0, 1.0};
Point(13) = {-150, 0, 0, 1.0};

//Lines
Line(1) = {8, 9}; Transfinite Line {1} = 25 Using Progression 1;
Line(2) = {4, 5}; Transfinite Line {2} = 25 Using Progression 1;
Line(3) = {2, 3}; Transfinite Line {3} = 25 Using Progression 1;
Line(4) = {6, 7}; Transfinite Line {4} = 25 Using Progression 1;
Line(5) = {10,11}; Transfinite Line {5} = 25 Using Progression 1;
Line(6) = {12,13}; Transfinite Line {6} = 25 Using Progression 1;

//Cirlces
Circle(7) = {12, 1, 4}; Transfinite Line {7} = 9 Using Progression 1;
Circle(8) = {8, 1, 2}; Transfinite Line {8} = 9 Using Progression 1;
Circle(9) = {2, 1, 11}; Transfinite Line {9} = 9 Using Progression 1;
Circle(10) = {6, 1, 12}; Transfinite Line {10} = 9 Using Progression 1;
Circle(11) = {13, 1, 5}; Transfinite Line {11} = 9 Using Progression 1;
Circle(12) = {9, 1, 3}; Transfinite Line {12} = 9 Using Progression 1;
Circle(13) = {3, 1, 10}; Transfinite Line {13} = 9 Using Progression 1;
Circle(14) = {7, 1, 13}; Transfinite Line {14} = 9 Using Progression 1;

//Surfaces
Line Loop(1) = {7, 2, -11, -6};
Plane Surface(1) = {1}; Transfinite Surface {1};
Line Loop(2) = {1, 12, -3, -8};
Plane Surface(2) = {2}; Transfinite Surface {2};
Line Loop(3) = {13, 5, -9, 3};
Plane Surface(3) = {3}; Transfinite Surface {3};
Line Loop(4) = {6, -14, -4, 10};
Plane Surface(4) = {4}; Transfinite Surface {4};
