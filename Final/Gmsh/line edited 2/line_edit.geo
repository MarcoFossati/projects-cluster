//Points
Point(1) = {0, 0, 0, 1};
Point(2) = {30, 0, 0, 1};
Point(3) = {150, 0, 0, 1};
Point(4) = {0, 30, 0, 1};
Point(5) = {0, 150, 0, 1};
Point(6) = {0, -30, 0, 1};
Point(7) = {0, -150, 0, 1};

//Outer Circle
Circle(1) = {5, 1, 7}; Transfinite Line {1} = 19 Using Progression 1;

//Inner Circle
Circle(2) = {4, 1, 6}; Transfinite Line {2} = 19 Using Progression 1;

//Lines
Line(5) = {5, 4}; Transfinite Line {5} = 25 Using Progression 1;
Line(7) = {7, 6}; Transfinite Line {7} = 25 Using Progression 1;

//Surfaces
Line Loop(1) = {5, 2, -7, -1};
Plane Surface(1) = {1}; Transfinite Surface {1};

//Recombine Surfaces
Recombine Surface {1};

//Revolve
Extrude {{0, 1, 0}, {0, 0, 0}, Pi/2}{
Surface{1};Layers{12};
}